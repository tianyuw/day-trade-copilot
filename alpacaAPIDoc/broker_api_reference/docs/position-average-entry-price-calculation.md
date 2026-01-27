---
source: https://docs.alpaca.markets/docs/position-average-entry-price-calculation
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

Position Average Entry Price Calculation
How is the average entry price of a position is calculated?

Description
The average entry price and the cost basis of a position are returned in the
avg_entry_price and
cost_basis fields in the positions endpoints.
JSON

{
 "asset_id": "904837e3-3b76-47ec-b432-046db621571b",
 "symbol": "AAPL ",
 "exchange": "NASDAQ",
 "asset_class": "us_equity",
 "avg_entry_price": "100.0",
 "qty": "5",
 "qty_available": "4",
 "side": "long",
 "market_value": "600.0",
 "cost_basis": "500.0",
 "unrealized_pl": "100.0",
 "unrealized_plpc": "0.20",
 "unrealized_intraday_pl": "5.0",
 "unrealized_intraday_plpc": "0.0084",
 "current_price": "120.0",
 "lastday_price": "119.0",
 "change_today": "0.0084"
}
There are different methods that can be used to calculate the cost basis and the average entry price of a position such as
Strict FIFO,
Compressed FIFO,
Weighted Average, and others. Each method has its own rules for calculating the cost basis and average entry price after a sell transaction. This page aims to clarify which method is Alpaca using.

Which Method is Alpaca Using?
Weighted Average is used for intraday positions (positions from intraday trades)

Compressed FIFO is used for the end-of-day positions (positions from previous trading days)

Strict FIFO (First-In, First-Out)
Under the Strict FIFO method, the first position bought is the first position sold. Let's understand how it works:

The cost basis after the sell is calculated by deducting from the previous cost basis the price of the first open position multiplied by the sell quantity. In Strict FIFO, the sell quantity is covered using the first open position, however, if the first open position's quantity is not enough to cover the sell quantity, subsequent open positions are used.

Example:
Suppose we have the following transactions:

Day 1:

Buy 100 shares at $10 per share (Cost basis = $1,000)

Buy 50 shares at $12 per share (Cost basis = $600)

Day 2:

Buy 30 shares at $15 per share (Cost basis = $450)

Day 3:

Sell 120 shares

After the sell transaction:

Cost basis:
2050 - 100*10 - 20*12 =
$810

Average Entry Price:
cost_basis/qty_left =
810/60 =
$13.5

Compressed FIFO (First-In, First-Out)
The Compressed FIFO method follows similar rules to Strict FIFO, with one key difference. It compresses intraday positions using a weighted average. Let's see how it differs:

Example 1:
Using the same example from before:
Day 1:

Buy 100 shares at $10 per share (Cost basis = $1,000)

Buy 50 shares at $12 per share (Cost basis = $600)

Day 2:

Buy 30 shares at $15 per share (Cost basis = $450)

Day 3:

Sell 120 shares

After the sell transaction:

Cost Basis:
2050 - 120*(100*10 + 50*12)/150 =
$770

Average entry price:
cost_basis/qty_left =
770/60 =
$12.83

As you can see the positions in Day 1 were compressed into a total of 150 shares with an average price of
(100*10 + 50*12)/150.

Example 2
Day 1:

Buy 100 shares at $10 per share (Cost basis = $1,000)

Buy 50 shares at $9 per share (Cost basis = $450)

Sell 50 shares

Buy 50 shares at $11 per share (Cost basis = $550)

At the end of Day 1:

Cost Basis:
2000 - 50*(100*10 + 50*9 + 50*11)/200 =
$1,500

Average Entry Price:
1500/150 =
$10

Weighted Average
The Weighted Average method calculates the cost basis based on the weighted average price per share. Here's how it works:

On Sell: The cost basis for the sold quantity is calculated by deducting the sell quantity multiplied by the average entry price of all the opened positions that the account holds.

Example:
Using the same example from before:

Day 1:

Buy 100 shares at $10 per share (Cost basis = $1,000)

Buy 50 shares at $12 per share (Cost basis = $600)

Day 2:

Buy 30 shares at $15 per share (Cost basis = $450)

Day 3:

Sell 120 shares

After the sell the calculations based on the Weighted average method would be:

Cost Basis:
2050 - 120*(100*10 + 50*12 + 30*15)/180 =
$683.33

Average Entry Price:
cost_basis/qty_left =
683.33/60 =
$11.39

FAQ
Why did the
avg_entry_price and
cost_basis of a position change the next day?
As described in the Which method is Alpaca using? the calculation method for determining the
avg_entry_price and
cost_basis differs between the
intraday positions and the
end-of-day positions. Consequently, it is possible for the
avg_entry_price and
cost_basis fields of a position to change the day after the last trade has occurred. This change occurs when our beginning-of-day (BOD) job executes and synchronizes positions from our ledger. For details regarding the timing of the beginning-of-day (BOD) job, please refer to the Daily Processes and Reconciliations.

Updated4 days ago
Websocket StreamingRegulatory FeesAsk AI
