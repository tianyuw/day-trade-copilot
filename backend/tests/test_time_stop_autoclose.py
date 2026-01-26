import asyncio

import pytest

from app.schemas import PositionManagementResponse
from app.stream_autopilot import run_manage_position
from app.trade_session import ActiveTrade, SymbolSession, TradeState


class _WS:
    def __init__(self) -> None:
        self.sent: list[dict] = []

    async def send_json(self, data: dict) -> None:
        self.sent.append(data)


class _Svc:
    def __init__(self, *, fail_if_called: bool) -> None:
        self.fail_if_called = fail_if_called
        self.calls: int = 0

    async def manage_position(self, req) -> PositionManagementResponse:
        self.calls += 1
        if self.fail_if_called:
            raise AssertionError("manage_position should not be called when time stop hits")
        return PositionManagementResponse(
            trade_id=req.trade_id,
            analysis_id="stub",
            timestamp=req.bar_time,
            symbol=req.symbol,
            bar_time=req.bar_time,
            decision={"action": "hold", "reasoning": "stub", "exit": None, "adjustments": None},
            position_option_quote=None,
            option_symbol=req.option_symbol,
        )


def _mk_session(*, entry_time: str, time_stop_minutes: int) -> SymbolSession:
    s = SymbolSession(symbol="META", mode="playback")
    s.state = TradeState.IN_POSITION
    s.trade = ActiveTrade(
        trade_id="t1",
        direction="long",
        option={"right": "call", "expiration": "2026-01-23", "strike": 660.0},
        option_symbol="META260123C00660000",
        contracts_total=5,
        contracts_remaining=5,
        entry_time=entry_time,
        entry_premium=3.0,
        risk={"time_stop_minutes": time_stop_minutes, "stop_loss_premium": None, "take_profit_premium": None},
    )
    return s


@pytest.mark.asyncio
async def test_time_stop_autoclose_skips_llm_call() -> None:
    ws = _WS()
    svc = _Svc(fail_if_called=True)
    sem = asyncio.Semaphore(1)
    s = _mk_session(entry_time="2026-01-01T00:00:00Z", time_stop_minutes=15)

    payload = await run_manage_position(
        ws,
        mode="playback",
        sem=sem,
        analysis_service=svc,
        session=s,
        bar_time="2026-01-01T00:15:00Z",
        ohlcv_1m=None,
        last_state_sent={},
    )
    assert payload is not None
    assert payload["decision"]["action"] == "close_all"
    assert svc.calls == 0
    assert s.trade is None
    assert s.state == TradeState.SCAN


@pytest.mark.asyncio
async def test_time_stop_not_hit_calls_llm() -> None:
    ws = _WS()
    svc = _Svc(fail_if_called=False)
    sem = asyncio.Semaphore(1)
    s = _mk_session(entry_time="2026-01-01T00:00:00Z", time_stop_minutes=15)

    payload = await run_manage_position(
        ws,
        mode="playback",
        sem=sem,
        analysis_service=svc,
        session=s,
        bar_time="2026-01-01T00:14:00Z",
        ohlcv_1m=None,
        last_state_sent={},
    )
    assert payload is not None
    assert payload["decision"]["action"] == "hold"
    assert svc.calls == 1
    assert s.trade is not None
    assert s.state == TradeState.IN_POSITION


@pytest.mark.asyncio
async def test_update_time_stop_is_increment_and_delays_autoclose() -> None:
    ws = _WS()
    sem = asyncio.Semaphore(1)
    s = _mk_session(entry_time="2026-01-01T00:00:00Z", time_stop_minutes=15)

    s.on_position_decision(
        {
            "decision": {
                "action": "update_time_stop",
                "reasoning": "extend",
                "exit": None,
                "adjustments": {"new_time_stop_minutes": 5},
            }
        }
    )
    assert s.trade is not None
    assert s.trade.risk.get("time_stop_minutes") == 20

    svc1 = _Svc(fail_if_called=False)
    payload_15 = await run_manage_position(
        ws,
        mode="playback",
        sem=sem,
        analysis_service=svc1,
        session=s,
        bar_time="2026-01-01T00:15:00Z",
        ohlcv_1m=None,
        last_state_sent={},
    )
    assert payload_15 is not None
    assert payload_15["decision"]["action"] == "hold"
    assert s.trade is not None

    svc2 = _Svc(fail_if_called=True)
    payload_20 = await run_manage_position(
        ws,
        mode="playback",
        sem=sem,
        analysis_service=svc2,
        session=s,
        bar_time="2026-01-01T00:20:00Z",
        ohlcv_1m=None,
        last_state_sent={},
    )
    assert payload_20 is not None
    assert payload_20["decision"]["action"] == "close_all"
    assert s.trade is None

