---
source_view: https://docs.alpaca.markets/reference/subscribetofundingstatussse
source_md: https://docs.alpaca.markets/reference/subscribetofundingstatussse.md
scraped_at_utc: 2026-01-27T04:30:48Z
---
# Subscribe to Funding Status Events (SSE)

The Events API provides event push as well as historical queries via SSE (server sent events).

You can listen to funding status updates as they get processed by our backoffice, for both end-user and firm accounts.

Historical events are streamed immediately if queried, and updates are pushed as events occur.

Query Params Rules:
- `since` required if `until` specified
- `since_id` required if `until_id` specified
- `since_ulid` required if `until_ulid` specified
- `since`, `since_id` or `since_ulid`  can’t be used at the same time
Behavior:
- if `since`, `since_id` or `since_ulid` not specified this will not return any historic data
- if `until`, `until_id` or `until_ulid` reached stream will end (status 200)

---

Note for people using the clients generated from this OAS spec. Currently OAS-3 doesn't have full support for representing SSE style responses from an API, so if you are using a generated client and don't specify a `since` and `until` there is a good chance the generated clients will hang waiting for the response to end.

If you require the streaming capabilities we recommend not using the generated clients for this specific usecase until the OAS-3 standards come to a consensus on how to represent this correctly in OAS-3.

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
    "/v2/events/funding/status": {
      "get": {
        "summary": "Subscribe to Funding Status Events (SSE)",
        "tags": [
          "Events"
        ],
        "responses": {
          "200": {
            "description": "Connected. Events will now start streaming as long as you keep the connection open.",
            "content": {
              "text/event-stream": {
                "schema": {
                  "type": "array",
                  "items": {
                    "oneOf": [
                      {
                        "description": "Represents a change in a Funding entity's status, sent over the events streaming api. Currently, the suppported entities are: bank relationships, bank wires and transfers.",
                        "type": "object",
                        "x-examples": {
                          "example-1": {
                            "event_id": "01F7VQQ782DM57SJNWAYMD14J9",
                            "at": "2025-04-11T19:52:24.066998Z",
                            "account_id": "8e00606a-c9ac-409a-ba45-f55e8f77984a",
                            "correspondent": "LPCA",
                            "entity_id": "c4ed4206-697b-4859-ab71-b9de6649859d",
                            "entity_type": "BankRelationship",
                            "status_from": null,
                            "status_to": "QUEUED"
                          },
                          "example-2": {
                            "event_id": "01F7VQQ782DM57SJNWAYMD14J9",
                            "at": "2025-04-11T19:52:24.066998Z",
                            "account_id": "8e00606a-c9ac-409a-ba45-f55e8f77984a",
                            "correspondent": "LPCA",
                            "entity_id": "c4ed4206-697b-4859-ab71-b9de6649859d",
                            "entity_type": "BankRelationship",
                            "status_from": "QUEUED",
                            "status_to": "REJECTED",
                            "reason": "bank account owner name does not match brokerage account name"
                          }
                        },
                        "title": "StatusFundingEvent",
                        "properties": {
                          "event_id": {
                            "type": "string",
                            "format": "ulid",
                            "minLength": 1,
                            "description": "lexically sortable, monotonically increasing character array"
                          },
                          "at": {
                            "type": "string",
                            "minLength": 1,
                            "description": "Timedate of when the transfer status changed"
                          },
                          "account_id": {
                            "type": "string",
                            "minLength": 1,
                            "description": "Account UUID",
                            "format": "uuid"
                          },
                          "correspondent": {
                            "type": "string",
                            "minLength": 1,
                            "maxLength": 4,
                            "description": "Correspondent's code",
                            "format": "ABCD"
                          },
                          "entity_id": {
                            "type": "string",
                            "minLength": 1,
                            "description": "Entity's UUID",
                            "format": "uuid"
                          },
                          "entity_type": {
                            "type": "string",
                            "minLength": 1,
                            "description": "Valid values are BankRelationship, WireBank and Transfer.",
                            "format": "uuid"
                          },
                          "status_from": {
                            "type": "string",
                            "description": "Valid values are based on entity type:\n- BankRelationship:\n  - QUEUED\n  - CANCEL_REQUESTED\n  - CANCEL_SENT\n  - CANCEL_FAILED\n  - PENDING\n  - SENT_TO_CLEARING\n  - APPROVED\n  - CANCELED\n  - REJECTED\n- WireBank:\n  - QUEUED\n  - SENT_TO_CLEARING\n  - APPROVED\n  - CANCELED\n  - REJECTED\n- Transfer:\n  - QUEUED\n  - APPROVAL_PENDING\n  - CANCELED\n  - EXPIRED\n  - APPROVED\n  - REJECTED\n  - SENT_TO_CLEARING\n  - COMPLETE\n  - RETURNED\n"
                          },
                          "status_to": {
                            "type": "string",
                            "minLength": 1,
                            "description": "Valid values are based on entity type:\n- BankRelationship:\n  - QUEUED\n  - CANCEL_REQUESTED\n  - CANCEL_SENT\n  - CANCEL_FAILED\n  - PENDING\n  - SENT_TO_CLEARING\n  - APPROVED\n  - CANCELED\n  - REJECTED\n- WireBank:\n  - QUEUED\n  - SENT_TO_CLEARING\n  - APPROVED\n  - CANCELED\n  - REJECTED\n- Transfer:\n  - QUEUED\n  - APPROVAL_PENDING\n  - CANCELED\n  - EXPIRED\n  - APPROVED\n  - REJECTED\n  - SENT_TO_CLEARING\n  - COMPLETE\n  - RETURNED\n"
                          },
                          "reason": {
                            "type": "string",
                            "description": "Used when an a bank relationship is rejected, a wire bank is canceled, etc."
                          }
                        },
                        "required": [
                          "event_id",
                          "at",
                          "account_id",
                          "correspondent",
                          "entity_id",
                          "entity_type",
                          "status_to"
                        ],
                        "x-stoplight": {
                          "id": "ch42mh3ekwcmy"
                        },
                        "x-readme-ref-name": "StatusFundingEvent"
                      }
                    ]
                  }
                }
              }
            }
          }
        },
        "parameters": [
          {
            "name": "since",
            "in": "query",
            "schema": {
              "type": "string",
              "format": "date"
            },
            "description": "Format: YYYY-MM-DD"
          },
          {
            "name": "until",
            "in": "query",
            "schema": {
              "type": "string",
              "format": "date"
            },
            "description": "Format: YYYY-MM-DD"
          },
          {
            "name": "since_id",
            "in": "query",
            "schema": {
              "type": "integer"
            }
          },
          {
            "name": "until_id",
            "in": "query",
            "schema": {
              "type": "integer"
            }
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
          }
        ],
        "operationId": "subscribeToFundingStatusSSE",
        "description": "The Events API provides event push as well as historical queries via SSE (server sent events).\n\nYou can listen to funding status updates as they get processed by our backoffice, for both end-user and firm accounts.\n\nHistorical events are streamed immediately if queried, and updates are pushed as events occur.\n\nQuery Params Rules:\n- `since` required if `until` specified\n- `since_id` required if `until_id` specified\n- `since_ulid` required if `until_ulid` specified\n- `since`, `since_id` or `since_ulid`  can’t be used at the same time\nBehavior:\n- if `since`, `since_id` or `since_ulid` not specified this will not return any historic data\n- if `until`, `until_id` or `until_ulid` reached stream will end (status 200)\n\n---\n\nNote for people using the clients generated from this OAS spec. Currently OAS-3 doesn't have full support for representing SSE style responses from an API, so if you are using a generated client and don't specify a `since` and `until` there is a good chance the generated clients will hang waiting for the response to end.\n\nIf you require the streaming capabilities we recommend not using the generated clients for this specific usecase until the OAS-3 standards come to a consensus on how to represent this correctly in OAS-3."
      },
      "parameters": []
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
