---
source_view: https://docs.alpaca.markets/reference/getfundingwallettransferbyid
source_md: https://docs.alpaca.markets/reference/getfundingwallettransferbyid.md
scraped_at_utc: 2026-01-27T04:30:48Z
---
# Retrieve funding wallet transfer by ID

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
      "name": "Funding Wallets"
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
    "/v1beta/accounts/{account_id}/funding_wallet/transfers/{transfer_id}": {
      "get": {
        "tags": [
          "Funding Wallets"
        ],
        "summary": "Retrieve funding wallet transfer by ID",
        "operationId": "getFundingWalletTransferByID",
        "parameters": [
          {
            "name": "account_id",
            "in": "path",
            "description": "Alpaca account UUID",
            "required": true,
            "schema": {
              "type": "string"
            }
          },
          {
            "name": "transfer_id",
            "in": "path",
            "description": "transfer UUID",
            "required": true,
            "schema": {
              "type": "string"
            }
          }
        ],
        "responses": {
          "200": {
            "description": "transfer response if found",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "id": {
                      "type": "string",
                      "format": "uuid"
                    },
                    "account_id": {
                      "type": "string",
                      "format": "uuid"
                    },
                    "fees": {
                      "type": "array",
                      "items": {
                        "type": "object",
                        "required": [
                          "type",
                          "amount",
                          "currency",
                          "payment_type"
                        ],
                        "properties": {
                          "type": {
                            "type": "string",
                            "enum": [
                              "withdrawal_fee",
                              "fx_fee",
                              "network_fee",
                              "deposit_fee",
                              "ach_return_fee",
                              "parnter_fee",
                              "alpaca_fee"
                            ],
                            "description": "Status:\n  * `withdrawal_fee`: Withdrawal fee\n  * `fx_fee`: FX Fee\n  * `network_fee`\n  * `deposit_fee`\n  * `ach_return_fee`\n  * `parnter_fee`\n  * `alpaca_fee`\n",
                            "x-readme-ref-name": "FeeType"
                          },
                          "amount": {
                            "type": "string",
                            "nullable": false,
                            "format": "decimal"
                          },
                          "currency": {
                            "title": "Currency",
                            "x-stoplight": {
                              "id": "go8dbrpz277wf"
                            },
                            "type": "string",
                            "description": "\"USD\" // US Dollar\n\"JPY\" // Japanese Yen\n\"EUR\" // Euro\n\"CAD\" // Canadian Dollar\n\"GBP\" // British Pound Sterling\n\"CHF\" // Swiss Franc\n\"TRY\" // Turkish Lira\n\"AUD\" // Australian Dollar\n\"CZK\" // Czech Koruna\n\"SEK\" // Swedish Krona\n\"DKK\" // Danish Krone\n\"SGD\" // Singapore Dollar\n\"HKD\" // Hong Kong Dollar\n\"HUF\" // Hungarian Forint\n\"NZD\" // New Zealand Dollar\n\"NOK\" // Norwegian Krone\n\"PLN\" // Poland Złoty",
                            "x-readme-ref-name": "Currency"
                          },
                          "payment_type": {
                            "type": "string",
                            "enum": [
                              "invoice"
                            ],
                            "description": "Status:\n * `invoice`\n",
                            "x-readme-ref-name": "FeePaymentType"
                          }
                        },
                        "x-readme-ref-name": "TransferFee"
                      }
                    },
                    "requested_amount": {
                      "type": "string",
                      "format": "decimal",
                      "description": "The amount sent as part of the withdrawal creation"
                    },
                    "original_amount": {
                      "type": "string",
                      "format": "decimal",
                      "description": "The amount you should expect to receive, calculated as requested amount - fees"
                    },
                    "original_currency": {
                      "type": "string",
                      "description": "The currency of the withdrawn amount, 3-letter ISO code"
                    },
                    "direction": {
                      "type": "string",
                      "enum": [
                        "incoming",
                        "outgoing"
                      ],
                      "description": "Status:\n * `incoming`: incoming amount\n * `outgoing`: outgoing amount\n",
                      "x-readme-ref-name": "FundingWalletTransferDirection"
                    },
                    "status": {
                      "type": "string",
                      "enum": [
                        "PENDING",
                        "CANCELED",
                        "EXECUTED",
                        "FAILED",
                        "COMPLETE"
                      ],
                      "description": "Status:\n * `PENDING`: Created and waiting to be processed\n * `CANCELED`: Canceled\n * `FAILED`: Failed mostly due to technical reasons\n * `COMPLETE`: Transfer has settled\n",
                      "x-readme-ref-name": "FundingWalletTransferStatus"
                    },
                    "created_at": {
                      "type": "string",
                      "format": "date-time"
                    },
                    "updated_at": {
                      "type": "string",
                      "format": "date-time"
                    },
                    "usd": {
                      "type": "object",
                      "required": [
                        "amount"
                      ],
                      "properties": {
                        "amount": {
                          "type": "string",
                          "nullable": false,
                          "format": "decimal"
                        }
                      },
                      "x-readme-ref-name": "Usd"
                    },
                    "payment_type": {
                      "type": "string",
                      "enum": [
                        "swift_wire",
                        "local_rails"
                      ],
                      "description": "Status:\n * `swift_wire`: SWIFT wire\n * `local_rails`: Local scheme\n",
                      "x-readme-ref-name": "FundingDetailPaymentType"
                    }
                  },
                  "x-readme-ref-name": "FundingWalletTransfer"
                }
              }
            }
          },
          "404": {
            "description": "error response if transfer is not found"
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
