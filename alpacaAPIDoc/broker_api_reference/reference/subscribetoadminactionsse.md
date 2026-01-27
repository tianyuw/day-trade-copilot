---
source_view: https://docs.alpaca.markets/reference/subscribetoadminactionsse
source_md: https://docs.alpaca.markets/reference/subscribetoadminactionsse.md
scraped_at_utc: 2026-01-27T04:30:48Z
---
# Subscribe to Admin Action Events (SSE)

The Events API provides event push as well as historical queries via SSE (server sent events).

This endpoint streams events related to administrative actions performed by our systems.

Historical events are streamed immediately if queried, and updates are pushed as events occur.

Query Params Rules:
- `since` required if `until` specified
- `since_id` required if `until_id` specified
- `since` and `since_id` can’t be used at the same time
Behavior:
- if `since` or `since_id` not specified this will not return any historic data
- if `until` or `until_id` reached stream will end (status 200)

---

Warning: Currently OAS-3 doesn't have full support for representing SSE style responses from an API.

In case the client code is generated from this OAS spec, don't specify a `since` and `until` there is a good chance the generated clients will hang forever waiting for the response to end.

If you require the streaming capabilities we recommend not using the generated clients for this specific endpoint until the OAS-3 standards come to a consensus on how to represent this behavior in OAS-3.

---

###  Comment messages
According to the SSE specification, any line that starts with a colon is a comment which does not contain data.  It is typically a free text that does not follow any data schema. A few examples mentioned below for comment messages.

#####  Slow client

The server sends a comment when the client is not consuming messages fast enough. Example: `: you are reading too slowly, dropped 10000 messages`

##### Internal server error

An error message is sent as a comment when the server closes the connection on an internal server error (only sent by the v2 and v2beta1 endpoints). Example: `: internal server error`

---

**Event Types**

