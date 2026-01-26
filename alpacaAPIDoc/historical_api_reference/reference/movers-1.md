---
source_view: https://docs.alpaca.markets/reference/movers-1
source_md: https://docs.alpaca.markets/reference/movers-1.md
scraped_at_utc: 2026-01-26T01:04:10Z
---
# Top market movers

Returns the top market movers (gainers and losers) based on real time SIP data.
The change for each symbol is calculated from the previous closing price and the latest closing price.

For stocks, the endpoint resets at market open. Until then, it shows the previous market day's movers.
The data is split-adjusted. Only tradable symbols in exchanges are included.

For crypto, the endpoint resets at midnight.

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
      "name": "Screener",
      "description": "Endpoints for most active stocks and top movers."
    }
  ],
  "paths": {
    "/v1beta1/screener/{market_type}/movers": {
      "get": {
        "summary": "Top market movers",
        "tags": [
          "Screener"
        ],
        "parameters": [
          {
            "name": "market_type",
            "in": "path",
            "required": true,
            "schema": {
              "type": "string",
              "enum": [
                "stocks",
                "crypto"
              ],
              "description": "Market type (stocks or crypto).",
              "x-readme-ref-name": "market_type"
            },
            "description": "Screen-specific market (stocks or crypto)."
          },
          {
            "name": "top",
            "in": "query",
            "required": false,
            "schema": {
              "type": "integer",
              "format": "int32",
              "default": 10,
              "minimum": 1,
              "maximum": 50
            },
            "description": "Number of top market movers to fetch (gainers and losers). Will return this number of results for each. By default, 10 gainers and 10 losers.\n"
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
                  "description": "Contains list of market movers.",
                  "properties": {
                    "gainers": {
                      "type": "array",
                      "description": "List of top N gainers.",
                      "items": {
                        "title": "Mover",
                        "type": "object",
                        "description": "A symbol whose price moved significantly.",
                        "example": {
                          "symbol": "AGRI",
                          "percent_change": 145.56,
                          "change": 2.46,
                          "price": 4.15
                        },
                        "properties": {
                          "symbol": {
                            "type": "string",
                            "description": "Symbol of market moving asset."
                          },
                          "percent_change": {
                            "type": "number",
                            "format": "double",
                            "description": "Percentage difference change for the day."
                          },
                          "change": {
                            "type": "number",
                            "format": "double",
                            "description": "Difference in change for the day."
                          },
                          "price": {
                            "type": "number",
                            "format": "double",
                            "description": "Current price of market moving asset."
                          }
                        },
                        "required": [
                          "symbol",
                          "percent_change",
                          "change",
                          "price"
                        ],
                        "x-readme-ref-name": "mover"
                      }
                    },
                    "losers": {
                      "description": "List of top N losers.",
                      "type": "array",
                      "items": {
                        "title": "Mover",
                        "type": "object",
                        "description": "A symbol whose price moved significantly.",
                        "example": {
                          "symbol": "AGRI",
                          "percent_change": 145.56,
                          "change": 2.46,
                          "price": 4.15
                        },
                        "properties": {
                          "symbol": {
                            "type": "string",
                            "description": "Symbol of market moving asset."
                          },
                          "percent_change": {
                            "type": "number",
                            "format": "double",
                            "description": "Percentage difference change for the day."
                          },
                          "change": {
                            "type": "number",
                            "format": "double",
                            "description": "Difference in change for the day."
                          },
                          "price": {
                            "type": "number",
                            "format": "double",
                            "description": "Current price of market moving asset."
                          }
                        },
                        "required": [
                          "symbol",
                          "percent_change",
                          "change",
                          "price"
                        ],
                        "x-readme-ref-name": "mover"
                      }
                    },
                    "market_type": {
                      "type": "string",
                      "enum": [
                        "stocks",
                        "crypto"
                      ],
                      "description": "Market type (stocks or crypto).",
                      "x-readme-ref-name": "market_type"
                    },
                    "last_updated": {
                      "type": "string",
                      "description": "Time when the movers were last computed. Formatted as a RFC-3339 date-time with nanosecond precision.\n"
                    }
                  },
                  "required": [
                    "gainers",
                    "losers",
                    "market_type",
                    "last_updated"
                  ],
                  "x-readme-ref-name": "movers_resp"
                },
                "examples": {
                  "movers": {
                    "value": {
                      "gainers": [
                        {
                          "symbol": "AGRI",
                          "percent_change": 145.56,
                          "change": 2.46,
                          "price": 4.15
                        },
                        {
                          "symbol": "GRCYW",
                          "percent_change": 85.63,
                          "change": 0.03,
                          "price": 0.0594
                        }
                      ],
                      "losers": [
                        {
                          "symbol": "MTACW",
                          "percent_change": -63.07,
                          "change": -0.26,
                          "price": 0.1502
                        },
                        {
                          "symbol": "TIG",
                          "percent_change": -51.21,
                          "change": -3.61,
                          "price": 3.435
                        }
                      ],
                      "market_type": "stocks",
                      "last_updated": "2022-03-10T17:53:30.088309839Z"
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
        "operationId": "Movers",
        "description": "Returns the top market movers (gainers and losers) based on real time SIP data.\nThe change for each symbol is calculated from the previous closing price and the latest closing price.\n\nFor stocks, the endpoint resets at market open. Until then, it shows the previous market day's movers.\nThe data is split-adjusted. Only tradable symbols in exchanges are included.\n\nFor crypto, the endpoint resets at midnight."
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
