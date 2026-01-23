---
source_view: https://docs.alpaca.markets/reference/get-v2-corporate_actions-announcements-1
source_md: https://docs.alpaca.markets/reference/get-v2-corporate_actions-announcements-1.md
scraped_at_utc: 2026-01-22T23:02:18Z
---
# Retrieve Announcements

This endpoint is deprecated, please use [the new corporate actions endpoint](https://docs.alpaca.markets/reference/corporateactions-1) instead.

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
      "name": "Corporate Actions"
    }
  ],
  "paths": {
    "/v2/corporate_actions/announcements": {
      "get": {
        "summary": "Retrieve Announcements",
        "deprecated": true,
        "tags": [
          "Corporate Actions"
        ],
        "responses": {
          "200": {
            "description": "OK",
            "content": {
              "application/json": {
                "schema": {
                  "type": "array",
                  "items": {
                    "type": "object",
                    "properties": {
                      "id": {
                        "type": "string"
                      },
                      "corporate_actions_id": {
                        "type": "string"
                      },
                      "ca_type": {
                        "type": "string"
                      },
                      "ca_sub_type": {
                        "type": "string"
                      },
                      "initiating_symbol": {
                        "type": "string"
                      },
                      "initiating_original_cusip": {
                        "type": "string"
                      },
                      "target_symbol": {
                        "type": "string"
                      },
                      "target_original_cusip": {
                        "type": "string"
                      },
                      "declaration_date": {
                        "type": "string"
                      },
                      "expiration_date": {
                        "type": "string"
                      },
                      "record_date": {
                        "type": "string"
                      },
                      "payable_date": {
                        "type": "string"
                      },
                      "cash": {
                        "type": "string"
                      },
                      "old_rate": {
                        "type": "string"
                      },
                      "new_rate": {
                        "type": "string"
                      },
                      "corporate_action_id": {
                        "type": "string"
                      },
                      "ex_date": {
                        "type": "string"
                      }
                    }
                  },
                  "x-examples": {
                    "Example 1": [
                      {
                        "id": "be3c368a-4c7c-4384-808e-f02c9f5a8afe",
                        "corporate_actions_id": "F58684224_XY37",
                        "ca_type": "Dividend",
                        "ca_sub_type": "DIV",
                        "initiating_symbol": "MLLAX",
                        "initiating_original_cusip": 5.5275e+105,
                        "target_symbol": "MLLAX",
                        "target_original_cusip": 5.5275e+105,
                        "declaration_date": "2021-01-05",
                        "expiration_date": "2021-01-12",
                        "record_date": "2021-01-13",
                        "payable_date": "2021-01-14",
                        "cash": "0.018",
                        "old_rate": "1",
                        "new_rate": "1"
                      },
                      {
                        "corporate_action_id": "48251W104_AD21",
                        "ca_type": "Dividend",
                        "ca_sub_type": "cash",
                        "initiating_symbol": "KKR",
                        "initiating_original_cusip": "G52830109",
                        "target_symbol": "KKR",
                        "target_original_cusip": "G52830109",
                        "declaration_date": "2021-11-01",
                        "ex_date": "2021-11-12",
                        "record_date": "2021-11-15",
                        "payable_date": "2021-11-30",
                        "cash": "0.145",
                        "old_rate": "1",
                        "new_rate": "1"
                      }
                    ]
                  }
                }
              }
            }
          }
        },
        "operationId": "get-v2-corporate_actions-announcements",
        "description": "This endpoint is deprecated, please use [the new corporate actions endpoint](https://docs.alpaca.markets/reference/corporateactions-1) instead.",
        "parameters": [
          {
            "schema": {
              "type": "string"
            },
            "in": "query",
            "name": "ca_types",
            "description": "A comma-delimited list of Dividend, Merger, Spinoff, or Split.",
            "required": true
          },
          {
            "schema": {
              "type": "string"
            },
            "in": "query",
            "name": "since",
            "description": "The start (inclusive) of the date range when searching corporate action announcements. This should follow the YYYY-MM-DD format. The date range is limited to 90 days.",
            "required": true
          },
          {
            "schema": {
              "type": "string"
            },
            "in": "query",
            "name": "until",
            "description": "The end (inclusive) of the date range when searching corporate action announcements. This should follow the YYYY-MM-DD format. The date range is limited to 90 days.",
            "required": true
          },
          {
            "schema": {
              "type": "string"
            },
            "in": "query",
            "name": "symbol",
            "description": "The symbol of the company initiating the announcement."
          },
          {
            "schema": {
              "type": "string"
            },
            "in": "query",
            "name": "cusip",
            "description": "The CUSIP of the company initiating the announcement."
          },
          {
            "schema": {
              "type": "string"
            },
            "in": "query",
            "name": "date_type",
            "description": "declaration_date, ex_date, record_date, or payable_date"
          }
        ]
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
