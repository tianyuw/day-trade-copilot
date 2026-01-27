---
source: https://docs.alpaca.markets/docs/instant-funding
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

Instant Funding
Instant Funding for Broker API, allows broker partners to offer their customers instant access to funds by creating an instant funding transfer i.e. extending buying power at the customer account level. This enables customers to begin trading immediately without the need for funds to arrive and settle at Alpaca.

Key Features
Customers can access instant buying power allowing them to trade immediately.
Partners do not have to pre-fund or settle funds with Alpaca on T+0 for stock trading
The ability for a partner to set specific limits on end-user accounts for instant funding (by default USD 1000)
Partners have the option to create an additional revenue stream by configuring a flexible fee mark-up for customers

Cutoffs & Interest Requirements
Batching for Settlement:
All instant funding transfers within a 24-hour window (from 8 PM ET the previous day to 8 PM ET the current day) are grouped for settlement in the next cycle. The settlement of these instant transfers must be completed before 1 PM on T+1. Each settlement cycle has a report associated with it which can be obtained from the instant funding reports endpoint described here.

Late Payment & Interest Charges:
Instant funding transfers not settled by 1 PM ET on T+1 will incur late payment interest which is invoiced monthly to the partner.
Penalty interest on late payments is calculated at FED UB + 8% (based on FRED Economic Data) and it is charged to the partner
Unreconciled instant funding transfers are automatically canceled at 8 PM ET on T+1 (date of settlement). The account may incur a margin interest rate (documented here) and end up in a debit balance if the user has already spent the instant funding credit.

How it Works
Broker partners will collect funds from your customers and upon receipt of each payment you'll then call the Instant Funding API to create an instant funding transfer. This will extend the buying power to each end user.
The instant funding reports endpoint can be used to get the detail and summary report for the amount owed. The detailed view will give the breakdown of the amount owed for the instant funding transfer and the summary view will give the cumulative value.

You will then send one wire payment to Alpaca to settle the outstanding instant funding transfer by T+1 (the next business day) by 1 pm ET. This will be followed by using the settlement API to trigger the settlement which will check for funds in the SI account and perform the settlement.
Given below is a detailed overview of the process along with the working of the relevant APIs.

This flow is illustrated in the diagram above

How to Create an Instant Funding Transfer
Step 1: Create an Instant Funding Transfer
You must specify the account you would like to credit with an instant funding transfer, the firm account the buying power will be borrowed from, and the amount to credit.

Request
POST v1/instant_funding
JSON

{
 "account_no": "{ACCOUNT_NO}",
 "source_account_no": "{ACCOUNT_NO}",
 "amount": "20",
}
Response
JSON

{
 "account_no": "{ACCOUNT_NO}",
 "amount": "20",
 "created_at": "2024-11-11T08:20:10.726356556-05:00",
 "deadline": "2024-11-13",
 "fees": [],
 "id": "fcc6d9fc-ce36-484a-bd86-a27b98c2d1ab",
 "interests": [],
 "remaining_payable": "20",
 "source_account_no": "{ACCOUNT_NO}",
 "status": "PENDING",
 "system_date": "2024-11-12",
 "total_interest": "0"
}
Instant funding transfer executed (before settlement)
JSON

 {
 "id": "20241111000000000::6b784928-f314-47bc-905f-0a49ebc9e413",
 "account_id": "{ACCOUNT_ID}",
 "activity_type": "MEM",
 "date": "2024-11-11",
 "net_amount": "0",
 "description": "type: instant_funding_memopost, transfer_id: fcc6d9fc-ce36-484a-bd86-a27b98c2d1ab",
 "symbol": "INSTANTUSD",
 "qty": "20",
 "status": "executed"
 }
Instant funding transfer canceled (after settlement or after failed reconciliation)
JSON

{
 "id": "20241111000000000::6b784928-f314-47bc-905f-0a49ebc9e413",
 "account_id": "{ACCOUNT_ID}",
 "activity_type": "MEM",
 "date": "2024-11-11",
 "net_amount": "0",
 "description": "type: instant_funding_memopost, transfer_id: fcc6d9fc-ce36-484a-bd86-a27b98c2d1ab",
 "symbol": "INSTANTUSD",
 "qty": "20",
 "status": "canceled"
}
CSD executed (after settlement)
JSON

