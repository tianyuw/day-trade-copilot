# Alpaca News API (v1beta1) Documentation

## 1. Overview
The News API provides access to historical and real-time financial news articles (Benzinga).
- **Base URL (REST)**: `https://data.alpaca.markets/v1beta1`
- **Base URL (WebSocket)**: `wss://stream.data.alpaca.markets/v1beta1/news`

## 2. Historical News (REST)

### 2.1 Get News
**GET /v1beta1/news**
Returns a list of news articles based on query parameters.

**Parameters:**
- `symbols` (string, optional): Comma-separated list of tickers (e.g., `AAPL,TSLA`). If omitted, returns news for all symbols.
- `start` (string, optional): ISO 8601 timestamp.
- `end` (string, optional): ISO 8601 timestamp.
- `limit` (int, optional): Max 50. Default 10.
- `sort` (string, optional): `ASC` or `DESC` (default).
- `include_content` (bool, optional): Include full article content. Default `false`.
- `exclude_contentless` (bool, optional): Exclude articles with no content. Default `false`.
- `page_token` (string, optional).

**Response:**
```json
{
  "news": [
    {
      "id": 12345678,
      "headline": "Example News Headline",
      "author": "Benzinga",
      "created_at": "2023-10-27T14:30:00Z",
      "updated_at": "2023-10-27T14:35:00Z",
      "summary": "Brief summary...",
      "content": "Full content...",
      "url": "https://...",
      "symbols": ["AAPL"],
      "source": "benzinga"
    }
  ],
  "next_page_token": "..."
}
```

## 3. Real-Time News (WebSocket)

### 3.1 Connection
1. **Connect** to `wss://stream.data.alpaca.markets/v1beta1/news`
2. **Authenticate** (Same as Stocks API).
3. **Subscribe**:
   ```json
   {
     "action": "subscribe",
     "news": ["*"] 
   }
   ```
   *Note: Pass `["*"]` for all news or `["AAPL", "TSLA"]` for specific symbols.*

### 3.2 Message Format
```json
[
  {
    "T": "n",
    "id": 12345678,
    "headline": "Breaking News",
    "summary": "Summary text...",
    "created_at": "2023-10-27T15:00:00Z",
    "symbols": ["SPY"],
    "url": "https://..."
  }
]
```
