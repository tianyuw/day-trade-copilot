---
source_view: https://docs.alpaca.markets/reference/subscribetotradev2sse
source_md: https://docs.alpaca.markets/reference/subscribetotradev2sse.md
scraped_at_utc: 2026-01-27T04:30:48Z
---
# Subscribe to Trade Events (SSE)

The Events API provides event push as well as historical queries via SSE (server sent events).

You can listen to events related to trade updates. Most market trades sent during market hours are filled instantly; you can listen to limit order updates through this endpoint.

Historical events are streamed immediately if queried, and updates are pushed as events occur.

Query Params Rules:
- `since` required if `until` specified
- `since_id` required if `until_id` specified
- `since` and `since_id` can’t be used at the same time
Behavior:
- if `since` or `since_id` not specified this will not return any historic data
- if `until` or `until_id` reached stream will end (status 200)

---

Note for people using the clients generated from this OAS spec. Currently OAS-3 doesn't have full support for representing SSE style responses from an API, so if you are using a generated client and don't specify a `since` and `until` there is a good chance the generated clients will hang waiting for the response to end.

If you require the streaming capabilities we recommend not using the generated clients for this specific usecase until the OAS-3 standards come to a consensus on how to represent this correctly in OAS-3.

---

**Legacy trade events API**

**Deprecation notice**

As part of the deprecation process,
the legacy trade events API is now only available for existing broker-partners at: `GET /v1/events/trades` only for compatibility reasons.

All new broker partners will not have the option for the legacy trade event endpoint.

All new broker partners will have to integrate with the new `/v2/events/trades` endpoint.

Also, all existing broker partners are now recommended to upgrade to the `/v2/events/trades` endpoint, which provides faster event delivery times.

The legacy trade events api works the same way as the new one with the exception of the event_id which is an integer except of an ULID. This results in the request’s since_id and until_id are also being integers. This integer is monotonically increasing over time for events.

Please note that the new `/v2` endpoint, is the same as, and was originally available under `/v2beta1`.
We encourage all customers to adjust their codebase from that interim beta endpoint to the `/v2` stable endpoint.
In the near future we will setup permanent redirect from `/v2beta1` to `/v2` before we completely remove the beta endpoint.

---

###  Comment messages
According to the SSE specification, any line that starts with a colon is a comment which does not contain data.  It is typically a free text that does not follow any data schema. A few examples mentioned below for comment messages.

#####  Slow client

The server sends a comment when the client is not consuming messages fast enough. Example: `: you are reading too slowly, dropped 10000 messages`

##### Internal server error

An error message is sent as a comment when the server closes the connection on an internal server error (only sent by the v2 and v2beta1 endpoints). Example: `: internal server error`

---

**Common events**

These are the events that are the expected results of actions you may have taken by sending API requests.

The meaning of the timestamp field changes for each type; the meanings have been specified here for which types the timestamp field will be present.

- `accepted` Sent when an order recieved and accepted by Alpaca
- `pending_new` Sent when the order has been received by Alpaca and routed to the exchanges, but has not yet been accepted for execution.
- `new` Sent when an order has been routed to exchanges for execution.
- `fill` Sent when your order has been completely filled.
  - timestamp: The time at which the order was filled.
- `partial_fill` Sent when a number of shares less than the total remaining quantity on your order has been filled.
  - timestamp: The time at which the shares were filled.
- `canceled` Sent when your requested cancellation of an order is processed.
  - timestamp: The time at which the order was canceled.
- `expired` Sent when an order has reached the end of its lifespan, as determined by the order's time in force value.
  - timestamp: The time at which the order expired.
- `done_for_day` Sent when the order is done executing for the day, and will not receive further updates until the next trading day.
- `replaced` Sent when your requested replacement of an order is processed.
  - timestamp: The time at which the order was replaced.

**Rarer events**

These are events that may rarely be sent due to unexpected circumstances on the exchanges. It is unlikely you will need to design your code around them, but you may still wish to account for the possibility that they will occur.

- `rejected` Sent when your order has been rejected.
  - timestamp: The time at which the rejection occurred.
