---
source: https://docs.alpaca.markets/docs/ach-funding
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

ACH Funding
Plaid Integration for Bank Transfers
We have integrated with Plaid to allow you to seamlessly link your Plaid account to Alpaca. The integration will allow your end-users to verify their account instantly through Plaid's trusted front-end module.

Leveraging this allows you to generate Plaid Processor Tokens on behalf of your end-users, which allows Alpaca to immediately retrieve a user's bank details in order to deposit or withdraw funds on the Alpaca platform.

You can utilize your Plaid account and activate the Alpaca integration within the Plaid dashboard.

The integration requires Plaid API Keys

Obtaining a Plaid Processor Token
A Plaid processor token is used to enable Plaid integrations with partners. After a customer connects their bank using Plaid Link, a processor token can be generated at any time. Please refer to the Plaid Processor Token using Alpaca page for creating a token and additional details.

Exchange token
cURL

curl -X POST https://sandbox.plaid.com/item/public_token/exchange
	-H 'Content-Type: application/json'
	-d '{
 "client_id": "PLAID_CLIENT_ID",
 "secret": "PLAID_SECRET",
 "public_token": "PUBLIC_TOKEN"
}'
Create a processor token for a specific account id.
cURL

curl -X POST https://sandbox.plaid.com/processor/token/create
	-H 'Content-Type: application/json'
	-d '{
 "client_id": "PLAID_CLIENT_ID",
 "secret": "PLAID_SECRET",
 "access_token": "ACCESS_TOKEN",
 "account_id": "ACCOUNT_ID",
 "processor": "alpaca"
}'
For a valid request, the API will return a JSON response similar to:
JSON

{
 "processor_token": "processor-sandbox-0asd1-a92nc",
 "request_id": "m8MDnv9okwxFNBV"
}
Processor Token Flow
End-user links bank account using Plaid.

Plaid returns a public token to you.

You will submit a public token to Plaid in exchange for an access token.

You will submit access token to Plaid's /processor/token/create endpoint and receive Processor Token (specific to Alpaca).

You will make a call to the processor endpoint to pass Alpaca the processor token, to initiate the payment. To pass the processor token use the ACH relationships endpoint (Link).

Sample Request
POST
/v1/accounts/{account_id}/ach_relationships
JSON

{
 "processor_token": "processor-sandbox-161c86dd-d470-47e9-a741-d381c2b2cb6f"
}
Sample responseJSON

{
 "id": "794c3c51-71a8-4186-b5d0-247b6fb4045e",
 "account_id": "9d587d7a-7b2c-494f-8ad8-5796bfca0866",
 "created_at": "2021-04-08T23:01:53.35743328Z",
 "updated_at": "2021-04-08T23:01:53.35743328Z",
 "status": "QUEUED",
 "account_owner_name": "John Doe",
 "nickname": "Bank of America Checking"
}
Alpaca makes a call to Plaid to retrieve the Account and Routing number using the processor token.

Alpaca saves the processor token and account and routing number internally for future use. Alpaca uses account information for NACHA file creation and processing.

*Can include Auth, Identity, Balance info - if the broker API wants to initiate a transfer, we use the transfer endpoint.

ACH Status Flow
Updated4 days ago
Funding WalletsInstant FundingAsk AI
