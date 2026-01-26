import logging
import json
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

import pytest

from app.analysis_service import AnalysisService
from app.schemas import LLMAnalysisRequest
from app.settings import get_settings
from alpaca.data.historical import StockHistoricalDataClient

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class BacktestCase:
    id: str
    symbol: str
    description: str | None
    current_time_utc_iso: str | None
    range_start_utc_iso: str | None
    range_end_utc_iso: str | None
    mode: str
    expect: dict[str, Any]


def _parse_time_pst_to_utc_iso(s: str) -> str:
    dt = datetime.strptime(s, "%Y-%m-%d %H:%M").replace(tzinfo=ZoneInfo("America/Los_Angeles"))
    utc = dt.astimezone(ZoneInfo("UTC"))
    return utc.strftime("%Y-%m-%dT%H:%M:%SZ")


def _parse_time_utc_iso_to_dt(s: str) -> datetime:
    return datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=ZoneInfo("UTC"))


def _format_dt_to_utc_iso(dt: datetime) -> str:
    return dt.astimezone(ZoneInfo("UTC")).strftime("%Y-%m-%dT%H:%M:%SZ")


def _iter_utc_iso_minutes_inclusive(start_utc_iso: str, end_utc_iso: str) -> list[str]:
    start = _parse_time_utc_iso_to_dt(start_utc_iso)
    end = _parse_time_utc_iso_to_dt(end_utc_iso)
    if end < start:
        raise ValueError(f"range end before start: start={start_utc_iso} end={end_utc_iso}")
    out: list[str] = []
    cur = start
    while cur <= end:
        out.append(_format_dt_to_utc_iso(cur))
        cur = cur + timedelta(minutes=1)
    return out


def _load_cases() -> list[BacktestCase]:
    path = Path(__file__).resolve().parent / "fixtures" / "llm_backtest_cases.json"
    raw = json.loads(path.read_text(encoding="utf-8"))
    out: list[BacktestCase] = []
    for i, row in enumerate(raw):
        if not isinstance(row, dict):
            raise TypeError(f"case[{i}] must be object")
        case_id = str(row.get("id") or f"case_{i}")
        symbol = str(row.get("symbol") or "").strip().upper()
        if not symbol:
            raise ValueError(f"case[{i}] missing symbol")

        description_raw = row.get("description")
        description = str(description_raw).strip() if description_raw is not None else None
        if description == "":
            description = None

        mode = str(row.get("mode") or "playback").strip()

        utc_iso = row.get("current_time_utc_iso")
        time_pst = str(row.get("time_pst") or "").strip()
        time_range_pst = row.get("time_range_pst")
        time_pst_start = str(row.get("time_pst_start") or "").strip()
        time_pst_end = str(row.get("time_pst_end") or "").strip()

        has_single = bool(utc_iso) or bool(time_pst)
        has_range = bool(time_range_pst) or bool(time_pst_start) or bool(time_pst_end)
        if has_single and has_range:
            raise ValueError(f"case[{i}] cannot set both single time and time range")

        current_time: str | None = None
        range_start: str | None = None
        range_end: str | None = None

        if has_range:
            if (row.get("mode") is not None) and mode != "playback":
                raise ValueError(f"case[{i}] time range requires mode=playback (or omit mode)")
            mode = "playback"

            if time_range_pst is not None:
                if not isinstance(time_range_pst, dict):
                    raise TypeError(f"case[{i}] time_range_pst must be object")
                start_pst = str(time_range_pst.get("start") or "").strip()
                end_pst = str(time_range_pst.get("end") or "").strip()
            else:
                start_pst = time_pst_start
                end_pst = time_pst_end

            if not start_pst or not end_pst:
                raise ValueError(f"case[{i}] time range requires start/end (time_range_pst or time_pst_start/time_pst_end)")
            range_start = _parse_time_pst_to_utc_iso(start_pst)
            range_end = _parse_time_pst_to_utc_iso(end_pst)
        else:
            if utc_iso:
                current_time = str(utc_iso)
            else:
                if not time_pst:
                    raise ValueError(f"case[{i}] missing time_pst or current_time_utc_iso")
                current_time = _parse_time_pst_to_utc_iso(time_pst)

        expect = row.get("expect")
        if not isinstance(expect, dict):
            raise ValueError(f"case[{i}] expect must be object")
        out.append(
            BacktestCase(
                id=case_id,
                symbol=symbol,
                description=description,
                current_time_utc_iso=current_time,
                range_start_utc_iso=range_start,
                range_end_utc_iso=range_end,
                mode=mode,
                expect=expect,
            )
        )
    return out


