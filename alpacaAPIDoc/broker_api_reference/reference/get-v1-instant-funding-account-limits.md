---
source_view: https://docs.alpaca.markets/reference/get-v1-instant-funding-account-limits
source_md: https://docs.alpaca.markets/reference/get-v1-instant-funding-account-limits.md
scraped_at_utc: 2026-01-27T04:30:48Z
---
# Get instant funding account limits

Returns the limits for individual partner accounts.

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
      "name": "Instant Funding"
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
    "/v1/instant_funding/limits/accounts": {
      "get": {
        "description": "Returns the limits for individual partner accounts.",
        "summary": "Get instant funding account limits",
        "operationId": "get-v1-instant-funding-account-limits",
        "tags": [
          "Instant Funding"
        ],
        "parameters": [
          {
            "name": "account_numbers",
            "in": "query",
            "description": "filter limits based on comma separated account_numbers",
            "required": true,
            "style": "form",
            "explode": false,
            "schema": {
              "type": "array",
              "items": {
                "type": "string"
              }
            }
          }
        ],
        "responses": {
          "200": {
            "description": "invidual broker account limits",
            "content": {
              "application/json": {
                "schema": {
                  "type": "array",
                  "items": {
                    "type": "object",
                    "required": [
                      "account_no",
                      "amount_in_use",
                      "amount_available",
                      "amount_limit"
                    ],
                    "properties": {
                      "account_no": {
                        "type": "string"
                      },
                      "amount_in_use": {
                        "type": "string",
                        "format": "decimal"
                      },
                      "amount_available": {
                        "type": "string",
                        "format": "decimal"
                      },
                      "amount_limit": {
                        "type": "string",
                        "format": "decimal"
                      }
                    },
                    "x-readme-ref-name": "AccountLimit"
                  }
                }
              }
            }
          },
          "default": {
            "description": "error",
            "content": {
              "application/json": {
                "schema": {
                  "title": "Error",
                  "type": "object",
                  "properties": {
                    "code": {
                      "type": "number"
                    },
                    "message": {
                      "type": "string"
                    }
                  },
                  "required": [
                    "code",
                    "message"
                  ],
                  "x-stoplight": {
                    "id": "xu9mkrgjdtotd"
                  },
                  "x-readme-ref-name": "Error"
                }
              }
            }
          }
        }
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
