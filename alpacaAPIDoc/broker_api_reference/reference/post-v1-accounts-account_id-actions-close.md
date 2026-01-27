---
source_view: https://docs.alpaca.markets/reference/post-v1-accounts-account_id-actions-close
source_md: https://docs.alpaca.markets/reference/post-v1-accounts-account_id-actions-close.md
scraped_at_utc: 2026-01-27T04:30:48Z
---
# Close an Account

This operation closes an active account. The underlying records and information of the account are not deleted by this operation.

**Before closing an account, you are responsible for closing all the positions and withdrawing all the money associated with that account. Learn more in the Positions Documentation.**

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
    "/v1/accounts/{account_id}/actions/close": {
      "parameters": [
        {
          "schema": {
            "type": "string"
          },
          "name": "account_id",
          "in": "path",
          "required": true,
          "description": "The id of the account to be closed"
        }
      ],
      "post": {
        "summary": "Close an Account",
        "tags": [
          "Accounts"
        ],
        "operationId": "post-v1-accounts-account_id-actions-close",
        "responses": {
          "204": {
            "description": "Success"
          },
          "404": {
            "description": "Account Not Found"
          }
        },
        "description": "This operation closes an active account. The underlying records and information of the account are not deleted by this operation.\n\n**Before closing an account, you are responsible for closing all the positions and withdrawing all the money associated with that account. Learn more in the Positions Documentation.**"
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
