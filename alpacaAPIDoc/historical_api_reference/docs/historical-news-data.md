---
source: https://docs.alpaca.markets/docs/historical-news-data
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

Historical News Data
This API provides historical news data dating back to 2015. You can expect to receive an average of 130+ news articles per day. All news data is currently provided directly by Benzinga. With a single endpoint, you can request news for both stocks and cryptocurrency tickers. Check the API Reference for the detailed descriptions the endpoint.

Use Cases
News API is a versatile tool that can be used to support a variety of use cases, such as building an app with the Broker API or Algorithmic Trading using Sentiment Analysis on News with the Trading API.

News Widgets

News API can be used to create visual news widgets for web and mobile apps. These widgets can be used to display the latest news for any stock or crypto symbol, and they include different sized images to give your app a visual appeal.

News Sentiment Analysis
News API can be used to train models that can determine the sentiment of a given headline or news content. This can be done by using historical data from News API to train the model on a variety of different sentiment labels.

Realtime Trading on News
Real-time news over WebSockets can be used to enable your trading algorithms to react to the latest news across any stock or cryptocurrency.

Updated3 days ago
Historical Option DataWebSocket StreamAsk AI
