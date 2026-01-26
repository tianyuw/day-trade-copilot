---
source_view: https://docs.alpaca.markets/reference/cryptolatestbars-1
source_md: https://docs.alpaca.markets/reference/cryptolatestbars-1.md
scraped_at_utc: 2026-01-26T01:04:10Z
---
# Latest bars

The latest multi-bars endpoint returns the latest minute-aggregated historical bar data for each of the crypto symbols provided.


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
    "/v1beta3/crypto/{loc}/latest/bars": {
      "get": {
        "summary": "Latest bars",
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
                    "bars": {
                      "type": "object",
                      "additionalProperties": {
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
                    }
                  },
                  "required": [
                    "bars"
                  ],
                  "x-readme-ref-name": "crypto_latest_bars_resp"
                },
                "examples": {
                  "bars": {
                    "value": {
                      "bars": {
                        "BTC/USD": {
                          "t": "2022-05-27T10:18:00Z",
                          "o": 28999,
                          "h": 29003,
                          "l": 28999,
                          "c": 29003,
                          "v": 0.01,
                          "n": 4,
                          "vw": 29001
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
        "operationId": "CryptoLatestBars",
        "description": "The latest multi-bars endpoint returns the latest minute-aggregated historical bar data for each of the crypto symbols provided.\n"
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
