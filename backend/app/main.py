from __future__ import annotations

import asyncio
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
from .trade_session import SymbolSession, TradeState, _to_epoch_seconds
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
    paper_auto_trade_enabled = False
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
            paper_auto_trade_enabled=paper_auto_trade_enabled,
            live_trading_enabled=live_trading_enabled,
            default_execution=default_execution.value,
        )

    @app.post("/api/settings/trading", response_model=TradingSettings)
    async def set_trading_settings(payload: TradingSettings) -> TradingSettings:
        nonlocal paper_auto_trade_enabled
        nonlocal live_trading_enabled
        nonlocal default_execution
        paper_auto_trade_enabled = bool(payload.paper_auto_trade_enabled)
        live_trading_enabled = bool(payload.live_trading_enabled)
        default_execution = ExecutionMode(payload.default_execution)
        return TradingSettings(
            paper_auto_trade_enabled=paper_auto_trade_enabled,
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

        return {
            "server_time": server_time,
            "session": session,
            "is_open": is_open,
            "next_open": next_open,
            "next_close": next_close,
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
            if isinstance(plan, dict) and plan.get("trade_id"):
                trade_id = str(plan.get("trade_id"))
                ledger.upsert_trade(
                    {
                        "trade_id": trade_id,
                        "symbol": str(payload.get("symbol") or request.symbol).upper(),
                        "mode": str(getattr(request, "mode", "realtime") or "realtime"),
                        "execution": "paper" if paper_auto_trade_enabled else "simulated",
                        "option_symbol": None,
                        "option_right": plan.get("option", {}).get("right") if isinstance(plan.get("option"), dict) else None,
                        "option_expiration": plan.get("option", {}).get("expiration") if isinstance(plan.get("option"), dict) else None,
                        "option_strike": plan.get("option", {}).get("strike") if isinstance(plan.get("option"), dict) else None,
                        "contracts_total": plan.get("contracts"),
                        "contracts_remaining": plan.get("contracts"),
                        "entry_time": payload.get("timestamp"),
                    }
                )
                ledger.append_event(
                    trade_id=trade_id,
                    event_type="ai_verify_result",
                    timestamp=str(payload.get("timestamp") or ""),
                    analysis_id=str(payload.get("analysis_id") or ""),
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

        return {"prev_close": prev_close}

    @app.get("/api/ai/history/{symbol}")
    async def ai_history(symbol: str) -> dict:
        sym = symbol.strip().upper()
        if not sym:
            raise HTTPException(status_code=400, detail="symbol required")
        return {
            "symbol": sym,
            "analysis": [r.model_dump() for r in analysis_history.get(sym, [])],
            "positions": [r.model_dump() for r in position_history.get(sym, [])],
        }

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
        return await option_chain_service.build_chain(
            underlying=underlying,
            asof=asof,
            strikes_around_atm=strikes_around_atm,
            options_feed=feed,
        )

    @app.get("/api/options/quotes")
    async def options_quotes(
        symbols: Annotated[str, Query(min_length=1)],
        start: Annotated[str | None, Query()] = None,
        end: Annotated[str | None, Query()] = None,
        limit: Annotated[int, Query(ge=1, le=10000)] = 1000,
    ) -> dict:
        symbol_list = [s.strip().upper() for s in symbols.split(",") if s.strip()]
        quotes = await alpaca.get_option_quotes(symbol_list, start=start, end=end, limit=limit)
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
            timestamp=req.bar_time,
            bar_time=req.bar_time,
            payload={"symbol": req.symbol, "execution": "paper" if paper_auto_trade_enabled else "simulated"},
        )
        res = await analysis_service.manage_position(req)
        _append_position_history(res)
        payload = res.model_dump()
        ledger.append_event(
            trade_id=req.trade_id,
            event_type="position_mgmt_result",
            timestamp=str(payload.get("timestamp") or req.bar_time),
            analysis_id=str(payload.get("analysis_id") or ""),
            bar_time=req.bar_time,
            payload=payload,
        )
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
            in_pos = bool(s.trade and s.state == TradeState.IN_POSITION and s.trade.contracts_remaining > 0)
            rem = s.trade.contracts_remaining if s.trade else None
            key = (s.state.value, rem if isinstance(rem, int) else None)
            if last_state_sent.get(sym) == key:
                return
            last_state_sent[sym] = key
            await ws.send_json(
                StreamStateMessage(
                    type="state",
                    mode="realtime",
                    symbol=sym,
                    state=s.state.value,
                    in_position=in_pos,
                    contracts_total=s.trade.contracts_total if s.trade else None,
                    contracts_remaining=rem,
                    trade_id=s.trade.trade_id if s.trade else None,
                    option=s.trade.option if s.trade else None,
                    option_symbol=s.trade.option_symbol if s.trade else None,
                ).model_dump()
            )
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
            backfill_minutes = max(analysis_window_minutes, 200) + 50
            backfill_start = (now_utc - timedelta(minutes=backfill_minutes)).isoformat().replace("+00:00", "Z")
            backfill_end = now_utc.isoformat().replace("+00:00", "Z")

            async def fetch_intraday(sym: str) -> tuple[str, list]:
                data = await alpaca.get_bars([sym], timeframe="1Min", start=backfill_start, end=backfill_end, limit=200)
                bars = data.get(sym, [])
                if not bars:
                    data = await alpaca.get_bars([sym], timeframe="1Min", limit=200)
                    bars = data.get(sym, [])
                return sym, bars

            backfill_pairs = await asyncio.gather(*[fetch_intraday(sym) for sym in symbol_list])
            backfill: dict[str, list] = {sym: bars for sym, bars in backfill_pairs}

            for sym in symbol_list:
                bars = backfill.get(sym, [])
                # Process backfill to warmup indicators
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
                
                await ws.send_json(StreamInitMessage(type="init", mode="realtime", symbol=sym, bars=bars).model_dump())
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
                        
                    bar.indicators = {**z_res, **m_res, "signal": final_signal}
                    intraday_buffers[sym].append(bar)
                    intraday_buffers[sym] = intraday_buffers[sym][-max(analysis_window_minutes + 50, 250):]
                await ws.send_json(StreamBarMessage(type="bar", mode="realtime", symbol=sym, bar=bar).model_dump())

                session = sessions.get(sym)
                if not analyze or not session:
                    continue

                session.last_bar_time = bar.t
                now_epoch = _to_epoch_seconds(bar.t)
                session.update_watches(now_epoch)

                has_quant_signal = bool(bar.indicators and bar.indicators.get("signal"))

                await send_state(sym)

                async def run_analysis() -> None:
                    async with llm_sem:
                        session.analysis_inflight = True
                        session.state = TradeState.AI_VERIFY
                        await send_state(sym)
                        intraday_slice = intraday_buffers[sym][-analysis_window_minutes:]
                        df_intraday = pd.DataFrame([b.model_dump() for b in intraday_slice])
                        if df_intraday.empty:
                            return
                        df_intraday["timestamp"] = pd.to_datetime(df_intraday["t"])
                        df_intraday.set_index("timestamp", inplace=True)
                        df_intraday.rename(
                            columns={"o": "open", "h": "high", "l": "low", "c": "close", "v": "volume"},
                            inplace=True,
                        )
                        df_intraday["symbol"] = sym
                        if "indicators" in df_intraday.columns:
                            df_intraday.drop(columns=["indicators"], inplace=True)
                        df_intraday.sort_index(inplace=True)
                        analysis_req = LLMAnalysisRequest(symbol=sym, current_time=bar.t, mode="realtime")
                        llm_res = await analysis_service.analyze_signal(
                            analysis_req,
                            preloaded_daily_bars=daily_bars_df.get(sym),
                            preloaded_intraday_bars=df_intraday,
                        )
                        await ws.send_json(
                            StreamAnalysisMessage(
                                type="analysis",
                                mode="realtime",
                                symbol=sym,
                                result=llm_res,
                            ).model_dump()
                        )
                        payload = llm_res.model_dump()
                        session.on_analysis_result(payload)
                        if payload.get("action") in ("buy_long", "buy_short") and isinstance(payload.get("trade_plan"), dict):
                            plan = payload.get("trade_plan") or {}
                            opt = plan.get("option") if isinstance(plan.get("option"), dict) else {}
                            option_symbol: str | None = None
                            try:
                                exp = str(opt.get("expiration") or "")
                                right = str(opt.get("right") or "").lower()
                                strike = float(opt.get("strike") or 0.0)
                                if exp and right and strike:
                                    contracts = await option_chain_service.get_contracts(
                                        sym,
                                        asof_date=None,
                                        expiration_date_gte=exp,
                                        expiration_date_lte=exp,
                                        limit=1000,
                                    )
                                    for c in contracts:
                                        try:
                                            if str(c.get("type") or "").lower() != right:
                                                continue
                                            if str(c.get("expiration_date") or "") != exp:
                                                continue
                                            if abs(float(c.get("strike_price") or 0.0) - strike) > 1e-6:
                                                continue
                                            s2 = str(c.get("symbol") or "").upper()
                                            if s2:
                                                option_symbol = s2
                                                break
                                        except Exception:
                                            continue
                            except Exception:
                                option_symbol = None
                            session.enter_from_trade_plan(payload, option_symbol=option_symbol)
                        session.analysis_inflight = False
                        if session.state == TradeState.AI_VERIFY:
                            session.state = TradeState.SCAN
                        await send_state(sym)

                async def run_manage() -> None:
                    if not session.trade:
                        return
                    async with llm_sem:
                        session.manage_inflight = True
                        req_pm = PositionManagementRequest(
                            trade_id=session.trade.trade_id,
                            symbol=sym,
                            bar_time=bar.t,
                            position={
                                "direction": session.trade.direction,
                                "option": session.trade.option,
                                "contracts_total": session.trade.contracts_total,
                                "contracts_remaining": session.trade.contracts_remaining,
                                "entry": {"time": session.trade.entry_time, "premium": session.trade.entry_premium},
                                "risk": {
                                    "stop_loss_premium": session.trade.risk.get("stop_loss_premium"),
                                    "take_profit_premium": session.trade.risk.get("take_profit_premium"),
                                    "time_stop_minutes": session.trade.risk.get("time_stop_minutes"),
                                },
                            },
                            option_symbol=session.trade.option_symbol,
                            ohlcv_1m=None,
                        )
                        pm_res = await analysis_service.manage_position(req_pm)
                        await ws.send_json(
                            StreamPositionMessage(
                                type="position",
                                mode="realtime",
                                symbol=sym,
                                result=pm_res,
                            ).model_dump()
                        )
                        session.on_position_decision(pm_res.model_dump())
                        session.manage_inflight = False
                        await send_state(sym)

                if session.trade and session.state == TradeState.IN_POSITION and not session.manage_inflight:
                    try:
                        await run_manage()
                    except Exception as e:
                        print(f"Auto-PositionManage failed for {sym}: {e}")
                    continue

                if session.watches and bar.t:
                    hit = None
                    try:
                        close_px = float(bar.c)
                        for w in sorted(session.watches, key=lambda x: x.created_at_epoch_s):
                            if w.direction == "above" and close_px >= w.trigger_price:
                                hit = w
                                break
                            if w.direction == "below" and close_px <= w.trigger_price:
                                hit = w
                                break
                    except Exception:
                        hit = None
                    if hit and not session.analysis_inflight and last_analyzed_time.get(sym) != bar.t:
                        session.watches = [w for w in session.watches if w is not hit]
                        last_analyzed_time[sym] = bar.t
                        try:
                            await run_analysis()
                        except Exception as e:
                            print(f"Auto-Analysis failed for {sym}: {e}")
                        continue

                if session.state == TradeState.FOLLOW_UP_PENDING and session.follow_up.armed and bar.t:
                    if not has_quant_signal and not session.analysis_inflight and last_analyzed_time.get(sym) != bar.t:
                        session.follow_up = session.follow_up.__class__(armed=False)
                        last_analyzed_time[sym] = bar.t
                        try:
                            await run_analysis()
                        except Exception as e:
                            print(f"Auto-Analysis failed for {sym}: {e}")
                        continue

                if has_quant_signal and not session.analysis_inflight and last_analyzed_time.get(sym) != bar.t:
                    last_analyzed_time[sym] = bar.t
                    try:
                        await run_analysis()
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
        start: str | None = Query(default=None),
        speed: float = Query(default=1.0, ge=0.05, le=60.0),
        flow: str = Query(default="timer"),
        limit: int = Query(default=600, ge=50, le=10000),
        cursor: int = Query(default=200, ge=0, le=10000),
    ) -> None:
        await ws.accept()
        symbol_list = [s.strip().upper() for s in symbols.split(",") if s.strip()]
        sessions: dict[str, SymbolSession] = {sym: SymbolSession(symbol=sym, mode="playback") for sym in symbol_list}
        try:
            warmup_minutes = 200 + 21
            warmup_minutes = 200 + 21
            base_cursor = 0
            request_start = start
            start_dt = None
            if start:
                start_dt = datetime.fromisoformat(start.replace("Z", "+00:00"))
                # We need enough history for:
                # 1. Indicator warmup (21 mins)
                # 2. Initial visible history (200 mins)
                warmup_start_dt = start_dt - timedelta(minutes=warmup_minutes)
                request_start = warmup_start_dt.isoformat().replace("+00:00", "Z")
                base_cursor = warmup_minutes
            
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

            bars_by_symbol = await alpaca.get_bars(symbol_list, timeframe="1Min", start=request_start, limit=limit)
            if all(len(v) == 0 for v in bars_by_symbol.values()):
                bars_by_symbol = await alpaca.get_bars(symbol_list, timeframe="1Min", limit=limit)
            
            # Fix: cursor is an absolute index from frontend, so we shouldn't add base_cursor to it again.
            # We use max(cursor, base_cursor) to ensure we start at least after the warmup period.
            safe_cursor = max(cursor + 200, base_cursor)
            
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

            history_padding = warmup_minutes
            for sym, bars in bars_by_symbol.items():
                # Correctly calculate slicing indices relative to the 'start' time
                # 'safe_cursor' is roughly where the playback should start (200 bars in)
                # But if we want the chart to end exactly at 'start' time, we need to find that index.
                
                # If start_dt is provided, we want the init bars to end exactly at start_dt
                target_end_index = safe_cursor
                if start_dt:
                     # Find the index of the bar closest to start_dt
                     for idx, bar in enumerate(bars):
                         bar_dt = datetime.fromisoformat(bar.t.replace("Z", "+00:00"))
                         if bar_dt >= start_dt:
                             target_end_index = idx
                             break
                     else:
                         target_end_index = len(bars)
                
                end = target_end_index
                start_i = max(0, end - 200) # Show 200 bars history
                init = bars[start_i:end]
                
                # Update i to continue from where init left off
                safe_cursor = end 
                
                await ws.send_json(
                    StreamInitMessage(type="init", mode="playback", symbol=sym, bars=init, cursor=end).model_dump()
                )
                s = sessions.get(sym)
                if s:
                    await ws.send_json(
                        StreamStateMessage(
                            type="state",
                            mode="playback",
                            symbol=sym,
                            state=s.state.value,
                            in_position=False,
                        ).model_dump()
                    )

            i = safe_cursor
            while True:
                any_sent = False
                for sym, bars in bars_by_symbol.items():
                    if i < len(bars):
                        bar = bars[i]
                        await ws.send_json(
                            StreamBarMessage(type="bar", mode="playback", symbol=sym, bar=bar, i=i).model_dump()
                        )
                        any_sent = True
                        
                        if bar.indicators and bar.indicators.get("signal"):
                            try:
                                daily_list = daily_bars.get(sym, [])
                                df_daily = pd.DataFrame([b.model_dump() for b in daily_list])
                                if not df_daily.empty:
                                    df_daily['timestamp'] = pd.to_datetime(df_daily['t'])
                                    df_daily.set_index('timestamp', inplace=True)
                                    df_daily.rename(columns={'o': 'open', 'h': 'high', 'l': 'low', 'c': 'close', 'v': 'volume'}, inplace=True)
                                else:
                                    df_daily = None

                                start_slice = max(0, i - 300)
                                intraday_slice = bars[start_slice : i+1]
                                df_intraday = pd.DataFrame([b.model_dump() for b in intraday_slice])
                                if not df_intraday.empty:
                                    df_intraday['timestamp'] = pd.to_datetime(df_intraday['t'])
                                    df_intraday.set_index('timestamp', inplace=True)
                                    df_intraday.rename(columns={'o': 'open', 'h': 'high', 'l': 'low', 'c': 'close', 'v': 'volume'}, inplace=True)
                                    df_intraday['symbol'] = sym
                                    if 'indicators' in df_intraday.columns:
                                        df_intraday.drop(columns=['indicators'], inplace=True)
                                else:
                                    df_intraday = None
                                
                                if df_intraday is not None:
                                    analysis_req = LLMAnalysisRequest(symbol=sym, current_time=bar.t, mode="playback")
                                    llm_res = await analysis_service.analyze_signal(
                                        analysis_req,
                                        preloaded_daily_bars=df_daily,
                                        preloaded_intraday_bars=df_intraday,
                                    )
                                    await ws.send_json(
                                        StreamAnalysisMessage(
                                            type="analysis",
                                            mode="playback",
                                            symbol=sym,
                                            result=llm_res,
                                        ).model_dump()
                                    )
                                
                            except Exception as e:
                                print(f"Auto-Analysis failed for {sym}: {e}")
                                pass

                if not any_sent:
                    break
                i += 1
                if flow == "ack":
                    try:
                        msg = await asyncio.wait_for(ws.receive_json(), timeout=60.0)
                        if isinstance(msg, dict) and msg.get("type") == "ack":
                            pass
                    except asyncio.TimeoutError:
                        pass
                else:
                    await asyncio.sleep(speed)
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
