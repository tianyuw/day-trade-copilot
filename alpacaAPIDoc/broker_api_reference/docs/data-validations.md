---
source: https://docs.alpaca.markets/docs/data-validations
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

Data Validations
As part of Alpaca Securities LLC’s regulatory obligation to comply with new reporting requirements defined by FINRA, we are required to submit user information to comply with FINRA’s Customer & Account Information System (CAIS). The CAIS system will begin validating the data for correct formatting so we need to ensure that data is provided in correct format at the time of account creation to avoid errors and potential delays with reporting.

This validation will be live in production on March 25, 2024. The validation will be released in sandbox first on March 5, 2024 so you can carry out any testing required.

Validation Criteria
A validation check on user information submitted via the account creation (POST /v1/accounts) and update (PATCH /v1/accounts/{account_id}) endpoints will return a 422 error if the information submitted does not meet our validation criteria. The validation criteria will include the following:

Name and Address Romanization

given_name,
middle_name,
family_name,
street_address,
unit,
city,
state,
postal_code,
email_address, and
tax_id are all required to be provided in latin characters. The accepted input for these fields will be limited to ASCII character range 32-126

We have introduced the following fields to continue accepting name and address information in its original script if desired -
local_given_name,
local_middle_name,
local_family_name,
local_street_address,
local_unit,
local_city, and
local_state

given_name is now required for all users

Tax ID Number Validation

tax_id is required for securities accounts

If the tax ID type is
USA_SSN or
USA_TIN then the following must be met:
No values having an Area Number (first three digits) of 000 nor 666.

No values having a Group Number (middle two digits) of 00.

No values having a Serial Number (last four digits) of 0000.

No values all of the same digit such as 000-00-0000, 111-11-1111, 333-33-3333, 666-66- 6666, 999-99-9999, nor all increasing or decreasing characters i.e. 123-45-6789 or 987-65-4321.

Values must be exactly 9 characters in length after dashes have been stripped

All tax ID types will undergo the following validation:
The length must be greater than 1 character i.e. submitting 0 as a tax ID will not be permitted

No values all of the same digit such as 000-00-0000, 111-11-1111, 333-33-3333, 666-66- 6666, 999-99-9999, nor all increasing or decreasing characters i.e. 123-45-6789 or 987-65-4321.

Max length of 40 characters

Only letters, digits, dashes (denoted by ASCII char 45), periods, and plus (+) signs will be permitted

Value most contain digits (i.e. submitting TIN_NOT_ISSUED or xxx-xxx-xxxx will not be permitted)
As a general reminder to our partners that onboard users in regions where tax ID numbers are not issued, there is still a requirement for a unique identifier to be submitted for those users. The identifier should be either a national identity card number, passport number, permanent resident number, drivers license number, etc. We have introduced the following tax_id_type values to support these classifications. These are also available in our documentation here.

NATIONAL_ID

PASSPORT

PERMANENT_RESIDENT

DRIVER_LICENSE

OTHER_GOV_ID

street_address Validation
No values consisting of only digits

Length must be greater than 1 character

A new validation has been introduced to the street_address field to prevent the submission of US Post Office Boxes (PO Boxes) for a residential address. This validation is case-insensitive and detects keywords indicative of a PO Box, including: PO Box, Post Office Box, P.O. Box, and Box #. If a prohibited value is detected, the request will be blocked, returning a 422 error with the specific message:
"street_address cannot be a P.O. Box". This validation applies to requests via the
POST /v1/accounts and
PATCH /v1/accounts/{account_id} endpoints, and partners should ensure their systems are prepared to handle this new validation error.

Postal Code Validation
If country of tax residence = USA:
The
postal_code attribute will be required upon account creation

No values less than 5 characters in length and the first 5 characters must only contain digits

No values greater than 10 digits

date_of_birth Validation
No values greater than or less than 10 characters in length. Values must be in YYYY-MM-DD format.

Email addresses, after aliases are removed, are restricted to a maxim of 60 characters in length. Alpaca defines an alias as all characters after a + sign and before the @ sign.

State Validation
For all countries
The max length for state should not be greater than 50 characters

State cannot consist of only digits. It can be alphanumeric

If country of tax residence = USA
State will be limited to either the 2 letter abbreviation code for the state or the complete name of the state as defined in our documentation here

The
city attribute cannot consist of only digits. It can be alphanumeric

Whitespace validation
The following validation will be applied to the
given_name,
middle_name,
family_name,
street_address,
unit,
city,
state,
postal_code,
email_address,
tax_id_type, and
tax_id fields on the Accounts API:
The space character, denoted by ASCII character 32, will be the only whitespace character we accept

Leading and trailing spaces present in the string will return a 422 error

Additionally, we will be cleaning up the existing accounts in our system that contain invalid whitespace characters. We will follow up directly with the affected partners and share the complete list of accounts and data points that we will be updating.

Updated4 days ago
Domestic (USA) AccountsIRA Accounts OverviewAsk AI