def _eval_expect(expect: dict[str, Any], *, action: str, confidence: float) -> tuple[bool, str]:
    if expect.get("action_any") is True:
        return True, "action_any"

    if "action_is" in expect:
        want = str(expect["action_is"])
        ok = action == want
        return ok, f"action_is={want} actual={action}"

    if "action_not" in expect:
        bad = str(expect["action_not"])
        ok = action != bad
        return ok, f"action_not={bad} actual={action}"

    if "action_in" in expect:
        want = expect["action_in"]
        if not isinstance(want, list) or not all(isinstance(x, str) for x in want):
            return False, "action_in must be string[]"
        ok = action in set(want)
        return ok, f"action_in={want} actual={action}"

    if "confidence_gte" in expect:
        try:
            thr = float(expect["confidence_gte"])
        except Exception:
            return False, "confidence_gte must be number"
        ok = confidence >= thr
        return ok, f"confidence_gte={thr} actual={confidence}"

    if "confidence_lte" in expect:
        try:
            thr = float(expect["confidence_lte"])
        except Exception:
            return False, "confidence_lte must be number"
        ok = confidence <= thr
        return ok, f"confidence_lte={thr} actual={confidence}"

    return False, f"unsupported expect keys: {sorted(expect.keys())}"


@pytest.mark.asyncio
@pytest.mark.parametrize("case", _load_cases(), ids=lambda c: c.id)
async def test_llm_timestamp_backtest(case: BacktestCase, request):
    logger.info("case start: id=%s symbol=%s mode=%s description=%s", case.id, case.symbol, case.mode, case.description)
    settings = get_settings()
    assert (settings.alpaca_api_key or "").strip()
    assert (settings.alpaca_secret_key or "").strip()

    alpaca = StockHistoricalDataClient(settings.alpaca_api_key, settings.alpaca_secret_key)
    service = AnalysisService(alpaca)

    if case.current_time_utc_iso:
        logger.info("single time: %s", case.current_time_utc_iso)
        llm_req = LLMAnalysisRequest(
            symbol=case.symbol,
            current_time=case.current_time_utc_iso,
            mode=case.mode,
        )
        resp = await service.analyze_signal(llm_req)

        ok, detail = _eval_expect(case.expect, action=resp.action, confidence=float(resp.confidence))
        logger.info("single result: action=%s confidence=%.3f ok=%s detail=%s", resp.action, float(resp.confidence), ok, detail)
        result_row = {
            "id": case.id,
            "symbol": case.symbol,
            "description": case.description,
            "current_time_utc_iso": case.current_time_utc_iso,
            "mode": case.mode,
            "expect": case.expect,
            "actual": {"action": resp.action, "confidence": float(resp.confidence), "analysis_id": resp.analysis_id},
            "passed": bool(ok),
            "detail": detail,
            "reasoning": (resp.reasoning or "")[:2000],
        }
        request.config._llm_backtest_results.append(result_row)
        assert ok, detail
        return

    if not case.range_start_utc_iso or not case.range_end_utc_iso:
        raise AssertionError("BacktestCase must include either current_time_utc_iso or range_start_utc_iso/range_end_utc_iso")

    series = _iter_utc_iso_minutes_inclusive(case.range_start_utc_iso, case.range_end_utc_iso)
    logger.info("time range: start=%s end=%s total_samples=%d", case.range_start_utc_iso, case.range_end_utc_iso, len(series))
    if len(series) > 20:
        raise ValueError(
            f"time range has {len(series)} samples (>20). Split into multiple cases: "
            f"start={case.range_start_utc_iso} end={case.range_end_utc_iso}"
        )

    any_expect = case.expect.get("any")
    if not isinstance(any_expect, dict):
        raise ValueError("time range expect must include any: { ... }")

    attempts: list[dict[str, Any]] = []
    ok = False
    detail = ""
    matched: dict[str, Any] | None = None
    first_detail: str | None = None
    for idx, t in enumerate(series, start=1):
        llm_req = LLMAnalysisRequest(symbol=case.symbol, current_time=t, mode="playback")
        resp = await service.analyze_signal(llm_req)
        row = {
            "current_time_utc_iso": t,
            "action": resp.action,
            "confidence": float(resp.confidence),
            "analysis_id": resp.analysis_id,
            "reasoning": (resp.reasoning or "")[:300],
        }
        attempts.append(row)

        ok_i, detail_i = _eval_expect(any_expect, action=resp.action, confidence=float(resp.confidence))
        logger.info(
            "range sample %d/%d: t=%s action=%s confidence=%.3f ok=%s detail=%s",
            idx,
            len(series),
            t,
            resp.action,
            float(resp.confidence),
            ok_i,
            detail_i,
        )
        if ok_i:
            ok = True
            matched = {"current_time_utc_iso": t, "action": resp.action, "confidence": float(resp.confidence)}
            detail = f"any matched at {t} ({detail_i})"
            logger.info("range matched: t=%s action=%s confidence=%.3f", t, resp.action, float(resp.confidence))
            break
        if first_detail is None:
            first_detail = detail_i

    if not ok:
        detail = f"no sample matched expect.any (first_detail={first_detail})"
        logger.info("range no match: %s", detail)

    result_row = {
        "id": case.id,
        "symbol": case.symbol,
        "description": case.description,
        "range_start_utc_iso": case.range_start_utc_iso,
        "range_end_utc_iso": case.range_end_utc_iso,
        "mode": "playback",
        "expect": case.expect,
        "actual": {"matched": matched, "attempts": attempts, "total_samples": len(series), "attempted_samples": len(attempts)},
        "passed": bool(ok),
        "detail": detail,
    }
    request.config._llm_backtest_results.append(result_row)
    assert ok, detail
