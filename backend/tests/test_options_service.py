import re
from datetime import datetime, timedelta, timezone

import pytest

from app.analysis_service import AnalysisService
from app.schemas import AlpacaBar, LLMAnalysisRequest


class _StubLLMBackend:
    model_name = "stub"

    def __init__(self) -> None:
        self.last_system_prompt: str | None = None
        self.last_user_content_text: str | None = None

    async def analyze_chart(self, *, system_prompt: str, user_content_text: str, chart_image_base64: str) -> str:
        self.last_system_prompt = system_prompt
        self.last_user_content_text = user_content_text
        return '{"action":"ignore","confidence":0.5,"reasoning":"stub"}'


class FakeAlpaca:
    def __init__(self) -> None:
        self._contracts = [
            {"symbol": "META240123C0063000", "expiration_date": "2026-01-23", "type": "call", "strike_price": 630.0, "tradable": True, "status": "active"},
            {"symbol": "META240123P0063000", "expiration_date": "2026-01-23", "type": "put", "strike_price": 630.0, "tradable": True, "status": "active"},
            {"symbol": "META240130C0064000", "expiration_date": "2026-01-30", "type": "call", "strike_price": 640.0, "tradable": True, "status": "active"},
        ]

        self._chain_snapshots = {
            "META240123C0063000": {
                "latestQuote": {"bp": 3.0, "ap": 3.2, "t": "2026-01-22T19:15:00Z"},
                "impliedVolatility": 0.45,
                "greeks": {"delta": 0.55},
                "latestTrade": {"p": 3.1},
            },
            "META240123P0063000": {
                "latestQuote": {"bp": 2.5, "ap": 2.7, "t": "2026-01-22T19:15:00Z"},
                "impliedVolatility": 0.52,
            },
        }

        self._latest_quotes = {
            "META240123C0063000": {"bp": 3.05, "ap": 3.25, "t": "2026-01-22T19:16:00Z"},
            "META240123P0063000": {"bp": 2.55, "ap": 2.75, "t": "2026-01-22T19:16:00Z"},
        }

    async def get_option_contracts(self, underlying_symbols, **kwargs):
        gte = kwargs.get("expiration_date_gte")
        lte = kwargs.get("expiration_date_lte")

        def in_range(exp: str) -> bool:
            if gte and exp < str(gte):
                return False
            if lte and exp > str(lte):
                return False
            return True

        contracts = [c for c in self._contracts if in_range(str(c.get("expiration_date")))]
        return {"option_contracts": contracts, "page_token": None}

    async def get_option_chain_snapshots(self, underlying_or_symbols, feed=None, page_token=None):
        return {"snapshots": self._chain_snapshots, "next_page_token": None}

    async def get_option_quotes(self, symbols, start=None, end=None, limit=1000):
        out = {}
        for s in symbols:
            out[s] = [
                {"bp": 3.0, "ap": 3.2, "t": "2026-01-22T19:14:00Z"},
                {"bp": 3.0, "ap": 3.2, "t": "2026-01-22T19:15:00Z"},
            ]
        return out

    async def get_bars(self, symbols, timeframe="1Min", start=None, end=None, limit=200):
        sym = str(symbols[0]).upper()
        if timeframe == "1Day":
            base = datetime(2025, 11, 1, tzinfo=timezone.utc)
            bars = []
            for i in range(60):
                t = (base + timedelta(days=i)).strftime("%Y-%m-%dT%H:%M:%SZ")
                px = 600.0 + i * 0.1
                bars.append(AlpacaBar(t=t, o=px, h=px + 1, l=px - 1, c=px, v=100000))
            return {sym: bars}

        end_dt = datetime.fromisoformat(str(end).replace("Z", "+00:00")) if end else datetime(2026, 1, 22, 19, 15, tzinfo=timezone.utc)
        start_dt = end_dt - timedelta(minutes=300)
        bars = []
        cur = start_dt
        px = 630.0
        while cur <= end_dt:
            t = cur.strftime("%Y-%m-%dT%H:%M:%SZ")
            bars.append(AlpacaBar(t=t, o=px, h=px + 0.5, l=px - 0.5, c=px + 0.1, v=1000))
            cur += timedelta(minutes=1)
        return {sym: bars[-limit:]}

    async def get_snapshots(self, symbols):
        sym = str(symbols[0]).upper()
        return {sym: {"latestQuote": {"bp": 630.0, "ap": 631.0}}}

    async def get_option_latest_quotes(self, symbols, feed=None):
        out = {}
        for s in symbols:
            if s in self._latest_quotes:
                out[s] = self._latest_quotes[s]
        return out


def _extract_nearest_expiration(user_content_text: str) -> str:
    m = re.search(r"Option Chain \(Nearest Expiration: (\d{4}-\d{2}-\d{2})", user_content_text)
    assert m, "missing Option Chain (Nearest Expiration: ...) in user prompt"
    return m.group(1)


@pytest.mark.asyncio
async def test_prompt_includes_option_chain_realtime():
    alpaca = FakeAlpaca()
    service = AnalysisService(alpaca)
    stub = _StubLLMBackend()
    service.llm_client.client = stub

    req = LLMAnalysisRequest(symbol="META", current_time="2026-01-22T19:15:00Z", mode="realtime")
    await service.analyze_signal(req)

    assert stub.last_user_content_text is not None
    exp = _extract_nearest_expiration(stub.last_user_content_text)
    assert exp == "2026-01-23"


@pytest.mark.asyncio
async def test_prompt_includes_option_chain_playback_nearest_expiration():
    alpaca = FakeAlpaca()
    service = AnalysisService(alpaca)
    stub = _StubLLMBackend()
    service.llm_client.client = stub

    req = LLMAnalysisRequest(symbol="META", current_time="2026-01-22T19:15:00Z", mode="playback")
    await service.analyze_signal(req)

    assert stub.last_user_content_text is not None
    exp = _extract_nearest_expiration(stub.last_user_content_text)
    assert exp == "2026-01-23"
