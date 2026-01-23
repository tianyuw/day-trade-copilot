---
source_view: https://docs.alpaca.markets/reference/listcryptofundingwallets
source_md: https://docs.alpaca.markets/reference/listcryptofundingwallets.md
scraped_at_utc: 2026-01-22T23:02:18Z
---
# Retrieve Crypto Funding Wallets

Lists wallets for the account given in the path parameter. If an asset is specified and no wallet for the account and asset pair exists one will be created. If no asset is specified only existing wallets will be listed for the account. An account may have at most one wallet per asset.

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
    "/v2/wallets": {
      "parameters": [
        {
          "name": "asset",
          "in": "query",
          "schema": {
            "type": "string"
          }
        },
        {
          "name": "network",
          "in": "query",
          "description": "Optional network identifier. Use to request wallets for a specific network when asset is a multi-chain crypto asset. If not specified, the default network (ehtereum) will be used.",
          "schema": {
            "type": "string",
            "enum": [
              "ethereum",
              "solana"
            ]
          }
        }
      ],
      "get": {
        "tags": [
          "Crypto Funding"
        ],
        "summary": "Retrieve Crypto Funding Wallets",
        "description": "Lists wallets for the account given in the path parameter. If an asset is specified and no wallet for the account and asset pair exists one will be created. If no asset is specified only existing wallets will be listed for the account. An account may have at most one wallet per asset.",
        "operationId": "listCryptoFundingWallets",
        "responses": {
          "200": {
            "description": "A single wallet object if an asset is specified or an array of wallet objects if no asset is specified",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "chain": {
                      "type": "string"
                    },
                    "address": {
                      "type": "string"
                    },
                    "created_at": {
                      "type": "string",
                      "format": "date-time",
                      "description": "Timestamp (RFC3339) of account creation."
                    }
                  },
                  "x-readme-ref-name": "CryptoWallet"
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
