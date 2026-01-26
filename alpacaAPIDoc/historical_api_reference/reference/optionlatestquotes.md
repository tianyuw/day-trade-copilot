---
source_view: https://docs.alpaca.markets/reference/optionlatestquotes
source_md: https://docs.alpaca.markets/reference/optionlatestquotes.md
scraped_at_utc: 2026-01-26T01:04:10Z
---
# Latest quotes

The latest multi-quotes endpoint provides the latest bid and ask prices for each given contract symbol.


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
    "/v1beta1/options/quotes/latest": {
      "get": {
        "summary": "Latest quotes",
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
                      }
                    }
                  },
                  "required": [
                    "quotes"
                  ],
                  "x-readme-ref-name": "option_latest_quotes_resp"
                },
                "examples": {
                  "quotes": {
                    "value": {
                      "quotes": {
                        "AAPL240419P00140000": {
                          "t": "2024-02-28T15:30:28.046330624Z",
                          "ax": "w",
                          "ap": 0.16,
                          "as": 669,
                          "bx": "W",
                          "bp": 0.15,
                          "bs": 164,
                          "c": "A"
                        },
                        "AAPL250321C00190000": {
                          "t": "2024-02-28T15:47:13.663636224Z",
                          "ax": "X",
                          "ap": 17,
                          "as": 622,
                          "bx": "X",
                          "bp": 16.75,
                          "bs": 368,
                          "c": " "
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
        "operationId": "OptionLatestQuotes",
        "description": "The latest multi-quotes endpoint provides the latest bid and ask prices for each given contract symbol.\n"
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
