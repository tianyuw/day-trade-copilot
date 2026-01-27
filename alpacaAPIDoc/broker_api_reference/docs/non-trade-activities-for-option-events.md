---
source: https://docs.alpaca.markets/docs/non-trade-activities-for-option-events
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

Non-Trade Activities for Option Events
This page provides an overview of new NTAs for options-specific events

Option Exercise

[
 {
 "id": "20190801011955195::5f596936-6f23-4cef-bdf1-3806aae57dbf",
 "activity_type": "OPEXC",
 "date": "2023-07-21",
 "net_amount": "0",
 "description": "Option Exercise",
 "symbol": "AAPL230721C00150000",
 "qty": "-2",
 "status": "executed"
 },
 {
 "id": "20190801011955195::5f596936-6f23-4cef-bdf1-3806aae57dbf",
 "activity_type": "OPTRD",
 "date": "2023-07-21",
 "net_amount": "-30000",
 "description": "Option Trade",
 "symbol": "AAPL",
 "qty": "200",
 "price": "90",
 "status": "executed"
 }
]
The exercise event (OPEXC) is applicable to 2 contracts, and the corresponding trade (OPTRD) represents 200 of the underlying shares being purchased at a per-share amount of $150 (strike price).

Option Assignment

[
 {
 "id": "20190801011955195::5f596936-6f23-4cef-bdf1-3806aae57dbf",
 "activity_type": "OPASN",
 "date": "2023-07-01",
 "net_amount": "0",
 "description": "Option Assignment",
 "symbol": "AAPL230721C00150000",
 "qty": "2",
 "status": "executed"
 },
 {
 "activity_type": "OPTRD",
 "id": "20190801011955195::5f596936-6f23-4cef-bdf1-3806aae57dbf",
 "date": "2023-07-01",
 "net_amount": "30000",
 "description": "Option Trade",
 "symbol": "AAPL",
 "qty": "-200",
 "price": "150",
 "status": "executed"
 }
]
The assignment event (OPASN) is applicable to 2 contracts, and the corresponding trade (OPTRD) represents 200 of the underlying shares being sold at a per-share amount of $150 (strike price).

ITM Option Expiry
In the event of an in-the-money (ITM) option reaching expiration without being designated as "Do Not Exercise" (DNE), the Alpaca system will automatically initiate the exercise process on behalf of the user. This process mirrors the Exercise event described earlier. In cases where there is insufficient buying power or underlying positions to facilitate the exercise, the system will generate an automated order for the liquidation of the position.

OTM Option Expiry

[
 {
 "id": "20190801011955195::5f596936-6f23-4cef-bdf1-3806aae57dbf",
 "activity_type": "OPEXP",
 "date": "2023-07-21",
 "net_amount": "0",
 "description": "Option Expiry",
 "symbol": "AAPL230721C00150000",
 "qty": "-2",
 "status": "executed"
 }
]
When a contract expires OTM, the Alpaca system will flatten the position and no further action is taken.

Updated4 days ago
Options Level 3 TradingAccount ActivitiesAsk AI
