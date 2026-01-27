---
source: https://docs.alpaca.markets/docs/account-status-events-for-kycaas
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

Account Status Events for KYCaaS
For partners who utilize Alpaca’s KYC service for opening brokerage accounts, if an account is moved to
ACTION_REQUIRED or
APPROVAL_PENDING then that indicates that additional action may be needed from you or your user to approve the account. These status updates, along with the reason for the status change, will be relayed in real time via the Account Status Events. The specific KYC results that may require action from your end user will wind up in
ACCEPT,
INDETERMINATE, or
REJECT. The
additional_information field will be used to relay custom messages from our account opening team. If a KYC result is returned via the
ACCEPT object then no further action is needed to resolve the request. KYC results returned in the
INDETERMINATE or
REJECT objects will require further action before the account can be opened. The following tables can be used to determine what is required from the account opener.

Documentation Required
KYC Result CodeGovernment Issued ID CardTax ID CardStatement (utility bill, etc.)Selfie
IDENTITY_VERIFICATIONREQUIRED
TAX_IDENTIFICATIONREQUIRED
ADDRESS_VERIFICATIONOPTIONALOPTIONAL
DATE_OF_BIRTHREQUIRED
SELFIE_VERIFICATIONREQUIRED
Additional Information Required
KYC Result CodeAdditional Information Required
PEPJob title / occupation and address
FAMILY_MEMBER_PEPName of politically exposed person if immediate family
CONTROL_PERSONCompany name, company address, and company email
AFFILIATEDCompany / firm name, company / firm address, company / firm email
VISA_TYPE_OTHERVisa type and expiration date
W8BEN_CORRECTIONAn updated W8BEN form with corrected information
OTHERFor specific cases our operational team might return with a customized message within the additional_information attribute.
Updated4 days ago
SSE EventsDaily Processes and ReconcilationsAsk AI
