---
source_view: https://docs.alpaca.markets/reference/getwatchlists-1
source_md: https://docs.alpaca.markets/reference/getwatchlists-1.md
scraped_at_utc: 2026-01-22T23:02:18Z
---
# Get All Watchlists

Returns the list of watchlists registered under the account.

# OpenAPI definition

```json
{
  "openapi": "3.0.0",
  "info": {
    "title": "Trading API",
    "description": "Alpaca's Trading API is a modern platform for algorithmic trading.",
    "version": "2.0.1",
    "contact": {
      "name": "Alpaca Support",
      "email": "support@alpaca.markets",
      "url": "https://alpaca.markets/support"
    },
    "termsOfService": "https://s3.amazonaws.com/files.alpaca.markets/disclosures/library/TermsAndConditions.pdf"
  },
  "servers": [
    {
      "url": "https://paper-api.alpaca.markets",
      "description": "Paper"
    },
    {
      "url": "https://api.alpaca.markets",
      "description": "Live"
    }
  ],
  "tags": [
    {
      "name": "Watchlists"
    }
  ],
  "paths": {
    "/v2/watchlists": {
      "get": {
        "tags": [
          "Watchlists"
        ],
        "summary": "Get All Watchlists",
        "parameters": [],
        "responses": {
          "200": {
            "description": "Successful response",
            "content": {
              "application/json": {
                "examples": {
                  "example-1": {
                    "value": [
                      {
                        "id": "3174d6df-7726-44b4-a5bd-7fda5ae6e009",
                        "account_id": "abe25343-a7ba-4255-bdeb-f7e013e9ee5d",
                        "created_at": "2022-01-31T21:49:05.14628Z",
                        "updated_at": "2022-01-31T21:49:05.14628Z",
                        "name": "Primary Watchlist"
                      }
                    ]
                  }
                },
                "schema": {
                  "type": "array",
                  "items": {
                    "description": "The watchlist API provides CRUD operation for the account’s watchlist. An account can have multiple watchlists and each is uniquely identified by id but can also be addressed by user-defined name.\n",
                    "type": "object",
                    "x-examples": {
                      "example-1": {
                        "id": "3174d6df-7726-44b4-a5bd-7fda5ae6e009",
                        "account_id": "abe25343-a7ba-4255-bdeb-f7e013e9ee5d",
                        "created_at": "2022-01-31T21:49:05.14628Z",
                        "updated_at": "2022-01-31T21:49:05.14628Z",
                        "name": "Primary Watchlist"
                      }
                    },
                    "title": "Watchlist",
                    "properties": {
                      "id": {
                        "type": "string",
                        "format": "uuid",
                        "description": "watchlist id"
                      },
                      "account_id": {
                        "type": "string",
                        "format": "uuid",
                        "description": "account ID"
                      },
                      "created_at": {
                        "type": "string",
                        "format": "date-time"
                      },
                      "updated_at": {
                        "type": "string",
                        "format": "date-time"
                      },
                      "name": {
                        "type": "string",
                        "minLength": 1,
                        "description": "user-defined watchlist name (up to 64 characters)"
                      }
                    },
                    "required": [
                      "id",
                      "account_id",
                      "created_at",
                      "updated_at",
                      "name"
                    ],
                    "x-readme-ref-name": "WatchlistWithoutAsset"
                  }
                }
              }
            }
          }
        },
        "operationId": "getWatchlists",
        "description": "Returns the list of watchlists registered under the account."
      }
    }
  },
  "components": {
    "securitySchemes": {
      "API_Key": {
        "name": "APCA-API-KEY-ID",
        "type": "apiKey",
        "in": "header",
        "description": ""
      },
      "API_Secret": {
        "name": "APCA-API-SECRET-KEY",
        "type": "apiKey",
        "in": "header",
        "description": ""
      }
    }
  },
  "security": [
    {
      "API_Key": [],
      "API_Secret": []
    }
  ],
  "x-readme": {
    "explorer-enabled": true,
    "proxy-enabled": false
  }
}
```
