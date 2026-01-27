---
source_view: https://docs.alpaca.markets/reference/createachrelationshipforaccount
source_md: https://docs.alpaca.markets/reference/createachrelationshipforaccount.md
scraped_at_utc: 2026-01-27T04:30:48Z
---
# Create an ACH Relationship

Create a new ACHRelationship for an account

If successful, will return 200 code with a newly created ACH Relationship entity.

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
      "post": {
        "summary": "Create an ACH Relationship",
        "operationId": "createACHRelationshipForAccount",
        "responses": {
          "200": {
            "description": "returns the newly created ACH Relationship entity.",
            "content": {
              "application/json": {
                "schema": {
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
          },
          "400": {
            "description": "Malformed input.",
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
          },
          "401": {
            "description": "Client is not authorized for this operation.",
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
          },
          "409": {
            "description": "The account already has an active relationship.",
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
        },
        "description": "Create a new ACHRelationship for an account\n\nIf successful, will return 200 code with a newly created ACH Relationship entity.",
        "requestBody": {
          "required": true,
          "content": {
            "application/json": {
              "schema": {
                "description": "Represents the fields used in creation of a new ACHRelationship.\n\nYou can create an ACHRelationship by passing the required fields here or if you have an account with Plaid you can use our integration with Plaid to create a relationship.\n\nPlease see the documentation [here](https://alpaca.markets/docs/api-references/broker-api/funding/ach/#plaid-integration-for-bank-transfers) for more info on using Plaid with Alpaca",
                "type": "object",
                "title": "CreateACHRelationshipRequest",
                "x-stoplight": {
                  "id": "2vv9f2s2sc8om"
                },
                "properties": {
                  "account_owner_name": {
                    "type": "string",
                    "minLength": 1
                  },
                  "bank_account_type": {
                    "type": "string",
                    "minLength": 1,
                    "enum": [
                      "CHECKING",
                      "SAVINGS"
                    ],
                    "description": "Must be `CHECKING` or `SAVINGS`"
                  },
                  "bank_account_number": {
                    "type": "string",
                    "minLength": 1,
                    "description": "In sandbox, this still must be a valid format"
                  },
                  "bank_routing_number": {
                    "type": "string",
                    "minLength": 1,
                    "description": "In sandbox, this still must be a valid format"
                  },
                  "nickname": {
                    "type": "string",
                    "minLength": 1
                  },
                  "processor_token": {
                    "type": "string",
                    "description": "If using Plaid, you can specify a Plaid processor token here "
                  },
                  "instant": {
                    "type": "boolean",
                    "x-stoplight": {
                      "id": "zs4ueaei5ins9"
                    }
                  }
                },
                "required": [
                  "account_owner_name",
                  "bank_account_type",
                  "bank_account_number",
                  "bank_routing_number"
                ],
                "x-readme-ref-name": "CreateACHRelationshipRequest"
              }
            }
          },
          "description": "Create ACH Relationship "
        },
        "tags": [
          "Funding"
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
