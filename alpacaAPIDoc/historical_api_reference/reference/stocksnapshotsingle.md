---
source_view: https://docs.alpaca.markets/reference/stocksnapshotsingle
source_md: https://docs.alpaca.markets/reference/stocksnapshotsingle.md
scraped_at_utc: 2026-01-26T01:04:10Z
---
# Snapshot (single symbol)

The snapshot endpoint provides the latest trade, latest quote, minute bar, daily bar, and previous daily bar data for a given ticker symbol.


# OpenAPI definition

```json
{
  "openapi": "3.0.0",
  "info": {
    "title": "Market Data API",
    "description": "Access real-time and historical market data for US equities, options, crypto, and foreign exchange data through the Alpaca REST and WebSocket APIs. There are APIs for Stock Pricing, Option Pricing, Crypto Pricing, Forex, Logos, Fixed income, Corporate Actions, Screener, and News.\n",
    "version": "1.1",
    "contact": {
      "name": "Alpaca Support",
      "email": "support@alpaca.markets",
      "url": "https://alpaca.markets/support"
    },
    "termsOfService": "https://s3.amazonaws.com/files.alpaca.markets/disclosures/library/TermsAndConditions.pdf",
    "license": {
      "name": "Creative Commons Attribution Share Alike 4.0 International",
      "url": "https://spdx.org/licenses/CC-BY-SA-4.0.html"
    }
  },
  "servers": [
    {
      "description": "Production",
      "url": "https://data.alpaca.markets"
    },
    {
      "description": "Sandbox",
      "url": "https://data.sandbox.alpaca.markets"
    }
  ],
  "security": [
    {
      "apiKey": [],
      "apiSecret": []
    }
  ],
  "tags": [
    {
      "name": "Stock",
      "description": "Endpoints for stocks."
    }
  ],
  "paths": {
    "/v2/stocks/{symbol}/snapshot": {
      "get": {
        "summary": "Snapshot (single symbol)",
        "tags": [
          "Stock"
        ],
        "parameters": [
          {
            "name": "symbol",
            "in": "path",
            "description": "The symbol to query.",
            "required": true,
            "schema": {
              "type": "string"
            },
            "example": "AAPL"
          },
          {
            "name": "feed",
            "in": "query",
            "description": "The source feed of the data.\n\n - `sip`: all US exchanges\n - `iex`: Investors EXchange\n - `delayed_sip`: SIP with a 15 minute delay\n - `boats`: Blue Ocean, overnight US trading data\n - `overnight`: derived overnight US trading data\n - `otc`: over-the-counter exchanges\n\nDefault: `sip` if the user has the unlimited subscription, otherwise `iex`.\n",
            "schema": {
              "type": "string",
              "enum": [
                "delayed_sip",
                "iex",
                "otc",
                "sip",
                "boats",
                "overnight"
              ],
              "x-readme-ref-name": "stock_latest_feed"
            }
          },
          {
            "name": "currency",
            "in": "query",
            "description": "The currency of all prices in ISO 4217 format. Default: USD.\n",
            "schema": {
              "type": "string"
            }
          }
        ],
        "responses": {
          "200": {
            "description": "OK",
            "headers": {
              "X-RateLimit-Limit": {
                "schema": {
                  "type": "integer"
                },
                "example": 100,
                "description": "Request limit per minute."
              },
              "X-RateLimit-Remaining": {
                "schema": {
                  "type": "integer"
                },
                "example": 90,
                "description": "Request limit per minute remaining."
              },
              "X-RateLimit-Reset": {
                "schema": {
                  "type": "integer"
                },
                "example": 1674044551,
                "description": "The UNIX epoch when the remaining quota changes."
              }
            },
            "content": {
              "application/json": {
                "schema": {
                  "allOf": [
                    {
                      "type": "object",
                      "properties": {
                        "symbol": {
                          "type": "string"
                        },
                        "currency": {
                          "type": "string"
                        }
                      }
                    },
                    {
                      "type": "object",
                      "description": "A snapshot provides the latest trade, latest quote, latest minute bar, current daily bar and previous daily bar.\n",
                      "properties": {
                        "dailyBar": {
                          "type": "object",
                          "description": "OHLC aggregate of all the trades in a given interval.\n",
                          "example": {
                            "t": "2022-01-03T09:00:00Z",
                            "o": 178.26,
                            "h": 178.34,
                            "l": 177.76,
                            "c": 178.08,
                            "v": 60937,
                            "n": 1727,
                            "vw": 177.954244
                          },
                          "properties": {
                            "t": {
                              "type": "string",
                              "description": "Timestamp in RFC-3339 format with nanosecond precision.",
                              "format": "date-time",
                              "x-go-name": "Timestamp",
                              "x-readme-ref-name": "timestamp"
                            },
                            "o": {
                              "type": "number",
                              "format": "double",
                              "description": "Opening price.",
                              "x-go-name": "Open"
                            },
                            "h": {
                              "type": "number",
                              "format": "double",
                              "description": "High price.",
                              "x-go-name": "High"
                            },
                            "l": {
                              "type": "number",
                              "format": "double",
                              "description": "Low price.",
                              "x-go-name": "Low"
                            },
                            "c": {
                              "type": "number",
                              "format": "double",
                              "description": "Closing price.",
                              "x-go-name": "Close"
                            },
                            "v": {
                              "type": "integer",
                              "format": "int64",
                              "description": "Bar volume.",
                              "x-go-name": "Volume"
                            },
                            "n": {
                              "type": "integer",
                              "format": "int64",
                              "description": "Trade count in the bar.",
                              "x-go-name": "TradeCount"
                            },
                            "vw": {
                              "type": "number",
                              "format": "double",
                              "description": "Volume weighted average price.",
                              "x-go-name": "VWAP"
                            }
                          },
                          "required": [
                            "t",
                            "o",
                            "h",
                            "l",
                            "c",
                            "v",
                            "n",
                            "vw"
                          ],
                          "x-readme-ref-name": "stock_bar"
                        },
                        "latestQuote": {
                          "type": "object",
                          "description": "The best bid and ask information for a given security.",
                          "example": {
                            "t": "2021-02-06T13:35:08.946977536Z",
                            "ax": "C",
                            "ap": 387.7,
                            "as": 1,
                            "bx": "N",
                            "bp": 387.67,
                            "bs": 1,
                            "c": [
                              "R"
                            ],
                            "z": "C"
                          },
                          "properties": {
                            "t": {
                              "type": "string",
                              "description": "Timestamp in RFC-3339 format with nanosecond precision.",
                              "format": "date-time",
                              "x-go-name": "Timestamp",
                              "x-readme-ref-name": "timestamp"
                            },
                            "bx": {
                              "type": "string",
                              "description": "Bid exchange. See `v2/stocks/meta/exchanges` for more details.",
                              "x-go-name": "BidExchange"
                            },
                            "bp": {
                              "type": "number",
                              "format": "double",
                              "description": "Bid price. 0 means the security has no active bid.",
                              "x-go-name": "BidPrice"
                            },
                            "bs": {
                              "type": "integer",
                              "format": "uint32",
                              "description": "Bid size in shares (round lots prior to November 3, 2025).",
                              "x-go-name": "BidSize"
                            },
                            "ax": {
                              "type": "string",
                              "description": "Ask exchange. See `v2/stocks/meta/exchanges` for more details.",
                              "x-go-name": "AskExchange"
                            },
                            "ap": {
                              "type": "number",
                              "format": "double",
                              "description": "Ask price. 0 means the security has no active ask.",
                              "x-go-name": "AskPrice"
                            },
                            "as": {
                              "type": "integer",
                              "format": "uint32",
                              "description": "Ask size in shares (round lots prior to November 3, 2025).",
                              "x-go-name": "AskSize"
                            },
                            "c": {
                              "description": "Condition flags. See `v2/stocks/meta/conditions/quote` for more details. If the array contains one flag, it applies to both the bid and ask. If the array contains two flags, the first one applies to the bid and the second one to the ask.\n",
                              "type": "array",
                              "items": {
                                "type": "string"
                              },
                              "x-go-name": "Conditions"
                            },
                            "z": {
                              "type": "string",
                              "description": "- A: New York Stock Exchange\n- B: NYSE Arca, Bats, IEX and other regional exchanges\n- C: NASDAQ\n- N: Overnight\n- O: OTC\n",
                              "x-go-name": "Tape",
                              "enum": [
                                "A",
                                "B",
                                "C",
                                "N",
                                "O"
                              ],
                              "x-readme-ref-name": "stock_tape"
                            }
                          },
                          "required": [
                            "t",
                            "bx",
                            "bp",
                            "bs",
                            "ap",
                            "as",
                            "ax",
                            "c",
                            "z"
                          ],
                          "x-readme-ref-name": "stock_quote"
                        },
                        "latestTrade": {
                          "type": "object",
                          "description": "A stock trade.",
                          "example": {
                            "t": "2022-01-03T09:00:00.086175744Z",
                            "x": "P",
                            "p": 178.26,
                            "s": 246,
                            "c": [
                              "@",
                              "T"
                            ],
                            "i": 1,
                            "z": "C"
                          },
                          "properties": {
                            "t": {
                              "type": "string",
                              "description": "Timestamp in RFC-3339 format with nanosecond precision.",
                              "format": "date-time",
                              "x-go-name": "Timestamp",
                              "x-readme-ref-name": "timestamp"
                            },
                            "x": {
                              "type": "string",
                              "description": "Exchange code. See `v2/stocks/meta/exchanges` for more details.",
                              "x-go-name": "Exchange"
                            },
                            "p": {
                              "type": "number",
                              "format": "double",
                              "description": "Trade price.",
                              "x-go-name": "Price"
                            },
                            "s": {
                              "type": "integer",
                              "format": "uint32",
                              "description": "Trade size.",
                              "x-go-name": "Size"
                            },
                            "i": {
                              "type": "integer",
                              "format": "uint64",
                              "description": "Trade ID sent by the exchange.",
                              "x-go-name": "ID"
                            },
                            "c": {
                              "description": "Condition flags. See `v2/stocks/meta/conditions/trade` for more details.",
                              "type": "array",
                              "items": {
                                "type": "string"
                              },
                              "x-go-name": "Conditions"
                            },
                            "z": {
                              "type": "string",
                              "description": "- A: New York Stock Exchange\n- B: NYSE Arca, Bats, IEX and other regional exchanges\n- C: NASDAQ\n- N: Overnight\n- O: OTC\n",
                              "x-go-name": "Tape",
                              "enum": [
                                "A",
                                "B",
                                "C",
                                "N",
                                "O"
                              ],
                              "x-readme-ref-name": "stock_tape"
                            },
                            "u": {
                              "type": "string",
                              "x-go-name": "Update",
                              "description": "Update to the trade. This field is optional, if it's missing, the trade is valid. Otherwise, it can have these values:\n - canceled: indicates that the trade has been canceled\n - incorrect: indicates that the trade has been corrected and the given trade is no longer valid\n - corrected: indicates that this trade is the correction of a previous (incorrect) trade\n"
                            }
                          },
                          "required": [
                            "t",
                            "i",
                            "x",
                            "p",
                            "s",
                            "c",
                            "z"
                          ],
                          "x-readme-ref-name": "stock_trade"
                        },
                        "minuteBar": {
                          "type": "object",
                          "description": "OHLC aggregate of all the trades in a given interval.\n",
                          "example": {
                            "t": "2022-01-03T09:00:00Z",
                            "o": 178.26,
                            "h": 178.34,
                            "l": 177.76,
                            "c": 178.08,
                            "v": 60937,
                            "n": 1727,
                            "vw": 177.954244
                          },
                          "properties": {
                            "t": {
                              "type": "string",
                              "description": "Timestamp in RFC-3339 format with nanosecond precision.",
                              "format": "date-time",
                              "x-go-name": "Timestamp",
                              "x-readme-ref-name": "timestamp"
                            },
                            "o": {
                              "type": "number",
                              "format": "double",
                              "description": "Opening price.",
                              "x-go-name": "Open"
                            },
                            "h": {
                              "type": "number",
                              "format": "double",
                              "description": "High price.",
                              "x-go-name": "High"
                            },
                            "l": {
                              "type": "number",
                              "format": "double",
                              "description": "Low price.",
                              "x-go-name": "Low"
                            },
                            "c": {
                              "type": "number",
                              "format": "double",
                              "description": "Closing price.",
                              "x-go-name": "Close"
                            },
                            "v": {
                              "type": "integer",
                              "format": "int64",
                              "description": "Bar volume.",
                              "x-go-name": "Volume"
                            },
                            "n": {
                              "type": "integer",
                              "format": "int64",
                              "description": "Trade count in the bar.",
                              "x-go-name": "TradeCount"
                            },
                            "vw": {
                              "type": "number",
                              "format": "double",
                              "description": "Volume weighted average price.",
                              "x-go-name": "VWAP"
                            }
                          },
                          "required": [
                            "t",
                            "o",
                            "h",
                            "l",
                            "c",
                            "v",
                            "n",
                            "vw"
                          ],
                          "x-readme-ref-name": "stock_bar"
                        },
                        "prevDailyBar": {
                          "type": "object",
                          "description": "OHLC aggregate of all the trades in a given interval.\n",
                          "example": {
                            "t": "2022-01-03T09:00:00Z",
                            "o": 178.26,
                            "h": 178.34,
                            "l": 177.76,
                            "c": 178.08,
                            "v": 60937,
                            "n": 1727,
                            "vw": 177.954244
                          },
                          "properties": {
                            "t": {
                              "type": "string",
                              "description": "Timestamp in RFC-3339 format with nanosecond precision.",
                              "format": "date-time",
                              "x-go-name": "Timestamp",
                              "x-readme-ref-name": "timestamp"
                            },
                            "o": {
                              "type": "number",
                              "format": "double",
                              "description": "Opening price.",
                              "x-go-name": "Open"
                            },
                            "h": {
                              "type": "number",
                              "format": "double",
                              "description": "High price.",
                              "x-go-name": "High"
                            },
                            "l": {
                              "type": "number",
                              "format": "double",
                              "description": "Low price.",
                              "x-go-name": "Low"
                            },
                            "c": {
                              "type": "number",
                              "format": "double",
                              "description": "Closing price.",
                              "x-go-name": "Close"
                            },
                            "v": {
                              "type": "integer",
                              "format": "int64",
                              "description": "Bar volume.",
                              "x-go-name": "Volume"
                            },
                            "n": {
                              "type": "integer",
                              "format": "int64",
                              "description": "Trade count in the bar.",
                              "x-go-name": "TradeCount"
                            },
                            "vw": {
                              "type": "number",
                              "format": "double",
                              "description": "Volume weighted average price.",
                              "x-go-name": "VWAP"
                            }
                          },
                          "required": [
                            "t",
                            "o",
                            "h",
                            "l",
                            "c",
                            "v",
                            "n",
                            "vw"
                          ],
                          "x-readme-ref-name": "stock_bar"
                        }
                      },
                      "x-readme-ref-name": "stock_snapshot"
                    }
                  ],
                  "x-readme-ref-name": "stock_snapshots_resp_single"
                },
                "examples": {
                  "snapshot": {
                    "value": {
                      "symbol": "AAPL",
                      "latestTrade": {
                        "t": "2022-08-17T10:19:30.735811394Z",
                        "x": "Q",
                        "p": 172.55,
                        "s": 229,
                        "c": [
                          "@",
                          "T"
                        ],
                        "i": 1040,
                        "z": "C"
                      },
                      "latestQuote": {
                        "t": "2022-08-17T10:19:30.805564086Z",
                        "ax": "Q",
                        "ap": 172.65,
                        "as": 1,
                        "bx": "P",
                        "bp": 172.51,
                        "bs": 1,
                        "c": [
                          "R"
                        ],
                        "z": "C"
                      },
                      "minuteBar": {
                        "t": "2022-08-17T10:18:00Z",
                        "o": 172.65,
                        "h": 172.65,
                        "l": 172.6,
                        "c": 172.6,
                        "v": 3746,
                        "n": 57,
                        "vw": 172.618377
                      },
                      "dailyBar": {
                        "t": "2022-08-16T04:00:00Z",
                        "o": 172.62,
                        "h": 173.71,
                        "l": 171.6618,
                        "c": 173.03,
                        "v": 56457696,
                        "n": 515139,
                        "vw": 172.743391
                      },
                      "prevDailyBar": {
                        "t": "2022-08-15T04:00:00Z",
                        "o": 171.5,
                        "h": 173.39,
                        "l": 171.345,
                        "c": 173.19,
                        "v": 54091719,
                        "n": 501626,
                        "vw": 172.625371
                      }
                    }
                  }
                }
              }
            }
          },
          "400": {
            "description": "One of the request parameters is invalid. See the returned message for details.\n",
            "headers": {
              "X-RateLimit-Limit": {
                "schema": {
                  "type": "integer"
                },
                "example": 100,
                "description": "Request limit per minute."
              },
              "X-RateLimit-Remaining": {
                "schema": {
                  "type": "integer"
                },
                "example": 90,
                "description": "Request limit per minute remaining."
              },
              "X-RateLimit-Reset": {
                "schema": {
                  "type": "integer"
                },
                "example": 1674044551,
                "description": "The UNIX epoch when the remaining quota changes."
              }
            }
          },
          "401": {
            "description": "Authentication headers are missing or invalid. Make sure you authenticate your request with a valid API key.\n"
          },
          "403": {
            "description": "The requested resource is forbidden.\n"
          },
          "429": {
            "description": "Too many requests. You hit the rate limit. Use the X-RateLimit-... response headers to make sure you're under the rate limit.\n",
            "headers": {
              "X-RateLimit-Limit": {
                "schema": {
                  "type": "integer"
                },
                "example": 100,
                "description": "Request limit per minute."
              },
              "X-RateLimit-Remaining": {
                "schema": {
                  "type": "integer"
                },
                "example": 90,
                "description": "Request limit per minute remaining."
              },
              "X-RateLimit-Reset": {
                "schema": {
                  "type": "integer"
                },
                "example": 1674044551,
                "description": "The UNIX epoch when the remaining quota changes."
              }
            }
          },
          "500": {
            "description": "Internal server error. We recommend retrying these later. If the issue persists, please contact us on [Slack](https://alpaca.markets/slack) or on the [Community Forum](https://forum.alpaca.markets/).\n"
          }
        },
        "operationId": "StockSnapshotSingle",
        "description": "The snapshot endpoint provides the latest trade, latest quote, minute bar, daily bar, and previous daily bar data for a given ticker symbol.\n"
      }
    }
  },
  "components": {
    "securitySchemes": {
      "apiKey": {
        "type": "apiKey",
        "in": "header",
        "name": "APCA-API-KEY-ID"
      },
      "apiSecret": {
        "type": "apiKey",
        "in": "header",
        "name": "APCA-API-SECRET-KEY"
      }
    }
  }
}
```
