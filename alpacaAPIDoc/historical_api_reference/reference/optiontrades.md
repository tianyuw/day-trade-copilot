---
source_view: https://docs.alpaca.markets/reference/optiontrades
source_md: https://docs.alpaca.markets/reference/optiontrades.md
scraped_at_utc: 2026-01-26T01:04:10Z
---
# Historical trades

The historical option trades API provides trade data for a list of contract symbols between the specified dates.

The returned results are sorted by symbol first then by trade timestamp.
This means that you are likely to see only one symbol in your first response if there are enough trades for that symbol to hit the limit you requested.

In these situations, if you keep requesting again with the `next_page_token` from the previous response, you will eventually reach the other symbols if any trades were found for them.

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
    "/v1beta1/options/trades": {
      "get": {
        "summary": "Historical trades",
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
            "name": "start",
            "in": "query",
            "required": false,
            "schema": {
              "type": "string",
              "format": "date-time"
            },
            "examples": {
              "RFC-3339 second": {
                "value": "2024-01-03T00:00:00Z",
                "summary": "RFC-3339 date-time with second accuracy"
              },
              "RFC-3339 nanosecond": {
                "value": "2024-01-03T01:02:03.123456789Z",
                "summary": "RFC-3339 date-time with nanosecond accuracy"
              },
              "RFC-3339 with timezone": {
                "value": "2024-01-03T09:30:00-04:00",
                "summary": "RFC-3339 date-time with time zone"
              },
              "date": {
                "value": "2024-01-03",
                "summary": "Date"
              }
            },
            "description": "The inclusive start of the interval. Format: RFC-3339 or YYYY-MM-DD.\nDefault: the beginning of the current day, but at least 15 minutes ago if the user doesn't have real-time access for the feed.\n"
          },
          {
            "name": "end",
            "in": "query",
            "required": false,
            "schema": {
              "type": "string",
              "format": "date-time"
            },
            "examples": {
              "RFC-3339 second": {
                "value": "2024-01-04T00:00:00Z",
                "summary": "RFC-3339 date-time with second accuracy"
              },
              "RFC-3339 nanosecond": {
                "value": "2024-01-04T01:02:03.123456789Z",
                "summary": "RFC-3339 date-time with nanosecond accuracy"
              },
              "RFC-3339 with timezone": {
                "value": "2024-01-04T09:30:00-04:00",
                "summary": "RFC-3339 date-time with time zone"
              },
              "date": {
                "value": "2024-01-04",
                "summary": "Date"
              }
            },
            "description": "The inclusive end of the interval. Format: RFC-3339 or YYYY-MM-DD.\nDefault: the current time if the user has a real-time access for the feed, otherwise 15 minutes before the current time.\n"
          },
          {
            "name": "limit",
            "in": "query",
            "required": false,
            "schema": {
              "type": "integer",
              "minimum": 1,
              "maximum": 10000,
              "default": 1000
            },
            "description": "The maximum number of data points to return in the response page.\nThe API may return less, even if there are more available data points in the requested interval.\nAlways check the `next_page_token` for more pages.\nThe limit applies to the total number of data points, not per symbol!\n"
          },
          {
            "name": "page_token",
            "in": "query",
            "schema": {
              "type": "string"
            },
            "description": "The pagination token from which to continue. The value to pass here is returned in specific requests when more data is available, usually because of a response result limit.\n"
          },
          {
            "name": "sort",
            "in": "query",
            "description": "Sort data in ascending or descending order.",
            "schema": {
              "type": "string",
              "description": "Sort data in ascending or descending order.",
              "enum": [
                "asc",
                "desc"
              ],
              "default": "asc",
              "x-go-name": "TypeSort",
              "x-readme-ref-name": "sort"
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
                        "type": "array",
                        "items": {
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
                    "currency": {
                      "type": "string"
                    },
                    "next_page_token": {
                      "type": "string",
                      "description": "Pagination token for the next page.",
                      "nullable": true,
                      "x-readme-ref-name": "next_page_token"
                    }
                  },
                  "required": [
                    "trades",
                    "next_page_token"
                  ],
                  "x-readme-ref-name": "option_trades_resp"
                },
                "examples": {
                  "trades": {
                    "value": {
                      "trades": {
                        "AAPL240112C00182500": [
                          {
                            "t": "2024-01-18T15:03:44.56339456Z",
                            "x": "B",
                            "p": 0.37,
                            "s": 1,
                            "c": "I"
                          },
                          {
                            "t": "2024-01-18T16:02:38.994758144Z",
                            "x": "C",
                            "p": 0.34,
                            "s": 1,
                            "c": "g"
                          }
                        ]
                      },
                      "next_page_token": "QUFQTHwyMDIyLTAxLTAzVDA5OjAwOjAwLjI0NDgzOTY4MFp8UHwwOTIyMzM3MjAzNjg1NDc3NTgxMA=="
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
        "operationId": "OptionTrades",
        "description": "The historical option trades API provides trade data for a list of contract symbols between the specified dates.\n\nThe returned results are sorted by symbol first then by trade timestamp.\nThis means that you are likely to see only one symbol in your first response if there are enough trades for that symbol to hit the limit you requested.\n\nIn these situations, if you keep requesting again with the `next_page_token` from the previous response, you will eventually reach the other symbols if any trades were found for them."
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
