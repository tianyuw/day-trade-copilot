---
source_view: https://docs.alpaca.markets/reference/getcalendar-1
source_md: https://docs.alpaca.markets/reference/getcalendar-1.md
scraped_at_utc: 2026-01-22T23:02:18Z
---
# Get Market Calendar info

The calendar API serves the full list of market days from 1970 to 2029. It can also be queried by specifying a start and/or end time to narrow down the results. In addition to the dates, the response also contains the specific open and close times for the market days, taking into account early closures.

Returns the market calendar.

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
      "name": "Calendar"
    }
  ],
  "paths": {
    "/v2/calendar": {
      "get": {
        "summary": "Get Market Calendar info",
        "tags": [
          "Calendar"
        ],
        "parameters": [
          {
            "schema": {
              "type": "string",
              "format": "date-time"
            },
            "in": "query",
            "name": "start",
            "description": "The first date to retrieve data for (inclusive)"
          },
          {
            "schema": {
              "type": "string",
              "format": "date-time"
            },
            "in": "query",
            "name": "end",
            "description": "The last date to retrieve data for (inclusive)"
          },
          {
            "schema": {
              "type": "string"
            },
            "in": "query",
            "name": "date_type",
            "description": "Indicates what start and end mean. Enum: ‘TRADING’ or ‘SETTLEMENT’. Default value is ‘TRADING’. If TRADING is specified, returns a calendar whose trading date matches start, end. If SETTLEMENT is specified, returns the calendar whose settlement date matches start and end."
          }
        ],
        "responses": {
          "200": {
            "description": "OK",
            "content": {
              "application/json": {
                "schema": {
                  "type": "array",
                  "items": {
                    "type": "object",
                    "x-examples": {
                      "example-1": {
                        "date": "2022-02-01",
                        "open": "09:30",
                        "close": "16:00",
                        "session_open": "0700",
                        "session_close": "1900"
                      }
                    },
                    "title": "Calendar",
                    "properties": {
                      "date": {
                        "type": "string",
                        "minLength": 1,
                        "description": "Date string in “%Y-%m-%d” format"
                      },
                      "open": {
                        "type": "string",
                        "minLength": 1,
                        "description": "The time the market opens at on this date in “%H:%M” format"
                      },
                      "close": {
                        "type": "string",
                        "minLength": 1,
                        "description": "The time the market closes at on this date in “%H:%M” format"
                      },
                      "settlement_date": {
                        "type": "string",
                        "x-stoplight": {
                          "id": "e0st09dxvsjt5"
                        },
                        "description": "Date string in “%Y-%m-%d” format. representing the settlement date for the trade date."
                      }
                    },
                    "required": [
                      "date",
                      "open",
                      "close",
                      "settlement_date"
                    ],
                    "x-readme-ref-name": "Calendar"
                  }
                }
              }
            }
          }
        },
        "operationId": "getCalendar",
        "description": "The calendar API serves the full list of market days from 1970 to 2029. It can also be queried by specifying a start and/or end time to narrow down the results. In addition to the dates, the response also contains the specific open and close times for the market days, taking into account early closures.\n\nReturns the market calendar."
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
