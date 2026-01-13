# Alpaca Options Data API (v1beta1) Documentation

## 1. Overview
The Options Data API (v1beta1) provides historical and real-time market data for US options.
- **Base URL (REST)**: `https://data.alpaca.markets/v1beta1`
- **Base URL (WebSocket)**: `wss://stream.data.alpaca.markets/v1beta1/options`

## 2. Historical & Snapshot Data (REST)

### 2.1 Option Snapshots (Chain Data)
**GET /v1beta1/options/snapshots/{symbol_or_symbols}**
Returns the latest trade, quote, and Greeks for the requested option contracts. This is the primary endpoint for retrieving "Option Chain" data.

**Parameters:**
- `symbol_or_symbols` (path parameter): Comma-separated list of option symbols (e.g., `SPY231027C00420000`).
- `feed` (query param, optional): `indicative` (default) or `opra`.

**Response:**
```json
{
  "SPY231027C00420000": {
    "latestTrade": {
      "t": "2023-10-25T14:30:00Z",
      "p": 2.50,
      "s": 10,
      "x": "C",
      "c": ["@"]
    },
    "latestQuote": {
      "t": "2023-10-25T14:30:00Z",
      "bp": 2.48,
      "bs": 50,
      "ap": 2.52,
      "as": 45,
      "bx": "C",
      "ax": "C"
    },
    "greeks": {
      "delta": 0.54,
      "gamma": 0.05,
      "theta": -0.02,
      "vega": 0.15,
      "rho": 0.01
    },
    "impliedVolatility": 0.18
  }
}
```

### 2.2 Historical Bars
**GET /v1beta1/options/bars**
Returns historical OHLCV bars for option contracts.

**Parameters:**
- `symbols` (string, required): Comma-separated option symbols.
- `timeframe` (string, required): `1Min` (Currently only 1Min is supported for options).
- `start` / `end` (string, optional): RFC-3339 timestamps.
- `limit` (int, optional): Default 1000.
- `page_token` (string, optional).

**Response:**
Standard bar objects (`t`, `o`, `h`, `l`, `c`, `v`, `n`, `vw`).

### 2.3 Historical Trades
**GET /v1beta1/options/trades**
Returns historical trades for option contracts.

### 2.4 Historical Quotes
**GET /v1beta1/options/quotes**
Returns historical quotes for option contracts.

## 3. Real-Time Data (WebSocket)

### 3.1 Connection
1. **Connect** to `wss://stream.data.alpaca.markets/v1beta1/options`
2. **Authenticate** (Same as Stocks API).
3. **Subscribe**:
   ```json
   {
     "action": "subscribe",
     "trades": ["SPY231027C00420000"],
     "quotes": ["*"]
   }
   ```

### 3.2 Channels
- **trades**: Real-time option trades.
- **quotes**: Real-time option quotes.

### 3.3 Message Format
```json
[
  {
    "T": "t",
    "S": "SPY231027C00420000",
    "p": 2.55,
    "s": 5,
    "t": "2023-10-25T14:35:00Z",
    "c": ["@"]
  }
]
```
