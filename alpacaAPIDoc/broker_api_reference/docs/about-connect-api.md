---
source: https://docs.alpaca.markets/docs/about-connect-api
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

About Connect API
Develop applications on Alpaca’s platform using OAuth2. Let 4M+ users with an Alpaca brokerage account connect to your app.

Develop applications on Alpaca’s platform using OAuth2. Alpaca’s OAuth allows you to seamlessly integrate financial markets into your application and expand your audience to the over 100K brokerage accounts on Alpaca’s platform.

Read Register Your App to learn how you can register your app. In addition, you can visit OAuth Integration Guide to learn more about using OAuth to connect your applications with Alpaca.

Broker Partners
Broker partners are able to create their own OAuth service. Allow your end users to use OAuth apps like TradingView through your Broker API application. Learn more about OAuth with Broker API in the Broker API reference

Terms of Access and Use
You must read the terms and register in order to connect and use Alpaca’s APIs

All API clients must authenticate with OAuth 2.0

You may not imply that the app was developed by Alpaca.

If you are building a commercial application that makes money (including ads, in-app purchases, etc), you must disclose it in the registration form and receive written approval.

To allow live trading for other users, the app needs to be approved by Alpaca. Please contact [email protected].

Live trading is allowed for the app developer user without approval.
❗️
This is not an offer, solicitation of an offer, or advice to open a brokerage account.
Disclosure can be found here

FAQs
Q: What can an OAuth app do?
A: OAuth allows you to manage your end-user’s Alpaca brokerage account on their behalf. This means you can create many types of financial services including automated investing, portfolio analytics and much more.

Q: Should I use OAuth or Broker API?
A: OAuth allows you to expand your audience to users with Alpaca brokerage accounts. On the otherhand, Broker API allows you to build an application fully within your environment. Users sign up for a brokerage account under your application. If you want to create your own brokerage, automated investment app, or any app where you want to own your users, use the Broker API. If you want to build your trading service on Alpaca’s platform, use OAuth.

Q: How secure is OAuth?
A: OAuth2 itself is very secure. However you must make sure to follow good practices in how you handle tokens. Make sure to never publicly expose your client secret and access tokens.

Q: How to get OAuth App live?
A: You will need to register your app in the OAuth apps section of the dashboard. Learn more about Register Your App.

Q: I’m developing an app/service targeting non-US users. Can we integrate with Alpaca’s OAuth API?
A: Alpaca’s platform supports brokerage accounts for international users. When you build an app on OAuth, all users on Alpaca’s platform will be able to use your service, including international users.

Updated4 days ago
Market Data FAQRegistering Your AppAsk AI
