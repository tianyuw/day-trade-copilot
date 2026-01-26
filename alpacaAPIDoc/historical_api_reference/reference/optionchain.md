---
source_view: https://docs.alpaca.markets/reference/optionchain
source_md: https://docs.alpaca.markets/reference/optionchain.md
scraped_at_utc: 2026-01-26T01:04:10Z
---
# Option chain

The option chain endpoint provides the latest trade, latest quote, and greeks for each contract symbol of the underlying symbol.


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
    "/v1beta1/options/snapshots/{underlying_symbol}": {
      "get": {
        "summary": "Option chain",
        "tags": [
          "Option"
        ],
        "parameters": [
          {
            "name": "underlying_symbol",
            "description": "The financial instrument on which an option contract is based or derived.",
            "in": "path",
            "required": true,
            "schema": {
              "type": "string"
            },
            "example": "AAPL"
          },
          {
            "name": "feed",
            "in": "query",
            "description": "The source feed of the data. `opra` is the official OPRA feed, `indicative` is a free indicative feed where trades are delayed and quotes are modified. Default: `opra` if the user has a subscription, otherwise `indicative`.\n",
            "schema": {
              "type": "string",
              "enum": [
                "opra",
                "indicative"
              ],
              "default": "opra",
              "x-readme-ref-name": "option_feed"
            }
          },
          {
            "name": "limit",
            "in": "query",
            "schema": {
              "type": "integer",
              "minimum": 1,
              "maximum": 1000,
              "default": 100
            },
            "description": "Number of maximum snapshots to return in a response.\nThe limit applies to the total number of data points, not the number per symbol!\nUse `next_page_token` to fetch the next set of responses.\n"
          },
          {
            "name": "updated_since",
            "in": "query",
            "required": false,
            "schema": {
              "type": "string",
              "format": "date-time"
            },
            "description": "Filter to snapshots that were updated since this timestamp, meaning that the timestamp of the trade or the quote is greater than or equal to this value.\nFormat: RFC-3339 or YYYY-MM-DD. If missing, all values are returned.\n"
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
            "name": "type",
            "in": "query",
            "description": "Filter contracts by the type (call or put).",
            "schema": {
              "type": "string",
              "enum": [
                "call",
                "put"
              ]
            }
          },
          {
            "name": "strike_price_gte",
            "in": "query",
            "description": "Filter contracts with strike price greater than or equal to the specified value.",
            "schema": {
              "type": "number",
              "format": "double"
            }
          },
          {
            "name": "strike_price_lte",
            "in": "query",
            "description": "Filter contracts with strike price less than or equal to the specified value.",
            "schema": {
              "type": "number",
              "format": "double"
            }
          },
          {
            "name": "expiration_date",
            "in": "query",
            "description": "Filter contracts by the exact expiration date (format: YYYY-MM-DD).",
            "schema": {
              "type": "string",
              "format": "date"
            }
          },
          {
            "name": "expiration_date_gte",
            "in": "query",
            "description": "Filter contracts with expiration date greater than or equal to the specified date.",
            "schema": {
              "type": "string",
              "format": "date"
            }
          },
          {
            "name": "expiration_date_lte",
            "in": "query",
            "description": "Filter contracts with expiration date less than or equal to the specified date.",
            "schema": {
              "type": "string",
              "format": "date"
            }
          },
          {
            "name": "root_symbol",
            "in": "query",
            "description": "Filter contracts by the root symbol.",
            "schema": {
              "type": "string"
            },
            "example": "AAPL1"
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
                    "snapshots": {
                      "type": "object",
                      "additionalProperties": {
                        "type": "object",
                        "description": "A snapshot provides the latest trade and latest quote.",
                        "properties": {
                          "dailyBar": {
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
                          },
                          "greeks": {
                            "type": "object",
                            "description": "The greeks for the contract calculated using the Black-Scholes model.",
                            "properties": {
                              "delta": {
                                "type": "number",
                                "format": "double"
                              },
                              "gamma": {
                                "type": "number",
                                "format": "double"
                              },
                              "theta": {
                                "type": "number",
                                "format": "double"
                              },
                              "vega": {
                                "type": "number",
                                "format": "double"
                              },
                              "rho": {
                                "type": "number",
                                "format": "double"
                              }
                            },
                            "required": [
                              "delta",
                              "gamma",
                              "theta",
                              "vega",
                              "rho"
                            ],
                            "x-readme-ref-name": "option_greeks"
                          },
                          "impliedVolatility": {
                            "description": "Implied volatility calculated using the Black-Scholes model.",
                            "format": "double",
                            "type": "number"
                          },
                          "latestQuote": {
                            "type": "object",
                            "description": "The best bid and ask information for a given option.\n",
                            "example": {
                              "t": "2024-02-28T15:30:28.046330624Z",
                              "ax": "w",
                              "ap": 0.16,
                              "as": 669,
                              "bx": "W",
                              "bp": 0.15,
                              "bs": 164,
                              "c": "A"
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
                                "description": "Bid exchange.",
                                "x-go-name": "BidExchange"
                              },
                              "bp": {
                                "type": "number",
                                "format": "double",
                                "description": "Bid price.",
                                "x-go-name": "BidPrice"
                              },
                              "bs": {
                                "type": "integer",
                                "format": "uint32",
                                "description": "Bid size.",
                                "x-go-name": "BidSize"
                              },
                              "ax": {
                                "type": "string",
                                "description": "Ask exchange.",
                                "x-go-name": "AskExchange"
                              },
                              "ap": {
                                "type": "number",
                                "format": "double",
                                "description": "Ask price.",
                                "x-go-name": "AskPrice"
                              },
                              "as": {
                                "type": "integer",
                                "format": "uint32",
                                "description": "Ask size.",
                                "x-go-name": "AskSize"
                              },
                              "c": {
                                "type": "string",
                                "description": "Quote condition.",
                                "x-go-name": "Condition"
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
                              "c"
                            ],
                            "x-readme-ref-name": "option_quote"
                          },
                          "latestTrade": {
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
                          },
                          "minuteBar": {
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
                          },
                          "prevDailyBar": {
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
                        },
                        "x-readme-ref-name": "option_snapshot"
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
                    "snapshots",
                    "next_page_token"
                  ],
                  "x-readme-ref-name": "option_snapshots_resp"
                },
                "examples": {
                  "snapshots": {
                    "value": {
                      "snapshots": {
                        "AAPL240426C00162500": {
                          "greeks": {
                            "delta": 0.7521304109871954,
                            "gamma": 0.06241426404871288,
                            "rho": 0.009910739032549095,
                            "theta": -0.2847623059595503,
                            "vega": 0.047540520834498785
                          },
                          "impliedVolatility": 0.3372405712050441,
                          "latestQuote": {
                            "ap": 4.3,
                            "as": 91,
                            "ax": "B",
                            "bp": 4.15,
                            "bs": 16,
                            "bx": "C",
                            "c": "A",
                            "t": "2024-04-22T19:59:59.992734208Z"
                          },
                          "latestTrade": {
                            "c": "I",
                            "p": 4.1,
                            "s": 1,
                            "t": "2024-04-22T19:57:32.589554432Z",
                            "x": "A"
                          }
                        }
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
        "operationId": "OptionChain",
        "description": "The option chain endpoint provides the latest trade, latest quote, and greeks for each contract symbol of the underlying symbol.\n"
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
