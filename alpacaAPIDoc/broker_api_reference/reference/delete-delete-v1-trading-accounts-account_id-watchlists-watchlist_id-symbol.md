---
source_view: https://docs.alpaca.markets/reference/delete-delete-v1-trading-accounts-account_id-watchlists-watchlist_id-symbol
source_md: https://docs.alpaca.markets/reference/delete-delete-v1-trading-accounts-account_id-watchlists-watchlist_id-symbol.md
scraped_at_utc: 2026-01-27T04:30:48Z
---
# Remove a Symbol from a Watchlist

Delete one entry for an asset by symbol name

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
    "/v1/trading/accounts/{account_id}/watchlists/{watchlist_id}/{symbol}": {
      "parameters": [
        {
          "schema": {
            "type": "string"
          },
          "name": "account_id",
          "in": "path",
          "required": true,
          "description": "Account identifier."
        },
        {
          "schema": {
            "type": "string"
          },
          "name": "watchlist_id",
          "in": "path",
          "required": true,
          "description": "The Watchlist ID"
        },
        {
          "schema": {
            "type": "string"
          },
          "name": "symbol",
          "in": "path",
          "required": true,
          "description": "The symbol "
        }
      ],
      "delete": {
        "summary": "Remove a Symbol from a Watchlist",
        "tags": [
          "Watchlist"
        ],
        "operationId": "delete-DELETE-v1-trading-accounts-account_id-watchlists-watchlist_id-symbol",
        "responses": {
          "200": {
            "description": "OK"
          },
          "404": {
            "description": "The requested watchlist is not found"
          }
        },
        "description": "Delete one entry for an asset by symbol name"
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
