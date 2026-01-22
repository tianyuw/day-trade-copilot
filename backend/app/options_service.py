from __future__ import annotations

import time
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Any


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

        expirations = sorted({c["expiration"] for c in norm})
        nearest_exp = expirations[0] if expirations else None
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

        strikes = sorted({c["strike"] for c in exp_contracts})
        if not strikes:
            return {"underlying": under, "asof": asof, "expiration": nearest_exp, "underlying_price": underlying_price, "items": []}

        if underlying_price is None:
            atm_idx = len(strikes) // 2
        else:
            atm_idx = min(range(len(strikes)), key=lambda i: abs(strikes[i] - underlying_price))

        lo = max(0, atm_idx - int(strikes_around_atm))
        hi = min(len(strikes), atm_idx + int(strikes_around_atm) + 1)
        selected_strikes = set(strikes[lo:hi])
        selected = [c for c in exp_contracts if c["strike"] in selected_strikes]

        symbols = [c["symbol"] for c in selected]
        snapshots = await self._alpaca.get_option_chain_snapshots(",".join(symbols), feed=options_feed)

        hist_quotes: dict[str, dict[str, Any]] = {}
        if asof_dt and symbols:
            q_start = (asof_dt - timedelta(minutes=2)).isoformat().replace("+00:00", "Z")
            q_end = asof_dt.isoformat().replace("+00:00", "Z")
            raw_q = await self._alpaca.get_option_quotes(symbols, start=q_start, end=q_end, limit=1000)
            if isinstance(raw_q, dict):
                for sym, rows in raw_q.items():
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
                }
            )

        items.sort(key=lambda x: (x["strike"], x["right"]))
        return {"underlying": under, "asof": asof, "expiration": nearest_exp, "underlying_price": underlying_price, "items": items}