- `held` For multi-leg orders, the secondary orders (stop loss, take profit) will enter this state while waiting to be triggered.
- `stopped` Sent when your order has been stopped, and a trade is guaranteed for the order, usually at a stated price or better, but has not yet occurred.
- `pending_cancel` Sent when the order is awaiting cancellation. Most cancellations will occur without the order entering this state.
- `pending_replace` Sent when the order is awaiting replacement.
- `calculated` Sent when the order has been completed for the day - it is either filled or done_for_day - but remaining settlement calculations are still pending.
- `suspended` Sent when the order has been suspended and is not eligible for trading.
- `order_replace_rejected` Sent when the order replace has been rejected.
- `order_cancel_rejected` Sent when the order cancel has been rejected.
- `trade_bust`: Sent when a previously reported execution has been canceled (“busted”) by the upstream exchange.
- `trade_correct`: Sent when a previously reported trade has been corrected. For example, the exchange may have updated the price, quantity, or another execution parameter after the trade was initially reported.
- `restated`: Sent when the order is manually modified.

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
    },
    {
      "name": "Events"
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
    "/v2/events/trades": {
      "get": {
        "summary": "Subscribe to Trade Events (SSE)",
        "tags": [
          "Events",
          "Trading"
        ],
        "responses": {
          "200": {
            "description": "Connected. Events will now start streaming as long as you keep the connection open.",
            "content": {
              "text/event-stream": {
                "schema": {
                  "type": "array",
                  "items": {
                    "description": "Represents an update to an order/trade, sent over the events streaming api.",
                    "type": "object",
                    "title": "TradeUpdateEvent",
                    "properties": {
                      "account_id": {
                        "type": "string",
                        "minLength": 1,
                        "description": "Account UUID",
                        "format": "uuid"
                      },
                      "at": {
                        "type": "string",
                        "minLength": 1,
                        "description": "Timestamp of event",
                        "format": "date-time"
                      },
                      "event": {
                        "type": "string",
                        "description": "**Common events**\n\nThese are the events that are the expected results of actions you may have taken by sending API requests.\n\nThe meaning of the `timestamp` field changes for each type; the meanings have been specified here for which types the\ntimestamp field will be present.\n\n- `new`: Sent when an order has been routed to exchanges for execution.\n- `fill`: Sent when your order has been completely filled.\n  - `timestamp`: The time at which the order was filled.\n- `partial_fill`: Sent when a number of shares less than the total remaining quantity on your order has been filled.\n  - `timestamp`: The time at which the shares were filled.\n- `canceled`: Sent when your requested cancellation of an order is processed.\n  - `timestamp`: The time at which the order was canceled.\n- `expired`: Sent when an order has reached the end of its lifespan, as determined by the order’s time in force value.\n  - `timestamp`: The time at which the order expired.\n- `done_for_day`: Sent when the order is done executing for the day, and will not receive further updates until the next trading day.\n- `replaced`: Sent when your requested replacement of an order is processed.\n  - `timestamp`: The time at which the order was replaced.\n\n**Rarer events**\n\nThese are events that may rarely be sent due to unexpected circumstances on the exchanges. It is unlikely you will need to design your code around them, but you may still wish to account for the possibility that they will occur.\n\n- `rejected`: Sent when your order has been rejected.\n  - `timestamp`: The time at which the rejection occurred.\n- `pending_new`: Sent when the order has been received by Alpaca and routed to the exchanges, but has not yet been accepted for execution.\n- `stopped`: Sent when your order has been stopped, and a trade is guaranteed for the order, usually at a stated price or better, but has not yet occurred.\n- `pending_cancel`: Sent when the order is awaiting cancellation. Most cancellations will occur without the order entering this state.\n- `pending_replace`: Sent when the order is awaiting replacement.\n- `calculated`: Sent when the order has been completed for the day - it is either `filled` or `done_for_day` - but remaining settlement calculations are still pending.\n- `suspended`: Sent when the order has been suspended and is not eligible for trading.\n- `order_replace_rejected`: Sent when the order replace has been rejected.\n- `order_cancel_rejected`: Sent when the order cancel has been rejected.\n- `trade_bust`: Sent when a previously reported execution has been canceled (“busted”) by the upstream exchange.\n- `trade_correct`: Sent when a previously reported trade has been corrected. For example, the exchange may have updated the price, quantity, or another execution parameter after the trade was initially reported.\n- `restated`: Sent when the order is manually modified.\n",
                        "enum": [
                          "new",
                          "fill",
                          "partial_fill",
                          "canceled",
                          "expired",
                          "done_for_day",
                          "replaced",
                          "rejected",
                          "pending_new",
                          "stopped",
                          "pending_cancel",
                          "pending_replace",
                          "calculated",
                          "suspended",
                          "order_replace_rejected",
                          "order_cancel_rejected",
                          "trade_bust",
                          "trade_correct"
                        ],
                        "x-stoplight": {
                          "id": "hsatty9b5tgrf"
                        },
                        "x-readme-ref-name": "TradeUpdateEventType"
                      },
                      "event_id": {
                        "type": "string",
                        "format": "ulid",
                        "description": "lexically sortable, monotonically increasing character array"
                      },
                      "execution_id": {
                        "type": "string",
                        "description": "Corresponding execution of an order. If an order gets filled over two executions (a partial_fill for example), you will receive two events with different IDs.\nNot present for `MultilegOptions`\n",
                        "format": "uui"
                      },
                      "previous_execution_id": {
                        "type": "string",
                        "description": "ID of the original execution that was busted or corrected (present only in trade_bust and trade_correct events).",
                        "format": "uuid"
                      },
                      "order": {
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
                      "timestamp": {
                        "type": "string",
                        "description": "Has various different meanings depending on the value of `event`, please see the [Trading Events](https://alpaca.markets/docs/api-references/broker-api/events/#trade-events)\nEnum in the documentation or the TradeUpdateEventType model for more details on when it means different things.\n",
                        "format": "date-time"
                      },
                      "price": {
                        "type": "string",
                        "description": "Only present when event is either `fill` or `partial_fill`. The average price per share at which the order was filled."
                      },
                      "swap_rate": {
                        "type": "string",
                        "description": "Only present for `local currency trading account` or `crypto asset trade` when event is either `fill` or `partial_fill`. The swap rate at which the current trade was filled."
                      },
                      "position_qty": {
                        "type": "string",
                        "description": "Only present when event is either `fill` or `partial_fill` other than `MultilegOptions`. The size of your total position, after this fill event, in shares. Positive for long positions, negative for short positions.\n"
                      },
                      "position_qtys": {
                        "type": "string",
                        "description": "Only present when event is either `fill` or `partial_fill` for `MultilegOptions`. The size of your total position, after this fill event, in shares. Positive for long positions, negative for short positions.\n"
                      },
                      "qty": {
                        "type": "string",
                        "description": "Only present when event is either `fill`, `partial_fill`, `trade_bust` and `trade_correct`. The amount of shares this Trade order was for. <br /> For `trade_bust` events, the qty field may be negative, representing a reversal of the original quantity."
                      },
                      "legs": {
                        "type": "array",
                        "description": "Only present when event is for `MultilegOptions`. Represents filled qty/price of legs.\n",
                        "items": {
                          "description": "Represents filled qty/price of legs.",
                          "type": "object",
                          "title": "TradeUpdateEventV2Leg",
                          "properties": {
                            "qty": {
                              "type": "string",
                              "description": "The amount of shares filled for this event"
                            },
                            "price": {
                              "type": "string",
                              "description": "The average price per share for this event."
                            },
                            "symbol": {
                              "type": "string",
                              "description": "Symbol of an asset"
                            },
                            "order_id": {
                              "type": "string",
                              "minLength": 1,
                              "description": "Order UUID",
                              "format": "uuid"
                            },
                            "timestamp": {
                              "type": "string",
                              "description": "Timestamp of this event leg\n",
                              "format": "date-time"
                            },
                            "execution_id": {
                              "type": "string",
                              "description": "Corresponding execution of an order. If an order gets filled over two executions (a partial_fill for example), you will receive two events with different IDs.",
                              "format": "uuid"
                            }
                          },
                          "x-readme-ref-name": "TradeUpdateEventV2Leg"
                        }
                      }
                    },
                    "x-readme-ref-name": "TradeUpdateEventV2"
                  }
                },
                "examples": {
                  "new": {
                    "value": {
                      "account_id": "529248ad-c4cc-4a50-bea4-6bfd2953f83a",
                      "at": "2022-04-19T14:12:30.656741Z",
                      "event": "new",
                      "event_id": "01G112NTT0XAXKDZK3AABK68TH",
                      "execution_id": "7e544af3-3104-4e1a-8cbc-dab2624949ff",
                      "previous_execution_id": "aeb60660-412f-4537-8d1f-1101b3fc8f64",
                      "order": {
                        "asset_class": "us_equity",
                        "asset_id": "a4778bc8-fad1-47b7-87fe-d5cde10d43f4",
                        "cancel_requested_at": null,
                        "canceled_at": null,
                        "client_order_id": "6d873193-dac6-4f72-8e13-c57853a9339d",
                        "commission": "1",
                        "created_at": "2022-04-19T10:12:30.57117938-04:00",
                        "expired_at": null,
                        "extended_hours": false,
                        "failed_at": null,
                        "filled_at": null,
                        "filled_avg_price": null,
                        "filled_qty": "0",
                        "hwm": null,
                        "id": "edada91a-8b55-4916-a153-8c7a9817e708",
                        "legs": null,
                        "limit_price": "700",
                        "notional": null,
                        "order_class": "",
                        "order_type": "limit",
                        "qty": "4",
                        "replaced_at": null,
                        "replaced_by": null,
                        "replaces": null,
                        "side": "buy",
                        "position_intent": "buy_to_open",
                        "status": "new",
                        "stop_price": null,
                        "submitted_at": "2022-04-19T10:12:30.403135025-04:00",
                        "symbol": "TSLA",
                        "time_in_force": "day",
                        "trail_percent": null,
                        "trail_price": null,
                        "type": "limit",
                        "updated_at": "2022-04-19T10:12:30.609783218-04:00",
                        "expires_at": "2022-04-19T21:00:00Z"
                      },
                      "timestamp": "2022-04-19T14:12:30.602193534Z"
                    }
                  },
                  "MultilegOptions-fill": {
                    "value": {
                      "account_id": "529248ad-c4cc-4a50-bea4-6bfd2953f83a",
                      "at": "2025-01-14T16:05:51.872012Z",
                      "event_id": "01G112NTT0XAXKDZK3AABK68TH",
                      "qty": "1",
                      "legs": [
                        {
                          "qty": "1",
                          "price": "0.04",
                          "symbol": "AAPL250117P00200000",
                          "order_id": "8d58279f-7dc8-415f-8495-32f394935509",
                          "timestamp": "2025-01-14T16:05:51.867802561Z",
                          "execution_id": "ccf7d1dc-78e1-4eb5-92c6-5c86b2bcca8f"
                        },
                        {
                          "qty": "1",
                          "price": "0.03",
                          "symbol": "AAPL250117C00250000",
                          "order_id": "8b0e2cff-eace-4e6a-8810-cad42c63df59",
                          "timestamp": "2025-01-14T16:05:51.867813051Z",
                          "execution_id": "06f94555-6db7-4059-a4c4-0b993084ccd0"
                        }
                      ],
                      "event": "fill",
                      "order": {
                        "id": "8af45a94-0b35-4053-ad4e-716c6783fcc9",
                        "hwm": null,
                        "qty": "1",
                        "legs": [
                          {
                            "id": "8d58279f-7dc8-415f-8495-32f394935509",
                            "hwm": null,
                            "qty": "1",
                            "legs": null,
                            "side": "buy",
                            "position_intent": "buy_to_open",
                            "type": "",
                            "status": "filled",
                            "symbol": "AAPL250117P00200000",
                            "asset_id": "8d1ba989-d98b-4551-889f-4647c2e86e20",
                            "notional": null,
                            "replaces": null,
                            "failed_at": null,
                            "filled_at": "2025-01-14T16:05:51.867802561Z",
                            "ratio_qty": "1",
                            "created_at": "2025-01-14T16:05:51.79424769Z",
                            "expired_at": null,
                            "filled_qty": "1",
                            "order_type": "",
                            "stop_price": null,
                            "updated_at": "2025-01-14T16:05:51.869810922Z",
                            "asset_class": "us_option",
                            "canceled_at": null,
                            "limit_price": null,
                            "order_class": "mleg",
                            "replaced_at": null,
                            "replaced_by": null,
                            "trail_price": null,
                            "submitted_at": "2025-01-14T16:05:51.800245966Z",
                            "time_in_force": "day",
                            "trail_percent": null,
                            "extended_hours": false,
                            "client_order_id": "9c5ce763-bd6f-41eb-b1b1-ed2c0b99d268",
                            "filled_avg_price": "0.04",
                            "cancel_requested_at": null,
                            "expires_at": "2025-01-14T21:00:00Z"
                          },
                          {
                            "id": "8b0e2cff-eace-4e6a-8810-cad42c63df59",
                            "hwm": null,
                            "qty": "1",
                            "legs": null,
                            "side": "buy",
                            "position_intent": "buy_to_open",
                            "type": "",
                            "status": "filled",
                            "symbol": "AAPL250117C00250000",
                            "asset_id": "e9f8c9ba-de7c-4e51-9eef-629f4cb79049",
                            "notional": null,
                            "replaces": null,
                            "failed_at": null,
                            "filled_at": "2025-01-14T16:05:51.867813051Z",
                            "ratio_qty": "1",
                            "created_at": "2025-01-14T16:05:51.79424769Z",
                            "expired_at": null,
                            "filled_qty": "1",
                            "order_type": "",
                            "stop_price": null,
                            "updated_at": "2025-01-14T16:05:51.870879612Z",
                            "asset_class": "us_option",
                            "canceled_at": null,
                            "limit_price": null,
                            "order_class": "mleg",
                            "replaced_at": null,
                            "replaced_by": null,
                            "trail_price": null,
                            "submitted_at": "2025-01-14T16:05:51.802310606Z",
                            "time_in_force": "day",
                            "trail_percent": null,
                            "extended_hours": false,
                            "client_order_id": "9cda9826-8fd5-4c01-8ee1-30c5286e2387",
                            "filled_avg_price": "0.03",
                            "cancel_requested_at": null,
                            "expires_at": "2025-01-14T21:00:00Z"
                          }
                        ],
                        "side": "buy",
                        "position_intent": "",
                        "type": "limit",
                        "status": "filled",
                        "symbol": "",
                        "asset_id": "00000000-0000-0000-0000-000000000000",
                        "notional": null,
                        "replaces": null,
                        "failed_at": null,
                        "filled_at": "2025-01-14T16:05:51.867813051Z",
                        "created_at": "2025-01-14T16:05:51.79424769Z",
                        "expired_at": null,
                        "filled_qty": "1",
                        "order_type": "limit",
                        "stop_price": null,
                        "updated_at": "2025-01-14T16:05:51.870937762Z",
                        "asset_class": "",
                        "canceled_at": null,
                        "limit_price": "0.6",
                        "order_class": "mleg",
                        "replaced_at": null,
                        "replaced_by": null,
                        "trail_price": null,
                        "submitted_at": "2025-01-14T16:05:51.802310606Z",
                        "time_in_force": "day",
                        "trail_percent": null,
                        "extended_hours": false,
                        "client_order_id": "9d2f39de-adae-4dae-a67e-838bf21fb5ae",
                        "filled_avg_price": "0.07",
                        "cancel_requested_at": null
                      },
                      "price": "0.07",
                      "timestamp": "2025-01-14T16:05:51.867813051Z",
                      "position_qtys": {
                        "AAPL250117C00250000": "1",
                        "AAPL250117P00200000": "1"
                      }
                    }
                  }
                }
              }
            }
          }
        },
        "parameters": [
          {
            "name": "since",
            "in": "query",
            "schema": {
              "type": "string",
              "format": "date"
            },
            "description": "Format: YYYY-MM-DD"
          },
          {
            "name": "until",
            "in": "query",
            "schema": {
              "type": "string",
              "format": "date"
            },
            "description": "Format: YYYY-MM-DD"
          },
          {
            "name": "since_id",
            "in": "query",
            "schema": {
              "type": "string",
              "format": "ulid"
            }
          },
          {
            "name": "until_id",
            "in": "query",
            "schema": {
              "type": "string",
              "format": "ulid"
            }
          }
        ],
        "operationId": "subscribeToTradeV2SSE",
        "description": "The Events API provides event push as well as historical queries via SSE (server sent events).\n\nYou can listen to events related to trade updates. Most market trades sent during market hours are filled instantly; you can listen to limit order updates through this endpoint.\n\nHistorical events are streamed immediately if queried, and updates are pushed as events occur.\n\nQuery Params Rules:\n- `since` required if `until` specified\n- `since_id` required if `until_id` specified\n- `since` and `since_id` can’t be used at the same time\nBehavior:\n- if `since` or `since_id` not specified this will not return any historic data\n- if `until` or `until_id` reached stream will end (status 200)\n\n---\n\nNote for people using the clients generated from this OAS spec. Currently OAS-3 doesn't have full support for representing SSE style responses from an API, so if you are using a generated client and don't specify a `since` and `until` there is a good chance the generated clients will hang waiting for the response to end.\n\nIf you require the streaming capabilities we recommend not using the generated clients for this specific usecase until the OAS-3 standards come to a consensus on how to represent this correctly in OAS-3.\n\n---\n\n**Legacy trade events API**\n\n**Deprecation notice**\n\nAs part of the deprecation process,\nthe legacy trade events API is now only available for existing broker-partners at: `GET /v1/events/trades` only for compatibility reasons.\n\nAll new broker partners will not have the option for the legacy trade event endpoint.\n\nAll new broker partners will have to integrate with the new `/v2/events/trades` endpoint.\n\nAlso, all existing broker partners are now recommended to upgrade to the `/v2/events/trades` endpoint, which provides faster event delivery times.\n\nThe legacy trade events api works the same way as the new one with the exception of the event_id which is an integer except of an ULID. This results in the request’s since_id and until_id are also being integers. This integer is monotonically increasing over time for events.\n\nPlease note that the new `/v2` endpoint, is the same as, and was originally available under `/v2beta1`.\nWe encourage all customers to adjust their codebase from that interim beta endpoint to the `/v2` stable endpoint.\nIn the near future we will setup permanent redirect from `/v2beta1` to `/v2` before we completely remove the beta endpoint.\n\n---\n\n###  Comment messages\nAccording to the SSE specification, any line that starts with a colon is a comment which does not contain data.  It is typically a free text that does not follow any data schema. A few examples mentioned below for comment messages.\n\n#####  Slow client\n\nThe server sends a comment when the client is not consuming messages fast enough. Example: `: you are reading too slowly, dropped 10000 messages`\n\n##### Internal server error\n\nAn error message is sent as a comment when the server closes the connection on an internal server error (only sent by the v2 and v2beta1 endpoints). Example: `: internal server error`\n\n---\n\n**Common events**\n\nThese are the events that are the expected results of actions you may have taken by sending API requests.\n\nThe meaning of the timestamp field changes for each type; the meanings have been specified here for which types the timestamp field will be present.\n\n- `accepted` Sent when an order recieved and accepted by Alpaca\n- `pending_new` Sent when the order has been received by Alpaca and routed to the exchanges, but has not yet been accepted for execution.\n- `new` Sent when an order has been routed to exchanges for execution.\n- `fill` Sent when your order has been completely filled.\n  - timestamp: The time at which the order was filled.\n- `partial_fill` Sent when a number of shares less than the total remaining quantity on your order has been filled.\n  - timestamp: The time at which the shares were filled.\n- `canceled` Sent when your requested cancellation of an order is processed.\n  - timestamp: The time at which the order was canceled.\n- `expired` Sent when an order has reached the end of its lifespan, as determined by the order's time in force value.\n  - timestamp: The time at which the order expired.\n- `done_for_day` Sent when the order is done executing for the day, and will not receive further updates until the next trading day.\n- `replaced` Sent when your requested replacement of an order is processed.\n  - timestamp: The time at which the order was replaced.\n\n**Rarer events**\n\nThese are events that may rarely be sent due to unexpected circumstances on the exchanges. It is unlikely you will need to design your code around them, but you may still wish to account for the possibility that they will occur.\n\n- `rejected` Sent when your order has been rejected.\n  - timestamp: The time at which the rejection occurred.\n- `held` For multi-leg orders, the secondary orders (stop loss, take profit) will enter this state while waiting to be triggered.\n- `stopped` Sent when your order has been stopped, and a trade is guaranteed for the order, usually at a stated price or better, but has not yet occurred.\n- `pending_cancel` Sent when the order is awaiting cancellation. Most cancellations will occur without the order entering this state.\n- `pending_replace` Sent when the order is awaiting replacement.\n- `calculated` Sent when the order has been completed for the day - it is either filled or done_for_day - but remaining settlement calculations are still pending.\n- `suspended` Sent when the order has been suspended and is not eligible for trading.\n- `order_replace_rejected` Sent when the order replace has been rejected.\n- `order_cancel_rejected` Sent when the order cancel has been rejected.\n- `trade_bust`: Sent when a previously reported execution has been canceled (“busted”) by the upstream exchange.\n- `trade_correct`: Sent when a previously reported trade has been corrected. For example, the exchange may have updated the price, quantity, or another execution parameter after the trade was initially reported.\n- `restated`: Sent when the order is manually modified."
      },
      "parameters": []
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
