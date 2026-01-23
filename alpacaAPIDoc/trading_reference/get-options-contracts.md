---
source_view: https://docs.alpaca.markets/reference/get-options-contracts
source_md: https://docs.alpaca.markets/reference/get-options-contracts.md
scraped_at_utc: 2026-01-22T23:02:18Z
---
# Get Option Contracts

This endpoint allows you to retrieve a list of option contracts based on various filtering criteria.
By default only active contracts that expire before the upcoming weekend are returned.


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
      "name": "Assets"
    }
  ],
  "paths": {
    "/v2/options/contracts": {
      "get": {
        "summary": "Get Option Contracts",
        "description": "This endpoint allows you to retrieve a list of option contracts based on various filtering criteria.\nBy default only active contracts that expire before the upcoming weekend are returned.\n",
        "tags": [
          "Assets"
        ],
        "operationId": "get-options-contracts",
        "parameters": [
          {
            "name": "underlying_symbols",
            "in": "query",
            "description": "Filter contracts by one or more underlying symbols.",
            "schema": {
              "type": "string"
            },
            "example": "AAPL,SPY"
          },
          {
            "name": "show_deliverables",
            "in": "query",
            "description": "Include deliverables array in the response.",
            "schema": {
              "type": "boolean"
            },
            "example": true
          },
          {
            "name": "status",
            "in": "query",
            "description": "Filter contracts by status (active/inactive). By default only active contracts are returned.",
            "schema": {
              "type": "string",
              "enum": [
                "active",
                "inactive"
              ]
            },
            "example": "active"
          },
          {
            "name": "expiration_date",
            "in": "query",
            "description": "Filter contracts by the exact expiration date (format: YYYY-MM-DD).",
            "schema": {
              "type": "string",
              "format": "date"
            },
            "example": "2025-06-20"
          },
          {
            "name": "expiration_date_gte",
            "in": "query",
            "description": "Filter contracts with expiration date greater than or equal to the specified date.",
            "schema": {
              "type": "string",
              "format": "date"
            },
            "example": "2025-06-20"
          },
          {
            "name": "expiration_date_lte",
            "in": "query",
            "description": "Filter contracts with expiration date less than or equal to the specified date. By default this is set to the next weekend.",
            "schema": {
              "type": "string",
              "format": "date"
            },
            "example": "2025-06-20"
          },
          {
            "name": "root_symbol",
            "in": "query",
            "description": "Filter contracts by the root symbol.",
            "schema": {
              "type": "string"
            },
            "example": "AAPL"
          },
          {
            "name": "type",
            "in": "query",
            "description": "Filter contracts by the type (call/put).",
            "schema": {
              "type": "string",
              "enum": [
                "call",
                "put"
              ]
            },
            "example": "call"
          },
          {
            "name": "style",
            "in": "query",
            "description": "Filter contracts by the style (american/european).",
            "schema": {
              "type": "string",
              "enum": [
                "american",
                "european"
              ]
            },
            "example": "american"
          },
          {
            "name": "strike_price_gte",
            "in": "query",
            "description": "Filter contracts with strike price greater than or equal to the specified value.",
            "schema": {
              "type": "number"
            },
            "example": 50
          },
          {
            "name": "strike_price_lte",
            "in": "query",
            "description": "Filter contracts with strike price less than or equal to the specified value.",
            "schema": {
              "type": "number"
            },
            "example": 100
          },
          {
            "name": "page_token",
            "in": "query",
            "required": false,
            "description": "Used for pagination, this token retrieves the next page of results. It is obtained from the response of the preceding page when additional pages are available.",
            "schema": {
              "type": "string",
              "example": "MA=="
            }
          },
          {
            "name": "limit",
            "in": "query",
            "description": "The number of contracts to limit per page (default=100, max=10000).",
            "schema": {
              "type": "integer"
            },
            "example": 100
          },
          {
            "name": "ppind",
            "in": "query",
            "schema": {
              "type": "boolean"
            },
            "example": "true",
            "description": "The ppind(Penny Program Indicator) field indicates whether an option contract is eligible for penny price increments,\nwith `true` meaning it is part of the Penny Program and `false` meaning it is not."
          }
        ],
        "responses": {
          "200": {
            "description": "Successful Response.",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "option_contracts": {
                      "type": "array",
                      "items": {
                        "type": "object",
                        "properties": {
                          "id": {
                            "type": "string",
                            "description": "The unique identifier of the option contract.",
                            "example": "98359ef7-5124-49f3-85ea-5cf02df6defa"
                          },
                          "symbol": {
                            "type": "string",
                            "description": "The symbol representing the option contract.",
                            "example": "AAPL250620C00100000"
                          },
                          "name": {
                            "type": "string",
                            "description": "The name of the option contract.",
                            "example": "AAPL Jun 20 2025 100 Call"
                          },
                          "status": {
                            "type": "string",
                            "description": "The status of the option contract.",
                            "enum": [
                              "active",
                              "inactive"
                            ],
                            "example": "active"
                          },
                          "tradable": {
                            "type": "boolean",
                            "description": "Indicates whether the option contract is tradable.",
                            "example": true
                          },
                          "expiration_date": {
                            "type": "string",
                            "format": "date",
                            "description": "The expiration date of the option contract.",
                            "example": "2025-06-20"
                          },
                          "root_symbol": {
                            "type": "string",
                            "description": "The root symbol of the option contract.",
                            "example": "AAPL"
                          },
                          "underlying_symbol": {
                            "type": "string",
                            "description": "The underlying symbol of the option contract.",
                            "example": "AAPL"
                          },
                          "underlying_asset_id": {
                            "type": "string",
                            "description": "The unique identifier of the underlying asset.",
                            "example": "b0b6dd9d-8b9b-48a9-ba46-b9d54906e415"
                          },
                          "type": {
                            "type": "string",
                            "description": "The type of the option contract.",
                            "enum": [
                              "call",
                              "put"
                            ],
                            "example": "call"
                          },
                          "style": {
                            "type": "string",
                            "description": "The style of the option contract.",
                            "enum": [
                              "american",
                              "european"
                            ],
                            "example": "american"
                          },
                          "strike_price": {
                            "type": "string",
                            "description": "The strike price of the option contract.",
                            "example": "100"
                          },
                          "multiplier": {
                            "type": "string",
                            "description": "The multiplier of the option contract is crucial for calculating both the trade premium and the extended strike price. In standard contracts, the multiplier is always set to 100.\nFor instance, if a contract is traded at $1.50 and the multiplier is 100, the total amount debited when buying the contract would be $150.00.\nSimilarly, when exercising a call contract, the total cost will be equal to the strike price times the multiplier.",
                            "example": "100"
                          },
                          "size": {
                            "type": "string",
                            "description": "Represents the number of underlying shares to be delivered in case the contract is exercised/assigned. For standard contracts, this is always 100.\nThis field should **not** be used as a multiplier, specially for non-standard contracts.",
                            "example": "100"
                          },
                          "open_interest": {
                            "type": "string",
                            "description": "The open interest of the option contract.",
                            "example": "237"
                          },
                          "open_interest_date": {
                            "type": "string",
                            "format": "date",
                            "description": "The date of the open interest data.",
                            "example": "2023-12-11"
                          },
                          "close_price": {
                            "type": "string",
                            "description": "The close price of the option contract.",
                            "example": "148.38"
                          },
                          "close_price_date": {
                            "type": "string",
                            "format": "date",
                            "example": "2023-12-11",
                            "description": "The date of the close price data."
                          },
                          "deliverables": {
                            "type": "array",
                            "description": "Represents the deliverables tied to the option contract. While standard contracts entail a single deliverable, non-standard ones can encompass multiple deliverables, each potentially customized with distinct parameters.\nThis array is included in the list contracts response only if the query parameter show_deliverables=true is provided.\n",
                            "items": {
                              "type": "object",
                              "properties": {
                                "type": {
                                  "type": "string",
                                  "description": "Type of deliverable, indicating whether it's cash or equity. For standard contracts, it is always \"equity\".\n",
                                  "enum": [
                                    "cash",
                                    "equity"
                                  ],
                                  "example": "equity"
                                },
                                "symbol": {
                                  "type": "string",
                                  "description": "Symbol of the deliverable. For standard contracts, this is equivalent to the underlying symbol of the contract.\n",
                                  "example": "AAPL"
                                },
                                "asset_id": {
                                  "type": "string",
                                  "description": "Unique identifier of the deliverable asset. For standard contracts, this is equivalent to underlying_asset_id of the contracts.\nThis field is not returned for cash deliverables.\n",
                                  "example": "b0b6dd9d-8b9b-48a9-ba46-b9d54906e415"
                                },
                                "amount": {
                                  "type": "string",
                                  "description": "The deliverable amount. For cash deliverables, this is the cash amount.\nFor standard contract, this is always 100.\nThis field can be null in case the deliverable settlement is delayed and the amount is yet to be determined.\n",
                                  "example": "100"
                                },
                                "allocation_percentage": {
                                  "type": "string",
                                  "description": "Cost allocation percentage of the deliverable.\nThis is used to determine the cost basis of the equity shares received from the exercise, specially for non-standard contracts with multiple deliverables.\n",
                                  "example": "100"
                                },
                                "settlement_type": {
                                  "type": "string",
                                  "description": "Indicates when the deliverable will be settled if the contract is exercised/assigned.\n",
                                  "enum": [
                                    "T+0",
                                    "T+1",
                                    "T+2",
                                    "T+3",
                                    "T+4",
                                    "T+5"
                                  ],
                                  "example": "T+2"
                                },
                                "settlement_method": {
                                  "type": "string",
                                  "description": "Indicates the settlement method that will be used:\n- **BTOB**: Broker to Broker\n- **CADF**: Cash Difference\n- **CAFX**: Cash Fixed\n- **CCC**: Correspondent Clearing Corp\n",
                                  "enum": [
                                    "BTOB",
                                    "CADF",
                                    "CAFX",
                                    "CCC"
                                  ],
                                  "example": "CCC"
                                },
                                "delayed_settlement": {
                                  "type": "boolean",
                                  "description": "If true, the settlement of the deliverable will be delayed.\nFor instance, in the event of a contract with a delayed deliverable being exercised, both the availability of the deliverable and its settlement may be postponed beyond the typical timeframe.\n",
                                  "example": false
                                }
                              },
                              "required": [
                                "type",
                                "symbol",
                                "amount",
                                "allocation_percentage",
                                "settlement_type",
                                "settlement_method",
                                "delayed_settlement"
                              ],
                              "x-readme-ref-name": "OptionDeliverable"
                            }
                          }
                        },
                        "required": [
                          "id",
                          "symbol",
                          "name",
                          "status",
                          "tradable",
                          "expiration_date",
                          "underlying_symbol",
                          "underlying_asset_id",
                          "type",
                          "style",
                          "strike_price",
                          "multiplier",
                          "size"
                        ],
                        "x-readme-ref-name": "OptionContract"
                      }
                    },
                    "next_page_token": {
                      "type": "string",
                      "description": "Use this token in your next API call to paginate through the dataset and retrieve the next page of results. A null token indicates there are no more data to fetch.\n",
                      "nullable": true,
                      "example": "MTAwMA==",
                      "x-readme-ref-name": "NextPageToken"
                    }
                  },
                  "required": [
                    "option_contracts"
                  ]
                }
              }
            }
          }
        }
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
