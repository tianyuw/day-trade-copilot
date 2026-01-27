---
source: https://docs.alpaca.markets/docs/credential-management
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

Credentials Management
Authentication into the Broker API can be done through 2 different flows:

Client credentials (recommended)
Client Secret

Private Key JWT

Legacy flow

Both these flows offer access to expiration dates & fine-grained access control through BrokerDash.

User Permissions
All user roles can view the credentials management page and see the list of existing API keys. However, only superusers have the ability to create new API credentials. This permission structure ensures proper access control while maintaining visibility of existing credentials for all team members.

Credentials Expiration
To help enhance the security of your account and integration, all generated credentials can be assigned a specific expiration timeframe. This feature is a critical security control that automatically deactivates a key after a set period, limiting the risk associated with a key being compromised or forgotten.

The following options are available:

Never

1 week

30 days

90 days

6 months

1 year

Custom - select your own expiration date

Fine-grained access control
When generating new API credentials, you have the option to define granular permissions using Access Controls. This feature is designed to enhance the security of your integration, while also allowing you to ensure a key only has the access required to perform its designated function.

You can choose from three distinct access control levels:

Read only: Grants permission to view data across all API scopes.

Full access: Grants permission to view and modify data across all API scopes.

Custom: Grants fine-grained, specific permissions for each API scope individually.

Custom Access Controls
Instead of granting universal Read only or Full access, you can specify the access level for each distinct API scope.

For each API scope you can assign one of the following access levels:

Read & Write: Grants full permission to both view and modify data within that scope.

Read only: Grants permission to view data only.

No Access: Completely blocks all endpoints within that scope for this key.

You can choose one of the three custom access level for the following scopes:

Accounts

Funding

Admin

Crypto

Rebalancing

Trading

Journaling

Data

Reporting

SSE events

Updated4 days ago
Getting Started with Broker APIUse CasesAsk AI
