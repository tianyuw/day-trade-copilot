import os
from datetime import datetime, timedelta

import pytest

from app.alpaca_client import AlpacaClient
from app.options_service import OptionChainService
from app.settings import get_settings


@pytest.mark.asyncio
async def test_option_chain_playback_prices_meta_20260123_0805pst():
    if os.getenv("RUN_ALPACA_INTEGRATION", "").strip().lower() not in {"1", "true", "yes"}:
        pytest.skip("set RUN_ALPACA_INTEGRATION=1 to run")

    try:
        settings = get_settings()
    except Exception as e:
        pytest.skip(str(e))

    alpaca = AlpacaClient(settings)
    svc = OptionChainService(alpaca)

    asof = "2026-01-23T16:05:00Z"
    chain = await svc.get_chain_asof(underlying="META", asof=asof, strikes_around_atm=5)

    exp = chain.get("expiration")
    assert exp == "2026-01-23"

    items = chain.get("items")
    assert isinstance(items, list)
    assert items

    asof_dt = datetime.fromisoformat(asof.replace("Z", "+00:00"))
    for it in items[:6]:
        assert isinstance(it, dict)
        sym = str(it.get("symbol") or "").strip().upper()
        asof_px = it.get("asof_price")
        asof_bar_time = it.get("asof_bar_time")

        assert sym
        assert asof_px is not None
        assert asof_bar_time

        assert datetime.fromisoformat(str(asof_bar_time).replace("Z", "+00:00")) <= asof_dt

        start = (asof_dt - timedelta(minutes=5)).isoformat().replace("+00:00", "Z")
        end = asof_dt.isoformat().replace("+00:00", "Z")
        payload = await alpaca.get_option_bars([sym], timeframe="1Min", start=start, end=end, limit=1000)
        rows = payload.get(sym) if isinstance(payload, dict) else None
        assert isinstance(rows, list) and rows

        rows_sorted = sorted([r for r in rows if isinstance(r, dict) and r.get("t")], key=lambda r: str(r.get("t")))
        assert rows_sorted
        last = rows_sorted[-1]
        assert datetime.fromisoformat(str(last.get("t")).replace("Z", "+00:00")) <= asof_dt

        assert float(asof_px) == pytest.approx(float(last.get("c")))
