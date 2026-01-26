---
source_view: https://docs.alpaca.markets/reference/stocktrades-1
source_md: https://docs.alpaca.markets/reference/stocktrades-1.md
scraped_at_utc: 2026-01-26T01:04:10Z
---
# Historical trades

The historical stock trades API provides trade data for a list of stock symbols between the specified dates.

The returned results are sorted by symbol first then by trade timestamp. This means that you are likely to see only one symbol in your first response if there are enough trades for that symbol to hit the limit you requested.

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
      "name": "Stock",
      "description": "Endpoints for stocks."
    }
  ],
  "paths": {
    "/v2/stocks/trades": {
      "get": {
        "summary": "Historical trades",
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
            "name": "asof",
            "in": "query",
            "description": "The as-of date of the queried stock symbol(s). Format: YYYY-MM-DD. Default: current day.\n\nThis date is used to identify the underlying entity of the provided symbol(s), so that name changes for this entity can be found. Data for past symbol(s) is returned if the query date range spans the name change.\n\nThe special value of \"-\" means symbol mapping is skipped. Data is returned based on the symbol alone without looking up previous names. The same happens if the queried symbol is not found on the given `asof` date.\n\nExample: FB was renamed to META in 2022-06-09. Querying META with an `asof` date after 2022-06-09 will also yield FB data. The data for the FB ticker will be labeled as META because they are considered the same underlying entity as of 2022-06-09. Querying FB with an `asof` date after 2022-06-09 will only return data with the FB ticker, not with META. But with an `asof` date before 2022-06-09, META will also be returned (as FB).\n",
            "schema": {
              "type": "string"
            }
          },
          {
            "name": "feed",
            "in": "query",
            "description": "The source feed of the data.\n - `sip`: all US exchanges\n - `iex`: Investors EXchange\n - `boats`: Blue Ocean ATS, overnight US trading data\n - `otc`: over-the-counter exchanges\n",
            "schema": {
              "type": "string",
              "enum": [
                "iex",
                "otc",
                "sip",
                "boats"
              ],
              "default": "sip",
              "x-readme-ref-name": "stock_historical_feed"
            }
          },
          {
            "name": "currency",
            "in": "query",
            "description": "The currency of all prices in ISO 4217 format. Default: USD.\n",
            "schema": {
              "type": "string"
            }
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
                  "x-readme-ref-name": "stock_trades_resp"
                },
                "examples": {
                  "trades": {
                    "value": {
                      "trades": {
                        "AAPL": [
                          {
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
                          {
                            "t": "2022-01-03T09:00:00.24483968Z",
                            "x": "P",
                            "p": 178.26,
                            "s": 1,
                            "c": [
                              "@",
                              "F",
                              "T",
                              "I"
                            ],
                            "i": 2,
                            "z": "C"
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
        "operationId": "StockTrades",
        "description": "The historical stock trades API provides trade data for a list of stock symbols between the specified dates.\n\nThe returned results are sorted by symbol first then by trade timestamp. This means that you are likely to see only one symbol in your first response if there are enough trades for that symbol to hit the limit you requested.\n\nIn these situations, if you keep requesting again with the `next_page_token` from the previous response, you will eventually reach the other symbols if any trades were found for them."
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
