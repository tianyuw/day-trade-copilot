import os
import json
from openai import AsyncOpenAI
from .schemas import LLMAnalysisResponse, LLMAnalysisRequest

class OpenRouterAPIClient:
    def __init__(self):
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        if not self.api_key:
            print("Warning: OPENROUTER_API_KEY not found in environment variables")
        
        print("Using OpenRouter API")
        self.client = AsyncOpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=self.api_key,
        )
        self.model = os.getenv("OPENROUTER_MODEL", "google/gemini-2.0-flash-001")

    async def analyze_chart(
        self, 
        system_prompt: str,
        user_content_text: str,
        chart_image_base64: str
    ) -> str:
        
        user_content = [
            {
                "type": "text",
                "text": user_content_text
            },
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/png;base64,{chart_image_base64}"
                }
            }
        ]

        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_content}
                ],
                response_format={"type": "json_object"},
                temperature=0.2,
                max_tokens=1000
            )
            
            content = response.choices[0].message.content
            print(f"DEBUG: Raw OpenRouter API Response Content: '{content}'")
            
            if not content:
                raise ValueError("OpenRouter API returned empty response content")
                
            return content
            
        except Exception as e:
            print(f"OpenRouter API Error: {e}")
            raise e
