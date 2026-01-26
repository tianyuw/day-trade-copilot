---
source: https://docs.alpaca.markets/docs/about-market-data-api
scraped_at_utc: 2026-01-26T01:04:10Z
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

About Market Data API
Gain seamless access to a wealth of data with Alpaca Market Data API, offering real-time and historical information for equities, options, crypto and more.

Overview
The Market Data API offers seamless access to market data through both HTTP and WebSocket protocols. With a focus on historical and real-time data, developers can efficiently integrate these APIs into their applications.

To simplify the integration process, we provide user-friendly SDKs in Python, Go, NodeJS, and C#. These SDKs offer comprehensive functionalities, making it easier for developers to work with the Market Data APIs & Web Sockets.

To experiment with the APIs, developers can try them with Postman: either through the public workspace on Postman or directly from our GitHub repository.

By leveraging Alpaca Market Data API and its associated SDKs, developers can seamlessly incorporate historical and real-time market data into their applications, enabling them to build powerful and data-driven financial products.

Subscription Plans
For regular users we offer two subscription plans: Basic and Algo Trader Plus.

The Basic plan serves as the default option for both Paper and Live trading accounts, ensuring all users can access essential data with zero cost. However, this plan only includes limited real-time data: for equities only the IEX exchange, for options only the indicative feed. For advanced traders we recommend subscribing to Algo Trader Plus which includes complete market coverage for stocks and options as well.

EquitiesBasicAlgo Trader PlusPricingFree$99 / monthSecurities coverageUS Stocks & ETFsUS Stocks & ETFsReal-time market coverageIEXAll US Stock ExchangesWebsocket subscriptions30 symbolsUnlimitedHistorical data timeframeSince 2016Since 2016Historical data limitation*latest 15 minutesno restrictionHistorical API calls200 / min10,000 / min
Our data sources are directly fed by the CTA (Consolidated Tape Association), which is administered by NYSE (New York Stock Exchange), and the UTP (Unlisted Trading Privileges) stream, which is administered by Nasdaq. The synergy of these two sources ensures comprehensive market coverage, encompassing 100% of market volume.

OptionsBasicAlgo Trader PlusSecurities coverageUS Options SecuritiesUS Options SecuritiesReal-time market coverageIndicative Pricing FeedOPRA FeedWebsocket subscriptions200 quotes1000 quotesHistorical data limitation*latest 15 minutesno restrictionHistorical API calls200 / min10,000 / min
Our options data sources are directly fed by OPRA (Options Price Reporting Authority).

Broker partners
For equities, the below subscription plans are available.
Subscription NameRPM (Request Per Minute)Stream Connection LimitStream Symbol LimitPrice (per month)Options Indicative FeedStandard1,0005unlimitedincludedadditional $1,000 per monthStandardPlus30003,0005unlimited$500additional $1,000 per monthStandardPlus50005,0005unlimited$1,000includedStandardPlus1000010,00010unlimited$2,000included
*Note: Standard subscription plans will only be active when integration starts. Prior to that, the account will be on the Basic plan listed above. Additionally, similar to the free plan all the standard plans are real time IEX or 15 mins delayed SIP.

For partners on the Standard and StandardPlus3000 plans, an additional subscription fee of $1,000 / month enables access to the same equities plan for options. For StandardPlus5000 and StandardPlus10000 plans, options are included.

We offer custom pricing and tailored solutions for Broker API partners seeking to leverage our comprehensive market data. Our goal is to meet the specific needs and requirements of our valued partners, ensuring they have access to the data and tools necessary to enhance their services and provide exceptional value to their customers. If none of the subscription plans listed above are believed to be suitable, kindly reach out to our sales team.

Authentication
With the exception of historical crypto data, all market data endpoints require authentication. Authentication differs between the Trading & Broker API. API keys can be acquired in the web UI (under the API keys on the right sidebar).

Trading API
You should authenticate by passing the key / secret pair in the HTTP request headers named
APCA-API-KEY-ID and
APCA-API-SECRET-KEY, respectively.

Broker API
You should authenticate using HTTP Basic authentication. Use your correspondent API_KEY and API_SECRET as the username and password. The format is
key:secret. Encode the string with base-64 encoding, and you can pass it as an authentication header in the
Authorization header.

Note: For the WebSocket stream authentication, kindly refer to the WebSocket Stream documentation.

Updated3 days ago
Alpaca MCP ServerGetting Started with Market Data APIAsk AI
