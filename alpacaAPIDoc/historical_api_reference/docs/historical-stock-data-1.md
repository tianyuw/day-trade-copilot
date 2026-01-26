---
source: https://docs.alpaca.markets/docs/historical-stock-data-1
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

Historical Stock Data
This API provides historical market data for equities. Check the API Reference for detailed descriptions of all endpoints.

Data Sources
Alpaca offers market data from various data sources described below. You can use the
feed parameter on all the stock endpoints to switch between them.

Source

Description

iex

IEX (The Investors Exchange) is ideal for initial app testing and situations where precise pricing may not be the primary focus. It's a single US exchange that accounts for approximately ~2.5% of the market volume.

ℹ️ This is the only feed that can be used without a subscription.

sip

This feed covers all US exchanges, originating directly from exchanges and is consolidated by the Securities Information Processors: UTP (Nasdaq) and CTA (NYSE). These SIPs play a crucial role in connecting various U.S. markets, processing and consolidating all bid/ask quotes and trades from multiple trading venues into a single, easily accessible data feed.

Our data delivery ensures ultra-low latency and high reliability, as the information is transmitted directly to Alpaca's bare metal servers located in New Jersey, situated alongside many market participants.

SIP data is particularly advantageous for developing your trading app, where precise and up-to-date price information is essential for traders and internal operations. It accounts for 100% of the market volume, providing comprehensive coverage for your trading needs.

boats

Blue Ocean ATS is the first alternative trading system to expand market hours, filling the gap to trade equities continuously throughout US evening hours.

overnight

Our "overnight" feed is Alpaca's derived feed from the original BOATS source. It offers a cheaper, but slightly less accurate alternative for overnight US market data. The trades are 15 minutes delayed and adjusted to fit the bid-ask spread.

Updated3 days ago
Historical APIHistorical Crypto DataAsk AI
