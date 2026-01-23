---
source_view: https://docs.alpaca.markets/reference/listcryptofundingtransfers
source_md: https://docs.alpaca.markets/reference/listcryptofundingtransfers.md
scraped_at_utc: 2026-01-22T23:02:18Z
---
# Retrieve Crypto Funding Transfers

Returns an array of all transfers associated with the given account across all wallets.

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
    "/v2/wallets/transfers": {
      "get": {
        "tags": [
          "Crypto Funding"
        ],
        "summary": "Retrieve Crypto Funding Transfers",
        "description": "Returns an array of all transfers associated with the given account across all wallets.",
        "operationId": "listCryptoFundingTransfers",
        "responses": {
          "200": {
            "description": "An array of transfer objects",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "description": "Transfers allow you to transfer assets into your end customer's account (deposits) or out (withdrawal).",
                  "properties": {
                    "id": {
                      "type": "string",
                      "format": "uuid",
                      "description": "The crypto transfer ID"
                    },
                    "tx_hash": {
                      "type": "string",
                      "description": "On-chain transaction hash (e.g. 0xabc...xyz)"
                    },
                    "direction": {
                      "type": "string",
                      "example": "INCOMING",
                      "enum": [
                        "INCOMING",
                        "OUTGOING"
                      ],
                      "x-readme-ref-name": "TransferDirection"
                    },
                    "status": {
                      "type": "string",
                      "example": "PROCESSING",
                      "enum": [
                        "PROCESSING",
                        "FAILED",
                        "COMPLETE"
                      ],
                      "x-readme-ref-name": "CryptoTransferStatus"
                    },
                    "amount": {
                      "type": "string",
                      "description": "Amount of transfer denominated in the underlying crypto asset"
                    },
                    "usd_value": {
                      "type": "string",
                      "description": "Equivalent USD value at time of transfer"
                    },
                    "network_fee": {
                      "type": "string"
                    },
                    "fees": {
                      "type": "string"
                    },
                    "chain": {
                      "type": "string",
                      "description": "Underlying network for given transfer"
                    },
                    "asset": {
                      "type": "string",
                      "description": "Symbol of crypto asset for given transfer (e.g. BTC )"
                    },
                    "from_address": {
                      "type": "string",
                      "description": "Originating address of the transfer"
                    },
                    "to_address": {
                      "type": "string",
                      "description": "Destination address of the transfer"
                    },
                    "created_at": {
                      "type": "string",
                      "format": "date-time",
                      "description": "Timedate when transfer was created"
                    }
                  },
                  "x-stoplight": {
                    "id": "f986mttnx5c4n"
                  },
                  "x-readme-ref-name": "CryptoTransfer"
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
