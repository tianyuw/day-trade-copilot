---
source_view: https://docs.alpaca.markets/reference/corporateactions-1
source_md: https://docs.alpaca.markets/reference/corporateactions-1.md
scraped_at_utc: 2026-01-26T01:04:10Z
---
# Corporate actions

This endpoint provides data about the corporate actions for each given symbol over a specified time period.

> ⚠️ Warning
>
> Currently Alpaca has no guarantees on the creation time of corporate actions. There may be delays in receiving corporate actions from our data providers, and there may be delays in processing and making them available via this API. As a result, corporate actions may not be available immediately after they are announced.


# OpenAPI definition

```json
{
  "openapi": "3.0.0",
  "info": {
    "title": "Market Data API",
    "description": "Access real-time and historical market data for US equities, options, crypto, and foreign exchange data through the Alpaca REST and WebSocket APIs. There are APIs for Stock Pricing, Option Pricing, Crypto Pricing, Forex, Logos, Fixed income, Corporate Actions, Screener, and News.\n",
    "version": "1.1",
    "contact": {
      "name": "Alpaca Support",
      "email": "support@alpaca.markets",
      "url": "https://alpaca.markets/support"
    },
    "termsOfService": "https://s3.amazonaws.com/files.alpaca.markets/disclosures/library/TermsAndConditions.pdf",
    "license": {
      "name": "Creative Commons Attribution Share Alike 4.0 International",
      "url": "https://spdx.org/licenses/CC-BY-SA-4.0.html"
    }
  },
  "servers": [
    {
      "description": "Production",
      "url": "https://data.alpaca.markets"
    },
    {
      "description": "Sandbox",
      "url": "https://data.sandbox.alpaca.markets"
    }
  ],
  "security": [
    {
      "apiKey": [],
      "apiSecret": []
    }
  ],
  "tags": [
    {
      "name": "Corporate actions",
      "description": "Corporate actions (splits, dividends, etc.)."
    }
  ],
  "paths": {
    "/v1/corporate-actions": {
      "get": {
        "summary": "Corporate actions",
        "tags": [
          "Corporate actions"
        ],
        "parameters": [
          {
            "name": "symbols",
            "description": "A comma-separated list of symbols.",
            "in": "query",
            "schema": {
              "type": "string"
            },
            "example": "AAPL,TSLA"
          },
          {
            "name": "cusips",
            "description": "A comma-separated list of CUSIPs.",
            "in": "query",
            "schema": {
              "type": "string"
            },
            "example": "037833100,88160R101"
          },
          {
            "name": "types",
            "in": "query",
            "schema": {
              "type": "string"
            },
            "example": "forward_split,reverse_split",
            "description": "A comma-separated list of types. If not provided, search all types.\n\nThe following types are supported:\n  - reverse_split\n  - forward_split\n  - unit_split\n  - cash_dividend\n  - stock_dividend\n  - spin_off\n  - cash_merger\n  - stock_merger\n  - stock_and_cash_merger\n  - redemption\n  - name_change\n  - worthless_removal\n  - rights_distribution\n"
          },
          {
            "name": "start",
            "in": "query",
            "schema": {
              "type": "string",
              "format": "date"
            },
            "examples": {
              "date": {
                "value": "2024-08-14"
              }
            },
            "description": "The inclusive start of the interval. The corporate actions are sorted by their `process_date`. Format: YYYY-MM-DD. Default: current day.\n"
          },
          {
            "name": "end",
            "in": "query",
            "schema": {
              "type": "string",
              "format": "date"
            },
            "examples": {
              "date": {
                "value": "2024-08-25",
                "summary": "Date"
              }
            },
            "description": "The inclusive end of the interval. The corporate actions are sorted by their `process_date`. Format: YYYY-MM-DD. Default: current day.\n"
          },
          {
            "name": "ids",
            "description": "A comma-separated list of corporate action IDs. This parameter is mutually exclusive with all other filters (symbols, types, start, end).\n",
            "in": "query",
            "schema": {
              "type": "string"
            },
            "example": "1dbc7685-9517-4a77-a236-8527d49cefdc,f8489167-4e4b-431d-a0be-6017ae1cf08a"
          },
          {
            "name": "limit",
            "in": "query",
            "schema": {
              "type": "integer",
              "minimum": 1,
              "maximum": 1000,
              "default": 100
            },
            "description": "Maximum number of corporate actions to return in a response.\nThe limit applies to the total number of data points, not the count per symbol!\nUse `next_page_token` to fetch the next set of corporate actions.\n"
          },
          {
            "name": "page_token",
            "in": "query",
            "schema": {
              "type": "string"
            },
            "description": "The pagination token from which to continue. The value to pass here is returned in specific requests when more data is available, usually because of a response result limit.\n"
          },
          {
            "name": "sort",
            "in": "query",
            "description": "Sort data in ascending or descending order.",
            "schema": {
              "type": "string",
              "description": "Sort data in ascending or descending order.",
              "enum": [
                "asc",
                "desc"
              ],
              "default": "asc",
              "x-go-name": "TypeSort",
              "x-readme-ref-name": "sort"
            }
          }
        ],
        "responses": {
          "200": {
            "description": "OK",
            "headers": {
              "X-RateLimit-Limit": {
                "schema": {
                  "type": "integer"
                },
                "example": 100,
                "description": "Request limit per minute."
              },
              "X-RateLimit-Remaining": {
                "schema": {
                  "type": "integer"
                },
                "example": 90,
                "description": "Request limit per minute remaining."
              },
              "X-RateLimit-Reset": {
                "schema": {
                  "type": "integer"
                },
                "example": 1674044551,
                "description": "The UNIX epoch when the remaining quota changes."
              }
            },
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "corporate_actions": {
                      "type": "object",
                      "properties": {
                        "reverse_splits": {
                          "type": "array",
                          "x-go-type-skip-optional-pointer": true,
                          "items": {
                            "type": "object",
                            "description": "Reverse split.",
                            "properties": {
                              "id": {
                                "type": "string",
                                "format": "uuid",
                                "description": "The internal Alpaca identifier of the corporate action.",
                                "x-readme-ref-name": "ca_id"
                              },
                              "symbol": {
                                "type": "string"
                              },
                              "old_cusip": {
                                "type": "string"
                              },
                              "new_cusip": {
                                "type": "string"
                              },
                              "new_rate": {
                                "type": "number",
                                "format": "double"
                              },
                              "old_rate": {
                                "type": "number",
                                "format": "double"
                              },
                              "process_date": {
                                "type": "string",
                                "format": "date",
                                "description": "The date when the corporate action is processed by Alpaca.",
                                "x-readme-ref-name": "process_date"
                              },
                              "ex_date": {
                                "type": "string",
                                "format": "date",
                                "description": "The ex-date marks the cutoff point for shareholders to be credited.",
                                "x-readme-ref-name": "ex_date"
                              },
                              "record_date": {
                                "type": "string",
                                "format": "date",
                                "x-readme-ref-name": "record_date"
                              },
                              "payable_date": {
                                "type": "string",
                                "format": "date",
                                "x-readme-ref-name": "payable_date"
                              }
                            },
                            "required": [
                              "id",
                              "symbol",
                              "old_cusip",
                              "new_cusip",
                              "new_rate",
                              "old_rate",
                              "process_date",
                              "ex_date"
                            ],
                            "example": {
                              "ex_date": "2023-08-24",
                              "id": "913de862-c02c-46dc-a89c-fc8779a50d30",
                              "new_cusip": "60879E200",
                              "new_rate": 1,
                              "old_cusip": "60879E101",
                              "old_rate": 50,
                              "process_date": "2023-08-24",
                              "record_date": "2023-08-24",
                              "symbol": "MNTS"
                            },
                            "x-readme-ref-name": "reverse_split"
                          }
                        },
                        "forward_splits": {
                          "type": "array",
                          "x-go-type-skip-optional-pointer": true,
                          "items": {
                            "type": "object",
                            "description": "Forward split.",
                            "properties": {
                              "id": {
                                "type": "string",
                                "format": "uuid",
                                "description": "The internal Alpaca identifier of the corporate action.",
                                "x-readme-ref-name": "ca_id"
                              },
                              "symbol": {
                                "type": "string"
                              },
                              "cusip": {
                                "type": "string"
                              },
                              "new_rate": {
                                "type": "number",
                                "format": "double"
                              },
                              "old_rate": {
                                "type": "number",
                                "format": "double"
                              },
                              "process_date": {
                                "type": "string",
                                "format": "date",
                                "description": "The date when the corporate action is processed by Alpaca.",
                                "x-readme-ref-name": "process_date"
                              },
                              "ex_date": {
                                "type": "string",
                                "format": "date",
                                "description": "The ex-date marks the cutoff point for shareholders to be credited.",
                                "x-readme-ref-name": "ex_date"
                              },
                              "record_date": {
                                "type": "string",
                                "format": "date",
                                "x-readme-ref-name": "record_date"
                              },
                              "payable_date": {
                                "type": "string",
                                "format": "date",
                                "x-readme-ref-name": "payable_date"
                              },
                              "due_bill_redemption_date": {
                                "type": "string",
                                "format": "date",
                                "x-readme-ref-name": "due_bill_redemption_date"
                              }
                            },
                            "required": [
                              "id",
                              "symbol",
                              "cusip",
                              "new_rate",
                              "old_rate",
                              "process_date",
                              "ex_date"
                            ],
                            "example": {
                              "cusip": "816851109",
                              "due_bill_redemption_date": "2023-08-23",
                              "ex_date": "2023-08-22",
                              "id": "189bd849-ab9f-4b4d-aaaa-a6d415fd976d",
                              "new_rate": 2,
                              "old_rate": 1,
                              "payable_date": "2023-08-21",
                              "process_date": "2023-08-22",
                              "record_date": "2023-08-14",
                              "symbol": "SRE"
                            },
                            "x-readme-ref-name": "forward_split"
                          }
                        },
                        "unit_splits": {
                          "type": "array",
                          "x-go-type-skip-optional-pointer": true,
                          "items": {
                            "type": "object",
                            "description": "Unit split.",
                            "properties": {
                              "id": {
                                "type": "string",
                                "format": "uuid",
                                "description": "The internal Alpaca identifier of the corporate action.",
                                "x-readme-ref-name": "ca_id"
                              },
                              "old_symbol": {
                                "type": "string"
                              },
                              "old_cusip": {
                                "type": "string"
                              },
                              "old_rate": {
                                "type": "number",
                                "format": "double"
                              },
                              "new_symbol": {
                                "type": "string"
                              },
                              "new_cusip": {
                                "type": "string"
                              },
                              "new_rate": {
                                "type": "number",
                                "format": "double"
                              },
                              "alternate_symbol": {
                                "type": "string"
                              },
                              "alternate_cusip": {
                                "type": "string"
                              },
                              "alternate_rate": {
                                "type": "number",
                                "format": "double"
                              },
                              "process_date": {
                                "type": "string",
                                "format": "date",
                                "description": "The date when the corporate action is processed by Alpaca.",
                                "x-readme-ref-name": "process_date"
                              },
                              "effective_date": {
                                "type": "string",
                                "format": "date",
                                "description": "The effective date marks the cutoff point for shareholders to be credited.",
                                "x-readme-ref-name": "effective_date"
                              },
                              "payable_date": {
                                "type": "string",
                                "format": "date",
                                "x-readme-ref-name": "payable_date"
                              }
                            },
                            "required": [
                              "id",
                              "old_symbol",
                              "old_cusip",
                              "old_rate",
                              "new_symbol",
                              "new_cusip",
                              "new_rate",
                              "alternate_symbol",
                              "alternate_cusip",
                              "alternate_rate",
                              "process_date",
                              "effective_date"
                            ],
                            "example": {
                              "alternate_cusip": "G5391L110",
                              "alternate_rate": 0.3333,
                              "alternate_symbol": "LVROW",
                              "effective_date": "2023-03-01",
                              "id": "3e68e87e-ae95-4d68-91d1-715d52ef143a",
                              "new_cusip": "G5391L102",
                              "new_rate": 1,
                              "new_symbol": "LVRO",
                              "old_cusip": "G8990L119",
                              "old_rate": 1,
                              "old_symbol": "TPBAU",
                              "process_date": "2023-03-01"
                            },
                            "x-readme-ref-name": "unit_split"
                          }
                        },
                        "stock_dividends": {
                          "type": "array",
                          "x-go-type-skip-optional-pointer": true,
                          "items": {
                            "type": "object",
                            "description": "Stock dividend.",
                            "properties": {
                              "id": {
                                "type": "string",
                                "format": "uuid",
                                "description": "The internal Alpaca identifier of the corporate action.",
                                "x-readme-ref-name": "ca_id"
                              },
                              "symbol": {
                                "type": "string"
                              },
                              "cusip": {
                                "type": "string"
                              },
                              "rate": {
                                "type": "number",
                                "format": "double"
                              },
                              "process_date": {
                                "type": "string",
                                "format": "date",
                                "description": "The date when the corporate action is processed by Alpaca.",
                                "x-readme-ref-name": "process_date"
                              },
                              "ex_date": {
                                "type": "string",
                                "format": "date",
                                "description": "The ex-date marks the cutoff point for shareholders to be credited.",
                                "x-readme-ref-name": "ex_date"
                              },
                              "record_date": {
                                "type": "string",
                                "format": "date",
                                "x-readme-ref-name": "record_date"
                              },
                              "payable_date": {
                                "type": "string",
                                "format": "date",
                                "x-readme-ref-name": "payable_date"
                              }
                            },
                            "required": [
                              "id",
                              "symbol",
                              "cusip",
                              "rate",
                              "process_date",
                              "ex_date"
                            ],
                            "example": {
                              "cusip": "605015106",
                              "ex_date": "2023-05-19",
                              "id": "3ae94c30-2d37-473a-bf29-5f7b4ab6d3ca",
                              "payable_date": "2023-05-05",
                              "process_date": "2023-05-19",
                              "rate": 0.05,
                              "record_date": "2023-05-22",
                              "symbol": "MSBC"
                            },
                            "x-readme-ref-name": "stock_dividend"
                          }
                        },
                        "cash_dividends": {
                          "type": "array",
                          "x-go-type-skip-optional-pointer": true,
                          "items": {
                            "type": "object",
                            "description": "Cash dividend.",
                            "properties": {
                              "id": {
                                "type": "string",
                                "format": "uuid",
                                "description": "The internal Alpaca identifier of the corporate action.",
                                "x-readme-ref-name": "ca_id"
                              },
                              "symbol": {
                                "type": "string"
                              },
                              "cusip": {
                                "type": "string"
                              },
                              "rate": {
                                "type": "number",
                                "format": "double"
                              },
                              "special": {
                                "type": "boolean"
                              },
                              "foreign": {
                                "type": "boolean"
                              },
                              "process_date": {
                                "type": "string",
                                "format": "date",
                                "description": "The date when the corporate action is processed by Alpaca.",
                                "x-readme-ref-name": "process_date"
                              },
                              "ex_date": {
                                "type": "string",
                                "format": "date",
                                "description": "The ex-date marks the cutoff point for shareholders to be credited.",
                                "x-readme-ref-name": "ex_date"
                              },
                              "record_date": {
                                "type": "string",
                                "format": "date",
                                "x-readme-ref-name": "record_date"
                              },
                              "payable_date": {
                                "type": "string",
                                "format": "date",
                                "x-readme-ref-name": "payable_date"
                              },
                              "due_bill_on_date": {
                                "type": "string",
                                "format": "date"
                              },
                              "due_bill_off_date": {
                                "type": "string",
                                "format": "date"
                              }
                            },
                            "required": [
                              "id",
                              "symbol",
                              "cusip",
                              "rate",
                              "special",
                              "foreign",
                              "process_date",
                              "ex_date"
                            ],
                            "example": {
                              "cusip": "319829107",
                              "ex_date": "2023-05-04",
                              "foreign": false,
                              "id": "11cfd108-292e-4cc6-bfbf-5999cdbc4029",
                              "payable_date": "2023-05-19",
                              "process_date": "2023-05-19",
                              "rate": 0.125,
                              "record_date": "2023-05-05",
                              "special": false,
                              "symbol": "FCF"
                            },
                            "x-readme-ref-name": "cash_dividend"
                          }
                        },
                        "spin_offs": {
                          "type": "array",
                          "x-go-type-skip-optional-pointer": true,
                          "items": {
                            "type": "object",
                            "description": "Spin-off.",
                            "properties": {
                              "id": {
                                "type": "string",
                                "format": "uuid",
                                "description": "The internal Alpaca identifier of the corporate action.",
                                "x-readme-ref-name": "ca_id"
                              },
                              "source_symbol": {
                                "type": "string"
                              },
                              "source_cusip": {
                                "type": "string"
                              },
                              "source_rate": {
                                "type": "number",
                                "format": "double"
                              },
                              "new_symbol": {
                                "type": "string"
                              },
                              "new_cusip": {
                                "type": "string"
                              },
                              "new_rate": {
                                "type": "number",
                                "format": "double"
                              },
                              "process_date": {
                                "type": "string",
                                "format": "date",
                                "description": "The date when the corporate action is processed by Alpaca.",
                                "x-readme-ref-name": "process_date"
                              },
                              "ex_date": {
                                "type": "string",
                                "format": "date",
                                "description": "The ex-date marks the cutoff point for shareholders to be credited.",
                                "x-readme-ref-name": "ex_date"
                              },
                              "record_date": {
                                "type": "string",
                                "format": "date",
                                "x-readme-ref-name": "record_date"
                              },
                              "payable_date": {
                                "type": "string",
                                "format": "date",
                                "x-readme-ref-name": "payable_date"
                              },
                              "due_bill_redemption_date": {
                                "type": "string",
                                "format": "date",
                                "x-readme-ref-name": "due_bill_redemption_date"
                              }
                            },
                            "required": [
                              "id",
                              "source_symbol",
                              "source_cusip",
                              "source_rate",
                              "new_symbol",
                              "new_cusip",
                              "new_rate",
                              "process_date",
                              "ex_date"
                            ],
                            "example": {
                              "ex_date": "2023-08-15",
                              "id": "82e602f6-35bc-4651-a5dd-f6d88ff37c55",
                              "new_cusip": "85237B101",
                              "new_rate": 1,
                              "new_symbol": "SRM",
                              "process_date": "2023-08-15",
                              "record_date": "2023-08-15",
                              "source_rate": 19.35,
                              "source_cusip": "48208F105",
                              "source_symbol": "JUPW"
                            },
                            "x-readme-ref-name": "spin_off"
                          }
                        },
                        "cash_mergers": {
                          "type": "array",
                          "x-go-type-skip-optional-pointer": true,
                          "items": {
                            "type": "object",
                            "description": "Cash merger.",
                            "properties": {
                              "id": {
                                "type": "string",
                                "format": "uuid",
                                "description": "The internal Alpaca identifier of the corporate action.",
                                "x-readme-ref-name": "ca_id"
                              },
                              "acquirer_symbol": {
                                "type": "string"
                              },
                              "acquirer_cusip": {
                                "type": "string"
                              },
                              "acquiree_symbol": {
                                "type": "string"
                              },
                              "acquiree_cusip": {
                                "type": "string"
                              },
                              "rate": {
                                "type": "number",
                                "format": "double"
                              },
                              "process_date": {
                                "type": "string",
                                "format": "date",
                                "description": "The date when the corporate action is processed by Alpaca.",
                                "x-readme-ref-name": "process_date"
                              },
                              "effective_date": {
                                "type": "string",
                                "format": "date",
                                "description": "The effective date marks the cutoff point for shareholders to be credited.",
                                "x-readme-ref-name": "effective_date"
                              },
                              "payable_date": {
                                "type": "string",
                                "format": "date",
                                "x-readme-ref-name": "payable_date"
                              }
                            },
                            "required": [
                              "id",
                              "acquiree_symbol",
                              "acquiree_cusip",
                              "rate",
                              "process_date",
                              "effective_date"
                            ],
                            "example": {
                              "acquiree_cusip": "Y2687W108",
                              "acquiree_symbol": "GLOP",
                              "effective_date": "2023-07-17",
                              "id": "3772bbd7-4ad5-44d4-9cc0-f69156a2f8f5",
                              "payable_date": "2023-07-17",
                              "process_date": "2023-07-17",
                              "rate": 5.37
                            },
                            "x-readme-ref-name": "cash_merger"
                          }
                        },
                        "stock_mergers": {
                          "type": "array",
                          "x-go-type-skip-optional-pointer": true,
                          "items": {
                            "type": "object",
                            "description": "Stock merger.",
                            "properties": {
                              "id": {
                                "type": "string",
                                "format": "uuid",
                                "description": "The internal Alpaca identifier of the corporate action.",
                                "x-readme-ref-name": "ca_id"
                              },
                              "acquirer_symbol": {
                                "type": "string"
                              },
                              "acquirer_cusip": {
                                "type": "string"
                              },
                              "acquirer_rate": {
                                "type": "number",
                                "format": "double"
                              },
                              "acquiree_symbol": {
                                "type": "string"
                              },
                              "acquiree_cusip": {
                                "type": "string"
                              },
                              "acquiree_rate": {
                                "type": "number",
                                "format": "double"
                              },
                              "process_date": {
                                "type": "string",
                                "format": "date",
                                "description": "The date when the corporate action is processed by Alpaca.",
                                "x-readme-ref-name": "process_date"
                              },
                              "effective_date": {
                                "type": "string",
                                "format": "date",
                                "description": "The effective date marks the cutoff point for shareholders to be credited.",
                                "x-readme-ref-name": "effective_date"
                              },
                              "payable_date": {
                                "type": "string",
                                "format": "date",
                                "x-readme-ref-name": "payable_date"
                              }
                            },
                            "required": [
                              "id",
                              "acquirer_symbol",
                              "acquirer_cusip",
                              "acquirer_rate",
                              "acquiree_symbol",
                              "acquiree_cusip",
                              "acquiree_rate",
                              "process_date",
                              "effective_date"
                            ],
                            "example": {
                              "acquiree_cusip": "53223X107",
                              "acquiree_rate": 1,
                              "acquiree_symbol": "LSI",
                              "acquirer_cusip": "30225T102",
                              "acquirer_rate": 0.895,
                              "acquirer_symbol": "EXR",
                              "effective_date": "2023-07-20",
                              "id": "728f8cb2-a00e-4bc7-ad14-d15fe82bbcff",
                              "payable_date": "2023-07-20",
                              "process_date": "2023-07-20"
                            },
                            "x-readme-ref-name": "stock_merger"
                          }
                        },
                        "stock_and_cash_mergers": {
                          "type": "array",
                          "x-go-type-skip-optional-pointer": true,
                          "items": {
                            "type": "object",
                            "description": "Stock and cash merger.",
                            "properties": {
                              "id": {
                                "type": "string",
                                "format": "uuid",
                                "description": "The internal Alpaca identifier of the corporate action.",
                                "x-readme-ref-name": "ca_id"
                              },
                              "acquirer_symbol": {
                                "type": "string"
                              },
                              "acquirer_cusip": {
                                "type": "string"
                              },
                              "acquirer_rate": {
                                "type": "number",
                                "format": "double"
                              },
                              "acquiree_symbol": {
                                "type": "string"
                              },
                              "acquiree_cusip": {
                                "type": "string"
                              },
                              "acquiree_rate": {
                                "type": "number",
                                "format": "double"
                              },
                              "cash_rate": {
                                "type": "number",
                                "format": "double"
                              },
                              "process_date": {
                                "type": "string",
                                "format": "date",
                                "description": "The date when the corporate action is processed by Alpaca.",
                                "x-readme-ref-name": "process_date"
                              },
                              "effective_date": {
                                "type": "string",
                                "format": "date",
                                "description": "The effective date marks the cutoff point for shareholders to be credited.",
                                "x-readme-ref-name": "effective_date"
                              },
                              "payable_date": {
                                "type": "string",
                                "format": "date",
                                "x-readme-ref-name": "payable_date"
                              }
                            },
                            "required": [
                              "id",
                              "acquirer_symbol",
                              "acquirer_cusip",
                              "acquirer_rate",
                              "acquiree_symbol",
                              "acquiree_cusip",
                              "acquiree_rate",
                              "cash_rate",
                              "process_date",
                              "effective_date"
                            ],
                            "example": {
                              "acquiree_cusip": "561409103",
                              "acquiree_rate": 1,
                              "acquiree_symbol": "MLVF",
                              "acquirer_cusip": "31931U102",
                              "acquirer_rate": 0.7733,
                              "acquirer_symbol": "FRBA",
                              "cash_rate": 7.8,
                              "effective_date": "2023-07-18",
                              "id": "e5248356-2c06-42cf-aeb9-1595bd616cdb",
                              "payable_date": "2023-07-18",
                              "process_date": "2023-07-18"
                            },
                            "x-readme-ref-name": "stock_and_cash_merger"
                          }
                        },
                        "redemptions": {
                          "type": "array",
                          "x-go-type-skip-optional-pointer": true,
                          "items": {
                            "type": "object",
                            "description": "Redemption.",
                            "properties": {
                              "id": {
                                "type": "string",
                                "format": "uuid",
                                "description": "The internal Alpaca identifier of the corporate action.",
                                "x-readme-ref-name": "ca_id"
                              },
                              "symbol": {
                                "type": "string"
                              },
                              "cusip": {
                                "type": "string"
                              },
                              "rate": {
                                "type": "number",
                                "format": "double"
                              },
                              "process_date": {
                                "type": "string",
                                "format": "date",
                                "description": "The date when the corporate action is processed by Alpaca.",
                                "x-readme-ref-name": "process_date"
                              },
                              "payable_date": {
                                "type": "string",
                                "format": "date",
                                "x-readme-ref-name": "payable_date"
                              }
                            },
                            "required": [
                              "id",
                              "symbol",
                              "cusip",
                              "rate",
                              "process_date"
                            ],
                            "example": {
                              "cusip": "687305102",
                              "id": "395da031-0e57-4918-a6fb-64a7c713aca4",
                              "payable_date": "2023-06-13",
                              "process_date": "2023-06-13",
                              "rate": 0.141134,
                              "symbol": "ORPHY"
                            },
                            "x-readme-ref-name": "redemption"
                          }
                        },
                        "name_changes": {
                          "type": "array",
                          "x-go-type-skip-optional-pointer": true,
                          "items": {
                            "type": "object",
                            "description": "Name change.",
                            "properties": {
                              "id": {
                                "type": "string",
                                "format": "uuid",
                                "description": "The internal Alpaca identifier of the corporate action.",
                                "x-readme-ref-name": "ca_id"
                              },
                              "old_symbol": {
                                "type": "string"
                              },
                              "old_cusip": {
                                "type": "string"
                              },
                              "new_symbol": {
                                "type": "string"
                              },
                              "new_cusip": {
                                "type": "string"
                              },
                              "process_date": {
                                "type": "string",
                                "format": "date",
                                "description": "The date when the corporate action is processed by Alpaca.",
                                "x-readme-ref-name": "process_date"
                              }
                            },
                            "required": [
                              "id",
                              "old_symbol",
                              "old_cusip",
                              "new_symbol",
                              "new_cusip",
                              "process_date"
                            ],
                            "example": {
                              "id": "5a774c35-edec-4532-a812-a56d0bbb623a",
                              "new_cusip": "Y9390M103",
                              "new_symbol": "VFS",
                              "old_cusip": "G11537100",
                              "old_symbol": "BSAQ",
                              "process_date": "2023-08-15"
                            },
                            "x-readme-ref-name": "name_change"
                          }
                        },
                        "worthless_removals": {
                          "type": "array",
                          "x-go-type-skip-optional-pointer": true,
                          "items": {
                            "type": "object",
                            "description": "Worthless removal.",
                            "properties": {
                              "id": {
                                "type": "string",
                                "format": "uuid",
                                "description": "The internal Alpaca identifier of the corporate action.",
                                "x-readme-ref-name": "ca_id"
                              },
                              "symbol": {
                                "type": "string"
                              },
                              "cusip": {
                                "type": "string"
                              },
                              "process_date": {
                                "type": "string",
                                "format": "date",
                                "description": "The date when the corporate action is processed by Alpaca.",
                                "x-readme-ref-name": "process_date"
                              }
                            },
                            "required": [
                              "id",
                              "symbol",
                              "cusip",
                              "process_date"
                            ],
                            "example": {
                              "cusip": "078771300",
                              "id": "106c2149-ee04-4d2e-a943-98dbb4d21a3c",
                              "symbol": "BLPH",
                              "process_date": "2024-12-19"
                            },
                            "x-readme-ref-name": "worthless_removal"
                          }
                        },
                        "rights_distributions": {
                          "type": "array",
                          "x-go-type-skip-optional-pointer": true,
                          "items": {
                            "type": "object",
                            "description": "Rights distribution.",
                            "properties": {
                              "id": {
                                "type": "string",
                                "format": "uuid",
                                "description": "The internal Alpaca identifier of the corporate action.",
                                "x-readme-ref-name": "ca_id"
                              },
                              "source_symbol": {
                                "type": "string"
                              },
                              "source_cusip": {
                                "type": "string"
                              },
                              "new_symbol": {
                                "type": "string"
                              },
                              "new_cusip": {
                                "type": "string"
                              },
                              "rate": {
                                "type": "number",
                                "format": "double"
                              },
                              "process_date": {
                                "type": "string",
                                "format": "date",
                                "description": "The date when the corporate action is processed by Alpaca.",
                                "x-readme-ref-name": "process_date"
                              },
                              "ex_date": {
                                "type": "string",
                                "format": "date",
                                "description": "The ex-date marks the cutoff point for shareholders to be credited.",
                                "x-readme-ref-name": "ex_date"
                              },
                              "record_date": {
                                "type": "string",
                                "format": "date",
                                "x-readme-ref-name": "record_date"
                              },
                              "payable_date": {
                                "type": "string",
                                "format": "date",
                                "x-readme-ref-name": "payable_date"
                              },
                              "expiration_date": {
                                "type": "string",
                                "format": "date",
                                "x-readme-ref-name": "expiration_date"
                              }
                            },
                            "required": [
                              "id",
                              "source_symbol",
                              "source_cusip",
                              "new_symbol",
                              "new_cusip",
                              "rate",
                              "process_date",
                              "ex_date",
                              "payable_date"
                            ],
                            "example": {
                              "ex_date": "2024-04-17",
                              "expiration_date": "2024-05-14",
                              "id": "69794cfd-0adc-4e11-9211-9210a9cf8932",
                              "new_cusip": "454089111",
                              "new_symbol": "IFN.RTWI",
                              "payable_date": "2024-04-19",
                              "process_date": "2024-04-19",
                              "rate": 1,
                              "record_date": "2024-04-18",
                              "source_cusip": "454089103",
                              "source_symbol": "IFN"
                            },
                            "x-readme-ref-name": "rights_distribution"
                          }
                        }
                      },
                      "x-readme-ref-name": "corporate_actions"
                    },
                    "next_page_token": {
                      "type": "string",
                      "description": "Pagination token for the next page.",
                      "nullable": true,
                      "x-readme-ref-name": "next_page_token"
                    }
                  },
                  "required": [
                    "corporate_actions",
                    "next_page_token"
                  ],
                  "x-readme-ref-name": "corporate_actions_resp"
                }
              }
            }
          },
          "400": {
            "description": "One of the request parameters is invalid. See the returned message for details.\n",
            "headers": {
              "X-RateLimit-Limit": {
                "schema": {
                  "type": "integer"
                },
                "example": 100,
                "description": "Request limit per minute."
              },
              "X-RateLimit-Remaining": {
                "schema": {
                  "type": "integer"
                },
                "example": 90,
                "description": "Request limit per minute remaining."
              },
              "X-RateLimit-Reset": {
                "schema": {
                  "type": "integer"
                },
                "example": 1674044551,
                "description": "The UNIX epoch when the remaining quota changes."
              }
            }
          },
          "401": {
            "description": "Authentication headers are missing or invalid. Make sure you authenticate your request with a valid API key.\n"
          },
          "403": {
            "description": "The requested resource is forbidden.\n"
          },
          "429": {
            "description": "Too many requests. You hit the rate limit. Use the X-RateLimit-... response headers to make sure you're under the rate limit.\n",
            "headers": {
              "X-RateLimit-Limit": {
                "schema": {
                  "type": "integer"
                },
                "example": 100,
                "description": "Request limit per minute."
              },
              "X-RateLimit-Remaining": {
                "schema": {
                  "type": "integer"
                },
                "example": 90,
                "description": "Request limit per minute remaining."
              },
              "X-RateLimit-Reset": {
                "schema": {
                  "type": "integer"
                },
                "example": 1674044551,
                "description": "The UNIX epoch when the remaining quota changes."
              }
            }
          },
          "500": {
            "description": "Internal server error. We recommend retrying these later. If the issue persists, please contact us on [Slack](https://alpaca.markets/slack) or on the [Community Forum](https://forum.alpaca.markets/).\n"
          }
        },
        "operationId": "CorporateActions",
        "description": "This endpoint provides data about the corporate actions for each given symbol over a specified time period.\n\n> ⚠️ Warning\n>\n> Currently Alpaca has no guarantees on the creation time of corporate actions. There may be delays in receiving corporate actions from our data providers, and there may be delays in processing and making them available via this API. As a result, corporate actions may not be available immediately after they are announced.\n"
      }
    }
  },
  "components": {
    "securitySchemes": {
      "apiKey": {
        "type": "apiKey",
        "in": "header",
        "name": "APCA-API-KEY-ID"
      },
      "apiSecret": {
        "type": "apiKey",
        "in": "header",
        "name": "APCA-API-SECRET-KEY"
      }
    }
  }
}
```
