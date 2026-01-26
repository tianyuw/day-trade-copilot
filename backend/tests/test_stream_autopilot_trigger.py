from app.stream_autopilot import maybe_trigger_analysis
from app.trade_session import SymbolSession, TradeState, PendingWatch, FollowUpState


class _Bar:
    def __init__(self, t: str, c: float, signal: str | None):
        self.t = t
        self.c = c
        self.indicators = {"signal": signal} if signal else {}


def test_maybe_trigger_analysis() -> None:
    last_analyzed: dict[str, str] = {}
    s = SymbolSession(symbol="NVDA", mode="playback")

    b1 = _Bar("2026-01-01T00:00:00Z", 100.0, None)
    assert (
        maybe_trigger_analysis(session=s, bar=b1, has_quant_signal=False, last_analyzed_time=last_analyzed) is None
    ), "no signal should not trigger"

    b2 = _Bar("2026-01-01T00:01:00Z", 101.0, "long")
    assert (
        maybe_trigger_analysis(session=s, bar=b2, has_quant_signal=True, last_analyzed_time=last_analyzed) == "quant_signal"
    ), "signal should trigger"
    assert last_analyzed.get("NVDA") == b2.t, "signal should set last_analyzed_time"
    assert (
        maybe_trigger_analysis(session=s, bar=b2, has_quant_signal=True, last_analyzed_time=last_analyzed) is None
    ), "same bar.t should be deduped"

    s = SymbolSession(symbol="NVDA", mode="playback")
    s.state = TradeState.FOLLOW_UP_PENDING
    s.follow_up = FollowUpState(armed=True)
    last_analyzed = {}
    b3 = _Bar("2026-01-01T00:02:00Z", 102.0, None)
    assert (
        maybe_trigger_analysis(session=s, bar=b3, has_quant_signal=False, last_analyzed_time=last_analyzed) == "follow_up"
    ), "follow-up armed without signal should trigger"
    assert s.follow_up.armed is False, "follow-up should be disarmed when triggered"

    s = SymbolSession(symbol="NVDA", mode="playback")
    s.watches = [
        PendingWatch(trigger_price=105.0, direction="above", created_at_epoch_s=0, expires_at_epoch_s=9999999999),
    ]
    last_analyzed = {}
    b4 = _Bar("2026-01-01T00:03:00Z", 104.0, None)
    assert (
        maybe_trigger_analysis(session=s, bar=b4, has_quant_signal=False, last_analyzed_time=last_analyzed) is None
    ), "watch not hit should not trigger"
    b5 = _Bar("2026-01-01T00:04:00Z", 105.0, None)
    assert (
        maybe_trigger_analysis(session=s, bar=b5, has_quant_signal=False, last_analyzed_time=last_analyzed) == "watch_condition"
    ), "watch hit should trigger"
    assert len(s.watches) == 0, "hit watch should be removed"
