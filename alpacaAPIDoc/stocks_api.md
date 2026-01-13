# Alpaca Stocks Data API (v2) Documentation

## 1. Overview
The Stocks Data API (v2) provides historical and real-time market data for US equities.
- **Base URL (REST)**: `https://data.alpaca.markets/v2`
- **Base URL (WebSocket)**: 
  - IEX (Free): `wss://stream.data.alpaca.markets/v2/iex`
  - SIP (Paid): `wss://stream.data.alpaca.markets/v2/sip`

## 2. Historical Data (REST)

### 2.1 Historical Bars
**GET /v2/stocks/bars**
Returns aggregate historical data (OHLCV) for the requested symbols.

**Parameters:**
- `symbols` (string, required): Comma-separated list of symbols (e.g., "AAPL,MSFT").
- `timeframe` (string, required): Timeframe for the aggregation. Values: `1Min`, `5Min`, `15Min`, `1H`, `1D`.
- `start` (string, optional): Filter data equal to or after this time (RFC-3339 format).
- `end` (string, optional): Filter data equal to or before this time (RFC-3339 format).
- `limit` (int, optional): Number of data points to return. Default 1000, max 10000.
- `adjustment` (string, optional): `raw`, `split`, `dividend`, or `all`. Default `raw`.
- `feed` (string, optional): `iex` or `sip`. Default `iex`.
- `page_token` (string, optional): Pagination token.

**Response:**
```json
{
  "bars": {
    "AAPL": [
      {
        "t": "2023-10-25T14:30:00Z",
        "o": 171.88,
        "h": 172.05,
        "l": 171.88,
        "c": 172.01,
        "v": 5000,
        "n": 100,
        "vw": 171.95
      }
    ]
  },
  "next_page_token": "A..."
}
```

### 2.2 Historical Trades
**GET /v2/stocks/trades**
Returns historical trade data for the requested symbols.

**Parameters:**
- `symbols` (string, required): Comma-separated list of symbols.
- `start` / `end` (string, optional): RFC-3339 timestamps.
- `limit` (int, optional): Default 1000.
- `feed` (string, optional): `iex` or `sip`.

**Response:**
```json
{
  "trades": {
    "AAPL": [
      {
        "t": "2023-10-25T14:30:00.005Z",
        "x": "V",
        "p": 172.01,
        "s": 100,
        "c": ["@"],
        "i": 12345,
        "z": "C"
      }
    ]
  }
}
```

### 2.3 Historical Quotes
**GET /v2/stocks/quotes**
Returns historical NBBO quotes for the requested symbols.

**Parameters:**
- `symbols` (string, required).
- `start` / `end` (string, optional).
- `limit` (int, optional).
- `feed` (string, optional).

### 2.4 Snapshots
**GET /v2/stocks/snapshots**
Returns the most recent trade, quote, and minute bar for the requested symbols.

**Parameters:**
- `symbols` (string, required): Comma-separated list of symbols.
- `feed` (string, optional): `iex` or `sip`.

**Response:**
```json
{
  "AAPL": {
    "latestTrade": { ... },
    "latestQuote": { ... },
    "minuteBar": { ... },
    "dailyBar": { ... },
    "prevDailyBar": { ... }
  }
}
```

## 3. Real-Time Data (WebSocket)

### 3.1 Connection
1. **Connect** to the WebSocket URL.
2. **Authenticate**:
   ```json
   {"action": "auth", "key": "YOUR_KEY", "secret": "YOUR_SECRET"}
   ```
3. **Subscribe**:
   ```json
   {
     "action": "subscribe", 
     "bars": ["AAPL"], 
     "trades": ["*"], 
     "quotes": ["AMD"]
   }
   ```

### 3.2 Channels
- **bars**: Minute bars.
- **dailyBars**: Daily bars.
- **trades**: Real-time trades.
- **quotes**: Real-time quotes (NBBO).
- **statuses**: Trading statuses (e.g., trading halts).
- **luld**: Limit Up-Limit Down bands.

### 3.3 Message Format
Messages are arrays of objects.
```json
[
  {
    "T": "b",
    "S": "AAPL",
    "o": 170.5,
    "h": 171.0,
    "l": 170.2,
    "c": 170.9,
    "v": 10000,
    "t": "2023-10-25T14:31:00Z"
  }
]
```
