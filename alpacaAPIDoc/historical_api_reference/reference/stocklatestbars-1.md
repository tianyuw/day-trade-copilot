---
source_view: https://docs.alpaca.markets/reference/stocklatestbars-1
source_md: https://docs.alpaca.markets/reference/stocklatestbars-1.md
scraped_at_utc: 2026-01-26T01:04:10Z
---
# Latest bars

The latest bars endpoint provides the latest minute bar for the given ticker symbols.


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
    "/v2/stocks/bars/latest": {
      "get": {
        "summary": "Latest bars",
        "tags": [
          "Stock"
        ],
        "parameters": [
          {
            "name": "symbols",
            "description": "A comma-separated list of stock symbols.",
            "in": "query",
            "required": true,
            "schema": {
              "type": "string"
            },
            "example": "AAPL,TSLA"
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
                    "bars": {
                      "type": "object",
                      "additionalProperties": {
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
                    "currency": {
                      "type": "string"
                    }
                  },
                  "required": [
                    "bars"
                  ],
                  "x-readme-ref-name": "stock_latest_bars_resp"
                },
                "examples": {
                  "bars": {
                    "value": {
                      "bars": {
                        "TSLA": {
                          "t": "2022-08-17T08:57:00Z",
                          "o": 914.3,
                          "h": 914.3,
                          "l": 914.3,
                          "c": 914.3,
                          "v": 751,
                          "n": 20,
                          "vw": 914.294634
                        },
                        "AAPL": {
                          "t": "2022-08-17T08:58:00Z",
                          "o": 172.81,
                          "h": 172.81,
                          "l": 172.78,
                          "c": 172.79,
                          "v": 1002,
                          "n": 20,
                          "vw": 172.791417
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
        "operationId": "StockLatestBars",
        "description": "The latest bars endpoint provides the latest minute bar for the given ticker symbols.\n"
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
