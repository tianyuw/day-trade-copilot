---
source: https://docs.alpaca.markets/docs/accounts-statuses
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

Accounts Statuses
The following are the possible account status values. Accounts will have both
status and
crypto_status with
status denoting the account's equities trading status and
crypto_status denoting the account's crypto trading status.

Most likely, the account status is
ACTIVE unless there is an issue. The account status may get to
ACCOUNT_UPDATED when personal information is being updated from the API, in which case the end user may not be allowed trading for a short period of time until the change is approved.

For more on creating an account check out our API reference section on the Accounts Endpoint.
statusdescription
INACTIVEAccount not set to trade given asset.
ONBOARDINGThe account has been created but we haven’t performed KYC yet. This is only used with Onfido.
SUBMITTEDThe account application has been submitted and is being processed, this is a transitory status.
SUBMISSION_FAILEDThe account failed to be created in Alpaca's system. Accounts in this status are resolved by Alpaca and no further action is needed.
ACTION_REQUIREDThe account application requires manual action and a document upload is required from the user. KYCResults contains information about the details.
APPROVAL_PENDINGThe application requires manual checks from our team because the account did not pass the KYC automatic check, but most likely no document is required. KYCResults contains information about the details.
APPROVEDThe account application has been approved, waiting to be ACTIVE, this is a transitory status.
REJECTEDThe account application was rejected by our team. The account will not be able to continue to go active.
ACTIVEThe account is fully active and can start trading the enabled asset.
ACCOUNT_UPDATEDThe account personal information is being updated which needs to be reviewed before being moved back to ACTIVE.
ACCOUNT_CLOSEDThe account was closed, will not be able to trade or fund anymore.
Account statuses flowchart

Account Updated
Please note that outgoing transfers are restricted while in this status.

To move accounts from
ACCOUNT_UPDATED back to
ACTIVE, Alpaca will handle the process manually. The specific nature of the update will determine the necessary actions to be taken for returning to
ACTIVE status. For non-material updates, the accounts will be regularly moved back to
ACTIVE without requiring any action from the end-user or partner.

For material updates, additional documentation or confirmation will be needed, such as IDs, W8BEN corrections, address verifications, or new CIP reports. The required documents and instructions will be communicated to our partners accordingly.

Edits to the below fields will trigger a status change to
ACCOUNT_UPDATED:

given_name

family_name

street_address

unit

city

state

postal_code

country_of_citizenship

employer_name

employment_position

if any of the following disclosures are set to true when they were previously false then that triggers account_updated as well
is_control_person

is_politically_exposed

immediate_family_exposed

is_affiliated_exchange_or_finra

Updated4 days ago
Customer Account OpeningInternational AccountsAsk AI
