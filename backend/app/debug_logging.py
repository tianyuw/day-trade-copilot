from __future__ import annotations

import json
import os
import re
import time
import uuid
import base64
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def _utc_now_compact() -> tuple[str, str]:
    dt = datetime.now(timezone.utc)
    return dt.strftime("%Y-%m-%d"), dt.strftime("%H%M%SZ")


def is_debug_log_enabled() -> bool:
    v = (os.getenv("OUTPUT_DEBUG_LOG") or "").strip().lower()
    return v in {"1", "true", "yes", "y", "on"}


def get_debug_log_dir() -> Path:
    raw = (os.getenv("DEBUG_LOG_DIR") or "./logs").strip()
    p = Path(raw)
    if p.is_absolute():
        return p
    backend_root = Path(__file__).resolve().parents[1]
    return backend_root / p


_SAFE_RE = re.compile(r"[^a-zA-Z0-9._-]+")


def _safe_token(s: str) -> str:
    s = (s or "").strip()
    s = _SAFE_RE.sub("_", s)
    return s[:80] if len(s) > 80 else s


@dataclass(frozen=True)
class LLMExchangeMeta:
    kind: str
    model: str | None = None
    symbol: str | None = None
    analysis_id: str | None = None
    trade_id: str | None = None
    current_time: str | None = None
    bar_time: str | None = None


def write_llm_exchange(
    *,
    meta: LLMExchangeMeta,
    system_prompt: str,
    user_prompt: str,
    chart_image_base64: str | None,
    response_raw: str | None,
    parsed_json: dict[str, Any] | None,
    error: str | None,
    duration_ms: int | None,
) -> Path | None:
    if not is_debug_log_enabled():
        return None

    day, ts = _utc_now_compact()
    base_dir = get_debug_log_dir() / "llm" / _safe_token(meta.kind) / day
    base_dir.mkdir(parents=True, exist_ok=True)

    id_part = (
        _safe_token(meta.analysis_id)
        or _safe_token(meta.trade_id)
        or _safe_token(meta.symbol)
        or "unknown"
    )
    symbol_part = _safe_token(meta.symbol or "unknown")
    fname = f"{ts}_{symbol_part}_{id_part}_{uuid.uuid4().hex[:8]}.json"
    path = base_dir / fname

    payload: dict[str, Any] = {
        "timestamp_utc": f"{day}T{ts.replace('Z','')}Z",
        "kind": meta.kind,
        "model": meta.model,
        "symbol": meta.symbol,
        "analysis_id": meta.analysis_id,
        "trade_id": meta.trade_id,
        "current_time": meta.current_time,
        "bar_time": meta.bar_time,
        "duration_ms": duration_ms,
        "system_prompt": system_prompt,
        "user_prompt": user_prompt,
        "response_raw": response_raw,
        "parsed_json": parsed_json,
        "error": error,
    }

    tmp_path = path.with_suffix(".tmp")
    with open(tmp_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    os.replace(tmp_path, path)
    _maybe_write_chart_image(path, chart_image_base64)
    return path


def _maybe_write_chart_image(json_path: Path, chart_image_base64: str | None) -> None:
    if not chart_image_base64:
        return
    try:
        b64 = chart_image_base64.strip()
        if b64.startswith("data:"):
            comma = b64.find(",")
            if comma != -1:
                b64 = b64[comma + 1 :]
        img_bytes = base64.b64decode(b64, validate=False)
        img_path = json_path.with_suffix(".png")
        tmp_path = img_path.with_suffix(".tmp")
        with open(tmp_path, "wb") as f:
            f.write(img_bytes)
        os.replace(tmp_path, img_path)
    except Exception:
        return


class Stopwatch:
    def __init__(self) -> None:
        self._t0 = time.monotonic()

    def elapsed_ms(self) -> int:
        return int((time.monotonic() - self._t0) * 1000)
