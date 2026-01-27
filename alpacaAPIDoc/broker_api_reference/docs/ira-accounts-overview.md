---
source: https://docs.alpaca.markets/docs/ira-accounts-overview
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

IRA Accounts Overview
Individual Retirement Arrangement (IRA) accounts are a retirement account type available to US tax residents. Alpaca supports both Roth IRA and Traditional IRA accounts for our Broker API customers. This page serves as a guide to understanding IRA accounts at Alpaca and how to integrate them into your application. Please note IRA accounts have to be enabled for your account to begin creating them. Please reach out to Alpaca support to enable this feature for you in sandbox.

Account Opening
The existing account creation request will be used to create an IRA account but with the addition of a few new fields such as the
account_type and
account_sub_type fields. There will also be some additional onboarding questions that customers must answer to create their IRA account. Please reach out to your dedicated Customer Success Manager for the complete onboarding steps you'll need to guide your customers through.

Sample Request Body

{
 "account_type": "ira",
 "account_sub_type": "roth",
 "enabled_assets": ["us_equity"],
 "contact": {
 "email_address": "[email protected]",
 "phone_number": "555-666-7788",
 "street_address": ["20 N San Mateo Dr"],
 "unit": "6G",
 "city": "San Mateo",
 "state": "CA",
 "postal_code": "12345"
 },
 "identity": {
 "given_name": "John",
 "family_name": "Smith",
 "date_of_birth": "1940-01-01",
 "tax_id": "119119119",
 "tax_id_type": "USA_SSN",
 "country_of_citizenship": "USA",
 "country_of_tax_residence": "USA",
 "funding_source": ["employment_income"],
 "annual_income_min": "30000",
 "annual_income_max": "50000",
 "liquid_net_worth_min": "100000",
 "liquid_net_worth_max": "150000",
 "marital_status": "MARRIED"
 },
 "disclosures": {
 "is_control_person": false,
 "is_affiliated_exchange_or_finra": false,
 "is_politically_exposed": false,
 "immediate_family_exposed": false,
 "employment_status": "retired"
 },
 "agreements": [
 {
 "agreement": "customer_agreement",
 "signed_at": "2020-09-11T18:13:44Z",
 "ip_address": "185.13.21.99",
 "revision": "19.2022.02"
 }
 ],
 "beneficiaries": [
 {
 "given_name": "Jane",
 "middle_name": "middle",
 "family_name": "Smith",
 "date_of_birth": "1940-01-01",
 "tax_id": "119119119",
 "tax_id_type": "USA_SSN",
 "relationship": "spouse",
 "type": "primary",
 "share_pct": "33.34"
 },
 {
 "given_name": "John",
 "family_name": "Smith",
 "date_of_birth": "2000-01-01",
 "tax_id": "119119119",
 "tax_id_type": "USA_SSN",
 "relationship": "other",
 "type": "primary",
 "share_pct": "33.33"
 },
 {
 "given_name": "Sally",
 "family_name": "Smith",
 "date_of_birth": "2000-01-01",
 "tax_id": "119119119",
 "tax_id_type": "USA_SSN",
 "relationship": "other",
 "type": "primary",
 "share_pct": "33.33"
 }
 ]
}
Same user opening a taxable brokerage account and an IRA account
If the accounts are opened within 60 days of each other and Alpaca is performing KYC on each customer then we will reuse the KYC results tied to the account opened first provided that the original account was already approved. This means that you will only be charged for one KYC run from an invoicing perspective if these conditions are met. Please note this functionality has to be explicitly enabled for you so please reach out to Alpaca support to enable this feature to begin testing.

Regardless of the time that has passed since the user opened their first account, the user does not have to go through the full onboarding flow again. You can pre-populate the onboarding questions with their original answers, prompt the user to confirm information is still correct and allow them to modify any fields that need to be corrected, and present the user with the relevant account agreement and disclosure language to finish opening their second account.

Modifying Beneficiaries After Account Creation
Beneficiaries are especially important for IRA accounts since they are meant to be used to generate savings over a long period of time. However, to ensure a smooth onboarding experience, specifying beneficiaries at the time of account opening is not required. Beneficiaries can be set or updated anytime after account creation. This function would be managed via the existing account update endpoint.
🚧
Important note: updating beneficiaries via this endpoint will replace ALL existing beneficiaries associated with the IRA account.
Sample Request Body

{
 "beneficiaries": [
 {
 "given_name": "Jane",
 "middle_name": "middle",
 "family_name": "Smith",
 "date_of_birth": "1940-01-01",
 "tax_id": "119119119",
 "tax_id_type": "USA_SSN",
 "relationship": "spouse",
 "type": "primary",
 "share_pct": "50"
 },
 {
 "given_name": "Sally",
 "family_name": "Smith",
 "date_of_birth": "2000-01-01",
 "tax_id": "119119119",
 "tax_id_type": "USA_SSN",
 "relationship": "other",
 "type": "primary",
 "share_pct": "50"
 }
 ]
}
Spousal Consent in Community States
Please note that Alpaca is required to collect spousal consent in the event that a user has an IRA account, is married, does not list their spouse as a beneficiary, and resides in a community property state. The community property states as of October 2024 are Arizona, California, Idaho, Louisiana, Nevada, New Mexico, Texas, Washington, and Wisconsin. Alpaca will reach out to you with a list of accounts we are required to collect spousal consent on a manual basis as needed.

How to Process a Contribution (IRA Deposits)
Deposits to IRA accounts are considered contributions from the IRS’ perspective and Alpaca needs to collect additional data that isn't required for typical taxable brokerage accounts. The IRS sets specific contribution limits for how much a customer can deposit into their IRA account per tax year and allows contributions to the previous tax year up until the official deadline of April 15th.

