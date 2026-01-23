---
source_view: https://docs.alpaca.markets/reference/getclock-1
source_md: https://docs.alpaca.markets/reference/getclock-1.md
scraped_at_utc: 2026-01-22T23:02:18Z
---
# Get Market Clock info

The clock API serves the current market timestamp, whether or not the market is currently open, as well as the times of the next market open and close.

Returns the market clock.

# OpenAPI definition

```json
{
  "openapi": "3.0.0",
  "info": {
    "title": "Trading API",
    "description": "Alpaca's Trading API is a modern platform for algorithmic trading.",
    "version": "2.0.1",
    "contact": {
      "name": "Alpaca Support",
      "email": "support@alpaca.markets",
      "url": "https://alpaca.markets/support"
    },
    "termsOfService": "https://s3.amazonaws.com/files.alpaca.markets/disclosures/library/TermsAndConditions.pdf"
  },
  "servers": [
    {
      "url": "https://paper-api.alpaca.markets",
      "description": "Paper"
    },
    {
      "url": "https://api.alpaca.markets",
      "description": "Live"
    }
  ],
  "tags": [
    {
      "name": "Clock"
    }
  ],
  "paths": {
    "/v2/clock": {
      "get": {
        "summary": "Get Market Clock info",
        "parameters": [],
        "responses": {
          "200": {
            "description": "OK",
            "content": {
              "application/json": {
                "schema": {
                  "title": "Clock",
                  "type": "object",
                  "properties": {
                    "timestamp": {
                      "type": "string",
                      "description": "Current timestamp\n",
                      "format": "date-time"
                    },
                    "is_open": {
                      "type": "boolean",
                      "description": "Whether or not the market is open\n"
                    },
                    "next_open": {
                      "type": "string",
                      "description": "Next Market open timestamp",
                      "format": "date-time"
                    },
                    "next_close": {
                      "type": "string",
                      "description": "Next market close timestamp",
                      "format": "date-time"
                    }
                  },
                  "x-examples": {
                    "example-1": {
                      "timestamp": "2019-08-24T14:15:22Z",
                      "is_open": true,
                      "next_open": "2019-08-24T14:15:22Z",
                      "next_close": "2019-08-24T14:15:22Z"
                    }
                  },
                  "x-readme-ref-name": "Clock"
                }
              }
            }
          }
        },
        "operationId": "getClock",
        "description": "The clock API serves the current market timestamp, whether or not the market is currently open, as well as the times of the next market open and close.\n\nReturns the market clock.",
        "tags": [
          "Clock"
        ]
      }
    }
  },
  "components": {
    "securitySchemes": {
      "API_Key": {
        "name": "APCA-API-KEY-ID",
        "type": "apiKey",
        "in": "header",
        "description": ""
      },
      "API_Secret": {
        "name": "APCA-API-SECRET-KEY",
        "type": "apiKey",
        "in": "header",
        "description": ""
      }
    }
  },
  "security": [
    {
      "API_Key": [],
      "API_Secret": []
    }
  ],
  "x-readme": {
    "explorer-enabled": true,
    "proxy-enabled": false
  }
}
```
