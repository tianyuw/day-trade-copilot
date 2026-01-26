# Alpaca Historical API Reference（索引）

此文件由 `alpacaAPIDoc/historical_api_reference/reference/*.md` 的 OpenAPI JSON 自动提取生成，优先反映当前 docs.alpaca.markets 的 Reference 结构。

## Corporate actions

| Method | Path | Summary | Snapshot | Source |
|---|---|---|---|---|
| GET | /v1/corporate-actions | Corporate actions | [corporateactions-1](historical_api_reference/reference/corporateactions-1.md) | [corporateactions-1](https://docs.alpaca.markets/reference/corporateactions-1) |

## Crypto

| Method | Path | Summary | Snapshot | Source |
|---|---|---|---|---|
| GET | /v1beta3/crypto/{loc}/bars | Historical bars | [cryptobars-1](historical_api_reference/reference/cryptobars-1.md) | [cryptobars-1](https://docs.alpaca.markets/reference/cryptobars-1) |
| GET | /v1beta3/crypto/{loc}/latest/bars | Latest bars | [cryptolatestbars-1](historical_api_reference/reference/cryptolatestbars-1.md) | [cryptolatestbars-1](https://docs.alpaca.markets/reference/cryptolatestbars-1) |
| GET | /v1beta3/crypto/{loc}/latest/orderbooks | Latest orderbook | [cryptolatestorderbooks-1](historical_api_reference/reference/cryptolatestorderbooks-1.md) | [cryptolatestorderbooks-1](https://docs.alpaca.markets/reference/cryptolatestorderbooks-1) |
| GET | /v1beta3/crypto/{loc}/latest/quotes | Latest quotes | [cryptolatestquotes-1](historical_api_reference/reference/cryptolatestquotes-1.md) | [cryptolatestquotes-1](https://docs.alpaca.markets/reference/cryptolatestquotes-1) |
| GET | /v1beta3/crypto/{loc}/latest/trades | Latest trades | [cryptolatesttrades-1](historical_api_reference/reference/cryptolatesttrades-1.md) | [cryptolatesttrades-1](https://docs.alpaca.markets/reference/cryptolatesttrades-1) |
| GET | /v1beta3/crypto/{loc}/quotes | Historical quotes | [cryptoquotes-1](historical_api_reference/reference/cryptoquotes-1.md) | [cryptoquotes-1](https://docs.alpaca.markets/reference/cryptoquotes-1) |
| GET | /v1beta3/crypto/{loc}/snapshots | Snapshots | [cryptosnapshots-1](historical_api_reference/reference/cryptosnapshots-1.md) | [cryptosnapshots-1](https://docs.alpaca.markets/reference/cryptosnapshots-1) |
| GET | /v1beta3/crypto/{loc}/trades | Historical trades | [cryptotrades-1](historical_api_reference/reference/cryptotrades-1.md) | [cryptotrades-1](https://docs.alpaca.markets/reference/cryptotrades-1) |

## Fixed income

| Method | Path | Summary | Snapshot | Source |
|---|---|---|---|---|
| GET | /v1beta1/fixed_income/latest/prices | Latest prices | [fixedincomelatestprices](historical_api_reference/reference/fixedincomelatestprices.md) | [fixedincomelatestprices](https://docs.alpaca.markets/reference/fixedincomelatestprices) |

## Forex

| Method | Path | Summary | Snapshot | Source |
|---|---|---|---|---|
| GET | /v1beta1/forex/latest/rates | Latest rates for currency pairs | [latestrates-1](historical_api_reference/reference/latestrates-1.md) | [latestrates-1](https://docs.alpaca.markets/reference/latestrates-1) |
| GET | /v1beta1/forex/rates | Historical rates for currency pairs | [rates-1](historical_api_reference/reference/rates-1.md) | [rates-1](https://docs.alpaca.markets/reference/rates-1) |

## Logos

| Method | Path | Summary | Snapshot | Source |
|---|---|---|---|---|
| GET | /v1beta1/logos/{symbol} | Logos | [logos-5](historical_api_reference/reference/logos-5.md) | [logos-5](https://docs.alpaca.markets/reference/logos-5) |

## News

| Method | Path | Summary | Snapshot | Source |
|---|---|---|---|---|
| GET | /v1beta1/news | News articles | [news-3](historical_api_reference/reference/news-3.md) | [news-3](https://docs.alpaca.markets/reference/news-3) |

## Option

| Method | Path | Summary | Snapshot | Source |
|---|---|---|---|---|
| GET | /v1beta1/options/bars | Historical bars | [optionbars](historical_api_reference/reference/optionbars.md) | [optionbars](https://docs.alpaca.markets/reference/optionbars) |
| GET | /v1beta1/options/meta/conditions/{ticktype} | Condition codes | [optionmetaconditions](historical_api_reference/reference/optionmetaconditions.md) | [optionmetaconditions](https://docs.alpaca.markets/reference/optionmetaconditions) |
| GET | /v1beta1/options/meta/exchanges | Exchange codes | [optionmetaexchanges](historical_api_reference/reference/optionmetaexchanges.md) | [optionmetaexchanges](https://docs.alpaca.markets/reference/optionmetaexchanges) |
| GET | /v1beta1/options/quotes/latest | Latest quotes | [optionlatestquotes](historical_api_reference/reference/optionlatestquotes.md) | [optionlatestquotes](https://docs.alpaca.markets/reference/optionlatestquotes) |
| GET | /v1beta1/options/snapshots | Snapshots | [optionsnapshots](historical_api_reference/reference/optionsnapshots.md) | [optionsnapshots](https://docs.alpaca.markets/reference/optionsnapshots) |
| GET | /v1beta1/options/snapshots/{underlying_symbol} | Option chain | [optionchain](historical_api_reference/reference/optionchain.md) | [optionchain](https://docs.alpaca.markets/reference/optionchain) |
| GET | /v1beta1/options/trades | Historical trades | [optiontrades](historical_api_reference/reference/optiontrades.md) | [optiontrades](https://docs.alpaca.markets/reference/optiontrades) |
| GET | /v1beta1/options/trades/latest | Latest trades | [optionlatesttrades](historical_api_reference/reference/optionlatesttrades.md) | [optionlatesttrades](https://docs.alpaca.markets/reference/optionlatesttrades) |

## Screener

| Method | Path | Summary | Snapshot | Source |
|---|---|---|---|---|
| GET | /v1beta1/screener/stocks/most-actives | Most active stocks | [mostactives-1](historical_api_reference/reference/mostactives-1.md) | [mostactives-1](https://docs.alpaca.markets/reference/mostactives-1) |
| GET | /v1beta1/screener/{market_type}/movers | Top market movers | [movers-1](historical_api_reference/reference/movers-1.md) | [movers-1](https://docs.alpaca.markets/reference/movers-1) |

## Stock

| Method | Path | Summary | Snapshot | Source |
|---|---|---|---|---|
| GET | /v2/stocks/auctions | Historical auctions | [stockauctions-1](historical_api_reference/reference/stockauctions-1.md) | [stockauctions-1](https://docs.alpaca.markets/reference/stockauctions-1) |
| GET | /v2/stocks/bars | Historical bars | [stockbars](historical_api_reference/reference/stockbars.md) | [stockbars](https://docs.alpaca.markets/reference/stockbars) |
| GET | /v2/stocks/bars/latest | Latest bars | [stocklatestbars-1](historical_api_reference/reference/stocklatestbars-1.md) | [stocklatestbars-1](https://docs.alpaca.markets/reference/stocklatestbars-1) |
| GET | /v2/stocks/meta/conditions/{ticktype} | Condition codes | [stockmetaconditions-1](historical_api_reference/reference/stockmetaconditions-1.md) | [stockmetaconditions-1](https://docs.alpaca.markets/reference/stockmetaconditions-1) |
| GET | /v2/stocks/meta/exchanges | Exchange codes | [stockmetaexchanges-1](historical_api_reference/reference/stockmetaexchanges-1.md) | [stockmetaexchanges-1](https://docs.alpaca.markets/reference/stockmetaexchanges-1) |
| GET | /v2/stocks/quotes | Historical quotes | [stockquotes-1](historical_api_reference/reference/stockquotes-1.md) | [stockquotes-1](https://docs.alpaca.markets/reference/stockquotes-1) |
| GET | /v2/stocks/quotes/latest | Latest quotes | [stocklatestquotes-1](historical_api_reference/reference/stocklatestquotes-1.md) | [stocklatestquotes-1](https://docs.alpaca.markets/reference/stocklatestquotes-1) |
| GET | /v2/stocks/snapshots | Snapshots | [stocksnapshots-1](historical_api_reference/reference/stocksnapshots-1.md) | [stocksnapshots-1](https://docs.alpaca.markets/reference/stocksnapshots-1) |
| GET | /v2/stocks/trades | Historical trades | [stocktrades-1](historical_api_reference/reference/stocktrades-1.md) | [stocktrades-1](https://docs.alpaca.markets/reference/stocktrades-1) |
| GET | /v2/stocks/trades/latest | Latest trades | [stocklatesttrades-1](historical_api_reference/reference/stocklatesttrades-1.md) | [stocklatesttrades-1](https://docs.alpaca.markets/reference/stocklatesttrades-1) |
| GET | /v2/stocks/{symbol}/auctions | Historical auctions (single) | [stockauctionsingle-1](historical_api_reference/reference/stockauctionsingle-1.md) | [stockauctionsingle-1](https://docs.alpaca.markets/reference/stockauctionsingle-1) |
| GET | /v2/stocks/{symbol}/bars | Historical bars (single symbol) | [stockbarsingle-1](historical_api_reference/reference/stockbarsingle-1.md) | [stockbarsingle-1](https://docs.alpaca.markets/reference/stockbarsingle-1) |
| GET | /v2/stocks/{symbol}/bars/latest | Latest bar (single symbol) | [stocklatestbarsingle-1](historical_api_reference/reference/stocklatestbarsingle-1.md) | [stocklatestbarsingle-1](https://docs.alpaca.markets/reference/stocklatestbarsingle-1) |
| GET | /v2/stocks/{symbol}/quotes | Historical quotes (single symbol) | [stockquotesingle-1](historical_api_reference/reference/stockquotesingle-1.md) | [stockquotesingle-1](https://docs.alpaca.markets/reference/stockquotesingle-1) |
| GET | /v2/stocks/{symbol}/quotes/latest | Latest quote (single symbol) | [stocklatestquotesingle-1](historical_api_reference/reference/stocklatestquotesingle-1.md) | [stocklatestquotesingle-1](https://docs.alpaca.markets/reference/stocklatestquotesingle-1) |
| GET | /v2/stocks/{symbol}/snapshot | Snapshot (single symbol) | [stocksnapshotsingle](historical_api_reference/reference/stocksnapshotsingle.md) | [stocksnapshotsingle](https://docs.alpaca.markets/reference/stocksnapshotsingle) |
| GET | /v2/stocks/{symbol}/trades | Historical trades (single symbol) | [stocktradesingle-1](historical_api_reference/reference/stocktradesingle-1.md) | [stocktradesingle-1](https://docs.alpaca.markets/reference/stocktradesingle-1) |
| GET | /v2/stocks/{symbol}/trades/latest | Latest trade (single symbol) | [stocklatesttradesingle-1](historical_api_reference/reference/stocklatesttradesingle-1.md) | [stocklatesttradesingle-1](https://docs.alpaca.markets/reference/stocklatesttradesingle-1) |