Given this, Alpaca will require "tax_year" as an input parameter when depositing via ACH using our existing request transfer endpoint. If a deposit is made via a push transaction, (i.e. a wire deposit or an ACH push transaction), the system will automatically default to classify the contribution for the current tax year.

Sample Request Body

{
 "transfer_type": "ach",
 "relationship_id": "99eeed85-dcca-4d4b-b3ed-42d597a2f96d",
 "amount": "7000",
 "direction": "INCOMING",
 "ira": {
 "tax_year": "2024"
 }
}
Handling Excess Contributions
As mentioned above, the IRS imposes specific limits on how much a customer can contribute to their IRA in a given tax year. If a customer exceeds this limit, they may incur penalties during tax season. It’s advisable to monitor whether your customers are adhering to these IRS limits and, if not, send them a courtesy notice, guiding them to withdraw the excess funds to avoid penalties.

Alpaca simplifies this process by providing a new endpoint that allows you to pull the list of accounts that have over contributed on demand. It’s important to note that the exact limit the IRS enforces for each individual will change depending on their income bracket, tax filing status, and age – Alpaca only monitors against the maximum allowed limit by age. Since the contribution limit applies to all IRAs, including those held at other brokerages, customers are ultimately responsible for monitoring their own limits. Providing a notification to your customers as a courtesy is recommended but not required.

How to Process a Distribution (IRA Withdrawals)
Withdrawals from IRA accounts are considered distributions from the IRS’ perspective. Since these are designed for long term savings and retirement, there are several IRS rules that disincentivize individuals from withdrawing from an IRA account before they reach retirement age but there are limited exceptions that allow users to withdraw penalty free.

Because of this, the IRS requires we provide a reason for each distribution which must be collected from your end customer. There are also federal and state tax withholding elections that the customer must specify when requesting a distribution. As a guideline, the IRS requires 10% federal tax withholding unless the customer explicitly opts out. US state withholding requirements vary, so state-specific guidelines should be followed. Alpaca will withhold the elected amount (by deducting from the requested withdrawal amount) and remit payment to the IRS. Distributions will be processed via the existing withdrawal request endpoint.

Sample Request Body

{
 "transfer_type": "ach",
 "relationship_id": "1b6bb433-3ce3-40fa-8e08-15164a408c6b",
 "amount": "143",
 "direction": "OUTGOING",
 "ira": {
 "distribution_reason": "normal_roth",
 "tax_withholding": {
 "fed_pct": "10",
 "state_pct": "5.5"
 }
 }
}
DistributionReason ENUMs
We highly recommend researching when each tax code would be used for a given scenario and designing your frontend flow in a way that helps the user easily identify the correct reason to use. A brief description of each distribution reason Alpaca will support is provided below but the IRS guidelines should be considered the source of truth on this. Please also note that Alpaca will not support all IRA distribution types. If there is another distribution reason the user is eligible for (i.e. a disability distribution) the user would have to take an early distribution from Alpaca and work directly with the IRS to be reimbursed for any penalties that they may have incurred during tax season.
AttributeDescriptionApplicable for Traditional IRAsApplicable for Roth IRAsIRS Tax Code
normalNormal DistributionX7
normal_rothQualified distribution from a Roth IRA (IRA 5-year holding period has been reached and customer is over 59½, or is dead, or is disabled)XQ
early_no_exceptionEarly distribution, no known exceptionX1
excess_removal_current_yearExcess contributions plus earnings/excess deferrals (and/or earnings) taxable in current yearX8
excess_removal_current_year_under_59.5Removal of Excess Plus Earning/Excess Deferrals Taxable in current yr - < 59.5X81
excess_removal_rothRemoval of Excess from a Roth IRAX8J
excess_removal_1_year_prior_rothExcess contributions plus earnings in prior year - Roth IRAXPJ
excess_removal_1_year_prior_over_59.5Removal of Excess Plus Earning/Excess Deferrals Taxable in prior year - >59½XP
excess_removal_1_year_prior_under_59.5Removal of Excess Plus Earning/Excess Deferrals Taxable in prior year - <59½XP1
early_roth_no_exceptionEarly distribution from a Roth IRA, no known exception (when Code T or Code Q do not apply)XJ
Other Important Considerations
Tax Documents & Required Minimum Distribution (RMD) Notices
For IRA accounts, the primary documents provided will be tax statements and RMD notices for customers who are of RMD age. These documents will be attached to the account as an account document and available for download via the existing Broker API endpoint.

Updating Contributions and Distributions
There may be instances where a customer needs to make a correction on a contribution or distribution from time to time. For example, if a customer made a wire deposit and could not specify the tax year for the contribution – as a result, they might want to apply it to the prior tax year vs current. For these types of cases, it’s recommended that you reach out to [email protected] to handle each correction on a case by case basis.

Pricing
Please reach out to your sales representative to inquire about IRA pricing for your use case. You will need to sign a pricing amendment if the pricing is not outlined in your initial contract with Alpaca before the product can be enabled for you in production.

Notable Product Limitations
RMD amount calculations will not be offered by Alpaca

There is currently a limitation of 1 unique email address per user

IRA accounts are by default setup with limited margin (1x margin)

Crypto is not be supported for IRAs at this time

Options (up to level 2) is supported for IRAs

IRA transfers and rollovers and not yet supported at Alpaca

Currently the API does not allow transfers between a customers' taxable account and their IRA account

Resources
IRA Blog Post

IRA FAQs

IRA Learn Article

Updated4 days ago
Data ValidationsCrypto TradingAsk AI
