import asyncio
import os
import sys
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from dotenv import load_dotenv

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from app.settings import get_settings
from app.analysis_service import AnalysisService
from app.schemas import PositionManagementRequest, PositionState, PositionOption, PositionEntry, PositionRisk
from alpaca.data.historical import StockHistoricalDataClient


def to_utc_iso(pst_dt: datetime) -> str:
    utc_dt = pst_dt.astimezone(ZoneInfo("UTC"))
    return utc_dt.strftime("%Y-%m-%dT%H:%M:%SZ")


async def main():
    load_dotenv()

    settings = get_settings()
    if not settings.alpaca_api_key or not settings.alpaca_secret_key:
        print("Error: Alpaca credentials not found in backend/.env (ALPACA_*_API_KEY/SECRET_KEY)")
        return

    alpaca = StockHistoricalDataClient(settings.alpaca_api_key, settings.alpaca_secret_key)
    service = AnalysisService(alpaca)

    print(f"Using LLM Model (Google): {getattr(service.llm_client, 'model_name', 'unknown')}", flush=True)

    pst_time = datetime(2026, 1, 22, 11, 15, 0, tzinfo=ZoneInfo("America/Los_Angeles"))
    bar_time = to_utc_iso(pst_time)

    entry_time = to_utc_iso(pst_time - timedelta(minutes=10))

    req = PositionManagementRequest(
        trade_id="demo_trade_001",
        symbol="NVDA",
        bar_time=bar_time,
        position=PositionState(
            direction="long",
            option=PositionOption(
                right="call",
                expiration="2026-01-23",
                strike=190.0,
            ),
            contracts_total=5,
            contracts_remaining=3,
            entry=PositionEntry(time=entry_time, premium=2.10),
            risk=PositionRisk(
                stop_loss_premium=1.40,
                take_profit_premium=3.20,
                time_stop_minutes=20,
            ),
        ),
        option_symbol=None,
        ohlcv_1m=None,
    )

    original_analyze = service.llm_client.client.analyze_chart

    async def intercept_analyze(*, system_prompt: str, user_content_text: str, chart_image_base64: str):
        print("\n=== FULL Prompt Sent to LLM ===", flush=True)
        print("--- System Prompt ---", flush=True)
        print(system_prompt, flush=True)
        print("\n--- User Prompt ---", flush=True)
        print(user_content_text, flush=True)
        print("====================================\n", flush=True)

        prompt_path = os.path.abspath("debug_position_management_prompt.txt")
        with open(prompt_path, "w", encoding="utf-8") as f:
            f.write(f"--- System Prompt ---\n{system_prompt}\n\n--- User Prompt ---\n{user_content_text}\n")
        print(f"[SUCCESS] Full prompt saved to: {prompt_path}\n", flush=True)

        content = await original_analyze(
            system_prompt=system_prompt,
            user_content_text=user_content_text,
            chart_image_base64=chart_image_base64,
        )
        print("\n=== RAW LLM Response ===", flush=True)
        print(content, flush=True)
        return content

    service.llm_client.client.analyze_chart = intercept_analyze

    print(f"Testing Position Management for {req.symbol} @ {pst_time.isoformat()} (UTC: {req.bar_time})", flush=True)
    try:
        resp = await service.manage_position(req)
        print("\n=== Parsed PositionManagementResponse ===", flush=True)
        print(resp.model_dump_json(indent=2), flush=True)
    except Exception as e:
        print(f"\n[ERROR] Test failed: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())

