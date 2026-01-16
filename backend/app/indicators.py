import numpy as np
import pandas as pd
from typing import Dict, List, Optional

class ZScoreMomentum:
    def __init__(self, daily_bars: List[dict], period: int = 30):
        """
        Initialize with historical daily bars to calculate baseline stats.
        daily_bars: list of dicts with 'c' (close) and 't' (time)
        period: lookback period for daily stats
        """
        self.period = period
        self.ema5 = None
        self.prev_ema5 = None
        self.prev_diff = None
        
        # Calculate Daily Mean and StdDev from history
        if len(daily_bars) >= period:
            # Sort by time just in case
            sorted_bars = sorted(daily_bars, key=lambda x: x['t'])
            # Take the last 'period' days
            closes = [b['c'] for b in sorted_bars[-period:]]
            self.daily_mean = np.mean(closes)
            self.daily_std = np.std(closes)
        else:
            # Fallback if not enough data
            self.daily_mean = 0
            self.daily_std = 1
            if len(daily_bars) > 0:
                closes = [b['c'] for b in daily_bars]
                self.daily_mean = np.mean(closes)
                self.daily_std = np.std(closes) if len(closes) > 1 else 1

    def update(self, current_price: float) -> Dict[str, float | str | None]:
        """
        Update with intraday minute bar close price.
        Returns a dict containing:
          - z_score_diff: EMA5(z) - EMA5(z)[1]
          - signal: 'long' | 'short' | None
        """
        if self.daily_std == 0:
            z_score = 0
        else:
            z_score = (current_price - self.daily_mean) / self.daily_std
            
        # Calculate EMA5 of Z-Score
        # EMA_today = (Value_today * (k)) + (EMA_yesterday * (1-k))
        # k = 2 / (N + 1) = 2 / 6 = 1/3
        k = 2 / (5 + 1)
        
        if self.ema5 is None:
            self.ema5 = z_score
            self.prev_ema5 = z_score # Initial diff will be 0
        else:
            self.prev_ema5 = self.ema5
            self.ema5 = (z_score * k) + (self.prev_ema5 * (1 - k))
            
        diff = self.ema5 - self.prev_ema5
        
        signal = None
        if self.prev_diff is not None:
            # Check for crossovers
            # Upper Threshold: 0.006
            # Lower Threshold: -0.006
            if diff > 0.006 and self.prev_diff <= 0.006:
                signal = "long"
            elif diff < -0.006 and self.prev_diff >= -0.006:
                signal = "short"
        
        self.prev_diff = diff
        
        return {"z_score_diff": diff, "signal": signal}


class MACD:
    def __init__(self, fast_period: int = 12, slow_period: int = 26, signal_period: int = 9):
        self.fast_period = fast_period
        self.slow_period = slow_period
        self.signal_period = signal_period
        
        self.ema_fast = None
        self.ema_slow = None
        self.dea = None
        
        self.prev_dif = None
        self.prev_dea = None
        
        # Pre-calculate alpha values
        self.alpha_fast = 2 / (fast_period + 1)
        self.alpha_slow = 2 / (slow_period + 1)
        self.alpha_signal = 2 / (signal_period + 1)

    def update(self, current_price: float) -> Dict[str, float | str | None]:
        # Update Fast EMA
        if self.ema_fast is None:
            self.ema_fast = current_price
        else:
            self.ema_fast = (current_price * self.alpha_fast) + (self.ema_fast * (1 - self.alpha_fast))
            
        # Update Slow EMA
        if self.ema_slow is None:
            self.ema_slow = current_price
        else:
            self.ema_slow = (current_price * self.alpha_slow) + (self.ema_slow * (1 - self.alpha_slow))
            
        # Calculate DIF
        dif = self.ema_fast - self.ema_slow
        
        # Update DEA (EMA of DIF)
        if self.dea is None:
            self.dea = dif
        else:
            self.dea = (dif * self.alpha_signal) + (self.dea * (1 - self.alpha_signal))
            
        # Calculate Histogram
        hist = (dif - self.dea) * 2
        
        # Signal Detection
        signal = None
        if self.prev_dif is not None and self.prev_dea is not None:
            # Golden Cross: DIF crosses above DEA
            if dif > self.dea and self.prev_dif <= self.prev_dea:
                signal = "long"
            # Death Cross: DIF crosses below DEA
            elif dif < self.dea and self.prev_dif >= self.prev_dea:
                signal = "short"
                
        self.prev_dif = dif
        self.prev_dea = self.dea
        
        return {
            "macd_dif": dif,
            "macd_dea": self.dea,
            "macd_hist": hist,
            "signal": signal
        }
