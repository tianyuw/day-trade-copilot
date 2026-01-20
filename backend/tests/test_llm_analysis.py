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
from app.llm_prompts import get_llm_system_prompt
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
    pst_time = datetime(2026, 1, 16, 7, 3, 0, tzinfo=ZoneInfo("America/Los_Angeles"))
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
            system_prompt = get_llm_system_prompt()

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
            print(system_prompt, flush=True)
            print("\n--- User Prompt ---")
            print(user_content_text, flush=True)
            print("====================================\n")

            full_prompt = f"--- System Prompt ---\n{system_prompt}\n\n--- User Prompt ---\n{user_content_text}\n"
            prompt_path = os.path.abspath("debug_full_prompt.txt")
            with open(prompt_path, "w", encoding="utf-8") as f:
                f.write(full_prompt)
            print(f"[SUCCESS] Full prompt saved to: {prompt_path}\n", flush=True)
            
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
