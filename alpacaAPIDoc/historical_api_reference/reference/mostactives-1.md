---
source_view: https://docs.alpaca.markets/reference/mostactives-1
source_md: https://docs.alpaca.markets/reference/mostactives-1.md
scraped_at_utc: 2026-01-26T01:04:10Z
---
# Most active stocks

Returns the most active stocks by volume or trade count based on real time SIP data. By default, returns the top 10 symbols by volume.


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
    "/v1beta1/screener/stocks/most-actives": {
      "get": {
        "summary": "Most active stocks",
        "tags": [
          "Screener"
        ],
        "parameters": [
          {
            "name": "by",
            "in": "query",
            "required": false,
            "schema": {
              "type": "string",
              "enum": [
                "volume",
                "trades"
              ],
              "default": "volume"
            },
            "description": "The metric used for ranking the most active stocks."
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
              "maximum": 100
            },
            "description": "The number of top most active stocks to fetch per day."
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
                    "most_actives": {
                      "type": "array",
                      "description": "List of top N most active symbols.",
                      "items": {
                        "description": "A stock that is most active by either volume or trade count.",
                        "type": "object",
                        "example": {
                          "symbol": "AAPL",
                          "volume": 122709184,
                          "trade_count": 639626
                        },
                        "properties": {
                          "symbol": {
                            "type": "string"
                          },
                          "volume": {
                            "type": "integer",
                            "format": "int64",
                            "description": "Cumulative volume for the current trading day."
                          },
                          "trade_count": {
                            "type": "integer",
                            "format": "int64",
                            "description": "Cumulative trade count for the current trading day."
                          }
                        },
                        "required": [
                          "symbol",
                          "volume",
                          "trade_count"
                        ],
                        "x-readme-ref-name": "most_active"
                      }
                    },
                    "last_updated": {
                      "type": "string",
                      "description": "Time when the most actives were last computed. Formatted as a RFC-3339 date-time with nanosecond precision.\n"
                    }
                  },
                  "required": [
                    "most_actives",
                    "last_updated"
                  ],
                  "x-readme-ref-name": "most_actives_resp"
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
        "operationId": "MostActives",
        "description": "Returns the most active stocks by volume or trade count based on real time SIP data. By default, returns the top 10 symbols by volume.\n"
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
