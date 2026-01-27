---
source_view: https://docs.alpaca.markets/reference/getalljournals
source_md: https://docs.alpaca.markets/reference/getalljournals.md
scraped_at_utc: 2026-01-27T04:30:48Z
---
# Retrieve a List Journals

Returns an array of journal objects.

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
    "/v1/journals": {
      "get": {
        "summary": "Retrieve a List Journals",
        "tags": [
          "Journals"
        ],
        "parameters": [
          {
            "name": "after",
            "in": "query",
            "schema": {
              "type": "string",
              "format": "date"
            },
            "description": "By journal creation date. Format: 2020-01-01"
          },
          {
            "name": "before",
            "in": "query",
            "schema": {
              "type": "string",
              "format": "date"
            },
            "description": "By journal creation date. Format: 2020-01-01"
          },
          {
            "name": "status",
            "in": "query",
            "schema": {
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
              ]
            },
            "description": "See the JournalStatus model for more info"
          },
          {
            "name": "entry_type",
            "in": "query",
            "schema": {
              "type": "string",
              "enum": [
                "JNLC",
                "JNLS"
              ]
            },
            "description": "JNLC or JNLS"
          },
          {
            "name": "to_account",
            "in": "query",
            "schema": {
              "type": "string",
              "format": "uuid"
            },
            "description": "The account id that received the journal"
          },
          {
            "name": "from_account",
            "in": "query",
            "schema": {
              "type": "string",
              "format": "uuid"
            },
            "description": "The account id that initiated the journal"
          },
          {
            "name": "limit",
            "in": "query",
            "description": "The maximum number of results to return",
            "required": false,
            "schema": {
              "type": "integer"
            }
          }
        ],
        "responses": {
          "200": {
            "description": "OK",
            "content": {
              "application/json": {
                "schema": {
                  "discriminator": {
                    "propertyName": "entry_type",
                    "mapping": {
                      "JNLC": "#/components/schemas/JNLC",
                      "JNLS": "#/components/schemas/JNLS"
                    }
                  },
                  "type": "array",
                  "items": {
                    "title": "Journal",
                    "example": {
                      "id": "h7h5g33f-ef01-4458-9a4b-9598727a406f",
                      "entry_type": "JNLS",
                      "from_account": "8fjkjn-4483-4199-840f-6c5fe0b7ca24",
                      "to_account": "3gtt65jd-6f2a-433c-8c33-17b66b8941fa",
                      "status": "executed",
                      "symbol": "AAPL",
                      "qty": "2",
                      "settle_date": "2020-12-24",
                      "price": "128.23"
                    },
                    "x-examples": {
                      "example": {
                        "id": "h7h5g33f-ef01-4458-9a4b-9598727a406f",
                        "entry_type": "JNLS",
                        "from_account": "8fjkjn-4483-4199-840f-6c5fe0b7ca24",
                        "to_account": "3gtt65jd-6f2a-433c-8c33-17b66b8941fa",
                        "status": "executed",
                        "symbol": "AAPL",
                        "qty": "2",
                        "settle_date": "2020-12-24",
                        "price": "128.23"
                      },
                      "example-pending": {
                        "id": "6d2cba43-cb57-4534-9603-a6e159167c0a",
                        "entry_type": "JNLC",
                        "from_account": "3dcb795c-3ccc-402a-abb9-07e26a1b1326",
                        "to_account": "2a87c088-ffb6-472b-a4a3-cd9305c8605c",
                        "symbol": null,
                        "qty": null,
                        "price": "0",
                        "status": "pending",
                        "settle_date": "2022-02-17",
                        "system_date": "2022-02-17",
                        "net_amount": "645",
                        "description": ""
                      },
                      "example-queued": {
                        "id": "6d2cba43-cb57-4534-9603-a6e159167c0a",
                        "entry_type": "JNLC",
                        "from_account": "3dcb795c-3ccc-402a-abb9-07e26a1b1326",
                        "to_account": "2a87c088-ffb6-472b-a4a3-cd9305c8605c",
                        "symbol": "",
                        "qty": null,
                        "price": "0",
                        "status": "queued",
                        "settle_date": null,
                        "system_date": null,
                        "net_amount": "645",
                        "description": ""
                      }
                    },
                    "description": "Represents a cash or security transfer between accounts, as specified by the `entry_type` parameter.",
                    "allOf": [
                      {
                        "type": "object",
                        "required": [
                          "id",
                          "entry_type",
                          "from_account",
                          "to_account",
                          "settle_date"
                        ],
                        "properties": {
                          "id": {
                            "type": "string",
                            "format": "uuid",
                            "description": "journal ID"
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
                          "from_account": {
                            "type": "string",
                            "format": "uuid",
                            "description": "account ID the shares go from"
                          },
                          "to_account": {
                            "type": "string",
                            "format": "uuid",
                            "description": "account ID the shares go to"
                          },
                          "settle_date": {
                            "type": "string",
                            "format": "date"
                          },
                          "status": {
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
                          "transmitter_info": {
                            "type": "object",
                            "description": "Information about the transmitter to satisfy travel rule requirements. Required if the requesting correspondent qualifies as a financial institution\n",
                            "properties": {
                              "originator_full_name": {
                                "type": "string",
                                "description": "Required if the requesting correspondent qualifies as a financial institution\n"
                              },
                              "originator_street_address": {
                                "type": "string"
                              },
                              "originator_state": {
                                "type": "string"
                              },
                              "originator_city": {
                                "type": "string"
                              },
                              "originator_postal_code": {
                                "type": "string"
                              },
                              "originator_country": {
                                "type": "string",
                                "description": "Required if the requesting correspondent qualifies as a financial institution\n"
                              },
                              "originator_bank_account_number": {
                                "type": "string",
                                "description": "Required if the requesting correspondent qualifies as a financial institution\n"
                              },
                              "originator_bank_name": {
                                "type": "string",
                                "description": "Required if the requesting correspondent qualifies as a financial institution\n"
                              },
                              "other_identifying_information": {
                                "type": "string",
                                "description": "Used to facilitate transfer lookup in the event it is required. Recommended to be the originating bank's reference number for the transfer\n"
                              }
                            },
                            "x-readme-ref-name": "TransmitterInfo"
                          },
                          "created_at": {
                            "type": "string",
                            "format": "date-time"
                          }
                        }
                      },
                      {
                        "oneOf": [
                          {
                            "type": "object",
                            "x-examples": {
                              "Example 1": {
                                "id": "f45g67h8-d1fc-4136-aa4f-cf4460aecdfc",
                                "to_account": "g7h7rg66-6f2a-433c-8c33-17b66b8941fa",
                                "entry_type": "JNLS",
                                "symbol": "AAPL",
                                "qty": "0.5",
                                "price": "128.23",
                                "status": "executed",
                                "from_account": "8k4f3d-4483-4199-840f-6c5fe0b7ca24",
                                "settle_date": "2020-12-24",
                                "system_date": "2020-12-24",
                                "description": "this is a test journal"
                              }
                            },
                            "properties": {
                              "id": {
                                "type": "string",
                                "description": "The journal ID"
                              },
                              "to_account": {
                                "type": "string",
                                "description": "The account ID that received the journal - account_status must equal to ACTIVE"
                              },
                              "entry_type": {
                                "type": "string",
                                "description": "JNLS"
                              },
                              "symbol": {
                                "type": "string",
                                "description": "The symbol of the security journaled"
                              },
                              "qty": {
                                "type": "string",
                                "description": "The quantity of the securities journaled"
                              },
                              "price": {
                                "type": "string",
                                "description": "The price of the security journaled"
                              },
                              "status": {
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
                              "from_account": {
                                "type": "string",
                                "description": "The account ID that initiates the journal - account_status must equal to ACTIVE or CLOSE"
                              },
                              "settle_date": {
                                "type": "string",
                                "description": "Date string in “%Y-%m-%d” format"
                              },
                              "system_date": {
                                "type": "string",
                                "description": "Date string in “%Y-%m-%d” format"
                              },
                              "description": {
                                "type": "string"
                              },
                              "currency": {
                                "type": "string",
                                "x-stoplight": {
                                  "id": "29s5ect4watc4"
                                },
                                "description": "Currency denomination of the journal. USD by default."
                              }
                            },
                            "x-readme-ref-name": "JNLS"
                          },
                          {
                            "example": {
                              "id": "f45g67h8-d1fc-4136-aa4f-cf4460aecdfc",
                              "entry_type": "JNLC",
                              "from_account": "8fjkjn-4483-4199-840f-6c5fe0b7ca24",
                              "to_account": "3gtt65jd-6f2a-433c-8c33-17b66b8941fa",
                              "status": "pending",
                              "net_amount": "115.5"
                            },
                            "description": "Journal information specific to cash transfers. This field is required for `Journal`s with an `entry_type` of `jnlc` (cash transfers), but will be null for those with `jnls` (securities transfers).",
                            "type": "object",
                            "title": "JNLC",
                            "properties": {
                              "description": {
                                "type": "string",
                                "description": "ID the amount goes to. Only valid for JNLC journals. Null for JNLS."
                              },
                              "net_amount": {
                                "type": "string",
                                "format": "decimal",
                                "description": "Only valid for JNLC journals. Null for JNLS."
                              },
                              "transmitter_name": {
                                "type": "string",
                                "description": "Only valid for JNLC journals. Null for JNLS. Max 255 characters."
                              },
                              "transmitter_account_number": {
                                "type": "string",
                                "description": "Only valid for JNLC journals. Null for JNLS.max 255 characters"
                              },
                              "transmitter_address": {
                                "type": "string",
                                "description": "Only valid for JNLC journals. Null for JNLS.max 255 characters"
                              },
                              "transmitter_financial_institution": {
                                "type": "string",
                                "description": "Only valid for JNLC journals. Null for JNLS.max 255 characters"
                              },
                              "transmitter_timestamp": {
                                "type": "string",
                                "format": "date-time",
                                "description": "Only valid for JNLC journals. Null for JNLS."
                              }
                            },
                            "required": [
                              "net_amount"
                            ],
                            "x-examples": {},
                            "x-stoplight": {
                              "id": "qo2ttptb2frpx"
                            },
                            "x-readme-ref-name": "JNLC"
                          }
                        ]
                      }
                    ],
                    "x-stoplight": {
                      "id": "2isltcm8hzb23"
                    },
                    "x-readme-ref-name": "Journal"
                  }
                }
              }
            }
          },
          "400": {
            "description": "One of the parameters is invalid.",
            "content": {
              "application/json": {
                "schema": {
                  "type": "string"
                }
              }
            }
          },
          "422": {
            "description": "Result set exceeds 100,000 records.",
            "content": {
              "application/json": {
                "schema": {
                  "type": "string"
                }
              }
            }
          }
        },
        "operationId": "getAllJournals",
        "description": "Returns an array of journal objects."
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
