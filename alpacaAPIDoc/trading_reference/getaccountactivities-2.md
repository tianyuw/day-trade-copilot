---
source_view: https://docs.alpaca.markets/reference/getaccountactivities-2
source_md: https://docs.alpaca.markets/reference/getaccountactivities-2.md
scraped_at_utc: 2026-01-22T23:02:18Z
---
# Retrieve Account Activities

Returns a list of activities

Notes:
* Pagination is handled using the `page_token` and `page_size` parameters.
* `page_token` represents the ID of the last item on your current page of results.
   For example, if the ID of the last activity in your first response is `20220203000000000::045b3b8d-c566-4bef-b741-2bf598dd6ae7`, you would pass that value as `page_token` to retrieve the next page of results.

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
      "name": "Account Activities"
    }
  ],
  "paths": {
    "/v2/account/activities": {
      "get": {
        "summary": "Retrieve Account Activities",
        "tags": [
          "Account Activities"
        ],
        "responses": {
          "200": {
            "description": "returns an array of Account activities",
            "content": {
              "application/json": {
                "schema": {
                  "type": "array",
                  "items": {
                    "anyOf": [
                      {
                        "title": "AccountTradingActivities",
                        "type": "object",
                        "x-examples": {
                          "example-1": {
                            "id": "20220202135509981::2d7be4ff-d1f3-43e9-856a-0f5cf5c5088e",
                            "activity_type": "FILL",
                            "transaction_time": "2022-02-02T18:55:09.981482Z",
                            "type": "fill",
                            "price": "174.78",
                            "qty": "2",
                            "side": "buy",
                            "symbol": "AAPL",
                            "leaves_qty": "0",
                            "order_id": "b5abe576-6a8a-49f3-a353-46b72c1ccae9",
                            "cum_qty": "2",
                            "order_status": "filled"
                          }
                        },
                        "properties": {
                          "activity_type": {
                            "type": "string",
                            "title": "ActivityType",
                            "description": "- FILL\n  Order fills (both partial and full fills)\n\n- TRANS\n  Cash transactions (both CSD and CSW)\n\n- MISC\n  Miscellaneous or rarely used activity types (All types except those in TRANS, DIV, or FILL)\n\n- ACATC\n  ACATS IN/OUT (Cash)\n\n- ACATS\n  ACATS IN/OUT (Securities)\n\n- CFEE\n  Crypto fee\n\n- CSD\n  Cash deposit(+)\n\n- CSW\n  Cash withdrawal(-)\n\n- DIV\n  Dividends\n\n- DIVCGL\n  Dividend (capital gain long term)\n\n- DIVCGS\n  Dividend (capital gain short term)\n\n- DIVFEE\n  Dividend fee\n\n- DIVFT\n  Dividend adjusted (Foreign Tax Withheld)\n\n- DIVNRA\n  Dividend adjusted (NRA Withheld)\n\n- DIVROC\n  Dividend return of capital\n\n- DIVTW\n  Dividend adjusted (Tefra Withheld)\n\n- DIVTXEX\n  Dividend (tax exempt)\n\n- FEE\n  Fee denominated in USD\n\n- INT\n  Interest (credit/margin)\n\n- INTNRA\n  Interest adjusted (NRA Withheld)\n\n- INTTW\n  Interest adjusted (Tefra Withheld)\n\n- JNL\n  Journal entry\n\n- JNLC\n  Journal entry (cash)\n\n- JNLS\n  Journal entry (stock)\n\n- MA\n  Merger/Acquisition\n\n- NC\n  Name change\n\n- OPASN\n  Option assignment\n\n- OPCA\n  Option corporate action\n\n- OPCSH\n  Option cash deliverable for non-standard contracts\n\n- OPEXC\n  Option exercise\n\n- OPEXP\n  Option expiration\n\n- OPTRD\n  Option trade\n\n- PTC\n  Pass Thru Charge\n\n- PTR\n  Pass Thru Rebate\n\n- REORG\n  Reorg CA\n\n- SPIN\n  Stock spinoff\n\n- SPLIT\n  Stock split",
                            "enum": [
                              "FILL",
                              "TRANS",
                              "MISC",
                              "ACATC",
                              "ACATS",
                              "CFEE",
                              "CSD",
                              "CSW",
                              "DIV",
                              "DIVCGL",
                              "DIVCGS",
                              "DIVFEE",
                              "DIVFT",
                              "DIVNRA",
                              "DIVROC",
                              "DIVTW",
                              "DIVTXEX",
                              "FEE",
                              "INT",
                              "INTNRA",
                              "INTTW",
                              "JNL",
                              "JNLC",
                              "JNLS",
                              "MA",
                              "NC",
                              "OPASN",
                              "OPCA",
                              "OPCSH",
                              "OPEXC",
                              "OPEXP",
                              "OPTRD",
                              "PTC",
                              "PTR",
                              "REORG",
                              "SPIN",
                              "SPLIT"
                            ],
                            "x-examples": {
                              "example-1": "FILL"
                            },
                            "x-readme-ref-name": "ActivityType"
                          },
                          "id": {
                            "type": "string",
                            "description": "An id for the activity. Always in “::” format. Can be sent as page_token in requests to facilitate the paging of results."
                          },
                          "cum_qty": {
                            "description": "The cumulative quantity of shares involved in the execution.",
                            "type": "string"
                          },
                          "leaves_qty": {
                            "type": "string",
                            "description": "For partially_filled orders, the quantity of shares that are left to be filled.\n"
                          },
                          "price": {
                            "type": "string",
                            "description": "The per-share price that the trade was executed at."
                          },
                          "qty": {
                            "type": "string",
                            "description": "The number of shares involved in the trade execution."
                          },
                          "side": {
                            "type": "string",
                            "description": "buy or sell"
                          },
                          "symbol": {
                            "type": "string",
                            "description": "The symbol of the security being traded.",
                            "example": "AAPL"
                          },
                          "transaction_time": {
                            "type": "string",
                            "description": "The time at which the execution occurred.",
                            "format": "date-time"
                          },
                          "order_id": {
                            "type": "string",
                            "description": "The id for the order that filled.",
                            "format": "uuid"
                          },
                          "type": {
                            "type": "string",
                            "description": "fill or partial_fill",
                            "enum": [
                              "fill",
                              "partial_fill"
                            ],
                            "example": "fill"
                          },
                          "order_status": {
                            "type": "string",
                            "title": "OrderStatus",
                            "description": "An order executed through Alpaca can experience several status changes during its lifecycle. The most common statuses are described in detail below:\n\n- new\n  The order has been received by Alpaca, and routed to exchanges for execution. This is the usual initial state of an order.\n\n- partially_filled\n  The order has been partially filled.\n\n- filled\n  The order has been filled, and no further updates will occur for the order.\n\n- done_for_day\n  The order is done executing for the day, and will not receive further updates until the next trading day.\n\n- canceled\n  The order has been canceled, and no further updates will occur for the order. This can be either due to a cancel request by the user, or the order has been canceled by the exchanges due to its time-in-force.\n\n- expired\n  The order has expired, and no further updates will occur for the order.\n\n- replaced\n  The order was replaced by another order, or was updated due to a market event such as corporate action.\n\n- pending_cancel\n  The order is waiting to be canceled.\n\n- pending_replace\n  The order is waiting to be replaced by another order. The order will reject cancel request while in this state.\n\nLess common states are described below. Note that these states only occur on very rare occasions, and most users will likely never see their orders reach these states:\n\n- accepted\n  The order has been received by Alpaca, but hasn’t yet been routed to the execution venue. This could be seen often out side of trading session hours.\n\n- pending_new\n  The order has been received by Alpaca, and routed to the exchanges, but has not yet been accepted for execution. This state only occurs on rare occasions.\n\n- accepted_for_bidding\n  The order has been received by exchanges, and is evaluated for pricing. This state only occurs on rare occasions.\n\n- stopped\n  The order has been stopped, and a trade is guaranteed for the order, usually at a stated price or better, but has not yet occurred. This state only occurs on rare occasions.\n\n- rejected\n  The order has been rejected, and no further updates will occur for the order. This state occurs on rare occasions and may occur based on various conditions decided by the exchanges.\n\n- suspended\n  The order has been suspended, and is not eligible for trading. This state only occurs on rare occasions.\n\n- calculated\n  The order has been completed for the day (either filled or done for day), but remaining settlement calculations are still pending. This state only occurs on rare occasions.\n\n\nAn order may be canceled through the API up until the point it reaches a state of either filled, canceled, or expired.",
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
                            "example": "new",
                            "x-readme-ref-name": "OrderStatus"
                          }
                        },
                        "x-readme-ref-name": "TradingActivities"
                      },
                      {
                        "title": "AccountNonTradeActivities",
                        "type": "object",
                        "properties": {
                          "activity_type": {
                            "type": "string",
                            "title": "ActivityType",
                            "description": "- FILL\n  Order fills (both partial and full fills)\n\n- TRANS\n  Cash transactions (both CSD and CSW)\n\n- MISC\n  Miscellaneous or rarely used activity types (All types except those in TRANS, DIV, or FILL)\n\n- ACATC\n  ACATS IN/OUT (Cash)\n\n- ACATS\n  ACATS IN/OUT (Securities)\n\n- CFEE\n  Crypto fee\n\n- CSD\n  Cash deposit(+)\n\n- CSW\n  Cash withdrawal(-)\n\n- DIV\n  Dividends\n\n- DIVCGL\n  Dividend (capital gain long term)\n\n- DIVCGS\n  Dividend (capital gain short term)\n\n- DIVFEE\n  Dividend fee\n\n- DIVFT\n  Dividend adjusted (Foreign Tax Withheld)\n\n- DIVNRA\n  Dividend adjusted (NRA Withheld)\n\n- DIVROC\n  Dividend return of capital\n\n- DIVTW\n  Dividend adjusted (Tefra Withheld)\n\n- DIVTXEX\n  Dividend (tax exempt)\n\n- FEE\n  Fee denominated in USD\n\n- INT\n  Interest (credit/margin)\n\n- INTNRA\n  Interest adjusted (NRA Withheld)\n\n- INTTW\n  Interest adjusted (Tefra Withheld)\n\n- JNL\n  Journal entry\n\n- JNLC\n  Journal entry (cash)\n\n- JNLS\n  Journal entry (stock)\n\n- MA\n  Merger/Acquisition\n\n- NC\n  Name change\n\n- OPASN\n  Option assignment\n\n- OPCA\n  Option corporate action\n\n- OPCSH\n  Option cash deliverable for non-standard contracts\n\n- OPEXC\n  Option exercise\n\n- OPEXP\n  Option expiration\n\n- OPTRD\n  Option trade\n\n- PTC\n  Pass Thru Charge\n\n- PTR\n  Pass Thru Rebate\n\n- REORG\n  Reorg CA\n\n- SPIN\n  Stock spinoff\n\n- SPLIT\n  Stock split",
                            "enum": [
                              "FILL",
                              "TRANS",
                              "MISC",
                              "ACATC",
                              "ACATS",
                              "CFEE",
                              "CSD",
                              "CSW",
                              "DIV",
                              "DIVCGL",
                              "DIVCGS",
                              "DIVFEE",
                              "DIVFT",
                              "DIVNRA",
                              "DIVROC",
                              "DIVTW",
                              "DIVTXEX",
                              "FEE",
                              "INT",
                              "INTNRA",
                              "INTTW",
                              "JNL",
                              "JNLC",
                              "JNLS",
                              "MA",
                              "NC",
                              "OPASN",
                              "OPCA",
                              "OPCSH",
                              "OPEXC",
                              "OPEXP",
                              "OPTRD",
                              "PTC",
                              "PTR",
                              "REORG",
                              "SPIN",
                              "SPLIT"
                            ],
                            "x-examples": {
                              "example-1": "FILL"
                            },
                            "x-readme-ref-name": "ActivityType"
                          },
                          "activity_sub_type": {
                            "title": "ActivitySubType",
                            "type": "string",
                            "description": "Represents a more specific classification to the `activity_type`.\nThis field is optional and may not always be populated, depending on the activity type and the available data.\nEach `activity_type` has a set of valid `activity_sub_type` values.\n\nFull mapping of `activity_type` to `activity_sub_type`:\n\n- **DIV**: Dividend activity sub-types:\n  - **CDIV**: Cash Dividend\n  - **SDIV**: Stock Dividend\n  - **SPD**: Substitute Payment In Lieu Of Dividend\n\n- **FEE**: Fee-related activity sub-types:\n  - **REG**: Regulatory Fee\n  - **TAF**: Trading Activity Fee\n  - **LCT**: Local Currency Trading Fee\n  - **ORF**: Options Regulatory Fee\n  - **OCC**: Options Clearing Corporation Fee\n  - **NRC**: Non-Retail Commission Fee\n  - **NRV**: Non-Retail Venue Fee\n  - **COM**: Commission\n  - **CAT**: Consolidated Audit Trail Fee\n\n- **INT**: Interest-related activity sub-types:\n  - **MGN**: Margin Interest\n  - **CDT**: Credit Interest\n  - **SWP**: Sweep Interest\n  - **QII**: Qualified Interest\n\n- **MA**: Merger and Acquisition activity sub-types:\n  - **CMA**: Cash Merger\n  - **SMA**: Stock Merger\n  - **SCMA**: Stock & Cash Merger\n\n- **NC**: Name Change activity sub types\n  - **SNC**: Symbol Name Change\n  - **CNC**: CUSIP Name Change\n  - **SCNC**: Symbol & CUSIP Name Change\n\n- **OPCA**: Option Corporate Action activity sub-types:\n  - **DIV.CDIV**: Cash Dividend\n  - **DIV.SDIV**: Stock Dividend\n  - **MA.CMA**: Cash Merger\n  - **MA.SMA**: Stock Merger\n  - **MA.SCMA**: Stock & Cash Merger\n  - **NC.CNC**: CUSIP Name Change\n  - **NC.SNC**: Symbol Name Change\n  - **NC.SCNC**: Symbol & CUSIP Name Change\n  - **SPIN**: Spin-off\n  - **SPLIT.FSPLIT**: Forward Stock Split\n  - **SPLIT.RSPLIT**: Reverse Stock Split\n  - **SPLIT.USPLIT**: Unit Split\n\n- **REORG**: Reorganization activity sub-types:\n  - **WRM**: Worthless Removal\n\n- **SPLIT**: Stock Split activity sub-types:\n  - **FSPLIT**: Forward Stock Split\n  - **RSPLIT**: Reverse Stock Split\n  - **USPLIT**: Unit Split\n\n- **VOF**: Voluntary Offering activity sub-types:\n  - **VTND**: Tender Offer\n  - **VWRT**: Warrant Exercise\n  - **VRGT**: Rights Offer\n  - **VEXH**: Exchange Offer\n\n- **WH**: Withholding activity sub-types:\n  - **SWH**: State Withholding\n  - **FWH**: Federal Withholding\n  - **SLWH**: Sales Withholding",
                            "x-readme-ref-name": "ActivitySubType"
                          },
                          "id": {
                            "type": "string",
                            "description": "An ID for the activity, always in “::” format. Can be sent as page_token in requests to facilitate the paging of results."
                          },
                          "date": {
                            "type": "string",
                            "description": "The date on which the activity occurred or on which the transaction associated with the activity settled.",
                            "format": "date-time"
                          },
                          "net_amount": {
                            "type": "string",
                            "description": "The net amount of money (positive or negative) associated with the activity."
                          },
                          "symbol": {
                            "type": "string",
                            "description": "The symbol of the security involved with the activity. Not present for all activity types."
                          },
                          "cusip": {
                            "type": "string",
                            "description": "The CUSIP of the security involved with the activity. Not present for all activity types."
                          },
                          "qty": {
                            "type": "string",
                            "description": "For dividend activities, the number of shares that contributed to the payment. Not present for other activity types.\n"
                          },
                          "per_share_amount": {
                            "type": "string",
                            "description": "For dividend activities, the average amount paid per share. Not present for other activity types."
                          },
                          "group_id": {
                            "type": "string",
                            "description": "ID used to link activities who share a sibling relationship."
                          },
                          "status": {
                            "type": "string",
                            "description": "The activity status.",
                            "enum": [
                              "executed",
                              "correct",
                              "canceled"
                            ]
                          },
                          "created_at": {
                            "type": "string",
                            "format": "date-time",
                            "description": "Valid only for non-trading activity types. Null for trading activites."
                          }
                        },
                        "x-examples": {
                          "example-1": {
                            "activity_type": "DIV",
                            "activity_sub_type": "SDIV",
                            "id": "20190801011955195::5f596936-6f23-4cef-bdf1-3806aae57dbf",
                            "date": "2019-08-01",
                            "net_amount": "1.02",
                            "symbol": "T",
                            "qty": "2",
                            "per_share_amount": "0.51",
                            "status": "executed",
                            "created_at": "2021-05-10T14:01:04.650275Z"
                          }
                        },
                        "x-readme-ref-name": "NonTradeActivities"
                      }
                    ],
                    "description": "Will be a mix of TradingActivity or NonTradeActivity objects based on what is passed in the activity_types parameter"
                  }
                }
              }
            }
          }
        },
        "operationId": "getAccountActivities",
        "description": "Returns a list of activities\n\nNotes:\n* Pagination is handled using the `page_token` and `page_size` parameters.\n* `page_token` represents the ID of the last item on your current page of results.\n   For example, if the ID of the last activity in your first response is `20220203000000000::045b3b8d-c566-4bef-b741-2bf598dd6ae7`, you would pass that value as `page_token` to retrieve the next page of results.",
        "parameters": [
          {
            "name": "activity_types",
            "in": "query",
            "schema": {
              "type": "array",
              "items": {
                "type": "string",
                "title": "ActivityType",
                "description": "- FILL\n  Order fills (both partial and full fills)\n\n- TRANS\n  Cash transactions (both CSD and CSW)\n\n- MISC\n  Miscellaneous or rarely used activity types (All types except those in TRANS, DIV, or FILL)\n\n- ACATC\n  ACATS IN/OUT (Cash)\n\n- ACATS\n  ACATS IN/OUT (Securities)\n\n- CFEE\n  Crypto fee\n\n- CSD\n  Cash deposit(+)\n\n- CSW\n  Cash withdrawal(-)\n\n- DIV\n  Dividends\n\n- DIVCGL\n  Dividend (capital gain long term)\n\n- DIVCGS\n  Dividend (capital gain short term)\n\n- DIVFEE\n  Dividend fee\n\n- DIVFT\n  Dividend adjusted (Foreign Tax Withheld)\n\n- DIVNRA\n  Dividend adjusted (NRA Withheld)\n\n- DIVROC\n  Dividend return of capital\n\n- DIVTW\n  Dividend adjusted (Tefra Withheld)\n\n- DIVTXEX\n  Dividend (tax exempt)\n\n- FEE\n  Fee denominated in USD\n\n- INT\n  Interest (credit/margin)\n\n- INTNRA\n  Interest adjusted (NRA Withheld)\n\n- INTTW\n  Interest adjusted (Tefra Withheld)\n\n- JNL\n  Journal entry\n\n- JNLC\n  Journal entry (cash)\n\n- JNLS\n  Journal entry (stock)\n\n- MA\n  Merger/Acquisition\n\n- NC\n  Name change\n\n- OPASN\n  Option assignment\n\n- OPCA\n  Option corporate action\n\n- OPCSH\n  Option cash deliverable for non-standard contracts\n\n- OPEXC\n  Option exercise\n\n- OPEXP\n  Option expiration\n\n- OPTRD\n  Option trade\n\n- PTC\n  Pass Thru Charge\n\n- PTR\n  Pass Thru Rebate\n\n- REORG\n  Reorg CA\n\n- SPIN\n  Stock spinoff\n\n- SPLIT\n  Stock split",
                "enum": [
                  "FILL",
                  "TRANS",
                  "MISC",
                  "ACATC",
                  "ACATS",
                  "CFEE",
                  "CSD",
                  "CSW",
                  "DIV",
                  "DIVCGL",
                  "DIVCGS",
                  "DIVFEE",
                  "DIVFT",
                  "DIVNRA",
                  "DIVROC",
                  "DIVTW",
                  "DIVTXEX",
                  "FEE",
                  "INT",
                  "INTNRA",
                  "INTTW",
                  "JNL",
                  "JNLC",
                  "JNLS",
                  "MA",
                  "NC",
                  "OPASN",
                  "OPCA",
                  "OPCSH",
                  "OPEXC",
                  "OPEXP",
                  "OPTRD",
                  "PTC",
                  "PTR",
                  "REORG",
                  "SPIN",
                  "SPLIT"
                ],
                "x-examples": {
                  "example-1": "FILL"
                },
                "x-readme-ref-name": "ActivityType"
              }
            },
            "style": "form",
            "explode": false,
            "description": "A comma-separated list of activity types used to filter the results."
          },
          {
            "name": "category",
            "in": "query",
            "schema": {
              "type": "string",
              "enum": [
                "trade_activity",
                "non_trade_activity"
              ]
            },
            "description": "The activity category. Cannot be used with \"activity_types\" parameter."
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
            "schema": {
              "type": "string",
              "enum": [
                "asc",
                "desc"
              ],
              "default": "desc",
              "example": "desc"
            },
            "description": "The chronological order of response based on the activity datetime."
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
