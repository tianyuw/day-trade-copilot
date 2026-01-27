---
source: https://docs.alpaca.markets/docs/daily-processes-and-reconcilations
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

Daily Processes and Reconcilations
Daily Processes
There are a few daily timings you want to keep in mind when you think about the operation. Note that these schedules follow daylight savings time.
ProcessTimingNotesBeginning-of-day Sync (BOD)02:15AM-02:30AM ESTTrading accounts are updated with the previous day end-of-day values. Trade confirms are also synchronized around this time.Incoming wire processing08:00AM-08:30AM ESTThe incoming wires with FFC instructions are bookedOutgoing wire cutoff04:00PM ESTThe outgoing wire requests before the cutoff will be processed for the day.ACH cutoff02:00PM ESTThe credit/debit of ACH requests before the cutoff will be processed for the day.Trade reporting06:30PM-07:30PM ESTThe day’s trades are finalized and reported.End-of-day calculation (EOD)11:00PM-11:30PM ESTClose the day’s book, mark to market positions, cost basis calculation, margin requirements calculation etc.
Mandatory Corporate Actions
Currently the corporate actions are processed a semi-automated way, and you will see such records in Activity API as they happen. We are working to provide upfront information separately in the future.

Dividends
Dividends are the most common corporate actions. The cash is paid (credited) to the customer accounts after the pay date, as we receive the cash from DTC. Please note that the actual credit transactions may be after the pay date if we don’t receive the cash from DTC. When such payout is transacted, you will see the account activity in Activity API as the DIV entry type.

Dividends are income gain. If your end customers are non-US residents, 30% withholding is applied by default. In case you claim to apply different rates for the tax treaty, please contact us.

Dividends are processed without waiting for DTC in the sandbox environment. This may not reflect the live side operation.

Forward Splits and Reverse Splits
Share splits are processed as they happen and the beginning-of-day process will update the positions of the customer accounts. Both appear as a SPLIT entry type in the activity. In the case of reverse splits, there might be the cash in lieu for non-divisible shares which will not be processed immediately until we receive the cash from DTC.

Symbol/CUSIP Change and Listing/Delisting
The symbol or CUSIP can change one day for a particular asset. The asset master data is refreshed on a daily basis and we do recommend you retrieve the asset endpoint every morning before the market open (or after the beginning-of-day timing). While Alpaca does not currently participate in the initial public offering, such stock on the IPO day will become tradable on the day it is listed, and start filling orders once the secondary market opens.

Other Events
Mergers, acquisitions, and other type events are processed manually in our back office as they are rare and each case is often unique. Please contact Alpaca’s broker-dealer operation team if you have any questions.

ACATS
Alpaca processes both sending and receiving ACATS requests. As of today, you can request our operation team for the receiving request, but we plan to provide this service as an API in the future.

Monthly Processes
Monthly statement emails should be sent for the prior month on or before the 10th of the following month - for example, for the monthly statement for August, delivery via email must be on or prior to September 10.

Updated4 days ago
Account Status Events for KYCaaSBanking Holiday Funding ProcessesAsk AI
