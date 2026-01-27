---
source_view: https://docs.alpaca.markets/reference/createfundingwalletrecipientbank
source_md: https://docs.alpaca.markets/reference/createfundingwalletrecipientbank.md
scraped_at_utc: 2026-01-27T04:30:48Z
---
# Create a recipient bank

Creates a new recipient bank. Returns the new recipient bank entity on success. entity.

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
    "/v1beta/accounts/{account_id}/funding_wallet/recipient_bank": {
      "post": {
        "tags": [
          "Funding Wallets"
        ],
        "summary": "Create a recipient bank",
        "description": "Creates a new recipient bank. Returns the new recipient bank entity on success. entity.",
        "operationId": "createFundingWalletRecipientBank",
        "parameters": [
          {
            "name": "account_id",
            "in": "path",
            "description": "UUID alpaca account ID",
            "required": true,
            "schema": {
              "type": "string"
            }
          }
        ],
        "requestBody": {
          "content": {
            "application/json": {
              "schema": {
                "required": [
                  "bank_country",
                  "currency",
                  "bank_name",
                  "street_address",
                  "city",
                  "account_number"
                ],
                "properties": {
                  "bank_name": {
                    "type": "string"
                  },
                  "bank_account_holder_name": {
                    "type": "string",
                    "description": "Bank account holder's name."
                  },
                  "bank_country": {
                    "type": "string",
                    "description": "Two-letter code for the country in which the beneficiary's bank account is held."
                  },
                  "currency": {
                    "type": "string",
                    "description": "Currency in which money is held in the beneficiary's bank account. ISO-3 currency code."
                  },
                  "street_address": {
                    "type": "string",
                    "description": "First line of address."
                  },
                  "account_number": {
                    "type": "string",
                    "description": "Bank account number."
                  },
                  "routing_code_type": {
                    "type": "string",
                    "description": "Local payment routing system. If supplied, routing_code should also be supplied.",
                    "enum": [
                      "sort_code",
                      "aba",
                      "bsb_code",
                      "institution_no",
                      "bank_code",
                      "branch_code",
                      "clabe",
                      "cnaps",
                      "ifsc"
                    ]
                  },
                  "routing_code": {
                    "type": "string",
                    "description": "Routing code for routing_code_type. If supplied, routing_code_type should also be supplied."
                  },
                  "bic_swift": {
                    "type": "string",
                    "description": "BIC/SWIFT code"
                  },
                  "iban": {
                    "type": "string",
                    "description": "IBAN code"
                  },
                  "account_type": {
                    "type": "string",
                    "description": "Bank account type.",
                    "enum": [
                      "checking",
                      "savings"
                    ]
                  },
                  "city": {
                    "type": "string",
                    "description": "City"
                  },
                  "postal_code": {
                    "type": "string",
                    "description": "Postal code"
                  },
                  "state_or_province": {
                    "type": "string",
                    "description": "State or province."
                  }
                }
              }
            }
          }
        },
        "responses": {
          "200": {
            "description": "Success.",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "id": {
                      "type": "string",
                      "format": "uuid"
                    },
                    "first_name": {
                      "type": "string"
                    },
                    "last_name": {
                      "type": "string"
                    },
                    "company_name": {
                      "type": "string"
                    },
                    "payment_types": {
                      "type": "array",
                      "items": {
                        "type": "string",
                        "enum": [
                          "swift_wire",
                          "local_rails"
                        ],
                        "description": "Status:\n * `swift_wire`: SWIFT wire\n * `local_rails`: Local scheme\n",
                        "x-readme-ref-name": "FundingDetailPaymentType"
                      }
                    },
                    "street_address": {
                      "type": "string"
                    },
                    "country": {
                      "type": "string",
                      "description": "Two-letter ISO country code."
                    },
                    "city": {
                      "type": "string",
                      "description": "City"
                    },
                    "postal_code": {
                      "type": "string",
                      "description": "Postal code"
                    },
                    "state_or_province": {
                      "type": "string",
                      "description": "State or province."
                    },
                    "currency": {
                      "type": "string",
                      "description": "Currency in which money is held in the beneficiary's bank account. Three-digit currency code."
                    },
                    "account_number": {
                      "type": "string",
                      "description": "Bank account number."
                    },
                    "routing_code_type": {
                      "type": "string",
                      "description": "Local payment routing system."
                    },
                    "routing_code": {
                      "type": "string",
                      "description": "Value for \"routing_code_type\"."
                    },
                    "bic_swift": {
                      "type": "string",
                      "description": "BIC/SWIFT code"
                    },
                    "iban": {
                      "type": "string",
                      "description": "IBAN code"
                    },
                    "created_at": {
                      "type": "string",
                      "description": "Date the beneficiary record was created.",
                      "format": "date-time"
                    },
                    "updated_at": {
                      "type": "string",
                      "description": "Date the beneficiary record was last updated.",
                      "format": "date-time"
                    }
                  },
                  "x-readme-ref-name": "FundingWalletRecipientBank"
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
