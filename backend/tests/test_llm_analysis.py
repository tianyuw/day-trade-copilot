import asyncio
import os
import sys
import base64
from datetime import datetime
from zoneinfo import ZoneInfo
from dotenv import load_dotenv

# Add backend to path so we can import app modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from app.settings import get_settings
from app.analysis_service import AnalysisService
from app.schemas import LLMAnalysisRequest
from alpaca.data.historical import StockHistoricalDataClient

async def main():
    # Load env vars
    load_dotenv()
    
    settings = get_settings()
    if not settings.alpaca_api_key or not settings.alpaca_secret_key:
        print("Error: ALPACA_API_KEY or ALPACA_SECRET_KEY not found")
        return

    # Initialize Clients
    alpaca = StockHistoricalDataClient(settings.alpaca_api_key, settings.alpaca_secret_key)
    service = AnalysisService(alpaca)
    
    if hasattr(service.llm_client, 'model'):
        print(f"Using LLM Model (OpenRouter): {service.llm_client.model}")
    elif hasattr(service.llm_client, 'model_name'):
        print(f"Using LLM Model (Google): {service.llm_client.model_name}")

    # Target: NVDA @ 2026-01-15 08:38 PST
    # Convert to UTC ISO format
    pst_time = datetime(2026, 1, 15, 8, 38, 0, tzinfo=ZoneInfo("America/Los_Angeles"))
    utc_time = pst_time.astimezone(ZoneInfo("UTC"))
    utc_iso = utc_time.strftime('%Y-%m-%dT%H:%M:%SZ')
    
    print(f"Testing Analysis for NVDA at {pst_time} (UTC: {utc_iso})")
    
    request = LLMAnalysisRequest(
        symbol="NVDA",
        current_time=utc_iso
    )

    try:
        # We need to intercept the image generation to save it
        # Since analyze_signal calls generate_chart_image internally and sends it to LLM,
        # we can't easily get the image back unless we modify the service or mock it.
        # But wait, we can modify the service to return it, or we can just let it run 
        # and verify the LLM response.
        
        # To strictly follow the user request "Save the chart sent to LLM", 
        # let's monkey-patch the LLM client temporarily to capture the image
        
        original_analyze = service.llm_client.analyze_chart
        captured_image = None
        
        async def mock_analyze(req, img_b64, context):
            nonlocal captured_image
            captured_image = img_b64
            
            # Reconstruct the full prompt exactly as LLMClient does
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
- follow_up: Potential setup but need to wait for candle close or next candle for confirmation.
- check_when_condition_meet: Setup looks good but price needs to cross a specific level (e.g. key resistance) first. In this case, you MUST provide "watch_condition".
"""

            user_content_text = f"""Analyze the following market context for {req.symbol} at {req.current_time}.

Market Context:
{context}

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
            
            print("\n=== FULL Prompt Sent to LLM ===")
            print("--- System Prompt ---")
            print(system_prompt)
            print("\n--- User Prompt ---")
            print(user_content_text)
            print("====================================\n")
            
            # Call original
            return await original_analyze(req, img_b64, context)
            
        service.llm_client.analyze_chart = mock_analyze
        
        print("Calling Analysis Service...")
        response = await service.analyze_signal(request)
        
        print("\n=== LLM Response ===")
        print(response.model_dump_json(indent=2))
        
        if captured_image:
            # Decode and save image
            img_data = base64.b64decode(captured_image)
            output_path = "debug_chart_nvda.png"
            with open(output_path, "wb") as f:
                f.write(img_data)
            print(f"\n[SUCCESS] Chart image saved to: {os.path.abspath(output_path)}")
        else:
            print("\n[ERROR] Failed to capture chart image")

    except Exception as e:
        print(f"\n[ERROR] Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
