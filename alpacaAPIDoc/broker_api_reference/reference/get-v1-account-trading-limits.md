---
source_view: https://docs.alpaca.markets/reference/get-v1-account-trading-limits
source_md: https://docs.alpaca.markets/reference/get-v1-account-trading-limits.md
scraped_at_utc: 2026-01-27T04:30:48Z
---
# Retrieve real-time Trading Limits for an Account

This endpoint is only available to accounts with the trading limits feature enabled, and not on JIT.
The daily trading limit is set at the correspondent level (or the account level) and is used as the limit for the total amount due to Alpaca on the date of settlement.
The limit in use returns the real time usage of this limit, based on the setup it uses the usage is calculated differently.
If the limit in use reaches the `daily_net_limit` or `available` is zero, further purchasing activity will be halted, however, the limit can be adjusted by reaching out to Alpaca with the proposed new limit and the reason for the change.

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
      "name": "Trading"
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
    "/v1/trading/accounts/{account_id}/limits": {
      "get": {
        "summary": "Retrieve real-time Trading Limits for an Account",
        "tags": [
          "Trading"
        ],
        "parameters": [
          {
            "schema": {
              "type": "string"
            },
            "name": "account_id",
            "in": "path",
            "required": true
          }
        ],
        "responses": {
          "200": {
            "description": "Returns the trading limit set for the account and the real-time usage of the limit",
            "content": {
              "application/json": {
                "schema": {
                  "title": "AccountTradingLimit",
                  "type": "object",
                  "properties": {
                    "daily_net_limit": {
                      "type": "string",
                      "description": "The net buying limit that can be reached before further trading activity is restricted. Please reach out to learn more about how this limit is determined.",
                      "format": "decimal"
                    },
                    "available": {
                      "type": "string",
                      "description": "The remaining net buying limit that can be used for trading.",
                      "format": "decimal"
                    },
                    "used": {
                      "type": "string",
                      "description": "The real time net value of cash inflows (buy trades, etc.) with cash outflows (sell trades, etc). This will be dynamic throughout the day based on user activity, with executed orders being reset at the start of the next trading day.",
                      "format": "decimal"
                    },
                    "held": {
                      "type": "string",
                      "description": "The limit that is currently being held for open orders",
                      "format": "decimal"
                    },
                    "swap_rate": {
                      "type": "string",
                      "description": "The swap rate is applicable for Local Currency Trading (LCT) accounts",
                      "format": "decimal"
                    },
                    "usd": {
                      "title": "USDAccountTradingLimit",
                      "type": "object",
                      "properties": {
                        "daily_net_limit": {
                          "type": "string",
                          "description": "The net buying limit that can be reached before further trading activity is restricted. Please reach out to learn more about how this limit is determined.",
                          "format": "decimal"
                        },
                        "available": {
                          "type": "string",
                          "description": "The remaining net buying limit that can be used for trading.",
                          "format": "decimal"
                        },
                        "used": {
                          "type": "string",
                          "description": "The real time net value of cash inflows (buy trades, etc.) with cash outflows (sell trades, etc). This will be dynamic throughout the day based on user activity, with executed orders being reset at the start of the next trading day.",
                          "format": "decimal"
                        },
                        "held": {
                          "type": "string",
                          "description": "The limit that is currently being held for open orders",
                          "format": "decimal"
                        }
                      },
                      "x-readme-ref-name": "USDAccountTradingLimit"
                    }
                  },
                  "x-readme-ref-name": "AccountTradingLimit"
                }
              }
            }
          },
          "404": {
            "description": "Returned when the account is not configured for trading limits"
          }
        },
        "operationId": "get-v1-account-trading-limits",
        "description": "This endpoint is only available to accounts with the trading limits feature enabled, and not on JIT.\nThe daily trading limit is set at the correspondent level (or the account level) and is used as the limit for the total amount due to Alpaca on the date of settlement.\nThe limit in use returns the real time usage of this limit, based on the setup it uses the usage is calculated differently.\nIf the limit in use reaches the `daily_net_limit` or `available` is zero, further purchasing activity will be halted, however, the limit can be adjusted by reaching out to Alpaca with the proposed new limit and the reason for the change."
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
