---
source: https://docs.alpaca.markets/docs/regulatory-fees
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

Regulatory Fees
FEE types and effective rates
The following FEEs are applied to options trades.
TypeWhenCharged ByTrading Activity Fee (TAF)Sells onlyFINRAOptions Regulatory Fee (ORF)Buys and sellsOptions ExchangesOptions Clearing CorporationBuys and sells up to 2750 contractsOCCConsolidated Audit Trail (CAT)Buys and sellsFINRA-CAT
The following FEEs are applied to equities.
TypeWhenCharged ByTrading Activity Fee (TAF)Sells onlyFINRAConsolidated Audit Trail (CAT)Buys and sellsFINRA-CAT
For our current effective rates, please refer to our brokerage fee schedule available here:
https://alpaca.markets/disclosures

How Fees are charged and reflected in account balances
Alpaca's trading system keeps track of the accrued FEE amounts intraday and deducts the pending amounts from account balances.

At EOD, we charge each account the fees for that trading day

We round up total fees based on the currency’s precision to the nearest decimal place.
For example, USD has a precision of 0.01. If the total fee is calculated as 0.00083, it will be rounded up to 0.01 (i.e., 1 penny).

Additional resources
https://www.finra.org/rules-guidance/rulebooks/industry/trading-activity-fee

https://www.catnmsplan.com/

https://www.sec.gov/newsroom/press-releases/2024-47

Updated4 days ago
Position Average Entry Price CalculationAlpaca MCP ServerAsk AI
