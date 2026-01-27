---
source_view: https://docs.alpaca.markets/reference/deletewatchlistfromaccountbyid
source_md: https://docs.alpaca.markets/reference/deletewatchlistfromaccountbyid.md
scraped_at_utc: 2026-01-27T04:30:48Z
---
# Remove a Watchlist

Irrevocably delete a watchlist.

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
    "/v1/trading/accounts/{account_id}/watchlists/{watchlist_id}": {
      "parameters": [
        {
          "schema": {
            "type": "string",
            "format": "uuid"
          },
          "name": "account_id",
          "in": "path",
          "required": true,
          "description": "Unique identifier of an account"
        },
        {
          "schema": {
            "type": "string",
            "format": "uuid"
          },
          "name": "watchlist_id",
          "in": "path",
          "required": true,
          "description": "Unique identifier of a watchlist"
        }
      ],
      "delete": {
        "summary": "Remove a Watchlist",
        "tags": [
          "Watchlist"
        ],
        "operationId": "deleteWatchlistFromAccountById",
        "responses": {
          "200": {
            "description": "Watchlist deleted."
          }
        },
        "description": "Irrevocably delete a watchlist."
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
