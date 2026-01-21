from __future__ import annotations

import asyncio
import time
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from typing import Annotated

from fastapi import FastAPI, Query, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .alpaca_client import AlpacaClient
from .openrouter_client import OpenRouterClient
from .analysis_service import AnalysisService
from .schemas import (
    AIVerificationRequest,
    StreamBarMessage,
    StreamDoneMessage,
    StreamInitMessage,
    StreamAnalysisMessage,
    LLMAnalysisRequest,
    LLMAnalysisResponse,
    TradingSettings,
)
from .settings import get_settings
from .indicators import ZScoreMomentum, MACD
import pandas as pd


def create_app() -> FastAPI:
    settings = get_settings()
    alpaca = AlpacaClient(settings)
    ai = OpenRouterClient(settings)
    analysis_service = AnalysisService(alpaca)
    assets_lock = asyncio.Lock()
    assets_cache: dict[str, object] = {"expires_at": 0.0, "assets": []}
    assets_ttl_seconds = 6 * 60 * 60
    paper_auto_trade_enabled = False

    app = FastAPI(title="0DTE Copilot API", version="0.1.0")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/api/health")
    async def health() -> dict:
        return {"ok": True}

    @app.get("/api/settings/trading", response_model=TradingSettings)
    async def get_trading_settings() -> TradingSettings:
        return TradingSettings(paper_auto_trade_enabled=paper_auto_trade_enabled)

    @app.post("/api/settings/trading", response_model=TradingSettings)
    async def set_trading_settings(payload: TradingSettings) -> TradingSettings:
        nonlocal paper_auto_trade_enabled
        paper_auto_trade_enabled = bool(payload.paper_auto_trade_enabled)
        return TradingSettings(paper_auto_trade_enabled=paper_auto_trade_enabled)

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
            return response
        except Exception as e:
            print(f"Analysis Error: {e}")
            raise HTTPException(status_code=500, detail=str(e))

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

                if (
                    analyze
                    and bar.indicators
                    and bar.indicators.get("signal")
                    and last_analyzed_time.get(sym) != bar.t
                ):
                    try:
                        last_analyzed_time[sym] = bar.t

                        intraday_slice = intraday_buffers[sym][-analysis_window_minutes:]
                        df_intraday = pd.DataFrame([b.model_dump() for b in intraday_slice])
                        if not df_intraday.empty:
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

                            analysis_req = LLMAnalysisRequest(symbol=sym, current_time=bar.t)
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
        limit: int = Query(default=600, ge=50, le=10000),
        cursor: int = Query(default=200, ge=0, le=10000),
    ) -> None:
        await ws.accept()
        symbol_list = [s.strip().upper() for s in symbols.split(",") if s.strip()]
        try:
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
                                    analysis_req = LLMAnalysisRequest(
                                        symbol=sym,
                                        current_time=bar.t
                                    )
                                    
                                    llm_res = await analysis_service.analyze_signal(
                                        analysis_req,
                                        preloaded_daily_bars=df_daily,
                                        preloaded_intraday_bars=df_intraday
                                    )
                                    
                                    await ws.send_json(
                                        StreamAnalysisMessage(
                                            type="analysis", 
                                            mode="playback", 
                                            symbol=sym, 
                                            result=llm_res
                                        ).model_dump()
                                    )
                                
                            except Exception as e:
                                print(f"Auto-Analysis failed for {sym}: {e}")
                                pass

                if not any_sent:
                    break
                i += 1
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
