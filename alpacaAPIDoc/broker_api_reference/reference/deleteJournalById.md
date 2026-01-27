---
source_view: https://docs.alpaca.markets/reference/deletejournalbyid
source_md: https://docs.alpaca.markets/reference/deletejournalbyid.md
scraped_at_utc: 2026-01-27T04:30:48Z
---
# Cancel a Pending Journal

You can only delete a journal if the journal is still in a pending state, if a journal is executed you will not be able to delete. The alternative is to create a mirror journal entry to reverse the flow of funds.

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
      "name": "Journals"
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
    "/v1/journals/{journal_id}": {
      "parameters": [
        {
          "name": "journal_id",
          "in": "path",
          "required": true,
          "schema": {
            "type": "string",
            "format": "uuid"
          }
        }
      ],
      "delete": {
        "summary": "Cancel a Pending Journal",
        "tags": [
          "Journals"
        ],
        "description": "You can only delete a journal if the journal is still in a pending state, if a journal is executed you will not be able to delete. The alternative is to create a mirror journal entry to reverse the flow of funds.",
        "responses": {
          "204": {
            "description": "The cancel request succeeded. (No-content)\n"
          },
          "404": {
            "description": "The journal is not found.\n"
          },
          "422": {
            "description": "The journal is not in the pending status.\n"
          }
        },
        "operationId": "deleteJournalById"
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
