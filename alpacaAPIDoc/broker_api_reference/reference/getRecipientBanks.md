---
source_view: https://docs.alpaca.markets/reference/getrecipientbanks
source_md: https://docs.alpaca.markets/reference/getrecipientbanks.md
scraped_at_utc: 2026-01-27T04:30:48Z
---
# Retrieve Bank Relationships for an Account

Retrieves Bank Relationships for an account

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
      "get": {
        "tags": [
          "Funding",
          "Accounts"
        ],
        "summary": "Retrieve Bank Relationships for an Account",
        "parameters": [
          {
            "name": "status",
            "in": "query",
            "schema": {
              "type": "string",
              "enum": [
                "ACTIVE",
                "INACTIVE"
              ],
              "example": "ACTIVE"
            }
          },
          {
            "name": "bank_name",
            "in": "query",
            "schema": {
              "type": "string"
            }
          }
        ],
        "responses": {
          "200": {
            "description": "An array of Bank relationships attached to this Account.\n\nAn empty array will be returned if no Bank relationships have been attached to this account",
            "content": {
              "application/json": {
                "schema": {
                  "type": "array",
                  "items": {
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
            }
          },
          "400": {
            "description": "Bad request. The body in the request is not valid."
          }
        },
        "operationId": "getRecipientBanks",
        "description": "Retrieves Bank Relationships for an account"
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
