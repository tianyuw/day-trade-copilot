---
source_view: https://docs.alpaca.markets/reference/listwhitelistedaddress
source_md: https://docs.alpaca.markets/reference/listwhitelistedaddress.md
scraped_at_utc: 2026-01-22T23:02:18Z
---
# An array of whitelisted addresses

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
    "/v2/wallets/whitelists": {
      "get": {
        "tags": [
          "Crypto Funding"
        ],
        "summary": "An array of whitelisted addresses",
        "operationId": "listWhitelistedAddress",
        "responses": {
          "200": {
            "description": "An array of whitelisted objects",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "id": {
                      "type": "string",
                      "description": "Unique ID for whitelisted address"
                    },
                    "chain": {
                      "type": "string",
                      "description": "Underlying network this address represents"
                    },
                    "asset": {
                      "type": "string",
                      "description": "Symbol of underlying asset for the whitelisted address"
                    },
                    "address": {
                      "type": "string",
                      "description": "The whitelisted address"
                    },
                    "status": {
                      "type": "string",
                      "description": "Status of whitelisted address which is either ACTIVE or PENDING. Whitelisted addresses will be subjected to a 24 waiting period. After the waiting period is over the status will become ACTIVE.",
                      "enum": [
                        "APPROVED",
                        "PENDING"
                      ]
                    },
                    "created_at": {
                      "type": "string",
                      "format": "date-time",
                      "description": "Timestamp (RFC3339) of account creation."
                    }
                  },
                  "x-readme-ref-name": "WhitelistedAddress"
                }
              }
            }
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
