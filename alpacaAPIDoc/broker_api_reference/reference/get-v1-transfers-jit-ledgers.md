---
source_view: https://docs.alpaca.markets/reference/get-v1-transfers-jit-ledgers
source_md: https://docs.alpaca.markets/reference/get-v1-transfers-jit-ledgers.md
scraped_at_utc: 2026-01-27T04:30:48Z
---
# Retrieve JIT Ledgers

Returns an array of objects that correspond to each ledger account, each of whichcontain the following attributes.

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
    "/v1/transfers/jit/ledgers": {
      "get": {
        "summary": "Retrieve JIT Ledgers",
        "tags": [
          "Funding"
        ],
        "responses": {
          "200": {
            "description": "OK",
            "content": {
              "application/json": {
                "schema": {
                  "type": "array",
                  "items": {
                    "title": "JITLedgerAccount",
                    "x-stoplight": {
                      "id": "8qgcugadp72ky"
                    },
                    "type": "object",
                    "properties": {
                      "id": {
                        "type": "string",
                        "description": "The ledger ID"
                      },
                      "ledger_name": {
                        "type": "string",
                        "x-stoplight": {
                          "id": "177un5yfjzo30"
                        },
                        "description": "The ledger name"
                      },
                      "status": {
                        "type": "string",
                        "x-stoplight": {
                          "id": "f1h0v5xllvutk"
                        }
                      },
                      "created_at": {
                        "type": "string",
                        "x-stoplight": {
                          "id": "v28v0514mevfi"
                        },
                        "description": "Creation time in UNIX format"
                      }
                    },
                    "x-examples": {
                      "Example 1": {
                        "id": "2896b9e2-3198-44cd-a08e-4cc4079aee33",
                        "ledger_name": "Securities JIT IN",
                        "status": "active",
                        "created_at": "1653532627"
                      }
                    },
                    "x-readme-ref-name": "JITLedgerAccount"
                  }
                }
              }
            }
          }
        },
        "operationId": "get-v1-transfers-jit-ledgers",
        "description": "Returns an array of objects that correspond to each ledger account, each of whichcontain the following attributes."
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
