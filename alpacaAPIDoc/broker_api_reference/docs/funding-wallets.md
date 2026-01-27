---
source: https://docs.alpaca.markets/docs/funding-wallets
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

Funding Wallets
Funding Wallets for Broker API allows you to create a dedicated wallet with a distinct account number for each user to deposit funds into.

Deposit Flow
If funding wallet has not yet been created, create a funding wallet

Retrieve funding wallet details

Retrieve funding details for the funding wallet

Create a deposit request
In sandbox, this can be simulated via this endpoint

In production, customer initiates a deposit from the external bank to the funding details from #3

Check the status of transfers

Withdrawal Flow
If recipient bank has not yet been created, create a recipient bank
Do note that depending on the country and beneficiary, the required fields might differ.

Retrieve recipient bank details

Create a withdrawal request

Check the status of transfers

Statuses and Descriptions
The table below details the possible statuses and their descriptions. Transfers cannot be canceled, and
complete,
rejected,
failed are terminal statuses.
StatusDescriptionPendingThe transfer is pending to be processed.ExecutedThe transfer has been sent to the bank.CompleteThe transfer has been settled and the balances have been updated for the accounts involved in the transaction.RejectedThe transfer has been rejected by the bank, this is usually due to invalid input.FailedThe transfer has failed, this is usually due to bank errors.
You can read more in this blog post and our FAQs.

FAQ
See full list of FAQs for Funding Wallets here.

What local currencies are supported?

The list can be found here. For these local currencies, you can send a swift wire in that local currency for it to be converted to USD. You can also withdraw in these local currencies via a swift wire.

What regions are supported for local rail deposits?

The list can be found here. For these regions, local transfers can be converted to USD.

What regions are supported for local rail withdrawals?

The list can be found here. For these regions, USD can be converted to local currency and paid out locally.

What regions are supported for deposits to Funding Wallets?

The list can be found here. For these regions, we can support deposits via both local rails and swift wires. If a region is not listed here, that means that Currency Cloud (our partner) does not accept deposits from that region due to their own internal risk rating of that region.

Can I test the flow in sandbox?

Yes the end to end flow can be tested in sandbox using the demo deposit endpoint to mock receiving a push deposit in the sandbox environment. The only exception to note though is that testing the end to end flow in sandbox using local rails in the US is not currently supported. This is due to a limitation with Currencycloud that prevents us from fetching the local rail deposit instructions on a per account basis. This issue is only limited to the sandbox environment and the end to end flow is functional in the limited live and production environments.

Updated4 days ago
Journals APIACH FundingAsk AI
