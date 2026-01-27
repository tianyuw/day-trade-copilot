---
source_view: https://docs.alpaca.markets/reference/get-v1-transfers-jit-reports
source_md: https://docs.alpaca.markets/reference/get-v1-transfers-jit-reports.md
scraped_at_utc: 2026-01-27T04:30:48Z
---
# Retrieve JIT Reports

Returns all JIT reports

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
    "/v1/transfers/jit/reports": {
      "get": {
        "summary": "Retrieve JIT Reports",
        "tags": [
          "Funding"
        ],
        "responses": {
          "200": {
            "description": "OK",
            "content": {
              "application/json": {
                "schema": {
                  "title": "JITReport",
                  "x-stoplight": {
                    "id": "ragg7o909954y"
                  },
                  "type": "object",
                  "description": "JIT Securities reports are made available through the API and can be accessed within the hour after 11:30 PM EST on the trade date (T+0). The reports communicate transaction-level details as well as overall settlement amounts, transfer direction, and payment timing.",
                  "properties": {
                    "detail": {
                      "type": "string",
                      "x-stoplight": {
                        "id": "s4ezmhwn7oqxv"
                      },
                      "description": "Contains all activities that impact cash throughout the trading session including executed trades, trading fees, and corporate actions that involve cash allocations.\n\ncontent-type = application/csv"
                    },
                    "net_summary": {
                      "type": "string",
                      "x-stoplight": {
                        "id": "phtq9hmob3aux"
                      },
                      "description": "Consists of three columns and a single row, which lists the net money movement to or from Alpaca for T0, T1, and T2.\n\ncontent-type = application/csv"
                    },
                    "net_payment": {
                      "type": "string",
                      "x-stoplight": {
                        "id": "um5xd4us4djch"
                      },
                      "description": "Highlights the net amount due to Alpaca by settlement or to the partner on the date of settlement in a formalized invoice format.\n\ncontent-type = application/pdf"
                    },
                    "net_payment_final": {
                      "type": "string",
                      "x-stoplight": {
                        "id": "3q3ubyhwekvh4"
                      },
                      "description": "Includes additional information to account for T+0 and T+1 settling activity to clarify settlement journaling reconciliation. This report is generated after trading session close on T+1.\n\ncontent-type = application/pdf"
                    },
                    "obligation": {
                      "type": "string",
                      "description": "Lists of all open obligations towards the partner that are to be settled.\n\ncontent-type = application/csv"
                    }
                  },
                  "x-readme-ref-name": "JITReport"
                }
              }
            }
          }
        },
        "operationId": "get-v1-transfers-jit-reports",
        "parameters": [
          {
            "name": "report_type",
            "in": "query",
            "required": true,
            "schema": {
              "type": "string",
              "enum": [
                "detail",
                "net_summary",
                "net_payment",
                "net_payment_final",
                "gross_summary",
                "gross_payment",
                "gross_payment_final"
              ]
            },
            "description": "The type of report you want to get."
          },
          {
            "name": "system_date",
            "in": "query",
            "required": true,
            "schema": {
              "type": "string",
              "format": "date"
            },
            "description": "Date of file generation."
          },
          {
            "name": "asset_class",
            "in": "query",
            "schema": {
              "type": "string",
              "enum": [
                "us_equity",
                "crypto"
              ]
            },
            "description": "The asset class to retrieve for."
          }
        ],
        "description": "Returns all JIT reports"
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
