---
source: https://docs.alpaca.markets/docs/alpaca-elite-smart-router
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

DMA Gateway / Advanced Order Types
Take Control of Your Trades with Direct Market Access Gateway and Advanced Order Types

Elite Smart Router
Elite Smart Router is designed to meet the needs of institutional clients and experienced algorithmic traders. A wide array of advanced investing and trading strategies are supported with higher API limits and cost-effective pricing.

One year after launching Alpaca Elite, we are expanding the feature set of the Elite Smart Router. The two key additions are Direct Market Access (DMA) Gateway* and Advanced Order Types. Direct Market Access Gateway* (DMA Gateway) gives you direct control of where your orders are sent. This, along with advanced order types like Volume-Weighted Average Price (VWAP) and Time-Weighted Average Price (TWAP), enables you to efficiently manage large orders, control execution costs, help minimize market impact, and meet your specific trading objectives. DMA Gateway, VWAP, and TWAP can only be accessed if users are on the Elite Smart Router as part of the Alpaca Elite Program.

*Direct Market Access Gateway is provided solely by DASH Financial Technologies ("DASH"), a member of the listed exchanges. Alpaca enables customers to route orders to the selected exchange through DASH’s DMA capabilities.

DMA Gateway
DMA Gateway is a tool that gives you customization over where your trades are sent.

Benefits:

Efficiently manage large orders

Execution customization

Help minimize market impact

Meet your specific trading objectives

Implementation
DMA orders are configured using
advanced_instructions in your order request payload:
SubmitCancel

curl --request POST \
 --url $APIDOMAIN/v2/orders \
 --header 'accept: application/json' \
 --header 'content-type: application/json' \
 --header "Apca-Api-Key-Id: $APIKEY" \
 --header "Apca-Api-Secret-Key: $SECRET" \
 --data '
{
 "side": "buy",
 "symbol": "AAPL",
 "type": "limit",
 "qty": "100",
 "time_in_force": "day",
 "limit_price": "212",
 "order_class": "simple",
 "advanced_instructions": {
 "algorithm": "DMA",
 "destination": "NYSE",
 "display_qty": "100"
 }
}' | jq -r

curl --request DELETE \
 --url $APIDOMAIN/v2/orders/<your_order_id> \
 --header 'accept: application/json' \
 --header "Apca-Api-Key-Id: $APIKEY" \
 --header "Apca-Api-Secret-Key: $SECRET" \

ParametersParameterRequiredDescriptionValues
algorithmmandatoryMust be set to "DMA" for Direct Market Access routing
"DMA"
destinationmandatoryTarget exchange for order execution
"NYSE",
"NASDAQ",
"ARCA"
display_qtyoptionalMaximum shares/contracts displayed on the exchange at any timeMust be in round lot increments (100s)
Notes:

Parameter replacement is not supported for DMA orders

Available Destinations
NYSE - New York Stock Exchange

NASDAQ - NASDAQ Stock Market

ARCA - NYSE Arca

We’re starting with the three destinations listed above, with plans to expand to 10+ additional destinations—including BATS, IEX, AMEX, and more—in the coming months.

Extended Hours Trading
DMA orders support extended hours trading for the following destinations:

NASDAQ - Pre-market and after-hours sessions

ARCA - Pre-market and after-hours sessions

VWAP: Volume-Weighted Average Price Orders
A VWAP order is designed to execute a trade at or near the volume-weighted average price of a security over a specified time period. It is calculated by dividing the total dollar value traded for the security (price × volume) by the total volume traded during that period.

VWAP automatically weights each trade price by its corresponding trade volume, ensuring the average reflects both price and trading activity. This makes VWAP a valuable reference for assessing execution quality and market trends.

Benefits:

Market Impact Management: VWAP orders are designed to execute in proportion to market volume, which may help reduce the likelihood of large trades significantly influencing the market price.

