---
source_view: https://docs.alpaca.markets/reference/closeallpositionsforaccount
source_md: https://docs.alpaca.markets/reference/closeallpositionsforaccount.md
scraped_at_utc: 2026-01-27T04:30:48Z
---
# Close All Positions for an Account

Closes (liquidates) all of the account’s open long and short positions. A response will be provided for each order that is attempted to be cancelled. If an order is no longer cancelable, the server will respond with status 500 and reject the request.

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
    "/v1/trading/accounts/{account_id}/positions": {
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
        }
      ],
      "delete": {
        "summary": "Close All Positions for an Account",
        "operationId": "closeAllPositionsForAccount",
        "responses": {
          "207": {
            "description": "HTTP 207 Multi-Status with body; an array of objects that include the order id and http status code for each status request.",
            "content": {
              "application/json": {
                "schema": {
                  "type": "array",
                  "items": {
                    "title": "PositionClosedResponse",
                    "type": "object",
                    "description": "Represents the result of asking the api to close a position.\n\n`body` is the Order used to close out the position.",
                    "x-examples": {
                      "example-1": {
                        "symbol": "AAPL",
                        "status": 200,
                        "body": {
                          "id": "f7f25e89-939a-4587-aaf6-414a6b3c341d",
                          "client_order_id": "52f8574c-96d5-49b6-94c1-2570a268434e",
                          "created_at": "2022-02-04T16:53:29.53427917Z",
                          "updated_at": "2022-02-04T16:53:29.53427917Z",
                          "submitted_at": "2022-02-04T16:53:29.533738219Z",
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
                          "order_type": "market",
                          "type": "market",
                          "side": "sell",
                          "time_in_force": "day",
                          "limit_price": null,
                          "stop_price": null,
                          "status": "accepted",
                          "extended_hours": false,
                          "legs": null,
                          "trail_percent": null,
                          "trail_price": null,
                          "hwm": null,
                          "commision": "1.0"
                        }
                      }
                    },
                    "properties": {
                      "symbol": {
                        "type": "string",
                        "description": "Symbol name of the asset"
                      },
                      "status": {
                        "type": "integer",
                        "description": "Http status code for the attempt to close this position"
                      },
                      "body": {
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
                    },
                    "required": [
                      "symbol",
                      "status"
                    ],
                    "x-stoplight": {
                      "id": "86zc8o19d0xih"
                    },
                    "x-readme-ref-name": "PositionClosedResponse"
                  }
                },
                "examples": {
                  "example-1": {
                    "value": [
                      {
                        "symbol": "TSLA",
                        "status": 200,
                        "body": {
                          "id": "d1143025-89fc-4952-8936-db2409d899f3",
                          "client_order_id": "17dbfab4-cb86-4e0a-8fa6-f0606b0a9a4e",
                          "created_at": "2022-05-13T16:25:29.336330998Z",
                          "updated_at": "2022-05-13T16:25:29.336330998Z",
                          "submitted_at": "2022-05-13T16:25:29.335776073Z",
                          "filled_at": null,
                          "expired_at": null,
                          "canceled_at": null,
                          "failed_at": null,
                          "replaced_at": null,
                          "replaced_by": null,
                          "replaces": null,
                          "asset_id": "a4778bc8-fad1-47b7-87fe-d5cde10d43f4",
                          "symbol": "TSLA",
                          "asset_class": "us_equity",
                          "notional": null,
                          "qty": "4",
                          "filled_qty": "0",
                          "filled_avg_price": null,
                          "order_class": "",
                          "order_type": "market",
                          "type": "market",
                          "side": "sell",
                          "time_in_force": "day",
                          "limit_price": null,
                          "stop_price": null,
                          "status": "accepted",
                          "extended_hours": false,
                          "legs": null,
                          "trail_percent": null,
                          "trail_price": null,
                          "hwm": null,
                          "source": null
                        }
                      }
                    ]
                  }
                }
              }
            }
          },
          "500": {
            "description": "Failed to liquidate some positions"
          }
        },
        "description": "Closes (liquidates) all of the account’s open long and short positions. A response will be provided for each order that is attempted to be cancelled. If an order is no longer cancelable, the server will respond with status 500 and reject the request.",
        "parameters": [
          {
            "schema": {
              "type": "boolean"
            },
            "in": "query",
            "name": "cancel_orders",
            "description": "If true is specified, cancel all open orders before liquidating all positions."
          }
        ],
        "tags": [
          "Trading"
        ]
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
