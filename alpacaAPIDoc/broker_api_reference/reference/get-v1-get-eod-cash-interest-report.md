---
source_view: https://docs.alpaca.markets/reference/get-v1-get-eod-cash-interest-report
source_md: https://docs.alpaca.markets/reference/get-v1-get-eod-cash-interest-report.md
scraped_at_utc: 2026-01-27T04:30:48Z
---
# Retrieve EOD Cash Interest Details

This API retrieves a list of cash interest details for the given date(s) for a single account or all accounts. End-of-day (EOD) details are typically accessible after 8:00pm Eastern Time (ET) and reflect that day’s ending state across cash balances, accrued interest, accrued fees, as well as additional ancillary details.

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
      "name": "Reporting"
    },
    {
      "name": "Cash Interest"
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
    "/v1/reporting/eod/cash_interest": {
      "get": {
        "summary": "Retrieve EOD Cash Interest Details",
        "description": "This API retrieves a list of cash interest details for the given date(s) for a single account or all accounts. End-of-day (EOD) details are typically accessible after 8:00pm Eastern Time (ET) and reflect that day’s ending state across cash balances, accrued interest, accrued fees, as well as additional ancillary details.",
        "operationId": "get-v1-get-eod-cash-interest-report",
        "tags": [
          "Reporting",
          "Cash Interest"
        ],
        "parameters": [
          {
            "name": "account_id",
            "in": "query",
            "description": "Account globally unique identifier. If not provided, the report will be generated for all accounts.",
            "required": false,
            "schema": {
              "type": "string",
              "format": "uuid"
            }
          },
          {
            "name": "date",
            "in": "query",
            "description": "A date in the format YYYY-MM-DD. If not provided, the report will be generated for the most recent date this report is available.",
            "required": false,
            "schema": {
              "type": "string",
              "format": "date"
            }
          },
          {
            "name": "after",
            "in": "query",
            "description": "A date in the format YYYY-MM-DD, valid only if account_id is provided and date is not provided. If not provided, this will use `before` value. If neither is provided the most recent available date is used for both `before` and `after`.",
            "required": false,
            "schema": {
              "type": "string",
              "format": "date"
            }
          },
          {
            "name": "before",
            "in": "query",
            "description": "A date in the format YYYY-MM-DD, valid only if account_id is provided and date is not provided. If not provided, this will use the most recent available date.",
            "required": false,
            "schema": {
              "type": "string",
              "format": "date"
            }
          },
          {
            "name": "direction",
            "in": "query",
            "description": "The direction to use for sorting responses, either `asc` or `desc`. Only valid for account_id queries, for which only sorting by date is supported. Defaults to `desc`.",
            "required": false,
            "schema": {
              "type": "string"
            }
          },
          {
            "name": "page_size",
            "in": "query",
            "description": "The page size, used for paginating responses. Defaults to 1000, with a maximum of 10,000.",
            "required": false,
            "schema": {
              "type": "integer",
              "maximum": 10000,
              "minimum": 1,
              "default": 1000
            }
          },
          {
            "name": "page_token",
            "in": "query",
            "description": "A token used to retrieve the next page for paginated queries. If provided the response will begin at the next page of the results for the response from which the `next_page_token` is used.",
            "required": false,
            "schema": {
              "type": "string"
            }
          }
        ],
        "responses": {
          "200": {
            "description": "Successful response, returns a list of daily interest accruals and an optional next page token.",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "interest": {
                      "type": "array",
                      "items": {
                        "type": "object",
                        "properties": {
                          "date": {
                            "type": "string",
                            "format": "date",
                            "example": "2024-09-27"
                          },
                          "account_id": {
                            "type": "string",
                            "format": "uuid",
                            "example": "02e5c5ba-36d2-467a-8699-81dc24271291"
                          },
                          "apr_tier_name": {
                            "type": "string",
                            "example": "gold"
                          },
                          "apr_tier_id": {
                            "type": "string",
                            "format": "uuid",
                            "example": "13d149c8-d620-43e0-978b-88af8abb2ef1"
                          },
                          "currency": {
                            "type": "string",
                            "example": "USD"
                          },
                          "cash_balance": {
                            "type": "string",
                            "format": "decimal",
                            "example": "10485.76"
                          },
                          "account_rate_bps": {
                            "type": "integer",
                            "example": 423
                          },
                          "account_accrued_interest": {
                            "type": "string",
                            "format": "decimal",
                            "example": "1.2152"
                          },
                          "correspondent_rate_bps": {
                            "type": "integer",
                            "example": 25
                          },
                          "correspondent_fee": {
                            "type": "string",
                            "format": "decimal",
                            "example": "0.0718"
                          }
                        },
                        "x-readme-ref-name": "DailyCashInterest"
                      }
                    },
                    "next_page_token": {
                      "type": "string",
                      "nullable": true,
                      "example": "293639be-8807-423f-b00d-68c781e8bb56"
                    }
                  },
                  "x-readme-ref-name": "EoDCashInterestReportResponse"
                }
              }
            }
          },
          "400": {
            "description": "A client error occurred. Please check the provided request parameters and try again.",
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
          },
          "401": {
            "description": "Unauthorized. Please check your API key and try again.",
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
          },
          "429": {
            "description": "Too many requests. Please wait a moment and try again.",
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
          },
          "500": {
            "description": "A server error occurred. Please contact Alpaca.",
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
