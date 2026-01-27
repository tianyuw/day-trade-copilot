from __future__ import annotations

import asyncio
import json
from datetime import datetime, timedelta, timezone
from typing import AsyncIterator, Iterable

import httpx
import websockets

from .schemas import AlpacaBar
from .settings import Settings


class AlpacaClient:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings

    @property
    def _headers(self) -> dict[str, str]:
        return {
            "APCA-API-KEY-ID": self._settings.alpaca_api_key,
            "APCA-API-SECRET-KEY": self._settings.alpaca_secret_key,
        }

    async def get_bars(
        self,
        symbols: list[str],
        timeframe: str = "1Min",
        start: str | None = None,
        end: str | None = None,
        limit: int = 1000,
    ) -> dict[str, list[AlpacaBar]]:
        symbols = [s.strip().upper() for s in symbols if s.strip()]
        now = datetime.now(timezone.utc)
        if start is None:
            start = (now - timedelta(days=7)).isoformat().replace("+00:00", "Z")

        if len(symbols) > 1:
            async def fetch_one(sym: str) -> tuple[str, list[AlpacaBar]]:
                data = await self.get_bars([sym], timeframe=timeframe, start=start, end=end, limit=limit)
                return sym, data.get(sym, [])

            pairs = await asyncio.gather(*[fetch_one(s) for s in symbols])
            return {sym: bars for sym, bars in pairs}

        request_limit = min(10000, max(1, limit))

        params = {
            "symbols": ",".join(symbols),
            "timeframe": timeframe,
            "feed": self._settings.alpaca_feed,
            "limit": str(request_limit),
            "start": start,
        }
        if end:
            params["end"] = end

        url = f"{self._settings.alpaca_data_base_url}/stocks/bars"
        bars_by_symbol: dict[str, list[AlpacaBar]] = {s: [] for s in symbols}
        page_token: str | None = None

        async with httpx.AsyncClient(timeout=30.0) as client:
            for _ in range(10):
                if page_token:
                    params["page_token"] = page_token
                else:
                    params.pop("page_token", None)

                r = await client.get(url, headers=self._headers, params=params)
                r.raise_for_status()
                payload = r.json()

                raw = payload.get("bars", {}) or {}
                for sym, bars in raw.items():
                    if sym not in bars_by_symbol:
                        bars_by_symbol[sym] = []
                    bars_by_symbol[sym].extend([AlpacaBar.model_validate(b) for b in (bars or [])])

                page_token = payload.get("next_page_token")
                if not page_token:
                    break
                if all(len(bars_by_symbol.get(s, [])) >= limit for s in symbols):
                    break

        for sym in list(bars_by_symbol.keys()):
            bars = bars_by_symbol[sym]
            bars.sort(key=lambda b: b.t)
            if len(bars) > limit:
                bars_by_symbol[sym] = bars[-limit:]

        return bars_by_symbol

    async def get_snapshots(self, symbols: list[str]) -> dict:
        params = {"symbols": ",".join(symbols), "feed": self._settings.alpaca_feed}
        url = f"{self._settings.alpaca_data_base_url}/stocks/snapshots"
        async with httpx.AsyncClient(timeout=30.0) as client:
            r = await client.get(url, headers=self._headers, params=params)
            r.raise_for_status()
            return r.json()

    async def get_clock(self) -> dict:
        url = f"{self._settings.alpaca_trading_base_url}/v2/clock"
        async with httpx.AsyncClient(timeout=10.0) as client:
            r = await client.get(url, headers=self._headers)
            r.raise_for_status()
            return r.json()

    async def get_assets(self, status: str = "active", asset_class: str = "us_equity") -> list[dict]:
        params = {"status": status, "asset_class": asset_class}
        url = f"{self._settings.alpaca_trading_base_url}/v2/assets"
        async with httpx.AsyncClient(timeout=30.0) as client:
            r = await client.get(url, headers=self._headers, params=params)
            r.raise_for_status()
            data = r.json()
            if isinstance(data, list):
                return data
            return []

    def _trading_base_and_headers(self, execution: str) -> tuple[str, dict[str, str]]:
        ex = str(execution or "paper").strip().lower()
        if ex == "live":
            if not self._settings.alpaca_live_api_key or not self._settings.alpaca_live_secret_key:
                raise RuntimeError("Live trading credentials are not configured")
            return (
                self._settings.alpaca_trading_base_url_live,
                {
                    "APCA-API-KEY-ID": self._settings.alpaca_live_api_key,
                    "APCA-API-SECRET-KEY": self._settings.alpaca_live_secret_key,
                },
            )
        return (
            self._settings.alpaca_trading_base_url_paper,
            {
                "APCA-API-KEY-ID": self._settings.alpaca_paper_api_key,
                "APCA-API-SECRET-KEY": self._settings.alpaca_paper_secret_key,
            },
        )

    async def get_account(self, execution: str = "paper") -> dict:
        base, headers = self._trading_base_and_headers(execution)
        url = f"{base}/v2/account"
        async with httpx.AsyncClient(timeout=30.0) as client:
            r = await client.get(url, headers=headers)
            r.raise_for_status()
            return r.json()

    async def get_portfolio_history(
        self,
        execution: str = "paper",
        period: str | None = None,
        timeframe: str | None = None,
        date_end: str | None = None,
        extended_hours: bool | None = None,
    ) -> dict:
        base, headers = self._trading_base_and_headers(execution)
        url = f"{base}/v2/account/portfolio/history"
        params: dict[str, str] = {}
        if period:
            params["period"] = str(period)
        if timeframe:
            params["timeframe"] = str(timeframe)
        if date_end:
            params["date_end"] = str(date_end)
        if extended_hours is not None:
            params["extended_hours"] = "true" if extended_hours else "false"
        async with httpx.AsyncClient(timeout=30.0) as client:
            r = await client.get(url, headers=headers, params=params or None)
            r.raise_for_status()
            return r.json()

    async def list_positions(self, execution: str = "paper") -> list[dict]:
        base, headers = self._trading_base_and_headers(execution)
        url = f"{base}/v2/positions"
        async with httpx.AsyncClient(timeout=30.0) as client:
            r = await client.get(url, headers=headers)
            r.raise_for_status()
            data = r.json()
            return data if isinstance(data, list) else []

    async def get_position(self, symbol: str, execution: str = "paper") -> dict:
        base, headers = self._trading_base_and_headers(execution)
        url = f"{base}/v2/positions/{symbol}"
        async with httpx.AsyncClient(timeout=30.0) as client:
            r = await client.get(url, headers=headers)
            r.raise_for_status()
            return r.json()

    async def close_position(
        self,
        symbol: str,
        execution: str = "paper",
        qty: str | None = None,
        percentage: str | None = None,
    ) -> dict:
        base, headers = self._trading_base_and_headers(execution)
        url = f"{base}/v2/positions/{symbol}"
        params: dict[str, str] = {}
        if qty is not None:
            params["qty"] = str(qty)
        if percentage is not None:
            params["percentage"] = str(percentage)
        async with httpx.AsyncClient(timeout=30.0) as client:
            r = await client.delete(url, headers=headers, params=params or None)
            r.raise_for_status()
            return r.json()

    async def close_all_positions(self, execution: str = "paper") -> list[dict]:
        base, headers = self._trading_base_and_headers(execution)
        url = f"{base}/v2/positions"
        async with httpx.AsyncClient(timeout=30.0) as client:
            r = await client.delete(url, headers=headers)
            r.raise_for_status()
            data = r.json()
            return data if isinstance(data, list) else []

    async def submit_order(self, payload: dict, execution: str = "paper") -> dict:
        base, headers = self._trading_base_and_headers(execution)
        url = f"{base}/v2/orders"
        async with httpx.AsyncClient(timeout=30.0) as client:
            r = await client.post(url, headers=headers, json=payload)
            r.raise_for_status()
            return r.json()

    async def list_orders(self, execution: str = "paper", params: dict | None = None) -> list[dict]:
        base, headers = self._trading_base_and_headers(execution)
        url = f"{base}/v2/orders"
        async with httpx.AsyncClient(timeout=30.0) as client:
            r = await client.get(url, headers=headers, params=params or None)
            r.raise_for_status()
            data = r.json()
            return data if isinstance(data, list) else []

    async def get_order(self, order_id: str, execution: str = "paper") -> dict:
        base, headers = self._trading_base_and_headers(execution)
        url = f"{base}/v2/orders/{order_id}"
        async with httpx.AsyncClient(timeout=30.0) as client:
            r = await client.get(url, headers=headers)
            r.raise_for_status()
            return r.json()

    async def cancel_order(self, order_id: str, execution: str = "paper") -> None:
        base, headers = self._trading_base_and_headers(execution)
        url = f"{base}/v2/orders/{order_id}"
        async with httpx.AsyncClient(timeout=30.0) as client:
            r = await client.delete(url, headers=headers)
            r.raise_for_status()
            return None

    async def cancel_all_orders(self, execution: str = "paper") -> list[dict]:
        base, headers = self._trading_base_and_headers(execution)
        url = f"{base}/v2/orders"
        async with httpx.AsyncClient(timeout=30.0) as client:
            r = await client.delete(url, headers=headers)
            r.raise_for_status()
            data = r.json()
            return data if isinstance(data, list) else []

    async def replace_order(self, order_id: str, payload: dict, execution: str = "paper") -> dict:
        base, headers = self._trading_base_and_headers(execution)
        url = f"{base}/v2/orders/{order_id}"
        async with httpx.AsyncClient(timeout=30.0) as client:
            r = await client.patch(url, headers=headers, json=payload)
            r.raise_for_status()
            return r.json()

    async def list_account_activities(self, execution: str = "paper", params: dict | None = None) -> list[dict]:
        base, headers = self._trading_base_and_headers(execution)
        url = f"{base}/v2/account/activities"
        async with httpx.AsyncClient(timeout=30.0) as client:
            r = await client.get(url, headers=headers, params=params or None)
            r.raise_for_status()
            data = r.json()
            return data if isinstance(data, list) else []

    async def get_option_contracts(
        self,
        underlying_symbols: list[str],
        status: str | None = None,
        expiration_date_lte: str | None = None,
        expiration_date_gte: str | None = None,
        limit: int = 100,
        page_token: str | None = None,
    ) -> dict:
        underlyings = [s.strip().upper() for s in underlying_symbols if s.strip()]
        params: dict[str, str] = {"underlying_symbols": ",".join(underlyings), "limit": str(limit)}
        if status:
            q_status = str(status).strip().lower()
            if q_status in {"active", "inactive"}:
                params["status"] = q_status
        if expiration_date_lte:
            params["expiration_date_lte"] = expiration_date_lte
        if expiration_date_gte:
            params["expiration_date_gte"] = expiration_date_gte
        if page_token:
            params["page_token"] = page_token

        url = f"{self._settings.alpaca_trading_base_url}/v2/options/contracts"
        async with httpx.AsyncClient(timeout=30.0) as client:
            r = await client.get(url, headers=self._headers, params=params)
            r.raise_for_status()
            return r.json()

    async def get_option_chain_snapshots(
        self,
        underlying_or_symbols: str,
        feed: str | None = None,
        page_token: str | None = None,
    ) -> dict:
        q_feed = (feed or self._settings.alpaca_options_feed or "").strip().lower() or "indicative"
        if q_feed not in {"indicative", "opra"}:
            q_feed = "indicative"
        params = {"feed": q_feed}
        if page_token:
            params["page_token"] = page_token
        target = str(underlying_or_symbols).strip().upper()
        url = f"{self._settings.alpaca_options_data_base_url}/options/snapshots/{target}"
        async with httpx.AsyncClient(timeout=30.0) as client:
            r = await client.get(url, headers=self._headers, params=params)
            r.raise_for_status()
            data = r.json()
            if isinstance(data, dict):
                return data
            return {}

    async def get_option_bars(
        self,
        symbols: list[str],
        timeframe: str = "1Min",
        start: str | None = None,
        end: str | None = None,
        limit: int = 1000,
    ) -> dict:
        symbols_norm = [s.strip().upper() for s in symbols if s.strip()]
        params: dict[str, str] = {"symbols": ",".join(symbols_norm), "timeframe": timeframe, "limit": str(limit)}
        if start:
            params["start"] = start
        if end:
            params["end"] = end

        url = f"{self._settings.alpaca_options_data_base_url}/options/bars"
        out: dict[str, list[dict]] = {s: [] for s in symbols_norm}
        page_token: str | None = None

        async with httpx.AsyncClient(timeout=30.0) as client:
            for _ in range(20):
                if page_token:
                    params["page_token"] = page_token
                else:
                    params.pop("page_token", None)

                r = await client.get(url, headers=self._headers, params=params)
                r.raise_for_status()
                payload = r.json()
                raw = payload.get("bars", {}) if isinstance(payload, dict) else {}
                if isinstance(raw, dict):
                    for sym, bars in raw.items():
                        if isinstance(bars, list):
                            out.setdefault(sym, []).extend(bars)

                page_token = payload.get("next_page_token") if isinstance(payload, dict) else None
                if not page_token:
                    break
        return out

    async def get_option_quotes(
        self,
        symbols: list[str],
        start: str | None = None,
        end: str | None = None,
        limit: int = 1000,
    ) -> dict:
        symbols_norm = [s.strip().upper() for s in symbols if s.strip()]
        params: dict[str, str] = {"symbols": ",".join(symbols_norm), "limit": str(limit)}
        if start:
            params["start"] = start
        if end:
            params["end"] = end

        url = f"{self._settings.alpaca_options_data_base_url}/options/quotes"
        out: dict[str, list[dict]] = {s: [] for s in symbols_norm}
        page_token: str | None = None

        async with httpx.AsyncClient(timeout=30.0) as client:
            for _ in range(20):
                if page_token:
                    params["page_token"] = page_token
                else:
                    params.pop("page_token", None)

                r = await client.get(url, headers=self._headers, params=params)
                r.raise_for_status()
                payload = r.json()
                raw = payload.get("quotes", {}) if isinstance(payload, dict) else {}
                if isinstance(raw, dict):
                    for sym, quotes in raw.items():
                        if isinstance(quotes, list):
                            out.setdefault(sym, []).extend(quotes)

                page_token = payload.get("next_page_token") if isinstance(payload, dict) else None
                if not page_token:
                    break
        return out

    async def get_option_latest_quotes(self, symbols: list[str], feed: str | None = None) -> dict:
        symbols_norm = [s.strip().upper() for s in symbols if s.strip()]
        if not symbols_norm:
            return {}

        q_feed = (feed or self._settings.alpaca_options_feed or "").strip().lower() or "indicative"
        if q_feed not in {"indicative", "opra"}:
            q_feed = "indicative"

        url = f"{self._settings.alpaca_options_data_base_url}/options/quotes/latest"
        out: dict[str, dict] = {}
        async with httpx.AsyncClient(timeout=30.0) as client:
            for i in range(0, len(symbols_norm), 100):
                chunk = symbols_norm[i : i + 100]
                params: dict[str, str] = {"symbols": ",".join(chunk), "feed": q_feed}
                r = await client.get(url, headers=self._headers, params=params)
                r.raise_for_status()
                payload = r.json()
                quotes = payload.get("quotes") if isinstance(payload, dict) else None
                if not isinstance(quotes, dict):
                    continue
                for sym, q in quotes.items():
                    if isinstance(q, dict):
                        out[str(sym).upper()] = q
        return out

    async def get_option_trades(
        self,
        symbols: list[str],
        start: str | None = None,
        end: str | None = None,
        limit: int = 1000,
    ) -> dict:
        symbols_norm = [s.strip().upper() for s in symbols if s.strip()]
        params: dict[str, str] = {"symbols": ",".join(symbols_norm), "limit": str(limit)}
        if start:
            params["start"] = start
        if end:
            params["end"] = end

        url = f"{self._settings.alpaca_options_data_base_url}/options/trades"
        out: dict[str, list[dict]] = {s: [] for s in symbols_norm}
        page_token: str | None = None

        async with httpx.AsyncClient(timeout=30.0) as client:
            for _ in range(20):
                if page_token:
                    params["page_token"] = page_token
                else:
                    params.pop("page_token", None)

                r = await client.get(url, headers=self._headers, params=params)
                r.raise_for_status()
                payload = r.json()
                raw = payload.get("trades", {}) if isinstance(payload, dict) else {}
                if isinstance(raw, dict):
                    for sym, trades in raw.items():
                        if isinstance(trades, list):
                            out.setdefault(sym, []).extend(trades)

                page_token = payload.get("next_page_token") if isinstance(payload, dict) else None
                if not page_token:
                    break
        return out

    async def stream_minute_bars(self, symbols: Iterable[str]) -> AsyncIterator[tuple[str, AlpacaBar]]:
        symbols_list = [s.strip().upper() for s in symbols if s.strip()]
        if not symbols_list:
            return

        backoff = 1.0
        while True:
            try:
                async with websockets.connect(self._settings.alpaca_stream_url, ping_interval=20, ping_timeout=20) as ws:
                    await ws.send(
                        json.dumps({"action": "auth", "key": self._settings.alpaca_api_key, "secret": self._settings.alpaca_secret_key})
                    )
                    await ws.send(json.dumps({"action": "subscribe", "bars": symbols_list}))
                    backoff = 1.0

                    while True:
                        raw = await ws.recv()
                        try:
                            msg = json.loads(raw)
                        except Exception:
                            continue

                        if isinstance(msg, dict) and msg.get("T") == "error":
                            raise RuntimeError(f"Alpaca stream error: {msg}")

                        if not isinstance(msg, list):
                            continue

                        for item in msg:
                            if not isinstance(item, dict):
                                continue
                            if item.get("T") != "b":
                                continue
                            sym = str(item.get("S", "")).upper()
                            yield sym, AlpacaBar(
                                t=item["t"],
                                o=float(item["o"]),
                                h=float(item["h"]),
                                l=float(item["l"]),
                                c=float(item["c"]),
                                v=float(item.get("v", 0)),
                                n=None,
                                vw=None,
                            )

                        await asyncio.sleep(0)
            except asyncio.CancelledError:
                raise
            except websockets.exceptions.ConnectionClosed:
                await asyncio.sleep(backoff)
                backoff = min(backoff * 2, 10.0)
            except Exception:
                await asyncio.sleep(backoff)
                backoff = min(backoff * 2, 10.0)
