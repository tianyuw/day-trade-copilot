---
source_view: https://docs.alpaca.markets/reference/replaceorderforaccount
source_md: https://docs.alpaca.markets/reference/replaceorderforaccount.md
scraped_at_utc: 2026-01-27T04:30:48Z
---
# Replace an Order

Replaces a single order with updated parameters. Each parameter overrides the corresponding attribute of the existing order. The other attributes remain the same as the existing order.

A success return code from a replaced order does NOT guarantee the existing open order has been replaced. If the existing open order is filled before the replacing (new) order reaches the execution venue, the replacing (new) order is rejected, and these events are sent in the trade_updates stream channel found [here](https://docs.alpaca.markets/reference/subscribetotradev2sse).

While an order is being replaced, the account's buying power is reduced by the larger of the two orders that have been placed (the old order being replaced, and the newly placed order to replace it). If you are replacing a buy entry order with a higher limit price than the original order, the buying power is calculated based on the newly placed order. If you are replacing it with a lower limit price, the buying power is calculated based on the old order.

Note: Order cannot be replaced when the status is `accepted`, `pending_new`, `pending_cancel` or `pending_replace`.

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
      "name": "Trading"
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
    "/v1/trading/accounts/{account_id}/orders/{order_id}": {
      "parameters": [
        {
          "name": "account_id",
          "in": "path",
          "required": true,
          "description": "Account identifier.",
          "schema": {
            "type": "string",
            "format": "uuid"
          }
        },
        {
          "name": "order_id",
          "in": "path",
          "required": true,
          "description": "Order identifier.",
          "schema": {
            "type": "string"
          }
        }
      ],
      "patch": {
        "summary": "Replace an Order",
        "tags": [
          "Trading"
        ],
        "description": "Replaces a single order with updated parameters. Each parameter overrides the corresponding attribute of the existing order. The other attributes remain the same as the existing order.\n\nA success return code from a replaced order does NOT guarantee the existing open order has been replaced. If the existing open order is filled before the replacing (new) order reaches the execution venue, the replacing (new) order is rejected, and these events are sent in the trade_updates stream channel found [here](https://docs.alpaca.markets/reference/subscribetotradev2sse).\n\nWhile an order is being replaced, the account's buying power is reduced by the larger of the two orders that have been placed (the old order being replaced, and the newly placed order to replace it). If you are replacing a buy entry order with a higher limit price than the original order, the buying power is calculated based on the newly placed order. If you are replacing it with a lower limit price, the buying power is calculated based on the old order.\n\nNote: Order cannot be replaced when the status is `accepted`, `pending_new`, `pending_cancel` or `pending_replace`.",
        "requestBody": {
          "required": true,
          "content": {
            "application/json": {
              "schema": {
                "type": "object",
                "title": "OrderUpdateRequest",
                "description": "Represents the fields that are editable in an order replace/update call.\n\nNote: client_order_id is currently not editable on its own, one of the other fields must be changed at the same time to effectively replace the order",
                "properties": {
                  "qty": {
                    "type": "string",
                    "format": "decimal",
                    "example": "4",
                    "description": "You can only patch full shares for now.\n\nQty of equity fractional/notional orders are not allowed to change.\nIn case of multi-leg orders represents the number of units to trade of this strategy."
                  },
                  "time_in_force": {
                    "type": "string",
                    "title": "TimeInForce",
                    "description": "The Time-In-Force values supported by Alpaca vary based on the order's security type. Here is a breakdown of the supported TIFs for each specific security type:\n- Equity trading: day, gtc, opg, cls, ioc, fok.\n- Options trading: day.\n- Crypto trading: gtc, ioc.\n\nBelow are the descriptions of each TIF:\n- day:\n  A day order is eligible for execution only on the day it is live. By default, the order is only valid during Regular Trading Hours (9:30am - 4:00pm ET). If unfilled after the closing auction, it is automatically canceled. If submitted after the close, it is queued and submitted the following trading day. However, if marked as eligible for extended hours, the order can also execute during supported extended hours.\n\n- gtc:\n  The order is good until canceled. Non-marketable GTC limit orders are subject to price adjustments to offset corporate actions affecting the issue. We do not currently support Do Not Reduce(DNR) orders to opt out of such price adjustments.\n\n- opg:\n  Use this TIF with a market/limit order type to submit “market on open” (MOO) and “limit on open” (LOO) orders. This order is eligible to execute only in the market opening auction. Any unfilled orders after the open will be cancelled. OPG orders submitted after 9:28am but before 7:00pm ET will be rejected. OPG orders submitted after 7:00pm will be queued and routed to the following day’s opening auction. On open/on close orders are routed to the primary exchange. Such orders do not necessarily execute exactly at 9:30am / 4:00pm ET but execute per the exchange’s auction rules.\n\n- cls:\n  Use this TIF with a market/limit order type to submit “market on close” (MOC) and “limit on close” (LOC) orders. This order is eligible to execute only in the market closing auction. Any unfilled orders after the close will be cancelled. CLS orders submitted after 3:50pm but before 7:00pm ET will be rejected. CLS orders submitted after 7:00pm will be queued and routed to the following day’s closing auction. Only available with API v2.\n\n- ioc:\n  An Immediate Or Cancel (IOC) order requires all or part of the order to be executed immediately. Any unfilled portion of the order is canceled. Only available with API v2. Most market makers who receive IOC orders will attempt to fill the order on a principal basis only, and cancel any unfilled balance. On occasion, this can result in the entire order being cancelled if the market maker does not have any existing inventory of the security in question.\n\n- fok:\n  A Fill or Kill (FOK) order is only executed if the entire order quantity can be filled, otherwise the order is canceled. Only available with API v2.",
                    "enum": [
                      "day",
                      "gtc",
                      "opg",
                      "cls",
                      "ioc",
                      "fok"
                    ],
                    "example": "gtc",
                    "x-readme-ref-name": "TimeInForce"
                  },
                  "limit_price": {
                    "type": "string",
                    "format": "decimal",
                    "example": "3.14",
                    "description": "Required if original order's `type` field was `limit` or `stop_limit`.\nIn case of `mleg`, the limit_price parameter is expressed with the following notation:\n- A positive value indicates a debit, representing a cost or payment to be made.\n- A negative value signifies a credit, reflecting an amount to be received."
                  },
                  "stop_price": {
                    "type": "string",
                    "format": "decimal",
                    "example": "3.14",
                    "description": "Required if original order's `type` field was stop or stop_limit"
                  },
                  "trail": {
                    "type": "string",
                    "format": "decimal",
                    "example": "3.14",
                    "description": "The new value of the trail_price or trail_percent"
                  },
                  "client_order_id": {
                    "type": "string",
                    "example": "61e69015-8549-4bfd-b9c3-01e75843f47d",
                    "description": "A unique identifier for the new order. Automatically generated if not sent. (<= 128 characters)",
                    "maxLength": 128
                  }
                },
                "x-stoplight": {
                  "id": "iip4vylvgdefq"
                },
                "x-readme-ref-name": "UpdateOrderRequest"
              }
            }
          }
        },
        "responses": {
          "200": {
            "description": "A new Order object with a new order_id",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "x-stoplight": {
                    "id": "aygszffe87j44"
                  },
                  "properties": {
                    "id": {
                      "type": "string",
                      "format": "uuid",
                      "example": "61e69015-8549-4bfd-b9c3-01e75843f47d",
                      "description": "Order ID generated by Alpaca"
                    },
                    "client_order_id": {
                      "type": "string",
                      "example": "61e69015-8549-4bfd-b9c3-01e75843f47d",
                      "description": "Client unique order ID",
                      "maxLength": 128
                    },
                    "created_at": {
                      "type": "string",
                      "format": "date-time",
                      "example": "2021-03-16T18:38:01.942282Z",
                      "description": "Time when order was entered"
                    },
                    "updated_at": {
                      "type": "string",
                      "format": "date-time",
                      "example": "2021-03-16T18:38:01.942282Z",
                      "description": "Time of most recent change to the order"
                    },
                    "submitted_at": {
                      "type": "string",
                      "format": "date-time",
                      "example": "2021-03-16T18:38:01.942282Z",
                      "description": "Time the order was submitted for execution or, if not yet submitted the created_at time. Because orders are submitted for execution asynchronous to database updates, at times this may be before the created_at time."
                    },
                    "filled_at": {
                      "type": "string",
                      "format": "date-time",
                      "example": "2021-03-16T18:38:01.942282Z",
                      "description": "Time the order was filled. Can be null if not filled",
                      "nullable": true
                    },
                    "cancel_requested_at": {
                      "type": "string",
                      "format": "date-time",
                      "example": "2021-03-16T18:38:01.942282Z",
                      "description": "Time when cancellation or bust was requested (if applicable)",
                      "nullable": true
                    },
                    "expired_at": {
                      "type": "string",
                      "format": "date-time",
                      "example": "2021-03-16T18:38:01.942282Z",
                      "description": "Can be null",
                      "nullable": true
                    },
                    "canceled_at": {
                      "type": "string",
                      "format": "date-time",
                      "example": "2021-03-16T18:38:01.942282Z",
                      "description": "Can be null",
                      "nullable": true
                    },
                    "failed_at": {
                      "type": "string",
                      "format": "date-time",
                      "example": "2021-03-16T18:38:01.942282Z",
                      "description": "Can be null",
                      "nullable": true
                    },
                    "replaced_at": {
                      "type": "string",
                      "format": "date-time",
                      "example": "2021-03-16T18:38:01.942282Z",
                      "description": "Can be null",
                      "nullable": true
                    },
                    "replaced_by": {
                      "type": "string",
                      "format": "uuid",
                      "example": "61e69015-8549-4bfd-b9c3-01e75843f47d",
                      "description": "The order ID that this order was replaced by. (Can be null)",
                      "nullable": true
                    },
                    "replaces": {
                      "type": "string",
                      "format": "uuid",
                      "example": "61e69015-8549-4bfd-b9c3-01e75843f47d",
                      "description": "The order ID that this order replaces. (Can be null)",
                      "nullable": true
                    },
                    "asset_id": {
                      "type": "string",
                      "format": "uuid",
                      "example": "61e69015-8549-4bfd-b9c3-01e75843f47d",
                      "description": "The asset ID (For options this represents the option contract ID)"
                    },
                    "symbol": {
                      "type": "string",
                      "example": "AALP",
                      "description": "The asset symbol"
                    },
                    "asset_class": {
                      "type": "string",
                      "description": "This represents the category to which the asset belongs to. It serves to identify the nature of the financial instrument, with options including \"us_equity\" for U.S. equities, \"us_option\" for U.S. options, and \"crypto\" for cryptocurrencies.",
                      "enum": [
                        "us_equity",
                        "us_option",
                        "crypto"
                      ],
                      "x-stoplight": {
                        "id": "0stvwzkbv2e0u"
                      },
                      "x-readme-ref-name": "AssetClass"
                    },
                    "notional": {
                      "type": "string",
                      "format": "decimal",
                      "example": "4.2",
                      "description": "Ordered notional amount. If entered, qty will be null. Can take up to 2 decimal points.",
                      "nullable": true
                    },
                    "qty": {
                      "type": "string",
                      "format": "decimal",
                      "example": "4.2",
                      "description": "Ordered quantity. If entered, notional will be null. Can take up to 2 decimal points.",
                      "nullable": true
                    },
                    "filled_qty": {
                      "type": "string",
                      "format": "decimal",
                      "example": "4.2",
                      "description": "Filled quantity"
                    },
                    "filled_avg_price": {
                      "type": "string",
                      "format": "decimal",
                      "example": "4.2",
                      "description": "Filled average price. Can be 0 until order is processed in case order is passed outside of market hours",
                      "nullable": true
                    },
                    "order_class": {
                      "type": "string",
                      "enum": [
                        "simple",
                        "bracket",
                        "oco",
                        "oto",
                        "mleg"
                      ],
                      "description": "The order classes supported by Alpaca vary based on the order's security type. The following provides a comprehensive breakdown of the supported order classes for each category:\n  - Equity trading: simple (or \"\"), oco, oto, bracket.\n  - Options trading:\n    - simple (or \"\")\n    - mleg (required for multi-leg complex option strategies)\n  - Crypto trading: simple (or \"\").",
                      "example": "bracket",
                      "x-stoplight": {
                        "id": "5lrkevtge17ap"
                      },
                      "x-readme-ref-name": "OrderClass"
                    },
                    "order_type": {
                      "type": "string",
                      "enum": [
                        "market",
                        "limit",
                        "stop",
                        "stop_limit",
                        "trailing_stop"
                      ],
                      "example": "market",
                      "description": "The order types supported by Alpaca vary based on the order's security type. The following provides a comprehensive breakdown of the supported order types for each category:\n - Equity trading: market, limit, stop, stop_limit, trailing_stop.\n - Options trading: market, limit.\n - Options Multileg trading: market, limit.\n - Crypto trading: market, limit, stop_limit.",
                      "title": "OrderType",
                      "x-readme-ref-name": "OrderType"
                    },
                    "type": {
                      "type": "string",
                      "enum": [
                        "market",
                        "limit",
                        "stop",
                        "stop_limit",
                        "trailing_stop"
                      ],
                      "example": "market",
                      "description": "The order types supported by Alpaca vary based on the order's security type. The following provides a comprehensive breakdown of the supported order types for each category:\n - Equity trading: market, limit, stop, stop_limit, trailing_stop.\n - Options trading: market, limit.\n - Options Multileg trading: market, limit.\n - Crypto trading: market, limit, stop_limit.",
                      "title": "OrderType",
                      "x-readme-ref-name": "OrderType"
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
                    "time_in_force": {
                      "type": "string",
                      "title": "TimeInForce",
                      "description": "The Time-In-Force values supported by Alpaca vary based on the order's security type. Here is a breakdown of the supported TIFs for each specific security type:\n- Equity trading: day, gtc, opg, cls, ioc, fok.\n- Options trading: day.\n- Crypto trading: gtc, ioc.\n\nBelow are the descriptions of each TIF:\n- day:\n  A day order is eligible for execution only on the day it is live. By default, the order is only valid during Regular Trading Hours (9:30am - 4:00pm ET). If unfilled after the closing auction, it is automatically canceled. If submitted after the close, it is queued and submitted the following trading day. However, if marked as eligible for extended hours, the order can also execute during supported extended hours.\n\n- gtc:\n  The order is good until canceled. Non-marketable GTC limit orders are subject to price adjustments to offset corporate actions affecting the issue. We do not currently support Do Not Reduce(DNR) orders to opt out of such price adjustments.\n\n- opg:\n  Use this TIF with a market/limit order type to submit “market on open” (MOO) and “limit on open” (LOO) orders. This order is eligible to execute only in the market opening auction. Any unfilled orders after the open will be cancelled. OPG orders submitted after 9:28am but before 7:00pm ET will be rejected. OPG orders submitted after 7:00pm will be queued and routed to the following day’s opening auction. On open/on close orders are routed to the primary exchange. Such orders do not necessarily execute exactly at 9:30am / 4:00pm ET but execute per the exchange’s auction rules.\n\n- cls:\n  Use this TIF with a market/limit order type to submit “market on close” (MOC) and “limit on close” (LOC) orders. This order is eligible to execute only in the market closing auction. Any unfilled orders after the close will be cancelled. CLS orders submitted after 3:50pm but before 7:00pm ET will be rejected. CLS orders submitted after 7:00pm will be queued and routed to the following day’s closing auction. Only available with API v2.\n\n- ioc:\n  An Immediate Or Cancel (IOC) order requires all or part of the order to be executed immediately. Any unfilled portion of the order is canceled. Only available with API v2. Most market makers who receive IOC orders will attempt to fill the order on a principal basis only, and cancel any unfilled balance. On occasion, this can result in the entire order being cancelled if the market maker does not have any existing inventory of the security in question.\n\n- fok:\n  A Fill or Kill (FOK) order is only executed if the entire order quantity can be filled, otherwise the order is canceled. Only available with API v2.",
                      "enum": [
                        "day",
                        "gtc",
                        "opg",
                        "cls",
                        "ioc",
                        "fok"
                      ],
                      "example": "gtc",
                      "x-readme-ref-name": "TimeInForce"
                    },
                    "limit_price": {
                      "type": "string",
                      "format": "decimal",
                      "example": "3.14",
                      "description": "Limit price",
                      "nullable": true
                    },
                    "stop_price": {
                      "type": "string",
                      "format": "decimal",
                      "example": "3.14",
                      "description": "Stop price",
                      "nullable": true
                    },
                    "status": {
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
                    },
                    "extended_hours": {
                      "type": "boolean",
                      "example": true
                    },
                    "legs": {
                      "type": "array",
                      "description": "When querying non-simple order_class orders in a nested style, an array of Order entities associated with this order. Otherwise, null.",
                      "nullable": true,
                      "items": {
                        "type": "object",
                        "properties": {
                          "id": {
                            "type": "string",
                            "format": "uuid",
                            "example": "61e69015-8549-4bfd-b9c3-01e75843f47d",
                            "description": "Order ID generated by Alpaca"
                          },
                          "client_order_id": {
                            "type": "string",
                            "example": "61e69015-8549-4bfd-b9c3-01e75843f47d",
                            "description": "Client unique order ID",
                            "maxLength": 128
                          },
                          "created_at": {
                            "type": "string",
                            "format": "date-time",
                            "example": "2021-03-16T18:38:01.942282Z",
                            "description": "Time when order was entered"
                          },
                          "updated_at": {
                            "type": "string",
                            "format": "date-time",
                            "example": "2021-03-16T18:38:01.942282Z",
                            "description": "Time of most recent change to the order"
                          },
                          "submitted_at": {
                            "type": "string",
                            "format": "date-time",
                            "example": "2021-03-16T18:38:01.942282Z",
                            "description": "Time the order was submitted for execution or, if not yet submitted the created_at time. Because orders are submitted for execution asynchronous to database updates, at times this may be before the created_at time."
                          },
                          "filled_at": {
                            "type": "string",
                            "format": "date-time",
                            "example": "2021-03-16T18:38:01.942282Z",
                            "description": "Time the order was filled. Can be null if not filled",
                            "nullable": true
                          },
                          "expired_at": {
                            "type": "string",
                            "format": "date-time",
                            "example": "2021-03-16T18:38:01.942282Z",
                            "description": "Can be null",
                            "nullable": true
                          },
                          "canceled_at": {
                            "type": "string",
                            "format": "date-time",
                            "example": "2021-03-16T18:38:01.942282Z",
                            "description": "Can be null",
                            "nullable": true
                          },
                          "failed_at": {
                            "type": "string",
                            "format": "date-time",
                            "example": "2021-03-16T18:38:01.942282Z",
                            "description": "Can be null",
                            "nullable": true
                          },
                          "replaced_at": {
                            "type": "string",
                            "format": "date-time",
                            "example": "2021-03-16T18:38:01.942282Z",
                            "description": "Can be null",
                            "nullable": true
                          },
                          "replaced_by": {
                            "type": "string",
                            "format": "uuid",
                            "example": "61e69015-8549-4bfd-b9c3-01e75843f47d",
                            "description": "The order ID that this order was replaced by. (Can be null)",
                            "nullable": true
                          },
                          "replaces": {
                            "type": "string",
                            "format": "uuid",
                            "example": "61e69015-8549-4bfd-b9c3-01e75843f47d",
                            "description": "The order ID that this order replaces. (Can be null)",
                            "nullable": true
                          },
                          "asset_id": {
                            "type": "string",
                            "format": "uuid",
                            "example": "61e69015-8549-4bfd-b9c3-01e75843f47d",
                            "description": "The asset ID (For options this represents the option contract ID)"
                          },
                          "symbol": {
                            "type": "string",
                            "example": "AALP",
                            "description": "The asset symbol"
                          },
                          "asset_class": {
                            "type": "string",
                            "description": "This represents the category to which the asset belongs to. It serves to identify the nature of the financial instrument, with options including \"us_equity\" for U.S. equities, \"us_option\" for U.S. options, and \"crypto\" for cryptocurrencies.",
                            "enum": [
                              "us_equity",
                              "us_option",
                              "crypto"
                            ],
                            "x-stoplight": {
                              "id": "0stvwzkbv2e0u"
                            },
                            "x-readme-ref-name": "AssetClass"
                          },
                          "notional": {
                            "type": "string",
                            "format": "decimal",
                            "example": "4.2",
                            "description": "Ordered notional amount. If entered, qty will be null. Can take up to 2 decimal points.",
                            "nullable": true
                          },
                          "qty": {
                            "type": "string",
                            "format": "decimal",
                            "example": "4.2",
                            "description": "Ordered quantity. If entered, notional will be null. Can take up to 2 decimal points.",
                            "nullable": true
                          },
                          "filled_qty": {
                            "type": "string",
                            "format": "decimal",
                            "example": "4.2",
                            "description": "Filled quantity"
                          },
                          "filled_avg_price": {
                            "type": "string",
                            "format": "decimal",
                            "example": "4.2",
                            "description": "Filled average price. Can be 0 until order is processed in case order is passed outside of market hours",
                            "nullable": true
                          },
                          "order_class": {
                            "type": "string",
                            "enum": [
                              "simple",
                              "bracket",
                              "oco",
                              "oto",
                              "mleg"
                            ],
                            "description": "The order classes supported by Alpaca vary based on the order's security type. The following provides a comprehensive breakdown of the supported order classes for each category:\n  - Equity trading: simple (or \"\"), oco, oto, bracket.\n  - Options trading:\n    - simple (or \"\")\n    - mleg (required for multi-leg complex option strategies)\n  - Crypto trading: simple (or \"\").",
                            "example": "bracket",
                            "x-stoplight": {
                              "id": "5lrkevtge17ap"
                            },
                            "x-readme-ref-name": "OrderClass"
                          },
                          "order_type": {
                            "type": "string",
                            "enum": [
                              "market",
                              "limit",
                              "stop",
                              "stop_limit",
                              "trailing_stop"
                            ],
                            "example": "market",
                            "description": "The order types supported by Alpaca vary based on the order's security type. The following provides a comprehensive breakdown of the supported order types for each category:\n - Equity trading: market, limit, stop, stop_limit, trailing_stop.\n - Options trading: market, limit.\n - Options Multileg trading: market, limit.\n - Crypto trading: market, limit, stop_limit.",
                            "title": "OrderType",
                            "x-readme-ref-name": "OrderType"
                          },
                          "type": {
                            "type": "string",
                            "enum": [
                              "market",
                              "limit",
                              "stop",
                              "stop_limit",
                              "trailing_stop"
                            ],
                            "example": "market",
                            "description": "The order types supported by Alpaca vary based on the order's security type. The following provides a comprehensive breakdown of the supported order types for each category:\n - Equity trading: market, limit, stop, stop_limit, trailing_stop.\n - Options trading: market, limit.\n - Options Multileg trading: market, limit.\n - Crypto trading: market, limit, stop_limit.",
                            "title": "OrderType",
                            "x-readme-ref-name": "OrderType"
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
                          "time_in_force": {
                            "type": "string",
                            "title": "TimeInForce",
                            "description": "The Time-In-Force values supported by Alpaca vary based on the order's security type. Here is a breakdown of the supported TIFs for each specific security type:\n- Equity trading: day, gtc, opg, cls, ioc, fok.\n- Options trading: day.\n- Crypto trading: gtc, ioc.\n\nBelow are the descriptions of each TIF:\n- day:\n  A day order is eligible for execution only on the day it is live. By default, the order is only valid during Regular Trading Hours (9:30am - 4:00pm ET). If unfilled after the closing auction, it is automatically canceled. If submitted after the close, it is queued and submitted the following trading day. However, if marked as eligible for extended hours, the order can also execute during supported extended hours.\n\n- gtc:\n  The order is good until canceled. Non-marketable GTC limit orders are subject to price adjustments to offset corporate actions affecting the issue. We do not currently support Do Not Reduce(DNR) orders to opt out of such price adjustments.\n\n- opg:\n  Use this TIF with a market/limit order type to submit “market on open” (MOO) and “limit on open” (LOO) orders. This order is eligible to execute only in the market opening auction. Any unfilled orders after the open will be cancelled. OPG orders submitted after 9:28am but before 7:00pm ET will be rejected. OPG orders submitted after 7:00pm will be queued and routed to the following day’s opening auction. On open/on close orders are routed to the primary exchange. Such orders do not necessarily execute exactly at 9:30am / 4:00pm ET but execute per the exchange’s auction rules.\n\n- cls:\n  Use this TIF with a market/limit order type to submit “market on close” (MOC) and “limit on close” (LOC) orders. This order is eligible to execute only in the market closing auction. Any unfilled orders after the close will be cancelled. CLS orders submitted after 3:50pm but before 7:00pm ET will be rejected. CLS orders submitted after 7:00pm will be queued and routed to the following day’s closing auction. Only available with API v2.\n\n- ioc:\n  An Immediate Or Cancel (IOC) order requires all or part of the order to be executed immediately. Any unfilled portion of the order is canceled. Only available with API v2. Most market makers who receive IOC orders will attempt to fill the order on a principal basis only, and cancel any unfilled balance. On occasion, this can result in the entire order being cancelled if the market maker does not have any existing inventory of the security in question.\n\n- fok:\n  A Fill or Kill (FOK) order is only executed if the entire order quantity can be filled, otherwise the order is canceled. Only available with API v2.",
                            "enum": [
                              "day",
                              "gtc",
                              "opg",
                              "cls",
                              "ioc",
                              "fok"
                            ],
                            "example": "gtc",
                            "x-readme-ref-name": "TimeInForce"
                          },
                          "limit_price": {
                            "type": "string",
                            "format": "decimal",
                            "example": "3.14",
                            "description": "Limit price",
                            "nullable": true
                          },
                          "stop_price": {
                            "type": "string",
                            "format": "decimal",
                            "example": "3.14",
                            "description": "Stop price",
                            "nullable": true
                          },
                          "status": {
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
                          },
                          "extended_hours": {
                            "type": "boolean",
                            "example": true
                          },
                          "legs": {
                            "type": "array",
                            "description": "When querying non-simple order_class orders in a nested style, an array of Order entities associated with this order. Otherwise, null.",
                            "nullable": true
                          },
                          "trail_price": {
                            "type": "string",
                            "format": "decimal",
                            "example": "3.14",
                            "description": "The dollar value away from the high water mark for trailing stop orders.",
                            "nullable": true
                          },
                          "trail_percent": {
                            "type": "string",
                            "format": "decimal",
                            "example": "5.0",
                            "description": "The percent value away from the high water mark for trailing stop orders.",
                            "nullable": true
                          },
                          "hwm": {
                            "type": "string",
                            "format": "decimal",
                            "example": "3.14",
                            "description": "The highest (lowest) market price seen since the trailing stop order was submitted.",
                            "nullable": true
                          },
                          "position_intent": {
                            "type": "string",
                            "enum": [
                              "buy_to_open",
                              "buy_to_close",
                              "sell_to_open",
                              "sell_to_close"
                            ],
                            "example": "buy_to_open",
                            "title": "PositionIntent",
                            "description": "Represents the desired position strategy.",
                            "x-readme-ref-name": "PositionIntent"
                          },
                          "commission": {
                            "type": "string",
                            "format": "decimal",
                            "example": "3.14",
                            "description": "The dollar value commission you want to charge the end user."
                          },
                          "commission_bps": {
                            "type": "string",
                            "format": "decimal",
                            "example": "10",
                            "deprecated": true,
                            "description": "**deprecated**: Please use the commission_type = bps instead and set the desired bps value in the `commission` field.\nThe percent commission you want to charge the end user on the order (expressed in bps). Alpaca will convert the order to a notional amount for purposes of calculating commission.\n"
                          },
                          "commission_type": {
                            "type": "string",
                            "enum": [
                              "notional",
                              "qty",
                              "bps"
                            ],
                            "default": "notional",
                            "example": "qty",
                            "title": "CommissionType",
                            "description": "An enum to select how to interpret the value provided in the commission field.\n\n- notional:\nCharge commission on a per order basis. (When the `commission_type` field is omitted from the order request, this is used as the default).\n\n- qty:\nCharge commission on a per qty/contract basis, pro rated.\n\n- bps:\nThe percent commission you want to charge the end user on the order (expressed in bps). Alpaca will convert the order to a notional amount for purposes of calculating commission.\nCommission value in bps can have up to two decimal places.",
                            "x-readme-ref-name": "CommissionType"
                          },
                          "swap_rate": {
                            "type": "string",
                            "description": "Swap rate is the exchange rate (without mark-up) used to convert the price into local currency or crypto asset"
                          },
                          "swap_fee_bps": {
                            "type": "string",
                            "description": "Fee in basis points on top swap rate charged by the correspondent on every order"
                          },
                          "usd": {
                            "type": "object",
                            "description": "Nested object to encompass the USD equivalent fields for the local currency fields"
                          }
                        },
                        "required": [
                          "id",
                          "symbol"
                        ],
                        "x-readme-ref-name": "OrderLeg"
                      }
                    },
                    "trail_price": {
                      "type": "string",
                      "format": "decimal",
                      "example": "3.14",
                      "description": "The dollar value away from the high water mark for trailing stop orders.",
                      "nullable": true
                    },
                    "trail_percent": {
                      "type": "string",
                      "format": "decimal",
                      "example": "5.0",
                      "description": "The percent value away from the high water mark for trailing stop orders.",
                      "nullable": true
                    },
                    "hwm": {
                      "type": "string",
                      "format": "decimal",
                      "example": "3.14",
                      "description": "The highest (lowest) market price seen since the trailing stop order was submitted.",
                      "nullable": true
                    },
                    "position_intent": {
                      "type": "string",
                      "enum": [
                        "buy_to_open",
                        "buy_to_close",
                        "sell_to_open",
                        "sell_to_close"
                      ],
                      "example": "buy_to_open",
                      "title": "PositionIntent",
                      "description": "Represents the desired position strategy.",
                      "x-readme-ref-name": "PositionIntent"
                    },
                    "commission": {
                      "type": "string",
                      "format": "decimal",
                      "example": "3.14",
                      "description": "The dollar value commission for this order."
                    },
                    "commission_bps": {
                      "type": "string",
                      "format": "decimal",
                      "example": "10",
                      "deprecated": true,
                      "description": "**deprecated**: Please use the commission_type = bps instead and set the desired bps value in the `commission` field.\nThe percent commission you want to charge the end user on the order (expressed in bps). Alpaca will convert the order to a notional amount for purposes of calculating commission.\n"
                    },
                    "commission_type": {
                      "type": "string",
                      "enum": [
                        "notional",
                        "qty",
                        "bps"
                      ],
                      "default": "notional",
                      "example": "qty",
                      "title": "CommissionType",
                      "description": "An enum to select how to interpret the value provided in the commission field.\n\n- notional:\nCharge commission on a per order basis. (When the `commission_type` field is omitted from the order request, this is used as the default).\n\n- qty:\nCharge commission on a per qty/contract basis, pro rated.\n\n- bps:\nThe percent commission you want to charge the end user on the order (expressed in bps). Alpaca will convert the order to a notional amount for purposes of calculating commission.\nCommission value in bps can have up to two decimal places.",
                      "x-readme-ref-name": "CommissionType"
                    },
                    "swap_rate": {
                      "type": "string",
                      "x-stoplight": {
                        "id": "n291a2g9jl9xe"
                      },
                      "description": "Swap rate is the exchange rate (without mark-up) used to convert the price into local currency or crypto asset"
                    },
                    "swap_fee_bps": {
                      "type": "string",
                      "x-stoplight": {
                        "id": "89yg6cj3l3g2h"
                      },
                      "description": "Fee in basis points on top swap rate charged by the correspondent on every order"
                    },
                    "usd": {
                      "type": "object",
                      "x-stoplight": {
                        "id": "h8eckru1banfe"
                      },
                      "description": "Nested object to encompass the USD equivalent fields for the local currency fields"
                    }
                  },
                  "required": [
                    "id",
                    "symbol"
                  ],
                  "x-readme-ref-name": "Order"
                }
              }
            }
          },
          "400": {
            "description": "Malformed input.",
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
          "403": {
            "description": "Buying power or shares are not sufficient"
          },
          "404": {
            "description": "Resource does not exist.",
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
        },
        "operationId": "replaceOrderForAccount"
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
