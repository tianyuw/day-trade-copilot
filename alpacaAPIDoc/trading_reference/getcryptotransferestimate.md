---
source_view: https://docs.alpaca.markets/reference/getcryptotransferestimate
source_md: https://docs.alpaca.markets/reference/getcryptotransferestimate.md
scraped_at_utc: 2026-01-22T23:02:18Z
---
# Returns the estimated gas fee for a proposed transaction.

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
    "/v2/wallets/fees/estimate": {
      "get": {
        "tags": [
          "Crypto Funding"
        ],
        "summary": "Returns the estimated gas fee for a proposed transaction.",
        "operationId": "getCryptoTransferEstimate",
        "parameters": [
          {
            "name": "asset",
            "in": "query",
            "description": "The asset for the proposed transaction",
            "schema": {
              "type": "string"
            }
          },
          {
            "name": "from_address",
            "in": "query",
            "description": "The originating address of the proposed transaction",
            "schema": {
              "type": "string"
            }
          },
          {
            "name": "to_address",
            "in": "query",
            "description": "The destination address of the proposed transaction",
            "schema": {
              "type": "string"
            }
          },
          {
            "name": "amount",
            "in": "query",
            "description": "The amount, denoted in the specified asset, of the proposed transaction",
            "schema": {
              "type": "string"
            }
          }
        ],
        "responses": {
          "200": {
            "description": "OK",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "fee": {
                      "type": "string"
                    }
                  }
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
