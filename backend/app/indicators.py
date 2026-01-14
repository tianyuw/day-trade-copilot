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

    def update(self, current_price: float) -> float:
        """
        Update with intraday minute bar close price.
        Returns the diff value: EMA5(z) - EMA5(z)[1]
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
        return diff
