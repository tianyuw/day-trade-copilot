---
source: https://docs.alpaca.markets/docs/funding-accounts
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

Funding Accounts
The funding process can vary depending on your setup and region and we support many cases, but everyone can do the same in the sandbox environment.

Sandbox Funding
In the sandbox environment, Transfer API simulates deposits and withdrawals to/from an account. The target account is immediately credited or debited upon such a request. Once an account is credited, the account can start trading with the Orders API.

ACH (US Domestic)
For US ACH, you will need to use Plaid to obtain the user’s bank account information. You then pass the information to Alpaca using ACH API to create a Bank Link object. Once a Bank Link between a user and their bank account is established, then you can initiate both deposit and withdrawal transactions using the Transfers API.

Wire
Beginning June 1, 2022, we will begin charging for outgoing wires, both domestic and international. To help you provide the optimal customer experience we support two different flows for handling the fees:

The end user pays the fee for every outgoing wire transfer that they initiate. The
fee_payment_method field will be equal to user in this case. It’s important to note that the fee stated in your contract with Alpaca will automatically be deducted from the amount entered via the Transfers API so we strongly recommend adding a notice to your UI stating that the end user will incur a fee and they should incorporate that fee into their withdrawal request.

You will also have the option to pay the fee on behalf of your user for any given transfer. When creating the transfer, you will have to set the
fee_payment_method field to invoice. The fee stated in your contract will not be deducted from the amount entered via the Transfers API but you will be charged this fee in your next monthly invoice.

Wire (US Domestic)
You can initiate a withdrawal transaction with wire transfer using the Transfers API. You need to create a bank object before that. For US domestic wire transactions, we will need ABA/routing number and the account number. You can supply additional text in each transaction.

In order for us to receive the deposits and book automatically, we need an “FFC” instruction in each incoming wire transaction. Please contact us for more details.

International Wire (SWIFT)
Alpaca supports international wire transfers and the API endpoint is the same as the US domestic case. You need to provide the SWIFT code and account number of the beneficiary, as well as the address and name of the receiving bank.

The FFC instructions above work for international wires too.

Cash Pooling
If you wish and are eligible, you can send customer deposits in a bulk to your firm account first and reconcile later using the Journals API.

We need to review the entire flow first to allow you to do so, and also you may need a local license to implement this process. Please check your counsel for the local requirements.

Travel Rule
In an effort to fight the criminal financial transactions, FinCEN enacted the Travel Rule, which mandates that financial institutions transmitting funds more than $3,000 must share specific information with the recipient institutions. FAFT further adopted this from FinCEN to set the global standard, to regulate financial institutions including virtual asset service providers (VASPs) and is being implemented by many countries. However, Alpaca requires adherence to this policy for all incoming deposits, regardless of amount.

Under this rule, financial institutions that transmit the funds are required to submit the following information to the recipient financial institutions (financial institutions here include banks and nonbanks; essentially any party that initiates the transfers).

When using the following APIs, you will need to ensure compliance with the Travel Rule by including breakdowns and transmitter information where applicable.

Journals API
Create a Journal

Instant Funding API - There are two APIs under instant funding that accept transmitter information, the recommendation is to pass the information at the time of settlement creation.
Create an intant funding request

Create a new settlement

The table given below gives an overview of the relevant fields for both the APIs along with the field descriptions.

Journals

Instant Funding

Field description

transmitter_name

originator_full_name

The full name of the customer who is initiating the transaction.

transmitter_account_number

originator_bank_account_number

The bank account number of the customer or the account number on broker partner's system that can be used to uniquely identify the customer.

transmitter_address

originator_street_address

originator_state

originator_city

originator_country

The street, city, state and country of the financial institution responsible for transmitting the funds.

transmitter_financial_institution

originator_bank_name

The name of the transmitter's financial institution

other_identifying_information

Recommended to be the originating bank's reference number for the transfer

Please note that the purpose of this requirement is for the investigators to track the flow of funds in case they need to. Failure to do so could cause a civil enforcement.

Alpaca retains the collected information for at least five years. If the journal activities are used as part of the money transfer (other than cash movement within Alpaca), and if the journal requests don’t contain the transmitter information, we may contact you.

Instant Deposit (Beta)
As international money transfers can take days usually, under certain conditions, Alpaca supports instant deposit for better user experience. Please contact us for more details.

Post-trade Settlement
We support the post-trade settlement process (higher requirements and restrictions apply). Please contact us for more details.

Updated4 days ago
Crypto Wallets APIJournals APIAsk AI
