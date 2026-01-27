---
source: https://docs.alpaca.markets/docs/authentication
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

Authentication
How to call our API
Alpaca's APIs are available under different domain names, and you first need to make sure that you are calling the right one. This page describes the machine-to-machine authentication types available in the following scenarios:

If you have a live account, you can call:
Trading API endpoints on
api.alpaca.markets

Market Data API endpoints on
data.alpaca.markets

If you have a paper account, you can call:
Trading API endpoints on
paper-api.alpaca.markets

Market Data API endpoints on
data.alpaca.markets

If you are a live broker partner, you can call:
Broker API endpoints on
broker-api.alpaca.markets

Market Data API endpoints on
data.alpaca.markets

Authentication endpoints on
authx.alpaca.markets

If you are a sandbox broker partner, you can call:
Broker API endpoints on
broker-api.sandbox.alpaca.markets

Market Data API endpoints on
data.sandbox.alpaca.markets

Authentication endpoints on
authx.sandbox.alpaca.markets

If you have more than one account (or in case of broker partners, more than one correspondent), each of those have separate credentials. As an example, you cannot use your live account's credentials with the paper API, or vice versa.

Authentication flows
Client credentials🚧
The Client Credentials authentication flow is not yet available for Trading API.

When using this flow, you first need to exchange your credentials for a short-lived access token, then use that token to authenticate with our API. Do not request a new access token for each API call. Access tokens issued by our token endpoint are valid for 15 minutes.

We offer two types of credentials you can use with this flow:

Use a client ID and a client secret (
client_secret) - this is easier, as you can simply pass the secret that was generated when you created your credentials to our token endpoint. Note that we only support passing the client secret in the request body (
client_secret_post), not in the
Authorization header (
client_secret_basic).

Use a client ID and a signed client assertion (
private_key_jwt) - this ensures that the private key used to sign client assertions never leaves your custody, but it requires you to construct and sign a JWT token with a private key before each call to the token endpoint. See RFC 7523 for more information on how to do so.

As an example, here is how a Broker API user would request an access token from our token endpoint using the first method:
cURL

curl -X POST "https://authx.alpaca.markets/v1/oauth2/token" \
 -H "Content-Type: application/x-www-form-urlencoded" \
 -d "grant_type=client_credentials" \
 -d "client_id={YOUR_CLIENT_ID}" \
 -d "client_secret={YOUR_CLIENT_SECRET}"
The response will contain an access token:
JSON

{
 "access_token": "{TOKEN}",
 "expires_in": 899,
 "token_type": "Bearer"
}
The returned token can be used to authenticate with Broker API:
cURL

curl -X GET "https://broker-api.alpaca.markets/v1/accounts" \
 -H "Authorization: Bearer {TOKEN}"
Legacy
Our older authentication flow lets you authenticate with your key ID and secret key directly. You have two options to authenticate your requests:

Use HTTP Basic Authentication, send your key ID as the username, and your secret key as the password.

Use the
APCA-API-KEY-ID and
APCA-API-SECRET-KEY headers to send your key ID and secret key.

As an example, here is how a Trading API user would authenticate with our API using the second method:
cURL

curl -X GET "https://api.alpaca.markets/v2/account" \
 -H "APCA-API-KEY-ID: {YOUR_API_KEY_ID}" \
 -H "APCA-API-SECRET-KEY: {YOUR_API_SECRET_KEY}"

Updated4 days ago
Alpaca API PlatformSDKs and ToolsAsk AI
