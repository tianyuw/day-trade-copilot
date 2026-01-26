from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class TradeState(str, Enum):
    SCAN = "SCAN"
    AI_VERIFY = "AI_VERIFY"
    FOLLOW_UP_PENDING = "FOLLOW_UP_PENDING"
    WATCH_PENDING = "WATCH_PENDING"
    ENTRY_PENDING = "ENTRY_PENDING"
    IN_POSITION = "IN_POSITION"
    EXIT_PENDING = "EXIT_PENDING"
    CLOSED = "CLOSED"


@dataclass
class PendingWatch:
    trigger_price: float
    direction: str
    created_at_epoch_s: int
    expires_at_epoch_s: int


@dataclass
class ActiveTrade:
    trade_id: str
    direction: str
    option: dict[str, Any]
    option_symbol: str | None
    contracts_total: int
    contracts_remaining: int
    entry_time: str
    entry_premium: float | None
    risk: dict[str, Any]


@dataclass
class FollowUpState:
    armed: bool = False


@dataclass
class SymbolSession:
    symbol: str
    mode: str
    state: TradeState = TradeState.SCAN
    follow_up: FollowUpState = field(default_factory=FollowUpState)
    watches: list[PendingWatch] = field(default_factory=list)
    trade: ActiveTrade | None = None
    last_bar_time: str | None = None
    analysis_inflight: bool = False
    manage_inflight: bool = False

    def reset_to_scan(self) -> None:
        self.state = TradeState.SCAN
        self.follow_up = FollowUpState(armed=False)
        self.watches = []
        self.trade = None
        self.analysis_inflight = False
        self.manage_inflight = False

    def on_analysis_result(self, res: dict[str, Any]) -> None:
        action = str(res.get("action") or "")
        if action == "follow_up":
            self.state = TradeState.FOLLOW_UP_PENDING
            self.follow_up = FollowUpState(armed=True)
            self.watches = []
            return

        if action == "check_when_condition_meet" and isinstance(res.get("watch_condition"), dict):
            cond = res.get("watch_condition") or {}
            try:
                trigger = float(cond.get("trigger_price"))
                direction = str(cond.get("direction") or "")
                expiry_min = int(cond.get("expiry_minutes"))
            except Exception:
                self.reset_to_scan()
                return

            now_epoch = _to_epoch_seconds(str(res.get("timestamp") or ""))
            expires = now_epoch + max(0, expiry_min) * 60
            self.watches.append(
                PendingWatch(
                    trigger_price=trigger,
                    direction=direction,
                    created_at_epoch_s=now_epoch,
                    expires_at_epoch_s=expires,
                )
            )
            self.state = TradeState.WATCH_PENDING
            self.follow_up = FollowUpState(armed=False)
            return

        if action in {"buy_long", "buy_short"} and isinstance(res.get("trade_plan"), dict):
            self.state = TradeState.ENTRY_PENDING
            return

        self.reset_to_scan()

    def enter_from_trade_plan(self, res: dict[str, Any], *, option_symbol: str | None) -> None:
        plan = res.get("trade_plan") if isinstance(res.get("trade_plan"), dict) else None
        if not isinstance(plan, dict):
            return
        opt = plan.get("option") if isinstance(plan.get("option"), dict) else None
        if not isinstance(opt, dict):
            return
        risk_in = plan.get("risk") if isinstance(plan.get("risk"), dict) else {}
        try:
            contracts = int(plan.get("contracts") or 0)
        except Exception:
            contracts = 0
        if contracts <= 0:
            return
        self.trade = ActiveTrade(
            trade_id=str(plan.get("trade_id") or ""),
            direction=str(plan.get("direction") or ""),
            option={"right": opt.get("right"), "expiration": opt.get("expiration"), "strike": opt.get("strike")},
            option_symbol=option_symbol,
            contracts_total=contracts,
            contracts_remaining=contracts,
            entry_time=str(res.get("timestamp") or ""),
            entry_premium=None,
            risk={
                "stop_loss_premium": risk_in.get("stop_loss_premium"),
                "take_profit_premium": plan.get("take_profit_premium"),
                "time_stop_minutes": risk_in.get("time_stop_minutes"),
            },
        )
        self.state = TradeState.IN_POSITION
        self.follow_up = FollowUpState(armed=False)
        self.watches = []

    def on_position_decision(self, decision: dict[str, Any]) -> None:
        if not self.trade:
            return
        d = decision.get("decision") if isinstance(decision.get("decision"), dict) else None
        if not isinstance(d, dict):
            return
        act = str(d.get("action") or "")
        if act == "close_all":
            self.trade.contracts_remaining = 0
        elif act == "close_partial":
            exit_ = d.get("exit") if isinstance(d.get("exit"), dict) else None
            n = int(exit_.get("contracts_to_close") or 0) if isinstance(exit_, dict) else 0
            self.trade.contracts_remaining = max(0, self.trade.contracts_remaining - max(0, n))
        elif act == "tighten_stop":
            adj = d.get("adjustments") if isinstance(d.get("adjustments"), dict) else None
            if isinstance(adj, dict) and adj.get("new_stop_loss_premium") is not None:
                try:
                    self.trade.risk["stop_loss_premium"] = float(adj.get("new_stop_loss_premium"))
                except Exception:
                    pass
        elif act == "adjust_take_profit":
            adj = d.get("adjustments") if isinstance(d.get("adjustments"), dict) else None
            if isinstance(adj, dict) and adj.get("new_take_profit_premium") is not None:
                try:
                    self.trade.risk["take_profit_premium"] = float(adj.get("new_take_profit_premium"))
                except Exception:
                    pass
        elif act == "update_time_stop":
            adj = d.get("adjustments") if isinstance(d.get("adjustments"), dict) else None
            if isinstance(adj, dict) and adj.get("new_time_stop_minutes") is not None:
                try:
                    old_total = int(self.trade.risk.get("time_stop_minutes") or 0)
                    delta = int(adj.get("new_time_stop_minutes"))
                    self.trade.risk["time_stop_minutes"] = max(0, old_total) + max(0, delta)
                except Exception:
                    pass

        if self.trade.contracts_remaining <= 0:
            self.state = TradeState.SCAN
            self.trade = None
            self.follow_up = FollowUpState(armed=False)
            self.watches = []
            self.manage_inflight = False
            self.analysis_inflight = False

    def update_watches(self, now_epoch: int) -> None:
        if not self.watches:
            return
        self.watches = [w for w in self.watches if now_epoch < w.expires_at_epoch_s]
        if not self.watches and self.state == TradeState.WATCH_PENDING:
            self.state = TradeState.SCAN


def _to_epoch_seconds(iso: str) -> int:
    from datetime import datetime

    if not iso:
        return 0
    try:
        dt = datetime.fromisoformat(iso.replace("Z", "+00:00"))
        return int(dt.timestamp())
    except Exception:
        return 0
