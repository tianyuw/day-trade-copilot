import io
import base64
import pandas as pd
import mplfinance as mpf
from typing import List, Dict

def generate_chart_image(bars: List[Dict], indicators: List[Dict]) -> str:
    """
    Generate a chart image from bar data and indicators using mplfinance.
    Returns base64 encoded string of the image.
    """
    if not bars:
        return ""

    # Convert to DataFrame
    df = pd.DataFrame(bars)
    df['Date'] = pd.to_datetime(df['t'])
    df.set_index('Date', inplace=True)
    
    # Rename columns to match mplfinance expectations
    df.rename(columns={
        'o': 'Open',
        'h': 'High',
        'l': 'Low',
        'c': 'Close',
        'v': 'Volume'
    }, inplace=True)

    for col in ("Open", "High", "Low", "Close", "Volume"):
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    df = df.dropna(subset=["Open", "High", "Low", "Close"])
    if df.empty:
        return ""
    
    # Prepare indicator dataframes
    # We assume indicators list aligns with bars
    # Extract indicators into columns
    
    # Initialize indicator columns with NaN
    df['EMA9'] = float('nan')
    df['EMA21'] = float('nan')
    df['VWAP'] = float('nan')
    df['BBUpper'] = float('nan')
    df['BBMiddle'] = float('nan')
    df['BBLower'] = float('nan')
    df['MACD_DIF'] = float('nan')
    df['MACD_DEA'] = float('nan')
    df['MACD_Hist'] = float('nan')

    def _num(x) -> float:
        try:
            if x is None or (isinstance(x, float) and pd.isna(x)) or pd.isna(x):
                return float("nan")
            return float(x)
        except Exception:
            return float("nan")

    for i, ind in enumerate(indicators):
        if i < len(df):
            df.iloc[i, df.columns.get_loc('EMA9')] = _num(ind.get('ema9'))
            df.iloc[i, df.columns.get_loc('EMA21')] = _num(ind.get('ema21'))
            df.iloc[i, df.columns.get_loc('VWAP')] = _num(ind.get('vwap'))
            df.iloc[i, df.columns.get_loc('BBUpper')] = _num(ind.get('bb_upper'))
            df.iloc[i, df.columns.get_loc('BBMiddle')] = _num(ind.get('bb_middle'))
            df.iloc[i, df.columns.get_loc('BBLower')] = _num(ind.get('bb_lower'))
            df.iloc[i, df.columns.get_loc('MACD_DIF')] = _num(ind.get('macd_dif'))
            df.iloc[i, df.columns.get_loc('MACD_DEA')] = _num(ind.get('macd_dea'))
            df.iloc[i, df.columns.get_loc('MACD_Hist')] = _num(ind.get('macd_hist'))

    # Create custom style to match frontend
    # Frontend colors:
    # Up: #22d3ee (Cyan), Down: #f87171 (Red)
    # Background: Black/Transparent (we'll use dark gray for image)
    # Grid: White alpha 0.06
    
    marketcolors = mpf.make_marketcolors(
        up='#22d3ee',
        down='#f87171',
        edge={'up': '#22d3ee', 'down': '#f87171'},
        wick={'up': '#22d3ee', 'down': '#f87171'},
        volume={'up': '#224444', 'down': '#442222'}, # Darker volume
    )
    
    style = mpf.make_mpf_style(
        marketcolors=marketcolors,
        gridstyle='dotted',
        gridcolor='#333333',
        facecolor='#0f172a', # Slate-900 like background
        edgecolor='#333333',
        figcolor='#0f172a',
        rc={'text.color': 'white', 'axes.labelcolor': 'white', 'xtick.color': 'white', 'ytick.color': 'white'}
    )

    def _has_values(s: pd.Series) -> bool:
        try:
            return not s.dropna().empty
        except Exception:
            return False

    volume_ok = False
    if "Volume" in df.columns:
        vol = df["Volume"]
        if _has_values(vol) and float(vol.fillna(0).abs().sum()) > 0:
            volume_ok = True

    macd_panel = 2 if volume_ok else 1
    apds = []

    if _has_values(df["EMA9"]):
        apds.append(mpf.make_addplot(df["EMA9"], color="#22c55e", width=1, panel=0))
    if _has_values(df["EMA21"]):
        apds.append(mpf.make_addplot(df["EMA21"], color="#f87171", width=1, panel=0))
    if _has_values(df["VWAP"]):
        apds.append(mpf.make_addplot(df["VWAP"], color="#f8fafc", width=1, panel=0))
    if _has_values(df["BBUpper"]):
        apds.append(mpf.make_addplot(df["BBUpper"], color="#a855f7", width=0.8, panel=0))
    if _has_values(df["BBMiddle"]):
        apds.append(mpf.make_addplot(df["BBMiddle"], color="#3b82f6", width=0.8, panel=0))
    if _has_values(df["BBLower"]):
        apds.append(mpf.make_addplot(df["BBLower"], color="#facc15", width=0.8, panel=0))

    macd_apds = []
    if _has_values(df["MACD_DIF"]):
        macd_apds.append(mpf.make_addplot(df["MACD_DIF"], color="#ffffff", width=1, panel=macd_panel, ylabel="MACD"))
    if _has_values(df["MACD_DEA"]):
        macd_apds.append(mpf.make_addplot(df["MACD_DEA"], color="#facc15", width=1, panel=macd_panel))
    if _has_values(df["MACD_Hist"]):
        hist = df["MACD_Hist"]
        colors = ["#22c55e" if pd.notna(x) and float(x) >= 0 else "#ef4444" for x in hist]
        macd_apds.append(mpf.make_addplot(hist, type="bar", color=colors, panel=macd_panel, alpha=0.5))

    apds.extend(macd_apds)

    has_macd_panel = len(macd_apds) > 0
    if volume_ok and has_macd_panel:
        panel_ratios = (6, 2, 2)
    elif volume_ok or has_macd_panel:
        panel_ratios = (6, 2)
    else:
        panel_ratios = None

    # Buffer to save image
    buf = io.BytesIO()
    
    # Plot
    # volume=True puts volume in panel 1
    # We want tight layout
    plot_kwargs = dict(
        type="candle",
        style=style,
        volume=volume_ok,
        figsize=(12, 8),
        savefig=dict(fname=buf, format="png", bbox_inches="tight", pad_inches=0.1),
        tight_layout=True,
    )
    if apds:
        plot_kwargs["addplot"] = apds
    scale_adj = {"candle": 1.2}
    if volume_ok:
        scale_adj["volume"] = 0.7
    plot_kwargs["scale_width_adjustment"] = scale_adj
    if panel_ratios is not None:
        plot_kwargs["panel_ratios"] = panel_ratios

    try:
        mpf.plot(df, **plot_kwargs)
    except Exception:
        return ""
    
    buf.seek(0)
    img_str = base64.b64encode(buf.read()).decode('utf-8')
    return img_str
