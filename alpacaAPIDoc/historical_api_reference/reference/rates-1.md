---
source_view: https://docs.alpaca.markets/reference/rates-1
source_md: https://docs.alpaca.markets/reference/rates-1.md
scraped_at_utc: 2026-01-26T01:04:10Z
---
# Historical rates for currency pairs

Get historical forex rates for the given currency pairs in the given time interval and at the given timeframe (snapshot frequency).


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
    "/v1beta1/forex/rates": {
      "get": {
        "summary": "Historical rates for currency pairs",
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
          },
          {
            "name": "timeframe",
            "in": "query",
            "required": false,
            "schema": {
              "type": "string",
              "default": "1Min",
              "description": "The sampling interval of the currency rates. For example, 5S returns forex rates sampled every five seconds.\nYou can use the following values:\n - `5Sec` or `5S`\n - `1Min` or `1T`\n - `1Day` or `1D`\n",
              "x-readme-ref-name": "forex_timeframe"
            }
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
          },
          {
            "name": "page_token",
            "in": "query",
            "schema": {
              "type": "string"
            },
            "description": "The pagination token from which to continue. The value to pass here is returned in specific requests when more data is available, usually because of a response result limit.\n"
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
                    "rates": {
                      "type": "object",
                      "additionalProperties": {
                        "type": "array",
                        "items": {
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
                    "next_page_token": {
                      "type": "string",
                      "description": "Pagination token for the next page.",
                      "nullable": true,
                      "x-readme-ref-name": "next_page_token"
                    }
                  },
                  "required": [
                    "rates",
                    "next_page_token"
                  ],
                  "x-readme-ref-name": "forex_rates_resp"
                },
                "examples": {
                  "USDJPY": {
                    "value": {
                      "next_page_token": "VVNESlBZfDIwMjItMDEtMDNUMDA6MDM6MDBa",
                      "rates": {
                        "USDJPY": [
                          {
                            "bp": 114.192,
                            "mp": 115.144,
                            "ap": 115.18,
                            "t": "2022-01-03T00:01:00Z"
                          },
                          {
                            "bp": 114.189,
                            "mp": 115.138,
                            "ap": 115.185,
                            "t": "2022-01-03T00:02:00Z"
                          },
                          {
                            "bp": 115.122,
                            "mp": 115.131,
                            "ap": 115.148,
                            "t": "2022-01-03T00:03:00Z"
                          }
                        ]
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
        "operationId": "Rates",
        "description": "Get historical forex rates for the given currency pairs in the given time interval and at the given timeframe (snapshot frequency).\n"
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