{
 "id": "20241111000000000::daa5e4e9-7974-4273-a926-7ab0647d8850",
 "account_id": "{ACCOUNT_ID}",
 "activity_type": "CSD",
 "date": "2024-11-11",
 "net_amount": "20",
 "description": "type: instant_funding_deposit, transfer_id: fcc6d9fc-ce36-484a-bd86-a27b98c2d1ab, settlement_id: 28f27c76-ea14-4d4c-8a04-8f666b14a224",
 "status": "executed"
}
Step 1.1: Check status of an Instant Funding Transfer
Fetch a specific instant funding transfer to check the current status of the transfer.

Request

GET v1/instant_funding/:instant_funding_id

Response
JSON

{
 "account_no": "{ACCOUNT_NO}",
 "amount": "20",
 "created_at": "2024-09-10T09:12:36.88272Z",
 "deadline": "2024-09-11",
 "fees": [],
 "id": "d96bdc91-6d1c-49b5-a3c3-03f16c70321b",
 "interests": [],
 "remaining_payable": "20",
 "source_account_no": "{ACCOUNT_NO}",
 "status": "EXECUTED",
 "system_date": "2024-09-10",
 "total_interest": "0"
}
Additionally, all instant funding transfers can be listed using the following API

Request

GET v1/instant_funding?sort_by=created_at&sort_order=DESC

Response
JSON

{
 "account_no": "{ACCOUNT_NO}",
 "amount": "20",
 "created_at": "2024-09-10T09:12:36.88272Z",
 "deadline": "2024-09-11",
 "fees": [],
 "id": "d96bdc91-6d1c-49b5-a3c3-03f16c70321b",
 "interests": [],
 "remaining_payable": "20",
 "source_account_no": "{ACCOUNT_NO}",
 "status": "EXECUTED",
 "system_date": "2024-09-10",
 "total_interest": "0"
}
Step 1.2: Display Increase in Buying Power
Once the instant funding transfer is moved to a EXECUTED status you can fetch the user’s buying power via the GET trading account endpoint and guide your user to begin trading with their immediate funds.

Request
GET /v1/trading/accounts/fc304c4d-5c2c-41f2-b357-99bbbed9ec90/account

Response
JSON

{
 "id": "{ACCOUNT_ID}",
 "admin_configurations": {
 "allow_instant_ach": true,
 "disable_shorting": true,
 "max_margin_multiplier": "1"
 },
 "user_configurations": null,
 "account_number": "{ACCOUNT_NO}",
 "status": "ACTIVE",
 "crypto_status": "INACTIVE",
 "currency": "USD",
 "buying_power": "100",
 "regt_buying_power": "100",
 "daytrading_buying_power": "0",
 "effective_buying_power": "100",
 "non_marginable_buying_power": "0",
 "bod_dtbp": "0",
 "cash": "100",
 "cash_withdrawable": "0",
 "cash_transferable": "0",
 "accrued_fees": "0",
 "pending_transfer_out": "0",
 "pending_transfer_in": "0",
 "portfolio_value": "0",
 "pattern_day_trader": false,
 "trading_blocked": false,
 "transfers_blocked": false,
 "account_blocked": false,
 "created_at": "2024-07-10T17:23:51.655324Z",
 "trade_suspended_by_user": false,
 "multiplier": "1",
 "shorting_enabled": false,
 "equity": "0",
 "last_equity": "0",
 "long_market_value": "0",
 "short_market_value": "0",
 "position_market_value": "0",
 "initial_margin": "0",
 "maintenance_margin": "0",
 "last_maintenance_margin": "0",
 "sma": "0",
 "daytrade_count": 0,
 "balance_asof": "2024-07-09",
 "previous_close": "2024-07-09T20:00:00-04:00",
 "last_long_market_value": "0",
 "last_short_market_value": "0",
 "last_cash": "0",
 "last_initial_margin": "0",
 "last_regt_buying_power": "0",
 "last_daytrading_buying_power": "0",
 "last_buying_power": "0",
 "last_daytrade_count": 0,
 "clearing_broker": "ALPACA_APCA",
 "memoposts": "100",
 "intraday_adjustments": "0",
 "pending_reg_taf_fees": "0"
}
Step 2: Manage Limits (optional)
The total amount of buying power you can extend to all of your end users combined will be limited. This limit will be determined based on your business needs in production. In sandbox, this will be $100,000 USD by default but can be updated as needed. The amount you can credit to each end user will also be limited to $1,000 USD by default. If you anticipate needing a higher limit per account this can also be updated on request.

