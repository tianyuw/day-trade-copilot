---
source_view: https://docs.alpaca.markets/reference/createrecipientbank
source_md: https://docs.alpaca.markets/reference/createrecipientbank.md
scraped_at_utc: 2026-01-27T04:30:48Z
---
# Create a Bank Relationship for an Account

If successful, retrieves Bank Relationships for an account

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
    "/v1/accounts/{account_id}/recipient_banks": {
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
        "tags": [
          "Funding",
          "Accounts"
        ],
        "summary": "Create a Bank Relationship for an Account",
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
        "requestBody": {
          "required": true,
          "content": {
            "application/json": {
              "schema": {
                "title": "CreateBankRequest",
                "type": "object",
                "description": "Represents the possible fields to send when creating a new associated Bank resource for an account",
                "x-stoplight": {
                  "id": "dqsm6v1t25vuq"
                },
                "properties": {
                  "name": {
                    "type": "string",
                    "description": "Name of recipient bank"
                  },
                  "bank_code": {
                    "type": "string",
                    "description": "9-Digit ABA RTN (Routing Number) or BIC"
                  },
                  "bank_code_type": {
                    "type": "string",
                    "enum": [
                      "ABA",
                      "BIC"
                    ],
                    "description": "ABA (Domestic) or BIC (International)"
                  },
                  "account_number": {
                    "type": "string"
                  },
                  "country": {
                    "type": "string",
                    "description": "Only for international banks, ie if bank_code_type = BIC"
                  },
                  "state_province": {
                    "type": "string",
                    "description": "Only for international banks, ie if bank_code_type = BIC"
                  },
                  "postal_code": {
                    "type": "string",
                    "description": "Only for international banks, ie if bank_code_type = BIC. Minimum of 3 characters"
                  },
                  "city": {
                    "type": "string",
                    "description": "Only for international banks, ie if bank_code_type = BIC"
                  },
                  "street_address": {
                    "type": "string",
                    "description": "Only for international banks, ie if bank_code_type = BIC"
                  }
                },
                "required": [
                  "name",
                  "bank_code",
                  "bank_code_type",
                  "account_number"
                ],
                "x-readme-ref-name": "CreateBankRequest"
              }
            }
          }
        },
        "responses": {
          "200": {
            "description": "The created Bank relationship",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "x-examples": {
                    "example-1": {
                      "id": "8475c676-68e3-4cfc-a683-9ca2f47a6172",
                      "account_id": "56712986-9ff7-4d8f-8e52-077e099e533e",
                      "name": "Bank XYZ",
                      "status": "QUEUED",
                      "country": "",
                      "state_province": "",
                      "postal_code": "",
                      "city": "",
                      "street_address": "",
                      "account_number": "123456789abc",
                      "bank_code": "123456789",
                      "bank_code_type": "ABA",
                      "created_at": "2022-02-11T21:35:19.268681613Z",
                      "updated_at": "2022-02-11T21:35:19.268681613Z"
                    }
                  },
                  "properties": {
                    "id": {
                      "type": "string",
                      "format": "uuid",
                      "example": "61e69015-8549-4bfd-b9c3-01e75843f47d"
                    },
                    "created_at": {
                      "type": "string",
                      "format": "date-time",
                      "example": "2021-03-16T18:38:01.942282Z",
                      "description": "Format: 2020-01-01T01:01:01Z"
                    },
                    "updated_at": {
                      "type": "string",
                      "format": "date-time",
                      "example": "2021-03-16T18:38:01.942282Z",
                      "description": "Format: 2020-01-01T01:01:01Z"
                    },
                    "account_id": {
                      "type": "string",
                      "format": "uuid"
                    },
                    "status": {
                      "type": "string",
                      "enum": [
                        "QUEUED",
                        "SENT_TO_CLEARING",
                        "APPROVED",
                        "REJECTED",
                        "CANCELED"
                      ],
                      "description": "QUEUED, SENT_TO_CLEARING, APPROVED, REJECTED, CANCELED"
                    },
                    "name": {
                      "type": "string",
                      "description": "Name of recipient bank"
                    },
                    "bank_code": {
                      "type": "string",
                      "description": "9-Digit ABA RTN (Routing Number) or BIC"
                    },
                    "bank_code_type": {
                      "type": "string",
                      "enum": [
                        "ABA",
                        "BIC"
                      ],
                      "description": "ABA (Domestic) or BIC (International)"
                    },
                    "country": {
                      "type": "string",
                      "description": "Only for international banks"
                    },
                    "state_province": {
                      "type": "string",
                      "description": "Only for international banks"
                    },
                    "postal_code": {
                      "type": "string",
                      "description": "Only for international banks"
                    },
                    "city": {
                      "type": "string",
                      "description": "Only for international banks"
                    },
                    "street_address": {
                      "type": "string",
                      "description": "Only for international banks"
                    },
                    "account_number": {
                      "type": "string"
                    }
                  },
                  "required": [
                    "id",
                    "created_at",
                    "updated_at",
                    "name",
                    "bank_code",
                    "bank_code_type",
                    "account_number"
                  ],
                  "x-stoplight": {
                    "id": "zb27jqls868ez"
                  },
                  "x-readme-ref-name": "Bank"
                }
              }
            }
          },
          "400": {
            "description": "Bad Request"
          },
          "409": {
            "description": "A Bank relationship already exists for this account"
          }
        },
        "operationId": "createRecipientBank",
        "description": "If successful, retrieves Bank Relationships for an account"
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
