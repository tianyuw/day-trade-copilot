---
source_view: https://docs.alpaca.markets/reference/patch-v1-accounts-account_id-onfido-sdk
source_md: https://docs.alpaca.markets/reference/patch-v1-accounts-account_id-onfido-sdk.md
scraped_at_utc: 2026-01-27T04:30:48Z
---
# Update the Onfido SDK Outcome

This request allows you to send Alpaca the result of the Onfido SDK flow in your app. A notification of a successful outcome is required for Alpaca to continue the KYC process.

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
      "name": "KYC"
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
    "/v1/accounts/{account_id}/onfido/sdk": {
      "parameters": [
        {
          "schema": {
            "type": "string"
          },
          "name": "account_id",
          "in": "path",
          "required": true
        }
      ],
      "patch": {
        "summary": "Update the Onfido SDK Outcome",
        "operationId": "patch-v1-accounts-account_id-onfido-sdk",
        "responses": {
          "200": {
            "description": "OK"
          },
          "404": {
            "description": "Account Not Found​"
          },
          "422": {
            "description": "Invalid input value for outcome."
          }
        },
        "description": "This request allows you to send Alpaca the result of the Onfido SDK flow in your app. A notification of a successful outcome is required for Alpaca to continue the KYC process.",
        "requestBody": {
          "content": {
            "application/json": {
              "schema": {
                "type": "object",
                "x-examples": {
                  "Example 1": {
                    "outcome": "USER_EXITED",
                    "reason": "User denied consent",
                    "token": "header.payload.signature"
                  }
                },
                "properties": {
                  "outcome": {
                    "title": "OnfidoSDKOutcome",
                    "x-stoplight": {
                      "id": "gasz29uxpmhoo"
                    },
                    "type": "string",
                    "description": "\"NOT_STARTED\"\tThe user has not started the SDK flow yet. outcome is set to this default value upon token generation\n\"USER_EXITED\"\tThe user exited the SDK flow\n\"SDK_ERROR\"\tAn error occurred in the SDK flow\n\"USER_COMPLETED\"\tThe user completed the SDK flow",
                    "x-readme-ref-name": "OnfidoSDKOutcome"
                  },
                  "reason": {
                    "type": "string",
                    "description": "Any additional information related to the outcome"
                  },
                  "token": {
                    "type": "string",
                    "description": "The SDK token associated with the SDK flow you are updating the outcome for"
                  }
                },
                "required": [
                  "outcome",
                  "token"
                ]
              }
            }
          }
        },
        "tags": [
          "KYC"
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
