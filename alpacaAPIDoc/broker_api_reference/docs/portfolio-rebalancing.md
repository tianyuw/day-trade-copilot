---
source: https://docs.alpaca.markets/docs/portfolio-rebalancing
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

Portfolio Rebalancing
Rebalancing API offers investment advisors a way to easily create investment portfolios that are automatically updated to the specified cash, stock symbol percentage weights, rebalance conditions, and triggers selected. Some helpful definitions before an overview of the rebalancing flow:

Portfolios: An allocation containing securities and/or cash with specific weights and conditions to be met

Subscriptions: Accounts can be subscribed to a created portfolio and follow rebalancing events to ensure the account if kept in sync with the target portfolio

Runs: A run is a set of orders that will be sent for execution to achieve a goal (liquidating a specified amount to set it aside for withdrawal or doing a full rebalance to the target allocation)
📘
Rebalancing API Resource
Postman Collection

How to Get Started with Rebalancing API

Rebalancing API Reference

Types of Rebalancing
Rebalancing API offers two types of rebalancing conditions:

Drift Band: When a portfolio breaches a certain threshold, irrespective of the time period elapsed, the portfolio is adjusted. For instance, if we put a +/- 10% band on a portfolio, we would automatically adjust the entire portfolio when we reach the threshold for one of the holdings

Calendar: At the desired period, the state of the portfolio is analyzed and the portfolio is rebalanced to the default portfolio. For example, on April 1st our 50:50 AAPL TLT portfolio is not 55:45, so we would need to liquidate TLT and buy more AAPL to return to the desired state of exposure of 50:50.

Create a Portfolio
To create a portfolio use the Create Portfolio
POST endpoint.

See below see example payload to create a portfolio with a mix of cash and securities:
JSON

{
 "name": "Balanced",
 "description": "A balanced portfolio of stocks and bonds",
 "weights": [
 {
 "type": "cash",
 "percent": "5"
 },
 {
 "type": "asset",
 "symbol": "SPY",
 "percent": "60"
 },
 {
 "type": "asset",
 "symbol": "TLT",
 "percent": "35"
 }
 ],
 "cooldown_days": 7,
 "rebalance_conditions": [
 {
 "type": "drift_band",
 "sub_type": "absolute",
 "percent": "5"
 },
 {
 "type": "drift_band",
 "sub_type": "relative",
 "percent": "20"
 }
 ]
}
Once exeuted, you can find the portfolio ID in the response payload similar to the one below. In our case our newly created portfolio ID is 2d49d00e-ab1c-4014-89d8-70c5f64df2fc. This will be needed to be able to subscribe an account to follow this new portfolio.
JSON

{
 "id": "2d49d00e-ab1c-4014-89d8-70c5f64df2fc",
 "name": "Balanced Two",
 "description": "A balanced portfolio of stocks and bonds",
 "status": "active",
 "cooldown_days": 7,
 "created_at": "2022-08-07T14:56:45.116867815-04:00",
 "updated_at": "2022-08-07T14:56:45.196857944-04:00",
 "weights": [
 {
 "type": "cash",
 "symbol": null,
 "percent": "5"
 },
 {
 "type": "asset",
 "symbol": "SPY",
 "percent": "60"
 },
 {
 "type": "asset",
 "symbol": "TLT",
 "percent": "35"
 }
 ],
 "rebalance_conditions": [
 {
 "type": "drift_band",
 "sub_type": "absolute",
 "percent": "5",
 "day": null
 },
 {
 "type": "drift_band",
 "sub_type": "relative",
 "percent": "20",
 "day": null
 }
 ]
}

You can also list all your created portfolios with the List All Portfolios endpoint.

Subscribe Account to a Portfolio
Once you have a portfolio created, the next step is to subscribe a given account to follow a portfolio. This will ensure that when rebalancing conditions are found the accounts is subscribed to have the needed orders executed.

To subscribe an account to our newly created portfolio and its rebalancing conditions we create a new subscription. For example, to subscribe account ID bf2b0f93-f296-4276-a9cf-288586cf4fb7 to our newly created portfolio from before, we use the Create Subscriptions endpoint with the following JSON payload,
JSON

{
 "account_id": "bf2b0f93-f296-4276-a9cf-288586cf4fb7",
 "portfolio_id": "57d4ec79-9658-4916-9eb1-7c672be97e3e"
}
Check Rebalancing Events
Once an account is subscribed to a portfolio, we need to wait for the first rebalancing event to happen. We can check completed rebalancing events for all our accounts by using the List All Runs endpoint.
cURL

curl --location --request GET '{{HOST}}/v1/beta/rebalancing/runs?status=COMPLETED_SUCCESS' \
--header 'Authorization: Basic <TOKEN>' \
--data-raw ''
See example payload of a succesful run,
JSON