Benchmark Alignment: VWAP can be used as a benchmark strategy, aiming to achieve execution prices close to the volume-weighted average price over a specified time period. This approach may help align fills with average market pricing trends.

Implementation
VWAP orders are configured using
advanced_instructions in your order request payload:
SubmitReplaceCancel

curl --request POST \
 --url $APIDOMAIN/v2/orders \
 --header 'accept: application/json' \
 --header 'content-type: application/json' \
 --header "Apca-Api-Key-Id: $APIKEY" \
 --header "Apca-Api-Secret-Key: $SECRET" \
 --data '
{
 "side": "buy",
 "symbol": "AAPL",
 "type": "limit",
 "qty": "100",
 "time_in_force": "day",
 "limit_price": "212",
 "order_class": "simple",
 "advanced_instructions": {
 "algorithm": "VWAP",
 "start_time": "2025-07-21T09:30:00-04:00",
 "end_time": "2025-07-21T15:30:00-04:00",
 "max_percentage": "0.123"
 }
}' | jq -r

curl --request PATCH \
 --url $APIDOMAIN/v2/orders/<your_order_id> \
 --header 'accept: application/json' \
 --header 'content-type: application/json' \
 --header "Apca-Api-Key-Id: $APIKEY" \
 --header "Apca-Api-Secret-Key: $SECRET" \
 --data '
{
 "qty": "200",
 "advanced_instructions": {
 "algorithm": "VWAP",
 "start_time": "2025-07-21T09:40:00-04:00",
 "end_time": "2025-07-21T15:20:00-04:00",
 "max_percentage": "0.321"
 }
}' | jq -r

curl --request DELETE \
 --url $APIDOMAIN/v2/orders/<your_order_id> \
 --header 'accept: application/json' \
 --header "Apca-Api-Key-Id: $APIKEY" \
 --header "Apca-Api-Secret-Key: $SECRET" \

Notes:

If
advanced_instructions is not included in the replace payload then it will remain the same

If
advanced_instructions is included in the replace payload then it will replace the original one. So if the client wants to update only the
end_time and keep the rest parameters as is, then the whole
advanced_instructions payload needs to be sent in the replace request, including the unchanged parameters.

Parameters
Parameter

Required

Description

Values

algorithm

mandatory

Must be set to "VWAP" for Volume-Weighted Average Price Orders

"VWAP"

start_time

optional

When the algorithm is to start executing

RFC3339 Timestamp, must be within current market trading hours. Defaults to start immediately or at start of the regular market hours (whichever is later). VWAP orders do NOT participate in Open Auction.

end_time

optional

When the algorithm is to be done executing

RFC3339 Timestamp, must be within current market trading hours and after
start_time. Defaults to end of regular market hours. VWAP orders do NOT participate in Close Auction.

max_percentage

optional

Maximum percentage of the ticker's period volume this
order might participate in

Decimal number, must be 0 <
max_percentage < 1, with up to 3 decimal points precision.

TWAP: Time-Weighted Average Price Orders
A TWAP order is designed to execute a trade evenly over a specified time period, regardless of market volume. The order is divided into equal-sized trades that are placed at regular, pre-defined intervals until the order is complete.

Benefits:

Reduces Market Impact: By spreading the order evenly across time, TWAP can help minimize the risk of significant price swings caused by large trades.

Execution Predictability: Unlike VWAP, which adjusts based on market volume, TWAP may offer more consistent, evenly paced execution, which can be helpful in managing certain trading strategies.

Effective in Low-Liquidity Environments: When volume patterns are unpredictable, TWAP can help prevent trades from disrupting the market and can help maintain price stability.

Implementation
TWAP orders are configured using
advanced_instructions in your order request payload:
SubmitReplaceCancel

