from __future__ import annotations

import asyncio
from datetime import datetime
from typing import Any, Literal, Callable, Awaitable

import pandas as pd

from .schemas import (
    LLMAnalysisRequest,
    PositionManagementRequest,
    PositionManagementResponse,
    TriggerReason,
    StreamAnalysisMessage,
    StreamPositionMessage,
    StreamStateMessage,
)
from .trade_session import TradeState, SymbolSession


StreamMode = Literal["realtime", "playback"]


def _to_epoch_seconds(iso: str) -> int:
    if not iso:
        return 0
    try:
        dt = datetime.fromisoformat(iso.replace("Z", "+00:00"))
        return int(dt.timestamp())
    except Exception:
        return 0


def to_daily_df(daily_list: list[Any]) -> pd.DataFrame | None:
    df = pd.DataFrame([b.model_dump() if hasattr(b, "model_dump") else b for b in (daily_list or [])])
    if df.empty:
        return None
    df["timestamp"] = pd.to_datetime(df["t"])
    df.set_index("timestamp", inplace=True)
    df.rename(columns={"o": "open", "h": "high", "l": "low", "c": "close", "v": "volume"}, inplace=True)
    df.sort_index(inplace=True)
    return df


def to_intraday_df(bars: list[Any], symbol: str) -> pd.DataFrame | None:
    df = pd.DataFrame([b.model_dump() if hasattr(b, "model_dump") else b for b in (bars or [])])
    if df.empty:
        return None
    df["timestamp"] = pd.to_datetime(df["t"])
    df.set_index("timestamp", inplace=True)
    df.rename(columns={"o": "open", "h": "high", "l": "low", "c": "close", "v": "volume"}, inplace=True)
    df["symbol"] = symbol
    if "indicators" in df.columns:
        df.drop(columns=["indicators"], inplace=True)
    df.sort_index(inplace=True)
    return df


async def send_state(
    ws: Any,
    *,
    session: SymbolSession,
    mode: StreamMode,
    last_state_sent: dict[str, tuple[str, int | None]],
) -> None:
    in_pos = bool(session.trade and session.state == TradeState.IN_POSITION and session.trade.contracts_remaining > 0)
    rem = session.trade.contracts_remaining if session.trade else None
    key = (session.state.value, rem if isinstance(rem, int) else None)
    if last_state_sent.get(session.symbol) == key:
        return
    last_state_sent[session.symbol] = key
    try:
        await ws.send_json(
            StreamStateMessage(
                type="state",
                mode=mode,
                symbol=session.symbol,
                state=session.state.value,
                in_position=in_pos,
                contracts_total=session.trade.contracts_total if session.trade else None,
                contracts_remaining=rem,
                trade_id=session.trade.trade_id if session.trade else None,
                option=session.trade.option if session.trade else None,
                option_symbol=session.trade.option_symbol if session.trade else None,
            ).model_dump()
        )
    except Exception:
        return


def maybe_trigger_analysis(
    *,
    session: SymbolSession,
    bar: Any,
    has_quant_signal: bool,
    last_analyzed_time: dict[str, str],
) -> TriggerReason | None:
    bar_t = str(getattr(bar, "t", "") or "")
    if not bar_t:
        return None
    if session.analysis_inflight:
        return None
    if last_analyzed_time.get(session.symbol) == bar_t:
        return None

    if session.watches:
        hit = None
        try:
            close_px = float(getattr(bar, "c", 0.0))
            for w in sorted(session.watches, key=lambda x: x.created_at_epoch_s):
                if w.direction == "above" and close_px >= w.trigger_price:
                    hit = w
                    break
                if w.direction == "below" and close_px <= w.trigger_price:
                    hit = w
                    break
        except Exception:
            hit = None
        if hit is not None:
            session.watches = [w for w in session.watches if w is not hit]
            last_analyzed_time[session.symbol] = bar_t
            return "watch_condition"

    if session.state == TradeState.FOLLOW_UP_PENDING and session.follow_up.armed:
        if not has_quant_signal:
            session.follow_up = session.follow_up.__class__(armed=False)
            last_analyzed_time[session.symbol] = bar_t
            return "follow_up"

    if has_quant_signal:
        last_analyzed_time[session.symbol] = bar_t
        return "quant_signal"

    return None


