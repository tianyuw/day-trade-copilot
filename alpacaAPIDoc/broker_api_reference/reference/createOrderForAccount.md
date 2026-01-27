---
source_view: https://docs.alpaca.markets/reference/createorderforaccount
source_md: https://docs.alpaca.markets/reference/createorderforaccount.md
scraped_at_utc: 2026-01-27T04:30:48Z
---
# Create an Order for an Account

Creating an order for your end customer. Each trading request must pass in the account_id in the URL.

- Note that when submitting crypto orders, `market`, `limit` and `stop_limit` orders are supported while the supported `time_in_force` values are `gtc`, and `ioc`.
- For equities and crypto we accept fractional orders as well with either `notional` or `qty` provided.
- Note that submitting an options order is only available for partners who have been enabled for Options BETA.
- In case of Fixed Income, only `market` and `limit` order types with `day` `time_in_force` are supported, and order replacement is not supported.
Note that submitting Fixed Income orders is only available for partners who have been enabled for Fixed Income.

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
    "/v1/trading/accounts/{account_id}/orders": {
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
      "post": {
        "summary": "Create an Order for an Account",
        "tags": [
          "Trading"
        ],
        "description": "Creating an order for your end customer. Each trading request must pass in the account_id in the URL.\n\n- Note that when submitting crypto orders, `market`, `limit` and `stop_limit` orders are supported while the supported `time_in_force` values are `gtc`, and `ioc`.\n- For equities and crypto we accept fractional orders as well with either `notional` or `qty` provided.\n- Note that submitting an options order is only available for partners who have been enabled for Options BETA.\n- In case of Fixed Income, only `market` and `limit` order types with `day` `time_in_force` are supported, and order replacement is not supported.\nNote that submitting Fixed Income orders is only available for partners who have been enabled for Fixed Income.",
        "requestBody": {
          "required": true,
          "content": {
            "application/json": {
              "schema": {
                "type": "object",
                "x-stoplight": {
                  "id": "d27prln6qqj0i"
                },
                "properties": {
                  "symbol": {
                    "type": "string",
                    "example": "AAPL",
                    "description": "Symbol or asset ID to identify the asset to trade. Required for all order classes except for `mleg`."
                  },
                  "qty": {
                    "type": "string",
                    "format": "decimal",
                    "example": "4.124",
                    "description": "- For equities, the number of shares to trade. Can be fractionable for only market and day order types.\n- Required for `mleg` order class, represents the number of units to trade of this strategy.\n- For Fixed Income securities, qty represents the order size in par value (face value).\nFor example, to place an order for 1 bond with a face value of $1,000, provide a qty of 1000.\n"
                  },
                  "notional": {
                    "type": "string",
                    "format": "decimal",
                    "example": "3",
                    "description": "Dollar amount to trade. Cannot work with qty. Only market and limit orders supported with time_in_force = day; Only limit orders for extended hours."
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
                    "description": "Required if type is `limit` or `stop_limit`.\n- In case of `mleg`, the limit_price parameter is expressed with the following notation:\n  - A positive value indicates a debit, representing a cost or payment to be made.\n  - A negative value signifies a credit, reflecting an amount to be received.\n- In case of Fied Income, the price is expressed in percentage of par value (face value).\nPrice is always clean price, meaning it does not include accrued interest."
                  },
                  "stop_price": {
                    "type": "string",
                    "format": "decimal",
                    "example": "3.14",
                    "description": "Required if type is stop or stop_limit"
                  },
                  "trail_price": {
                    "type": "string",
                    "format": "decimal",
                    "example": "3.14",
                    "description": "If type is trailing_stop, then one of trail_price or trail_percent is required"
                  },
                  "trail_percent": {
                    "type": "string",
                    "format": "decimal",
                    "example": "5.0",
                    "description": "If type is trailing_stop, then one of trail_price or trail_percent is required"
                  },
                  "extended_hours": {
                    "type": "boolean",
                    "example": false,
                    "description": "Defaults to false. If true, order will be eligible to execute in premarket/afterhours. Only works with type limit and time_in_force = day."
                  },
                  "client_order_id": {
                    "type": "string",
                    "example": "eb9e2aaa-f71a-4f51-b5b4-52a6c565dad4",
                    "description": "A unique identifier for the order. Automatically generated if not sent. (<= 128 characters)",
                    "maxLength": 128
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
                  "legs": {
                    "type": "array",
                    "description": "list of order legs (<= 4)",
                    "items": {
                      "description": "Represents an individual leg of a multileg options order.",
                      "type": "object",
                      "title": "MLegOrderLeg",
                      "properties": {
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
                        "symbol": {
                          "type": "string",
                          "description": "symbol or asset ID to identify the asset to trade"
                        },
                        "ratio_qty": {
                          "type": "string",
                          "example": "1",
                          "description": "proportional quantity of this leg in relation to the overall multileg order qty"
                        }
                      },
                      "required": [
                        "symbol",
                        "ratio_qty"
                      ],
                      "x-readme-ref-name": "MLegOrderLeg"
                    },
                    "maxLength": 4
                  },
                  "take_profit": {
                    "type": "object",
                    "description": "Takes in a string/number value for limit_price",
                    "properties": {
                      "limit_price": {
                        "type": "string",
                        "format": "decimal",
                        "example": "3.14"
                      }
                    }
                  },
                  "stop_loss": {
                    "description": "Takes in a string/number values for stop_price and limit_price",
                    "type": "object",
                    "properties": {
                      "stop_price": {
                        "type": "string",
                        "format": "decimal",
                        "example": "3.14"
                      },
                      "limit_price": {
                        "type": "string",
                        "format": "decimal",
                        "example": "3.14"
                      }
                    }
                  },
                  "commission": {
                    "type": "string",
                    "format": "decimal",
                    "example": "1.0",
                    "description": "The commission you want to collect from the user."
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
                  "source": {
                    "type": "string",
                    "x-stoplight": {
                      "id": "6lusmwaj5fmzf"
                    }
                  },
                  "instructions": {
                    "type": "string",
                    "x-stoplight": {
                      "id": "8jlb3tz44l3tl"
                    }
                  },
                  "subtag": {
                    "type": "string",
                    "x-stoplight": {
                      "id": "zajfuuduk4uss"
                    }
                  },
                  "swap_fee_bps": {
                    "type": "string",
                    "x-stoplight": {
                      "id": "hs4bv5gu00jjh"
                    },
                    "format": "decimal"
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
                  "type",
                  "time_in_force"
                ],
                "x-readme-ref-name": "CreateOrderRequest"
              },
              "examples": {
                "Equity": {
                  "summary": "Buy an equity stock",
                  "value": {
                    "symbol": "AAPL",
                    "qty": "2",
                    "side": "buy",
                    "type": "limit",
                    "limit_price": "150",
                    "time_in_force": "gtc"
                  }
                },
                "Options": {
                  "summary": "Buy an option contract (BETA)",
                  "value": {
                    "symbol": "AAPL250620C00100000",
                    "qty": "2",
                    "side": "buy",
                    "type": "limit",
                    "limit_price": "10",
                    "time_in_force": "day"
                  }
                },
                "Crypto": {
                  "summary": "Buy a crypto coin",
                  "value": {
                    "symbol": "ETH/USD",
                    "qty": "0.02",
                    "side": "buy",
                    "type": "limit",
                    "limit_price": "2100",
                    "time_in_force": "gtc"
                  }
                },
                "FixedIncome": {
                  "summary": "Buy a US Treasury Bill",
                  "value": {
                    "symbol": "US912797QN08",
                    "qty": "5000",
                    "side": "buy",
                    "type": "limit",
                    "limit_price": "99.15",
                    "time_in_force": "day"
                  }
                }
              }
            }
          }
        },
        "responses": {
          "200": {
            "description": "OK",
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
            "description": "Request is forbidden",
            "content": {
              "application/json": {
                "schema": {
                  "type": "string"
                }
              }
            }
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
          },
          "422": {
            "description": "Some parameters are not valid"
          }
        },
        "operationId": "createOrderForAccount"
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
