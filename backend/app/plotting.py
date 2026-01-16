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

    for i, ind in enumerate(indicators):
        if i < len(df):
            df.iloc[i, df.columns.get_loc('EMA9')] = ind.get('ema9')
            df.iloc[i, df.columns.get_loc('EMA21')] = ind.get('ema21')
            df.iloc[i, df.columns.get_loc('VWAP')] = ind.get('vwap')
            df.iloc[i, df.columns.get_loc('BBUpper')] = ind.get('bb_upper')
            df.iloc[i, df.columns.get_loc('BBMiddle')] = ind.get('bb_middle')
            df.iloc[i, df.columns.get_loc('BBLower')] = ind.get('bb_lower')
            df.iloc[i, df.columns.get_loc('MACD_DIF')] = ind.get('macd_dif')
            df.iloc[i, df.columns.get_loc('MACD_DEA')] = ind.get('macd_dea')
            df.iloc[i, df.columns.get_loc('MACD_Hist')] = ind.get('macd_hist')

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

    # Create addplots for indicators
    apds = [
        # Main Chart Overlays
        mpf.make_addplot(df['EMA9'], color='#22c55e', width=1, panel=0), # Green
        mpf.make_addplot(df['EMA21'], color='#f87171', width=1, panel=0), # Red
        mpf.make_addplot(df['VWAP'], color='#f8fafc', width=1, panel=0), # White
        mpf.make_addplot(df['BBUpper'], color='#a855f7', width=0.8, panel=0), # Purple
        mpf.make_addplot(df['BBMiddle'], color='#3b82f6', width=0.8, panel=0), # Blue
        mpf.make_addplot(df['BBLower'], color='#facc15', width=0.8, panel=0), # Yellow
        
        # MACD Subplot (Panel 2, since Volume is Panel 1 by default if volume=True)
        # However, we want MACD to be explicit.
        # Let's use panel=2 for MACD
        mpf.make_addplot(df['MACD_DIF'], color='#ffffff', width=1, panel=2, ylabel='MACD'), # White
        mpf.make_addplot(df['MACD_DEA'], color='#facc15', width=1, panel=2), # Yellow
        mpf.make_addplot(df['MACD_Hist'], type='bar', color=['#22c55e' if x >= 0 else '#ef4444' for x in df['MACD_Hist']], panel=2, alpha=0.5),
    ]

    # Buffer to save image
    buf = io.BytesIO()
    
    # Plot
    # volume=True puts volume in panel 1
    # We want tight layout
    mpf.plot(
        df,
        type='candle',
        style=style,
        addplot=apds,
        volume=True,
        panel_ratios=(6, 2, 2), # Main:Volume:MACD ratios
        figsize=(12, 8),
        savefig=dict(fname=buf, format='png', bbox_inches='tight', pad_inches=0.1),
        tight_layout=True,
        scale_width_adjustment=dict(volume=0.7, candle=1.2)
    )
    
    buf.seek(0)
    img_str = base64.b64encode(buf.read()).decode('utf-8')
    return img_str