As you create instant funding transfers for multiple users throughout the day, you will want to keep an eye on how much of your total instant funding limit you’ve used up or how much buying power you are still able to extend to a specific account. Both of these limits can be monitored via API as shown below.

Step 2.1: View Instant Funding Limits at correspondent level
View the instant funding limit available for you to use across all your end users.

Request
GET v1/instant_funding/limits

Response
JSON

{
 "amount_available": "99900",
 "amount_in_use": "100",
 "amount_limit": "100000"
}
Step 2.2: View Account Level Instant Funding Limits
View the instant funding limit available for a specific account or multiple accounts at once.
Request
GET v1/instant_funding/limits/accounts?account_numbers={ACCOUNT_NO}

Response
JSON

[
 {
 "account_no": "{ACCOUNT_NO}",
 "amount_available": "900",
 "amount_in_use": "100",
 "amount_limit": "1000"
 }
]
How to Settle an Instant Funding Transfer
All instant funding transfers are expected to be settled on T+1 by 1 pm ET, meaning that you will have one business day to convert the instant funding credit from an extension of buying power to actual settled cash. Alpaca makes this easy and convenient by providing two reports that you can rely on to determine exactly how much is owed for settlement and by when.

Once the funds have been sent to Alpaca you will have to explicitly trigger settlement via API.

When a settlement is triggered, Alpaca will perform balance checks to determine if the amount sent is sufficient to complete settlement or if there is an insufficient balance then settlement will not be executed. Excess funds will also be swept to a separate dedicated firm account, denoted by the FW suffix, as the expectation is that the SI firm account is meant to complete instant funding settlement and should be zeroed out after each settlement is completed.

This flow is illustrated in the diagram above

Step 1: Fetch a Settlement Report
Alpaca provides a high level summary report which shows the total amount due for settlement and a detailed report that is broken down to show each of the associated instant funding transfers that are due. These reports are meant to help you quickly understand how much you are expected to send to settle all instant funding transfers created on T+0 or to look back historically and know how much was owed for any given day.

Two kinds of reports can be obtained using this API:
Summary report - This presents an aggregated view of the balance owed to Alpaca
Detail report - This returns both the aggregate and amount at a per instant transfer level owed to Alpaca.

Getting the summary settlement report :

Request
GET v1/instant_funding/reports?report_type=summary&system_date=2024-05-15

Response
JSON

[
 {
 "account_no": "{ACCOUNT_NO}",
 "deadline": "2024-05-16",
 "system_date": "2024-05-15",
 "total_amount_owed": "900",
 "total_interest_penalty": "0.7"
 }
]
Getting the detail settlement report :

Request
GET /v1/instant_funding/reports?report_type=detail&system_date=2024-09-09

Response
JSON

[
 {
 "account_no": "{ACCOUNT_NO}",
 "deadline": "2024-09-10",
 "instant_funding_transfers": [
 {
 "account_no": "{ACCOUNT_NO}",
 "amount": "10",
 "created_at": "2024-09-09T13:20:13.175309Z",
 "deadline": "2024-09-10",
 "fees": [],
 "id": "fade4447-b6ca-4ddf-b87b-3a475861cfeb",
 "interests": [],
 "remaining_payable": "10",
 "source_account_no": "{ACCOUNT_NO}",
 "status": "EXECUTED",
 "system_date": "2024-09-09",
 "total_interest": "0"
 },
 {
 "account_no": "{ACCOUNT_NO}",
 "amount": "20",
 "created_at": "2024-09-09T13:21:48.050636Z",
 "deadline": "2024-09-10",
 "fees": [],
 "id": "f1544394-a6f2-42a8-8758-408e8e0d5099",
 "interests": [],
 "remaining_payable": "20",
 "source_account_no": "{ACCOUNT_NO}",
 "status": "EXECUTED",
 "system_date": "2024-09-09",
 "total_interest": "0"
 }
 ],
 "system_date": "2024-09-09",
 "total_amount_owed": "30",
 "total_interest_penalty": "0.11"
 }
]
Step 2: Submit Payment to Alpaca
Once you are confident that you know exactly how much is owed for settlement, you can initiate a wire payment from your external bank account to Alpaca to be credited to your firm account denoted with the SI suffix. You can monitor the non trade events stream to know exactly when the funds are credited to your account.

