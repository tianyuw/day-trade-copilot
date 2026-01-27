---
source: https://docs.alpaca.markets/docs/example-trading-app-ribbit
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

Example Trading App (Ribbit)
What is Ribbit?
Ribbit is a skeleton mobile app designed to showcase the capabilities of the Broker API. It’s a fully functional trading application that demonstrates how users would interact with your product. It uses all the different functionality that the Broker API offers including onboarding new users, funding an account, managing market data, and handling trade activity.

User Experience Example
The screenshots below demonstrate how a native user would walk through Ribbit to accomplish various tasks.

Create a New Account
Once Ribbit users sign up with their email and create a password, it triggers the brokerage account onboarding process to begin. The following screens prompt users to input their information such as name, date of birth, tax ID, and more information that is required by law to open a brokerage account. At the end of this process, Ribbit calls the Accounts API to submit all the information to Alpaca where we verify the information and approve the account application.

The app demonstrates a common flow that brokerage apps have to implement to collect all the necessary data points and required user agreements. For your own app, you may also be interested in performing various input checks on the client side so that the account approval process is as quick as possible. See below screenshots of the actual flow.

Once the account creation flow is completed, Ribbit continues to use the Accounts API to retrieve real-time information about the user’s account. The API can also be used to update the account information as well as request to close an account.

Beginning and end state of an account opening experience

Fund an Account
The next step for the new users is to deposit the money to start trading. Ribbit uses Plaid to validate the bank information so that Alpaca can simply link the bank account to the brokerage account. From the Plaid Link component, Ribbit receives the bank routing number and account number for the user and submits the bank link request using ACH Relationships.

As a demo app, Ribbit uses the Plaid sandbox which simulates the production environment behavior. When you try the app, use
user_good and
pass_good for the credentials with any banks shown in the app. Alpaca’s sandbox where Ribbit simulates the ACH transactions and the virtual money is credited in the user’s account in a moment.

Allowing your end users to connect to their personal bank and fund their account on your app can be intimidating if you aren’t familiar with the high level financial requirements and flows. Fortunately, our Bank, ACH Relationships, and Transfers APIs make it easy to achieve this! The Bank API lets you create, retrieve, and delete bank relationships between their personal bank and their account on your app. The ACH Relationships API deals with connecting, getting, and deleting your end user’s specific bank account that will be used to initiate and receive ACH transfers from your app. Finally, the Transfers API initiates, lists, and cancels the actual transfer initiated from your app on behalf of your end user. See how this flow is implemented from your user’s perspective below.

Example of a funding flow using Plaid

View and Execute Trades
When it comes to managing stock market data, Alpaca provides seamless integration via the Market Data API. Ribbit uses the historical data endpoint to draw the chart in the individual stock screen, and the real-time data endpoint to show the most up-to-date price information in the order screen. See how Ribbit makes use of the Market Data API below.

Typical screens for trading and portfolio

In the order screen, Ribbit uses the Orders API. It allows you to submit a new order, replace/cancel an open order, and retrieve a list of orders from a user’s history. Ribbit connects to Alpaca’s sandbox environment where an order execution simulator engine runs. This simulator will take the order you submitted on the backend and execute it using the real-time market price which makes it easy to test trading functionality before you launch your app to users.

Ribbit shows all the account activities using the Activities API which returns the relevant transaction history for a given account. As a trading app, some of the important requirements to deliver to your users are monthly statements and trade confirmations. Ribbit accomplishes this by using the Documents API. The documents are generated in PDF format by Alpaca so all you need to do is call the API to retrieve the list of downloadable URLs and show them in the app.

Architecture
The end user interacts with Ribbit’s UI to achieve a task while Ribbit’s backend processes the requests by making calls to Broker API. See the diagram below for an example of how the account creation process works.

The backend application serves as a thin layer to proxy the API requests coming from the mobile app but makes sure each request is authorized for the appropriate user.

Technology
The user interface is written in Swift for iOS and Java for Android. The backend is implemented using Go.

Alpaca APIs
All of the technology that is needed for users to interact with Ribbit’s core functionality is acheived through the Broker API. Accessing information related to the market is gathered using the Market Data API.
📘
Where Can I Access the Source Code?
The codebase is hosted on GitHub and separated into three different repositories for the implementation of the backend, iOS user interface, and Android user interface.

Updated4 days ago
Local Currency Trading (LCT)Options Trading OverviewAsk AI
