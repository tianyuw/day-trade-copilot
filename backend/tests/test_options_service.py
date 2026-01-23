import asyncio
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from app.options_service import OptionChainService


class FakeAlpaca:
    def __init__(self) -> None:
        self.contracts_payload = {
            "option_contracts": [
                {"symbol": "META240123C0063000", "expiration_date": "2026-01-23", "type": "call", "strike_price": 630.0, "tradable": True, "status": "active"},
                {"symbol": "META240123P0063000", "expiration_date": "2026-01-23", "type": "put", "strike_price": 630.0, "tradable": True, "status": "active"},
                {"symbol": "META240130C0064000", "expiration_date": "2026-01-30", "type": "call", "strike_price": 640.0, "tradable": True, "status": "active"},
            ],
            "page_token": None,
        }
        self.chain_snapshots = {
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
        self.latest_quotes = {
            "META240123C0063000": {"bp": 3.05, "ap": 3.25, "t": "2026-01-22T19:16:00Z"},
            "META240123P0063000": {"bp": 2.55, "ap": 2.75, "t": "2026-01-22T19:16:00Z"},
        }

    async def get_option_contracts(self, underlying_symbols, **kwargs):
        return self.contracts_payload

    async def get_option_chain_snapshots(self, underlying_or_symbols, feed=None, page_token=None):
        return {"snapshots": self.chain_snapshots, "next_page_token": None}

    async def get_option_quotes(self, symbols, start=None, end=None, limit=1000):
        out = {}
        for s in symbols:
            out[s] = [
                {"bp": 3.0, "ap": 3.2, "t": "2026-01-22T19:14:00Z"},
                {"bp": 3.0, "ap": 3.2, "t": "2026-01-22T19:15:00Z"},
            ]
        return out

    async def get_option_bars(self, symbols, timeframe="1Min", start=None, end=None, limit=100):
        out = {}
        for s in symbols:
            out[s] = [
                {"t": "2026-01-22T19:10:00Z", "o": 2.9, "h": 3.0, "l": 2.8, "c": 2.95, "v": 10},
                {"t": "2026-01-22T19:15:00Z", "o": 3.0, "h": 3.2, "l": 3.0, "c": 3.1, "v": 20},
            ]
        return out

    async def get_bars(self, symbols, timeframe="1Min", start=None, end=None, limit=200):
        # Only used for underlying price; use a simple constant series
        from app.schemas import AlpacaBar

        sym = symbols[0]
        return {sym: [AlpacaBar(t="2026-01-22T19:15:00Z", o=630.0, h=631.0, l=629.0, c=630.5, v=1000)]}

    async def get_snapshots(self, symbols):
        sym = symbols[0]
        return {
            sym: {
                "latestQuote": {"bp": 630.0, "ap": 631.0},
            }
        }

    async def get_option_latest_quotes(self, symbols, feed=None):
        out = {}
        for s in symbols:
            if s in self.latest_quotes:
                out[s] = self.latest_quotes[s]
        return out


async def test_get_chain_realtime():
    client = OptionChainService(FakeAlpaca())
    chain = await client.get_chain_realtime("META", strikes_around_atm=1)
    assert chain["expiration"] == "2026-01-23"
    items = chain["items"]
    assert any(it["symbol"] == "META240123C0063000" for it in items)
    call = next(it for it in items if it["symbol"] == "META240123C0063000")
    assert call["quote"]["bid"] == 3.05
    assert call["quote"]["ask"] == 3.25
    print("test_get_chain_realtime passed")


async def test_get_chain_asof_with_bars():
    client = OptionChainService(FakeAlpaca())
    asof = "2026-01-22T19:15:00Z"
    chain = await client.get_chain_asof("META", asof=asof, strikes_around_atm=1, include_bars_minutes=10)
    items = chain["items"]
    call = next(it for it in items if it["symbol"] == "META240123C0063000")
    assert abs(call["asof_price"] - 3.1) < 1e-6
    assert "bars_1m" in call and len(call["bars_1m"]) >= 2
    print("test_get_chain_asof_with_bars passed")


async def main():
    await test_get_chain_realtime()
    await test_get_chain_asof_with_bars()
    print("All OptionChainService tests passed.")


if __name__ == "__main__":
    asyncio.run(main())
