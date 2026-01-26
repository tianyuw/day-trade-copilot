from __future__ import annotations

import asyncio
import json
import time
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from typing import Annotated, Any

from fastapi import FastAPI, Query, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .alpaca_client import AlpacaClient
from .openrouter_client import OpenRouterClient
from .analysis_service import AnalysisService
from .options_service import OptionChainService
from .schemas import (
    AIVerificationRequest,
    StreamBarMessage,
    StreamDoneMessage,
    StreamInitMessage,
    StreamAnalysisMessage,
    StreamPositionMessage,
    StreamStateMessage,
    LLMAnalysisRequest,
    LLMAnalysisResponse,
    PositionManagementRequest,
    PositionManagementResponse,
    TradingSettings,
)
from .trade_session import ActiveTrade, SymbolSession, TradeState, _to_epoch_seconds
from .intraday_bootstrap import (
    DEFAULT_CHART_WINDOW_MINUTES,
    DEFAULT_PLAYBACK_FORWARD_CHUNK_MINUTES,
    DEFAULT_PLAYBACK_PREFETCH_LOW_WATERMARK_MINUTES,
    analysis_keep_minutes,
    bootstrap_minutes,
    parse_iso_z,
    playback_initial_fetch_window,
    to_iso_z,
)
from .stream_autopilot import (
    maybe_trigger_analysis as autopilot_maybe_trigger_analysis,
    run_analysis as autopilot_run_analysis,
    run_manage_position as autopilot_run_manage_position,
    send_state as autopilot_send_state,
    to_daily_df as autopilot_to_daily_df,
    to_intraday_df as autopilot_to_intraday_df,
)
from .trading_schemas import (
    CancelOrderRequest,
    ClosePositionRequest,
    ExecutionMode,
    EquityOCORequest,
    ListActivitiesRequest,
    ListOrdersRequest,
    OrderCreateRequest,
    OrderReplaceRequest,
    OptionSyntheticOCOCreateRequest,
    OptionSyntheticOCOUpdateRequest,
)
from .settings import get_settings
from .indicators import ZScoreMomentum, MACD
from .ledger import Ledger
import pandas as pd


