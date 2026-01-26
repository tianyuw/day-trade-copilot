---
source_view: https://docs.alpaca.markets/reference/stocklatestquotes-1
source_md: https://docs.alpaca.markets/reference/stocklatestquotes-1.md
scraped_at_utc: 2026-01-26T01:04:10Z
---
# Latest quotes

The latest quotes endpoint provides the latest best bid and ask prices for the given ticker symbols.


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
    "/v2/stocks/quotes/latest": {
      "get": {
        "summary": "Latest quotes",
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
            "name": "feed",
            "in": "query",
            "description": "The source feed of the data.\n\n - `sip`: all US exchanges\n - `iex`: Investors EXchange\n - `delayed_sip`: SIP with a 15 minute delay\n - `boats`: Blue Ocean, overnight US trading data\n - `overnight`: derived overnight US trading data\n - `otc`: over-the-counter exchanges\n\nDefault: `sip` if the user has the unlimited subscription, otherwise `iex`.\n",
            "schema": {
              "type": "string",
              "enum": [
                "delayed_sip",
                "iex",
                "otc",
                "sip",
                "boats",
                "overnight"
              ],
              "x-readme-ref-name": "stock_latest_feed"
            }
          },
          {
            "name": "currency",
            "in": "query",
            "description": "The currency of all prices in ISO 4217 format. Default: USD.\n",
            "schema": {
              "type": "string"
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
                        "type": "object",
                        "description": "The best bid and ask information for a given security.",
                        "example": {
                          "t": "2021-02-06T13:35:08.946977536Z",
                          "ax": "C",
                          "ap": 387.7,
                          "as": 1,
                          "bx": "N",
                          "bp": 387.67,
                          "bs": 1,
                          "c": [
                            "R"
                          ],
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
                          "bx": {
                            "type": "string",
                            "description": "Bid exchange. See `v2/stocks/meta/exchanges` for more details.",
                            "x-go-name": "BidExchange"
                          },
                          "bp": {
                            "type": "number",
                            "format": "double",
                            "description": "Bid price. 0 means the security has no active bid.",
                            "x-go-name": "BidPrice"
                          },
                          "bs": {
                            "type": "integer",
                            "format": "uint32",
                            "description": "Bid size in shares (round lots prior to November 3, 2025).",
                            "x-go-name": "BidSize"
                          },
                          "ax": {
                            "type": "string",
                            "description": "Ask exchange. See `v2/stocks/meta/exchanges` for more details.",
                            "x-go-name": "AskExchange"
                          },
                          "ap": {
                            "type": "number",
                            "format": "double",
                            "description": "Ask price. 0 means the security has no active ask.",
                            "x-go-name": "AskPrice"
                          },
                          "as": {
                            "type": "integer",
                            "format": "uint32",
                            "description": "Ask size in shares (round lots prior to November 3, 2025).",
                            "x-go-name": "AskSize"
                          },
                          "c": {
                            "description": "Condition flags. See `v2/stocks/meta/conditions/quote` for more details. If the array contains one flag, it applies to both the bid and ask. If the array contains two flags, the first one applies to the bid and the second one to the ask.\n",
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
                          }
                        },
                        "required": [
                          "t",
                          "bx",
                          "bp",
                          "bs",
                          "ap",
                          "as",
                          "ax",
                          "c",
                          "z"
                        ],
                        "x-readme-ref-name": "stock_quote"
                      }
                    },
                    "currency": {
                      "type": "string"
                    }
                  },
                  "required": [
                    "quotes"
                  ],
                  "x-readme-ref-name": "stock_latest_quotes_resp"
                },
                "examples": {
                  "quotes": {
                    "value": {
                      "quotes": {
                        "AAPL": {
                          "t": "2022-08-17T10:07:40.286587431Z",
                          "ax": "Q",
                          "ap": 172.7,
                          "as": 1,
                          "bx": "Q",
                          "bp": 172.62,
                          "bs": 2,
                          "c": [
                            "R"
                          ],
                          "z": "C"
                        },
                        "TSLA": {
                          "t": "2022-08-17T10:07:49.387064037Z",
                          "ax": "Q",
                          "ap": 911.6,
                          "as": 1,
                          "bx": "K",
                          "bp": 911.3,
                          "bs": 1,
                          "c": [
                            "R"
                          ],
                          "z": "C"
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
        "operationId": "StockLatestQuotes",
        "description": "The latest quotes endpoint provides the latest best bid and ask prices for the given ticker symbols.\n"
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
