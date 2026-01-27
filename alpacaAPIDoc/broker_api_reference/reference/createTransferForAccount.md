---
source_view: https://docs.alpaca.markets/reference/createtransferforaccount
source_md: https://docs.alpaca.markets/reference/createtransferforaccount.md
scraped_at_utc: 2026-01-27T04:30:48Z
---
# Request a New Transfer

Create a new transfer to an account to fund it.

In the sandbox environment, you can instantly deposit to or withdraw from an account with a virtual money amount. In the production environment, this endpoint is used only for requesting an outgoing (withdrawal) wire transfer at this moment. For the wire transfer (in production), you need to create a bank resource first using the Bank API. For more on how to fund an account in sandbox please check out this tutorial [here](https://alpaca.markets/learn/fund-broker-api/).

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
      "name": "Accounts"
    },
    {
      "name": "Funding"
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
    "/v1/accounts/{account_id}/transfers": {
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
      "post": {
        "summary": "Request a New Transfer",
        "tags": [
          "Funding",
          "Accounts"
        ],
        "description": "Create a new transfer to an account to fund it.\n\nIn the sandbox environment, you can instantly deposit to or withdraw from an account with a virtual money amount. In the production environment, this endpoint is used only for requesting an outgoing (withdrawal) wire transfer at this moment. For the wire transfer (in production), you need to create a bank resource first using the Bank API. For more on how to fund an account in sandbox please check out this tutorial [here](https://alpaca.markets/learn/fund-broker-api/).",
        "parameters": [
          {
            "name": "account_id",
            "in": "path",
            "required": true,
            "schema": {
              "type": "string",
              "format": "uuid"
            }
          }
        ],
        "requestBody": {
          "required": true,
          "content": {
            "application/json": {
              "schema": {
                "title": "CreateTransferRequest",
                "type": "object",
                "description": "[See main docs here](https://alpaca.markets/docs/api-references/broker-api/funding/transfers/#creating-a-transfer-entity)",
                "x-stoplight": {
                  "id": "p5r8jvdp1gmvw"
                },
                "properties": {
                  "transfer_type": {
                    "type": "string",
                    "example": "ach",
                    "enum": [
                      "ach",
                      "wire"
                    ],
                    "description": "**NOTE:** The Sandbox environment currently only supports `ach`\n\n- **ach**\nTransfer via ACH (US Only).\n- **wire**\nTransfer via wire (international).\n",
                    "title": "TransferType",
                    "x-stoplight": {
                      "id": "bn365jqublfc6"
                    },
                    "x-readme-ref-name": "TransferType"
                  },
                  "relationship_id": {
                    "type": "string",
                    "format": "uuid",
                    "description": "Required if type = `ach`\n\nThe ach_relationship created for the account_id [here](https://alpaca.markets/docs/api-references/broker-api/funding/ach/#creating-an-ach-relationship)"
                  },
                  "bank_id": {
                    "type": "string",
                    "format": "uuid",
                    "description": "Required if type = `wire`\n\nThe bank_relationship created for the account_id [here](https://alpaca.markets/docs/api-references/broker-api/funding/bank/#creating-a-new-bank-relationship)"
                  },
                  "amount": {
                    "type": "string",
                    "format": "decimal",
                    "description": "Must be > 0.00"
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
                  "timing": {
                    "type": "string",
                    "example": "immediate",
                    "enum": [
                      "immediate"
                    ],
                    "description": "Only `immediate` is currently supported.\n\nvalues:\n\n- **immediate**\n\n- **next_day**",
                    "x-stoplight": {
                      "id": "v6623fj1j3umc"
                    },
                    "x-readme-ref-name": "TransferTiming"
                  },
                  "additional_information": {
                    "type": "string",
                    "description": "Additional details for when type = `wire`",
                    "nullable": true
                  },
                  "fee_payment_method": {
                    "title": "FeePaymentMethod",
                    "x-stoplight": {
                      "id": "ycxjjvxcdifuc"
                    },
                    "type": "string",
                    "description": "Only outgoing wire fees are currently supported for automated processing.\n\n\n**user**\tThe end user will pay any applicable fees\n**invoice**\tAny applicable fees will be billed to the client in the following monthly invoice",
                    "x-readme-ref-name": "FeePaymentMethod"
                  },
                  "ira": {
                    "description": "This field is used for IRA Account only",
                    "type": "object",
                    "properties": {
                      "tax_year": {
                        "type": "string",
                        "example": "2024"
                      },
                      "distribution_reason": {
                        "type": "string",
                        "example": "normal"
                      },
                      "tax_withholding": {
                        "type": "object",
                        "properties": {
                          "fed_pct": {
                            "type": "string",
                            "example": "10.25"
                          },
                          "state_pct": {
                            "type": "string",
                            "example": "8.25"
                          }
                        },
                        "x-readme-ref-name": "TransferIRATaxWithholding"
                      }
                    },
                    "x-readme-ref-name": "TransferIRA"
                  }
                },
                "required": [
                  "transfer_type",
                  "amount",
                  "direction",
                  "timing"
                ],
                "x-readme-ref-name": "CreateTransferRequest"
              }
            }
          }
        },
        "responses": {
          "200": {
            "description": "Successfully requested a transfer.",
            "content": {
              "application/json": {
                "schema": {
                  "title": "Transfer",
                  "type": "object",
                  "x-examples": {
                    "example-1": {
                      "id": "497f6eca-6276-4993-bfeb-53cbbbba6f08",
                      "relationship_id": "81412018-ffa2-43f9-a3eb-d39f1c5e0f87",
                      "bank_id": "f1ae96de-94c1-468e-93a3-6b7213930ca8",
                      "account_id": "449e7a5c-69d3-4b8a-aaaf-5c9b713ebc65",
                      "type": "ach",
                      "status": "QUEUED",
                      "reason": "string",
                      "amount": "string",
                      "direction": "INCOMING",
                      "created_at": "2019-08-24T14:15:22Z",
                      "updated_at": "2019-08-24T14:15:22Z",
                      "expires_at": "2019-08-24T14:15:22Z",
                      "additional_information": "string",
                      "ira": {
                        "tax_year": "2024",
                        "fed_withholding_pct": "10.25",
                        "fed_withholding_amount": "102.5",
                        "state_withholding_pct": "9.75",
                        "state_withholding_amount": "97.5",
                        "distribution_reason": "normal"
                      }
                    }
                  },
                  "description": "Transfers allow you to transfer money/balance into your end customers' account (deposits) or out (withdrawal).\n\n[Main docs here](https://alpaca.markets/docs/api-references/broker-api/funding/transfers/#the-transfer-object)",
                  "properties": {
                    "id": {
                      "type": "string",
                      "format": "uuid",
                      "description": "The transfer ID"
                    },
                    "relationship_id": {
                      "type": "string",
                      "format": "uuid",
                      "description": "The ACH relationship ID only present if type = \"ach\""
                    },
                    "bank_id": {
                      "type": "string",
                      "format": "uuid",
                      "description": "The ID of the Bank, only present if type = \"wire\""
                    },
                    "account_id": {
                      "type": "string",
                      "format": "uuid",
                      "description": "The account ID"
                    },
                    "type": {
                      "type": "string",
                      "example": "ach",
                      "enum": [
                        "ach",
                        "wire"
                      ],
                      "description": "**NOTE:** The Sandbox environment currently only supports `ach`\n\n- **ach**\nTransfer via ACH (US Only).\n- **wire**\nTransfer via wire (international).\n",
                      "title": "TransferType",
                      "x-stoplight": {
                        "id": "bn365jqublfc6"
                      },
                      "x-readme-ref-name": "TransferType"
                    },
                    "status": {
                      "type": "string",
                      "example": "QUEUED",
                      "enum": [
                        "QUEUED",
                        "APPROVAL_PENDING",
                        "PENDING",
                        "SENT_TO_CLEARING",
                        "REJECTED",
                        "CANCELED",
                        "APPROVED",
                        "COMPLETE",
                        "RETURNED"
                      ],
                      "description": "- **QUEUED**\nTransfer is in queue to be processed.\n- **APPROVAL_PENDING**\nTransfer is pending approval.\n- **PENDING**\nTransfer is pending processing.\n- **SENT_TO_CLEARING**\nTransfer is being processed by the clearing firm.\n- **REJECTED**\nTransfer is rejected.\n- **CANCELED**\nClient initiated transfer cancellation.\n- **APPROVED**\nTransfer is approved.\n- **COMPLETE**\nTransfer is completed.\n- **RETURNED**\nThe bank issued an ACH return for the transfer.\n",
                      "x-stoplight": {
                        "id": "mqx0hpg6h25vt"
                      },
                      "x-readme-ref-name": "TransferStatus"
                    },
                    "reason": {
                      "type": "string",
                      "description": "Cause of the status",
                      "nullable": true
                    },
                    "amount": {
                      "type": "string",
                      "description": "Must be > 0.00",
                      "format": "decimal"
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
                    "created_at": {
                      "type": "string",
                      "format": "date-time",
                      "description": "Timedate when transfer was created"
                    },
                    "updated_at": {
                      "type": "string",
                      "format": "date-time",
                      "description": "Timedate when transfer was updated"
                    },
                    "expires_at": {
                      "type": "string",
                      "format": "date-time",
                      "description": "Timedate when transfer was expired"
                    },
                    "additional_information": {
                      "type": "string",
                      "description": "Additional information. Only applies when type = \"wire\".",
                      "nullable": true
                    },
                    "hold_until": {
                      "type": "string",
                      "format": "date-time"
                    },
                    "instant_amount": {
                      "type": "string"
                    },
                    "requested_amount": {
                      "type": "string",
                      "description": "Must be > 0.00. Only applies when type = \"wire\".",
                      "format": "decimal",
                      "nullable": true
                    },
                    "fee": {
                      "type": "string",
                      "description": "Fee amount to be collected. Only applies when type = \"wire\".",
                      "format": "decimal",
                      "nullable": true
                    },
                    "fee_payment_method": {
                      "type": "string",
                      "description": "Either \"user\" or \"invoice\". Only applies when type = \"wire\".",
                      "nullable": true
                    },
                    "ira": {
                      "type": "object",
                      "properties": {
                        "tax_year": {
                          "type": "string",
                          "example": "2024"
                        },
                        "fed_withholding_pct": {
                          "type": "string",
                          "example": "10.25"
                        },
                        "fed_withholding_amount": {
                          "type": "string",
                          "example": "102.5"
                        },
                        "state_withholding_pct": {
                          "type": "string",
                          "example": "9.75"
                        },
                        "state_withholding_amount": {
                          "type": "string",
                          "example": "97.5"
                        },
                        "distribution_reason": {
                          "type": "string",
                          "example": "normal"
                        }
                      },
                      "x-readme-ref-name": "TransferIRADetails"
                    }
                  },
                  "required": [
                    "id",
                    "account_id",
                    "type",
                    "status",
                    "amount",
                    "direction",
                    "created_at"
                  ],
                  "x-stoplight": {
                    "id": "f986mttnx5c4n"
                  },
                  "x-readme-ref-name": "Transfer"
                }
              }
            }
          }
        },
        "operationId": "createTransferForAccount"
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
