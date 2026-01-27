---
source_view: https://docs.alpaca.markets/reference/queryMarketClock
source_md: https://docs.alpaca.markets/reference/queryMarketClock.md
scraped_at_utc: 2026-01-27T04:30:48Z
---
# Retrieve the Market Clock

The Clock API serves the current market timestamp, whether or not the market is currently open, as well as the times of the next market open and close.

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
      "name": "Clock"
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
    "/v1/clock": {
      "get": {
        "tags": [
          "Clock"
        ],
        "summary": "Retrieve the Market Clock",
        "responses": {
          "200": {
            "description": "The current market's timestamp",
            "content": {
              "application/json": {
                "schema": {
                  "description": "Represents the current market time and open/close events.",
                  "type": "object",
                  "x-examples": {
                    "example": {
                      "timestamp": "2018-04-01T12:00:00.000Z",
                      "is_open": true,
                      "next_open": "2018-04-01T12:00:00.000Z",
                      "next_close": "2018-04-01T12:00:00.000Z"
                    },
                    "example-1": {
                      "timestamp": "2022-02-16T13:06:05.210563128-05:00",
                      "is_open": true,
                      "next_open": "2022-02-17T09:30:00-05:00",
                      "next_close": "2022-02-16T16:00:00-05:00"
                    }
                  },
                  "title": "Clock",
                  "x-stoplight": {
                    "id": "rfhpxij3x0o6m"
                  },
                  "properties": {
                    "timestamp": {
                      "type": "string",
                      "minLength": 1,
                      "format": "date-time",
                      "description": "Current timestamp",
                      "example": "2022-02-16T13:06:05.210563128-05:00"
                    },
                    "is_open": {
                      "type": "boolean",
                      "description": "Whether the market is open or not"
                    },
                    "next_open": {
                      "type": "string",
                      "minLength": 1,
                      "format": "date-time",
                      "description": "Next market open timestamp - inclusive of timestamp"
                    },
                    "next_close": {
                      "type": "string",
                      "minLength": 1,
                      "format": "date-time",
                      "description": "Next market close timestamp - inclusive of timestamp"
                    }
                  },
                  "required": [
                    "timestamp",
                    "is_open",
                    "next_open",
                    "next_close"
                  ],
                  "x-readme-ref-name": "Clock"
                },
                "examples": {}
              }
            }
          }
        },
        "operationId": "queryMarketClock",
        "description": "The Clock API serves the current market timestamp, whether or not the market is currently open, as well as the times of the next market open and close."
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
