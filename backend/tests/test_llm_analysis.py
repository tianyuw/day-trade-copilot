from datetime import datetime
from zoneinfo import ZoneInfo
import pytest

from app.settings import get_settings
from app.analysis_service import AnalysisService
from app.schemas import LLMAnalysisRequest
from alpaca.data.historical import StockHistoricalDataClient


def _to_utc_iso(pst_time: datetime) -> str:
    utc_time = pst_time.astimezone(ZoneInfo("UTC"))
    return utc_time.strftime("%Y-%m-%dT%H:%M:%SZ")


@pytest.mark.asyncio
async def test_llm_analysis_smoke():
    settings = get_settings()
    assert (settings.alpaca_api_key or "").strip()
    assert (settings.alpaca_secret_key or "").strip()

    alpaca = StockHistoricalDataClient(settings.alpaca_api_key, settings.alpaca_secret_key)
    service = AnalysisService(alpaca)

    pst_time = datetime(2026, 1, 16, 7, 3, 0, tzinfo=ZoneInfo("America/Los_Angeles"))
    utc_iso = _to_utc_iso(pst_time)
    request = LLMAnalysisRequest(
        symbol="NVDA",
        current_time=utc_iso,
        mode="playback",
    )

    response = await service.analyze_signal(request)
    assert response.symbol == "NVDA"
    assert response.timestamp == utc_iso
    assert response.action in {"buy_long", "buy_short", "ignore", "follow_up", "check_when_condition_meet"}
