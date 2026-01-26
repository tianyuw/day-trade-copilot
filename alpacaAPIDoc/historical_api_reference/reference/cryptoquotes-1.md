---
source_view: https://docs.alpaca.markets/reference/cryptoquotes-1
source_md: https://docs.alpaca.markets/reference/cryptoquotes-1.md
scraped_at_utc: 2026-01-26T01:04:10Z
---
# Historical quotes

The crypto quotes API provides historical quote data for a list of crypto symbols between the specified dates.
The oldest date to retrieve historical quotes of us-1 location is 14th October, 2025 12AM UTC.

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
    "/v1beta3/crypto/{loc}/quotes": {
      "get": {
        "summary": "Historical quotes",
        "tags": [
          "Crypto"
        ],
        "security": [],
        "parameters": [
          {
            "name": "loc",
            "in": "path",
            "description": "Crypto location from where the historical market data is retrieved.\n- `us`: Alpaca US\n- `us-1`: Kraken US\n- `eu-1`: Kraken EU\n",
            "required": true,
            "schema": {
              "type": "string",
              "enum": [
                "us",
                "us-1",
                "eu-1"
              ],
              "description": "Crypto location from where the historical market data is retrieved.",
              "x-go-name": "TypeHistoricalLoc",
              "x-readme-ref-name": "crypto_historical_loc"
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
                    "quotes": {
                      "type": "object",
                      "additionalProperties": {
                        "type": "array",
                        "items": {
                          "type": "object",
                          "description": "The best bid and ask information for a given security.",
                          "example": {
                            "t": "2022-05-26T11:47:18.44347136Z",
                            "bp": 29058,
                            "bs": 0.3544,
                            "ap": 29059,
                            "as": 3.252
                          },
                          "properties": {
                            "t": {
                              "type": "string",
                              "description": "Timestamp in RFC-3339 format with nanosecond precision.",
                              "format": "date-time",
                              "x-go-name": "Timestamp",
                              "x-readme-ref-name": "timestamp"
                            },
                            "bp": {
                              "type": "number",
                              "format": "double",
                              "description": "Bid price.",
                              "x-go-name": "BidPrice"
                            },
                            "bs": {
                              "type": "number",
                              "format": "double",
                              "description": "Bid size.",
                              "x-go-name": "BidSize"
                            },
                            "ap": {
                              "type": "number",
                              "format": "double",
                              "description": "Ask price.",
                              "x-go-name": "AskPrice"
                            },
                            "as": {
                              "type": "number",
                              "format": "double",
                              "description": "Ask size.",
                              "x-go-name": "AskSize"
                            }
                          },
                          "required": [
                            "t",
                            "bp",
                            "bs",
                            "ap",
                            "as"
                          ],
                          "x-readme-ref-name": "crypto_quote"
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
                    "quotes",
                    "next_page_token"
                  ],
                  "x-readme-ref-name": "crypto_quotes_resp"
                },
                "examples": {
                  "quotes": {
                    "value": {
                      "quotes": {
                        "BTC/USD": [
                          {
                            "t": "2022-05-26T11:47:18.44347136Z",
                            "bp": 29058,
                            "bs": 0.3544,
                            "ap": 29059,
                            "as": 3.252
                          }
                        ],
                        "ETH/USD": [
                          {
                            "t": "2022-05-26T11:47:18.499478272Z",
                            "bp": 1817,
                            "bs": 4.76,
                            "ap": 1817.7,
                            "as": 6.137
                          }
                        ]
                      },
                      "next_page_token": null
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
        "operationId": "CryptoQuotes",
        "description": "The crypto quotes API provides historical quote data for a list of crypto symbols between the specified dates.\nThe oldest date to retrieve historical quotes of us-1 location is 14th October, 2025 12AM UTC."
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
