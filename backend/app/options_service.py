from __future__ import annotations

import asyncio
import time
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Any, Iterable, Sequence


@dataclass(frozen=True)
class OptionChainItem:
    symbol: str
    right: str
    expiration: str
    strike: float
    bid: float | None
    ask: float | None
    quote_time: str | None
    implied_volatility: float | None


class OptionChainService:
    def __init__(self, alpaca_client: Any) -> None:
        self._alpaca = alpaca_client
        self._contracts_cache: dict[str, tuple[float, list[dict[str, Any]]]] = {}
        self._contracts_ttl_seconds = 6 * 60 * 60

    def _cache_key(self, underlying: str, asof_date: str | None) -> str:
        u = str(underlying).strip().upper()
        d = str(asof_date or "").strip()
        return f"{u}|{d}"

    async def get_contracts(
        self,
        underlying: str,
        asof_date: str | None = None,
        expiration_date_lte: str | None = None,
        expiration_date_gte: str | None = None,
        limit: int = 100,
    ) -> list[dict[str, Any]]:
        now = time.monotonic()
        key = self._cache_key(underlying, asof_date)
        cached = self._contracts_cache.get(key)
        if cached and cached[0] > now:
            return cached[1]

        under = str(underlying).strip().upper()
        page_token: str | None = None
        out: list[dict[str, Any]] = []
        for _ in range(20):
            payload = await self._alpaca.get_option_contracts(
                [under],
                expiration_date_lte=expiration_date_lte,
                expiration_date_gte=expiration_date_gte,
                limit=limit,
                page_token=page_token,
            )
            contracts = payload.get("option_contracts") if isinstance(payload, dict) else None
            if isinstance(contracts, list):
                for c in contracts:
                    if isinstance(c, dict):
                        out.append(c)
            page_token = payload.get("page_token") if isinstance(payload, dict) else None
            if not page_token:
                break

        self._contracts_cache[key] = (time.monotonic() + self._contracts_ttl_seconds, out)
        return out

    async def build_chain(
        self,
        underlying: str,
        asof: str | None = None,
        strikes_around_atm: int = 5,
        options_feed: str | None = None,
    ) -> dict[str, Any]:
        under = str(underlying).strip().upper()
        asof_dt: datetime | None = None
        if asof:
            asof_dt = datetime.fromisoformat(asof.replace("Z", "+00:00"))
            if asof_dt.tzinfo is None:
                asof_dt = asof_dt.replace(tzinfo=timezone.utc)

        asof_date = asof_dt.date().isoformat() if asof_dt else None
        expiration_gte = asof_date
        expiration_lte = None
        if asof_dt:
            expiration_lte = (asof_dt.date() + timedelta(days=10)).isoformat()

        contracts = await self.get_contracts(
            under,
            asof_date=asof_date,
            expiration_date_gte=expiration_gte,
            expiration_date_lte=expiration_lte,
            limit=100,
        )

        norm: list[dict[str, Any]] = []
        for c in contracts:
            if c.get("tradable") is False:
                continue
            if c.get("status") and str(c.get("status")).lower() != "active":
                continue
            sym = str(c.get("symbol") or "").strip().upper()
            exp = str(c.get("expiration_date") or "").strip()
            right = str(c.get("type") or "").strip().lower()
            strike_raw = c.get("strike_price")
            if not sym or not exp or right not in {"call", "put"}:
                continue
            try:
                strike = float(strike_raw)
            except Exception:
                continue
            norm.append({"symbol": sym, "expiration": exp, "right": right, "strike": strike})

        nearest_exp = self.select_nearest_expiration(norm)
        if not nearest_exp:
            return {"underlying": under, "asof": asof, "expiration": None, "underlying_price": None, "items": []}

        exp_contracts = [c for c in norm if c["expiration"] == nearest_exp]

        underlying_price: float | None = None
        if asof_dt:
            start = (asof_dt - timedelta(minutes=45)).isoformat().replace("+00:00", "Z")
            end = asof_dt.isoformat().replace("+00:00", "Z")
            bars = await self._alpaca.get_bars([under], timeframe="1Min", start=start, end=end, limit=200)
            b = (bars.get(under) or [])[-1:]  # last bar
            if b:
                try:
                    underlying_price = float(b[0].c)
                except Exception:
                    underlying_price = None
        else:
            try:
                snap = await self._alpaca.get_snapshots([under])
                raw = snap.get(under) if isinstance(snap, dict) else None
                latest_quote = raw.get("latestQuote") if isinstance(raw, dict) else None
                if isinstance(latest_quote, dict):
                    ap = latest_quote.get("ap")
                    bp = latest_quote.get("bp")
                    if ap is not None and bp is not None:
                        underlying_price = (float(ap) + float(bp)) / 2
            except Exception:
                underlying_price = None

        selected = self.select_strikes_around_atm(exp_contracts, underlying_price=underlying_price, strikes_around_atm=strikes_around_atm)
        if not selected:
            return {"underlying": under, "asof": asof, "expiration": nearest_exp, "underlying_price": underlying_price, "items": []}

        symbols = [c["symbol"] for c in selected]
        snapshots = await self._fetch_chain_snapshots_for_symbols(under, symbols, feed=options_feed)

        hist_quotes: dict[str, dict[str, Any]] = {}
        if asof_dt and symbols:
            q_start = (asof_dt - timedelta(minutes=2)).isoformat().replace("+00:00", "Z")
            q_end = asof_dt.isoformat().replace("+00:00", "Z")
            tasks = [self._alpaca.get_option_quotes([sym], start=q_start, end=q_end, limit=200) for sym in symbols]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            for sym, res in zip(symbols, results, strict=False):
                if isinstance(res, Exception):
                    continue
                rows = res.get(sym) if isinstance(res, dict) else None
                if isinstance(rows, list) and rows:
                    last = rows[-1]
                    if isinstance(last, dict):
                        hist_quotes[sym] = last

        items: list[dict[str, Any]] = []
        for c in selected:
            sym = c["symbol"]
            snap = snapshots.get(sym) if isinstance(snapshots, dict) else None
            latest_quote = snap.get("latestQuote") if isinstance(snap, dict) else None
            iv = snap.get("impliedVolatility") if isinstance(snap, dict) else None
            greeks = snap.get("greeks") if isinstance(snap, dict) else None
            latest_trade = snap.get("latestTrade") if isinstance(snap, dict) else None

            bid = latest_quote.get("bp") if isinstance(latest_quote, dict) else None
            ask = latest_quote.get("ap") if isinstance(latest_quote, dict) else None
            qt = latest_quote.get("t") if isinstance(latest_quote, dict) else None

            if sym in hist_quotes:
                q = hist_quotes[sym]
                bid = q.get("bp", bid)
                ask = q.get("ap", ask)
                qt = q.get("t", qt)

            items.append(
                {
                    "symbol": sym,
                    "right": c["right"],
                    "expiration": c["expiration"],
                    "strike": c["strike"],
                    "quote": {"bid": bid, "ask": ask, "t": qt},
                    "implied_volatility": iv,
                    "greeks": greeks if isinstance(greeks, dict) else None,
                    "latest_trade": latest_trade if isinstance(latest_trade, dict) else None,
                }
            )

        items.sort(key=lambda x: (x["strike"], x["right"]))
        return {
            "underlying": under,
            "asof": asof,
            "expiration": nearest_exp,
            "underlying_price": underlying_price,
            "items": items,
        }

    async def _fetch_chain_snapshots_for_symbols(
        self,
        underlying: str,
        symbols: Sequence[str],
        *,
        feed: str | None,
        max_pages: int = 20,
    ) -> dict[str, dict[str, Any]]:
        want = {str(s).strip().upper() for s in symbols if str(s).strip()}
        if not want:
            return {}

        out: dict[str, dict[str, Any]] = {}
        page_token: str | None = None
        for _ in range(max_pages):
            payload = await self._alpaca.get_option_chain_snapshots(underlying, feed=feed, page_token=page_token)
            if not isinstance(payload, dict):
                break
            snaps = payload.get("snapshots")
            if not isinstance(snaps, dict):
                snaps = {}
            missing = want - set(out.keys())
            for sym in list(missing):
                v = snaps.get(sym)
                if isinstance(v, dict):
                    out[sym] = v
            page_token = payload.get("next_page_token") if isinstance(payload.get("next_page_token"), str) else None
            if not page_token or len(out) == len(want):
                break
        return out

    @staticmethod
    def select_nearest_expiration(contracts: Sequence[dict[str, Any]]) -> str | None:
        expirations: list[str] = []
        for c in contracts:
            if not isinstance(c, dict):
                continue
            exp = c.get("expiration")
            if isinstance(exp, str) and exp:
                expirations.append(exp)
        expirations = sorted(set(expirations))
        return expirations[0] if expirations else None

    @staticmethod
    def select_strikes_around_atm(
        contracts: Sequence[dict[str, Any]],
        *,
        underlying_price: float | None,
        strikes_around_atm: int,
    ) -> list[dict[str, Any]]:
        strikes: list[float] = []
        for c in contracts:
            if not isinstance(c, dict):
                continue
            s = c.get("strike")
            try:
                if s is not None:
                    strikes.append(float(s))
            except Exception:
                continue
        strikes = sorted(set(strikes))
        if not strikes:
            return []

        if underlying_price is None:
            atm_idx = len(strikes) // 2
        else:
            atm_idx = min(range(len(strikes)), key=lambda i: abs(strikes[i] - underlying_price))

        lo = max(0, atm_idx - int(strikes_around_atm))
        hi = min(len(strikes), atm_idx + int(strikes_around_atm) + 1)
        selected_strikes = set(strikes[lo:hi])
        return [c for c in contracts if isinstance(c, dict) and c.get("strike") in selected_strikes]

    async def get_chain_realtime(
        self,
        underlying: str,
        *,
        strikes_around_atm: int = 5,
        options_feed: str | None = None,
    ) -> dict[str, Any]:
        base = await self.build_chain(
            underlying=underlying,
            asof=None,
            strikes_around_atm=strikes_around_atm,
            options_feed=options_feed,
        )
        items = base.get("items") or []
        symbols: list[str] = [str(it.get("symbol")).upper() for it in items if isinstance(it, dict) and it.get("symbol")]
        if not symbols:
            return base

        try:
            latest = await self._alpaca.get_option_latest_quotes(symbols, feed=options_feed)
        except Exception:
            return base

        for it in items:
            if not isinstance(it, dict):
                continue
            sym = str(it.get("symbol") or "").upper()
            q = latest.get(sym) if isinstance(latest, dict) else None
            if not isinstance(q, dict):
                continue
            quote = it.get("quote") if isinstance(it.get("quote"), dict) else {}
            bid = q.get("bp", quote.get("bid"))
            ask = q.get("ap", quote.get("ask"))
            t = q.get("t", quote.get("t"))
            it["quote"] = {"bid": bid, "ask": ask, "t": t}
        return base

    async def get_option_bars_1m(
        self,
        symbol: str,
        *,
        start: str,
        end: str,
        limit: int = 120,
    ) -> list[dict[str, Any]]:
        sym = str(symbol).strip().upper()
        if not sym:
            return []
        try:
            payload = await self._alpaca.get_option_bars([sym], timeframe="1Min", start=start, end=end, limit=limit)
        except Exception:
            return []
        bars = payload.get(sym) if isinstance(payload, dict) else None
        out: list[dict[str, Any]] = []
        if isinstance(bars, list):
            for b in bars:
                if isinstance(b, dict):
                    out.append(b)
        return out

    async def get_chain_asof(
        self,
        underlying: str,
        asof: str,
        *,
        strikes_around_atm: int = 5,
        options_feed: str | None = None,
        include_bars_minutes: int = 0,
    ) -> dict[str, Any]:
        base = await self.build_chain(
            underlying=underlying,
            asof=asof,
            strikes_around_atm=strikes_around_atm,
            options_feed=options_feed,
        )

        items = base.get("items") or []
        if not isinstance(items, list):
            return base

        for it in items:
            if not isinstance(it, dict):
                continue
            quote = it.get("quote") if isinstance(it.get("quote"), dict) else {}
            bid = quote.get("bid")
            ask = quote.get("ask")
            mid: float | None = None
            try:
                if bid is not None and ask is not None:
                    mid = (float(bid) + float(ask)) / 2.0
            except Exception:
                mid = None
            it["asof_price"] = mid

        if include_bars_minutes <= 0:
            return base

        try:
            asof_dt = datetime.fromisoformat(asof.replace("Z", "+00:00"))
            if asof_dt.tzinfo is None:
                asof_dt = asof_dt.replace(tzinfo=timezone.utc)
        except Exception:
            return base

        start_dt = asof_dt - timedelta(minutes=int(include_bars_minutes))
        start_iso = start_dt.isoformat().replace("+00:00", "Z")
        end_iso = asof_dt.isoformat().replace("+00:00", "Z")

        for it in items:
            if not isinstance(it, dict):
                continue
            sym = str(it.get("symbol") or "").upper()
            if not sym:
                continue
            bars = await self.get_option_bars_1m(sym, start=start_iso, end=end_iso, limit=include_bars_minutes + 5)
            if not bars:
                continue
            bars_sorted = sorted(bars, key=lambda b: b.get("t", ""))
            it["bars_1m"] = bars_sorted
            last = bars_sorted[-1]
            try:
                c = last.get("c")
                if c is not None:
                    it["asof_price"] = float(c)
            except Exception:
                pass

        return base