async def run_analysis(
    ws: Any,
    *,
    mode: StreamMode,
    sem: asyncio.Semaphore,
    analysis_service: Any,
    option_chain_service: Any,
    session: SymbolSession,
    bar_time: str,
    trigger_reason: TriggerReason | None,
    intraday_df: pd.DataFrame | None,
    daily_df: pd.DataFrame | None,
    last_state_sent: dict[str, tuple[str, int | None]],
    after_analysis: Callable[[Any, dict[str, Any], str | None], Awaitable[None] | None] | None = None,
) -> dict[str, Any] | None:
    if session.analysis_inflight:
        return None
    if intraday_df is None or intraday_df.empty:
        return None

    payload_out: dict[str, Any] | None = None
    option_symbol_out: str | None = None

    async with sem:
        session.analysis_inflight = True
        session.state = TradeState.AI_VERIFY
        await send_state(ws, session=session, mode=mode, last_state_sent=last_state_sent)
        try:
            analysis_req = LLMAnalysisRequest(symbol=session.symbol, current_time=bar_time, mode=mode)
            llm_res = await analysis_service.analyze_signal(
                analysis_req,
                preloaded_daily_bars=daily_df,
                preloaded_intraday_bars=intraday_df,
            )
            payload = llm_res.model_dump()
            session.on_analysis_result(payload)

            if payload.get("action") in ("buy_long", "buy_short") and isinstance(payload.get("trade_plan"), dict):
                plan = payload.get("trade_plan") or {}
                opt = plan.get("option") if isinstance(plan.get("option"), dict) else {}
                option_symbol: str | None = None
                try:
                    exp = str(opt.get("expiration") or "")
                    right = str(opt.get("right") or "").lower()
                    strike = float(opt.get("strike") or 0.0)
                    if exp and right and strike:
                        contracts = await option_chain_service.get_contracts(
                            session.symbol,
                            asof_date=None,
                            expiration_date_gte=exp,
                            expiration_date_lte=exp,
                            limit=1000,
                        )
                        best_sym: str | None = None
                        best_diff: float | None = None
                        for c in contracts:
                            try:
                                if str(c.get("type") or "").lower() != right:
                                    continue
                                if str(c.get("expiration_date") or "") != exp:
                                    continue
                                diff = abs(float(c.get("strike_price") or 0.0) - strike)
                                s2 = str(c.get("symbol") or "").upper()
                                if not s2:
                                    continue
                                if best_diff is None or diff < best_diff:
                                    best_diff = diff
                                    best_sym = s2
                            except Exception:
                                continue
                        if best_sym and (best_diff is None or best_diff <= 5.0):
                            option_symbol = best_sym
                except Exception:
                    option_symbol = None

                option_symbol_out = option_symbol
                if llm_res.trade_plan is not None:
                    try:
                        llm_res = llm_res.model_copy(
                            update={"trade_plan": llm_res.trade_plan.model_copy(update={"option_symbol": option_symbol})}
                        )
                    except Exception:
                        pass
                try:
                    payload = llm_res.model_dump()
                except Exception:
                    pass
                session.enter_from_trade_plan(payload, option_symbol=option_symbol)

            try:
                await ws.send_json(
                    StreamAnalysisMessage(
                        type="analysis",
                        mode=mode,
                        symbol=session.symbol,
                        trigger_reason=trigger_reason,
                        result=llm_res,
                    ).model_dump()
                )
            except Exception:
                return None

            payload_out = payload

            if after_analysis is not None and payload_out is not None:
                res = after_analysis(llm_res, payload_out, option_symbol_out)
                if asyncio.iscoroutine(res):
                    await res
        finally:
            session.analysis_inflight = False
            if session.state == TradeState.AI_VERIFY:
                session.state = TradeState.SCAN
            await send_state(ws, session=session, mode=mode, last_state_sent=last_state_sent)

    return payload_out


