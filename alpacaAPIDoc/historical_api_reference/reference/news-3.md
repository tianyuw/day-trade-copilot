---
source_view: https://docs.alpaca.markets/reference/news-3
source_md: https://docs.alpaca.markets/reference/news-3.md
scraped_at_utc: 2026-01-26T01:04:10Z
---
# News articles

Returns the latest news articles across stocks and crypto. By default, returns the latest 10 news articles.


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
      "name": "News",
      "description": "Endpoints for getting news articles about the stock market."
    }
  ],
  "paths": {
    "/v1beta1/news": {
      "get": {
        "summary": "News articles",
        "parameters": [
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
            "name": "sort",
            "in": "query",
            "description": "Sort articles by updated date.",
            "schema": {
              "type": "string",
              "enum": [
                "asc",
                "desc"
              ],
              "default": "desc"
            }
          },
          {
            "name": "symbols",
            "in": "query",
            "schema": {
              "type": "string",
              "example": "AAPL,TSLA,BTCUSD"
            },
            "description": "A comma-separated list of symbols for which to query news."
          },
          {
            "name": "limit",
            "in": "query",
            "schema": {
              "type": "integer",
              "minimum": 1,
              "maximum": 50
            },
            "description": "Limit of news items to be returned for a result page.",
            "example": 10
          },
          {
            "name": "include_content",
            "in": "query",
            "schema": {
              "type": "boolean"
            },
            "description": "Boolean indicator to include content for news articles (if available)."
          },
          {
            "name": "exclude_contentless",
            "in": "query",
            "schema": {
              "type": "boolean"
            },
            "description": "Boolean indicator to exclude news articles that do not contain content."
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
            "content": {
              "application/json": {
                "examples": {
                  "news-response-example": {
                    "value": {
                      "news": [
                        {
                          "id": 24843171,
                          "headline": "Apple Leader in Phone Sales in China for Second Straight Month in November With 23.6% Share, According to Market Research Data",
                          "author": "Charles Gross",
                          "created_at": "2021-12-31T11:08:42Z",
                          "updated_at": "2021-12-31T11:08:43Z",
                          "summary": "This headline-only article is meant to show you why a stock is moving, the most difficult aspect of stock trading",
                          "content": "<p>This headline-only article is meant to show you why a stock is moving, the most difficult aspect of stock trading....</p>",
                          "url": "https://www.benzinga.com/news/21/12/24843171/apple-leader-in-phone-sales-in-china-for-second-straight-month-in-november-with-23-6-share-according",
                          "images": [],
                          "symbols": [
                            "AAPL"
                          ],
                          "source": "benzinga"
                        }
                      ],
                      "next_page_token": "MTY0MDk0ODkyMzAwMDAwMDAwMHwyNDg0MzE3MQ=="
                    }
                  }
                },
                "schema": {
                  "type": "object",
                  "properties": {
                    "news": {
                      "type": "array",
                      "items": {
                        "description": "Model representing a news article.",
                        "type": "object",
                        "properties": {
                          "id": {
                            "type": "integer",
                            "format": "int64",
                            "description": "News article ID."
                          },
                          "headline": {
                            "type": "string",
                            "minLength": 1,
                            "description": "Headline or title of the article."
                          },
                          "author": {
                            "type": "string",
                            "minLength": 1,
                            "description": "Original author of news article."
                          },
                          "created_at": {
                            "type": "string",
                            "format": "date-time",
                            "description": "Date article was created (RFC-3339)."
                          },
                          "updated_at": {
                            "type": "string",
                            "format": "date-time",
                            "description": "Date article was updated (RFC-3339)."
                          },
                          "summary": {
                            "type": "string",
                            "minLength": 1,
                            "description": "Summary text for the article (may be first sentence of content)."
                          },
                          "content": {
                            "type": "string",
                            "minLength": 1,
                            "description": "Content of the news article (might contain HTML)."
                          },
                          "url": {
                            "type": "string",
                            "format": "uri",
                            "description": "URL of article (if applicable).",
                            "nullable": true
                          },
                          "images": {
                            "type": "array",
                            "uniqueItems": true,
                            "description": "List of images (URLs) related to given article (may be empty).",
                            "items": {
                              "description": "A model representing images for a news article. Simply a URL to the image along with a size parameter suggesting the display size of the image.",
                              "type": "object",
                              "properties": {
                                "size": {
                                  "type": "string",
                                  "minLength": 1,
                                  "description": "Possible values for size are thumb, small and large.",
                                  "example": "thumb",
                                  "enum": [
                                    "thumb",
                                    "small",
                                    "large"
                                  ]
                                },
                                "url": {
                                  "type": "string",
                                  "minLength": 1,
                                  "description": "URL to image from news article.",
                                  "format": "uri"
                                }
                              },
                              "required": [
                                "size",
                                "url"
                              ],
                              "x-readme-ref-name": "news_image"
                            }
                          },
                          "symbols": {
                            "type": "array",
                            "description": "List of related or mentioned symbols.",
                            "items": {
                              "type": "string"
                            }
                          },
                          "source": {
                            "type": "string",
                            "minLength": 1,
                            "description": "Source where the news originated from (e.g. Benzinga)."
                          }
                        },
                        "required": [
                          "id",
                          "headline",
                          "author",
                          "created_at",
                          "updated_at",
                          "summary",
                          "content",
                          "images",
                          "symbols",
                          "source"
                        ],
                        "x-readme-ref-name": "news"
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
                    "news",
                    "next_page_token"
                  ],
                  "x-readme-ref-name": "news_resp"
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
        "operationId": "News",
        "description": "Returns the latest news articles across stocks and crypto. By default, returns the latest 10 news articles.\n",
        "tags": [
          "News"
        ]
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
