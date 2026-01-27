---
source: https://docs.alpaca.markets/docs/account-plans
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

Trading Account
Alpaca Brokerage Account (Live Trading)
After creating an Alpaca Paper Only Account, you can enable live trading by becoming an Alpaca Brokerage Account holder. This requires you to go through an account on-boarding process with Alpaca Securities LLC, a FINRA member and SEC registered broker-dealer. We now support brokerage accounts for individuals and business entities from around the world.

With a brokerage account, you will be able to fully utilize Alpaca for your automated trading and investing needs. Using the Alpaca API, you’ll be able to buy and sell stocks in your brokerage account, and you’ll receive real-time consolidated market data. In addition, you will continue to be able to test your strategies and simulate your trades in our paper trading environment. And with the Alpaca web dashboard, it’s easy to monitor both your paper trading and your real money brokerage account. All accounts are opened as margin accounts. Accounts with $2,000 or more equity will have access to margin trading and short selling.

Individuals
Alpaca Securities LLC supports individual taxable brokerage accounts. At this time, we do not support retirement accounts.

Businesses/Incorporated Entities
You can open a business trading account to use Alpaca for trading purposes, but not for building apps/services.
👀
Alpaca currently accepts entities that are Corporations, LLCs and Partnerships in the U.S., and around the world. There is a $30,000 minimum deposit required for opening a business account at Alpaca.
Markets Supported
Currently, Alpaca only supports trading of listed U.S. stocks and select cryptocurrencies.

The Account Object
The account API serves important information related to an account, including account status, funds available for trade, funds available for withdrawal, and various flags relevant to an account’s ability to trade.

An account maybe be blocked for just for trades (
trading_blocked flag) or for both trades and transfers (
account_blocked flag) if Alpaca identifies the account to be engaging in any suspicious activity. Also, in accordance with FINRA’s pattern day trading rule, an account may be flagged for pattern day trading (
pattern_day_trader flag), which would inhibit an account from placing any further day-trades.

Please note that cryptocurrencies are not eligible assets to be used as collateral for margin accounts and will require the asset be traded using cash only.

Sample ObjectJSON

{
 "account_blocked": false,
 "account_number": "010203ABCD",
 "buying_power": "262113.632",
 "cash": "-23140.2",
 "created_at": "2019-06-12T22:47:07.99658Z",
 "currency": "USD",
 "crypto_status": "ACTIVE",
 "non_marginable_buying_power": "7386.56",
 "accrued_fees": "0",
 "pending_transfer_in": "0",
 "pending_transfer_out": "0",
 "daytrade_count": "0",
 "daytrading_buying_power": "262113.632",
 "equity": "103820.56",
 "id": "e6fe16f3-64a4-4921-8928-cadf02f92f98",
 "initial_margin": "63480.38",
 "last_equity": "103529.24",
 "last_maintenance_margin": "38000.832",
 "long_market_value": "126960.76",
 "maintenance_margin": "38088.228",
 "multiplier": "4",
 "pattern_day_trader": false,
 "portfolio_value": "103820.56",
 "regt_buying_power": "80680.36",
 "short_market_value": "0",
 "shorting_enabled": true,
 "sma": "0",
 "status": "ACTIVE",
 "trade_suspended_by_user": false,
 "trading_blocked": false,
 "transfers_blocked": false
}
Account Properties
Attribute

Type

Description

id

string
<uuid>

Account ID.

account_number

string

Account number.

status

string<account_status>

See detailed account statuses below

crypto_status

string<account_status>

The current status of the crypto enablement. See detailed crypto statuses below.

currency

string

"USD"

cash

string
<number>

Cash balance

portfolio_value

string
<number>

lpaca Broker* Total value of cash + holding positions (Equivalent to the equity field)

non_marginable_buying_power

string
<number>

Current available non-margin dollar buying power

accrued_fees

string
<number>

The fees collected.

pending_transfer_in

string
<number>

Cash pending transfer in.

pending_transfer_out

string
<number>

Cash pending transfer out

pattern_day_trader

boolean

Whether or not the account has been flagged as a pattern day trader

trade_suspended_by_user

boolean

User setting. If
true, the account is not allowed to place orders.

trading_blocked

boolean

If
true, the account is not allowed to place orders.

transfers_blocked

boolean

If
true, the account is not allowed to request money transfers.

account_blocked

boolean

If
true, the account activity by user is prohibited.

created_at

string
<timestamp>

Timestamp this account was created at

shorting_enabled

boolean

Flag to denote whether or not the account is permitted to short

long_market_value

string
<number>

Real-time MtM value of all long positions held in the account

short_market_value

string
<number>

Real-time MtM value of all short positions held in the account

equity

string
<number>

cash +
long_market_value +
short_market_value

last_equity

string
<number>

Equity as of previous trading day at 16:00:00 ET

multiplier

string
<number>

Buying power (BP) multiplier that represents account margin classification

Valid values:

1 (standard limited margin account with 1x BP),

2 (reg T margin account with 2x intraday and overnight BP; this is the default for all non-PDT accounts with $2,000 or more equity),

4 (PDT account with 4x intraday BP and 2x reg T overnight BP)

buying_power

string
<number>

Current available $ buying power; If multiplier = 4, this is your daytrade buying power which is calculated as (last_equity - (last) maintenance_margin)_ 4; If multiplier = 2, buying_power = max(equity – initial_margin,0)_ 2; If multiplier = 1, buying_power = cash

initial_margin

string
<number>

Reg T initial margin requirement (continuously updated value)

maintenance_margin

string
<number>

Maintenance margin requirement (continuously updated value)

sma

string
<number>

Value of special memorandum account (will be used at a later date to provide additional buying_power)

daytrade_count

int

The current number of daytrades that have been made in the last 5 trading days (inclusive of today)

last_maintenance_margin

string
<number>

Your maintenance margin requirement on the previous trading day

daytrading_buying_power

string
<number>

Your buying power for day trades (continuously updated value)

regt_buying_power

string
<number>

Your buying power under Regulation T (your excess equity - equity minus margin value - times your margin multiplier)

Account Status ENUMS
The following are the possible account status values. Most likely, the account status is
ACTIVE unless there is an issue. The account status may get to
ACCOUNT_UPDATED when personal information is being updated from the dashboard, in which case you may not be allowed trading for a short period of time until the change is approved.
statusdescription
ONBOARDINGThe account is onboarding.
SUBMISSION_FAILEDThe account application submission failed for some reason.
SUBMITTEDThe account application has been submitted for review.
ACCOUNT_UPDATEDThe account information is being updated.
APPROVAL_PENDINGThe final account approval is pending.
ACTIVEThe account is active for trading.
REJECTEDThe account application has been rejected.
Updated4 days ago
Paper TradingCrypto Spot TradingAsk AI
