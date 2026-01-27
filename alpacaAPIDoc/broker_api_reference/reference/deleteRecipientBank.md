---
source_view: https://docs.alpaca.markets/reference/deleterecipientbank
source_md: https://docs.alpaca.markets/reference/deleterecipientbank.md
scraped_at_utc: 2026-01-27T04:30:48Z
---
# Delete a Bank Relationship for an Account

If successful, deletes Bank Relationship for an account

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
    "/v1/accounts/{account_id}/recipient_banks/{bank_id}": {
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
        },
        {
          "name": "bank_id",
          "in": "path",
          "required": true,
          "schema": {
            "type": "string",
            "format": "uuid"
          }
        }
      ],
      "delete": {
        "tags": [
          "Funding"
        ],
        "summary": "Delete a Bank Relationship for an Account",
        "responses": {
          "204": {
            "description": "Success (No Content)"
          },
          "400": {
            "description": "Bad Request"
          },
          "404": {
            "description": "No Bank Relationship with the id specified by bank_id was found for this Account"
          }
        },
        "operationId": "deleteRecipientBank",
        "description": "If successful, deletes Bank Relationship for an account"
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
