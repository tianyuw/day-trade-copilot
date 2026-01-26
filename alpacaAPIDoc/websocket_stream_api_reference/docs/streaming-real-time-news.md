---
source: https://docs.alpaca.markets/docs/streaming-real-time-news
scraped_at_utc: 2026-01-26T01:09:58Z
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

Real-time News
This API provides stock market news on a websocket stream. You can find the general description of the real-time WebSocket Stream here. This page focuses on the news stream.

URL
The URL for the news stream is

wss://stream.data.alpaca.markets/v1beta1/news
Sandbox URL:

wss://stream.data.sandbox.alpaca.markets/v1beta1/news
Channels
News
SchemaAttributeTypeNotesTstringType of message (“n” for news)idintNews article IDheadlinestringHeadline or title of the articlesummarystringSummary text for article (may be first sentence of content)authorstringOriginal author of news articlecreated_atstringDate article was created in RFC-3339 formatupdated_atstringDate article was updated in RFC-3339 formatcontentstringContent of news article (might contain HTML)urlstringURL of article (if applicable)symbolsarray
<string>List of related or mentioned symbolssourcestringSource where the news originated from (e.g. Benzinga)
ExampleJSON

{
 "T": "n",
 "id": 24918784,
 "headline": "Corsair Reports Purchase Of Majority Ownership In iDisplay, No Terms Disclosed",
 "summary": "Corsair Gaming, Inc. (NASDAQ:CRSR) (“Corsair”), a leading global provider and innovator of high-performance gear for gamers and content creators, today announced that it acquired a 51% stake in iDisplay",
 "author": "Benzinga Newsdesk",
 "created_at": "2022-01-05T22:00:37Z",
 "updated_at": "2022-01-05T22:00:38Z",
 "url": "https://www.benzinga.com/m-a/22/01/24918784/corsair-reports-purchase-of-majority-ownership-in-idisplay-no-terms-disclosed",
 "content": "\u003cp\u003eCorsair Gaming, Inc. (NASDAQ:\u003ca class=\"ticker\" href=\"https://www.benzinga.com/stock/CRSR#NASDAQ\"\u003eCRSR\u003c/a\u003e) (\u0026ldquo;Corsair\u0026rdquo;), a leading global ...",
 "symbols": ["CRSR"],
 "source": "benzinga"
}
ExampleJSON

$ websocat -H="APCA-API-KEY-ID: ${APCA_API_KEY_ID}" -H="APCA-API-SECRET-KEY: ${APCA_API_SECRET_KEY}" \
 "${APCA_API_STREAM_URL}/v1beta1/news"
[{"T":"success","msg":"connected"}]
[{"T":"success","msg":"authenticated"}]
{"action":"subscribe","news":["*"]}
[{"T":"subscription","news":["*"]}]
[{"T":"n","id":40892639,"headline":"VinFast Officially Launches VF 3 Electric Vehicle In The Philippines","summary":"VinFast Auto has officially opened pre-orders for the VF 3 in the Philippines. From September 19 to 30, early customers who reserve the VF 3 will enjoy several attractive incentives and privileges, including a","author":"Benzinga Newsdesk","created_at":"2024-09-17T09:02:44Z","updated_at":"2024-09-17T09:02:45Z","url":"https://www.benzinga.com/news/24/09/40892639/vinfast-officially-launches-vf-3-electric-vehicle-in-the-philippines","content":"\u003cp\u003eVinFast Auto has officially opened pre-orders for the VF 3 in the Philippines.\u003c/p\u003e\u003cp\u003e\u0026nbsp;\u003c/p\u003e\u003cp\u003eFrom September 19 to 30, early customers who reserve the VF 3 will enjoy several attractive incentives and privileges, including a special price of 605,000 pesos (battery subscription) or 705,000 pesos (battery included). After this period, the prices will revert to the MSRP of 645,000 pesos (battery subscription) and 745,000 pesos (battery included).\u003cbr\u003e\u003cbr\u003eAdditionally, early VF 3 customers will have the privilege of choosing from nine striking exterior paint colors, including four base colors and five premium options, free of charge. Premium paint colors will cost an additional 20,000 pesos after this period.\u003cbr\u003e\u003cbr\u003eMoreover, from September 19 to 30, for only 40,000 pesos, early customers can customize their car's paint beyond the nine available colors. This will be the only time VinFast offers this exclusive privilege for the VF 3.\u003cbr\u003e\u003cbr\u003eVinFast is accepting deposits of 5,000 pesos through its official website or at authorized dealerships (refundable under VinFast's terms).\u003cbr\u003e\u0026nbsp;\u003c/p\u003e","symbols":["VFS"],"source":"benzinga"}]
Updated3 days ago
Real-time Crypto DataReal-time Option DataAsk AI
