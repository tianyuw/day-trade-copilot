---
source_view: https://docs.alpaca.markets/reference/deletewhitelistedaddress
source_md: https://docs.alpaca.markets/reference/deletewhitelistedaddress.md
scraped_at_utc: 2026-01-22T23:02:18Z
---
# Delete a whitelisted address

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
      "name": "Crypto Funding"
    }
  ],
  "paths": {
    "/v2/wallets/whitelists/{whitelisted_address_id}": {
      "parameters": [
        {
          "schema": {
            "type": "string"
          },
          "name": "whitelisted_address_id",
          "in": "path",
          "required": true,
          "description": "The whitelisted address to delete"
        }
      ],
      "delete": {
        "tags": [
          "Crypto Funding"
        ],
        "summary": "Delete a whitelisted address",
        "operationId": "deleteWhitelistedAddress",
        "responses": {
          "200": {
            "description": "Successfully deleted a whitelisted address"
          }
        }
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