{
 "runs": [
 {
 "id": "36699e7f-56a0-4b87-8e03-968363f4b6df",
 "type": "full_rebalance",
 "amount": null,
 "initiated_from": "system",
 "status": "COMPLETED_SUCCESS",
 "reason": null,
 "account_id": "b3130eeb-1219-46f3-8bfb-7715f00d736b",
 "portfolio_id": "4ad7d634-a60d-4e6e-955f-3c68ee24d285",
 "weights": [
 {
 "type": "cash",
 "symbol": null,
 "percent": "5"
 },
 {
 "type": "asset",
 "symbol": "SPY",
 "percent": "60"
 },
 {
 "type": "asset",
 "symbol": "TLT",
 "percent": "35"
 }
 ],
 "orders": [
 {
 "id": "c29dd94b-eaaf-4681-9d1f-4fd47571804b",
 "client_order_id": "cb2d1ff5-8355-4c92-84d7-dfff43f44cb2",
 "created_at": "2022-03-08T16:51:07.442125Z",
 "updated_at": "2022-03-08T16:51:07.525039Z",
 "submitted_at": "2022-03-08T16:51:07.438495Z",
 "filled_at": "2022-03-08T16:51:07.520169Z",
 "expired_at": null,
 "canceled_at": null,
 "failed_at": null,
 "replaced_at": null,
 "replaced_by": null,
 "replaces": null,
 "asset_id": "3b64361a-1960-421a-9464-a484544193df",
 "symbol": "SPY",
 "asset_class": "us_equity",
 "notional": "30443.177578017",
 "qty": null,
 "filled_qty": "72.865432211",
 "filled_avg_price": "417.8",
 "order_class": "",
 "order_type": "market",
 "type": "market",
 "side": "buy",
 "time_in_force": "day",
 "limit_price": null,
 "stop_price": null,
 "status": "filled",
 "extended_hours": false,
 "legs": null,
 "trail_percent": null,
 "trail_price": null,
 "hwm": null,
 "subtag": null,
 "source": null
 },
 {
 "id": "ab772dcb-b67c-4173-a5b5-e31b9ad236b5",
 "client_order_id": "d6278f6c-3010-45ce-aaee-6e64136deec0",
 "created_at": "2022-03-08T16:51:07.883352Z",
 "updated_at": "2022-03-08T16:51:07.934602Z",
 "submitted_at": "2022-03-08T16:51:07.877726Z",
 "filled_at": "2022-03-08T16:51:07.928907Z",
 "expired_at": null,
 "canceled_at": null,
 "failed_at": null,
 "replaced_at": null,
 "replaced_by": null,
 "replaces": null,
 "asset_id": "a106d0ef-e6f2-4736-8750-5dee1cadf75b",
 "symbol": "TLT",
 "asset_class": "us_equity",
 "notional": "17121.076868834",
 "qty": null,
 "filled_qty": "124.408348124",
 "filled_avg_price": "137.62",
 "order_class": "",
 "order_type": "market",
 "type": "market",
 "side": "buy",
 "time_in_force": "day",
 "limit_price": null,
 "stop_price": null,
 "status": "filled",
 "extended_hours": false,
 "legs": null,
 "trail_percent": null,
 "trail_price": null,
 "hwm": null,
 "subtag": null,
 "source": null
 }
 ],
 "completed_at": null,
 "canceled_at": null,
 "created_at": "2022-03-08T16:36:07.053482Z",
 "updated_at": "2022-03-08T16:51:08.53806Z"
 },
 ...
 ],
 "next_page_token": 100
}
📘
Note
Cash inflows to the account (deposits, cash journals, etc.) will trigger buy trades to reduce drift.

Manually Trigger Rebalancing Event (Run)
Rebalancing API will automatically configure systems to watch for portfolio rebalancing conditions and execute necessary orders. However, if you need to execute a rebalancing run see reference of Create Run endpoint.
🚧
Manually executing a run is currently only allowed for accounts who do not have an active subscription.
Portfolio Rebalance Evaluation
Portfolios are evaluated for potential rebalancing based on specific conditions checked in a defined order.

Prerequisites:

Status:

Only portfolios with an
active status are considered for evaluation.

If an asset within a portfolio is found to be inactive, non-fractionable, or untradable during a rebalance, the portfolio's status automatically transitions to
needs_adjustment.

Change required: Portfolios in
needs_adjustment are excluded from evaluation. To re-enable evaluation for such portfolios, you must first update their status back to
active using a
PATCH request.

Weights:

portfolio weights are required to have a
percent greater than zero.

If a weight of type cash has its percent set to zero, it will be automatically removed from the portfolio configuration

Evaluation Order and Conditions:

The system checks for the following conditions sequentially. The first condition met may trigger a rebalance (or place the portfolio in a state requiring rebalance):

in_cooldown: Checks if the portfolio is currently within a defined cooldown period following a previous rebalance. If true, evaluation may stop here for this cycle.

calendar: Checks for scheduled rebalancing based on predefined intervals:
Annually

Quarterly

Monthly

Weekly

