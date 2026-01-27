---
source_view: https://docs.alpaca.markets/reference/queryMarketCalendar
source_md: https://docs.alpaca.markets/reference/queryMarketCalendar.md
scraped_at_utc: 2026-01-27T04:30:48Z
---
# Retrieve the Market Calendar

The calendar API serves the full list of market days from 1970 to 2029. It can also be queried by specifying a start and/or end time to narrow down the results. In addition to the dates, the response also contains the specific open and close times for the market days, taking into account early closures.

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
      "name": "Calendar"
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
    "/v1/calendar": {
      "get": {
        "tags": [
          "Calendar"
        ],
        "summary": "Retrieve the Market Calendar",
        "parameters": [
          {
            "name": "start",
            "description": "The first date to retrieve data for. (Inclusive) in YYYY-MM-DD format",
            "in": "query",
            "schema": {
              "type": "string",
              "format": "date",
              "example": "2022-01-01"
            }
          },
          {
            "name": "end",
            "description": "The last date to retrieve data for. (Inclusive) in YYYY-MM-DD format",
            "in": "query",
            "schema": {
              "type": "string",
              "format": "date",
              "example": "2022-01-01"
            }
          },
          {
            "name": "date_type",
            "schema": {
              "type": "string"
            },
            "in": "query",
            "description": "‘trading’ or ‘settlement’. Default value is ‘trading’. Indicates to filter by trade date or settlement date if start or end are specified."
          }
        ],
        "responses": {
          "200": {
            "description": "Returns the calendar object",
            "content": {
              "application/json": {
                "schema": {
                  "type": "array",
                  "items": {
                    "title": "Calendar",
                    "type": "object",
                    "description": "The calendar API serves the full list of market days from 1970 to 2029. It can also be queried by specifying a start and/or end time to narrow down the results. In addition to the dates, the response also contains the specific open and close times for the market days, taking into account early closures.",
                    "x-stoplight": {
                      "id": "6w3glz9nvzann"
                    },
                    "properties": {
                      "date": {
                        "type": "string",
                        "example": "2021-04-06",
                        "format": "date",
                        "description": "Date string in YYYY-MM-DD format"
                      },
                      "open": {
                        "type": "string",
                        "example": "09:30",
                        "description": "The time the market opens at on this date in HH:MM format"
                      },
                      "close": {
                        "type": "string",
                        "example": "16:00",
                        "description": "The time the market closes at on this date in HH:MM format"
                      },
                      "session_open": {
                        "type": "string",
                        "example": "0700",
                        "deprecated": true,
                        "description": "this field has been deprecated please ignore"
                      },
                      "session_close": {
                        "type": "string",
                        "example": "1900",
                        "deprecated": true,
                        "description": "this field has been deprecated please ignore"
                      },
                      "settlement_date": {
                        "type": "string",
                        "x-stoplight": {
                          "id": "6lmmqwon4mjk0"
                        },
                        "description": "Date string in “%Y-%m-%d” format. representing the settlement date for the trade date"
                      }
                    },
                    "required": [
                      "date",
                      "open",
                      "close"
                    ],
                    "x-readme-ref-name": "Calendar"
                  }
                }
              }
            }
          }
        },
        "operationId": "queryMarketCalendar",
        "description": "The calendar API serves the full list of market days from 1970 to 2029. It can also be queried by specifying a start and/or end time to narrow down the results. In addition to the dates, the response also contains the specific open and close times for the market days, taking into account early closures."
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
