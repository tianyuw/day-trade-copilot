---
source_view: https://docs.alpaca.markets/reference/optionlatesttrades
source_md: https://docs.alpaca.markets/reference/optionlatesttrades.md
scraped_at_utc: 2026-01-26T01:04:10Z
---
# Latest trades

The latest multi-trades endpoint provides the latest historical trade data for multiple given contract symbols.


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
      "name": "Option",
      "description": "Endpoints for option data."
    }
  ],
  "paths": {
    "/v1beta1/options/trades/latest": {
      "get": {
        "summary": "Latest trades",
        "tags": [
          "Option"
        ],
        "parameters": [
          {
            "name": "symbols",
            "description": "A comma-separated list of contract symbols with a limit of 100.",
            "in": "query",
            "required": true,
            "schema": {
              "type": "string"
            },
            "example": "AAPL241220C00300000,AAPL240315C00225000"
          },
          {
            "name": "feed",
            "in": "query",
            "description": "The source feed of the data. `opra` is the official OPRA feed, `indicative` is a free indicative feed where trades are delayed and quotes are modified. Default: `opra` if the user has a subscription, otherwise `indicative`.\n",
            "schema": {
              "type": "string",
              "enum": [
                "opra",
                "indicative"
              ],
              "default": "opra",
              "x-readme-ref-name": "option_feed"
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
                    "trades": {
                      "type": "object",
                      "additionalProperties": {
                        "type": "object",
                        "description": "An option trade.",
                        "example": {
                          "t": "2024-01-18T15:03:44.56339456Z",
                          "x": "B",
                          "p": 0.37,
                          "s": 1,
                          "c": "I"
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
                          "c": {
                            "type": "string",
                            "description": "Trade condition.",
                            "x-go-name": "Condition"
                          }
                        },
                        "required": [
                          "t",
                          "x",
                          "p",
                          "s",
                          "c"
                        ],
                        "x-readme-ref-name": "option_trade"
                      }
                    }
                  },
                  "required": [
                    "trades"
                  ],
                  "x-readme-ref-name": "option_latest_trades_resp"
                },
                "examples": {
                  "trades": {
                    "value": {
                      "trades": {
                        "AAPL250321C00190000": {
                          "t": "2024-02-28T15:26:12.728701696Z",
                          "x": "B",
                          "p": 17.15,
                          "s": 900,
                          "c": "e"
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
        "operationId": "OptionLatestTrades",
        "description": "The latest multi-trades endpoint provides the latest historical trade data for multiple given contract symbols.\n"
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
