---
source_view: https://docs.alpaca.markets/reference/get-v1-accounts-account_id-onfido-sdk-tokens
source_md: https://docs.alpaca.markets/reference/get-v1-accounts-account_id-onfido-sdk-tokens.md
scraped_at_utc: 2026-01-27T04:30:48Z
---
# Retrieve an Onfido SDK Token

Get an SDK token to activate the Onfido SDK flow within your app. You will have to keep track of the SDK token so you can pass it back when you upload the SDK outcome. We recommend storing the token in memory rather than persistent storage to reduce any unnecessary overhead in your app.

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
    "/v1/accounts/{account_id}/onfido/sdk/tokens": {
      "get": {
        "summary": "Retrieve an Onfido SDK Token",
        "tags": [
          "KYC"
        ],
        "parameters": [
          {
            "name": "account_id",
            "in": "path",
            "schema": {
              "type": "string",
              "format": "uuid"
            },
            "required": true,
            "description": "The account ID"
          },
          {
            "name": "referrer",
            "in": "query",
            "schema": {
              "type": "string"
            },
            "description": "The referrer URL of your web app or the application ID of your mobile app. If not passed in, will default to the * wildcard"
          },
          {
            "name": "platform",
            "in": "query",
            "schema": {
              "type": "string"
            },
            "description": "Required if referrer provided. Enum values are either mobile or web"
          }
        ],
        "responses": {
          "200": {
            "description": "OK",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "token": {
                      "type": "string"
                    }
                  },
                  "x-examples": {
                    "Example 1": {
                      "token": "header.payload.signature"
                    }
                  }
                }
              }
            }
          },
          "422": {
            "description": "Onfido applicant not yet created for account. If you haven’t already contacted Alapca to enable Onfido, please do so."
          }
        },
        "operationId": "get-v1-accounts-account_id-onfido-sdk-tokens",
        "description": "Get an SDK token to activate the Onfido SDK flow within your app. You will have to keep track of the SDK token so you can pass it back when you upload the SDK outcome. We recommend storing the token in memory rather than persistent storage to reduce any unnecessary overhead in your app."
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
