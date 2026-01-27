---
source: https://docs.alpaca.markets/docs/about-broker-api
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

About Broker API
This is the documentation about Broker API that helps you build trading apps and brokerage services for your end users. If you are looking to build your own trading bots and algos, read the Trading API documentation. With Alpaca Broker API, you can build the full brokerage experiences for your end users around account opening, funding and trading. This document describes all you need to know to build your trading app.

Broker API Use Cases
There are several different use cases for Broker API integration. Below are some common ones, but please do not hesitate to reach out to our sales team if you have a different case in mind. We want our platform to encourage a broad range of use cases.

Broker dealer (fully-disclosed, omnibus)

Registered Investment Advisor (RIA)

We support most use cases internationally.

Depending on the case, the API methods you want to use could vary. For example, the omnibus broker-dealer case never uses API to open a customer account since the trading accounts are created upfront and you will submit orders to them, and manage your end customer accounting on your end. More details on each use case are described in the following sections.

Updated4 days ago
Additional ResourcesGetting Started with Broker APIAsk AI