- **LegacyNote:** Old free text based admin notes
- **Liquidation:** Event for a position liquidation which initialized by an admin
- **TransactionCancel:** Event for a manually cancelled transaction

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
    "/v2/events/admin-actions": {
      "get": {
        "summary": "Subscribe to Admin Action Events (SSE)",
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
                        "description": "Represents structure of a LegacyNote type AdminAction",
                        "x-examples": {
                          "example-1": {
                            "event_id": "01GTVS4FVS2KJDTPYH2WM6NAXF",
                            "at": "2023-03-06T16:38:01Z",
                            "belongs_to": {
                              "kind": "account",
                              "value": "0bbf1dd7-4235-4eca-8b1a-0db63572c735"
                            },
                            "created_by": {
                              "kind": "admin",
                              "value": "19455a3c-595f-457f-97b3-64a2b5aeae96"
                            },
                            "type": "legacy_note_admin_event",
                            "category": "other",
                            "visibility": "internal",
                            "note": "Performed action: Positions split AMZN (long): 1.011266402\n",
                            "correspondent": "LPCA",
                            "context": null
                          }
                        },
                        "allOf": [
                          {
                            "description": "Represents general fields for all AdminAction type",
                            "type": "object",
                            "title": "AdminActionEvent",
                            "properties": {
                              "event_id": {
                                "type": "string",
                                "format": "ulid",
                                "description": "Lexically sortable, monotonically increasing character array"
                              },
                              "replaces_event_id": {
                                "type": "string",
                                "format": "ulid",
                                "description": "Id of the replaced event (optional)"
                              },
                              "at": {
                                "type": "string",
                                "format": "date-time",
                                "description": "Timestamp of event"
                              },
                              "belongs_to": {
                                "description": "Represents structure of an Identifier for all AdminAction type",
                                "type": "object",
                                "title": "AdminActionBelongsTo",
                                "properties": {
                                  "kind": {
                                    "enum": [
                                      "account",
                                      "owner",
                                      "correspondent"
                                    ],
                                    "x-readme-ref-name": "AdminActionBelongsToKind"
                                  },
                                  "id_reference": {
                                    "type": "string"
                                  }
                                },
                                "x-readme-ref-name": "AdminActionBelongsTo"
                              },
                              "created_by": {
                                "description": "Represents structure of an Creator's Identifier for all AdminAction type\n",
                                "type": "object",
                                "title": "AdminActionCreatedBy",
                                "properties": {
                                  "kind": {
                                    "enum": [
                                      "admin"
                                    ],
                                    "x-readme-ref-name": "AdminActionCreatedByKind"
                                  },
                                  "id_reference": {
                                    "type": "string"
                                  }
                                },
                                "x-readme-ref-name": "AdminActionCreatedBy"
                              },
                              "type": {
                                "description": "Type of the Admin Action",
                                "enum": [
                                  "liquidation_admin_event",
                                  "legacy_note_admin_event",
                                  "transaction_cancel_admin_event"
                                ],
                                "x-readme-ref-name": "AdminActionType"
                              },
                              "category": {
                                "description": "Category of the Admin Action",
                                "enum": [
                                  "order",
                                  "other"
                                ],
                                "x-readme-ref-name": "AdminActionCategory"
                              },
                              "visibility": {
                                "description": "Visibility of the Admin Action",
                                "enum": [
                                  "internal",
                                  "external",
                                  "correspondent_only"
                                ],
                                "x-readme-ref-name": "AdminActionVisibility"
                              },
                              "note": {
                                "type": "string",
                                "description": "Free text form description of the admin action"
                              },
                              "correspondent": {
                                "type": "string",
                                "description": "Related correspondent"
                              }
                            },
                            "required": [
                              "event_id",
                              "at",
                              "belongs_to",
                              "created_by",
                              "type",
                              "category",
                              "visibility",
                              "note",
                              "correspondent",
                              "context"
                            ],
                            "x-readme-ref-name": "AdminActionEventGeneral"
                          },
                          {
                            "type": "object",
                            "title": "AdminActionContextLegacyNote",
                            "properties": {
                              "context": {
                                "description": "Variable schema type which depends on the type",
                                "type": "object"
                              }
                            }
                          }
                        ],
                        "x-readme-ref-name": "AdminActionLegacyNote"
                      },
                      {
                        "description": "Represents structure of a Liquidation type AdminAction",
                        "x-examples": {
                          "example-1": {
                            "event_id": "01GTVS4FVS2KJDTPYH2WM6NAXF",
                            "at": "2023-03-06T16:38:01Z",
                            "belongs_to": {
                              "kind": "account",
                              "value": "0bbf1dd7-4235-4eca-8b1a-0db63572c735"
                            },
                            "created_by": {
                              "kind": "admin",
                              "value": "19455a3c-595f-457f-97b3-64a2b5aeae96"
                            },
                            "type": "liquidation_admin_event",
                            "category": "accounts",
                            "visibility": "external",
                            "note": "Performed action: Position liquidated: Asset: TSLA, Quantity: 0.0001, Reason: Liquidation due to real time risk\n",
                            "correspondent": "LPCA",
                            "context": {
                              "symbol": "TSLA",
                              "reason": "Liquidation due to real time risk",
                              "available_qty": "0.0001",
                              "requested_qty": "0.0001",
                              "error": ""
                            }
                          }
                        },
                        "allOf": [
                          {
                            "description": "Represents general fields for all AdminAction type",
                            "type": "object",
                            "title": "AdminActionEvent",
                            "properties": {
                              "event_id": {
                                "type": "string",
                                "format": "ulid",
                                "description": "Lexically sortable, monotonically increasing character array"
                              },
                              "replaces_event_id": {
                                "type": "string",
                                "format": "ulid",
                                "description": "Id of the replaced event (optional)"
                              },
                              "at": {
                                "type": "string",
                                "format": "date-time",
                                "description": "Timestamp of event"
                              },
                              "belongs_to": {
                                "description": "Represents structure of an Identifier for all AdminAction type",
                                "type": "object",
                                "title": "AdminActionBelongsTo",
                                "properties": {
                                  "kind": {
                                    "enum": [
                                      "account",
                                      "owner",
                                      "correspondent"
                                    ],
                                    "x-readme-ref-name": "AdminActionBelongsToKind"
                                  },
                                  "id_reference": {
                                    "type": "string"
                                  }
                                },
                                "x-readme-ref-name": "AdminActionBelongsTo"
                              },
                              "created_by": {
                                "description": "Represents structure of an Creator's Identifier for all AdminAction type\n",
                                "type": "object",
                                "title": "AdminActionCreatedBy",
                                "properties": {
                                  "kind": {
                                    "enum": [
                                      "admin"
                                    ],
                                    "x-readme-ref-name": "AdminActionCreatedByKind"
                                  },
                                  "id_reference": {
                                    "type": "string"
                                  }
                                },
                                "x-readme-ref-name": "AdminActionCreatedBy"
                              },
                              "type": {
                                "description": "Type of the Admin Action",
                                "enum": [
                                  "liquidation_admin_event",
                                  "legacy_note_admin_event",
                                  "transaction_cancel_admin_event"
                                ],
                                "x-readme-ref-name": "AdminActionType"
                              },
                              "category": {
                                "description": "Category of the Admin Action",
                                "enum": [
                                  "order",
                                  "other"
                                ],
                                "x-readme-ref-name": "AdminActionCategory"
                              },
                              "visibility": {
                                "description": "Visibility of the Admin Action",
                                "enum": [
                                  "internal",
                                  "external",
                                  "correspondent_only"
                                ],
                                "x-readme-ref-name": "AdminActionVisibility"
                              },
                              "note": {
                                "type": "string",
                                "description": "Free text form description of the admin action"
                              },
                              "correspondent": {
                                "type": "string",
                                "description": "Related correspondent"
                              }
                            },
                            "required": [
                              "event_id",
                              "at",
                              "belongs_to",
                              "created_by",
                              "type",
                              "category",
                              "visibility",
                              "note",
                              "correspondent",
                              "context"
                            ],
                            "x-readme-ref-name": "AdminActionEventGeneral"
                          },
                          {
                            "type": "object",
                            "title": "AdminActionContextLiquidation",
                            "properties": {
                              "context": {
                                "description": "Variable schema type which depends on the type",
                                "type": "object",
                                "properties": {
                                  "symbol": {
                                    "type": "string"
                                  },
                                  "reason": {
                                    "type": "string"
                                  },
                                  "available_qty": {
                                    "type": "string",
                                    "format": "decimal"
                                  },
                                  "requested_qty": {
                                    "type": "string",
                                    "format": "decimal"
                                  },
                                  "error": {
                                    "type": "string"
                                  }
                                }
                              }
                            }
                          }
                        ],
                        "x-readme-ref-name": "AdminActionLiquidation"
                      },
                      {
                        "description": "Represents structure of a TransactionCancel type AdminAction",
                        "x-examples": {
                          "example-1": {
                            "event_id": "01GTVS4FVS2KJDTPYH2WM6NAXF",
                            "at": "2023-03-06T16:38:01Z",
                            "belongs_to": {
                              "kind": "account",
                              "value": "0bbf1dd7-4235-4eca-8b1a-0db63572c735"
                            },
                            "created_by": {
                              "kind": "admin",
                              "value": "19455a3c-595f-457f-97b3-64a2b5aeae96"
                            },
                            "type": "transaction_cancel_admin_event",
                            "category": "accounts",
                            "visibility": "external",
                            "note": "\"Transaction fdf18af2-142b-409e-8aad-d1731e276af0 cancelled for LPCA-12345678\n",
                            "correspondent": "LPCA",
                            "context": {
                              "transaction_id": "fdf18af2-142b-409e-8aad-d1731e276af0",
                              "entry_type": "JNLC",
                              "external_id": "d5eede2c-1c08-45df-9800-87ad5eefc11f"
                            }
                          }
                        },
                        "allOf": [
                          {
                            "description": "Represents general fields for all AdminAction type",
                            "type": "object",
                            "title": "AdminActionEvent",
                            "properties": {
                              "event_id": {
                                "type": "string",
                                "format": "ulid",
                                "description": "Lexically sortable, monotonically increasing character array"
                              },
                              "replaces_event_id": {
                                "type": "string",
                                "format": "ulid",
                                "description": "Id of the replaced event (optional)"
                              },
                              "at": {
                                "type": "string",
                                "format": "date-time",
                                "description": "Timestamp of event"
                              },
                              "belongs_to": {
                                "description": "Represents structure of an Identifier for all AdminAction type",
                                "type": "object",
                                "title": "AdminActionBelongsTo",
                                "properties": {
                                  "kind": {
                                    "enum": [
                                      "account",
                                      "owner",
                                      "correspondent"
                                    ],
                                    "x-readme-ref-name": "AdminActionBelongsToKind"
                                  },
                                  "id_reference": {
                                    "type": "string"
                                  }
                                },
                                "x-readme-ref-name": "AdminActionBelongsTo"
                              },
                              "created_by": {
                                "description": "Represents structure of an Creator's Identifier for all AdminAction type\n",
                                "type": "object",
                                "title": "AdminActionCreatedBy",
                                "properties": {
                                  "kind": {
                                    "enum": [
                                      "admin"
                                    ],
                                    "x-readme-ref-name": "AdminActionCreatedByKind"
                                  },
                                  "id_reference": {
                                    "type": "string"
                                  }
                                },
                                "x-readme-ref-name": "AdminActionCreatedBy"
                              },
                              "type": {
                                "description": "Type of the Admin Action",
                                "enum": [
                                  "liquidation_admin_event",
                                  "legacy_note_admin_event",
                                  "transaction_cancel_admin_event"
                                ],
                                "x-readme-ref-name": "AdminActionType"
                              },
                              "category": {
                                "description": "Category of the Admin Action",
                                "enum": [
                                  "order",
                                  "other"
                                ],
                                "x-readme-ref-name": "AdminActionCategory"
                              },
                              "visibility": {
                                "description": "Visibility of the Admin Action",
                                "enum": [
                                  "internal",
                                  "external",
                                  "correspondent_only"
                                ],
                                "x-readme-ref-name": "AdminActionVisibility"
                              },
                              "note": {
                                "type": "string",
                                "description": "Free text form description of the admin action"
                              },
                              "correspondent": {
                                "type": "string",
                                "description": "Related correspondent"
                              }
                            },
                            "required": [
                              "event_id",
                              "at",
                              "belongs_to",
                              "created_by",
                              "type",
                              "category",
                              "visibility",
                              "note",
                              "correspondent",
                              "context"
                            ],
                            "x-readme-ref-name": "AdminActionEventGeneral"
                          },
                          {
                            "type": "object",
                            "title": "AdminActionContextTransactionCancel",
                            "properties": {
                              "context": {
                                "description": "Variable schema type which depends on the type",
                                "type": "object",
                                "properties": {
                                  "transaction_id": {
                                    "type": "string",
                                    "format": "uuid"
                                  },
                                  "entry_type": {
                                    "type": "string"
                                  },
                                  "external_id": {
                                    "type": "string"
                                  }
                                }
                              }
                            }
                          }
                        ],
                        "x-readme-ref-name": "AdminActionTransactionCancel"
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
              "format": "date-time"
            },
            "description": "Format: RFC3339 or YYYY-MM-DD"
          },
          {
            "name": "until",
            "in": "query",
            "schema": {
              "type": "string",
              "format": "date-time"
            },
            "description": "Format: RFC3339 or YYYY-MM-DD"
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
          }
        ],
        "operationId": "subscribeToAdminActionSSE",
        "description": "The Events API provides event push as well as historical queries via SSE (server sent events).\n\nThis endpoint streams events related to administrative actions performed by our systems.\n\nHistorical events are streamed immediately if queried, and updates are pushed as events occur.\n\nQuery Params Rules:\n- `since` required if `until` specified\n- `since_id` required if `until_id` specified\n- `since` and `since_id` can’t be used at the same time\nBehavior:\n- if `since` or `since_id` not specified this will not return any historic data\n- if `until` or `until_id` reached stream will end (status 200)\n\n---\n\nWarning: Currently OAS-3 doesn't have full support for representing SSE style responses from an API.\n\nIn case the client code is generated from this OAS spec, don't specify a `since` and `until` there is a good chance the generated clients will hang forever waiting for the response to end.\n\nIf you require the streaming capabilities we recommend not using the generated clients for this specific endpoint until the OAS-3 standards come to a consensus on how to represent this behavior in OAS-3.\n\n---\n\n###  Comment messages\nAccording to the SSE specification, any line that starts with a colon is a comment which does not contain data.  It is typically a free text that does not follow any data schema. A few examples mentioned below for comment messages.\n\n#####  Slow client\n\nThe server sends a comment when the client is not consuming messages fast enough. Example: `: you are reading too slowly, dropped 10000 messages`\n\n##### Internal server error\n\nAn error message is sent as a comment when the server closes the connection on an internal server error (only sent by the v2 and v2beta1 endpoints). Example: `: internal server error`\n\n---\n\n**Event Types**\n\n- **LegacyNote:** Old free text based admin notes\n- **Liquidation:** Event for a position liquidation which initialized by an admin\n- **TransactionCancel:** Event for a manually cancelled transaction"
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
