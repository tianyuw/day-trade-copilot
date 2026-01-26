---
source_view: https://docs.alpaca.markets/reference/cryptolatestquotes-1
source_md: https://docs.alpaca.markets/reference/cryptolatestquotes-1.md
scraped_at_utc: 2026-01-26T01:04:10Z
---
# Latest quotes

The latest quotes endpoint returns the latest bid and ask prices for the crypto symbols provided.


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
    "/v1beta3/crypto/{loc}/latest/quotes": {
      "get": {
        "summary": "Latest quotes",
        "tags": [
          "Crypto"
        ],
        "security": [],
        "parameters": [
          {
            "name": "loc",
            "in": "path",
            "description": "Crypto location from where the latest market data is retrieved.\n- `us`: Alpaca US\n- `us-1`: Kraken US\n- `eu-1`: Kraken EU\n",
            "required": true,
            "schema": {
              "type": "string",
              "enum": [
                "us",
                "us-1",
                "eu-1"
              ],
              "description": "Crypto location from where the latest market data is retrieved.",
              "x-go-name": "TypeLatestLoc",
              "x-readme-ref-name": "crypto_latest_loc"
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
                  "required": [
                    "quotes"
                  ],
                  "x-readme-ref-name": "crypto_latest_quotes_resp"
                },
                "examples": {
                  "quotes": {
                    "value": {
                      "quotes": {
                        "ETH/USD": {
                          "t": "2022-05-26T11:47:18.499478272Z",
                          "bp": 1817,
                          "bs": 4.76,
                          "ap": 1817.7,
                          "as": 6.137
                        },
                        "BTC/USD": {
                          "t": "2022-05-26T11:47:18.44347136Z",
                          "bp": 29058,
                          "bs": 0.3544,
                          "ap": 29059,
                          "as": 3.252
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
        "operationId": "CryptoLatestQuotes",
        "description": "The latest quotes endpoint returns the latest bid and ask prices for the crypto symbols provided.\n"
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
