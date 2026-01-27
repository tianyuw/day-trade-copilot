---
source: https://docs.alpaca.markets/docs/account-opening
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

Customer Account Opening
If you are a fully-disclosed broker-dealer, an RIA, or a trading app setup, you can open your end customer’s account using Account API. The POST method allows you to submit all KYC information to Alpaca. There are slight differences between setups. #

Trading/Investing App and RIA
In this use case, Alpaca is responsible for the account approval step, while you can own the user experiences for collecting the end-customer information. We require you to collect a set of the information required for our approval process.

Upon the POST request, the account status starts from
SUBMITTED status. Alpaca system will run the automatic KYC process asynchronously and update the KYC result as the account status. You can receive such updates in the Event API stream.

If all KYC information is verified without problems, the account status will be
APPROVED and shortly transition to
ACTIVE. In some cases, if the final approval is pending, the account status becomes
APPROVAL_PENDING which will transition to
APPROVED once it is approved. In the case of some action is required, the status becomes
ACTION_REQUIRED and you will receive the reason for this. In most cases, you will need to collect additional information from the end user. One example would be that the residential address is not verified, so a copy of a document such as a utility bill needs to be uploaded. You can use Document API to upload additional documents when requested.

Fully-Disclosed Broker-Dealer
As a reminder, in this setup, you are required to have a proper broker-dealer license in your local jurisdiction and you are the broker on the record. Alpaca relies on your KYC process to open customers' accounts which you will send via the CIP API.

In this case, as soon as a
POST request is made and all fields are validated, we will first screen the account against our internal list of blacklisted accounts and an exact, or similar, match against this list will result in the account moving to either
REJECTED or
APPROVAL_PENDING. If there is no match then the account status starts from
APPROVED status, meaning you have approved the account opening. Therefore, you need to complete your KYC for the account before making the
POST request.

Omnibus Broker-Dealer
In an omnibus setup, you will not request any new account opening. Your trading accounts will be set up by Alpaca when the go-live is approved. That said, you may want to simulate this structure using Account API and you can open as many accounts as you want in the sandbox environment even if you are an omnibus.

Account Type
Alpaca currently opens all accounts as margin accounts. We support individual taxable accounts and business accounts. Other types of accounts such as cash and IRA accounts are on our roadmap.

Even though all accounts at Alpaca are margin accounts, you have the ability to set accounts to be cash accounts (100% buying power) to disable margin trading for your users through account configurations here.

Updated4 days ago
Fixed IncomeAccounts StatusesAsk AI
