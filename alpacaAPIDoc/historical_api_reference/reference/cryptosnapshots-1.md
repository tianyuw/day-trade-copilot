---
source_view: https://docs.alpaca.markets/reference/cryptosnapshots-1
source_md: https://docs.alpaca.markets/reference/cryptosnapshots-1.md
scraped_at_utc: 2026-01-26T01:04:10Z
---
# Snapshots

The snapshots endpoint returns the latest trade, latest quote, latest minute bar, latest daily bar, and previous daily bar data for crypto symbols.


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
      "name": "Crypto",
      "description": "Endpoints for cryptocurrencies."
    }
  ],
  "paths": {
    "/v1beta3/crypto/{loc}/snapshots": {
      "get": {
        "summary": "Snapshots",
        "tags": [
          "Crypto"
        ],
        "security": [],
        "parameters": [
          {
            "name": "loc",
            "in": "path",
            "description": "Crypto location from where the latest market data is retrieved.\n- `us`: Alpaca US\n- `us-1`: Kraken US\n- `eu-1`: Kraken EU\n",
            "required": true,
            "schema": {
              "type": "string",
              "enum": [
                "us",
                "us-1",
                "eu-1"
              ],
              "description": "Crypto location from where the latest market data is retrieved.",
              "x-go-name": "TypeLatestLoc",
              "x-readme-ref-name": "crypto_latest_loc"
            }
          },
          {
            "name": "symbols",
            "description": "A comma-separated list of crypto symbols.",
            "in": "query",
            "required": true,
            "schema": {
              "type": "string"
            },
            "example": "BTC/USD,LTC/USD"
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
                  "type": "object",
                  "properties": {
                    "snapshots": {
                      "type": "object",
                      "additionalProperties": {
                        "type": "object",
                        "description": "A snapshot provides the latest trade, latest quote, latest minute bar, latest daily bar and previous daily bar.\n",
                        "properties": {
                          "dailyBar": {
                            "type": "object",
                            "description": "OHLC aggregate of all the trades in a given interval.",
                            "example": {
                              "t": "2022-05-27T10:18:00Z",
                              "o": 28999,
                              "h": 29003,
                              "l": 28999,
                              "c": 29003,
                              "v": 0.01,
                              "n": 4,
                              "vw": 29001
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
                                "type": "number",
                                "format": "double",
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
                            "x-readme-ref-name": "crypto_bar"
                          },
                          "latestQuote": {
                            "type": "object",
                            "description": "The best bid and ask information for a given security.",
                            "example": {
                              "t": "2022-05-26T11:47:18.44347136Z",
                              "bp": 29058,
                              "bs": 0.3544,
                              "ap": 29059,
                              "as": 3.252
                            },
                            "properties": {
                              "t": {
                                "type": "string",
                                "description": "Timestamp in RFC-3339 format with nanosecond precision.",
                                "format": "date-time",
                                "x-go-name": "Timestamp",
                                "x-readme-ref-name": "timestamp"
                              },
                              "bp": {
                                "type": "number",
                                "format": "double",
                                "description": "Bid price.",
                                "x-go-name": "BidPrice"
                              },
                              "bs": {
                                "type": "number",
                                "format": "double",
                                "description": "Bid size.",
                                "x-go-name": "BidSize"
                              },
                              "ap": {
                                "type": "number",
                                "format": "double",
                                "description": "Ask price.",
                                "x-go-name": "AskPrice"
                              },
                              "as": {
                                "type": "number",
                                "format": "double",
                                "description": "Ask size.",
                                "x-go-name": "AskSize"
                              }
                            },
                            "required": [
                              "t",
                              "bp",
                              "bs",
                              "ap",
                              "as"
                            ],
                            "x-readme-ref-name": "crypto_quote"
                          },
                          "latestTrade": {
                            "type": "object",
                            "description": "A crypto trade.",
                            "example": {
                              "t": "2022-05-18T12:00:05.225055Z",
                              "p": 29798,
                              "s": 0.1209,
                              "tks": "S",
                              "i": 31455277
                            },
                            "properties": {
                              "t": {
                                "type": "string",
                                "description": "Timestamp in RFC-3339 format with nanosecond precision.",
                                "format": "date-time",
                                "x-go-name": "Timestamp",
                                "x-readme-ref-name": "timestamp"
                              },
                              "p": {
                                "type": "number",
                                "format": "double",
                                "description": "Trade price.",
                                "x-go-name": "Price"
                              },
                              "s": {
                                "type": "number",
                                "format": "double",
                                "description": "Trade size.",
                                "x-go-name": "Size"
                              },
                              "i": {
                                "type": "integer",
                                "format": "int64",
                                "description": "Trade ID.",
                                "x-go-name": "ID"
                              },
                              "tks": {
                                "type": "string",
                                "description": "Taker side: B for buyer, S for seller\n",
                                "x-go-name": "TakerSide"
                              }
                            },
                            "required": [
                              "t",
                              "p",
                              "s",
                              "i",
                              "tks"
                            ],
                            "x-readme-ref-name": "crypto_trade"
                          },
                          "minuteBar": {
                            "type": "object",
                            "description": "OHLC aggregate of all the trades in a given interval.",
                            "example": {
                              "t": "2022-05-27T10:18:00Z",
                              "o": 28999,
                              "h": 29003,
                              "l": 28999,
                              "c": 29003,
                              "v": 0.01,
                              "n": 4,
                              "vw": 29001
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
                                "type": "number",
                                "format": "double",
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
                            "x-readme-ref-name": "crypto_bar"
                          },
                          "prevDailyBar": {
                            "type": "object",
                            "description": "OHLC aggregate of all the trades in a given interval.",
                            "example": {
                              "t": "2022-05-27T10:18:00Z",
                              "o": 28999,
                              "h": 29003,
                              "l": 28999,
                              "c": 29003,
                              "v": 0.01,
                              "n": 4,
                              "vw": 29001
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
                                "type": "number",
                                "format": "double",
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
                            "x-readme-ref-name": "crypto_bar"
                          }
                        },
                        "x-readme-ref-name": "crypto_snapshot"
                      }
                    }
                  },
                  "required": [
                    "snapshots"
                  ],
                  "x-readme-ref-name": "crypto_snapshots_resp"
                },
                "examples": {
                  "snapshots": {
                    "value": {
                      "snapshots": {
                        "BTC/USD": {
                          "dailyBar": {
                            "c": 31744,
                            "h": 31807,
                            "l": 31416,
                            "n": 438,
                            "o": 31660,
                            "t": "2022-05-31T05:00:00Z",
                            "v": 67.3518,
                            "vw": 31582.7034526175
                          },
                          "latestQuote": {
                            "ap": 31742,
                            "as": 0.395,
                            "bp": 31741,
                            "bs": 0.395,
                            "t": "2022-05-31T11:55:58.507608832Z"
                          },
                          "latestTrade": {
                            "i": 32396097,
                            "p": 31744,
                            "s": 0.0543,
                            "t": "2022-05-31T11:53:45.027481Z",
                            "tks": "B"
                          },
                          "minuteBar": {
                            "c": 31744,
                            "h": 31744,
                            "l": 31744,
                            "n": 2,
                            "o": 31744,
                            "t": "2022-05-31T11:53:00Z",
                            "v": 0.0886,
                            "vw": 31744
                          },
                          "prevDailyBar": {
                            "c": 31649,
                            "h": 32251,
                            "l": 30251,
                            "n": 8221,
                            "o": 30310,
                            "t": "2022-05-30T05:00:00Z",
                            "v": 1856.4065,
                            "vw": 30877.2751897281
                          }
                        }
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
        "operationId": "CryptoSnapshots",
        "description": "The snapshots endpoint returns the latest trade, latest quote, latest minute bar, latest daily bar, and previous daily bar data for crypto symbols.\n"
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