curl --request POST \
 --url $APIDOMAIN/v2/orders \
 --header 'accept: application/json' \
 --header 'content-type: application/json' \
 --header "Apca-Api-Key-Id: $APIKEY" \
 --header "Apca-Api-Secret-Key: $SECRET" \
 --data '
{
 "side": "buy",
 "symbol": "AAPL",
 "type": "limit",
 "qty": "100",
 "time_in_force": "day",
 "limit_price": "212",
 "order_class": "simple",
 "advanced_instructions": {
 "algorithm": "TWAP",
 "start_time": "2025-07-21T09:30:00-04:00",
 "end_time": "2025-07-21T15:30:00-04:00",
 "max_percentage": "0.123"
 }
}' | jq -r

curl --request PATCH \
 --url $APIDOMAIN/v2/orders/<your_order_id> \
 --header 'accept: application/json' \
 --header 'content-type: application/json' \
 --header "Apca-Api-Key-Id: $APIKEY" \
 --header "Apca-Api-Secret-Key: $SECRET" \
 --data '
{
 "qty": "200",
 "advanced_instructions": {
 "algorithm": "TWAP",
 "start_time": "2025-07-21T09:40:00-04:00",
 "end_time": "2025-07-21T15:20:00-04:00",
 "max_percentage": "0.321"
 }
}' | jq -r

curl --request DELETE \
 --url $APIDOMAIN/v2/orders/<your_order_id> \
 --header 'accept: application/json' \
 --header "Apca-Api-Key-Id: $APIKEY" \
 --header "Apca-Api-Secret-Key: $SECRET" \

Notes:

If
advanced_instructions is not included in the replace payload then it will remain the same

If
advanced_instructions is included in the replace payload then it will replace the original one. So if the client wants to update only the
end_time and keep the rest parameters as is, then the whole
advanced_instructions payload needs to be sent in the replace request, including the unchanged parameters.

Parameters
Parameter

Required

Description

Values

algorithm

mandatory

Must be set to "TWAP" for Time-Weighted Average Price Orders

"TWAP"

start_time

optional

When the algorithm is to start executing

RFC3339 Timestamp, must be within current market trading hours. Defaults to start immediately or at start of the regular market hours (whichever is later). TWAP orders do NOT participate in Open Auction.

end_time

optional

When the algorithm is to be done executing

RFC3339 Timestamp, must be within current market trading hours and after
start_time. Defaults to end of regular market hours. TWAP orders do NOT participate in Close Auction.

max_percentage

optional

Maximum percentage of the ticker's period volume this
order might participate in

Decimal number, must be 0 <
max_percentage < 1, with up to 3 decimal points precision.

Key Considerations:

advanced_instructions will be accepted for paper trading; however, the order will not be simulated in the paper environment.

DMA gateway only supports market and limit orders and Time in Force (TIF) = day. If you wish to use MOO/MOC, gtc, or stop orders, you cannot specify advanced_instructions

Direct Market Access Gateway is provided solely by DASH Financial Technologies ("DASH"), a member of the listed exchanges. Alpaca enables customers to route orders to the selected exchange through DASH’s DMA capabilities..

Please note that this is currently only available to users who are on theElite Smart Router. For more information on Alpaca Elite please see the term and conditions.

The content of this article is for general informational purposes only. All examples are for illustrative purposes only.

All investments involve risk, and the past performance of a security, or financial product does not guarantee future results or returns. There is no guarantee that any investment strategy will achieve its objectives. Please note that diversification does not ensure a profit, or protect against loss. There is always the potential of losing money when you invest in securities, or other financial products. Investors should consider their investment objectives and risks carefully before investing.

Securities brokerage services are provided by Alpaca Securities LLC ("Alpaca Securities"), memberFINRA/SIPC, a wholly-owned subsidiary of AlpacaDB, Inc. Technology and services are offered by AlpacaDB, Inc.

This is not an offer, solicitation of an offer, or advice to buy or sell securities or open a brokerage account in any jurisdiction where Alpaca Securities are not registered or licensed, as applicable.

Updated4 days ago
Placing OrdersUser ProtectionAsk AI
