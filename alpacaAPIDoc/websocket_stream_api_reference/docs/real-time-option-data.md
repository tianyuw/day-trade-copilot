---
source: https://docs.alpaca.markets/docs/real-time-option-data
scraped_at_utc: 2026-01-26T01:09:58Z
---
Introduction
Welcome

About Alpaca

Alpaca API Platform

Authentication

SDKs and Tools

Additional Resources

BROKER API
About Broker API

Getting Started with Broker API

Credentials Management

Use Cases

Integration Setup with Alpaca

Broker API FAQs
Mandatory Corporate Actions

Voluntary Corporate Actions

FDIC Sweep Program

Instant Funding

Fully Paid Securities Lending

24/5 Trading

OmniSub

Fixed Income

Customer Account Opening
Accounts Statuses

International Accounts

Domestic (USA) Accounts

Data Validations

IRA Accounts Overview

Crypto Trading
Crypto Wallets API

Funding Accounts
Journals API

Funding Wallets

ACH Funding

Instant Funding

Trading

Portfolio Rebalancing

SSE Events
Account Status Events for KYCaaS

Daily Processes and Reconcilations
Banking Holiday Funding Processes

Statements and Confirms

Local Currency Trading (LCT)

Example Trading App (Ribbit)

Options Trading Overview

Fixed Income

Tokenization Guide for Issuer

Tokenization Guide for Authorized Participant

Custodial accounts

TRADING API
About Trading API

Getting Started with Trading API
Working with /account

Working with /assets

Working with /orders

Working with /positions

Paper Trading

Trading Account

Crypto Spot Trading
Crypto Orders

Crypto Pricing Data

Crypto Spot Trading Fees

Options Trading
Options Orders

Options Level 3 Trading

Non-Trade Activities for Option Events

Account Activities

Fractional Trading

Margin and Short Selling

Placing Orders

DMA Gateway / Advanced Order Types

User Protection

Websocket Streaming

Trading API FAQs
Position Average Entry Price Calculation

Regulatory Fees

Alpaca MCP Server

Market Data API
About Market Data API

Getting Started with Market Data API

Historical API
Historical Stock Data

Historical Crypto Data

Historical Option Data

Historical News Data

WebSocket Stream
Real-time Stock Data

Real-time Crypto Data

Real-time News

Real-time Option Data

Market Data FAQ

Connect API
About Connect API

Registering Your App

Using OAuth2 and Trading API

FIX API
About FIX API
FIX Specification

Real-time Option Data
This API provides option market data on a websocket stream. This helps receive the most up to date market information that could help your trading strategy to act upon certain market movements. If you wish to access the latest pricing data, using the stream provides much better accuracy and performance than polling the latest historical endpoints.

You can find the general description of the real-time WebSocket Stream here. This page focuses on the option stream.

URL
The URL for the option stream is

wss://stream.data.alpaca.markets/v1beta1/{feed}
Sandbox URL:

wss://stream.data.sandbox.alpaca.markets/v1beta1/{feed}
Substitute
indicative or
opra for
{feed} depending on your subscription. The capabilities and differences for the
indicative and
opra subscriptions can be found [here].

Any attempt to access a data feed not available for your subscription will result in an error during authentication.

Message format🚧
Msgpack
Unlike the stock and crypto stream, the option stream is only available in msgpack format. The SDKs are using this format automatically. For readability, the examples in the rest of this documentation will still be in json format (because msgpack is binary encoded).

Channels
Trades
SchemaAttributeTypeNotes
Tstringmessage type, always “t”
Sstringsymbol
tstringRFC-3339 formatted timestamp with nanosecond precision
pnumbertrade price
sinttrade size
xstringexchange code where the trade occurred
cstringtrade condition
ExampleJSON

{
 "T": "t",
 "S": "AAPL240315C00172500",
 "t": "2024-03-11T13:35:35.13312256Z",
 "p": 2.84,
 "s": 1,
 "x": "N",
 "c": "S"
}
Quotes
SchemaAttributeTypeNotes
Tstringmessage type, always “q”
Sstringsymbol
tstringRFC-3339 formatted timestamp with nanosecond precision
bxstringbid exchange code
bpnumberbid price
bsintbid size
axstringask exchange code
apnumberask price
asintask size
cstringquote condition
ExampleJSON

{
 "T": "q",
 "S": "SPXW240327P04925000",
 "t": "2024-03-12T11:59:38.897261568Z",
 "bx": "C",
 "bp": 9.46,
 "bs": 53,
 "ax": "C",
 "ap": 9.66,
 "as": 38,
 "c": "A"
}
Errors
Other than the general stream errors, you may receive these option-specific errors during your session:
Error MessageDescription
[{"T":"error","code":412,"msg":"option messages are only available in MsgPack format"}]Use the
Content-Type: application/msgpack header.
[{"T":"error","code":413,"msg":"star subscription is not allowed for option quotes"}]You cannot subscribe to
* for option quotes (there are simply too many of them).
Updated3 days ago
Real-time NewsMarket Data FAQAsk AI
