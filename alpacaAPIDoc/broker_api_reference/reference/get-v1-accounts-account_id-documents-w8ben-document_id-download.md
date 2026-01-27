---
source_view: https://docs.alpaca.markets/reference/get-v1-accounts-account_id-documents-w8ben-document_id-download
source_md: https://docs.alpaca.markets/reference/get-v1-accounts-account_id-documents-w8ben-document_id-download.md
scraped_at_utc: 2026-01-27T04:30:48Z
---
# Download the W8BEN document for the primary owner of an account

This endpoint allows you to download a W-8 BEN document for the primary owner of an account based on the document_id passed as a path parameter. The returned document is in PDF format.

For certain individuals, a W-8 BEN form should be submitted at onboarding. If the individual is not a registered U.S. taxpayer (not subject to a W-9), the W-8 BEN form may need to be submitted. The IRS explains which individuals this applies to and provides instructions on completing the form. Every three years, in addition to the calendar year it was signed, a new W-8 BEN form must be submitted.

The form can be submitted in JSON, JSONC, PNG, JPEG or PDF. If submitting it in JSON, please see the W-8 BEN completed with the corresponding field names for the API here.

Note: The dates collected on the form are in a slightly different format than how they need to be submitted via Accounts API. It is requested by the user on the form in MM-DD-YYYY, but should be submitted as YYYY-MM-DD.

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
      "name": "Documents"
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
    "/v1/accounts/{account_id}/documents/w8ben/{document_id}/download": {
      "parameters": [
        {
          "schema": {
            "type": "string"
          },
          "name": "account_id",
          "in": "path",
          "required": true,
          "description": "The id of the related account"
        },
        {
          "schema": {
            "type": "string"
          },
          "name": "document_id",
          "in": "path",
          "required": true,
          "description": "The id of the W8BEN to download"
        }
      ],
      "get": {
        "summary": "Download the W8BEN document for the primary owner of an account",
        "tags": [
          "Documents"
        ],
        "responses": {
          "301": {
            "description": "Redirects to a presigned download link for the document PDF."
          },
          "404": {
            "description": "Document Not Found"
          }
        },
        "operationId": "get-v1-accounts-account_id-documents-w8ben-document_id-download",
        "description": "This endpoint allows you to download a W-8 BEN document for the primary owner of an account based on the document_id passed as a path parameter. The returned document is in PDF format.\n\nFor certain individuals, a W-8 BEN form should be submitted at onboarding. If the individual is not a registered U.S. taxpayer (not subject to a W-9), the W-8 BEN form may need to be submitted. The IRS explains which individuals this applies to and provides instructions on completing the form. Every three years, in addition to the calendar year it was signed, a new W-8 BEN form must be submitted.\n\nThe form can be submitted in JSON, JSONC, PNG, JPEG or PDF. If submitting it in JSON, please see the W-8 BEN completed with the corresponding field names for the API here.\n\nNote: The dates collected on the form are in a slightly different format than how they need to be submitted via Accounts API. It is requested by the user on the form in MM-DD-YYYY, but should be submitted as YYYY-MM-DD."
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
