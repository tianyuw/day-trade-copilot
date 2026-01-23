from __future__ import annotations

from enum import Enum
from typing import Any, Literal

from pydantic import BaseModel, Field


class ExecutionMode(str, Enum):
    paper = "paper"
    live = "live"


class TradingSettingsV2(BaseModel):
    paper_auto_trade_enabled: bool = False
    live_trading_enabled: bool = False
    default_execution: ExecutionMode = ExecutionMode.paper


class OrderCreateRequest(BaseModel):
    execution: ExecutionMode = ExecutionMode.paper
    symbol: str
    side: Literal["buy", "sell"]
    type: Literal["market", "limit", "stop", "stop_limit", "trailing_stop"] = "market"
    time_in_force: str = "day"
    qty: str | None = None
    notional: str | None = None
    limit_price: str | None = None
    stop_price: str | None = None
    trail_price: str | None = None
    trail_percent: str | None = None
    extended_hours: bool | None = None
    client_order_id: str | None = Field(default=None, max_length=128)
    order_class: str | None = None
    take_profit: dict[str, Any] | None = None
    stop_loss: dict[str, Any] | None = None
    legs: list[dict[str, Any]] | None = None
    position_intent: str | None = None


class OrderReplaceRequest(BaseModel):
    execution: ExecutionMode = ExecutionMode.paper
    qty: str | None = None
    time_in_force: str | None = None
    limit_price: str | None = None
    stop_price: str | None = None
    trail: str | None = None
    client_order_id: str | None = Field(default=None, max_length=128)


class CancelOrderRequest(BaseModel):
    execution: ExecutionMode = ExecutionMode.paper


class ClosePositionRequest(BaseModel):
    execution: ExecutionMode = ExecutionMode.paper
    qty: str | None = None
    percentage: str | None = None


class ListOrdersRequest(BaseModel):
    execution: ExecutionMode = ExecutionMode.paper
    status: str | None = None
    limit: int | None = None
    after: str | None = None
    until: str | None = None
    direction: str | None = None
    nested: bool | None = None
    symbols: str | None = None


class ListActivitiesRequest(BaseModel):
    execution: ExecutionMode = ExecutionMode.paper
    activity_type: str | None = None
    after: str | None = None
    until: str | None = None
    page_size: int | None = None


class EquityOCORequest(BaseModel):
    execution: ExecutionMode = ExecutionMode.paper
    symbol: str
    qty: str
    take_profit_limit_price: str
    stop_loss_stop_price: str
    stop_loss_limit_price: str | None = None
    time_in_force: str = "gtc"


class OptionSyntheticOCOCreateRequest(BaseModel):
    execution: ExecutionMode = ExecutionMode.paper
    trade_id: str
    option_symbol: str
    qty: str
    take_profit_limit_price: str
    stop_loss_premium: str
    time_stop_minutes: int | None = None


class OptionSyntheticOCOUpdateRequest(BaseModel):
    execution: ExecutionMode = ExecutionMode.paper
    take_profit_limit_price: str | None = None
    stop_loss_premium: str | None = None
    time_stop_minutes: int | None = None
