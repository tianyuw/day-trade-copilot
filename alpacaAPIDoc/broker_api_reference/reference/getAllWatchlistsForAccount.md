---
source_view: https://docs.alpaca.markets/reference/getallwatchlistsforaccount
source_md: https://docs.alpaca.markets/reference/getallwatchlistsforaccount.md
scraped_at_utc: 2026-01-27T04:30:48Z
---
# Retrieve all Watchlists for an Account

Fetch a list of all watchlists currently in an account.

# OpenAPI definition

```json
{
  "openapi": "3.0.0",
  "x-stoplight": {
    "id": "y5xqkgq9w6jde"
  },
  "info": {
    "title": "Broker API",
    "description": "Open brokerage accounts, enable stock, options and crypto trading. Manage the ongoing user experience and brokerage customer lifecycle with the Alpaca Broker API",
    "version": "1.1.1",
    "contact": {
      "name": "Alpaca Support",
      "email": "support@alpaca.markets",
      "url": "https://alpaca.markets/support"
    },
    "termsOfService": "https://s3.amazonaws.com/files.alpaca.markets/disclosures/library/TermsAndConditions.pdf"
  },
  "servers": [
    {
      "url": "https://broker-api.sandbox.alpaca.markets",
      "description": "Sandbox endpoint"
    },
    {
      "url": "https://broker-api.alpaca.markets",
      "description": "Production endpoint"
    }
  ],
  "tags": [
    {
      "name": "Watchlist"
    }
  ],
  "components": {
    "securitySchemes": {
      "BasicAuth": {
        "type": "http",
        "scheme": "basic"
      }
    }
  },
  "paths": {
    "/v1/trading/accounts/{account_id}/watchlists": {
      "parameters": [
        {
          "schema": {
            "type": "string",
            "format": "uuid"
          },
          "name": "account_id",
          "in": "path",
          "required": true,
          "description": "Unique identifier of an account."
        }
      ],
      "get": {
        "summary": "Retrieve all Watchlists for an Account",
        "tags": [
          "Watchlist"
        ],
        "responses": {
          "200": {
            "description": "OK",
            "content": {
              "application/json": {
                "schema": {
                  "type": "array",
                  "items": {
                    "title": "Watchlist",
                    "type": "object",
                    "description": "Represents a set of securities observed by a user.",
                    "properties": {
                      "id": {
                        "type": "string",
                        "format": "uuid",
                        "description": "Unique identifier of the watchlist itself.\n"
                      },
                      "account_id": {
                        "type": "string",
                        "format": "uuid",
                        "description": "Unique identifier of the account that owns this watchlist.\n"
                      },
                      "created_at": {
                        "type": "string",
                        "format": "date-time",
                        "description": "When watchlist was created"
                      },
                      "updated_at": {
                        "type": "string",
                        "format": "date-time",
                        "description": "When watchlist was last updated"
                      },
                      "name": {
                        "type": "string",
                        "pattern": "^[a-zA-Z0-9]+$",
                        "description": "User friendly Name of watchlist"
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
        "operationId": "getAllWatchlistsForAccount",
        "description": "Fetch a list of all watchlists currently in an account."
      }
    }
  },
  "security": [
    {
      "BasicAuth": []
    }
  ],
  "x-readme": {
    "explorer-enabled": true,
    "proxy-enabled": false
  }
}
```
