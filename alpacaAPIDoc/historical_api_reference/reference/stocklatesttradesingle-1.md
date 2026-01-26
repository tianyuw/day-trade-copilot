---
source_view: https://docs.alpaca.markets/reference/stocklatesttradesingle-1
source_md: https://docs.alpaca.markets/reference/stocklatesttradesingle-1.md
scraped_at_utc: 2026-01-26T01:04:10Z
---
# Latest trade (single symbol)

The latest trade endpoint provides the latest trade for the given ticker symbol.

Trades with any conditions that causes them to not update the bar price are excluded. For example a trade with condition `I` (odd lot) will never appear on this endpoint. You can find the complete list of excluded conditions in [this FAQ](https://docs.alpaca.markets/docs/market-data-faq#how-are-bars-aggregated).

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
    "/v2/stocks/{symbol}/trades/latest": {
      "get": {
        "summary": "Latest trade (single symbol)",
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
                  "type": "object",
                  "properties": {
                    "trade": {
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
                    "symbol": {
                      "type": "string"
                    },
                    "currency": {
                      "type": "string"
                    }
                  },
                  "required": [
                    "trade",
                    "symbol"
                  ],
                  "x-readme-ref-name": "stock_latest_trades_resp_single"
                },
                "examples": {
                  "trade": {
                    "value": {
                      "symbol": "AAPL",
                      "trade": {
                        "t": "2022-08-17T09:53:16.845580544Z",
                        "x": "P",
                        "p": 172.6,
                        "s": 100,
                        "c": [
                          "@",
                          "T"
                        ],
                        "i": 689,
                        "z": "C"
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
        "operationId": "StockLatestTradeSingle",
        "description": "The latest trade endpoint provides the latest trade for the given ticker symbol.\n\nTrades with any conditions that causes them to not update the bar price are excluded. For example a trade with condition `I` (odd lot) will never appear on this endpoint. You can find the complete list of excluded conditions in [this FAQ](https://docs.alpaca.markets/docs/market-data-faq#how-are-bars-aggregated)."
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