Step 3: Trigger Settlement
You will trigger settlement via API and submit the list of instant funding transfers that you wish to settle with the funds credited to your SI firm account. At this stage, you will also include the travel rule details which Alpaca is required to collect. For more information on the travel rule requirements please refer to the FinCEN Advisory as needed.

Please note that only one settlement can be in progress at a time i.e. in pending or awaiting_additional_funds status at a time.

Details of fields required to be sent as part of the transmitter information -
fielddescriptionoriginator_full_nameFull name of the customeroriginator_street_addressStreet address of the entity transmitting fundsoriginator_cityCity of the entity transmitting fundsoriginator_postal_codePostal code of the entity transmitting fundsoriginator_countryCountry of the entity transmitting fundsoriginator_bank_account_numberCustomer’s account number on the platformoriginator_bank_nameLegal entity that is transmitting the funds
Request
POST v1/instant_funding/settlements
JSON

{
 "transfers": [
 {
 "instant_transfer_id": "29d8afd1-b7b1-4b47-830d-263244c4d28b",
 "transmitter_info": {
 "originator_full_name": "John Doe",
 "originator_street_address": "123 Alpaca Way",
 "originator_city": "San Mateo",
 "originator_postal_code": "12345",
 "originator_country": "USA",
 "originator_bank_account_number": "123456789",
 "originator_bank_name": "Citibank"
 }
 }
 ],
 "additional_info": "bulk wire sent to account {ACCOUNT_NO} from Citibank account number 191919191"
}
Response
JSON

{
 "created_at": "2024-05-24T08:56:01.440771581-04:00",
 "id": "53d63f11-e844-4867-ab72-364bb1ac9258",
 "interest_amount": "0",
 "source_account_number": "{ACCOUNT_NO}",
 "status": "PENDING",
 "total_amount": "100",
 "updated_at": "2024-05-24T08:56:01.440771581-04:00"
}

Step 4: Check settlement status
After triggering the settlement, it’s important to check the status of the settlement to make sure that the reconciliation has been completed.

Request
GET /v1/instant_funding/settlements/c9a89b1b-94fe-4852-8ba1-140b67aa7280

Response
JSON

{
 "completed_at": "2024-10-29T14:50:46.337084Z",
 "created_at": "2024-10-29T14:50:15.926307Z",
 "id": "a0f41a2c-60f3-49f2-90cd-e4ec2560c819",
 "interest_amount": "0",
 "source_account_number": "{ACCOUNT_NO}",
 "status": "COMPLETED",
 "total_amount": "20",
 "updated_at": "2024-10-29T14:50:46.337131Z"
}
Step 4.1: Successful reconciliation
When a settlement is successful, the instant funding credit is canceled and the respective amount is debited from the SI account. In account activities, this is represented as a canceled MEM activity followed by an executed CSD activity for an amount equivalent to the instant funding transfer amount that was settled.

Given below is a sample response for a successful reconciliation.

Response
JSON

{
 "completed_at": "2024-08-26T15:10:03.337899Z",
 "created_at": "2024-08-26T15:09:18.077505Z",
 "id": "133cef1d-0300-41cc-9ac4-9c75cd1518b1",
 "interest_amount": "0",
 "source_account_number": "{ACCOUNT_NO}",
 "status": "COMPLETED",
 "total_amount": "20",
 "updated_at": "2024-08-26T15:10:03.337921Z"
}
Step 4.2: Handling failed reconciliation
If the settlement fails with the reason "reason": "insufficient balance, available: 0, required: 40", it implies that when the settlement was triggered, the source account did not have enough funds required for the reconciliation. In that case, additional funds can be added to the SI account by journaling money from RF to SI account or sending more funds to the SI account. Once the funds have been loaded, the settlement can be triggered again.

Here’s a sample response for a failed settlement -

Response
JSON

