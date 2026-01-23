---
source_view: https://docs.alpaca.markets/reference/optiondonotexercise
source_md: https://docs.alpaca.markets/reference/optiondonotexercise.md
scraped_at_utc: 2026-01-22T23:02:18Z
---
# Do Not Exercise an Options Position

This endpoint enables users to submit a do-not-exercise (DNE) instruction for a held option contract, preventing automatic exercise at expiry.
By default, Alpaca will automatically exercise in-the-money (ITM) contracts at expiry. This endpoint allows users to override that behavior.
To override this behavior and submit an exercise instruction, please contact our support team.

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
      "name": "Positions"
    }
  ],
  "paths": {
    "/v2/positions/{symbol_or_contract_id}/do-not-exercise": {
      "post": {
        "tags": [
          "Positions"
        ],
        "summary": "Do Not Exercise an Options Position",
        "description": "This endpoint enables users to submit a do-not-exercise (DNE) instruction for a held option contract, preventing automatic exercise at expiry.\nBy default, Alpaca will automatically exercise in-the-money (ITM) contracts at expiry. This endpoint allows users to override that behavior.\nTo override this behavior and submit an exercise instruction, please contact our support team.",
        "operationId": "optionDoNotExercise",
        "parameters": [
          {
            "schema": {
              "type": "string",
              "format": "uuid"
            },
            "name": "symbol_or_contract_id",
            "in": "path",
            "required": true,
            "description": "Option contract symbol or ID."
          }
        ],
        "requestBody": {
          "description": "Empty request body",
          "content": {}
        },
        "responses": {
          "200": {
            "description": "Successful Response\n\nDo-not-exercise instruction successfully submitted."
          },
          "403": {
            "description": "Forbidden\n\nAvailable position quantity is not sufficient or no position found.",
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
                  "x-readme-ref-name": "Error"
                },
                "examples": {
                  "No Available Position": {
                    "value": {
                      "code": 40310000,
                      "message": "no available position for the specified contract"
                    }
                  },
                  "Short Position": {
                    "value": {
                      "code": 40310001,
                      "message": "cannot submit DNE for short position"
                    }
                  }
                }
              }
            }
          },
          "422": {
            "description": "Invalid Parameters.\n\nOne or more parameters provided are invalid.",
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
                  "x-readme-ref-name": "Error"
                },
                "examples": {
                  "Invalid Symbol": {
                    "value": {
                      "code": 42210000,
                      "message": "invalid symbol"
                    }
                  }
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
