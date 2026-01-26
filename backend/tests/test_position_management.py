from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import pytest

from app.settings import get_settings
from app.analysis_service import AnalysisService
from app.schemas import PositionManagementRequest, PositionState, PositionOption, PositionEntry, PositionRisk
from alpaca.data.historical import StockHistoricalDataClient


def to_utc_iso(pst_dt: datetime) -> str:
    utc_dt = pst_dt.astimezone(ZoneInfo("UTC"))
    return utc_dt.strftime("%Y-%m-%dT%H:%M:%SZ")


@pytest.mark.asyncio
async def test_position_management_smoke():
    settings = get_settings()
    assert (settings.alpaca_api_key or "").strip()
    assert (settings.alpaca_secret_key or "").strip()

    alpaca = StockHistoricalDataClient(settings.alpaca_api_key, settings.alpaca_secret_key)
    service = AnalysisService(alpaca)

    pst_time = datetime(2026, 1, 22, 11, 15, 0, tzinfo=ZoneInfo("America/Los_Angeles"))
    bar_time = to_utc_iso(pst_time)

    entry_time = to_utc_iso(pst_time - timedelta(minutes=10))

    req = PositionManagementRequest(
        trade_id="demo_trade_001",
        symbol="NVDA",
        bar_time=bar_time,
        position=PositionState(
            direction="long",
            option=PositionOption(
                right="call",
                expiration="2026-01-23",
                strike=190.0,
            ),
            contracts_total=5,
            contracts_remaining=3,
            entry=PositionEntry(time=entry_time, premium=2.10),
            risk=PositionRisk(
                stop_loss_premium=1.40,
                take_profit_premium=3.20,
                time_stop_minutes=20,
            ),
        ),
        option_symbol=None,
        ohlcv_1m=None,
        mode="playback",
    )
    resp = await service.manage_position(req)
    assert (resp.trade_id or "").strip()
    assert resp.symbol == req.symbol
    assert resp.bar_time == req.bar_time
    assert resp.decision.action in {
        "hold",
        "close_all",
        "close_partial",
        "tighten_stop",
        "adjust_take_profit",
        "update_time_stop",
    }
