---
source_view: https://docs.alpaca.markets/reference/get-v1-events-nta
source_md: https://docs.alpaca.markets/reference/get-v1-events-nta.md
scraped_at_utc: 2026-01-27T04:30:48Z
---
# Subscribe to Non-Trading Activities Events (SSE)

The Events API provides event push as well as historical queries via SSE (server sent events).

You can listen to non-trading activities updates as they get processed by our backoffice, for both end-user and firm accounts.

Historical events are streamed immediately if queried, and updates are pushed as events occur.

You can listen to when NTAs are pushed such as CSDs, JNLC (journals) or FEEs.

Query Params Rules:
- `since` required if `until` specified
- `since_id` required if `until_id` specified
- `since_ulid` required if `until_ulid` specified
- `since`, `since_id` or `since_ulid`  can’t be used at the same time
Behavior:
- if `since`, `since_id` or `since_ulid` not specified this will not return any historic data
- if `until`, `until_id` or `until_ulid` reached stream will end (status 200)'

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
      "name": "Events"
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
    "/v1/events/nta": {
      "get": {
        "summary": "Subscribe to Non-Trading Activities Events (SSE)",
        "tags": [
          "Events"
        ],
        "responses": {
          "200": {
            "description": "OK",
            "content": {
              "application/json": {
                "schema": {
                  "description": "Represents a non-trade activity SSE event",
                  "type": "object",
                  "x-examples": {
                    "example-1": {
                      "id": "afb78fa2-7e4c-4e0a-bca2-2e0d26a87f88",
                      "qty": 0,
                      "status": "executed",
                      "symbol": null,
                      "entry_type": "JNLC",
                      "net_amount": 10,
                      "description": null,
                      "settle_date": "2024-11-26",
                      "system_date": "2024-11-26",
                      "account_id": "8e00606a-c9ac-409a-ba45-f55e8f77984a",
                      "at": "2024-11-26T15:25:17.803914Z",
                      "event_ulid": "01JDMH7BKCCB4XY5F11HN63NZX"
                    },
                    "example-2": {
                      "id": "d96cea8a-6a77-46cd-bb7b-df6d74442653",
                      "qty": 0,
                      "status": "executed",
                      "symbol": null,
                      "entry_type": "FEE",
                      "net_amount": -0.01,
                      "description": "TAF fee for proceed of 0.010052895 shares (1 trades) on 2024-11-11 by 613651765",
                      "settle_date": "2024-11-12",
                      "system_date": "2024-11-11",
                      "entry_sub_type": "TAF",
                      "account_id": "11629972-5fd6-4e14-ad9e-0f0cabd2777f",
                      "at": "2024-11-12T01:15:53.132425Z",
                      "event_ulid": "01JCEZ1ZDCE44GFX6WZ75N4199"
                    }
                  },
                  "title": "NonTradeActivityEvent",
                  "properties": {
                    "id": {
                      "type": "string",
                      "description": "Record UUID",
                      "format": "uuid"
                    },
                    "qty": {
                      "type": "number",
                      "description": "Quantity of the stock affected. 0 for cash events",
                      "format": "decimal"
                    },
                    "status": {
                      "type": "string",
                      "enum": [
                        "executed",
                        "correct",
                        "canceled"
                      ],
                      "example": "executed",
                      "description": "Status of the event"
                    },
                    "symbol": {
                      "type": "string",
                      "example": "AAPL",
                      "description": "Symbol the event is associated with, empty string when no symbol is applicable"
                    },
                    "cusip": {
                      "type": "string",
                      "example": "037833100",
                      "description": "CUSIP the event is associated with, not present when no CUSIP is applicable"
                    },
                    "entry_type": {
                      "type": "string",
                      "example": "JNLC",
                      "description": "Type of entry for e.g JNLC, FEE, INT, DIVNRA etc"
                    },
                    "net_amount": {
                      "type": "number",
                      "format": "decimal",
                      "example": 1,
                      "description": "Net amount if applicable, 0 otherwise"
                    },
                    "description": {
                      "type": "string",
                      "example": "Example description",
                      "description": "Additional information about the event, empty string if not applicable"
                    },
                    "settle_date": {
                      "type": "string",
                      "description": "Date of settlement if applicable",
                      "format": "date"
                    },
                    "system_date": {
                      "type": "string",
                      "description": "Date of the event recorded in the system",
                      "format": "date"
                    },
                    "price": {
                      "type": "string",
                      "format": "decimal",
                      "example": "0.38921",
                      "description": "Price if applicable."
                    },
                    "per_share_amount": {
                      "type": "number",
                      "format": "decimal",
                      "example": 0.3,
                      "description": "Per share amount if applicable"
                    },
                    "account_id": {
                      "type": "string",
                      "description": "Account UUID",
                      "format": "uuid"
                    },
                    "at": {
                      "type": "string",
                      "description": "Timedate of when the event was emitted",
                      "format": "date-time"
                    },
                    "event_id": {
                      "type": "integer",
                      "description": "Monotonically increasing 64bit integer"
                    },
                    "event_ulid": {
                      "type": "string",
                      "format": "ulid",
                      "description": "lexically sortable, monotonically increasing character array"
                    }
                  },
                  "required": [
                    "account_id",
                    "at",
                    "id",
                    "event_ulid",
                    "system_date",
                    "settle_date",
                    "net_amount",
                    "entry_type",
                    "description"
                  ],
                  "x-stoplight": {
                    "id": "ch42mh3ekwcmy"
                  },
                  "x-readme-ref-name": "NonTradeActivityEvent"
                }
              }
            }
          }
        },
        "operationId": "get-v1-events-nta",
        "description": "The Events API provides event push as well as historical queries via SSE (server sent events).\n\nYou can listen to non-trading activities updates as they get processed by our backoffice, for both end-user and firm accounts.\n\nHistorical events are streamed immediately if queried, and updates are pushed as events occur.\n\nYou can listen to when NTAs are pushed such as CSDs, JNLC (journals) or FEEs.\n\nQuery Params Rules:\n- `since` required if `until` specified\n- `since_id` required if `until_id` specified\n- `since_ulid` required if `until_ulid` specified\n- `since`, `since_id` or `since_ulid`  can’t be used at the same time\nBehavior:\n- if `since`, `since_id` or `since_ulid` not specified this will not return any historic data\n- if `until`, `until_id` or `until_ulid` reached stream will end (status 200)'",
        "parameters": [
          {
            "schema": {
              "type": "string"
            },
            "in": "query",
            "name": "id"
          },
          {
            "schema": {
              "type": "string",
              "format": "date"
            },
            "in": "query",
            "name": "since",
            "description": "Format: YYYY-MM-DD"
          },
          {
            "schema": {
              "type": "string",
              "format": "date"
            },
            "in": "query",
            "name": "until",
            "description": "Format: YYYY-MM-DD"
          },
          {
            "schema": {
              "type": "integer"
            },
            "in": "query",
            "name": "since_id"
          },
          {
            "schema": {
              "type": "integer"
            },
            "in": "query",
            "name": "until_id"
          },
          {
            "name": "since_ulid",
            "in": "query",
            "schema": {
              "type": "string",
              "format": "ulid"
            }
          },
          {
            "name": "until_ulid",
            "in": "query",
            "schema": {
              "type": "string",
              "format": "ulid"
            }
          },
          {
            "schema": {
              "type": "boolean"
            },
            "in": "query",
            "name": "include_preprocessing"
          },
          {
            "name": "group_id",
            "in": "query",
            "schema": {
              "type": "string",
              "format": "uuid"
            },
            "description": "ID used to link activities who share a sibling relationship"
          }
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