async def run_manage_position(
    ws: Any,
    *,
    mode: StreamMode,
    sem: asyncio.Semaphore,
    analysis_service: Any,
    session: SymbolSession,
    bar_time: str,
    ohlcv_1m: list[dict[str, Any]] | None,
    last_state_sent: dict[str, tuple[str, int | None]],
    after_position: Callable[[Any, dict[str, Any]], Awaitable[None] | None] | None = None,
) -> dict[str, Any] | None:
    if not session.trade:
        return None
    if session.manage_inflight:
        return None

    try:
        total_minutes = int(session.trade.risk.get("time_stop_minutes") or 0)
    except Exception:
        total_minutes = 0
    if total_minutes > 0:
        entry_epoch = _to_epoch_seconds(str(session.trade.entry_time or ""))
        bar_epoch = _to_epoch_seconds(str(bar_time or ""))
        if entry_epoch > 0 and bar_epoch >= entry_epoch and (bar_epoch - entry_epoch) >= total_minutes * 60:
            pm_res = PositionManagementResponse(
                trade_id=session.trade.trade_id,
                analysis_id=f"time_stop:{session.trade.trade_id}",
                timestamp=bar_time,
                symbol=session.symbol,
                bar_time=bar_time,
                decision={
                    "action": "close_all",
                    "reasoning": (
                        "Time stop hit: "
                        f"entry_time={session.trade.entry_time}, bar_time={bar_time}, "
                        f"elapsed_minutes={(bar_epoch - entry_epoch) // 60}, "
                        f"time_stop_minutes={total_minutes}"
                    ),
                    "exit": None,
                    "adjustments": None,
                },
                position_option_quote=None,
                option_symbol=session.trade.option_symbol,
            )
            await ws.send_json(
                StreamPositionMessage(
                    type="position",
                    mode=mode,
                    symbol=session.symbol,
                    trigger_reason="position_management",
                    result=pm_res,
                ).model_dump()
            )
            payload_out = pm_res.model_dump()
            session.on_position_decision(payload_out)
            if after_position is not None:
                res = after_position(pm_res, payload_out)
                if asyncio.iscoroutine(res):
                    await res
            await send_state(ws, session=session, mode=mode, last_state_sent=last_state_sent)
            return payload_out

    payload_out: dict[str, Any] | None = None

    async with sem:
        session.manage_inflight = True
        try:
            req_pm = PositionManagementRequest(
                trade_id=session.trade.trade_id,
                symbol=session.symbol,
                bar_time=bar_time,
                mode=mode,
                position={
                    "direction": session.trade.direction,
                    "option": session.trade.option,
                    "contracts_total": session.trade.contracts_total,
                    "contracts_remaining": session.trade.contracts_remaining,
                    "entry": {"time": session.trade.entry_time, "premium": session.trade.entry_premium},
                    "risk": {
                        "stop_loss_premium": session.trade.risk.get("stop_loss_premium"),
                        "take_profit_premium": session.trade.risk.get("take_profit_premium"),
                        "time_stop_minutes": session.trade.risk.get("time_stop_minutes"),
                    },
                },
                option_symbol=session.trade.option_symbol,
                ohlcv_1m=ohlcv_1m,
            )
            pm_res = await analysis_service.manage_position(req_pm)
            await ws.send_json(
                StreamPositionMessage(
                    type="position",
                    mode=mode,
                    symbol=session.symbol,
                    trigger_reason="position_management",
                    result=pm_res,
                ).model_dump()
            )
            payload_out = pm_res.model_dump()
            session.on_position_decision(payload_out)
            if after_position is not None and payload_out is not None:
                res = after_position(pm_res, payload_out)
                if asyncio.iscoroutine(res):
                    await res
        finally:
            session.manage_inflight = False
            await send_state(ws, session=session, mode=mode, last_state_sent=last_state_sent)

    return payload_out