{
 "created_at": "2024-08-27T08:30:24.517942Z",
 "id": "c9a89b1b-94fe-4852-8ba1-140b67aa7280",
 "interest_amount": "0",
 "reason": "insufficient balance, available: 0, required: 40",
 "source_account_number": "{ACCOUNT_NO}",
 "status": "FAILED",
 "total_amount": "40",
 "updated_at": "2024-08-27T09:36:01.026356Z"
}
Step 4.3: Late instant funding transfers and Accounts in debit balances
If an instant funding transfer is late i.e if it is not reconciled by 1 PM on T+1 and henceforth canceled by 8pm T+1, then one of the following scenarios would take place -

Account has sufficient funds - The cash balance in the customer account would be used to offset the outstanding amount of the instant funding transfer

Account has insufficient funds - Customer account would then fall into a debit balance and margin interest will be charged on this until the balance is no longer negative or Alpaca actions on the account to settle the negative balance.

When an account is in debit balance, the cash value for that account will be negative. The debit balance can be settled by the partners by journaling funds from the RF account to the customer’s account directly. The partner can also collect the needed funds locally from their customer before initiating this journal.

The debit balance of an account can be monitored as follows:

Request
GET v1/trading/accounts/:account_id/account

Response
JSON

{
 "id": "{ACCOUNT_ID}",
 "admin_configurations": {
 "allow_instant_ach": true,
 "disable_shorting": true,
 "max_margin_multiplier": "1"
 },
 "user_configurations": null,
 "account_number": "574631172",
 "status": "ACTIVE",
 "crypto_status": "ACTIVE",
 "currency": "USD",
 "buying_power": "0",
 "regt_buying_power": "0",
 "daytrading_buying_power": "0",
 "effective_buying_power": "0",
 "non_marginable_buying_power": "0",
 "bod_dtbp": "0",
 "cash": "-15.26",
 "cash_withdrawable": "0",
 "cash_transferable": "0",
 "accrued_fees": "0.113961944444418396",
 "pending_transfer_out": "0",
 "portfolio_value": "-2.31",
 "pattern_day_trader": false,
 "trading_blocked": false,
 "transfers_blocked": false,
 "account_blocked": false,
 "created_at": "2024-08-05T14:19:45.334013Z",
 "trade_suspended_by_user": false,
 "multiplier": "1",
 "shorting_enabled": false,
 "equity": "-2.31",
 "last_equity": "-1.54",
 "long_market_value": "62.95",
 "short_market_value": "0",
 "position_market_value": "62.95",
 "initial_margin": "62.95",
 "maintenance_margin": "18.88",
 "last_maintenance_margin": "63.61",
 "sma": "0",
 "daytrade_count": 0,
 "balance_asof": "2024-09-09",
 "previous_close": "2024-09-09T20:00:00-04:00",
 "last_long_market_value": "63.61",
 "last_short_market_value": "0",
 "last_cash": "-65.15",
 "last_initial_margin": "63.61",
 "last_regt_buying_power": "0",
 "last_daytrading_buying_power": "0",
 "last_buying_power": "0",
 "last_daytrade_count": 0,
 "clearing_broker": "ALPACA_APCA",
 "memoposts": "50",
 "intraday_adjustments": "0",
 "pending_reg_taf_fees": "0"
}
How to Delete an Instant Funding Transfer
In case an existing instant funding transfer needs to be reversed, the below request can be made to delete the transfer

Request
DELETE v1/instant_funding/{instant_funding_id}

Response
JSON

HTTP 200 OK
Other Resources
Instant Funding Blog Post

Frequently Asked Questions
See our FAQs available here & here.

The content article is for general information only and is believed to be accurate as of posting date but may be subject to change. Alpaca does not provide investment, tax, or legal advice. Please consult your own independent advisor as to any investment, tax, or legal statements made herein.
All investments involve risk, and the past performance of a security, or financial product does not guarantee future results or returns. There is no guarantee that any investment strategy will achieve its objectives. Please note that diversification does not assure a profit, or protect against loss. There is always the potential of losing money when you invest in securities, or other financial products. Investors should consider their investment objectives and risks carefully before investing.
Securities brokerage services are provided by Alpaca Securities LLC ("Alpaca Securities"), member FINRA/SIPC, a wholly-owned subsidiary of AlpacaDB, Inc. Technology and services are offered by AlpacaDB, Inc.
This is not an offer, solicitation of an offer, or advice to buy or sell securities or open a brokerage account in any jurisdiction where Alpaca Securities are not registered or licensed, as applicable.

Updated4 days ago
ACH FundingTradingAsk AI
