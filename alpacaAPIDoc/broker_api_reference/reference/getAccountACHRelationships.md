---
source_view: https://docs.alpaca.markets/reference/getaccountachrelationships
source_md: https://docs.alpaca.markets/reference/getaccountachrelationships.md
scraped_at_utc: 2026-01-27T04:30:48Z
---
# Retrieve ACH Relationships for an account

Returns a list of ACH Relationships for an account

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
    "/v1/accounts/{account_id}/ach_relationships": {
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
        "summary": "Retrieve ACH Relationships for an account",
        "tags": [
          "Funding"
        ],
        "responses": {
          "200": {
            "description": "Success",
            "content": {
              "application/json": {
                "schema": {
                  "type": "array",
                  "items": {
                    "title": "ACHRelationship",
                    "type": "object",
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
                          "APPROVED",
                          "REJECTED",
                          "PENDING",
                          "CANCEL_REQUESTED"
                        ]
                      },
                      "account_owner_name": {
                        "type": "string",
                        "minLength": 1,
                        "description": "Name of the account owner"
                      },
                      "bank_account_type": {
                        "type": "string",
                        "minLength": 1,
                        "enum": [
                          "CHECKING",
                          "SAVINGS"
                        ],
                        "description": "Must be CHECKING or SAVINGS"
                      },
                      "bank_account_number": {
                        "type": "string",
                        "minLength": 1
                      },
                      "bank_routing_number": {
                        "type": "string",
                        "minLength": 1
                      },
                      "nickname": {
                        "type": "string",
                        "minLength": 1
                      }
                    },
                    "required": [
                      "id",
                      "created_at",
                      "updated_at",
                      "account_id",
                      "status",
                      "account_owner_name"
                    ],
                    "x-stoplight": {
                      "id": "013jdl3wk8c87"
                    },
                    "x-readme-ref-name": "ACHRelationship"
                  }
                }
              }
            }
          }
        },
        "operationId": "getAccountACHRelationships",
        "description": "Returns a list of ACH Relationships for an account",
        "parameters": [
          {
            "schema": {
              "type": "string"
            },
            "in": "query",
            "name": "statuses",
            "description": "Comma-separated status values"
          }
        ]
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
