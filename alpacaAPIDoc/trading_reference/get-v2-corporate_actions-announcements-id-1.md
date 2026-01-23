---
source_view: https://docs.alpaca.markets/reference/get-v2-corporate_actions-announcements-id-1
source_md: https://docs.alpaca.markets/reference/get-v2-corporate_actions-announcements-id-1.md
scraped_at_utc: 2026-01-22T23:02:18Z
---
# Retrieve a Specific Announcement

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
    "/v2/corporate_actions/announcements/{id}": {
      "parameters": [
        {
          "schema": {
            "type": "string"
          },
          "name": "id",
          "in": "path",
          "required": true,
          "description": "The corporate announcement’s id"
        }
      ],
      "get": {
        "summary": "Retrieve a Specific Announcement",
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
                  "type": "object",
                  "x-examples": {
                    "Example 1": {
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
                    }
                  },
                  "properties": {
                    "id": {
                      "type": "string"
                    },
                    "corporate_actions_id": {
                      "type": "string"
                    },
                    "ca_type": {
                      "type": "string",
                      "description": "A comma-delimited list of Dividend, Merger, Spinoff, or Split."
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
                    }
                  }
                }
              }
            }
          }
        },
        "operationId": "get-v2-corporate_actions-announcements-id",
        "description": "This endpoint is deprecated, please use [the new corporate actions endpoint](https://docs.alpaca.markets/reference/corporateactions-1) instead."
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
