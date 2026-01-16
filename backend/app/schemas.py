from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field


class AlpacaBar(BaseModel):
    t: str
    o: float
    h: float
    l: float
    c: float
    v: float | int
    n: int | None = None
    vw: float | None = None
    indicators: dict[str, Any] | None = None


class StreamBarMessage(BaseModel):
    type: Literal["bar"]
    mode: Literal["realtime", "playback"]
    symbol: str
    bar: AlpacaBar
    i: int | None = None


class StreamInitMessage(BaseModel):
    type: Literal["init"]
    mode: Literal["realtime", "playback"]
    symbol: str
    bars: list[AlpacaBar]
    cursor: int | None = None


class StreamDoneMessage(BaseModel):
    type: Literal["done"]
    mode: Literal["realtime", "playback"]
    cursor: int | None = None

class StreamAnalysisMessage(BaseModel):
    type: Literal["analysis"]
    mode: Literal["realtime", "playback"]
    symbol: str
    result: LLMAnalysisResponse



# --- LLM Analysis Schemas ---

class LLMAnalysisRequest(BaseModel):
    symbol: str
    current_time: str  # ISO8601 string, the time of the bar that triggered the analysis

class WatchCondition(BaseModel):
    trigger_price: float
    direction: Literal["above", "below"]
    expiry_minutes: int

class LLMAnalysisResponse(BaseModel):
    analysis_id: str
    timestamp: str
    symbol: str
    action: Literal["buy_long", "buy_short", "ignore", "follow_up", "check_when_condition_meet"]
    confidence: float = Field(ge=0.0, le=1.0)
    reasoning: str
    pattern_name: str | None = None  # e.g., "Bull Flag Breakout", "Double Bottom", "VWAP Reclaim"
    breakout_price: float | None = None # The specific price level that was broken or needs to be broken
    watch_condition: WatchCondition | None = None



class AIActionPlan(BaseModel):
    option_type: Literal["call", "put"]
    strike_price: float
    option_stop_loss: float
    option_take_profit: float
    underlying_trigger_price: float


class AIVerificationResult(BaseModel):
    is_valid_buy_point: bool
    confidence: float = Field(ge=0.0, le=1.0)
    reasoning: str
    action_plan: AIActionPlan | None = None


class AIVerificationRequest(BaseModel):
    symbol: str
    ohlcv_1m: list[dict[str, Any]]
    indicators: dict[str, Any] | None = None
    option_chain: dict[str, Any] | None = None
    rolling_summary: str | None = None
