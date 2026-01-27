---
source_view: https://docs.alpaca.markets/reference/get-v1-transfers-jit-limits
source_md: https://docs.alpaca.markets/reference/get-v1-transfers-jit-limits.md
scraped_at_utc: 2026-01-27T04:30:48Z
---
# Retrieve Daily Trading Limits

The JIT Securities daily trading limit is set at the correspondent level and is used as the limit for the total amount due to Alpaca on the date of settlement. The limit in use returns the real time usage of this limit and is calculated by taking the net of trade and non-trade activity inflows and outflows. If the limit in use reaches the daily net limit, further purchasing activity will be halted, however, the limit can be adjusted by reaching out to Alpaca with the proposed new limit and the reason for the change.

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
    "/v1/transfers/jit/limits": {
      "get": {
        "summary": "Retrieve Daily Trading Limits",
        "tags": [
          "Funding"
        ],
        "responses": {
          "200": {
            "description": "Returns the JIT Securities Daily Trading Limit Object based off of real time calculations.",
            "content": {
              "application/json": {
                "schema": {
                  "title": "DailyTradingLimit",
                  "x-stoplight": {
                    "id": "at5t8fzsrjz6s"
                  },
                  "type": "object",
                  "properties": {
                    "daily_net_limit_in_use": {
                      "type": "string",
                      "x-stoplight": {
                        "id": "4159up5cilte2"
                      },
                      "description": "The real time net value of cash inflows (buy trades, etc.) with cash outflows (sell trades, dividends, etc). This will be dynamic throughout the day based on user activity, with executed orders being reset at the start of the next trading day.",
                      "format": "decimal"
                    },
                    "daily_net_limit": {
                      "type": "string",
                      "x-stoplight": {
                        "id": "s7lyx5zx2bxkq"
                      },
                      "format": "decimal",
                      "description": "The net buying limit that can be reached before further cash outflow trading activity is restricted. Please reach out to learn more about how this limit is determined."
                    }
                  },
                  "x-readme-ref-name": "DailyTradingLimit"
                }
              }
            }
          }
        },
        "operationId": "get-v1-transfers-jit-limits",
        "description": "The JIT Securities daily trading limit is set at the correspondent level and is used as the limit for the total amount due to Alpaca on the date of settlement. The limit in use returns the real time usage of this limit and is calculated by taking the net of trade and non-trade activity inflows and outflows. If the limit in use reaches the daily net limit, further purchasing activity will be halted, however, the limit can be adjusted by reaching out to Alpaca with the proposed new limit and the reason for the change."
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
