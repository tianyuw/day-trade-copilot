---
source_view: https://docs.alpaca.markets/reference/getaccountactivitiesbytype
source_md: https://docs.alpaca.markets/reference/getaccountactivitiesbytype.md
scraped_at_utc: 2026-01-27T04:30:48Z
---
# Retrieve Account Activities of Specific Type

Retrieves an Array of Activies by type

If {activity_type} is provided as part of the URL, category cannot be provided as query parameter. They are mutually exclusive.

Notes:
* Pagination is handled using the `page_token` and `page_size` parameters.
* `page_token` represents the ID of the end of your current page of results.
  for example if in your first response the id of the last Activiy item returned in the array was `20220203000000000::045b3b8d-c566-4bef-b741-2bf598dd6ae7`, you'd pass that value as `page_token` to get the next page of results

* If specified with a `direction` of `desc`, for example, the results will end before the activity with the specified ID.
* If specified with a `direction` of `asc`, results will begin with the activity immediately after the one specified.
* `page_size` is the maximum number of entries to return in the response.
* If `date` is not specified, the default and maximum value is 100.
* If `date` is specified, the default behavior is to return all results, and there is no maximum page size.

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
      "name": "Accounts"
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
    "/v1/accounts/activities/{activity_type}": {
      "parameters": [
        {
          "in": "path",
          "name": "activity_type",
          "required": true,
          "schema": {
            "type": "string",
            "enum": [
              "FILL",
              "ACATC",
              "ACATS",
              "CIL",
              "CSD",
              "CSW",
              "DIV",
              "DIVCGL",
              "DIVCGS",
              "DIVNRA",
              "DIVROC",
              "DIVTXEX",
              "FEE",
              "INT",
              "MEM",
              "JNLC",
              "JNLS",
              "MA",
              "OPASN",
              "OPCA",
              "OPCSH",
              "OPEXC",
              "OPEXP",
              "OPTRD",
              "PTC",
              "REORG",
              "SPIN",
              "SPLIT"
            ]
          },
          "description": "see ActivityType model for details about what the different types mean"
        }
      ],
      "get": {
        "tags": [
          "Accounts"
        ],
        "parameters": [
          {
            "name": "account_id",
            "in": "query",
            "schema": {
              "type": "string",
              "format": "uuid"
            },
            "description": "id of a single account to filter by"
          },
          {
            "name": "date",
            "in": "query",
            "schema": {
              "type": "string",
              "format": "date-time"
            },
            "description": "Filter activities by the activity date. Both formats YYYY-MM-DD and YYYY-MM-DDTHH:MM:SSZ are supported."
          },
          {
            "name": "until",
            "in": "query",
            "schema": {
              "type": "string",
              "format": "date-time"
            },
            "description": "Get activities created before this date. Both formats YYYY-MM-DD and YYYY-MM-DDTHH:MM:SSZ are supported."
          },
          {
            "name": "after",
            "in": "query",
            "schema": {
              "type": "string",
              "format": "date-time"
            },
            "description": "Get activities created after this date. Both formats YYYY-MM-DD and YYYY-MM-DDTHH:MM:SSZ are supported."
          },
          {
            "name": "direction",
            "in": "query",
            "description": "The chronological order of response based on the submission time. asc or desc. Defaults to desc.",
            "schema": {
              "type": "string",
              "enum": [
                "asc",
                "desc"
              ],
              "example": "desc"
            }
          },
          {
            "name": "page_size",
            "in": "query",
            "schema": {
              "type": "integer",
              "minimum": 1,
              "maximum": 100,
              "default": 100
            },
            "description": "The maximum number of entries to return in the response."
          },
          {
            "name": "page_token",
            "in": "query",
            "schema": {
              "type": "string"
            },
            "description": "Token used for pagination. Provide the ID of the last activity from the last page to retrieve the next set of results."
          }
        ],
        "summary": "Retrieve Account Activities of Specific Type",
        "responses": {
          "200": {
            "description": "Success",
            "content": {
              "application/json": {
                "schema": {
                  "type": "array",
                  "items": {
                    "title": "Activity",
                    "description": "Base for activity types",
                    "allOf": [
                      {
                        "type": "object",
                        "properties": {
                          "id": {
                            "type": "string",
                            "example": "20220208125959696::88b5f678-fef5-447b-af15-f21e367e6d8c"
                          },
                          "account_id": {
                            "type": "string",
                            "format": "uuid",
                            "example": "c8f1ef5d-edc0-4f23-9ee4-378f19cb92a4"
                          },
                          "activity_type": {
                            "title": "ActivityType",
                            "type": "string",
                            "enum": [
                              "FILL",
                              "ACATC",
                              "ACATS",
                              "CIL",
                              "CSD",
                              "CSW",
                              "DIV",
                              "DIVCGL",
                              "DIVCGS",
                              "DIVNRA",
                              "DIVROC",
                              "DIVTXEX",
                              "FEE",
                              "INT",
                              "JNLC",
                              "JNLS",
                              "MA",
                              "OPASN",
                              "OPCA",
                              "OPCSH",
                              "OPEXC",
                              "OPEXP",
                              "OPTRD",
                              "PTC",
                              "REORG",
                              "SPIN",
                              "SPLIT"
                            ],
                            "description": "Represents the various kinds of activity.\n\nTradeActivity's will always have the type `FILL`\n\n- **FILL**\n  Order Fills (Partial/Full)\n- **ACATC**\n  ACATS IN/OUT (Cash)\n- **ACATS**\n  ACATS IN/OUT (Securities)\n- **CIL**\n  Cash in Lieu of Stock\n- **CSD**\n  Cash Disbursement (+)\n- **CSW**\n  Cash Withdrawable\n- **DIV**\n  Dividend\n- **DIVCGL**\n  Dividend (Capital Gain Long Term)\n- **DIVCGS**\n  Dividend (Capital Gain Short Term)\n- **DIVNRA**\n  Dividend Adjusted (NRA Withheld)\n- **DIVROC**\n  Dividend Return of Capital\n- **DIVTXEX**\n  Dividend (Tax Exempt)\n- **FEE**\n  REG and TAF Fees\n- **INT**\n  Interest (Credit/Margin)\n- **JNLC**\n  Journal Entry (Cash)\n- **JNLS**\n  Journal Entry (Stock)\n- **OPASN**\n   Option Assignment\n- **OPCA**\n  Option Corporate Action\n- **OPCSH**\n   Option cash deliverable for non-standard contracts\n- **OPEXC**\n  Option Exercise\n- **OPEXP**\n  Option Expiration\n- **OPTRD**\n  Option Trade\n- **MA**\n  Merger/Acquisition\n- **PTC**\n  Pass Thru Change\n- **REORG**\n  Reorg CA\n- **SPIN**\n  Stock Spinoff\n- **SPLIT**\n  Stock Split",
                            "x-stoplight": {
                              "id": "y6utewjrnwcgk"
                            },
                            "x-readme-ref-name": "ActivityType"
                          }
                        }
                      },
                      {
                        "oneOf": [
                          {
                            "title": "TradeActivity",
                            "type": "object",
                            "properties": {
                              "transaction_time": {
                                "type": "string",
                                "format": "date-time",
                                "example": "2021-05-10T14:01:04.650275Z",
                                "description": "Valid only for trading activity types. Null for non-trading activites."
                              },
                              "type": {
                                "type": "string",
                                "enum": [
                                  "fill",
                                  "partial_fill"
                                ],
                                "example": "fill",
                                "description": "Valid only for trading activity types. Null for non-trading activites."
                              },
                              "price": {
                                "type": "string",
                                "format": "decimal",
                                "example": "3.1415",
                                "description": "Valid only for trading activity types. Null for non-trading activites."
                              },
                              "qty": {
                                "type": "string",
                                "format": "decimal",
                                "example": "0.38921",
                                "description": "Valid only for trading activity types. Null for non-trading activites."
                              },
                              "side": {
                                "type": "string",
                                "enum": [
                                  "buy",
                                  "sell",
                                  "buy_minus",
                                  "sell_plus",
                                  "sell_short",
                                  "sell_short_exempt",
                                  "undisclosed",
                                  "cross",
                                  "cross_short"
                                ],
                                "example": "buy",
                                "description": "Represents what side of the transaction an order was on. Required for all order classes except for `mleg`.",
                                "x-stoplight": {
                                  "id": "zrdcas15ugcl7"
                                },
                                "x-readme-ref-name": "OrderSide"
                              },
                              "symbol": {
                                "type": "string",
                                "example": "AAPL",
                                "description": "Valid only for trading activity types. Null for non-trading activites."
                              },
                              "leaves_qty": {
                                "type": "string",
                                "format": "decimal",
                                "example": "0.5123",
                                "description": "Valid only for trading activity types. Null for non-trading activites."
                              },
                              "order_id": {
                                "type": "string",
                                "format": "uuid",
                                "example": "fe060a1b-5b45-4eba-ba46-c3a3345d8255",
                                "description": "Valid only for trading activity types. Null for non-trading activites."
                              },
                              "cum_qty": {
                                "type": "string",
                                "format": "decimal",
                                "example": "0.9723",
                                "description": "Valid only for trading activity types. Null for non-trading activites."
                              },
                              "order_status": {
                                "type": "string",
                                "enum": [
                                  "new",
                                  "partially_filled",
                                  "filled",
                                  "done_for_day",
                                  "canceled",
                                  "expired",
                                  "replaced",
                                  "pending_cancel",
                                  "pending_replace",
                                  "accepted",
                                  "pending_new",
                                  "accepted_for_bidding",
                                  "stopped",
                                  "rejected",
                                  "suspended",
                                  "calculated"
                                ],
                                "example": "filled",
                                "x-stoplight": {
                                  "id": "742rdkivas7us"
                                },
                                "x-readme-ref-name": "OrderStatus"
                              }
                            },
                            "x-stoplight": {
                              "id": "q0bbbxhqaumis"
                            },
                            "x-readme-ref-name": "TradeActivity"
                          },
                          {
                            "title": "NonTradeActivity",
                            "type": "object",
                            "properties": {
                              "activity_sub_type": {
                                "title": "ActivitySubType",
                                "type": "string",
                                "description": "Represents a more specific classification to the `activity_type`.\nThis field is optional and may not always be populated, depending on the activity type and the available data.\nEach `activity_type` has a set of valid `activity_sub_type` values.\n\nFull mapping of `activity_type` to `activity_sub_type`:\n\n- **DIV**: Dividend activity sub-types:\n  - **CDIV**: Cash Dividend\n  - **SDIV**: Stock Dividend\n  - **SPD**: Substitute Payment In Lieu Of Dividend\n\n- **FEE**: Fee-related activity sub-types:\n  - **REG**: Regulatory Fee\n  - **TAF**: Trading Activity Fee\n  - **LCT**: Local Currency Trading Fee\n  - **ORF**: Options Regulatory Fee\n  - **OCC**: Options Clearing Corporation Fee\n  - **NRC**: Non-Retail Commission Fee\n  - **NRV**: Non-Retail Venue Fee\n  - **COM**: Commission\n  - **CAT**: Consolidated Audit Trail Fee\n\n- **INT**: Interest-related activity sub-types:\n  - **MGN**: Margin Interest\n  - **CDT**: Credit Interest\n  - **SWP**: Sweep Interest\n  - **QII**: Qualified Interest\n\n- **MA**: Merger and Acquisition activity sub-types:\n  - **CMA**: Cash Merger\n  - **SMA**: Stock Merger\n  - **SCMA**: Stock & Cash Merger\n\n- **NC**: Name Change activity sub types\n  - **SNC**: Symbol Name Change\n  - **CNC**: CUSIP Name Change\n  - **SCNC**: Symbol & CUSIP Name Change\n\n- **OPCA**: Option Corporate Action activity sub-types:\n  - **DIV.CDIV**: Cash Dividend\n  - **DIV.SDIV**: Stock Dividend\n  - **MA.CMA**: Cash Merger\n  - **MA.SMA**: Stock Merger\n  - **MA.SCMA**: Stock & Cash Merger\n  - **NC.CNC**: CUSIP Name Change\n  - **NC.SNC**: Symbol Name Change\n  - **NC.SCNC**: Symbol & CUSIP Name Change\n  - **SPIN**: Spin-off\n  - **SPLIT.FSPLIT**: Forward Stock Split\n  - **SPLIT.RSPLIT**: Reverse Stock Split\n  - **SPLIT.USPLIT**: Unit Split\n\n- **REORG**: Reorganization activity sub-types:\n  - **WRM**: Worthless Removal\n\n- **SPLIT**: Stock Split activity sub-types:\n  - **FSPLIT**: Forward Stock Split\n  - **RSPLIT**: Reverse Stock Split\n  - **USPLIT**: Unit Split\n\n- **VOF**: Voluntary Offering activity sub-types:\n  - **VTND**: Tender Offer\n  - **VWRT**: Warrant Exercise\n  - **VRGT**: Rights Offer\n  - **VEXH**: Exchange Offer\n\n- **WH**: Withholding activity sub-types:\n  - **SWH**: State Withholding\n  - **FWH**: Federal Withholding\n  - **SLWH**: Sales Withholding",
                                "x-readme-ref-name": "ActivitySubType"
                              },
                              "date": {
                                "type": "string",
                                "format": "date",
                                "example": "2021-05-21",
                                "description": "Valid only for non-trading activity types. Null for trading activites."
                              },
                              "net_amount": {
                                "type": "string",
                                "format": "decimal",
                                "example": "1234",
                                "description": "Valid only for non-trading activity types. Null for trading activites."
                              },
                              "description": {
                                "type": "string",
                                "example": "Example description",
                                "description": "Valid only for non-trading activity types. Null for trading activites."
                              },
                              "status": {
                                "type": "string",
                                "enum": [
                                  "executed",
                                  "correct",
                                  "canceled"
                                ],
                                "example": "executed",
                                "description": "Valid only for non-trading activity types. Null for trading activites."
                              },
                              "symbol": {
                                "type": "string",
                                "example": "AAPL",
                                "description": "Valid only for non-trading activity types. Null for trading activites."
                              },
                              "cusip": {
                                "type": "string",
                                "example": "037833100",
                                "description": "Valid only for non-trading activity types. Null for trading activites."
                              },
                              "qty": {
                                "type": "string",
                                "format": "decimal",
                                "example": "0.38921",
                                "description": "Valid only for non-trading activity types. Null for trading activites."
                              },
                              "per_share_amount": {
                                "type": "string",
                                "format": "decimal",
                                "example": "0.38921",
                                "description": "Valid only for non-trading activity types. Null for trading activites."
                              },
                              "group_id": {
                                "type": "string",
                                "format": "uuid",
                                "example": "13d96cf3-1cbe-4632-b2f2-86a9df5a3b9d",
                                "description": "ID used to link activities who share a sibling relationship"
                              },
                              "created_at": {
                                "type": "string",
                                "format": "date-time",
                                "example": "2021-05-10T14:01:04.650275Z",
                                "description": "Valid only for non-trading activity types. Null for trading activites."
                              }
                            },
                            "x-stoplight": {
                              "id": "iycf52rzeqwkt"
                            },
                            "x-readme-ref-name": "NonTradeActivity"
                          }
                        ]
                      }
                    ],
                    "required": [
                      "id",
                      "activity_type"
                    ],
                    "x-stoplight": {
                      "id": "1cd58vzvymj1a"
                    },
                    "x-readme-ref-name": "Activity"
                  }
                }
              }
            }
          }
        },
        "operationId": "getAccountActivitiesByType",
        "description": "Retrieves an Array of Activies by type\n\nIf {activity_type} is provided as part of the URL, category cannot be provided as query parameter. They are mutually exclusive.\n\nNotes:\n* Pagination is handled using the `page_token` and `page_size` parameters.\n* `page_token` represents the ID of the end of your current page of results.\n  for example if in your first response the id of the last Activiy item returned in the array was `20220203000000000::045b3b8d-c566-4bef-b741-2bf598dd6ae7`, you'd pass that value as `page_token` to get the next page of results\n\n* If specified with a `direction` of `desc`, for example, the results will end before the activity with the specified ID.\n* If specified with a `direction` of `asc`, results will begin with the activity immediately after the one specified.\n* `page_size` is the maximum number of entries to return in the response.\n* If `date` is not specified, the default and maximum value is 100.\n* If `date` is specified, the default behavior is to return all results, and there is no maximum page size."
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
