import os
import json
from .schemas import LLMAnalysisResponse, LLMAnalysisRequest
from .google_api_client import GoogleAPIClient
from .openrouter_api_client import OpenRouterAPIClient

class LLMClient:
    def __init__(self):
        # 1. Try Google Native First
        self.google_api_key = os.getenv("GOOGLE_API_KEY")
        self.use_google_native = False
        
        if self.google_api_key:
            print("Using Google Native API")
            self.client = GoogleAPIClient()
            self.use_google_native = True
            # Default model for Google Native
            self.model_name = os.getenv("GOOGLE_MODEL", "gemini-2.0-flash")
        else:
            # 2. Fallback to OpenRouter
            print("Using OpenRouter API")
            self.client = OpenRouterAPIClient()
            self.model = os.getenv("OPENROUTER_MODEL", "google/gemini-2.0-flash-001")

    async def analyze_chart(
        self, 
        request: LLMAnalysisRequest, 
        chart_image_base64: str,
        context_text: str
    ) -> LLMAnalysisResponse:
        
        system_prompt = """You are an expert day trader specializing in 0DTE options and scalping strategies.
Your goal is to analyze the provided chart and market context to make a high-confidence trading decision.

Decision Constraints (IMPORTANT):
- You MUST be conservative. Only output buy_long or buy_short when you are highly confident AND the setup quality is excellent.
- Only output buy_long/buy_short when you clearly see either:
  1) a valid breakout/breakdown aligned with the higher-timeframe trend (not a minor micro-break), OR
  2) a deep V reversal with strong confirmation (capitulation + decisive reclaim of key levels).
- You MUST require a strong risk/reward profile for buy_long/buy_short (high payoff relative to risk). If the market is in a tight range / narrow consolidation / choppy conditions, you MUST NOT output buy_long or buy_short.
- If the breakout/breakdown is not clearly confirmed yet, prefer follow_up (wait for next candle / close) or check_when_condition_meet (set a trigger price), rather than buy_long/buy_short.
- When you do output buy_long or buy_short, your reasoning MUST explicitly mention why this is a high-quality setup (trend alignment, confirmation, and risk/reward), and you MUST provide pattern_name and breakout_price.

Output MUST be a valid JSON object matching the following schema:
{
  "timestamp": "ISO8601",
  "symbol": "TICKER",
  "action": "buy_long" | "buy_short" | "ignore" | "follow_up" | "check_when_condition_meet",
  "confidence": float (0.0-1.0),
  "reasoning": "concise explanation",
  "pattern_name": "string" (optional, required if action is buy_long/buy_short),
  "breakout_price": float (optional, required if action is buy_long/buy_short),
  "watch_condition": { "trigger_price": float, "direction": "above"|"below", "expiry_minutes": int } (optional, ONLY used when action is "check_when_condition_meet", otherwise null)
}

Action Definitions:
- buy_long: Breakout confirmed, good momentum, clear entry. MUST specify "pattern_name" (e.g. "Bull Flag Breakout") and "breakout_price".
- buy_short: Breakdown confirmed, good momentum, clear entry. MUST specify "pattern_name" (e.g. "Head and Shoulders Breakdown") and "breakout_price".
- ignore: False breakout, low volume, hitting resistance/support, or chopping.
- follow_up: Potential setup but need to wait for the next candle for confirmation.
- check_when_condition_meet: Setup looks good but price needs to cross a specific level (e.g. key resistance/support) first. In this case, you MUST provide "watch_condition".
"""

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

        try:
            content = await self.client.analyze_chart(
                system_prompt=system_prompt,
                user_content_text=user_content_text,
                chart_image_base64=chart_image_base64
            )
            
            # Parse JSON and validate with Pydantic
            data = json.loads(content)
            
            # Ensure required fields that might be missing from LLM are present or set defaults
            import uuid
            data["analysis_id"] = str(uuid.uuid4())
            
            if "timestamp" not in data:
                data["timestamp"] = request.current_time
            if "symbol" not in data:
                data["symbol"] = request.symbol
                
            return LLMAnalysisResponse(**data)
            
        except Exception as e:
            print(f"LLM Error: {e}")
            # Fallback response
            import uuid
            return LLMAnalysisResponse(
                analysis_id=str(uuid.uuid4()),
                timestamp=request.current_time,
                symbol=request.symbol,
                action="ignore",
                confidence=0.0,
                reasoning=f"Error calling LLM: {str(e)}"
            )
