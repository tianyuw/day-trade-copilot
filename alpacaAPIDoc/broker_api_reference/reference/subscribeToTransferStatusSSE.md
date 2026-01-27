---
source_view: https://docs.alpaca.markets/reference/subscribetotransferstatussse
source_md: https://docs.alpaca.markets/reference/subscribetotransferstatussse.md
scraped_at_utc: 2026-01-27T04:30:48Z
---
# Subscribe to Transfer Events (SSE) (Legacy)

**Deprecation notice**

As part of the deprecation process, the legacy transfer events API is now only available for existing broker-partners at `GET /v1/events/transfers/status` and for compatibility reasons.

All new broker partners will not have the option to use the legacy transfer events endpoint.

They should integrate with the new `/v2/events/funding/status` endpoint instead.

Also, all existing broker partners are now recommended to upgrade to the `/v2/events/funding/status` endpoint, which provides faster event delivery times.

---

The Events API provides event push as well as historical queries via SSE (server sent events).

You can listen to transfer status updates as they get processed by our backoffice, for both end-user and firm accounts.

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
    "/v1/events/transfers/status": {
      "get": {
        "summary": "Subscribe to Transfer Events (SSE) (Legacy)",
        "deprecated": true,
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
                    "description": "Represents a change in a Transfer's status, sent over the events streaming api.",
                    "type": "object",
                    "x-examples": {
                      "example-1": {
                        "account_id": "8e00606a-c9ac-409a-ba45-f55e8f77984a",
                        "at": "2021-06-10T19:52:24.066998Z",
                        "event_id": 15961,
                        "event_ulid": "01F7VQQ782DM57SJNWAYMD14J9",
                        "status_from": "QUEUED",
                        "status_to": "SENT_TO_CLEARING",
                        "transfer_id": "c4ed4206-697b-4859-ab71-b9de6649859d"
                      },
                      "example-2": {
                        "account_id": "8e00606a-c9ac-409a-ba45-f55e8f77984a",
                        "at": "2021-06-10T20:02:24.280178Z",
                        "event_id": 15962,
                        "status_from": "SENT_TO_CLEARING",
                        "status_to": "COMPLETE",
                        "transfer_id": "c4ed4206-697b-4859-ab71-b9de6649859d"
                      }
                    },
                    "title": "TransferStatusEvent",
                    "properties": {
                      "account_id": {
                        "type": "string",
                        "minLength": 1,
                        "description": "Account UUID",
                        "format": "uuid"
                      },
                      "at": {
                        "type": "string",
                        "minLength": 1,
                        "description": "Timedate of when the transfer status changed",
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
                      },
                      "status_from": {
                        "type": "string",
                        "example": "QUEUED",
                        "enum": [
                          "QUEUED",
                          "APPROVAL_PENDING",
                          "PENDING",
                          "SENT_TO_CLEARING",
                          "REJECTED",
                          "CANCELED",
                          "APPROVED",
                          "COMPLETE",
                          "RETURNED"
                        ],
                        "description": "- **QUEUED**\nTransfer is in queue to be processed.\n- **APPROVAL_PENDING**\nTransfer is pending approval.\n- **PENDING**\nTransfer is pending processing.\n- **SENT_TO_CLEARING**\nTransfer is being processed by the clearing firm.\n- **REJECTED**\nTransfer is rejected.\n- **CANCELED**\nClient initiated transfer cancellation.\n- **APPROVED**\nTransfer is approved.\n- **COMPLETE**\nTransfer is completed.\n- **RETURNED**\nThe bank issued an ACH return for the transfer.\n",
                        "x-stoplight": {
                          "id": "mqx0hpg6h25vt"
                        },
                        "x-readme-ref-name": "TransferStatus"
                      },
                      "status_to": {
                        "type": "string",
                        "example": "QUEUED",
                        "enum": [
                          "QUEUED",
                          "APPROVAL_PENDING",
                          "PENDING",
                          "SENT_TO_CLEARING",
                          "REJECTED",
                          "CANCELED",
                          "APPROVED",
                          "COMPLETE",
                          "RETURNED"
                        ],
                        "description": "- **QUEUED**\nTransfer is in queue to be processed.\n- **APPROVAL_PENDING**\nTransfer is pending approval.\n- **PENDING**\nTransfer is pending processing.\n- **SENT_TO_CLEARING**\nTransfer is being processed by the clearing firm.\n- **REJECTED**\nTransfer is rejected.\n- **CANCELED**\nClient initiated transfer cancellation.\n- **APPROVED**\nTransfer is approved.\n- **COMPLETE**\nTransfer is completed.\n- **RETURNED**\nThe bank issued an ACH return for the transfer.\n",
                        "x-stoplight": {
                          "id": "mqx0hpg6h25vt"
                        },
                        "x-readme-ref-name": "TransferStatus"
                      },
                      "transfer_id": {
                        "type": "string",
                        "minLength": 1,
                        "description": "Transfer UUID",
                        "format": "uuid"
                      }
                    },
                    "required": [
                      "account_id",
                      "at",
                      "event_id",
                      "event_ulid",
                      "status_from",
                      "status_to",
                      "transfer_id"
                    ],
                    "x-stoplight": {
                      "id": "ch42mh3ekwcmy"
                    },
                    "x-readme-ref-name": "TransferStatusEvent"
                  }
                }
              }
            }
          },
          "410": {
            "description": "Deprecated. The endpoint is not available for this partner."
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
        "operationId": "subscribeToTransferStatusSSE",
        "description": "**Deprecation notice**\n\nAs part of the deprecation process, the legacy transfer events API is now only available for existing broker-partners at `GET /v1/events/transfers/status` and for compatibility reasons.\n\nAll new broker partners will not have the option to use the legacy transfer events endpoint.\n\nThey should integrate with the new `/v2/events/funding/status` endpoint instead.\n\nAlso, all existing broker partners are now recommended to upgrade to the `/v2/events/funding/status` endpoint, which provides faster event delivery times.\n\n---\n\nThe Events API provides event push as well as historical queries via SSE (server sent events).\n\nYou can listen to transfer status updates as they get processed by our backoffice, for both end-user and firm accounts.\n\nHistorical events are streamed immediately if queried, and updates are pushed as events occur.\n\nQuery Params Rules:\n- `since` required if `until` specified\n- `since_id` required if `until_id` specified\n- `since_ulid` required if `until_ulid` specified\n- `since`, `since_id` or `since_ulid`  can’t be used at the same time\nBehavior:\n- if `since`, `since_id` or `since_ulid` not specified this will not return any historic data\n- if `until`, `until_id` or `until_ulid` reached stream will end (status 200)\n\n---\n\nNote for people using the clients generated from this OAS spec. Currently OAS-3 doesn't have full support for representing SSE style responses from an API, so if you are using a generated client and don't specify a `since` and `until` there is a good chance the generated clients will hang waiting for the response to end.\n\nIf you require the streaming capabilities we recommend not using the generated clients for this specific usecase until the OAS-3 standards come to a consensus on how to represent this correctly in OAS-3."
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
