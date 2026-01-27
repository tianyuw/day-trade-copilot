---
source_view: https://docs.alpaca.markets/reference/subscribetojournalstatusv2sse
source_md: https://docs.alpaca.markets/reference/subscribetojournalstatusv2sse.md
scraped_at_utc: 2026-01-27T04:30:48Z
---
# Subscribe to Journal Events (SSE)

The Events API provides event push as well as historical queries via SSE (server sent events).

You can listen to journal status updates as they get processed by our backoffice.

Historical events are streamed immediately if queried, and updates are pushed as events occur.

Query Params Rules:
- `since` required if `until` specified
- `since_id` required if `until_id` specified
- `since` and `since_id` can’t be used at the same time
- `until` and `until_id` can’t be used at the same time
Behavior:
- if `since` or `since_ulid` not specified this will not return any historic data
- if `until` or `until_id` reached stream will end (status 200)

---

There is no compatibility between /v1/events/journals/status and /v2/events/journals/status, the ids (ulid) are always different, and the number of events might also different

Please note that the new `/v2` endpoint, is the same as, and was originally available under `/v2beta1`.
We encourage all customers to adjust their codebase from that interim beta endpoint to the `/v2` stable endpoint.
In the near future we will setup permanent redirect from `/v2beta1` to `/v2` before we completely remove the beta endpoint.

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
    "/v2/events/journals/status": {
      "get": {
        "summary": "Subscribe to Journal Events (SSE)",
        "tags": [
          "Events"
        ],
        "description": "The Events API provides event push as well as historical queries via SSE (server sent events).\n\nYou can listen to journal status updates as they get processed by our backoffice.\n\nHistorical events are streamed immediately if queried, and updates are pushed as events occur.\n\nQuery Params Rules:\n- `since` required if `until` specified\n- `since_id` required if `until_id` specified\n- `since` and `since_id` can’t be used at the same time\n- `until` and `until_id` can’t be used at the same time\nBehavior:\n- if `since` or `since_ulid` not specified this will not return any historic data\n- if `until` or `until_id` reached stream will end (status 200)\n\n---\n\nThere is no compatibility between /v1/events/journals/status and /v2/events/journals/status, the ids (ulid) are always different, and the number of events might also different\n\nPlease note that the new `/v2` endpoint, is the same as, and was originally available under `/v2beta1`.\nWe encourage all customers to adjust their codebase from that interim beta endpoint to the `/v2` stable endpoint.\nIn the near future we will setup permanent redirect from `/v2beta1` to `/v2` before we completely remove the beta endpoint.\n\n---\n\nNote for people using the clients generated from this OAS spec. Currently OAS-3 doesn't have full support for representing SSE style responses from an API, so if you are using a generated client and don't specify a `since` and `until` there is a good chance the generated clients will hang waiting for the response to end.\n\nIf you require the streaming capabilities we recommend not using the generated clients for this specific usecase until the OAS-3 standards come to a consensus on how to represent this correctly in OAS-3.\n",
        "parameters": [
          {
            "name": "since",
            "in": "query",
            "schema": {
              "type": "string",
              "format": "date-time"
            },
            "description": "Format: YYYY-MM-DD"
          },
          {
            "name": "until",
            "in": "query",
            "schema": {
              "type": "string",
              "format": "date-time"
            },
            "description": "Format: YYYY-MM-DD"
          },
          {
            "name": "since_id",
            "in": "query",
            "schema": {
              "type": "string",
              "format": "ulid"
            }
          },
          {
            "name": "until_id",
            "in": "query",
            "schema": {
              "type": "string",
              "format": "ulid"
            }
          },
          {
            "schema": {
              "type": "string"
            },
            "in": "query",
            "name": "id"
          }
        ],
        "responses": {
          "200": {
            "description": "Connected. Events will now start streaming as long as you keep the connection open.",
            "content": {
              "text/event-stream": {
                "schema": {
                  "type": "array",
                  "items": {
                    "description": "Represents a change in a Journal's status, sent over the events streaming api.\n",
                    "type": "object",
                    "x-examples": {
                      "example-1": {
                        "at": "2021-05-07T10:28:23.163857Z",
                        "entry_type": "JNLC",
                        "event_id": "01F535Y1FVY8WZHE763HCNS8SZ",
                        "journal_id": "2f144d2a-91e6-46ff-8e37-959a701cc58d",
                        "status_from": "",
                        "status_to": "queued",
                        "description": "Journal of cash between accounts"
                      },
                      "example-idempotency-key": {
                        "at": "2021-05-07T10:28:23.163857Z",
                        "entry_type": "JNLC",
                        "event_id": "01F535Y1FVY8WZHE763HCNS8SZ",
                        "journal_id": "2f144d2a-91e6-46ff-8e37-959a701cc58d",
                        "status_from": "queued",
                        "status_to": "executed",
                        "description": "Journal of cash between accounts",
                        "idempotency_key": "72bdf18f-7410-43ec-b4e8-b6e41c5c0160",
                        "idempotency_key_type": "single"
                      }
                    },
                    "title": "JournalStatusEvent",
                    "properties": {
                      "at": {
                        "type": "string",
                        "minLength": 1,
                        "description": "Timestamp of event",
                        "format": "date-time"
                      },
                      "entry_type": {
                        "type": "string",
                        "title": "",
                        "description": "This enum represents the various kinds of Journal alpaca supports.\n\nCurrent values are:\n\n- **JNLC**\n\n  Journal Cash between accounts\n\n- **JNLS**\n\n  Journal Securities between accounts",
                        "enum": [
                          "JNLC",
                          "JNLS"
                        ],
                        "x-stoplight": {
                          "id": "itme4epinxsnk"
                        },
                        "x-readme-ref-name": "JournalEntryType"
                      },
                      "event_id": {
                        "type": "string",
                        "format": "ulid",
                        "description": "lexically sortable, monotonically increasing character array"
                      },
                      "journal_id": {
                        "type": "string",
                        "description": "The UUID of the related Journal",
                        "format": "uuid"
                      },
                      "status_from": {
                        "type": "string",
                        "enum": [
                          "pending",
                          "canceled",
                          "executed",
                          "queued",
                          "rejected",
                          "deleted",
                          "refused",
                          "sent_to_clearing",
                          "correct"
                        ],
                        "description": "Represents the status that a Journal instance can be in.\n\n**Current Values**\n\nqueued\tJournal in queue to be processed. Journal is not processed yet.\n\nsent_to_clearing\tJournal sent to be processed by Alpaca’s booking system. The journal is not processed yet.\n\npending\t    Journal pending to be processed as it requires manual approval from Alpaca operations (for example due to hitting JNLC daily limits).\n\nexecuted\tJournal executed and balances updated for both sides of \nthe journal transaction. This is not a final status, journals can be reversed if there is an error.\n\nrejected\tJournal rejected. Please try again.\n\ncanceled\tJournal canceled. This is a **FINAL** status.\n\nrefused\tJournal refused. Please try again.\n\ndeleted\tJournal deleted. This is a **FINAL** status.\n\ncorrect\tJournal is corrected. Previously executed journal is cancelled and a new journal is corrected amount is created. This is a **FINAL** status.",
                        "x-stoplight": {
                          "id": "ay4nu4z1j11cu"
                        },
                        "x-readme-ref-name": "JournalStatus"
                      },
                      "status_to": {
                        "type": "string",
                        "enum": [
                          "pending",
                          "canceled",
                          "executed",
                          "queued",
                          "rejected",
                          "deleted",
                          "refused",
                          "sent_to_clearing",
                          "correct"
                        ],
                        "description": "Represents the status that a Journal instance can be in.\n\n**Current Values**\n\nqueued\tJournal in queue to be processed. Journal is not processed yet.\n\nsent_to_clearing\tJournal sent to be processed by Alpaca’s booking system. The journal is not processed yet.\n\npending\t    Journal pending to be processed as it requires manual approval from Alpaca operations (for example due to hitting JNLC daily limits).\n\nexecuted\tJournal executed and balances updated for both sides of \nthe journal transaction. This is not a final status, journals can be reversed if there is an error.\n\nrejected\tJournal rejected. Please try again.\n\ncanceled\tJournal canceled. This is a **FINAL** status.\n\nrefused\tJournal refused. Please try again.\n\ndeleted\tJournal deleted. This is a **FINAL** status.\n\ncorrect\tJournal is corrected. Previously executed journal is cancelled and a new journal is corrected amount is created. This is a **FINAL** status.",
                        "x-stoplight": {
                          "id": "ay4nu4z1j11cu"
                        },
                        "x-readme-ref-name": "JournalStatus"
                      },
                      "description": {
                        "type": "string",
                        "description": "The description of the journal event when submitted",
                        "example": "Journal of cash between accounts"
                      },
                      "idempotency_key": {
                        "type": "string",
                        "description": "The idempotency key of the journal event",
                        "format": "uuid"
                      },
                      "idempotency_key_type": {
                        "type": "string",
                        "description": "The type of idempotency key",
                        "enum": [
                          "single",
                          "batch"
                        ]
                      },
                      "batch_error_message": {
                        "type": "string",
                        "description": "If journal submitted in batch (that is, idempotency_key_type is batch), this is the error message of the batch journal execution."
                      }
                    },
                    "required": [
                      "at",
                      "entry_type",
                      "event_id",
                      "journal_id",
                      "status_from",
                      "status_to"
                    ],
                    "x-stoplight": {
                      "id": "0pbdls2h4h8zb"
                    },
                    "x-readme-ref-name": "JournalStatusEventV2"
                  }
                }
              }
            }
          }
        },
        "operationId": "subscribeToJournalStatusV2SSE"
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
