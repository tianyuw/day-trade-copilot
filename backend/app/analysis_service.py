import asyncio
import hashlib
import time
import json
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from typing import Dict, Any, List
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame

from .plotting import generate_chart_image
from .llm_client import LLMClient
from .llm_prompts import get_llm_system_prompt
from .schemas import (
    LLMAnalysisRequest,
    LLMAnalysisResponse,
    PositionManagementRequest,
    PositionManagementResponse,
)
from .indicators import ZScoreMomentum, MACD
from .options_service import OptionChainService
import os

class AnalysisService:
    def __init__(self, alpaca_client: Any):
        self.alpaca = alpaca_client
        self.llm_client = LLMClient()
        self.option_chain_service = OptionChainService(alpaca_client)
        self._analysis_cache: dict[str, tuple[float, LLMAnalysisResponse]] = {}
        self._analysis_inflight: dict[str, asyncio.Task[LLMAnalysisResponse]] = {}
        self._cache_lock = asyncio.Lock()
        self._cache_ttl_seconds = int(os.getenv("ANALYSIS_CACHE_TTL_SECONDS", "21600"))
        self._prompt_hash = hashlib.sha256(get_llm_system_prompt().encode("utf-8")).hexdigest()
        self._model_hint = (
            os.getenv("GOOGLE_MODEL", "gemini-3-flash-preview")
            if os.getenv("GOOGLE_API_KEY")
            else os.getenv("OPENROUTER_MODEL", "google/gemini-3-flash-preview")
        )
        self._daily_bars_cache: dict[str, tuple[float, pd.DataFrame]] = {}
        self._daily_bars_cache_ttl_seconds = 6 * 60 * 60

    async def _get_daily_bars_df_cached(self, symbol: str, end: datetime) -> pd.DataFrame:
        now = time.time()
        cached = self._daily_bars_cache.get(symbol)
        if cached and cached[0] > now:
            return cached[1]

        start = end - timedelta(days=60)
        df = await self._get_bars_df(symbol, "1Day", start, end, 100)
        self._daily_bars_cache[symbol] = (time.time() + self._daily_bars_cache_ttl_seconds, df)
        return df

    async def _get_bars_df(
        self,
        symbol: str,
        timeframe: str,
        start: datetime,
        end: datetime,
        limit: int,
    ) -> pd.DataFrame:
        if hasattr(self.alpaca, "get_bars"):
            start_iso = start.isoformat().replace("+00:00", "Z")
            end_iso = end.isoformat().replace("+00:00", "Z")
            data = await self.alpaca.get_bars([symbol], timeframe=timeframe, start=start_iso, end=end_iso, limit=limit)
            bars = data.get(symbol, [])
            df = pd.DataFrame([b.model_dump() for b in bars])
            if df.empty:
                return df
            df["timestamp"] = pd.to_datetime(df["t"])
            df.set_index("timestamp", inplace=True)
            df.rename(columns={"o": "open", "h": "high", "l": "low", "c": "close", "v": "volume"}, inplace=True)
            df.sort_index(inplace=True)
            return df

        if hasattr(self.alpaca, "get_stock_bars"):
            tf = TimeFrame.Day if timeframe == "1Day" else TimeFrame.Minute
            req = StockBarsRequest(
                symbol_or_symbols=symbol,
                timeframe=tf,
                start=start,
                end=end,
                limit=limit,
            )
            df = self.alpaca.get_stock_bars(req).df
            if df is None or df.empty:
                return pd.DataFrame()
            if isinstance(df.index, pd.MultiIndex):
                df = df.reset_index()
            if "timestamp" in df.columns:
                df["timestamp"] = pd.to_datetime(df["timestamp"])
                df.set_index("timestamp", inplace=True)
            df.sort_index(inplace=True)
            return df

        raise AttributeError("Alpaca client must provide get_bars or get_stock_bars")

    def _sma_last(self, close: pd.Series, window: int) -> float | None:
        if close is None or close.empty:
            return None
        if len(close) < window:
            return None
        v = close.rolling(window=window).mean().iloc[-1]
        try:
            return float(v)
        except Exception:
            return None

    def _stable_analysis_id(self, symbol: str, current_time: str) -> str:
        raw = f"{symbol}|{current_time}|{self._model_hint}|{self._prompt_hash}"
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()

    async def analyze_signal(
        self, 
        request: LLMAnalysisRequest, 
        preloaded_daily_bars: pd.DataFrame = None, 
        preloaded_intraday_bars: pd.DataFrame = None
    ) -> LLMAnalysisResponse:
        analysis_id = self._stable_analysis_id(request.symbol, request.current_time)
        now = time.monotonic()

        async with self._cache_lock:
            cached = self._analysis_cache.get(analysis_id)
            if cached and cached[0] > now:
                return cached[1]

            inflight = self._analysis_inflight.get(analysis_id)
            if inflight is None:
                inflight = asyncio.create_task(
                    self._analyze_signal_uncached(
                        request,
                        preloaded_daily_bars=preloaded_daily_bars,
                        preloaded_intraday_bars=preloaded_intraday_bars,
                    )
                )
                self._analysis_inflight[analysis_id] = inflight

        try:
            response = await inflight
        finally:
            async with self._cache_lock:
                if self._analysis_inflight.get(analysis_id) is inflight:
                    self._analysis_inflight.pop(analysis_id, None)

        response = response.model_copy(update={"analysis_id": analysis_id})
        async with self._cache_lock:
            self._analysis_cache[analysis_id] = (time.monotonic() + self._cache_ttl_seconds, response)
        return response

    async def get_cached_analysis(self, analysis_id: str) -> LLMAnalysisResponse | None:
        now = time.monotonic()
        async with self._cache_lock:
            cached = self._analysis_cache.get(analysis_id)
            if cached and cached[0] > now:
                return cached[1]
            if cached:
                self._analysis_cache.pop(analysis_id, None)
        return None

    async def _analyze_signal_uncached(
        self,
        request: LLMAnalysisRequest,
        preloaded_daily_bars: pd.DataFrame = None,
        preloaded_intraday_bars: pd.DataFrame = None,
    ) -> LLMAnalysisResponse:
        # 1. Parse current time
        current_dt = datetime.fromisoformat(request.current_time.replace("Z", "+00:00"))
        symbol = request.symbol

        # 2. Fetch Data (if not provided)
        if preloaded_daily_bars is not None:
            daily_bars = preloaded_daily_bars
        else:
            daily_start = (current_dt - timedelta(days=90)).date()
            daily_end = (current_dt.date() - timedelta(days=1))
            if hasattr(self.alpaca, "get_stock_bars"):
                daily_req = StockBarsRequest(
                    symbol_or_symbols=symbol,
                    timeframe=TimeFrame.Day,
                    start=daily_start,
                    end=daily_end,
                    limit=60,
                )
                daily_bars = self.alpaca.get_stock_bars(daily_req).df
            elif hasattr(self.alpaca, "get_bars"):
                start_iso = f"{daily_start.isoformat()}T00:00:00Z"
                end_iso = f"{daily_end.isoformat()}T23:59:59Z"
                daily_dict = await self.alpaca.get_bars([symbol], timeframe="1Day", start=start_iso, end=end_iso, limit=60)
                daily_list = daily_dict.get(symbol, [])
                df_daily = pd.DataFrame([b.model_dump() for b in daily_list])
                if df_daily.empty:
                    daily_bars = df_daily
                else:
                    df_daily["timestamp"] = pd.to_datetime(df_daily["t"])
                    df_daily.set_index("timestamp", inplace=True)
                    df_daily.rename(
                        columns={"o": "open", "h": "high", "l": "low", "c": "close", "v": "volume"},
                        inplace=True,
                    )
                    daily_bars = df_daily
            else:
                raise AttributeError("Alpaca client must provide get_bars or get_stock_bars")
        
        if preloaded_intraday_bars is not None:
            intraday_bars = preloaded_intraday_bars
        else:
            intraday_start = current_dt - timedelta(minutes=300)
            if hasattr(self.alpaca, "get_stock_bars"):
                intraday_req = StockBarsRequest(
                    symbol_or_symbols=symbol,
                    timeframe=TimeFrame.Minute,
                    start=intraday_start,
                    end=current_dt,
                    limit=1000,
                )
                intraday_bars = self.alpaca.get_stock_bars(intraday_req).df
            elif hasattr(self.alpaca, "get_bars"):
                start_iso = intraday_start.isoformat().replace("+00:00", "Z")
                end_iso = current_dt.isoformat().replace("+00:00", "Z")
                intra_dict = await self.alpaca.get_bars([symbol], timeframe="1Min", start=start_iso, end=end_iso, limit=1000)
                intra_list = intra_dict.get(symbol, [])
                df_intra = pd.DataFrame([b.model_dump() for b in intra_list])
                if df_intra.empty:
                    intraday_bars = df_intra
                else:
                    df_intra["timestamp"] = pd.to_datetime(df_intra["t"])
                    df_intra.set_index("timestamp", inplace=True)
                    df_intra.rename(
                        columns={"o": "open", "h": "high", "l": "low", "c": "close", "v": "volume"},
                        inplace=True,
                    )
                    intraday_bars = df_intra
            else:
                raise AttributeError("Alpaca client must provide get_bars or get_stock_bars")
        
        if intraday_bars.empty:
             raise ValueError("No intraday data found")

        # Handle 'symbol' column which might be part of index or column depending on how it was loaded
        if 'symbol' not in intraday_bars.columns and isinstance(intraday_bars.index, pd.MultiIndex):
             intraday_bars = intraday_bars.reset_index()

        # If it was preloaded from dict, 'symbol' column might be there, filter if needed
        if 'symbol' in intraday_bars.columns:
            # If we passed a single symbol DF, it might already be filtered, but safe to check
            if len(intraday_bars['symbol'].unique()) > 1:
                intraday_bars = intraday_bars[intraday_bars['symbol'] == symbol]
        
        # Ensure timestamp is datetime and set as index if not already
        if 'timestamp' in intraday_bars.columns and not isinstance(intraday_bars.index, pd.DatetimeIndex):
            intraday_bars['timestamp'] = pd.to_datetime(intraday_bars['timestamp'])
            intraday_bars.set_index('timestamp', inplace=True)
        elif isinstance(intraday_bars.index, pd.DatetimeIndex):
            # Already set, ensure column exists for later use if we reset index
            pass
        elif 't' in intraday_bars.columns: # From preloaded dict dumping
             intraday_bars['timestamp'] = pd.to_datetime(intraday_bars['t'])
             intraday_bars.set_index('timestamp', inplace=True)

        intraday_bars.sort_index(inplace=True)

        # Same for daily bars
        if isinstance(daily_bars, pd.DataFrame) and not daily_bars.empty:
             if 'timestamp' in daily_bars.columns and not isinstance(daily_bars.index, pd.DatetimeIndex):
                 daily_bars['timestamp'] = pd.to_datetime(daily_bars['timestamp'])
                 daily_bars.set_index('timestamp', inplace=True)
             elif 't' in daily_bars.columns:
                 daily_bars['timestamp'] = pd.to_datetime(daily_bars['t'])
                 daily_bars.set_index('timestamp', inplace=True)
             daily_bars.sort_index(inplace=True)

            
        # 3. Calculate Indicators
        # We need to re-calculate indicators for the fetched window to pass to plotter
        # We can reuse the indicator classes or just compute manually with pandas for batch efficiency
        # Using classes to ensure consistency with main app logic
        
        # Need daily stats for Z-Score
        if daily_bars is None:
            daily_records = []
        else:
            daily_records = daily_bars.reset_index().to_dict('records') if not daily_bars.empty else []
        # Map daily bars to expected format for ZScoreMomentum
        daily_for_z = [{'c': r['close'], 't': r['timestamp']} for r in daily_records if 'close' in r and 'timestamp' in r]
        
        z_indicator = ZScoreMomentum(daily_for_z)
        macd_indicator = MACD()
        
        # Process intraday bars to generate indicator values
        bars_with_indicators = []
        indicators_list = []
        
        # Calculate Bollinger Bands & VWAP manually or via simple pandas rolling
        # For consistency with plotting, let's add them to the dict
        
        intraday_records_df = intraday_bars.reset_index()
        if "timestamp" not in intraday_records_df.columns and "t" in intraday_records_df.columns:
            intraday_records_df["timestamp"] = pd.to_datetime(intraday_records_df["t"])
        intraday_records = intraday_records_df.to_dict("records")
        
        # Pre-calc Pandas based indicators for speed
        df = intraday_bars.copy()
        # Ensure index is datetime if it isn't already (redundant check but safe)
        if not isinstance(df.index, pd.DatetimeIndex):
            if 'timestamp' in df.columns:
                 df['timestamp'] = pd.to_datetime(df['timestamp'])
                 df.set_index('timestamp', inplace=True)
            elif 't' in df.columns:
                 df['timestamp'] = pd.to_datetime(df['t'])
                 df.set_index('timestamp', inplace=True)

        
        # EMA
        df['ema9'] = df['close'].ewm(span=9, adjust=False).mean()
        df['ema21'] = df['close'].ewm(span=21, adjust=False).mean()
        
        # Bollinger Bands (20, 2)
        df['bb_middle'] = df['close'].rolling(window=20).mean()
        df['bb_std'] = df['close'].rolling(window=20).std()
        df['bb_upper'] = df['bb_middle'] + (df['bb_std'] * 2)
        df['bb_lower'] = df['bb_middle'] - (df['bb_std'] * 2)
        
        # VWAP
        df['vwap'] = (df['volume'] * (df['high'] + df['low'] + df['close']) / 3).cumsum() / df['volume'].cumsum()

        # Iterative update for Z-Score & MACD (since they have internal state in our implementation)
        # Note: Ideally we should vectorize these too, but for 300 bars it's fast enough
        
        for i, row in enumerate(intraday_records):
            close = row['close']
            z_res = z_indicator.update(close) # Returns diff, internal state updated
            m_res = macd_indicator.update(close)
            
            # Get pandas calculated values for this timestamp
            ts = row.get("timestamp")
            if ts is None and row.get("t") is not None:
                ts = pd.to_datetime(row["t"])
            
            # If df.index is DatetimeIndex, ts should be Timestamp or convertible
            # But sometimes it might be str if conversion failed earlier.
            if not isinstance(ts, pd.Timestamp):
                try:
                    ts = pd.to_datetime(ts)
                except:
                    pass
            
            try:
                pd_row = df.loc[ts]
                # If duplicate index, take the first one (shouldn't happen with 1m bars usually)
                if isinstance(pd_row, pd.DataFrame):
                    pd_row = pd_row.iloc[0]
            except KeyError:
                # Fallback: if exact timestamp match fails (e.g. timezone mismatch), try nearest or just use current row values if available
                # But we rely on df for indicators like BB/EMA which we calculated on the whole DF.
                # Let's try to find by string matching if index is string
                print(f"Warning: Timestamp {ts} not found in DataFrame index. Available: {df.index[0]}...{df.index[-1]}")
                # Fallback to manual calculation or skip?
                # For robustness, let's use the values from the current row if they were there (but they aren't, they are in df)
                # Let's just use the i-th row of df if indices are aligned
                pd_row = df.iloc[i]

            # Construct indicator dict for plotting
            ind_dict = {
                'ema9': pd_row['ema9'],
                'ema21': pd_row['ema21'],
                'vwap': pd_row['vwap'],
                'bb_upper': pd_row['bb_upper'],
                'bb_middle': pd_row['bb_middle'],
                'bb_lower': pd_row['bb_lower'],
                'macd_dif': m_res.get('macd_dif'),
                'macd_dea': m_res.get('macd_dea'),
                'macd_hist': m_res.get('macd_hist'),
                'z_score_diff': z_res.get('z_score_diff')
            }
            indicators_list.append(ind_dict)
            
            # Map bar for plotting
            bars_with_indicators.append({
                't': ts,
                'o': row['open'],
                'h': row['high'],
                'l': row['low'],
                'c': row['close'],
                'v': row['volume']
            })

        # 4. Prepare Context for LLM
        # Slice last 60 minutes for plotting
        plot_bars = bars_with_indicators[-60:]
        plot_indicators = indicators_list[-60:]
        
        # Generate Image
        chart_base64 = generate_chart_image(plot_bars, plot_indicators)
        
        # Prepare Text Context
        # Find previous day stats
        prev_day_high = 0
        prev_day_low = 0
        prev_day_close = 0
        
        if len(daily_records) >= 1:
            last_day = daily_records[-1]
            prev_day_close = last_day['close']
            prev_day_high = last_day['high']
            prev_day_low = last_day['low']
            
        open_price = intraday_records[0]['open'] # Approximation of day open if we fetched enough
        
        # Find today's high/low
        # Filter intraday for today only
        today_str = current_dt.strftime('%Y-%m-%d')
        df_today = df[df.index.strftime('%Y-%m-%d') == today_str]
        
        if not df_today.empty:
            day_high = df_today['high'].max()
            day_low = df_today['low'].min()
            open_price = df_today.iloc[0]['open']
        else:
            day_high = 0
            day_low = 0

        # Construct textual context
        context_text = f"""
Timestamp (PST): {current_dt.astimezone(ZoneInfo("America/Los_Angeles")).strftime('%Y-%m-%d %H:%M:%S')}
Symbol: {symbol}

Daily Stats (Last 60 Days):
- Daily Trend (Last 60 Days): {', '.join([f"{r['close']:.2f}" for r in daily_records])}

Previous Day Stats:
- Close: {prev_day_close:.2f}
- High: {prev_day_high:.2f}
- Low: {prev_day_low:.2f}

Intraday Stats:
- Open: {open_price:.2f}
- Day High: {day_high:.2f}
- Day Low: {day_low:.2f}
- Current Price: {intraday_records[-1]['close']:.2f}

Technical Indicators (Latest):
- EMA9: {indicators_list[-1]['ema9']:.2f}
- EMA21: {indicators_list[-1]['ema21']:.2f}
- VWAP: {indicators_list[-1]['vwap']:.2f}
- Bollinger Upper: {indicators_list[-1]['bb_upper']:.2f}
- Bollinger Middle: {indicators_list[-1]['bb_middle']:.2f}
- Bollinger Lower: {indicators_list[-1]['bb_lower']:.2f}
- MACD DIF: {indicators_list[-1]['macd_dif']:.3f}
- MACD DEA: {indicators_list[-1]['macd_dea']:.3f}
- MACD Hist: {indicators_list[-1]['macd_hist']:.3f}

Recent Price Action (Last 60 mins):
"""
        for b in bars_with_indicators[-60:]:
            t_str = b['t'].strftime('%H:%M')
            context_text += f"- {t_str}: O={b['o']:.2f}, H={b['h']:.2f}, L={b['l']:.2f}, C={b['c']:.2f}, V={b['v']}\n"

        try:
            strikes_around_atm = int(os.getenv("OPTION_CHAIN_STRIKES_AROUND_ATM", "5"))
        except Exception:
            strikes_around_atm = 5

        try:
            if getattr(request, "mode", "realtime") == "realtime":
                chain = await self.option_chain_service.get_chain_realtime(
                    underlying=symbol,
                    strikes_around_atm=strikes_around_atm,
                )
            else:
                chain = await self.option_chain_service.get_chain_asof(
                    underlying=symbol,
                    asof=request.current_time,
                    strikes_around_atm=strikes_around_atm,
                )
            exp = chain.get("expiration") if isinstance(chain, dict) else None
            underlying_px = chain.get("underlying_price") if isinstance(chain, dict) else None
            items = chain.get("items") if isinstance(chain, dict) else None
            if exp and isinstance(items, list) and items:
                px_text = ""
                try:
                    if underlying_px is not None:
                        px_text = f", Underlying≈{float(underlying_px):.2f}"
                except Exception:
                    px_text = ""
                context_text += f"\nOption Chain (Nearest Expiration: {exp}{px_text}):\n"
                for it in items:
                    if not isinstance(it, dict):
                        continue
                    q = it.get("quote") if isinstance(it.get("quote"), dict) else {}
                    bid = q.get("bid")
                    ask = q.get("ask")
                    right = it.get("right")
                    strike = it.get("strike")
                    opt_sym = it.get("symbol")
                    asof_px = it.get("asof_price")
                    if asof_px is None and bid is not None and ask is not None:
                        try:
                            asof_px = (float(bid) + float(ask)) / 2.0
                        except Exception:
                            asof_px = None
                    context_text += f"- {opt_sym} {right} {strike}: last≈{asof_px}, bid={bid}, ask={ask}\n"
        except Exception:
            pass

        # Check for Hard Exit (Stop Loss / Take Profit) before calling LLM
        if position_option_quote and req.position.risk:
            try:
                bid = float(position_option_quote.get("bid") or 0.0)
                sl = float(req.position.risk.stop_loss_premium or 0.0)
                tp = float(req.position.risk.take_profit_premium or 0.0)
                
                decision_action = None
                decision_reason = ""
                
                if sl > 0 and bid > 0 and bid <= sl:
                    decision_action = "close_all"
                    decision_reason = f"Hard Stop Loss Triggered: Current Bid ({bid:.2f}) <= Stop Loss ({sl:.2f})"
                elif tp > 0 and bid > 0 and bid >= tp:
                    decision_action = "close_all"
                    decision_reason = f"Hard Take Profit Triggered: Current Bid ({bid:.2f}) >= Take Profit ({tp:.2f})"
                
                if decision_action:
                    return PositionManagementResponse(
                        trade_id=req.trade_id,
                        analysis_id="hard_exit_rule",
                        timestamp=req.bar_time,
                        symbol=req.symbol,
                        bar_time=req.bar_time,
                        decision={
                            "action": decision_action,
                            "reasoning": decision_reason,
                            "exit": {"contracts_to_close": req.position.contracts_remaining},
                            "adjustments": None
                        },
                        position_option_quote=position_option_quote
                    )
            except Exception as e:
                print(f"Hard exit check failed: {e}")
                pass

        context_text += "\nBenchmark Context (Proxy Futures):\n"
        benchmark_symbols = [s.strip().upper() for s in os.getenv("BENCHMARK_SYMBOLS", "QQQ,SPY").split(",") if s.strip()]
        benchmark_alias = {"QQQ": "NQ", "SPY": "ES", "DIA": "YM", "IWM": "RTY"}
        bench_daily_end = current_dt
        bench_daily_start = current_dt - timedelta(days=450)
        bench_intraday_start = current_dt - timedelta(minutes=300)

        for bsym in benchmark_symbols:
            df_b_daily = await self._get_bars_df(bsym, "1Day", bench_daily_start, bench_daily_end, 500)
            df_b_intra = await self._get_bars_df(bsym, "1Min", bench_intraday_start, current_dt, 1000)

            b_last = float(df_b_intra["close"].iloc[-1]) if not df_b_intra.empty else (float(df_b_daily["close"].iloc[-1]) if not df_b_daily.empty else 0.0)
            b_prev_high = float(df_b_daily["high"].iloc[-1]) if not df_b_daily.empty and "high" in df_b_daily.columns else 0.0
            b_prev_low = float(df_b_daily["low"].iloc[-1]) if not df_b_daily.empty and "low" in df_b_daily.columns else 0.0

            b_sma20 = self._sma_last(df_b_daily["close"], 20) if not df_b_daily.empty and "close" in df_b_daily.columns else None
            b_sma50 = self._sma_last(df_b_daily["close"], 50) if not df_b_daily.empty and "close" in df_b_daily.columns else None
            b_sma100 = self._sma_last(df_b_daily["close"], 100) if not df_b_daily.empty and "close" in df_b_daily.columns else None
            b_sma200 = self._sma_last(df_b_daily["close"], 200) if not df_b_daily.empty and "close" in df_b_daily.columns else None

            alias = benchmark_alias.get(bsym)
            alias_text = f"(≈ {alias})" if alias else ""
            context_text += f"""
- {bsym} {alias_text}
  - Current Price: {b_last:.2f}
  - Previous Day High: {b_prev_high:.2f}
  - Previous Day Low: {b_prev_low:.2f}
  - Daily SMA20: {b_sma20 if b_sma20 is not None else "N/A"}
  - Daily SMA50: {b_sma50 if b_sma50 is not None else "N/A"}
  - Daily SMA100: {b_sma100 if b_sma100 is not None else "N/A"}
  - Daily SMA200: {b_sma200 if b_sma200 is not None else "N/A"}
  - Recent 1m Price Action (Last 20 mins):
"""
            if not df_b_intra.empty:
                df_tail = df_b_intra.tail(20)
                for ts_i, r_i in df_tail.iterrows():
                    t_str = ts_i.strftime('%H:%M')
                    context_text += f"    - {t_str}: O={float(r_i['open']):.2f}, H={float(r_i['high']):.2f}, L={float(r_i['low']):.2f}, C={float(r_i['close']):.2f}, V={float(r_i.get('volume', 0))}\n"
            else:
                context_text += "    - N/A\n"

        response = await self.llm_client.analyze_chart(request, chart_base64, context_text)
        return response

    async def manage_position(self, req: PositionManagementRequest) -> PositionManagementResponse:
        current_dt = datetime.fromisoformat(req.bar_time.replace("Z", "+00:00"))
        if current_dt.tzinfo is None:
            current_dt = current_dt.replace(tzinfo=ZoneInfo("UTC"))

        symbol = req.symbol.strip().upper()

        daily_bars = await self._get_daily_bars_df_cached(symbol, current_dt)
        intraday_bars: pd.DataFrame

        if req.ohlcv_1m:
            intraday_bars = pd.DataFrame(req.ohlcv_1m)
        else:
            start = current_dt - timedelta(minutes=300)
            intraday_bars = await self._get_bars_df(symbol, "1Min", start, current_dt, 1000)

        if "timestamp" in intraday_bars.columns and not isinstance(intraday_bars.index, pd.DatetimeIndex):
            intraday_bars["timestamp"] = pd.to_datetime(intraday_bars["timestamp"])
            intraday_bars.set_index("timestamp", inplace=True)
        elif "t" in intraday_bars.columns and not isinstance(intraday_bars.index, pd.DatetimeIndex):
            intraday_bars["timestamp"] = pd.to_datetime(intraday_bars["t"])
            intraday_bars.set_index("timestamp", inplace=True)
        intraday_bars.sort_index(inplace=True)

        if "timestamp" in daily_bars.columns and not isinstance(daily_bars.index, pd.DatetimeIndex):
            daily_bars["timestamp"] = pd.to_datetime(daily_bars["timestamp"])
            daily_bars.set_index("timestamp", inplace=True)
        elif "t" in daily_bars.columns and not isinstance(daily_bars.index, pd.DatetimeIndex):
            daily_bars["timestamp"] = pd.to_datetime(daily_bars["t"])
            daily_bars.set_index("timestamp", inplace=True)
        daily_bars.sort_index(inplace=True)

        daily_records = daily_bars.reset_index().to_dict("records") if not daily_bars.empty else []
        daily_for_z = [{"c": r["close"], "t": r["timestamp"]} for r in daily_records if "close" in r and "timestamp" in r]

        z_indicator = ZScoreMomentum(daily_for_z)
        macd_indicator = MACD()

        intraday_records_df = intraday_bars.reset_index()
        if "timestamp" not in intraday_records_df.columns and "t" in intraday_records_df.columns:
            intraday_records_df["timestamp"] = pd.to_datetime(intraday_records_df["t"])
        intraday_records = intraday_records_df.to_dict("records")

        df = intraday_bars.copy()
        if not isinstance(df.index, pd.DatetimeIndex):
            if "timestamp" in df.columns:
                df["timestamp"] = pd.to_datetime(df["timestamp"])
                df.set_index("timestamp", inplace=True)
            elif "t" in df.columns:
                df["timestamp"] = pd.to_datetime(df["t"])
                df.set_index("timestamp", inplace=True)

        df["ema9"] = df["close"].ewm(span=9, adjust=False).mean()
        df["ema21"] = df["close"].ewm(span=21, adjust=False).mean()
        df["bb_middle"] = df["close"].rolling(window=20).mean()
        df["bb_std"] = df["close"].rolling(window=20).std()
        df["bb_upper"] = df["bb_middle"] + (df["bb_std"] * 2)
        df["bb_lower"] = df["bb_middle"] - (df["bb_std"] * 2)
        df["vwap"] = (df["volume"] * (df["high"] + df["low"] + df["close"]) / 3).cumsum() / df["volume"].cumsum()

        bars_with_indicators: list[dict[str, Any]] = []
        indicators_list: list[dict[str, Any]] = []

        for i, row in enumerate(intraday_records):
            close = row["close"]
            z_res = z_indicator.update(close)
            m_res = macd_indicator.update(close)

            ts = row.get("timestamp")
            if ts is None and row.get("t") is not None:
                ts = pd.to_datetime(row["t"])
            if not isinstance(ts, pd.Timestamp):
                ts = pd.to_datetime(ts)

            try:
                pd_row = df.loc[ts]
                if isinstance(pd_row, pd.DataFrame):
                    pd_row = pd_row.iloc[0]
            except Exception:
                pd_row = df.iloc[i]

            indicators_list.append(
                {
                    "ema9": float(pd_row["ema9"]),
                    "ema21": float(pd_row["ema21"]),
                    "vwap": float(pd_row["vwap"]),
                    "bb_upper": float(pd_row["bb_upper"]) if pd.notna(pd_row["bb_upper"]) else float("nan"),
                    "bb_middle": float(pd_row["bb_middle"]) if pd.notna(pd_row["bb_middle"]) else float("nan"),
                    "bb_lower": float(pd_row["bb_lower"]) if pd.notna(pd_row["bb_lower"]) else float("nan"),
                    "macd_dif": m_res.get("macd_dif"),
                    "macd_dea": m_res.get("macd_dea"),
                    "macd_hist": m_res.get("macd_hist"),
                    "z_score_diff": z_res.get("z_score_diff"),
                }
            )
            bars_with_indicators.append(
                {
                    "t": ts,
                    "o": row["open"],
                    "h": row["high"],
                    "l": row["low"],
                    "c": row["close"],
                    "v": row.get("volume", 0),
                }
            )

        plot_bars = bars_with_indicators[-60:]
        plot_indicators = indicators_list[-60:]
        chart_base64 = generate_chart_image(plot_bars, plot_indicators)

        prev_day_high = 0.0
        prev_day_low = 0.0
        prev_day_close = 0.0
        if daily_records:
            last_day = daily_records[-1]
            prev_day_close = float(last_day.get("close", 0.0) or 0.0)
            prev_day_high = float(last_day.get("high", 0.0) or 0.0)
            prev_day_low = float(last_day.get("low", 0.0) or 0.0)

        open_price = float(intraday_records[0]["open"]) if intraday_records else 0.0
        today_str = current_dt.strftime("%Y-%m-%d")
        df_today = df[df.index.strftime("%Y-%m-%d") == today_str]
        if not df_today.empty:
            day_high = float(df_today["high"].max())
            day_low = float(df_today["low"].min())
            open_price = float(df_today.iloc[0]["open"])
        else:
            day_high = 0.0
            day_low = 0.0

        latest_close = float(intraday_records[-1]["close"]) if intraday_records else 0.0
        daily_trend = ", ".join([f"{float(r['close']):.2f}" for r in daily_records if "close" in r])

        context_text = f"""
Timestamp (PST): {current_dt.astimezone(ZoneInfo("America/Los_Angeles")).strftime('%Y-%m-%d %H:%M:%S')}
Symbol: {symbol}

Daily Stats (Last 60 Days):
- Daily Trend (Last 60 Days): {daily_trend}

Previous Day Stats:
- Close: {prev_day_close:.2f}
- High: {prev_day_high:.2f}
- Low: {prev_day_low:.2f}

Intraday Stats:
- Open: {open_price:.2f}
- Day High: {day_high:.2f}
- Day Low: {day_low:.2f}
- Current Price: {latest_close:.2f}

Technical Indicators (Latest):
- EMA9: {indicators_list[-1]['ema9']:.2f}
- EMA21: {indicators_list[-1]['ema21']:.2f}
- VWAP: {indicators_list[-1]['vwap']:.2f}
- Bollinger Upper: {indicators_list[-1]['bb_upper']:.2f}
- Bollinger Middle: {indicators_list[-1]['bb_middle']:.2f}
- Bollinger Lower: {indicators_list[-1]['bb_lower']:.2f}
- MACD DIF: {indicators_list[-1]['macd_dif']:.3f}
- MACD DEA: {indicators_list[-1]['macd_dea']:.3f}
- MACD Hist: {indicators_list[-1]['macd_hist']:.3f}

Recent Price Action (Last 60 mins):
"""
        for b in bars_with_indicators[-60:]:
            t_str = b["t"].strftime("%H:%M")
            context_text += f"- {t_str}: O={b['o']:.2f}, H={b['h']:.2f}, L={b['l']:.2f}, C={b['c']:.2f}, V={b['v']}\n"

        position_option_quote: dict | None = None
        try:
            pos_opt = req.position.option
        except Exception:
            pos_opt = None  # type: ignore[assignment]

        try:
            try:
                strikes_around_atm_opt = int(os.getenv("OPTION_CHAIN_STRIKES_AROUND_ATM", "10"))
            except Exception:
                strikes_around_atm_opt = 10

            if getattr(req, "mode", "realtime") == "realtime":
                chain_opt = await self.option_chain_service.get_chain_realtime(
                    underlying=symbol,
                    strikes_around_atm=strikes_around_atm_opt,
                )
            else:
                chain_opt = await self.option_chain_service.get_chain_asof(
                    underlying=symbol,
                    asof=req.bar_time,
                    strikes_around_atm=strikes_around_atm_opt,
                    include_bars_minutes=0,
                )
            items_opt = chain_opt.get("items") if isinstance(chain_opt, dict) else None
            target = None
            opt_sym = (req.option_symbol or "").strip().upper() or None
            if isinstance(items_opt, list):
                if opt_sym:
                    for it in items_opt:
                        if isinstance(it, dict) and str(it.get("symbol") or "").upper() == opt_sym:
                            target = it
                            break
                if target is None and pos_opt is not None:
                    for it in items_opt:
                        if not isinstance(it, dict):
                            continue
                        try:
                            if (
                                str(it.get("expiration") or "") == getattr(pos_opt, "expiration", "")
                                and str(it.get("right") or "") == getattr(pos_opt, "right", "")
                                and float(it.get("strike")) == float(getattr(pos_opt, "strike", 0.0))
                            ):
                                target = it
                                break
                        except Exception:
                            continue

            if target is not None:
                q = target.get("quote") if isinstance(target.get("quote"), dict) else {}
                bid = q.get("bid")
                ask = q.get("ask")
                asof_px = target.get("asof_price")
                exp = target.get("expiration")
                strike = target.get("strike")
                right = target.get("right")
                sym = target.get("symbol") or opt_sym or ""
                if asof_px is None and bid is not None and ask is not None:
                    try:
                        asof_px = (float(bid) + float(ask)) / 2.0
                    except Exception:
                        asof_px = None
                position_option_quote = {
                    "symbol": sym,
                    "right": right,
                    "strike": strike,
                    "expiration": exp,
                    "asof": req.bar_time,
                    "asof_price": asof_px,
                    "bid": bid,
                    "ask": ask,
                }
                context_text += (
                    f"\nPosition Option Quote (as of {req.bar_time}):\n"
                    f"- {sym} {right} {strike} exp={exp}: last≈{asof_px}, bid={bid}, ask={ask}\n"
                )
            elif opt_sym:
                end_iso = current_dt.isoformat().replace("+00:00", "Z")
                start_iso = (current_dt - timedelta(minutes=2)).isoformat().replace("+00:00", "Z")
                quotes = await self.alpaca.get_option_quotes([opt_sym], start=start_iso, end=end_iso, limit=1000)
                rows = quotes.get(opt_sym, []) if isinstance(quotes, dict) else []
                last = rows[-1] if rows else None
                if isinstance(last, dict):
                    try:
                        bp = last.get("bp")
                        ap = last.get("ap")
                        mid = (float(bp) + float(ap)) / 2.0 if bp is not None and ap is not None else None
                    except Exception:
                        mid = None
                    position_option_quote = {
                        "symbol": opt_sym,
                        "asof": req.bar_time,
                        "asof_price": mid,
                        "bid": last.get("bp"),
                        "ask": last.get("ap"),
                        "t": last.get("t"),
                    }
                    context_text += (
                        f"\nPosition Option Quote (as of {req.bar_time}):\n"
                        f"- {opt_sym}: bid={last.get('bp')}, ask={last.get('ap')}, t={last.get('t')}\n"
                    )
        except Exception:
            pass

        context_text += "\nBenchmark Context (Proxy Futures):\n"
        benchmark_symbols = [s.strip().upper() for s in os.getenv("BENCHMARK_SYMBOLS", "QQQ,SPY").split(",") if s.strip()]
        benchmark_alias = {"QQQ": "NQ", "SPY": "ES", "DIA": "YM", "IWM": "RTY"}
        bench_daily_end = current_dt
        bench_daily_start = current_dt - timedelta(days=450)
        bench_intraday_start = current_dt - timedelta(minutes=300)

        for bsym in benchmark_symbols:
            df_b_daily = await self._get_bars_df(bsym, "1Day", bench_daily_start, bench_daily_end, 500)
            df_b_intra = await self._get_bars_df(bsym, "1Min", bench_intraday_start, current_dt, 1000)

            b_last = float(df_b_intra["close"].iloc[-1]) if not df_b_intra.empty else (float(df_b_daily["close"].iloc[-1]) if not df_b_daily.empty else 0.0)
            b_prev_high = float(df_b_daily["high"].iloc[-1]) if not df_b_daily.empty and "high" in df_b_daily.columns else 0.0
            b_prev_low = float(df_b_daily["low"].iloc[-1]) if not df_b_daily.empty and "low" in df_b_daily.columns else 0.0

            b_sma20 = self._sma_last(df_b_daily["close"], 20) if not df_b_daily.empty and "close" in df_b_daily.columns else None
            b_sma50 = self._sma_last(df_b_daily["close"], 50) if not df_b_daily.empty and "close" in df_b_daily.columns else None
            b_sma100 = self._sma_last(df_b_daily["close"], 100) if not df_b_daily.empty and "close" in df_b_daily.columns else None
            b_sma200 = self._sma_last(df_b_daily["close"], 200) if not df_b_daily.empty and "close" in df_b_daily.columns else None

            alias = benchmark_alias.get(bsym)
            alias_text = f"(≈ {alias})" if alias else ""
            context_text += f"""
- {bsym} {alias_text}
  - Current Price: {b_last:.2f}
  - Previous Day High: {b_prev_high:.2f}
  - Previous Day Low: {b_prev_low:.2f}
  - Daily SMA20: {b_sma20 if b_sma20 is not None else "N/A"}
  - Daily SMA50: {b_sma50 if b_sma50 is not None else "N/A"}
  - Daily SMA100: {b_sma100 if b_sma100 is not None else "N/A"}
  - Daily SMA200: {b_sma200 if b_sma200 is not None else "N/A"}
  - Recent 1m Price Action (Last 20 mins):
"""
            if not df_b_intra.empty:
                df_tail = df_b_intra.tail(20)
                for ts_i, r_i in df_tail.iterrows():
                    t_str = ts_i.strftime("%H:%M")
                    context_text += f"    - {t_str}: O={float(r_i['open']):.2f}, H={float(r_i['high']):.2f}, L={float(r_i['low']):.2f}, C={float(r_i['close']):.2f}, V={float(r_i.get('volume', 0))}\n"
            else:
                context_text += "    - N/A\n"

        resp = await self.llm_client.manage_position(req, chart_base64, context_text)
        if position_option_quote:
            try:
                resp = resp.model_copy(update={"position_option_quote": position_option_quote})
            except Exception:
                pass
        return resp
