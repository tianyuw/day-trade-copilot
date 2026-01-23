import os
import json
import google.generativeai as genai
from .schemas import LLMAnalysisResponse, LLMAnalysisRequest

class GoogleAPIClient:
    def __init__(self):
        self.api_key = os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            print("Warning: GOOGLE_API_KEY not found in environment variables")
        
        genai.configure(api_key=self.api_key)
        self.model_name = os.getenv("GOOGLE_MODEL", "gemini-2.0-flash")
        print(f"Initialized GoogleAPIClient with model: {self.model_name}")

    async def analyze_chart(
        self, 
        system_prompt: str,
        user_content_text: str,
        chart_image_base64: str
    ) -> str:
        
        try:
            model = genai.GenerativeModel(
                model_name=self.model_name,
                system_instruction=system_prompt,
                generation_config={"response_mime_type": "application/json"}
            )
            
            # Construct payload
            # Gemini expects a list of parts. 
            # Image part is {'mime_type': 'image/png', 'data': ...}
            prompt_parts = [
                user_content_text,
                {"mime_type": "image/png", "data": chart_image_base64}
            ]
            
            response = await model.generate_content_async(prompt_parts)
            content = response.text
            
            #print(f"DEBUG: Raw Google API Response Content: '{content}'")
            
            if not content:
                raise ValueError("Google API returned empty response content")
                
            return content
            
        except Exception as e:
            print(f"Google API Error: {e}")
            raise e
