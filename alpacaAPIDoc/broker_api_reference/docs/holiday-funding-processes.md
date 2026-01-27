---
source: https://docs.alpaca.markets/docs/holiday-funding-processes
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

Banking Holiday Funding Processes
This section addresses operational procedures for scenarios where the bank is closed for a holiday, but the stock market remains open for trading (e.g., Columbus Day, Veterans Day).

Funding & JIT

Bank Holiday but Markets Trading: The stock market will be open and trading as usual, but banks will be closed for the federal holiday.

JIT Operations Continue as Normal: Our Just-in-Time (JIT) funding operations will continue to run without interruption.

Still Reconcile and Send Reports: Partners should continue to reconcile trades and send required reports on time for both the preceding trading day and the market open holiday.

Partners Should Treat as Two Separate Normal Trading Days: Both the preceding trading day and the market open holiday trading sessions should be processed as distinct, regular trading days.

Settlement Due for Holiday & Next Business Day: Settlement Amount is Required by 1:00 PM EST business day after the bank holiday for Payment.

Two Separate Wires on the First Business Day After a Holiday: Partners should anticipate two distinct wire transfers on the morning of the first business day following a holiday — one representing the settlement from the prior business day and the other for the settlement on the holiday itself.

Implementing Safety Measures to Prevent Amount Errors: Our Engineering team have enhanced safety measures and checks to ensure accuracy and prevent any amount errors related to the dual-day settlement.

Instant Funding
Code Fixed to Base on Trade Settlement vs. Bank Holidays: Our Instant Funding logic has been fixed to prioritize the trade settlement schedule over bank holidays, ensuring more consistent processing.

Partners Need Settlement Amount by 1 PM ET: Partners must provide the necessary settlement amount by 1:00 PM ET on the bank holiday to ensure Instant Funding is processed for payment on the next bank business day.

RF Account Option for Instant Settlement During Holidays: Partners can utilize the RF account option for instant settlement of funds during bank holiday periods.

Partners Can Pre-Fund to Avoid Limit Issues: We encourage partners to pre-fund their accounts ahead of long weekends or holidays where applicable to avoid hitting pre-set funding limits.

Funds Processing
Currency Cloud Transactions May Still Post: Funds sent using Currency Cloud may still post to your account on a bank holiday, provided the transaction does not pass through a US bank for final processing.

Wire Transfers and ACH Will Not Be Processed: All standard US-based Wire Transfers and ACH transactions will be paused and will not be processed on the bank holiday. Processing will resume on the next bank business day.

Updated4 days ago
Daily Processes and ReconcilationsStatements and ConfirmsAsk AI
