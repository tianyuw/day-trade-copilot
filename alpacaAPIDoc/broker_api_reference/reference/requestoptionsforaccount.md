---
source_view: https://docs.alpaca.markets/reference/requestoptionsforaccount
source_md: https://docs.alpaca.markets/reference/requestoptionsforaccount.md
scraped_at_utc: 2026-01-27T04:30:48Z
---
# Request options trading for an account (BETA)

This endpoint requests options trading for an account.
Following submission, an assigned administrator will review the request.
Upon approval, the account's options_approved_level parameter will be modified, granting the account the ability to participate in options trading.
Note: This endpoint is only available for partners who have been enabled for Options BETA.

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
    "/v1/accounts/{account_id}/options/approval": {
      "post": {
        "tags": [
          "Accounts"
        ],
        "summary": "Request options trading for an account (BETA)",
        "description": "This endpoint requests options trading for an account.\nFollowing submission, an assigned administrator will review the request.\nUpon approval, the account's options_approved_level parameter will be modified, granting the account the ability to participate in options trading.\nNote: This endpoint is only available for partners who have been enabled for Options BETA.",
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
                "type": "object",
                "properties": {
                  "level": {
                    "type": "integer",
                    "description": "The desired option trading level. 1=Covered Call/Cash-Secured Put, 2=Long Call/Put, 3=Spreads/Straddles.",
                    "enum": [
                      1,
                      2,
                      3
                    ],
                    "example": 3
                  }
                },
                "x-readme-ref-name": "OptionsApprovalRequest"
              }
            }
          }
        },
        "responses": {
          "200": {
            "description": "The request was submitted successfully.",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "id": {
                      "type": "string",
                      "format": "uuid",
                      "description": "The request ID.",
                      "example": "88b5f678-fef5-447b-af15-f21e367e6d8c"
                    },
                    "account_id": {
                      "type": "string",
                      "format": "uuid",
                      "description": "The account ID.",
                      "example": "c8f1ef5d-edc0-4f23-9ee4-378f19cb92a4"
                    },
                    "created_at": {
                      "type": "string",
                      "format": "date-time",
                      "description": "The time when the request was submitted.",
                      "example": "2021-03-16T18:38:01.942282Z"
                    },
                    "updated_at": {
                      "type": "string",
                      "format": "date-time",
                      "description": "The time when the request was last updated.",
                      "example": "2021-03-16T18:38:01.942282Z"
                    },
                    "requested_level": {
                      "type": "integer",
                      "description": "The request option trading level. 0=Disabled, 1=Covered Call/Cash-Secured Put, 2=Long Call/Put, 3=Spreads/Straddles.",
                      "enum": [
                        0,
                        1,
                        2,
                        3
                      ],
                      "example": 3
                    },
                    "approved_level": {
                      "type": "integer",
                      "description": "The option trading level approved for this request. Only present once the request has completed processiing.\nNote that a subsequent request may be approved for a different level.\n0=Disabled, 1=Covered Call/Cash-Secured Put, 2=Long Call/Put, 3=Spreads/Straddles.\"\n",
                      "enum": [
                        0,
                        1,
                        2,
                        3
                      ],
                      "example": 3
                    },
                    "status": {
                      "type": "string",
                      "description": "The request status.\n- PENDING: The request is under review.\n- APPROVED: The request has been successfully approved, the account is now able to trade options.\n- LOWER_LEVEL_APPROVED: The request has been approved for a level lower than the requested one.\n- REJECTED: The request has been rejected.\n",
                      "enum": [
                        "PENDING",
                        "APPROVED",
                        "LOWER_LEVEL_APPROVED",
                        "REJECTED"
                      ],
                      "example": "PENDING",
                      "x-readme-ref-name": "OptionsApprovalStatus"
                    },
                    "requester": {
                      "type": "string",
                      "description": "The requester of the options approval request.",
                      "enum": [
                        "CORRESPONDENT",
                        "ALPACA_ADMIN"
                      ],
                      "example": "CORRESPONDENT"
                    }
                  },
                  "x-readme-ref-name": "OptionsApprovalResponse"
                }
              }
            }
          },
          "400": {
            "description": "The request body is invalid.",
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
            "description": "Client does not exist, you do not have access to the client, or “client_secret” is incorrect.\n",
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
          "422": {
            "description": "The request body did not pass all validations.",
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
        "operationId": "requestOptionsForAccount"
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