def create_app() -> FastAPI:
    settings = get_settings()
    alpaca = AlpacaClient(settings)
    ai = OpenRouterClient(settings)
    analysis_service = AnalysisService(alpaca)
    option_chain_service = OptionChainService(alpaca)
    ledger = Ledger()
    assets_lock = asyncio.Lock()
    assets_cache: dict[str, object] = {"expires_at": 0.0, "assets": []}
    assets_ttl_seconds = 6 * 60 * 60
    auto_trade_execution_enabled = False
    live_trading_enabled = False
    default_execution: ExecutionMode = ExecutionMode.paper
    option_synth_oco: dict[str, dict[str, Any]] = {}

    app = FastAPI(title="0DTE Copilot API", version="0.1.0")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    ledger.ensure_schema()

    @app.get("/api/health")
    async def health() -> dict:
        return {"ok": True}

    @app.get("/api/settings/trading", response_model=TradingSettings)
    async def get_trading_settings() -> TradingSettings:
        return TradingSettings(
            auto_trade_execution_enabled=auto_trade_execution_enabled,
            live_trading_enabled=live_trading_enabled,
            default_execution=default_execution.value,
        )

    @app.post("/api/settings/trading", response_model=TradingSettings)
    async def set_trading_settings(payload: TradingSettings) -> TradingSettings:
        nonlocal auto_trade_execution_enabled
        nonlocal live_trading_enabled
        nonlocal default_execution
        auto_trade_execution_enabled = bool(payload.auto_trade_execution_enabled)
        live_trading_enabled = bool(payload.live_trading_enabled)
        default_execution = ExecutionMode(payload.default_execution)
        return TradingSettings(
            auto_trade_execution_enabled=auto_trade_execution_enabled,
            live_trading_enabled=live_trading_enabled,
            default_execution=default_execution.value,
        )

    @app.get("/api/market/status")
    async def market_status() -> dict:
        et = ZoneInfo("America/New_York")
        now_et = datetime.now(et)

        clock: dict | None = None
        try:
            clock = await alpaca.get_clock()
        except Exception:
            clock = None

        def compute_session(dt_et: datetime) -> str:
            if dt_et.weekday() >= 5:
                return "closed"
            minutes = dt_et.hour * 60 + dt_et.minute
            if 9 * 60 + 30 <= minutes < 16 * 60:
                return "regular"
            if 4 * 60 <= minutes < 9 * 60 + 30:
                return "pre_market"
            if 16 * 60 <= minutes < 20 * 60:
                return "after_hours"
            return "closed"

        def next_weekday_open(dt_et: datetime) -> datetime:
            d = dt_et
            for _ in range(10):
                d = (d + timedelta(days=1)).replace(hour=9, minute=30, second=0, microsecond=0)
                if d.weekday() < 5:
                    return d
            return dt_et.replace(hour=9, minute=30, second=0, microsecond=0)

        session = compute_session(now_et)
        is_open = False
        next_open = next_weekday_open(now_et).astimezone(ZoneInfo("UTC")).isoformat().replace("+00:00", "Z")
        next_close = (datetime.fromisoformat(next_open.replace("Z", "+00:00")) + timedelta(hours=6, minutes=30)).isoformat().replace("+00:00", "Z")
        server_time = now_et.astimezone(ZoneInfo("UTC")).isoformat().replace("+00:00", "Z")
        last_rth_open = ""
        last_rth_close = ""

        if clock and isinstance(clock, dict):
            try:
                server_time = str(clock.get("timestamp") or server_time)
                is_open = bool(clock.get("is_open"))
                next_open = str(clock.get("next_open") or next_open)
                next_close = str(clock.get("next_close") or next_close)
                ts_et = datetime.fromisoformat(server_time.replace("Z", "+00:00")).astimezone(et)
                session = compute_session(ts_et)
                if is_open:
                    session = "regular"
            except Exception:
                pass

        try:
            dt_utc = datetime.fromisoformat(server_time.replace("Z", "+00:00"))
            ts_et = dt_utc.astimezone(et)
            minutes = ts_et.hour * 60 + ts_et.minute
            last_date = ts_et.date() if minutes >= 16 * 60 else (ts_et - timedelta(days=1)).date()
            while last_date.weekday() >= 5:
                last_date = (datetime(last_date.year, last_date.month, last_date.day, tzinfo=et) - timedelta(days=1)).date()
            last_open_et = datetime(last_date.year, last_date.month, last_date.day, 9, 30, tzinfo=et)
            last_close_et = datetime(last_date.year, last_date.month, last_date.day, 16, 0, tzinfo=et)
            last_rth_open = last_open_et.astimezone(ZoneInfo("UTC")).isoformat().replace("+00:00", "Z")
            last_rth_close = last_close_et.astimezone(ZoneInfo("UTC")).isoformat().replace("+00:00", "Z")
        except Exception:
            last_rth_open = ""
            last_rth_close = ""

        return {
            "server_time": server_time,
            "session": session,
            "is_open": is_open,
            "next_open": next_open,
            "next_close": next_close,
            "last_rth_open": last_rth_open,
            "last_rth_close": last_rth_close,
        }

    @app.post("/api/analyze", response_model=LLMAnalysisResponse)
    async def analyze_chart(request: LLMAnalysisRequest):
        """
        Endpoint to trigger LLM analysis for a specific symbol and time.
        """
        try:
            response = await analysis_service.analyze_signal(request)
            payload = response.model_dump()
            plan = payload.get("trade_plan") if isinstance(payload, dict) else None
            trade_id: str | None = str(plan.get("trade_id")) if isinstance(plan, dict) and plan.get("trade_id") else None
            if trade_id:
                ledger.upsert_trade(
                    {
                        "trade_id": trade_id,
                        "symbol": str(payload.get("symbol") or request.symbol).upper(),
                        "mode": str(getattr(request, "mode", "realtime") or "realtime"),
                        "execution": default_execution.value if auto_trade_execution_enabled else "simulated",
                        "state": "ENTRY_PENDING",
                        "option_symbol": None,
                        "option_right": plan.get("option", {}).get("right") if isinstance(plan.get("option"), dict) else None,
                        "option_expiration": plan.get("option", {}).get("expiration") if isinstance(plan.get("option"), dict) else None,
                        "option_strike": plan.get("option", {}).get("strike") if isinstance(plan.get("option"), dict) else None,
                        "contracts_total": plan.get("contracts"),
                        "contracts_remaining": plan.get("contracts"),
                        "entry_time": payload.get("timestamp"),
                        "extra": {
                            "direction": plan.get("direction"),
                            "risk": plan.get("risk"),
                            "take_profit_premium": plan.get("take_profit_premium"),
                        },
                    }
                )
            analysis_id = str(payload.get("analysis_id") or "")
            event_trade_id = trade_id or (f"analysis:{analysis_id}" if analysis_id else f"analysis:{request.symbol}:{payload.get('timestamp')}")
            ledger.append_event(
                trade_id=event_trade_id,
                event_type="llm_analysis_result",
                symbol=str(payload.get("symbol") or request.symbol).upper(),
                timestamp=str(payload.get("timestamp") or ""),
                analysis_id=analysis_id,
                bar_time=str(payload.get("timestamp") or request.current_time),
                payload=payload,
            )
            _append_analysis_history(response)
            return response
        except Exception as e:
            print(f"Analysis Error: {e}")
            raise HTTPException(status_code=500, detail=str(e))

    analysis_history: dict[str, list[LLMAnalysisResponse]] = {}
    position_history: dict[str, list[PositionManagementResponse]] = {}

    def _append_analysis_history(res: LLMAnalysisResponse) -> None:
        sym = str(res.symbol or "").upper()
        if not sym:
            return
        lst = analysis_history.setdefault(sym, [])
        lst.append(res)
        if len(lst) > 200:
            del lst[:-200]

    def _append_position_history(res: PositionManagementResponse) -> None:
        sym = str(res.symbol or "").upper()
        if not sym:
            return
        lst = position_history.setdefault(sym, [])
        lst.append(res)
        if len(lst) > 200:
            del lst[:-200]

    @app.get("/api/analysis/{analysis_id}", response_model=LLMAnalysisResponse)
    async def get_analysis(analysis_id: str) -> LLMAnalysisResponse:
        res = await analysis_service.get_cached_analysis(analysis_id)
        if res is None:
            raise HTTPException(status_code=404, detail="analysis_id not found or expired")
        return res

    @app.get("/api/stocks/bars")
    async def stocks_bars(
        symbols: Annotated[str, Query(min_length=1)],
        timeframe: Annotated[str, Query()] = "1Min",
        start: Annotated[str | None, Query()] = None,
        end: Annotated[str | None, Query()] = None,
        limit: Annotated[int, Query(ge=1, le=10000)] = 1000,
    ) -> dict:
        symbol_list = [s.strip().upper() for s in symbols.split(",") if s.strip()]
        bars = await alpaca.get_bars(symbol_list, timeframe=timeframe, start=start, end=end, limit=limit)
        return {"bars": {k: [b.model_dump() for b in v] for k, v in bars.items()}}

    @app.get("/api/stocks/snapshots")
    async def stocks_snapshots(symbols: Annotated[str, Query(min_length=1)]) -> dict:
        symbol_list = [s.strip().upper() for s in symbols.split(",") if s.strip()]
        return await alpaca.get_snapshots(symbol_list)

    @app.get("/api/stocks/prev_close")
    async def stocks_prev_close(
        symbols: Annotated[str, Query(min_length=1)],
        asof: Annotated[str, Query(min_length=1)],
    ) -> dict:
        symbol_list = [s.strip().upper() for s in symbols.split(",") if s.strip()]

        def parse_rfc3339(v: str) -> datetime:
            return datetime.fromisoformat(v.replace("Z", "+00:00"))

        asof_dt = parse_rfc3339(asof)
        start_dt = asof_dt - timedelta(days=21)
        daily = await alpaca.get_bars(
            symbol_list,
            timeframe="1Day",
            start=start_dt.isoformat().replace("+00:00", "Z"),
            end=asof_dt.isoformat().replace("+00:00", "Z"),
            limit=1000,
        )

        et = ZoneInfo("America/New_York")
        asof_date_et = asof_dt.astimezone(et).date()

        prev_close: dict[str, float | None] = {}
        for sym, bars in daily.items():
            if not bars:
                prev_close[sym] = None
                continue

            idx_today: int | None = None
            for i, b in enumerate(bars):
                try:
                    bar_date_et = parse_rfc3339(b.t).astimezone(et).date()
                except Exception:
                    continue
                if bar_date_et == asof_date_et:
                    idx_today = i

            if idx_today is not None and idx_today - 1 >= 0:
                prev_close[sym] = float(bars[idx_today - 1].c)
            else:
                prev_close[sym] = float(bars[-1].c)

        missing = [s for s in symbol_list if prev_close.get(s) is None]
        if missing:
            async def fallback(sym: str) -> tuple[str, float | None]:
                try:
                    data = await alpaca.get_bars([sym], timeframe="1Day", limit=10)
                    bars = data.get(sym, [])
                    if bars:
                        idx_today: int | None = None
                        for i, b in enumerate(bars):
                            try:
                                bar_date_et = parse_rfc3339(b.t).astimezone(et).date()
                            except Exception:
                                continue
                            if bar_date_et == asof_date_et:
                                idx_today = i
                        if idx_today is not None and idx_today - 1 >= 0:
                            return sym, float(bars[idx_today - 1].c)
                        return sym, float(bars[-1].c)
                except Exception:
                    pass

                try:
                    snap = await alpaca.get_snapshots([sym])
                    s = snap.get(sym) if isinstance(snap, dict) else None
                    prev = s.get("prevDailyBar") if isinstance(s, dict) else None
                    if isinstance(prev, dict) and prev.get("c") is not None:
                        return sym, float(prev.get("c"))
                except Exception:
                    pass

                return sym, None

            pairs = await asyncio.gather(*[fallback(s) for s in missing])
            for sym, val in pairs:
                if val is not None:
                    prev_close[sym] = val

        return {"prev_close": prev_close}

    def _et_midnight_utc_iso(now_utc: datetime) -> str:
        et = ZoneInfo("America/New_York")
        now_et = now_utc.astimezone(et)
        midnight_et = datetime(now_et.year, now_et.month, now_et.day, tzinfo=et)
        return midnight_et.astimezone(ZoneInfo("UTC")).isoformat().replace("+00:00", "Z")

    @app.get("/api/ai/history/{symbol}")
    async def ai_history(
        symbol: str,
        since: Annotated[str | None, Query()] = None,
        limit: Annotated[int, Query(ge=1, le=5000)] = 1000,
    ) -> dict:
        sym = symbol.strip().upper()
        if not sym:
            raise HTTPException(status_code=400, detail="symbol required")

        since_ts = since or _et_midnight_utc_iso(datetime.now(ZoneInfo("UTC")))
        events = ledger.list_events_by_symbol(
            sym,
            since_ts=since_ts,
            limit=limit,
            event_types=["llm_analysis_result", "ai_verify_result", "position_mgmt_requested", "position_mgmt_result"],
        )

        analysis: list[dict[str, Any]] = []
        positions: list[dict[str, Any]] = []
        for e in events:
            payload_json = e.get("payload_json")
            payload: Any = None
            if isinstance(payload_json, str) and payload_json:
                try:
                    payload = json.loads(payload_json)
                except Exception:
                    payload = None
            item = payload if isinstance(payload, dict) else {"raw": payload_json}
            item_ts = str(e.get("timestamp") or "")
            item.setdefault("timestamp", item_ts)
            item.setdefault("bar_time", e.get("bar_time"))
            item.setdefault("analysis_id", e.get("analysis_id"))
            item.setdefault("trade_id", e.get("trade_id"))
            item.setdefault("symbol", sym)

            etype = str(e.get("event_type") or "")
            if etype in {"position_mgmt_result", "position_mgmt_requested"}:
                positions.append(item)
            else:
                analysis.append(item)

        return {"symbol": sym, "analysis": analysis, "positions": positions}

    @app.get("/api/trades/active")
    async def active_trades(symbols: Annotated[str, Query(min_length=1)]) -> dict:
        symbol_list = [s.strip().upper() for s in symbols.split(",") if s.strip()]
        rows = ledger.get_active_trades(symbol_list)
        by_symbol: dict[str, dict[str, Any]] = {s: {"in_position": False} for s in symbol_list}
        for r in rows:
            sym = str(r.get("symbol") or "").upper()
            if not sym:
                continue
            by_symbol[sym] = {
                "in_position": True,
                "trade_id": r.get("trade_id"),
                "state": r.get("state") or "IN_POSITION",
                "contracts_total": r.get("contracts_total"),
                "contracts_remaining": r.get("contracts_remaining"),
                "option": {
                    "right": r.get("option_right"),
                    "expiration": r.get("option_expiration"),
                    "strike": r.get("option_strike"),
                },
                "option_symbol": r.get("option_symbol"),
                "updated_at": r.get("updated_at"),
            }
        return {"active": by_symbol}

    @app.get("/api/options/contracts")
    async def options_contracts(
        underlying: Annotated[str, Query(min_length=1)],
        expiration_date_lte: Annotated[str | None, Query()] = None,
        expiration_date_gte: Annotated[str | None, Query()] = None,
        limit: Annotated[int, Query(ge=1, le=1000)] = 100,
    ) -> dict:
        contracts = await option_chain_service.get_contracts(
            underlying=underlying,
            asof_date=expiration_date_gte,
            expiration_date_lte=expiration_date_lte,
            expiration_date_gte=expiration_date_gte,
            limit=limit,
        )
        return {"option_contracts": contracts}

    @app.get("/api/options/chain")
    async def options_chain(
        underlying: Annotated[str, Query(min_length=1)],
        asof: Annotated[str | None, Query()] = None,
        strikes_around_atm: Annotated[int, Query(ge=0, le=50)] = 5,
        feed: Annotated[str | None, Query()] = None,
    ) -> dict:
        if asof:
            return await option_chain_service.get_chain_asof(
                underlying=underlying,
                asof=asof,
                strikes_around_atm=strikes_around_atm,
                options_feed=feed,
            )
        return await option_chain_service.build_chain(
            underlying=underlying,
            asof=None,
            strikes_around_atm=strikes_around_atm,
            options_feed=feed,
        )

    @app.get("/api/options/quotes")
    async def options_quotes(
        symbols: Annotated[str, Query(min_length=1)],
        feed: Annotated[str | None, Query()] = None,
        start: Annotated[str | None, Query()] = None,
        end: Annotated[str | None, Query()] = None,
    ) -> dict:
        if start or end:
            raise HTTPException(status_code=400, detail="historical option quotes are not available; use /api/options/bars or /api/options/trades")
        symbol_list = [s.strip().upper() for s in symbols.split(",") if s.strip()]
        quotes = await alpaca.get_option_latest_quotes(symbol_list, feed=feed)
        return {"quotes": quotes}

    @app.get("/api/options/bars")
    async def options_bars(
        symbols: Annotated[str, Query(min_length=1)],
        timeframe: Annotated[str, Query()] = "1Min",
        start: Annotated[str | None, Query()] = None,
        end: Annotated[str | None, Query()] = None,
        limit: Annotated[int, Query(ge=1, le=10000)] = 1000,
    ) -> dict:
        symbol_list = [s.strip().upper() for s in symbols.split(",") if s.strip()]
        bars = await alpaca.get_option_bars(symbol_list, timeframe=timeframe, start=start, end=end, limit=limit)
        return {"bars": bars}

    async def get_cached_assets() -> list[dict]:
        now = time.time()
        expires_at = float(assets_cache.get("expires_at") or 0.0)
        cached = assets_cache.get("assets")
        if now < expires_at and isinstance(cached, list):
            return cached

        async with assets_lock:
            now2 = time.time()
            expires_at2 = float(assets_cache.get("expires_at") or 0.0)
            cached2 = assets_cache.get("assets")
            if now2 < expires_at2 and isinstance(cached2, list):
                return cached2

            assets = await alpaca.get_assets(status="active", asset_class="us_equity")
            assets_cache["assets"] = assets
            assets_cache["expires_at"] = now2 + assets_ttl_seconds
            return assets

    @app.get("/api/stocks/symbols")
    async def stocks_symbols(
        query: Annotated[str, Query(max_length=64)] = "",
        limit: Annotated[int, Query(ge=1, le=100)] = 20,
    ) -> dict:
        q = query.strip()
        if not q:
            return {"symbols": []}

        q_upper = q.upper()
        q_lower = q.lower()
        assets = await get_cached_assets()

        out: list[dict] = []
        seen: set[str] = set()

        for a in assets:
            if len(out) >= limit:
                break
            if not isinstance(a, dict):
                continue
            sym = str(a.get("symbol") or "").upper()
            if not sym or sym in seen:
                continue
            if a.get("tradable") is False:
                continue
            name = str(a.get("name") or "")
            if sym.startswith(q_upper):
                out.append({"symbol": sym, "name": name, "exchange": a.get("exchange")})
                seen.add(sym)

        if len(out) < limit:
            for a in assets:
                if len(out) >= limit:
                    break
                if not isinstance(a, dict):
                    continue
                sym = str(a.get("symbol") or "").upper()
                if not sym or sym in seen:
                    continue
                if a.get("tradable") is False:
                    continue
                name = str(a.get("name") or "")
                if q_upper in sym or (name and q_lower in name.lower()):
                    out.append({"symbol": sym, "name": name, "exchange": a.get("exchange")})
                    seen.add(sym)

        return {"symbols": out}

    @app.post("/api/ai/verify")
    async def ai_verify(req: AIVerificationRequest) -> dict:
        res = await ai.verify(req)
        return res.model_dump()

    @app.post("/api/ai/position_manage", response_model=PositionManagementResponse)
    async def position_manage(req: PositionManagementRequest) -> PositionManagementResponse:
        ledger.append_event(
            trade_id=req.trade_id,
            event_type="position_mgmt_requested",
            symbol=req.symbol,
            timestamp=req.bar_time,
            bar_time=req.bar_time,
            payload={"symbol": req.symbol, "execution": default_execution.value if auto_trade_execution_enabled else "simulated"},
        )
        res = await analysis_service.manage_position(req)
        _append_position_history(res)
        payload = res.model_dump()
        ledger.append_event(
            trade_id=req.trade_id,
            event_type="position_mgmt_result",
            symbol=req.symbol,
            timestamp=str(payload.get("timestamp") or req.bar_time),
            analysis_id=str(payload.get("analysis_id") or ""),
            bar_time=req.bar_time,
            payload=payload,
        )
        try:
            t = ledger.get_trade(req.trade_id) or {}
            remaining = t.get("contracts_remaining")
            try:
                remaining_i = int(remaining) if remaining is not None else int(req.position.get("contracts_remaining") or 0)
            except Exception:
                remaining_i = int(req.position.get("contracts_remaining") or 0)
            d = payload.get("decision") if isinstance(payload, dict) else None
            act = str(d.get("action") or "") if isinstance(d, dict) else ""
            if act == "close_all":
                remaining_i = 0
            elif act == "close_partial":
                exit_ = d.get("exit") if isinstance(d, dict) else None
                n = int(exit_.get("contracts_to_close") or 0) if isinstance(exit_, dict) else 0
                remaining_i = max(0, remaining_i - max(0, n))
            exit_time = str(payload.get("timestamp") or req.bar_time) if remaining_i <= 0 else None
            ledger.upsert_trade(
                {
                    "trade_id": req.trade_id,
                    "symbol": req.symbol,
                    "mode": str(getattr(req, "mode", "realtime") or "realtime"),
                    "execution": default_execution.value if auto_trade_execution_enabled else "simulated",
                    "state": "CLOSED" if remaining_i <= 0 else "IN_POSITION",
                    "contracts_total": (t.get("contracts_total") if isinstance(t, dict) else None) or req.position.get("contracts_total"),
                    "contracts_remaining": remaining_i,
                    "exit_time": exit_time,
                }
            )
        except Exception:
            pass
        return res

    def require_execution(execution: ExecutionMode) -> ExecutionMode:
        if execution == ExecutionMode.live and not live_trading_enabled:
            raise HTTPException(status_code=403, detail="Live trading disabled")
        return execution

    @app.get("/api/trading/account")
    async def trading_account(execution: ExecutionMode = Query(default=ExecutionMode.paper)) -> dict:
        execution = require_execution(execution)
        return await alpaca.get_account(execution.value)

    @app.get("/api/trading/positions")
    async def trading_positions(execution: ExecutionMode = Query(default=ExecutionMode.paper)) -> dict:
        execution = require_execution(execution)
        return {"positions": await alpaca.list_positions(execution.value)}

    @app.get("/api/trading/positions/{symbol}")
    async def trading_position(symbol: str, execution: ExecutionMode = Query(default=ExecutionMode.paper)) -> dict:
        execution = require_execution(execution)
        return await alpaca.get_position(symbol, execution.value)

    @app.delete("/api/trading/positions/{symbol}")
    async def trading_close_position(symbol: str, req: ClosePositionRequest) -> dict:
        execution = require_execution(req.execution)
        return await alpaca.close_position(symbol, execution.value, qty=req.qty, percentage=req.percentage)

    @app.get("/api/trading/orders")
    async def trading_orders(
        execution: ExecutionMode = Query(default=ExecutionMode.paper),
        status: str | None = None,
        limit: int | None = Query(default=None, ge=1, le=500),
        after: str | None = None,
        until: str | None = None,
        direction: str | None = None,
        nested: bool | None = None,
        symbols: str | None = None,
    ) -> dict:
        execution = require_execution(execution)
        params: dict[str, str] = {}
        if status is not None:
            params["status"] = status
        if limit is not None:
            params["limit"] = str(limit)
        if after is not None:
            params["after"] = after
        if until is not None:
            params["until"] = until
        if direction is not None:
            params["direction"] = direction
        if nested is not None:
            params["nested"] = "true" if nested else "false"
        if symbols is not None:
            params["symbols"] = symbols
        return {"orders": await alpaca.list_orders(execution.value, params=params or None)}

    @app.get("/api/trading/orders/{order_id}")
    async def trading_order(order_id: str, execution: ExecutionMode = Query(default=ExecutionMode.paper)) -> dict:
        execution = require_execution(execution)
        return await alpaca.get_order(order_id, execution.value)

    @app.post("/api/trading/orders")
    async def trading_submit_order(req: OrderCreateRequest) -> dict:
        execution = require_execution(req.execution)
        payload = req.model_dump(exclude={"execution"}, exclude_none=True)
        res = await alpaca.submit_order(payload, execution.value)
        ledger.append_event(
            trade_id=str(req.client_order_id or "unknown"),
            event_type="order_submitted",
            payload={"execution": execution.value, "order": res, "request": payload},
        )
        return res

    @app.post("/api/trading/oco")
    async def trading_submit_oco(req: EquityOCORequest) -> dict:
        execution = require_execution(req.execution)
        payload: dict[str, Any] = {
            "symbol": req.symbol,
            "qty": req.qty,
            "side": "sell",
            "type": "limit",
            "time_in_force": req.time_in_force,
            "order_class": "oco",
            "take_profit": {"limit_price": req.take_profit_limit_price},
            "stop_loss": {
                "stop_price": req.stop_loss_stop_price,
                **({"limit_price": req.stop_loss_limit_price} if req.stop_loss_limit_price else {}),
            },
        }
        res = await alpaca.submit_order(payload, execution.value)
        ledger.append_event(
            trade_id="unknown",
            event_type="oco_submitted",
            payload={"execution": execution.value, "order": res, "request": payload},
        )
        return res

    @app.post("/api/trading/options/synthetic_oco")
    async def trading_create_option_synthetic_oco(req: OptionSyntheticOCOCreateRequest) -> dict:
        execution = require_execution(req.execution)
        payload: dict[str, Any] = {
            "symbol": req.option_symbol,
            "qty": req.qty,
            "side": "sell",
            "type": "limit",
            "time_in_force": "day",
            "limit_price": req.take_profit_limit_price,
            "position_intent": "sell_to_close",
        }
        tp_order = await alpaca.submit_order(payload, execution.value)
        option_synth_oco[req.trade_id] = {
            "execution": execution.value,
            "option_symbol": req.option_symbol,
            "qty": req.qty,
            "tp_order_id": str(tp_order.get("id") or ""),
            "take_profit_limit_price": req.take_profit_limit_price,
            "stop_loss_premium": req.stop_loss_premium,
            "time_stop_minutes": req.time_stop_minutes,
        }
        ledger.append_event(
            trade_id=req.trade_id,
            event_type="option_synthetic_oco_created",
            payload={"execution": execution.value, "tp_order": tp_order, "rule": option_synth_oco[req.trade_id]},
        )
        return {"tp_order": tp_order, "rule": option_synth_oco[req.trade_id]}

    @app.get("/api/trading/options/synthetic_oco/{trade_id}")
    async def trading_get_option_synthetic_oco(trade_id: str) -> dict:
        return {"rule": option_synth_oco.get(trade_id)}

    @app.patch("/api/trading/options/synthetic_oco/{trade_id}")
    async def trading_update_option_synthetic_oco(trade_id: str, req: OptionSyntheticOCOUpdateRequest) -> dict:
        execution = require_execution(req.execution)
        cur = option_synth_oco.get(trade_id)
        if not cur:
            raise HTTPException(status_code=404, detail="synthetic_oco not found")
        if req.take_profit_limit_price is not None:
            tp_order_id = str(cur.get("tp_order_id") or "")
            if tp_order_id:
                await alpaca.replace_order(tp_order_id, {"limit_price": req.take_profit_limit_price}, execution.value)
            cur["take_profit_limit_price"] = req.take_profit_limit_price
        if req.stop_loss_premium is not None:
            cur["stop_loss_premium"] = req.stop_loss_premium
        if req.time_stop_minutes is not None:
            cur["time_stop_minutes"] = req.time_stop_minutes
        cur["execution"] = execution.value
        option_synth_oco[trade_id] = cur
        ledger.append_event(
            trade_id=trade_id,
            event_type="option_synthetic_oco_updated",
            payload={"execution": execution.value, "rule": cur},
        )
        return {"rule": cur}

    @app.get("/api/trades")
    async def list_trades(
        symbol: str | None = None,
        mode: str | None = None,
        execution: str | None = None,
        limit: int = Query(default=200, ge=1, le=1000),
    ) -> dict:
        return {"trades": ledger.list_trades(symbol=symbol, mode=mode, execution=execution, limit=limit)}

    @app.get("/api/trades/{trade_id}")
    async def get_trade(trade_id: str) -> dict:
        t = ledger.get_trade(trade_id)
        if t is None:
            raise HTTPException(status_code=404, detail="trade_id not found")
        return t

    @app.get("/api/trades/{trade_id}/events")
    async def get_trade_events(trade_id: str, limit: int = Query(default=500, ge=1, le=2000)) -> dict:
        return {"events": ledger.list_events(trade_id, limit=limit)}

    @app.patch("/api/trading/orders/{order_id}")
    async def trading_replace_order(order_id: str, req: OrderReplaceRequest) -> dict:
        execution = require_execution(req.execution)
        payload = req.model_dump(exclude={"execution"}, exclude_none=True)
        res = await alpaca.replace_order(order_id, payload, execution.value)
        ledger.append_event(
            trade_id=str(req.client_order_id or "unknown"),
            event_type="order_replaced",
            payload={"execution": execution.value, "order": res, "request": payload},
        )
        return res

    @app.delete("/api/trading/orders/{order_id}")
    async def trading_cancel_order(order_id: str, req: CancelOrderRequest) -> dict:
        execution = require_execution(req.execution)
        await alpaca.cancel_order(order_id, execution.value)
        ledger.append_event(
            trade_id="unknown",
            event_type="order_cancelled",
            payload={"execution": execution.value, "order_id": order_id},
        )
        return {"ok": True}

    @app.get("/api/trading/activities")
    async def trading_activities(
        execution: ExecutionMode = Query(default=ExecutionMode.paper),
        activity_type: str | None = None,
        after: str | None = None,
        until: str | None = None,
        page_size: int | None = Query(default=None, ge=1, le=1000),
    ) -> dict:
        execution = require_execution(execution)
        params: dict[str, str] = {}
        if activity_type is not None:
            params["activity_type"] = activity_type
        if after is not None:
            params["after"] = after
        if until is not None:
            params["until"] = until
        if page_size is not None:
            params["page_size"] = str(page_size)
        return {"activities": await alpaca.list_account_activities(execution.value, params=params or None)}

    @app.websocket("/ws/realtime")
    async def ws_realtime(
        ws: WebSocket,
        symbols: str = Query(default="AAPL,MSFT,NVDA,TSLA,SPY"),
        analyze: bool = Query(default=False),
        analysis_window_minutes: int = Query(default=300, ge=30, le=2000),
    ) -> None:
        await ws.accept()
        symbol_list = [s.strip().upper() for s in symbols.split(",") if s.strip()]
        
        # Initialize indicators for realtime
        indicators: dict[str, ZScoreMomentum] = {}
        macd_indicators: dict[str, MACD] = {}
        intraday_buffers: dict[str, list] = {sym: [] for sym in symbol_list}
        daily_bars_df: dict[str, pd.DataFrame | None] = {}
        last_analyzed_time: dict[str, str] = {}
        sessions: dict[str, SymbolSession] = {sym: SymbolSession(symbol=sym, mode="realtime") for sym in symbol_list}
        last_state_sent: dict[str, tuple[str, int | None]] = {}
        llm_sem = asyncio.Semaphore(2)

        async def send_state(sym: str) -> None:
            s = sessions.get(sym)
            if not s:
                return
            await autopilot_send_state(ws, session=s, mode="realtime", last_state_sent=last_state_sent)

        async def after_analysis(llm_res: LLMAnalysisResponse, payload: dict[str, Any], option_symbol: str | None) -> None:
            plan = payload.get("trade_plan") if isinstance(payload, dict) else None
            trade_id = str(plan.get("trade_id")) if isinstance(plan, dict) and plan.get("trade_id") else None
            analysis_id = str(payload.get("analysis_id") or "")
            event_trade_id = trade_id or (f"analysis:{analysis_id}" if analysis_id else f"analysis:{payload.get('symbol')}:{payload.get('timestamp')}")
            ledger.append_event(
                trade_id=event_trade_id,
                event_type="llm_analysis_result",
                symbol=str(payload.get("symbol") or "").upper() or llm_res.symbol,
                timestamp=str(payload.get("timestamp") or ""),
                analysis_id=analysis_id,
                bar_time=str(payload.get("bar_time") or payload.get("timestamp") or ""),
                payload=payload,
            )
            _append_analysis_history(llm_res)
            if payload.get("action") in ("buy_long", "buy_short") and isinstance(payload.get("trade_plan"), dict):
                plan2 = payload.get("trade_plan") or {}
                opt = plan2.get("option") if isinstance(plan2.get("option"), dict) else {}
                try:
                    ledger.upsert_trade(
                        {
                            "trade_id": str(plan2.get("trade_id") or ""),
                            "symbol": str(payload.get("symbol") or "").upper() or llm_res.symbol,
                            "mode": "realtime",
                            "execution": default_execution.value if auto_trade_execution_enabled else "simulated",
                            "state": "IN_POSITION",
                            "option_symbol": option_symbol,
                            "option_right": opt.get("right"),
                            "option_expiration": opt.get("expiration"),
                            "option_strike": opt.get("strike"),
                            "contracts_total": plan2.get("contracts"),
                            "contracts_remaining": plan2.get("contracts"),
                            "entry_time": payload.get("timestamp"),
                            "extra": {
                                "direction": plan2.get("direction"),
                                "risk": plan2.get("risk"),
                                "take_profit_premium": plan2.get("take_profit_premium"),
                            },
                        }
                    )
                except Exception:
                    pass

        async def after_position(pm_res: PositionManagementResponse, pm_payload: dict[str, Any]) -> None:
            trade_id = str(pm_payload.get("trade_id") or "")
            analysis_id = str(pm_payload.get("analysis_id") or "")
            ledger.append_event(
                trade_id=trade_id,
                event_type="position_mgmt_result",
                symbol=str(pm_payload.get("symbol") or "").upper() or pm_res.symbol,
                timestamp=str(pm_payload.get("timestamp") or ""),
                analysis_id=analysis_id,
                bar_time=str(pm_payload.get("bar_time") or pm_payload.get("timestamp") or ""),
                payload=pm_payload,
            )
            _append_position_history(pm_res)
            try:
                s = sessions.get(str(pm_payload.get("symbol") or "").upper() or pm_res.symbol)
                if s and s.trade:
                    ledger.upsert_trade(
                        {
                            "trade_id": s.trade.trade_id,
                            "symbol": s.symbol,
                            "mode": "realtime",
                            "execution": default_execution.value if auto_trade_execution_enabled else "simulated",
                            "state": "IN_POSITION",
                            "contracts_total": s.trade.contracts_total,
                            "contracts_remaining": s.trade.contracts_remaining,
                            "extra": {
                                "direction": s.trade.direction,
                                "risk": s.trade.risk,
                                "take_profit_premium": s.trade.risk.get("take_profit_premium"),
                            },
                        }
                    )
                else:
                    ledger.upsert_trade(
                        {
                            "trade_id": trade_id,
                            "symbol": str(pm_payload.get("symbol") or "").upper() or pm_res.symbol,
                            "mode": "realtime",
                            "execution": default_execution.value if auto_trade_execution_enabled else "simulated",
                            "state": "CLOSED",
                            "contracts_remaining": 0,
                            "exit_time": str(pm_payload.get("timestamp") or ""),
                        }
                    )
            except Exception:
                pass

        try:
            active_rows = ledger.get_active_trades(symbol_list)
            for r in active_rows:
                sym = str(r.get("symbol") or "").upper()
                s = sessions.get(sym)
                if not s:
                    continue
                extra: dict[str, Any] = {}
                try:
                    raw = r.get("extra_json")
                    if isinstance(raw, str) and raw:
                        parsed = json.loads(raw)
                        extra = parsed if isinstance(parsed, dict) else {}
                except Exception:
                    extra = {}

                try:
                    contracts_total = int(r.get("contracts_total") or 0)
                    contracts_remaining = int(r.get("contracts_remaining") or 0)
                except Exception:
                    continue
                if contracts_remaining <= 0:
                    continue

                direction = str(extra.get("direction") or "")
                opt = {
                    "right": r.get("option_right"),
                    "expiration": r.get("option_expiration"),
                    "strike": r.get("option_strike"),
                }
                risk_in = extra.get("risk") if isinstance(extra.get("risk"), dict) else {}
                take_profit = extra.get("take_profit_premium")
                risk = {
                    "stop_loss_premium": risk_in.get("stop_loss_premium"),
                    "take_profit_premium": take_profit if take_profit is not None else risk_in.get("take_profit_premium"),
                    "time_stop_minutes": risk_in.get("time_stop_minutes"),
                }

                s.trade = ActiveTrade(
                    trade_id=str(r.get("trade_id") or ""),
                    direction=direction,
                    option=opt,
                    option_symbol=str(r.get("option_symbol") or "").upper() or None,
                    contracts_total=contracts_total,
                    contracts_remaining=contracts_remaining,
                    entry_time=str(r.get("entry_time") or ""),
                    entry_premium=r.get("entry_premium"),
                    risk=risk,
                )
                st = str(r.get("state") or "IN_POSITION").upper()
                s.state = TradeState.IN_POSITION if st == "IN_POSITION" else TradeState.IN_POSITION
        except Exception:
            pass
        # Fetch daily history for indicators
        today = datetime.now(ZoneInfo("America/New_York")).date()
        daily_start = (today - timedelta(days=60)).isoformat() # Get enough history
        
        try:
            # We need daily bars for indicators
            daily_bars = await alpaca.get_bars(symbol_list, timeframe="1Day", start=daily_start, limit=100)
            for sym in symbol_list:
                bars = daily_bars.get(sym, [])
                indicators[sym] = ZScoreMomentum([b.model_dump() for b in bars])
                macd_indicators[sym] = MACD()
                df_daily = pd.DataFrame([b.model_dump() for b in bars])
                if not df_daily.empty:
                    df_daily["timestamp"] = pd.to_datetime(df_daily["t"])
                    df_daily.set_index("timestamp", inplace=True)
                    df_daily.rename(
                        columns={"o": "open", "h": "high", "l": "low", "c": "close", "v": "volume"},
                        inplace=True,
                    )
                    df_daily.sort_index(inplace=True)
                    daily_bars_df[sym] = df_daily
                else:
                    daily_bars_df[sym] = None

            now_utc = datetime.now(ZoneInfo("UTC"))
            keep_n = analysis_keep_minutes(analysis_window_minutes)
            backfill_minutes = bootstrap_minutes(
                analysis_window_minutes=analysis_window_minutes,
                chart_window_minutes=DEFAULT_CHART_WINDOW_MINUTES,
            )
            chart_minutes = DEFAULT_CHART_WINDOW_MINUTES
            backfill_start = (now_utc - timedelta(minutes=backfill_minutes)).isoformat().replace("+00:00", "Z")
            backfill_end = now_utc.isoformat().replace("+00:00", "Z")

            async def fetch_intraday(sym: str) -> tuple[str, list]:
                data = await alpaca.get_bars(
                    [sym],
                    timeframe="1Min",
                    start=backfill_start,
                    end=backfill_end,
                    limit=backfill_minutes,
                )
                bars = data.get(sym, [])
                if not bars:
                    data = await alpaca.get_bars(
                        [sym],
                        timeframe="1Min",
                        start=backfill_start,
                        limit=backfill_minutes,
                    )
                    bars = data.get(sym, [])
                return sym, bars

            backfill_pairs = await asyncio.gather(*[fetch_intraday(sym) for sym in symbol_list])
            backfill: dict[str, list] = {sym: bars for sym, bars in backfill_pairs}

            for sym in symbol_list:
                bars = backfill.get(sym, [])
                # Process backfill to warmup indicators
                last_bar = None
                last_z_res = None
                last_final_signal = None
                for bar in bars:
                    z_res = indicators[sym].update(float(bar.c))
                    m_res = macd_indicators[sym].update(float(bar.c))
                    
                    final_signal = None
                    if z_res.get('signal') == 'long':
                        final_signal = 'long'
                    elif z_res.get('signal') == 'short':
                        final_signal = 'short'

                    bar.indicators = {**z_res, **m_res, "signal": final_signal}
                    intraday_buffers[sym].append(bar)
                    last_bar = bar
                    last_z_res = z_res
                    last_final_signal = final_signal

                if last_bar is not None and last_z_res is not None:
                    first_t = bars[0].t if bars else None
                    print(
                        f"[QUANT] {sym} warmup {len(bars)} bars {first_t} -> {last_bar.t} | "
                        f"LastPrice: {last_bar.c} | Z-Diff: {last_z_res.get('z_score_diff')} | Signal: {last_final_signal}"
                    )
                
                init_bars = bars[-chart_minutes:] if len(bars) > chart_minutes else bars
                await ws.send_json(
                    StreamInitMessage(type="init", mode="realtime", symbol=sym, bars=init_bars).model_dump()
                )
                await send_state(sym)

            async for sym, bar in alpaca.stream_minute_bars(symbol_list):
                if sym in indicators:
                    z_res = indicators[sym].update(float(bar.c))
                    m_res = macd_indicators[sym].update(float(bar.c))
                    
                    final_signal = None
                    if z_res.get('signal') == 'long':
                        final_signal = 'long'
                    elif z_res.get('signal') == 'short':
                        final_signal = 'short'
                        
                    print(f"[QUANT] {sym} {bar.t} | Price: {bar.c} | Z-Diff: {z_res.get('z_score_diff')} | Signal: {final_signal}")

                    bar.indicators = {**z_res, **m_res, "signal": final_signal}
                    intraday_buffers[sym].append(bar)
                    intraday_buffers[sym] = intraday_buffers[sym][-keep_n:]

                session = sessions.get(sym)
                if not analyze or not session:
                    await ws.send_json(
                        StreamBarMessage(type="bar", mode="realtime", symbol=sym, bar=bar).model_dump()
                    )
                    continue

                session.last_bar_time = bar.t
                now_epoch = _to_epoch_seconds(bar.t)
                session.update_watches(now_epoch)

                has_quant_signal = bool(bar.indicators and bar.indicators.get("signal"))

                if session.trade and session.state == TradeState.IN_POSITION and not session.manage_inflight:
                    await ws.send_json(
                        StreamBarMessage(type="bar", mode="realtime", symbol=sym, bar=bar).model_dump()
                    )
                    await send_state(sym)
                    try:
                        pm_payload = await autopilot_run_manage_position(
                            ws,
                            mode="realtime",
                            sem=llm_sem,
                            analysis_service=analysis_service,
                            session=session,
                            bar_time=str(bar.t),
                            ohlcv_1m=None,
                            last_state_sent=last_state_sent,
                            after_position=after_position,
                        )
                    except Exception as e:
                        print(f"Auto-PositionManage failed for {sym}: {e}")
                        pm_payload = None
                    if session.trade is not None:
                        continue

                trigger_reason = autopilot_maybe_trigger_analysis(
                    session=session,
                    bar=bar,
                    has_quant_signal=has_quant_signal,
                    last_analyzed_time=last_analyzed_time,
                )
                await ws.send_json(
                    StreamBarMessage(
                        type="bar",
                        mode="realtime",
                        symbol=sym,
                        analysis_trigger_reason=trigger_reason,
                        bar=bar,
                    ).model_dump()
                )
                await send_state(sym)

                if trigger_reason:
                    intraday_slice = intraday_buffers[sym][-analysis_window_minutes:]
                    df_intraday = autopilot_to_intraday_df(intraday_slice, sym)
                    try:
                        await autopilot_run_analysis(
                            ws,
                            mode="realtime",
                            sem=llm_sem,
                            analysis_service=analysis_service,
                            option_chain_service=option_chain_service,
                            session=session,
                            bar_time=str(bar.t),
                            trigger_reason=trigger_reason,
                            intraday_df=df_intraday,
                            daily_df=daily_bars_df.get(sym),
                            last_state_sent=last_state_sent,
                            after_analysis=after_analysis,
                        )
                    except Exception as e:
                        print(f"Auto-Analysis failed for {sym}: {e}")
        except WebSocketDisconnect:
            return
        except Exception as e:
            try:
                await ws.send_json({"type": "error", "message": str(e)})
            except Exception:
                pass
            try:
                await ws.close()
            except Exception:
                pass

    @app.websocket("/ws/playback")
    async def ws_playback(
        ws: WebSocket,
        symbols: str = Query(default="AAPL,MSFT,NVDA,TSLA,SPY,AMD"),
        analyze: bool = Query(default=False),
        analysis_window_minutes: int = Query(default=300, ge=30, le=2000),
        start: str | None = Query(default=None),
        speed: float = Query(default=1.0, ge=0.05, le=60.0),
        flow: str = Query(default="timer"),
        limit: int = Query(default=600, ge=50, le=10000),
        cursor: int = Query(default=200, ge=0, le=10000),
    ) -> None:
        await ws.accept()
        symbol_list = [s.strip().upper() for s in symbols.split(",") if s.strip()]
        sessions: dict[str, SymbolSession] = {sym: SymbolSession(symbol=sym, mode="playback") for sym in symbol_list}
        last_analyzed_time: dict[str, str] = {}
        last_state_sent: dict[str, tuple[str, int | None]] = {}
        llm_sem = asyncio.Semaphore(2)
        intraday_buffers: dict[str, list] = {sym: [] for sym in symbol_list}
        try:
            chart_minutes = DEFAULT_CHART_WINDOW_MINUTES
            keep_n = analysis_keep_minutes(analysis_window_minutes)
            request_start, request_end, effective_limit, boot = playback_initial_fetch_window(
                start=start,
                analysis_window_minutes=analysis_window_minutes,
                requested_limit=limit,
                chart_window_minutes=chart_minutes,
            )
            start_dt = parse_iso_z(start) if start else None
            
            # Initialize indicators with history relative to playback start
            indicators: dict[str, ZScoreMomentum] = {}
            macd_indicators: dict[str, MACD] = {}
            if start_dt:
                daily_end = (start_dt - timedelta(days=1)).date().isoformat()
                daily_start = (start_dt - timedelta(days=60)).date().isoformat()
                daily_bars = await alpaca.get_bars(symbol_list, timeframe="1Day", start=daily_start, end=daily_end, limit=100)
                for sym in symbol_list:
                    bars = daily_bars.get(sym, [])
                    indicators[sym] = ZScoreMomentum([b.model_dump() for b in bars])
                    macd_indicators[sym] = MACD()
            else:
                # Default to recent history if no start time
                today = datetime.now(ZoneInfo("America/New_York")).date()
                daily_start = (today - timedelta(days=60)).isoformat()
                daily_bars = await alpaca.get_bars(symbol_list, timeframe="1Day", start=daily_start, limit=100)
                for sym in symbol_list:
                    bars = daily_bars.get(sym, [])
                    indicators[sym] = ZScoreMomentum([b.model_dump() for b in bars])
                    macd_indicators[sym] = MACD()

            daily_bars_df: dict[str, pd.DataFrame | None] = {
                sym: autopilot_to_daily_df(daily_bars.get(sym, [])) for sym in symbol_list
            }

            if request_start:
                bars_by_symbol = await alpaca.get_bars(
                    symbol_list,
                    timeframe="1Min",
                    start=request_start,
                    end=request_end,
                    limit=effective_limit,
                )
            else:
                bars_by_symbol = await alpaca.get_bars(symbol_list, timeframe="1Min", limit=effective_limit)
            if all(len(v) == 0 for v in bars_by_symbol.values()):
                bars_by_symbol = await alpaca.get_bars(symbol_list, timeframe="1Min", limit=effective_limit)
            safe_cursor = cursor
            
            # Pre-calculate indicators for all bars
            for sym, bars in bars_by_symbol.items():
                if sym in indicators:
                    # We need to re-run indicator update from start of bars to ensure EMA state is correct
                    # But if we jump via cursor, we might miss state updates. 
                    # For simplicity in playback, we re-run all from index 0 of fetched bars.
                    # Ideally we should fetch more warmup bars.
                    for bar in bars:
                        z_res = indicators[sym].update(float(bar.c))
                        m_res = macd_indicators[sym].update(float(bar.c))
                        
                        final_signal = None
                        if z_res.get('signal') == 'long':
                            final_signal = 'long'
                        elif z_res.get('signal') == 'short':
                            final_signal = 'short'
                        
                        bar.indicators = {**z_res, **m_res, "signal": final_signal}

            end_by_symbol: dict[str, int] = {}
            prefetch_inflight = False
            forward_chunk_minutes = DEFAULT_PLAYBACK_FORWARD_CHUNK_MINUTES
            prefetch_low_watermark = DEFAULT_PLAYBACK_PREFETCH_LOW_WATERMARK_MINUTES

            async def maybe_prefetch_more(current_i: int) -> None:
                nonlocal prefetch_inflight
                if prefetch_inflight:
                    return
                remaining = [len(bars) - current_i for bars in bars_by_symbol.values()]
                if not remaining or min(remaining) > prefetch_low_watermark:
                    return
                last_times: list[datetime] = []
                for bars in bars_by_symbol.values():
                    if bars:
                        last_times.append(parse_iso_z(str(bars[-1].t)))
                if not last_times:
                    return

                prefetch_inflight = True
                try:
                    common_start = to_iso_z(min(last_times) + timedelta(minutes=1))
                    fetched = await alpaca.get_bars(
                        symbol_list,
                        timeframe="1Min",
                        start=common_start,
                        limit=forward_chunk_minutes,
                    )
                    for sym in symbol_list:
                        existing = bars_by_symbol.get(sym, [])
                        new_bars = fetched.get(sym, []) or []
                        if not existing:
                            bars_by_symbol[sym] = new_bars
                            continue
                        last_dt = parse_iso_z(str(existing[-1].t))
                        for bar in new_bars:
                            bar_dt = parse_iso_z(str(bar.t))
                            if bar_dt <= last_dt:
                                continue
                            if sym in indicators:
                                z_res = indicators[sym].update(float(bar.c))
                                m_res = macd_indicators[sym].update(float(bar.c))
                                final_signal = None
                                if z_res.get("signal") == "long":
                                    final_signal = "long"
                                elif z_res.get("signal") == "short":
                                    final_signal = "short"
                                bar.indicators = {**z_res, **m_res, "signal": final_signal}
                            existing.append(bar)
                finally:
                    prefetch_inflight = False

            async def send_state(sym: str) -> None:
                s = sessions.get(sym)
                if not s:
                    return
                await autopilot_send_state(ws, session=s, mode="playback", last_state_sent=last_state_sent)

            async def wait_for_ack(expected_i: int) -> bool:
                try:
                    while True:
                        msg = await asyncio.wait_for(ws.receive_json(), timeout=60.0)
                        if not isinstance(msg, dict):
                            continue
                        if msg.get("type") != "ack":
                            continue
                        ack_i = msg.get("i")
                        if isinstance(ack_i, int) and ack_i == expected_i:
                            return True
                except asyncio.TimeoutError:
                    return False

            for sym, bars in bars_by_symbol.items():
                target_end_index = safe_cursor
                if start_dt:
                    last_le: int | None = None
                    first_ge: int | None = None
                    for idx, bar in enumerate(bars):
                        bar_dt = datetime.fromisoformat(bar.t.replace("Z", "+00:00"))
                        if bar_dt <= start_dt:
                            last_le = idx
                            continue
                        first_ge = idx
                        break
                    anchor = last_le if last_le is not None else first_ge
                    if anchor is None:
                        target_end_index = len(bars)
                    else:
                        target_end_index = max(target_end_index, anchor + 1)
                
                end = min(int(target_end_index), len(bars))
                end_by_symbol[sym] = end
                start_i = max(0, end - chart_minutes)
                init = bars[start_i:end]

                await ws.send_json(
                    StreamInitMessage(type="init", mode="playback", symbol=sym, bars=init, cursor=end).model_dump()
                )
                await send_state(sym)

            nonempty = [v for v in end_by_symbol.values() if v > 0]
            i = min(nonempty) if nonempty else 0
            if analyze and i > 0:
                for sym, bars in bars_by_symbol.items():
                    start_fill = max(0, i - keep_n)
                    intraday_buffers[sym] = list(bars[start_fill:i])
            while True:
                await maybe_prefetch_more(i)
                any_sent = False
                for sym, bars in bars_by_symbol.items():
                    if i < len(bars):
                        bar = bars[i]
                        any_sent = True

                        if analyze:
                            intraday_buffers[sym].append(bar)
                            intraday_buffers[sym] = intraday_buffers[sym][-keep_n:]

                            session = sessions.get(sym)
                            if session:
                                session.last_bar_time = str(bar.t)
                                now_epoch = _to_epoch_seconds(str(bar.t))
                                session.update_watches(now_epoch)
                                has_quant_signal = bool(bar.indicators and bar.indicators.get("signal"))

                                if session.trade and session.state == TradeState.IN_POSITION and not session.manage_inflight:
                                    await ws.send_json(
                                        StreamBarMessage(type="bar", mode="playback", symbol=sym, bar=bar, i=i).model_dump()
                                    )
                                    await send_state(sym)
                                    try:
                                        pm_payload = await autopilot_run_manage_position(
                                            ws,
                                            mode="playback",
                                            sem=llm_sem,
                                            analysis_service=analysis_service,
                                            session=session,
                                            bar_time=str(bar.t),
                                            ohlcv_1m=None,
                                            last_state_sent=last_state_sent,
                                        )
                                    except Exception as e:
                                        print(f"Auto-PositionManage failed for {sym}: {e}")
                                        pm_payload = None
                                    if session.trade is not None:
                                        continue

                                trigger_reason = autopilot_maybe_trigger_analysis(
                                    session=session,
                                    bar=bar,
                                    has_quant_signal=has_quant_signal,
                                    last_analyzed_time=last_analyzed_time,
                                )
                                await ws.send_json(
                                    StreamBarMessage(
                                        type="bar",
                                        mode="playback",
                                        symbol=sym,
                                        analysis_trigger_reason=trigger_reason,
                                        bar=bar,
                                        i=i,
                                    ).model_dump()
                                )
                                await send_state(sym)

                                if trigger_reason:
                                    intraday_slice = intraday_buffers[sym][-analysis_window_minutes:]
                                    df_intraday = autopilot_to_intraday_df(intraday_slice, sym)
                                    try:
                                        await autopilot_run_analysis(
                                            ws,
                                            mode="playback",
                                            sem=llm_sem,
                                            analysis_service=analysis_service,
                                            option_chain_service=option_chain_service,
                                            session=session,
                                            bar_time=str(bar.t),
                                            trigger_reason=trigger_reason,
                                            intraday_df=df_intraday,
                                            daily_df=daily_bars_df.get(sym),
                                            last_state_sent=last_state_sent,
                                        )
                                    except Exception as e:
                                        print(f"Auto-Analysis failed for {sym}: {e}")
                        else:
                            await ws.send_json(
                                StreamBarMessage(type="bar", mode="playback", symbol=sym, bar=bar, i=i).model_dump()
                            )

                if not any_sent:
                    break
                if flow == "ack":
                    ok = await wait_for_ack(i)
                    if not ok:
                        await ws.send_json({"type": "error", "message": "Replay ack timeout"})
                        await ws.close()
                        return
                else:
                    await asyncio.sleep(speed)
                i += 1
            await ws.send_json(StreamDoneMessage(type="done", mode="playback", cursor=i).model_dump())
            await ws.close()
        except WebSocketDisconnect:
            return
        except Exception as e:
            try:
                await ws.send_json({"type": "error", "message": str(e)})
            except Exception:
                pass
            try:
                await ws.close()
            except Exception:
                pass

    return app


app = create_app()
