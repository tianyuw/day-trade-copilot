---
source_view: https://docs.alpaca.markets/reference/optionexercise
source_md: https://docs.alpaca.markets/reference/optionexercise.md
scraped_at_utc: 2026-01-22T23:02:18Z
---
# Exercise an Options Position

This endpoint enables users to exercise a held option contract, converting it into the underlying asset based on the specified terms.
All available held shares of this option contract will be exercised.
By default, Alpaca will automatically exercise in-the-money (ITM) contracts at expiry.
Exercise requests will be processed immediately once received. Exercise requests submitted between market close and midnight will be rejected to avoid any confusion about when the exercise will settle.
To cancel an exercise request or to submit a Do-not-exercise (DNE) instruction, you can use the do-not-exercise endpoint or contact our support team.

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
    "/v2/positions/{symbol_or_contract_id}/exercise": {
      "post": {
        "tags": [
          "Positions"
        ],
        "summary": "Exercise an Options Position",
        "description": "This endpoint enables users to exercise a held option contract, converting it into the underlying asset based on the specified terms.\nAll available held shares of this option contract will be exercised.\nBy default, Alpaca will automatically exercise in-the-money (ITM) contracts at expiry.\nExercise requests will be processed immediately once received. Exercise requests submitted between market close and midnight will be rejected to avoid any confusion about when the exercise will settle.\nTo cancel an exercise request or to submit a Do-not-exercise (DNE) instruction, you can use the do-not-exercise endpoint or contact our support team.",
        "operationId": "optionExercise",
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
            "description": "Successful Response\n\nExercise instruction successfully submitted."
          },
          "403": {
            "description": "Forbidden\n\nAvailable position quantity is not sufficient.",
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
                      "message": "cannot exercise short position"
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
