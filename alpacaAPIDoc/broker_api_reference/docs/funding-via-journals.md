---
source: https://docs.alpaca.markets/docs/funding-via-journals
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

Journals API
Journals API allows you to move cash or securities from one account to another.

For more on creating and retrieving journals please check out our API reference section on journals.

The most common use case is cash pooling, a funding model where you can send bulk wires into your firm account and then move the money into each individual user account.

Cash pooling funds flow

There are two types of journals:

JNLC
Journal cash between accounts. You can simulate instant funding in both sandbox and production by journaling funds between your pre-funded sweep accounts and a user’s account.

You can only journal cash from a firm account to a user account and vice-versa but not from customer to customer.

JNLS
Journal securities between accounts. Reward your users upon signing up or referring others by journaling small quantities of shares into their portfolios.

You can only journal securities from a firm account to a user account and not vice-versa or customer-to-customer.

Journals Status
The most common status flow for journals is quite simple:

Upon creation, the journal will be created in a
queued state.

Then, the journal will be
sent_to_clearing meaning that the request has been submitted to our books and records system.

Lastly, if there are no issues the journal will be
executed, meaning that the cash or securities have been successfully moved into the receiving account.

Still, there are other cases in which the journal is
rejected,
refused or requires manual intervention from Alpaca's cashiering team.
StatusDescription
queuedThis is the initial status when the journal is still in the queue to be processed.
sent_to_clearingThe journal has been sent to be processed by Alpaca’s booking system.
executedThe journal has been completed and the balances have been updated for the accounts involved in the transaction. In some rare cases, journals can be reversed from this status by Alpaca's cashiering team if the transaction is not permitted.
pendingThe journal is pending to be processed as it requires manual approval from Alpaca operations, for example, this can be caused by hitting the journal limits.
rejectedThe journal has been manually rejected.
canceledThe journal has been canceled, either via an API request or by Alpaca's operations team.
refusedThe journal was never posted in Alpaca's ledger, probably because some of the preliminary checks failed. A common example would be a replayed request in close succession, where the first request is executed and the second request fails the balance check.
correctThe journal has been manually corrected. The previously executed journal is cancelled and a new journal with the correct amount is created.
deletedThe journal has been deleted from our ledger system.
Journal statuses flowchart

Updated4 days ago
Funding AccountsFunding WalletsAsk AI
