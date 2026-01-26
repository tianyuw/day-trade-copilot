---
source_view: https://docs.alpaca.markets/reference/optionbars
source_md: https://docs.alpaca.markets/reference/optionbars.md
scraped_at_utc: 2026-01-26T01:04:10Z
---
# Historical bars

The historical option bars API provides aggregates for a list of option symbols between the specified dates.

The returned results are sorted by symbol first, then by bar timestamp.
This means that you are likely to see only one symbol in your first response if there are enough bars for that symbol to hit the limit you requested.

In these situations, if you keep requesting again with the `next_page_token` from the previous response, you will eventually reach the other symbols if any bars were found for them.

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
    "/v1beta1/options/bars": {
      "get": {
        "summary": "Historical bars",
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
            "name": "timeframe",
            "in": "query",
            "schema": {
              "type": "string"
            },
            "required": true,
            "x-go-name": "TimeFrame",
            "example": "1Min",
            "description": "The timeframe represented by each bar in aggregation.\nYou can use any of the following values:\n - `[1-59]Min` or `[1-59]T`, e.g. `5Min` or `5T` creates 5-minute aggregations\n - `[1-23]Hour` or `[1-23]H`, e.g. `12Hour` or `12H` creates 12-hour aggregations\n - `1Day` or `1D` creates 1-day aggregations\n - `1Week` or `1W` creates 1-week aggregations\n - `[1,2,3,4,6,12]Month` or `[1,2,3,4,6,12]M`, e.g. `3Month` or `3M` creates 3-month aggregations\n"
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
                    "bars": {
                      "type": "object",
                      "additionalProperties": {
                        "type": "array",
                        "items": {
                          "type": "object",
                          "description": "OHLC aggregate of all the trades in a given interval.",
                          "example": {
                            "t": "2024-01-18T05:00:00Z",
                            "o": 0.28,
                            "h": 0.28,
                            "l": 0.23,
                            "c": 0.23,
                            "v": 224,
                            "n": 26,
                            "vw": 0.245045
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
                          "x-readme-ref-name": "option_bar"
                        }
                      }
                    },
                    "next_page_token": {
                      "type": "string",
                      "description": "Pagination token for the next page.",
                      "nullable": true,
                      "x-readme-ref-name": "next_page_token"
                    },
                    "currency": {
                      "type": "string"
                    }
                  },
                  "required": [
                    "bars",
                    "next_page_token"
                  ],
                  "x-readme-ref-name": "option_bars_resp"
                },
                "examples": {
                  "bars": {
                    "value": {
                      "bars": {
                        "AAPL240419P00140000": [
                          {
                            "t": "2024-01-18T05:00:00Z",
                            "o": 0.38,
                            "h": 0.38,
                            "l": 0.34,
                            "c": 0.34,
                            "v": 12,
                            "n": 7,
                            "vw": 0.3525
                          }
                        ]
                      },
                      "next_page_token": "QUFQTHxNfDIwMjItMDEtMDNUMDk6MDA6MDAuMDAwMDAwMDAwWg=="
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
        "operationId": "optionBars",
        "description": "The historical option bars API provides aggregates for a list of option symbols between the specified dates.\n\nThe returned results are sorted by symbol first, then by bar timestamp.\nThis means that you are likely to see only one symbol in your first response if there are enough bars for that symbol to hit the limit you requested.\n\nIn these situations, if you keep requesting again with the `next_page_token` from the previous response, you will eventually reach the other symbols if any bars were found for them."
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
