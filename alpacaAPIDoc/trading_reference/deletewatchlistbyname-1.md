---
source_view: https://docs.alpaca.markets/reference/deletewatchlistbyname-1
source_md: https://docs.alpaca.markets/reference/deletewatchlistbyname-1.md
scraped_at_utc: 2026-01-22T23:02:18Z
---
# Delete Watchlist By Name

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
    "/v2/watchlists:by_name": {
      "delete": {
        "tags": [
          "Watchlists"
        ],
        "summary": "Delete Watchlist By Name",
        "parameters": [
          {
            "schema": {
              "type": "string"
            },
            "in": "query",
            "name": "name",
            "required": true,
            "description": "name of the watchlist"
          }
        ],
        "responses": {
          "204": {
            "description": "No Content"
          }
        },
        "operationId": "deleteWatchlistByName",
        "description": "Delete a watchlist. This is a permanent deletion."
      },
      "parameters": []
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
