from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field, model_validator


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


class TradePlanOption(BaseModel):
    right: Literal["call", "put"]
    expiration: str
    strike: float


class TradePlanRisk(BaseModel):
    stop_loss_premium: float
    time_stop_minutes: int


class TradePlan(BaseModel):
    trade_id: str
    direction: Literal["long", "short"]
    option: TradePlanOption
    contracts: int
    risk: TradePlanRisk
    take_profit_premium: float

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
    trade_plan: TradePlan | None = None

    @model_validator(mode="after")
    def _validate_trade_plan(self) -> "LLMAnalysisResponse":
        if self.action in ("buy_long", "buy_short"):
            if self.trade_plan is None:
                raise ValueError("trade_plan is required when action is buy_long or buy_short")
            if self.action == "buy_long" and self.trade_plan.direction != "long":
                raise ValueError("trade_plan.direction must be long when action is buy_long")
            if self.action == "buy_short" and self.trade_plan.direction != "short":
                raise ValueError("trade_plan.direction must be short when action is buy_short")
        else:
            if self.trade_plan is not None:
                raise ValueError("trade_plan must be null unless action is buy_long or buy_short")
        return self



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


class TradingSettings(BaseModel):
    paper_auto_trade_enabled: bool = False
    live_trading_enabled: bool = False
    default_execution: Literal["paper", "live"] = "paper"


class PositionOption(BaseModel):
    right: Literal["call", "put"]
    expiration: str
    strike: float


class PositionEntry(BaseModel):
    time: str | None = None
    premium: float | None = None


class PositionRisk(BaseModel):
    stop_loss_premium: float | None = None
    take_profit_premium: float | None = None
    time_stop_minutes: int | None = None


class PositionState(BaseModel):
    direction: Literal["long", "short"]
    option: PositionOption
    contracts_total: int
    contracts_remaining: int
    entry: PositionEntry | None = None
    risk: PositionRisk | None = None


class PositionDecisionExit(BaseModel):
    contracts_to_close: int | None = None


class PositionDecisionAdjustments(BaseModel):
    new_stop_loss_premium: float | None = None
    new_take_profit_premium: float | None = None
    new_time_stop_minutes: int | None = None


class PositionDecision(BaseModel):
    action: Literal[
        "hold",
        "close_all",
        "close_partial",
        "tighten_stop",
        "adjust_take_profit",
        "update_time_stop",
    ]
    reasoning: str
    exit: PositionDecisionExit | None = None
    adjustments: PositionDecisionAdjustments | None = None


class PositionManagementRequest(BaseModel):
    trade_id: str
    symbol: str
    bar_time: str
    position: PositionState
    ohlcv_1m: list[dict[str, Any]] | None = None
    option_symbol: str | None = None


class PositionManagementResponse(BaseModel):
    trade_id: str
    analysis_id: str
    timestamp: str
    symbol: str
    bar_time: str
    decision: PositionDecision
