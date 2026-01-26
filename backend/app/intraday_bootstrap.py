from __future__ import annotations

import os
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo


def _env_int(name: str, default: int) -> int:
    raw = os.getenv(name)
    if raw is None or raw == "":
        return default
    try:
        return int(raw)
    except Exception:
        return default


DEFAULT_CHART_WINDOW_MINUTES = _env_int("STREAM_CHART_WINDOW_MINUTES", 200)
DEFAULT_INDICATOR_WARMUP_MINUTES = _env_int("STREAM_INDICATOR_WARMUP_MINUTES", 21)
DEFAULT_PLAYBACK_FORWARD_CHUNK_MINUTES = _env_int("PLAYBACK_FORWARD_CHUNK_MINUTES", 300)
DEFAULT_PLAYBACK_PREFETCH_LOW_WATERMARK_MINUTES = _env_int("PLAYBACK_PREFETCH_LOW_WATERMARK_MINUTES", 30)


def analysis_keep_minutes(analysis_window_minutes: int) -> int:
    return max(int(analysis_window_minutes) + 50, 250)


def bootstrap_minutes(
    analysis_window_minutes: int,
    chart_window_minutes: int = DEFAULT_CHART_WINDOW_MINUTES,
    indicator_warmup_minutes: int = DEFAULT_INDICATOR_WARMUP_MINUTES,
) -> int:
    return max(int(chart_window_minutes), analysis_keep_minutes(analysis_window_minutes)) + int(indicator_warmup_minutes)


def parse_iso_z(ts: str) -> datetime:
    dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=ZoneInfo("UTC"))
    return dt.astimezone(ZoneInfo("UTC"))


def to_iso_z(dt: datetime) -> str:
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=ZoneInfo("UTC"))
    return dt.astimezone(ZoneInfo("UTC")).isoformat().replace("+00:00", "Z")


def playback_initial_fetch_window(
    *,
    start: str | None,
    analysis_window_minutes: int,
    requested_limit: int,
    chart_window_minutes: int = DEFAULT_CHART_WINDOW_MINUTES,
    indicator_warmup_minutes: int = DEFAULT_INDICATOR_WARMUP_MINUTES,
) -> tuple[str | None, str | None, int, int]:
    boot = bootstrap_minutes(
        analysis_window_minutes=analysis_window_minutes,
        chart_window_minutes=chart_window_minutes,
        indicator_warmup_minutes=indicator_warmup_minutes,
    )
    effective_limit = max(int(requested_limit), boot + 1)
    if not start:
        return None, None, effective_limit, boot

    start_dt = parse_iso_z(start)
    request_start = to_iso_z(start_dt - timedelta(minutes=boot))
    forward_minutes = max(effective_limit - boot, 0)
    request_end = to_iso_z(start_dt + timedelta(minutes=forward_minutes))
    return request_start, request_end, effective_limit, boot
