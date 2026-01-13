from __future__ import annotations

import json

import httpx

from .schemas import AIVerificationRequest, AIVerificationResult
from .settings import Settings


class OpenRouterClient:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings

    async def verify(self, req: AIVerificationRequest) -> AIVerificationResult:
        system = (
            "You are a trading assistant for 0DTE options. "
            "Return ONLY valid JSON that matches the schema: "
            '{ "is_valid_buy_point": bool, "confidence": number 0..1, "reasoning": string, '
            '"action_plan": { "option_type": "call"|"put", "strike_price": number, "option_stop_loss": number, '
            '"option_take_profit": number, "underlying_trigger_price": number } | null }'
        )
        user = {
            "symbol": req.symbol,
            "ohlcv_1m": req.ohlcv_1m,
            "indicators": req.indicators,
            "option_chain": req.option_chain,
            "rolling_summary": req.rolling_summary,
        }

        payload = {
            "model": self._settings.openrouter_model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": json.dumps(user)},
            ],
            "temperature": 0.2,
        }

        headers = {
            "Authorization": f"Bearer {self._settings.openrouter_api_key}",
            "Content-Type": "application/json",
        }

        async with httpx.AsyncClient(timeout=60.0) as client:
            r = await client.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
            r.raise_for_status()
            data = r.json()

        content = (data.get("choices") or [{}])[0].get("message", {}).get("content", "")
        if not content:
            raise RuntimeError("Empty model response from OpenRouter")

        cleaned = content.strip()
        if cleaned.startswith("```"):
            cleaned = cleaned.strip("`").strip()
            if "\n" in cleaned:
                cleaned = cleaned.split("\n", 1)[1].strip()
        if cleaned.endswith("```"):
            cleaned = cleaned[: -3].strip()

        parsed = json.loads(cleaned)
        return AIVerificationResult.model_validate(parsed)
