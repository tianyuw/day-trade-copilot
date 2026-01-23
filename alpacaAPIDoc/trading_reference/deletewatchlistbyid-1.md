---
source_view: https://docs.alpaca.markets/reference/deletewatchlistbyid-1
source_md: https://docs.alpaca.markets/reference/deletewatchlistbyid-1.md
scraped_at_utc: 2026-01-22T23:02:18Z
---
# Delete Watchlist By Id

Delete a watchlist. This is a permanent deletion.

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
    "/v2/watchlists/{watchlist_id}": {
      "delete": {
        "tags": [
          "Watchlists"
        ],
        "summary": "Delete Watchlist By Id",
        "parameters": [],
        "responses": {
          "204": {
            "description": "No Content"
          },
          "404": {
            "description": "Watchlist not found"
          }
        },
        "operationId": "deleteWatchlistById",
        "description": "Delete a watchlist. This is a permanent deletion."
      },
      "parameters": [
        {
          "schema": {
            "type": "string",
            "format": "uuid"
          },
          "name": "watchlist_id",
          "in": "path",
          "required": true,
          "description": "watchlist id"
        }
      ]
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
