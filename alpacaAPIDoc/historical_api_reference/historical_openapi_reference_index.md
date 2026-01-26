# Alpaca Historical API Reference（OpenAPI 索引）

此文件由 `alpacaAPIDoc/historical_api_reference/historical_openapi.yaml` 自动提取生成，便于快速查找每个 REST 端点。

## Crypto Pricing Data API

| Method | Path | Summary | Reference |
|---|---|---|---|
| GET | /v1beta1/crypto/bars | Get Bars for multiple Crypto symbols | [getBarsForMultipleCryptoSymbols](https://docs.alpaca.markets/reference/getBarsForMultipleCryptoSymbols) |
| GET | /v1beta1/crypto/bars/latest | Get Latest Bars for multiple Crypto symbols | [getLatestBarsForMultipleCryptoSymbols](https://docs.alpaca.markets/reference/getLatestBarsForMultipleCryptoSymbols) |
| GET | /v1beta1/crypto/meta/spreads | Get list of crypto spreads per exchange | [getCryptoMetaSpreads](https://docs.alpaca.markets/reference/getCryptoMetaSpreads) |
| GET | /v1beta1/crypto/quotes | Get Quotes for multiple crypto symbols | [getQuotesForMultipleCryptoSymbols](https://docs.alpaca.markets/reference/getQuotesForMultipleCryptoSymbols) |
| GET | /v1beta1/crypto/quotes/latest | Get Latest Quotes for multiple Crypto symbols | [getLatestQuotesForMultipleCryptoSymbols](https://docs.alpaca.markets/reference/getLatestQuotesForMultipleCryptoSymbols) |
| GET | /v1beta1/crypto/snapshots | Get Snapshots for multiple crypto symbols | [getSnapshotsForMultipleCryptoSymbols](https://docs.alpaca.markets/reference/getSnapshotsForMultipleCryptoSymbols) |
| GET | /v1beta1/crypto/trades | Get Trade data for multiple crypto symbols | [getTradesForMultipleCryptoSymbols](https://docs.alpaca.markets/reference/getTradesForMultipleCryptoSymbols) |
| GET | /v1beta1/crypto/trades/latest | Get Latest Trade data for multiple Crypto symbols | [getLatestTradesForMultipleCryptoSymbols](https://docs.alpaca.markets/reference/getLatestTradesForMultipleCryptoSymbols) |
| GET | /v1beta1/crypto/xbbos/latest | Get Latest XBBO for multiple crypto symbols | [getLatestXBBOForMultipleCryptoSymbols](https://docs.alpaca.markets/reference/getLatestXBBOForMultipleCryptoSymbols) |
| GET | /v1beta1/crypto/{symbol}/bars | Get Bar data for a crypto symbol | [getBarsForCryptoSymbol](https://docs.alpaca.markets/reference/getBarsForCryptoSymbol) |
| GET | /v1beta1/crypto/{symbol}/bars/latest | Get Latest Bar data for a Crypto symbol | [getLatestBarsForCryptoSymbol](https://docs.alpaca.markets/reference/getLatestBarsForCryptoSymbol) |
| GET | /v1beta1/crypto/{symbol}/quotes | Get Quotes for crypto symbol | [getQuotesForCryptoSymbol](https://docs.alpaca.markets/reference/getQuotesForCryptoSymbol) |
| GET | /v1beta1/crypto/{symbol}/quotes/latest | Latest Quote | [getLatestQuoteForCryptoSymbol](https://docs.alpaca.markets/reference/getLatestQuoteForCryptoSymbol) |
| GET | /v1beta1/crypto/{symbol}/snapshot | Get a Snapshot for a crypto symbol | [getSnapshotForCryptoSymbol](https://docs.alpaca.markets/reference/getSnapshotForCryptoSymbol) |
| GET | /v1beta1/crypto/{symbol}/trades | Get Trade data for a crypto symbol | [getTradesForCryptoSymbol](https://docs.alpaca.markets/reference/getTradesForCryptoSymbol) |
| GET | /v1beta1/crypto/{symbol}/trades/latest | Latest Trades | [getLatestTradesForCryptoSymbol](https://docs.alpaca.markets/reference/getLatestTradesForCryptoSymbol) |
| GET | /v1beta1/crypto/{symbol}/xbbo/latest | Get Latest XBBO for a single crypto symbol | [getLatestXBBOForCryptoSymbol](https://docs.alpaca.markets/reference/getLatestXBBOForCryptoSymbol) |

## Logo

| Method | Path | Summary | Reference |
|---|---|---|---|
| GET | /v1beta1/logos/{crypto_or_stock_symbol} | Get Logo for symbol | [getLogoForSymbol](https://docs.alpaca.markets/reference/getLogoForSymbol) |

## News

| Method | Path | Summary | Reference |
|---|---|---|---|
| GET | /v1beta1/news | News API | [getNews](https://docs.alpaca.markets/reference/getNews) |

## Screener

| Method | Path | Summary | Reference |
|---|---|---|---|
| GET | /v1beta1/screener/{market_type}/movers | Get Top Market Movers by Market type | [getTopMoversByMarketType](https://docs.alpaca.markets/reference/getTopMoversByMarketType) |

## Stock Pricing Data API

| Method | Path | Summary | Reference |
|---|---|---|---|
| GET | /v2/stocks/bars | Get Bar data for multiple stock symbols | [getBarsForMultipleStockSymbols](https://docs.alpaca.markets/reference/getBarsForMultipleStockSymbols) |
| GET | /v2/stocks/bars/latest | Get Latest Bar data for multiple stock symbols | [getLatestBarsForMultipleStockSymbols](https://docs.alpaca.markets/reference/getLatestBarsForMultipleStockSymbols) |
| GET | /v2/stocks/meta/conditions/{type} | Get list of Conditions | [getConditions](https://docs.alpaca.markets/reference/getConditions) |
| GET | /v2/stocks/meta/exchanges | Get List of supported exchanges | [getExchanges](https://docs.alpaca.markets/reference/getExchanges) |
| GET | /v2/stocks/quotes | Get Quotes for multiple stock symbols | [getQuotesForMultipleStockSymbols](https://docs.alpaca.markets/reference/getQuotesForMultipleStockSymbols) |
| GET | /v2/stocks/quotes/latest | Get Latest Quotes for multiple stock symbols | [getLatestQuotesForMultipleStockSymbols](https://docs.alpaca.markets/reference/getLatestQuotesForMultipleStockSymbols) |
| GET | /v2/stocks/snapshots | Get Snapshots for multiple stock symbols | [getSnapshotsForMultipleStockSymbols](https://docs.alpaca.markets/reference/getSnapshotsForMultipleStockSymbols) |
| GET | /v2/stocks/trades | Get Trade data for multiple stock symbols | [getTradesForMultipleStockSymbols](https://docs.alpaca.markets/reference/getTradesForMultipleStockSymbols) |
| GET | /v2/stocks/trades/latest | Get Latest Trades data for multiple stock symbols | [getLatestTradesForMultipleStockSymbols](https://docs.alpaca.markets/reference/getLatestTradesForMultipleStockSymbols) |
| GET | /v2/stocks/{symbol}/bars | Bars | [getBarsForStockSymbol](https://docs.alpaca.markets/reference/getBarsForStockSymbol) |
| GET | /v2/stocks/{symbol}/bars/latest | Get Latest Bars for Symbol | [getLatestBarForStockSymbol](https://docs.alpaca.markets/reference/getLatestBarForStockSymbol) |
| GET | /v2/stocks/{symbol}/quotes | Get Quotes for stock symbol | [getQuotesForStockSymbol](https://docs.alpaca.markets/reference/getQuotesForStockSymbol) |
| GET | /v2/stocks/{symbol}/quotes/latest | Get Latest Quote for stock symbol | [getLatestQuoteForStockSymbol](https://docs.alpaca.markets/reference/getLatestQuoteForStockSymbol) |
| GET | /v2/stocks/{symbol}/snapshot | Get a Snapshot for a stock symbol | [getSnapshotForStockSymbol](https://docs.alpaca.markets/reference/getSnapshotForStockSymbol) |
| GET | /v2/stocks/{symbol}/trades | Trades | [getTradesForStockSymbol](https://docs.alpaca.markets/reference/getTradesForStockSymbol) |
| GET | /v2/stocks/{symbol}/trades/latest | Latest Trade | [getLatestTradeForStockSymbol](https://docs.alpaca.markets/reference/getLatestTradeForStockSymbol) |
