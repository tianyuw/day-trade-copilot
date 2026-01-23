import os
import json
from .schemas import (
    LLMAnalysisResponse,
    LLMAnalysisRequest,
    PositionManagementRequest,
    PositionManagementResponse,
)
from .google_api_client import GoogleAPIClient
from .llm_prompts import get_llm_system_prompt
from .debug_logging import LLMExchangeMeta, Stopwatch, write_llm_exchange

class LLMClient:
    def __init__(self):
        google_api_key = (os.getenv("GOOGLE_API_KEY") or "").strip()
        if not google_api_key:
            raise RuntimeError("Missing GOOGLE_API_KEY for Google Native LLM API")

        self.client = GoogleAPIClient()
        self.model_name = os.getenv("GOOGLE_MODEL", "gemini-3-flash-preview")

    async def analyze_chart(
        self, 
        request: LLMAnalysisRequest, 
        chart_image_base64: str,
        context_text: str
    ) -> LLMAnalysisResponse:
        
        system_prompt = get_llm_system_prompt()

        user_content_text = f"""Analyze the following market context for {request.symbol} at {request.current_time}.

Market Context:
{context_text}

Chart Description:
The attached chart contains three panels:
1. Top Panel (Price Action): 
   - Candles: Cyan=Up, Red=Down
   - Overlays: Green Line=EMA9, Red Line=EMA21, White Line=VWAP
   - Bollinger Bands: Purple=Upper, Blue=Middle, Yellow=Lower
2. Middle Panel (Volume): Bars
3. Bottom Panel (MACD):
   - White Line = DIF
   - Yellow Line = DEA
   - Green/Red Bars = Histogram

Based on the chart and context, provide your trading decision JSON.
"""

        content: str | None = None
        data: dict | None = None
        sw: Stopwatch | None = None
        try:
            sw = Stopwatch()
            content = await self.client.analyze_chart(
                system_prompt=system_prompt,
                user_content_text=user_content_text,
                chart_image_base64=chart_image_base64
            )
            
            # Parse JSON and validate with Pydantic
            parsed = json.loads(content)
            data = parsed
            if isinstance(data, list):
                if len(data) == 1 and isinstance(data[0], dict):
                    data = data[0]
                else:
                    raise ValueError("Model returned a JSON array; expected a single JSON object")
            
            # Ensure required fields that might be missing from LLM are present or set defaults
            import uuid
            analysis_id = str(uuid.uuid4())
            data["analysis_id"] = analysis_id
            
            if "timestamp" not in data:
                data["timestamp"] = request.current_time
            if "symbol" not in data:
                data["symbol"] = request.symbol
            
            write_llm_exchange(
                meta=LLMExchangeMeta(
                    kind="analysis",
                    model=getattr(self.client, "model_name", None),
                    symbol=request.symbol,
                    analysis_id=analysis_id,
                    current_time=request.current_time,
                ),
                system_prompt=system_prompt,
                user_prompt=user_content_text,
                response_raw=content,
                parsed_json=data if isinstance(data, dict) else None,
                error=None,
                duration_ms=sw.elapsed_ms() if sw else None,
            )

            return LLMAnalysisResponse(**data)
            
        except Exception as e:
            print(f"LLM Error: {e}")
            # Fallback response
            import uuid
            analysis_id = str(uuid.uuid4())
            write_llm_exchange(
                meta=LLMExchangeMeta(
                    kind="analysis",
                    model=getattr(self.client, "model_name", None),
                    symbol=request.symbol,
                    analysis_id=analysis_id,
                    current_time=request.current_time,
                ),
                system_prompt=system_prompt,
                user_prompt=user_content_text,
                response_raw=content,
                parsed_json=data if isinstance(data, dict) else None,
                error=str(e),
                duration_ms=sw.elapsed_ms() if sw else None,
            )
            return LLMAnalysisResponse(
                analysis_id=analysis_id,
                timestamp=request.current_time,
                symbol=request.symbol,
                action="ignore",
                confidence=0.0,
                reasoning=f"Error calling LLM: {str(e)}"
            )

    async def manage_position(
        self,
        request: PositionManagementRequest,
        chart_image_base64: str,
        context_text: str,
    ) -> PositionManagementResponse:
        system_prompt = (
            "You are an expert 0DTE options position manager. "
            "You are already in a position. "
            "Return ONLY valid JSON that matches the schema below. "
            "Replay mode does NOT compute PnL; do NOT require pnl fields.\n\n"
            'Schema:\n'
            '{\n'
            '  "trade_id": "string",\n'
            '  "timestamp": "ISO8601",\n'
            '  "symbol": "TICKER",\n'
            '  "bar_time": "ISO8601",\n'
            '  "decision": {\n'
            '    "action": "hold"|"close_all"|"close_partial"|"tighten_stop"|"adjust_take_profit"|"update_time_stop",\n'
            '    "reasoning": "string",\n'
            '    "exit": { "contracts_to_close": int } | null,\n'
            '    "adjustments": { "new_stop_loss_premium": number|null, "new_take_profit_premium": number|null, "new_time_stop_minutes": int|null } | null\n'
            "  }\n"
            "}\n\n"
            "Rules:\n"
            "- close_partial must specify contracts_to_close (1..contracts_remaining).\n"
            "- close_all should close all remaining contracts.\n"
            "- tighten_stop/adjust_take_profit/update_time_stop must specify the corresponding new_* field.\n"
        )

        marker = "\nPosition Option Quote (as of"
        bench_marker = "\nBenchmark Context (Proxy Futures):\n"
        opt_block = ""
        start_idx = context_text.find(marker)
        if start_idx != -1:
            end_idx = context_text.find(bench_marker, start_idx)
            if end_idx == -1:
                end_idx = len(context_text)
            opt_block = context_text[start_idx:end_idx]
            context_text = context_text[:start_idx] + context_text[end_idx:]

        user_content_text = f"""Manage the current position for {request.symbol} at {request.bar_time}.

Market Context:
{context_text}

Chart Description:
The attached chart contains three panels:
1. Top Panel (Price Action): 
   - Candles: Cyan=Up, Red=Down
   - Overlays: Green Line=EMA9, Red Line=EMA21, White Line=VWAP
   - Bollinger Bands: Purple=Upper, Blue=Middle, Yellow=Lower
2. Middle Panel (Volume): Bars
3. Bottom Panel (MACD):
   - White Line = DIF
   - Yellow Line = DEA
   - Green/Red Bars = Histogram

Position Context (JSON):
{json.dumps(request.position.model_dump(), ensure_ascii=False)}

"""

        if opt_block:
            opt_block_renamed = opt_block.replace("Position Option Quote", "Position Latest Option Quote", 1)
            user_content_text += f"""
{opt_block_renamed}
"""
        user_content_text += """
Based on the chart and context, provide your position management decision JSON.
"""

        content: str | None = None
        data: dict | None = None
        sw: Stopwatch | None = None
        try:
            sw = Stopwatch()
            content = await self.client.analyze_chart(
                system_prompt=system_prompt,
                user_content_text=user_content_text,
                chart_image_base64=chart_image_base64,
            )

            parsed = json.loads(content)
            data = parsed
            if isinstance(data, list):
                if len(data) == 1 and isinstance(data[0], dict):
                    data = data[0]
                else:
                    raise ValueError("Model returned a JSON array; expected a single JSON object")

            import uuid

            analysis_id = str(uuid.uuid4())
            data["analysis_id"] = analysis_id
            if "timestamp" not in data:
                data["timestamp"] = request.bar_time
            if "symbol" not in data:
                data["symbol"] = request.symbol
            if "trade_id" not in data:
                data["trade_id"] = request.trade_id
            if "bar_time" not in data:
                data["bar_time"] = request.bar_time

            write_llm_exchange(
                meta=LLMExchangeMeta(
                    kind="position_management",
                    model=getattr(self.client, "model_name", None),
                    symbol=request.symbol,
                    analysis_id=analysis_id,
                    trade_id=request.trade_id,
                    bar_time=request.bar_time,
                ),
                system_prompt=system_prompt,
                user_prompt=user_content_text,
                response_raw=content,
                parsed_json=data if isinstance(data, dict) else None,
                error=None,
                duration_ms=sw.elapsed_ms() if sw else None,
            )
            return PositionManagementResponse(**data)
        except Exception as e:
            import uuid

            analysis_id = str(uuid.uuid4())
            write_llm_exchange(
                meta=LLMExchangeMeta(
                    kind="position_management",
                    model=getattr(self.client, "model_name", None),
                    symbol=request.symbol,
                    analysis_id=analysis_id,
                    trade_id=request.trade_id,
                    bar_time=request.bar_time,
                ),
                system_prompt=system_prompt,
                user_prompt=user_content_text,
                response_raw=content,
                parsed_json=data if isinstance(data, dict) else None,
                error=str(e),
                duration_ms=sw.elapsed_ms() if sw else None,
            )
            return PositionManagementResponse(
                trade_id=request.trade_id,
                analysis_id=analysis_id,
                timestamp=request.bar_time,
                symbol=request.symbol,
                bar_time=request.bar_time,
                decision={
                    "action": "hold",
                    "reasoning": f"Error calling LLM: {str(e)}",
                    "exit": None,
                    "adjustments": None,
                },
            )
