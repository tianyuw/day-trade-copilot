---
source_view: https://docs.alpaca.markets/reference/get-v1-transfers-jit-ledger_id-balances
source_md: https://docs.alpaca.markets/reference/get-v1-transfers-jit-ledger_id-balances.md
scraped_at_utc: 2026-01-27T04:30:48Z
---
# Retrieve JIT Ledger Balances

Returns an array of objects that correspond to each ledger account.

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
    "/v1/transfers/jit/{ledger_id}/balances": {
      "get": {
        "summary": "Retrieve JIT Ledger Balances",
        "tags": [
          "Funding"
        ],
        "parameters": [
          {
            "name": "ledger_id",
            "schema": {
              "type": "string"
            },
            "in": "path",
            "required": true
          },
          {
            "name": "start_date",
            "in": "query",
            "schema": {
              "type": "string",
              "format": "date"
            },
            "description": "The start date (inclusive) of the ledgerbalances and activities."
          },
          {
            "name": "end_date",
            "in": "query",
            "schema": {
              "type": "string",
              "format": "date"
            },
            "description": "The end date (inclusive) of the ledgerbalances and activities."
          }
        ],
        "responses": {
          "200": {
            "description": "OK",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "id": {
                      "type": "string",
                      "x-stoplight": {
                        "id": "i93oh1b7w2em9"
                      },
                      "description": "The ledger ID"
                    },
                    "ledger_no": {
                      "type": "string",
                      "x-stoplight": {
                        "id": "ybo7l8ty2z4ba"
                      },
                      "description": "The ledger account number"
                    },
                    "ledger_name": {
                      "type": "string",
                      "x-stoplight": {
                        "id": "g2430brqomb76"
                      },
                      "description": "The ledger name"
                    },
                    "transactions": {
                      "type": "array",
                      "x-stoplight": {
                        "id": "7jnr31tbri9l0"
                      },
                      "items": {
                        "type": "object",
                        "x-examples": {
                          "Example 1": {
                            "account_id": "06b9d76e-1733-460c-844e-48d1ae0f10c3",
                            "account_no": "JTRJITS00",
                            "account_name": "Just In Time Receivable - JITS",
                            "system_date": "2022-06-10",
                            "entry_type": "JNLC",
                            "description": "debit balance = 4185.36, base_rate = 0.0375, spread = 0.05",
                            "contra_account_name": "Just In Time Interest Income",
                            "amount": "1",
                            "balance": "4186.36"
                          }
                        },
                        "properties": {
                          "account_id": {
                            "type": "string",
                            "description": "The ledger ID"
                          },
                          "account_no": {
                            "type": "string",
                            "description": "The ledger account number"
                          },
                          "account_name": {
                            "type": "string",
                            "description": "The ledger name"
                          },
                          "system_date": {
                            "type": "string",
                            "description": "Date of transaction"
                          },
                          "entry_type": {
                            "type": "string",
                            "description": "Type of transaction"
                          },
                          "description": {
                            "type": "string",
                            "description": "Plain text overview of the transaction"
                          },
                          "contra_account_name": {
                            "type": "string",
                            "description": "Contra account of transaction"
                          },
                          "amount": {
                            "type": "string",
                            "description": "Total amount of the transaction"
                          },
                          "balance": {
                            "type": "string",
                            "description": "Ending balance after thetransaction has been applied"
                          }
                        },
                        "x-readme-ref-name": "Transaction"
                      }
                    },
                    "starting_balance": {
                      "type": "string",
                      "x-stoplight": {
                        "id": "19ncib5wve17o"
                      },
                      "description": "Ledger balance at the beginning of the date range",
                      "format": "decimal"
                    },
                    "ending_balance": {
                      "type": "string",
                      "x-stoplight": {
                        "id": "etolgr1qisrz5"
                      },
                      "description": "Ledger balance at the end of the date range",
                      "format": "decimal"
                    },
                    "activity_amount": {
                      "type": "string",
                      "x-stoplight": {
                        "id": "eon4dv0x49fvs"
                      },
                      "description": "The number of transactions related to the ledger during the specified date range ",
                      "format": "decimal"
                    }
                  }
                }
              }
            }
          }
        },
        "operationId": "get-v1-transfers-jit-ledger_id-balances",
        "description": "Returns an array of objects that correspond to each ledger account."
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
