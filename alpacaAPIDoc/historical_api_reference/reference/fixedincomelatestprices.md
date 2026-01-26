---
source_view: https://docs.alpaca.markets/reference/fixedincomelatestprices
source_md: https://docs.alpaca.markets/reference/fixedincomelatestprices.md
scraped_at_utc: 2026-01-26T01:04:10Z
---
# Latest prices

This endpoint returns the latest prices for the given fixed income securities.


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
      "name": "Fixed income",
      "description": "Endpoints for fixed income data."
    }
  ],
  "paths": {
    "/v1beta1/fixed_income/latest/prices": {
      "get": {
        "summary": "Latest prices",
        "tags": [
          "Fixed income"
        ],
        "parameters": [
          {
            "name": "isins",
            "description": "A comma-separated list of ISINs with a limit of 1000.",
            "in": "query",
            "required": true,
            "schema": {
              "type": "string"
            },
            "example": "US912797KJ59,US912797KS58,US912797LB15"
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
                    "prices": {
                      "type": "object",
                      "additionalProperties": {
                        "type": "object",
                        "description": "The price of the instrument as a percentage of its par value.",
                        "example": {
                          "t": "2025-02-14T20:58:00.648Z",
                          "p": 99.6459,
                          "ytm": 4.249,
                          "ytw": 4.249
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
                            "description": "Price",
                            "x-go-name": "Price"
                          },
                          "ytm": {
                            "type": "number",
                            "format": "double",
                            "description": "Yield to maturity.",
                            "x-go-name": "YieldToMaturity"
                          },
                          "ytw": {
                            "type": "number",
                            "format": "double",
                            "description": "Yield to worst.",
                            "x-go-name": "YieldToWorst"
                          }
                        },
                        "required": [
                          "t",
                          "p"
                        ],
                        "x-readme-ref-name": "fixed_income_price"
                      }
                    }
                  },
                  "required": [
                    "prices"
                  ],
                  "x-readme-ref-name": "fixed_income_latest_prices_resp"
                },
                "examples": {
                  "prices": {
                    "value": {
                      "prices": {
                        "US912797KJ59": {
                          "t": "2025-02-14T20:58:00.648Z",
                          "p": 99.6459,
                          "ytm": 4.249,
                          "ytw": 4.249
                        },
                        "US912797KS58": {
                          "t": "2025-02-14T20:58:00.648Z",
                          "p": 99.3193,
                          "ytm": 4.2245,
                          "ytw": 4.2245
                        },
                        "US912797LB15": {
                          "t": "2025-02-14T20:58:00.648Z",
                          "p": 98.9927,
                          "ytm": 4.2165,
                          "ytw": 4.2165
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
        "operationId": "FixedIncomeLatestPrices",
        "description": "This endpoint returns the latest prices for the given fixed income securities.\n"
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
