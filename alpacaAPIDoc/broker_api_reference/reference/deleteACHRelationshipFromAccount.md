---
source_view: https://docs.alpaca.markets/reference/deleteachrelationshipfromaccount
source_md: https://docs.alpaca.markets/reference/deleteachrelationshipfromaccount.md
scraped_at_utc: 2026-01-27T04:30:48Z
---
# Delete an existing ACH relationship

Delete an existing ACH relationship for an account

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
    "/v1/accounts/{account_id}/ach_relationships/{ach_relationship_id}": {
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
          "schema": {
            "type": "string",
            "format": "uuid"
          },
          "name": "ach_relationship_id",
          "in": "path",
          "description": "ACH relationship identifier",
          "required": true
        }
      ],
      "delete": {
        "summary": "Delete an existing ACH relationship",
        "operationId": "deleteACHRelationshipFromAccount",
        "responses": {
          "204": {
            "description": "Success (No Content)"
          },
          "400": {
            "description": "the passed in account_id or relationship_id were invalid"
          },
          "404": {
            "description": "Relationship Not Found"
          }
        },
        "description": "Delete an existing ACH relationship for an account",
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
