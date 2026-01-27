---
source: https://docs.alpaca.markets/docs/statements-and-confirms
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

Statements and Confirms
Requirements
Under the FINRA and SEC rules, Alpaca is required to ensure the customer statements and trade confirms are delivered correctly in time to the end customers. That being said, the actual communication and delivery do not have to be done by Alpaca directly. Very often, you want to own the full user experiences and to be responsible for these communications, which is totally possible.

Document API Integration
You can retrieve the generated reports in PDF format through the Documents API. You can store the files on your storage if it is required for your regulation purpose, or you can let your customers download the files using the URL returned in the API response. If you are a fully-disclosed broker-dealer, you can insert your firm logo, name and address in the PDF template. Please send those data to Alpaca.

If you need even more customization on the template, we are currently working on the new API endpoint which will return only the data points so that you can build fully-customized documents with your own template. Alpaca still needs to review your final version of customized documents before delivering to the end customers for the first time.

Updated4 days ago
Banking Holiday Funding ProcessesLocal Currency Trading (LCT)Ask AI
