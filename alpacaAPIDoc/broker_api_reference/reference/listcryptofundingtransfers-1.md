---
source_view: https://docs.alpaca.markets/reference/listcryptofundingtransfers-1
source_md: https://docs.alpaca.markets/reference/listcryptofundingtransfers-1.md
scraped_at_utc: 2026-01-27T04:30:48Z
---
# Retrieve Crypto Funding Transfers

Returns an array of all transfers associated with the given account across all wallets.

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
      "name": "Crypto Funding"
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
    "/v1/accounts/{account_id}/wallets/transfers": {
      "parameters": [
        {
          "name": "account_id",
          "in": "path",
          "required": true,
          "description": "Account identifier.",
          "schema": {
            "type": "string",
            "format": "uuid"
          }
        }
      ],
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
                      "description": "- **INCOMING**\nFunds incoming to user’s account (deposit).\n- **OUTGOING**\nFunds outgoing from user’s account (withdrawal).\n",
                      "x-stoplight": {
                        "id": "mda3ylkcj1ceo"
                      },
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
          },
          "default": {
            "description": "error",
            "content": {
              "application/json": {
                "schema": {
                  "title": "Error",
                  "type": "object",
                  "properties": {
                    "code": {
                      "type": "number"
                    },
                    "message": {
                      "type": "string"
                    }
                  },
                  "required": [
                    "code",
                    "message"
                  ],
                  "x-stoplight": {
                    "id": "xu9mkrgjdtotd"
                  },
                  "x-readme-ref-name": "Error"
                }
              }
            }
          }
        }
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
