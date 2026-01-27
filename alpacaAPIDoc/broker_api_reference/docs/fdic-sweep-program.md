---
source: https://docs.alpaca.markets/docs/fdic-sweep-program
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

FDIC Sweep Program
What is an FDIC Sweep program?
An FDIC Bank Sweep Program, is an insured deposit program that allows customers who opt-in to earn interest on eligible cash balances and offers expanded FDIC insurance coverage on those cash balances*.

How does FDIC sweep work?
Through the Alpaca FDIC Bank Sweep Program, eligible uninvested cash in a customer brokerage account can be swept to one or more of the participating FDIC Sweep Program Banks, where the swept cash becomes eligible for FDIC insurance up to a total maximum of $1,000,000 (FDIC insurance coverage is limited to $250,000 at each program bank)*.

How much is insured?
Currently FDIC insurance up to a total maximum of $1,000,000 (FDIC insurance coverage is limited to $250,000 at each program bank)*.

What are the eligibility requirements?
Partners must be using a fully disclosed structure (not available to Partners with an omnibus structure at launch).

A customer must elect to opt-in their account into the program:
Existing: Customers with an existing Alpaca account that have signed a Customer Agreement before August 21, 2024 (prior to revision 22.2024.08) must provide opt-in consent by signing the updated Customer Agreement and be presented the Alpaca FDIC Bank Sweep Program Terms and Conditions on your front-end. Our Tech Integration team will help walk you through that process and the requirements.
New: Those who signed the Customer Agreement on or after August 21, 2024 (revision 22.2024.08 or newer) are automatically eligible to be enrolled.

The customer account is not flagged as a pattern day trader (PDT).

If an account is flagged as a PDT while enrolled in the FDIC Bank Sweep Program, it will be unenrolled from the program, and its sweep balance will be swept back from the program. Any accrued interest due will be paid, but no additional interest will be accrued unless the PDT flag is removed and the account is re-enrolled in the program by assigning an APR Tier.

The customer account has a base currency of USD.

The customer account is pre-funded (i.e., non-JIT).

How does a user enroll?
Please see our blog article Getting Started with High-Yield Cash for Broker API

How can a user opt-out of the FDIC Sweep Program?
To opt-out a user from the Alpaca FDIC Bank Sweep Program, please email [email protected].

What account types are supported?
We are currently supporting Individual Taxable and Custodial accounts at this time.

What are the benefits of a user enrolling?
Income: Earn interest on eligible cash balances
Security: Up to $1m FDIC insurance* per customer via FDIC Bank Sweep
Liquidity: Daily liquid, and available for use as buying power for trading activities

https://alpaca.markets/blog/alpacas-global-high-yield-cash-api/

How does a user withdraw funds from the program?
Customers are unable to withdraw directly from the program banks. Customers must therefore, request a withdrawal or transfer on the partner’s front-end the same way it’s implemented today, for which the corresponding cash will be swept out of the program to cover the request.

How can a user opt out of a specific bank in the program?
Currently, clients must opt out of the entire program by unenrolling. In an upcoming release, we aim to offer the ability to opt-out at the individual program bank level.

How frequently does interest accrue?
Daily

How often is interest compounded?
Monthly

When is interest available?
Last business day of the month. The accrued interest is booked to the customer account, but remains within the program to compound into yield.

What decimal is interest rounded to?
Daily accrued interest is rounded to 4 decimals, while month-end realized interest is rounded to 2 decimals

When can cash be swept into and out of the program?
Daily, excluding US weekends and holidays

Is the APR/APY fixed or variable?
The Program Rate is variable and subject to change without notice.

How can I access the FDIC Bank Sweep Program Deposit Bank List?
Deposit Bank List

Is there more detailed information available?**
Alpaca Securities LLC FDIC Bank Sweep Program Terms and Conditions

What are the key timing considerations to be mindful of?
11:45 am ET

-The cutoff for when a deposit can be settled and swept into the program same-day for accounts with cash_interest.status = ACTIVE.
-The cutoff for when a partial withdrawal request can be facilitated out of the program.
-The cutoff for when an Assignment API request will process the same-day.
-The cutoff for when a Reassignment API request will process the same-day.
-The cutoff for when an Unenroll API request will process the same-day.

12:15 pm - 2:00 pm ET

When cash_interest.status updates cycle from PENDING_CHANGE to ACTIVE or INACTIVE.

6:00 pm ET

When the Account Activities endpoint is updated to reflect realized interest credited to accounts on the last business day of the month. The qty will be reflected within that day’s cash_interest value from the EOD Cash Interest Details response.

8:00 pm ET

When the EOD Cash Interest Details endpoint is updated to reflect that day’s ending state.

*Alpaca Securities customers that enroll in the FDIC Bank Sweep are potentially eligible for enhanced FDIC pass-through insurance coverage. Neither Alpaca nor Alpaca Securities are FDIC-insured. FDIC pass-through insurance coverage is subject to various conditions. The Program’s enhanced FDIC insurance coverage is limited to the aggregate number of participating program banks, multiplied by the FDIC insurance limit (i.e., $250,000). The total number of program banks is subject to change and Alpaca Securities may not utilize all program banks at all times which will affect the Program’s enhanced FDIC insurance coverage amount. In addition, if a customer has a direct banking relationship with a program bank this may affect the amount of funds that are potentially eligible for FDIC-pass through insurance coverage. There is no guarantee that customer funds will be held in such a manner as to maximize possible FDIC pass-through insurance coverage.

Neither Alpaca, nor any of its affiliates or subsidiaries is a bank.

Alpaca Securities offers a cash management program pursuant to the FDIC Bank Sweep. Customer funds are treated differently and are subject to separate regulatory regimes depending on whether customer funds are held in their brokerage account or within the FDIC Bank Sweep. Specifically, Alpaca Securities is a member of the Securities Investor Protection Corporation (SIPC), which protects securities customers of its members up to $500,000 (including $250,000 for claims for cash). The Federal Deposit Insurance Corporation (FDIC) insures up to $250,000 per deposit against the failure of an FDIC member bank. Customer funds held in brokerage accounts are SIPC insured, but are not eligible for FDIC insurance coverage. Funds maintained in the FDIC Bank Sweep are intended to be eligible for pass-through FDIC insurance coverage, but are not subject to SIPC coverage. FDIC insurance coverage does not protect against the failure of Alpaca, Alpaca Securities, or any of its or their affiliates and/or malfeasance by any Alpaca or Alpaca Securities employee. Program banks that participate in the FDIC Bank Sweep are not members of SIPC and therefore funds held in the Program are not SIPC protected. Please see alpaca.markets/disclosures for important additional disclosures regarding Alpaca Securities brokerage offering as well as FDIC Bank Sweep terms and conditions.

Updated4 days ago
Voluntary Corporate ActionsInstant FundingAsk AI