drift_band: Checks if portfolio asset allocations have deviated beyond configured thresholds:

absolute: Deviation measured in absolute percentage points (e.g., target is 10%, drift triggers if allocation goes below 8% or above 12% for a 2% absolute threshold).

relative: Deviation measured relative to the target allocation percentage (e.g., target is 10%, drift triggers if allocation goes below 9% or above 11% for a 10% relative threshold).

Important Considerations:

Minimum Order Size: Be aware that a minimum order value (often around $1 per asset) typically applies during rebalancing trades. This means sufficient cash balance is required to execute orders across potentially many assets. An estimated minimum cash need could be
(Number of Assets in Portfolio) * $1. Plan account funding accordingly, especially for portfolios with many assets.

Daily Processing Runs

Portfolios are evaluated daily for one of two mutually exclusive processing runs:
full_rebalance or
invest_cash. Only one type of run can execute per portfolio per day. The system checks eligibility in the following order:

full_rebalance: To realign the portfolio's current holdings to match its target weights as closely as possible, it will execute both buy and sell orders. (Note: This run typically triggers based on portfolio drift or other rebalancing criteria).

invest_cash: If a
full_rebalance is not executed, the system then checks if an
invest_cash run can be performed. This requires the portfolio's account to have an available cash balance exceeding $10 USD. If triggered,
invest_cash only executes buy orders, utilizing the available cash to shift the portfolio's allocation closer to its target weights. This can occur a maximum of once per day.

FAQ
Q: What is the minimum cash required for a rebalancing run?

For a rebalancing run to occur, there must be a minimum of $1 per asset in the portfolio.

Example 1 - A portfolio that is 50% AAPL, 25% TSLA, 25% GOOGL
Assuming all other rebalancing conditions and cooldown days are met, a rebalancing run would only occur with at least $1 per asset in the portfolio deposited. Anything less would not trigger a rebalance.

Example 2 - A portfolio that is 50% AAPL, 25% TSLA, 25% CASH
Assuming all other rebalancing conditions and cooldown days are met, a rebalancing run would only occur with at least $1 per asset in the portfolio deposited. Anything less would not trigger a rebalance.

For an invest_cash run to occur, a minimum of $10 must be deposited.

Q: Can rebalancing run partially for some assets where minimum notional is satisfied but not run for the assets where minimum notional is not satisfied?

Yes. If a portfolio has 11 assets, but only $10 is deposited, there will be a partial rebalancing where 10 assets will be invested in.

Q: When does a Rebalancing Job or invest_cash job run at Alpaca?

When cash is first invested into a portfolio (assuming the minimum cash requirement is met), a rebalancing job of type full_rebalance will occur.

Thereafter, if a minimum of $10 is invested, an invest_cash job will run regardless of the portfolio rebalancing conditions and the cooldown period.

After the cooldown period, and if the rebalancing conditions are met, then a rebalancing job will run.

Both the rebalance and invest_cash jobs run between 930am -330pm EST .

Q: What are the steps for Cash Withdrawal if a user wants to close the positions and withdraw their cash?

The steps are as follows:

Unsubscribe the user using the https://broker-api.sandbox.alpaca.markets/v1/rebalancing/subscriptions/{subscription_id} DELETE request.

Execute a manual run with revised portfolio weights using the https://broker-api.sandbox.alpaca.markets/v1/rebalancing/runs POST request.

Wait for the desired amount to be available as withdrawable cash, and then make a GET request to https://broker-api.sandbox.alpaca.markets/v1/trading/accounts/{account_id}/account and check if cash_withdrawable has the desired amount.

*Note: The amount credited from the trade, will be available for withdrawal on the next trading day (T+1).

Journal the money from user account to firm account using the https://broker-api.sandbox.alpaca.markets/v1/journals POST request.

Subscribe the user back to their portfolio using the https://broker-api.sandbox.alpaca.markets/v1/rebalancing/subscriptions POST request.

Q: Under what conditions might the rebalancer stop rebalancing my portfolio?

The rebalancer may cease operations if your account encounters certain restrictions that block trading activities. These include:

Pattern Day Trading (PDT) Flag: If your account is marked as a Pattern Day Trader, trading will be restricted. For more details, refer to our PDT rule explanation.

ACH Return: When an ACH deposit is returned by your bank, your account is automatically restricted and will lead to trading blocks on your account.

Position to Equity Ratio Exceeded: This is calculated as (position_market_value / equity). If this ratio exceeds the maximum allowed limit (6:1), the account will be restricted during buying power verification.

Crypto Trading Restriction: Set when account is restricted to liquidation for crypto trading

Options Trading Restriction: Set when account is restricted to liquidation for options trading

Unspecified Restrictions: Other unforeseen issues may also result in trading limitations.

To ensure continuous rebalancing run functionality, it's crucial to monitor your account for these conditions and address any issues promptly.

Updated4 days ago
TradingSSE EventsAsk AI
