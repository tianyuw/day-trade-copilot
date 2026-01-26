---
source: https://docs.alpaca.markets/docs/historical-option-data
scraped_at_utc: 2026-01-26T01:04:10Z
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

Historical Option Data
This API provides historical market data for options. Check the API Reference for the detailed descriptions of all the endpoints.
🚧
Data availability
Currently we only offer historical option data since February 2024.

Data sources
Similarly to stocks, Alpaca offers two different data sources for options:
SourceDescriptionIndicativeIndicative Pricing Feed is a free derivative of the original OPRA feed: the quotes are not actual OPRA quotes, they’re just indicative derivatives. The trades are also derivatives and they’re delayed by 15 minutes.OPRA (Options Price Reporting Authority)OPRA is the consolidated BBO feed of OPRA. OPRA Plan defines the BBO as the highest bid and lowest offer for a series of options available in one or more of the options markets maintained by the parties. OPRA feed is only available to subscribed users.
Updated3 days ago
Historical Crypto DataHistorical News DataAsk AI
