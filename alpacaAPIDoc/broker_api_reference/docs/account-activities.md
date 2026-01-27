---
source: https://docs.alpaca.markets/docs/account-activities
scraped_at_utc: 2026-01-27T04:30:48Z
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

Account Activities
The account activities API provides access to a historical record of transaction activities that have impacted your account.

The TradeActivity Object
Sample TradeActivityJSON

{
 "activity_type": "FILL",
 "cum_qty": "1",
 "id": "20190524113406977::8efc7b9a-8b2b-4000-9955-d36e7db0df74",
 "leaves_qty": "0",
 "price": "1.63",
 "qty": "1",
 "side": "buy",
 "symbol": "LPCN",
 "transaction_time": "2019-05-24T15:34:06.977Z",
 "order_id": "904837e3-3b76-47ec-b432-046db621571b",
 "type": "fill"
}
PropertiesAttributeTypeDescription
activity_typestringFor trade activities, this will always be
FILL
cum_qtystring<number>The cumulative quantity of shares involved in the execution.
idstringAn ID for the activity. Always in
:: format. Can be sent as
page_token in requests to facilitate the paging of results.
leaves_qtystring<number>For
partially_filled orders, the quantity of shares that are left to be filled.
pricestring<number>The per-share price that the trade was executed at.
qtystring<number>The number of shares involved in the trade execution.
sidestring
buy or
sell
symbolstringThe symbol of the security being traded.
transaction_timestring<timestamp>The time at which the execution occurred.
order_idstring<uuid>The id for the order that filled.
typestring
fill or
partial_fill
The NonTradeActivity (NTA) Object
Sample NTAJSON

{
 "activity_type": "DIV",
 "id": "20190801011955195::5f596936-6f23-4cef-bdf1-3806aae57dbf",
 "date": "2019-08-01",
 "net_amount": "1.02",
 "symbol": "T",
 "cusip": "C00206R102",
 "qty": "2",
 "per_share_amount": "0.51"
}
PropertiesAttributeTypeDescription
activity_typestringSee below for a list of possible values.
idstringAn ID for the activity. Always in
:: format. Can be sent as
page_token in requests to facilitate the paging of results.
datestring<timestamp>The date on which the activity occurred or on which the transaction associated with the activity settled.
net_amountstring<number>The net amount of money (positive or negative) associated with the activity.
symbolstringThe symbol of the security involved with the activity. Not present for all activity types.
cusipstringThe CUSIP of the security involved with the activity. Not present for all activity types.
qtystring<number>For dividend activities, the number of shares that contributed to the payment. Not present for other activity types.
per_share_amountstring<number>For dividend activities, the average amount paid per share. Not present for other activity types.
Pagination of Results
Pagination is handled using the
page_token and
page_size parameters.

page_token represents the ID of the end of your current page of results. If specified with a direction of desc, for example, the results will end before the activity with the specified ID. If specified with a direction of
asc, results will begin with the activity immediately after the one specified.
page_size is the maximum number of entries to return in the response. If
date is not specified, the default and maximum value is 100. If
date is specified, the default behavior is to return all results, and there is no maximum page size.

Activity Types
activity_typeDescription
FILLOrder fills (both partial and full fills)
TRANSCash transactions (both CSD and CSW)
MISCMiscellaneous or rarely used activity types (All types except those in TRANS, DIV, or FILL)
ACATCACATS IN/OUT (Cash)
ACATSACATS IN/OUT (Securities)
CFEECrypto fee
CSDCash deposit(+)
CSWCash withdrawal(-)
DIVDividends
DIVCGLDividend (capital gain long term)
DIVCGSDividend (capital gain short term)
DIVFEEDividend fee
DIVFTDividend adjusted (Foreign Tax Withheld)
DIVNRADividend adjusted (NRA Withheld)
DIVROCDividend return of capital
DIVTWDividend adjusted (Tefra Withheld)
DIVTXEXDividend (tax exempt)
FEEFee denominated in USD
INTInterest (credit/margin)
INTNRAInterest adjusted (NRA Withheld)
INTTWInterest adjusted (Tefra Withheld)
JNLJournal entry
JNLCJournal entry (cash)
JNLSJournal entry (stock)
MAMerger/Acquisition
NCName change
OPASNOption assignment
OPEXPOption expiration
OPXRCOption exercise
PTCPass Thru Charge
PTRPass Thru Rebate
REORGReorg CA
SCSymbol change
SSOStock spinoff
SSPStock split
Updated4 days ago
Non-Trade Activities for Option EventsFractional TradingAsk AI
