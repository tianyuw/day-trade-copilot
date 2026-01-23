---
source_view: https://docs.alpaca.markets/reference/getallorders-1
source_md: https://docs.alpaca.markets/reference/getallorders-1.md
scraped_at_utc: 2026-01-22T23:02:18Z
---
# Get All Orders

Retrieves a list of orders for the account, filtered by the supplied query parameters.

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
      "name": "Orders"
    }
  ],
  "paths": {
    "/v2/orders": {
      "get": {
        "tags": [
          "Orders"
        ],
        "summary": "Get All Orders",
        "parameters": [
          {
            "schema": {
              "type": "string",
              "enum": [
                "open",
                "closed",
                "all"
              ],
              "example": "open"
            },
            "in": "query",
            "name": "status",
            "description": "Order status to be queried. open, closed or all. Defaults to open."
          },
          {
            "schema": {
              "type": "integer"
            },
            "in": "query",
            "name": "limit",
            "description": "The maximum number of orders in response. Defaults to 50 and max is 500."
          },
          {
            "schema": {
              "type": "string"
            },
            "in": "query",
            "name": "after",
            "description": "The response will include only ones submitted after this timestamp (exclusive.)"
          },
          {
            "schema": {
              "type": "string"
            },
            "in": "query",
            "name": "until",
            "description": "The response will include only ones submitted until this timestamp (exclusive.)"
          },
          {
            "schema": {
              "type": "string",
              "enum": [
                "asc",
                "desc"
              ]
            },
            "in": "query",
            "name": "direction",
            "description": "The chronological order of response based on the submission time. asc or desc. Defaults to desc."
          },
          {
            "schema": {
              "type": "boolean"
            },
            "in": "query",
            "name": "nested",
            "description": "If true, the result will roll up multi-leg orders under the legs field of primary order."
          },
          {
            "schema": {
              "type": "string"
            },
            "in": "query",
            "name": "symbols",
            "description": "A comma-separated list of symbols to filter by (ex. “AAPL,TSLA,MSFT”). A currency pair is required for crypto orders (ex. “BTCUSD,BCHUSD,LTCUSD,ETCUSD”)."
          },
          {
            "schema": {
              "type": "string"
            },
            "in": "query",
            "name": "side",
            "description": "Filters down to orders that have a matching side field set."
          },
          {
            "name": "asset_class",
            "in": "query",
            "description": "A comma seperated list of asset classes, the response will include only orders in the specified asset classes. By specifying `us_option` as the class, you can query option orders by underlying symbol using the symbols parameter.",
            "schema": {
              "type": "array",
              "items": {
                "type": "string",
                "enum": [
                  "us_equity",
                  "us_option",
                  "crypto",
                  "all"
                ]
              }
            }
          },
          {
            "schema": {
              "type": "string"
            },
            "in": "query",
            "name": "before_order_id",
            "description": "Return orders submitted before the order with this ID (exclusive).\nMutually exclusive with `after_order_id`. Do not combine with `after`/`until`.\n"
          },
          {
            "schema": {
              "type": "string"
            },
            "in": "query",
            "name": "after_order_id",
            "description": "Return orders submitted after the order with this ID (exclusive).\nMutually exclusive with `before_order_id`. Do not combine with `after`/`until`.\n"
          }
        ],
        "responses": {
          "200": {
            "description": "Successful response\n\nAn array of Order objects",
            "content": {
              "application/json": {
                "schema": {
                  "type": "array",
                  "items": {
                    "description": "The Orders API allows a user to monitor, place and cancel their orders with Alpaca.\n\nEach order has a unique identifier provided by the client. This client-side unique order ID will be automatically generated by the system if not provided by the client, and will be returned as part of the order object along with the rest of the fields described below. Once an order is placed, it can be queried using the client-side order ID to check the status.\n\nUpdates on open orders at Alpaca will also be sent over the streaming interface, which is the recommended method of maintaining order state.",
                    "type": "object",
                    "title": "Order",
                    "properties": {
                      "id": {
                        "type": "string",
                        "description": "Order ID"
                      },
                      "client_order_id": {
                        "type": "string",
                        "description": "Client unique order ID",
                        "maxLength": 128
                      },
                      "created_at": {
                        "type": "string",
                        "format": "date-time"
                      },
                      "updated_at": {
                        "type": "string",
                        "format": "date-time",
                        "nullable": true
                      },
                      "submitted_at": {
                        "type": "string",
                        "format": "date-time",
                        "nullable": true
                      },
                      "filled_at": {
                        "type": "string",
                        "format": "date-time",
                        "nullable": true
                      },
                      "expired_at": {
                        "type": "string",
                        "format": "date-time",
                        "nullable": true
                      },
                      "canceled_at": {
                        "type": "string",
                        "format": "date-time",
                        "nullable": true
                      },
                      "failed_at": {
                        "type": "string",
                        "format": "date-time",
                        "nullable": true
                      },
                      "replaced_at": {
                        "type": "string",
                        "format": "date-time",
                        "nullable": true
                      },
                      "replaced_by": {
                        "type": "string",
                        "format": "uuid",
                        "description": "The order ID that this order was replaced by",
                        "nullable": true
                      },
                      "replaces": {
                        "type": "string",
                        "format": "uuid",
                        "description": "The order ID that this order replaces",
                        "nullable": true
                      },
                      "asset_id": {
                        "type": "string",
                        "format": "uuid",
                        "description": "Asset ID (For options this represents the option contract ID)"
                      },
                      "symbol": {
                        "type": "string",
                        "minLength": 1,
                        "description": "Asset symbol, required for all order classes except for `mleg`"
                      },
                      "asset_class": {
                        "type": "string",
                        "title": "AssetClass",
                        "enum": [
                          "us_equity",
                          "us_option",
                          "crypto"
                        ],
                        "example": "us_equity",
                        "description": "This represents the category to which the asset belongs to. It serves to identify the nature of the financial instrument, with options including \"us_equity\" for U.S. equities, \"us_option\" for U.S. options, and \"crypto\" for cryptocurrencies.",
                        "x-examples": {
                          "example-1": "us_equity"
                        },
                        "x-readme-ref-name": "AssetClass"
                      },
                      "notional": {
                        "type": "string",
                        "minLength": 1,
                        "description": "Ordered notional amount. If entered, qty will be null. Can take up to 9 decimal points.",
                        "nullable": true
                      },
                      "qty": {
                        "type": "string",
                        "minLength": 1,
                        "description": "Ordered quantity. If entered, notional will be null. Can take up to 9 decimal points. Required if order class is `mleg`.",
                        "nullable": true
                      },
                      "filled_qty": {
                        "type": "string",
                        "minLength": 1,
                        "description": "Filled quantity"
                      },
                      "filled_avg_price": {
                        "type": "string",
                        "description": "Filled average price",
                        "nullable": true
                      },
                      "order_class": {
                        "type": "string",
                        "enum": [
                          "simple",
                          "bracket",
                          "oco",
                          "oto",
                          "mleg",
                          ""
                        ],
                        "example": "bracket",
                        "description": "The order classes supported by Alpaca vary based on the order's security type. The following provides a comprehensive breakdown of the supported order classes for each category:\n  - Equity trading: simple (or \"\"), oco, oto, bracket.\n  - Options trading:\n    - simple (or \"\")\n    - mleg (required for multi-leg complex option strategies)\n  - Crypto trading: simple (or \"\").",
                        "title": "OrderClass",
                        "x-readme-ref-name": "OrderClass"
                      },
                      "order_type": {
                        "type": "string",
                        "deprecated": true,
                        "description": "Deprecated in favour of the field \"type\" "
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
                        "description": "The order types supported by Alpaca vary based on the order's security type. The following provides a comprehensive breakdown of the supported order types for each category:\n - Equity trading: market, limit, stop, stop_limit, trailing_stop.\n - Options trading: market, limit.\n - Multileg Options trading: market, limit.\n - Crypto trading: market, limit, stop_limit.",
                        "title": "OrderType",
                        "x-readme-ref-name": "OrderType"
                      },
                      "side": {
                        "type": "string",
                        "enum": [
                          "buy",
                          "sell"
                        ],
                        "example": "buy",
                        "title": "OrderSide",
                        "description": "Represents which side this order was on:\n- buy\n- sell\nRequired for all order classes except for mleg.",
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
                        "example": "day",
                        "x-readme-ref-name": "TimeInForce"
                      },
                      "limit_price": {
                        "type": "string",
                        "description": "Limit price",
                        "nullable": true
                      },
                      "stop_price": {
                        "description": "Stop price",
                        "type": "string",
                        "nullable": true
                      },
                      "status": {
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
                      },
                      "extended_hours": {
                        "type": "boolean",
                        "description": "If true, eligible for execution outside regular trading hours."
                      },
                      "legs": {
                        "type": "array",
                        "description": "When querying non-simple order_class orders in a nested style, an array of Order entities associated with this order. Otherwise, null. Required if order class is `mleg`.",
                        "nullable": true,
                        "items": {
                          "description": "This is copy of Order response schemas as a workaround of displaying issue of nested Order recursively for legs",
                          "type": "object",
                          "title": "Order",
                          "properties": {
                            "id": {
                              "type": "string",
                              "description": "Order ID"
                            },
                            "client_order_id": {
                              "type": "string",
                              "description": "Client unique order ID",
                              "maxLength": 128
                            },
                            "created_at": {
                              "type": "string",
                              "format": "date-time"
                            },
                            "updated_at": {
                              "type": "string",
                              "format": "date-time",
                              "nullable": true
                            },
                            "submitted_at": {
                              "type": "string",
                              "format": "date-time",
                              "nullable": true
                            },
                            "filled_at": {
                              "type": "string",
                              "format": "date-time",
                              "nullable": true
                            },
                            "expired_at": {
                              "type": "string",
                              "format": "date-time",
                              "nullable": true
                            },
                            "canceled_at": {
                              "type": "string",
                              "format": "date-time",
                              "nullable": true
                            },
                            "failed_at": {
                              "type": "string",
                              "format": "date-time",
                              "nullable": true
                            },
                            "replaced_at": {
                              "type": "string",
                              "format": "date-time",
                              "nullable": true
                            },
                            "replaced_by": {
                              "type": "string",
                              "format": "uuid",
                              "description": "The order ID that this order was replaced by",
                              "nullable": true
                            },
                            "replaces": {
                              "type": "string",
                              "format": "uuid",
                              "description": "The order ID that this order replaces",
                              "nullable": true
                            },
                            "asset_id": {
                              "type": "string",
                              "format": "uuid",
                              "description": "Asset ID (For options this represents the option contract ID)"
                            },
                            "symbol": {
                              "type": "string",
                              "minLength": 1,
                              "description": "Asset symbol"
                            },
                            "asset_class": {
                              "type": "string",
                              "title": "AssetClass",
                              "enum": [
                                "us_equity",
                                "us_option",
                                "crypto"
                              ],
                              "example": "us_equity",
                              "description": "This represents the category to which the asset belongs to. It serves to identify the nature of the financial instrument, with options including \"us_equity\" for U.S. equities, \"us_option\" for U.S. options, and \"crypto\" for cryptocurrencies.",
                              "x-examples": {
                                "example-1": "us_equity"
                              },
                              "x-readme-ref-name": "AssetClass"
                            },
                            "notional": {
                              "type": "string",
                              "minLength": 1,
                              "description": "Ordered notional amount. If entered, qty will be null. Can take up to 9 decimal points.",
                              "nullable": true
                            },
                            "qty": {
                              "type": "string",
                              "minLength": 1,
                              "description": "Ordered quantity. If entered, notional will be null. Can take up to 9 decimal points.",
                              "nullable": true
                            },
                            "filled_qty": {
                              "type": "string",
                              "minLength": 1,
                              "description": "Filled quantity"
                            },
                            "filled_avg_price": {
                              "type": "string",
                              "description": "Filled average price",
                              "nullable": true
                            },
                            "order_class": {
                              "type": "string",
                              "enum": [
                                "simple",
                                "bracket",
                                "oco",
                                "oto",
                                "mleg",
                                ""
                              ],
                              "example": "bracket",
                              "description": "The order classes supported by Alpaca vary based on the order's security type. The following provides a comprehensive breakdown of the supported order classes for each category:\n  - Equity trading: simple (or \"\"), oco, oto, bracket.\n  - Options trading:\n    - simple (or \"\")\n    - mleg (required for multi-leg complex option strategies)\n  - Crypto trading: simple (or \"\").",
                              "title": "OrderClass",
                              "x-readme-ref-name": "OrderClass"
                            },
                            "order_type": {
                              "type": "string",
                              "deprecated": true,
                              "description": "Deprecated in favour of the field \"type\" "
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
                              "description": "The order types supported by Alpaca vary based on the order's security type. The following provides a comprehensive breakdown of the supported order types for each category:\n - Equity trading: market, limit, stop, stop_limit, trailing_stop.\n - Options trading: market, limit.\n - Multileg Options trading: market, limit.\n - Crypto trading: market, limit, stop_limit.",
                              "title": "OrderType",
                              "x-readme-ref-name": "OrderType"
                            },
                            "side": {
                              "type": "string",
                              "enum": [
                                "buy",
                                "sell"
                              ],
                              "example": "buy",
                              "title": "OrderSide",
                              "description": "Represents which side this order was on:\n- buy\n- sell\nRequired for all order classes except for mleg.",
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
                              "example": "day",
                              "x-readme-ref-name": "TimeInForce"
                            },
                            "limit_price": {
                              "type": "string",
                              "description": "Limit price",
                              "nullable": true
                            },
                            "stop_price": {
                              "description": "Stop price",
                              "type": "string",
                              "nullable": true
                            },
                            "status": {
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
                            },
                            "extended_hours": {
                              "type": "boolean",
                              "description": "If true, eligible for execution outside regular trading hours."
                            },
                            "legs": {
                              "type": "array",
                              "description": "When querying non-simple order_class orders in a nested style, an array of Order entities associated with this order. Otherwise, null.",
                              "nullable": true
                            },
                            "trail_percent": {
                              "type": "string",
                              "description": "The percent value away from the high water mark for trailing stop orders.",
                              "nullable": true
                            },
                            "trail_price": {
                              "type": "string",
                              "description": "The dollar value away from the high water mark for trailing stop orders.",
                              "nullable": true
                            },
                            "hwm": {
                              "type": "string",
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
                            }
                          },
                          "required": [
                            "symbol",
                            "notional",
                            "qty",
                            "type",
                            "side",
                            "time_in_force"
                          ],
                          "x-readme-ref-name": "OrderLeg"
                        }
                      },
                      "trail_percent": {
                        "type": "string",
                        "description": "The percent value away from the high water mark for trailing stop orders.",
                        "nullable": true
                      },
                      "trail_price": {
                        "type": "string",
                        "description": "The dollar value away from the high water mark for trailing stop orders.",
                        "nullable": true
                      },
                      "hwm": {
                        "type": "string",
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
                      }
                    },
                    "required": [
                      "notional",
                      "type",
                      "time_in_force"
                    ],
                    "x-readme-ref-name": "Order"
                  }
                },
                "examples": {
                  "Equity": {
                    "value": {
                      "id": "7b08df51-c1ac-453c-99f9-323a5f075f0d",
                      "client_order_id": "5680c4bc-9ac1-4a12-a44c-df427ba53032",
                      "created_at": "2023-12-12T22:31:24.668464435Z",
                      "updated_at": "2023-12-12T22:31:24.668464435Z",
                      "submitted_at": "2023-12-12T22:31:24.577215743Z",
                      "filled_at": null,
                      "expired_at": null,
                      "canceled_at": null,
                      "failed_at": null,
                      "replaced_at": null,
                      "replaced_by": null,
                      "replaces": null,
                      "asset_id": "b0b6dd9d-8b9b-48a9-ba46-b9d54906e415",
                      "symbol": "AAPL",
                      "asset_class": "us_equity",
                      "notional": null,
                      "qty": "2",
                      "filled_qty": "0",
                      "filled_avg_price": null,
                      "order_class": "",
                      "order_type": "limit",
                      "type": "limit",
                      "side": "buy",
                      "time_in_force": "gtc",
                      "limit_price": "150",
                      "stop_price": null,
                      "status": "accepted",
                      "extended_hours": false,
                      "legs": null,
                      "trail_percent": null,
                      "trail_price": null,
                      "hwm": null,
                      "subtag": null,
                      "source": null
                    }
                  },
                  "Options": {
                    "value": {
                      "id": "30a077fa-96f6-4f20-a052-4b921ee2f243",
                      "client_order_id": "58cd43a7-029e-457e-b77f-cd4f61f00f2a",
                      "created_at": "2023-12-12T21:35:49.102449524Z",
                      "updated_at": "2023-12-12T21:35:49.102504673Z",
                      "submitted_at": "2023-12-12T21:35:49.056332248Z",
                      "filled_at": null,
                      "expired_at": null,
                      "canceled_at": null,
                      "failed_at": null,
                      "replaced_at": null,
                      "replaced_by": null,
                      "replaces": null,
                      "asset_id": "98359ef7-5124-49f3-85ea-5cf02df6defa",
                      "symbol": "AAPL250620C00100000",
                      "asset_class": "us_option",
                      "notional": null,
                      "qty": "2",
                      "filled_qty": "0",
                      "filled_avg_price": null,
                      "order_class": "simple",
                      "order_type": "limit",
                      "type": "limit",
                      "side": "buy",
                      "time_in_force": "day",
                      "limit_price": "10",
                      "stop_price": null,
                      "status": "pending_new",
                      "extended_hours": false,
                      "legs": null,
                      "trail_percent": null,
                      "trail_price": null,
                      "hwm": null,
                      "subtag": null,
                      "source": null
                    }
                  },
                  "Crypto": {
                    "value": {
                      "id": "38e482f3-79a8-4f75-a057-f07a1ec6a397",
                      "client_order_id": "5b5d3d67-06ad-4ffa-af65-a117d0fc5a59",
                      "created_at": "2023-12-12T22:36:51.337711497Z",
                      "updated_at": "2023-12-12T22:36:51.337754768Z",
                      "submitted_at": "2023-12-12T22:36:51.313261061Z",
                      "filled_at": null,
                      "expired_at": null,
                      "canceled_at": null,
                      "failed_at": null,
                      "replaced_at": null,
                      "replaced_by": null,
                      "replaces": null,
                      "asset_id": "a1733398-6acc-4e92-af24-0d0667f78713",
                      "symbol": "ETH/USD",
                      "asset_class": "crypto",
                      "notional": null,
                      "qty": "0.02",
                      "filled_qty": "0",
                      "filled_avg_price": null,
                      "order_class": "",
                      "order_type": "limit",
                      "type": "limit",
                      "side": "buy",
                      "time_in_force": "gtc",
                      "limit_price": "2100",
                      "stop_price": null,
                      "status": "pending_new",
                      "extended_hours": false,
                      "legs": null,
                      "trail_percent": null,
                      "trail_price": null,
                      "hwm": null,
                      "subtag": null,
                      "source": null
                    }
                  },
                  "MultilegOptions": {
                    "value": {
                      "id": "83f37e9f-6b1f-49ed-8fc6-3e6af716323f",
                      "client_order_id": "646b1fe6-b212-4f54-94c6-429e7bcdee04",
                      "created_at": "2024-12-10T16:15:53.677230742Z",
                      "updated_at": "2024-12-10T16:15:53.725139688Z",
                      "submitted_at": "2024-12-10T16:15:53.684952901Z",
                      "filled_at": "2024-12-10T16:15:53.694Z",
                      "expired_at": null,
                      "canceled_at": null,
                      "failed_at": null,
                      "replaced_at": null,
                      "replaced_by": null,
                      "replaces": null,
                      "asset_id": "",
                      "symbol": "",
                      "asset_class": "",
                      "notional": null,
                      "qty": "1",
                      "filled_qty": "1",
                      "filled_avg_price": "1.28",
                      "order_class": "mleg",
                      "order_type": "limit",
                      "type": "limit",
                      "side": "",
                      "time_in_force": "day",
                      "limit_price": "10",
                      "stop_price": null,
                      "status": "filled",
                      "extended_hours": false,
                      "legs": [
                        {
                          "id": "df4ff24a-c58a-4e37-8b9f-ef32b83a11f2",
                          "client_order_id": "cc8cc104-fe43-476c-b25c-f62650fb73f9",
                          "created_at": "2024-12-10T16:15:53.677230742Z",
                          "updated_at": "2024-12-10T16:15:53.725091158Z",
                          "submitted_at": "2024-12-10T16:15:53.684952901Z",
                          "filled_at": "2024-12-10T16:15:53.694Z",
                          "expired_at": null,
                          "canceled_at": null,
                          "failed_at": null,
                          "replaced_at": null,
                          "replaced_by": null,
                          "replaces": null,
                          "asset_id": "f0ea14b2-8a49-4e9b-89d1-894c6e518a76",
                          "symbol": "AAPL241213C00250000",
                          "asset_class": "us_option",
                          "notional": null,
                          "qty": "3",
                          "filled_qty": "3",
                          "filled_avg_price": "0.43",
                          "order_class": "mleg",
                          "order_type": "",
                          "type": "",
                          "side": "buy",
                          "position_intent": "buy_to_open",
                          "time_in_force": "day",
                          "limit_price": null,
                          "stop_price": null,
                          "status": "filled",
                          "extended_hours": false,
                          "legs": null,
                          "trail_percent": null,
                          "trail_price": null,
                          "hwm": null,
                          "subtag": null,
                          "source": null,
                          "expires_at": "2024-12-10T21:00:00Z",
                          "ratio_qty": "3"
                        },
                        {
                          "id": "ecd91110-c34d-4e9d-a7bf-a9c27c40f8b5",
                          "client_order_id": "0bd2d36d-4af2-4dfb-8418-333a5d5026fa",
                          "created_at": "2024-12-10T16:15:53.677230742Z",
                          "updated_at": "2024-12-10T16:15:53.708983759Z",
                          "submitted_at": "2024-12-10T16:15:53.684952901Z",
                          "filled_at": "2024-12-10T16:15:53.694Z",
                          "expired_at": null,
                          "canceled_at": null,
                          "failed_at": null,
                          "replaced_at": null,
                          "replaced_by": null,
                          "replaces": null,
                          "asset_id": "f89940db-eeb1-46e6-8f9b-bb1f27a0b395",
                          "symbol": "AAPL241213C00260000",
                          "asset_class": "us_option",
                          "notional": null,
                          "qty": "1",
                          "filled_qty": "1",
                          "filled_avg_price": "0.01",
                          "order_class": "mleg",
                          "order_type": "",
                          "type": "",
                          "side": "sell",
                          "position_intent": "sell_to_open",
                          "time_in_force": "day",
                          "limit_price": null,
                          "stop_price": null,
                          "status": "filled",
                          "extended_hours": false,
                          "legs": null,
                          "trail_percent": null,
                          "trail_price": null,
                          "hwm": null,
                          "subtag": null,
                          "source": null,
                          "expires_at": "2024-12-10T21:00:00Z",
                          "ratio_qty": "1"
                        }
                      ],
                      "trail_percent": null,
                      "trail_price": null,
                      "hwm": null,
                      "subtag": null,
                      "source": null
                    }
                  }
                }
              }
            }
          }
        },
        "operationId": "getAllOrders",
        "description": "Retrieves a list of orders for the account, filtered by the supplied query parameters.",
        "x-internal": false
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
