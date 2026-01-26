---
source_view: https://docs.alpaca.markets/reference/latestrates-1
source_md: https://docs.alpaca.markets/reference/latestrates-1.md
scraped_at_utc: 2026-01-26T01:04:10Z
---
# Latest rates for currency pairs

Get the latest forex rates for the given currency pairs.


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
      "name": "Forex",
      "description": "Endpoints for forex currency rates."
    }
  ],
  "paths": {
    "/v1beta1/forex/latest/rates": {
      "get": {
        "summary": "Latest rates for currency pairs",
        "tags": [
          "Forex"
        ],
        "parameters": [
          {
            "name": "currency_pairs",
            "in": "query",
            "required": true,
            "schema": {
              "type": "string",
              "description": "A comma-separated string with currency pairs.",
              "example": "USDJPY,USDMXN",
              "x-go-name": "TypeCurrencyPairs",
              "x-readme-ref-name": "forex_currency_pairs"
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
                  "description": "The response object of the latest forex rates.",
                  "type": "object",
                  "properties": {
                    "rates": {
                      "type": "object",
                      "additionalProperties": {
                        "description": "A foreign exchange rate between two currencies at a given time.",
                        "type": "object",
                        "example": {
                          "bp": 127.702,
                          "mp": 127.757,
                          "ap": 127.763,
                          "t": "2022-04-20T18:23:00Z"
                        },
                        "properties": {
                          "bp": {
                            "type": "number",
                            "format": "double",
                            "x-go-name": "BidPrice",
                            "description": "The last bid price value of the currency at the end of the timeframe."
                          },
                          "mp": {
                            "type": "number",
                            "format": "double",
                            "x-go-name": "MidPrice",
                            "description": "The last mid price value of the currency at the end of the timeframe."
                          },
                          "ap": {
                            "type": "number",
                            "format": "double",
                            "x-go-name": "AskPrice",
                            "description": "The last ask price value of the currency at the end of the timeframe."
                          },
                          "t": {
                            "type": "string",
                            "format": "date-time",
                            "x-go-name": "Timestamp",
                            "description": "Timestamp of the rate."
                          }
                        },
                        "required": [
                          "bp",
                          "mp",
                          "ap",
                          "t"
                        ],
                        "x-readme-ref-name": "forex_rate"
                      }
                    }
                  },
                  "required": [
                    "rates"
                  ],
                  "x-readme-ref-name": "forex_latest_rates_resp"
                },
                "examples": {
                  "USDJPY": {
                    "value": {
                      "rates": {
                        "USDJPY": {
                          "bp": 127.752,
                          "mp": 127.779,
                          "ap": 128.112,
                          "t": "2022-05-20T05:38:41.311530885Z"
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
        "operationId": "LatestRates",
        "description": "Get the latest forex rates for the given currency pairs.\n"
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
