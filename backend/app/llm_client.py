import os
import json
from .schemas import LLMAnalysisResponse, LLMAnalysisRequest
from .google_api_client import GoogleAPIClient
from .openrouter_api_client import OpenRouterAPIClient
from .llm_prompts import get_llm_system_prompt

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
            self.model_name = os.getenv("GOOGLE_MODEL", "gemini-3-flash-preview")
        else:
            # 2. Fallback to OpenRouter
            print("Using OpenRouter API")
            self.client = OpenRouterAPIClient()
            self.model = os.getenv("OPENROUTER_MODEL", "google/gemini-3-flash-preview")

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

        try:
            content = await self.client.analyze_chart(
                system_prompt=system_prompt,
                user_content_text=user_content_text,
                chart_image_base64=chart_image_base64
            )
            
            # Parse JSON and validate with Pydantic
            data = json.loads(content)
            if isinstance(data, list):
                if len(data) == 1 and isinstance(data[0], dict):
                    data = data[0]
                else:
                    raise ValueError("Model returned a JSON array; expected a single JSON object")
            
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
