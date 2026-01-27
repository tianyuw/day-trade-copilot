---
source: https://docs.alpaca.markets/docs/margin-and-short-selling
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

Margin and Short Selling
In order to trade on margin or sell short, you must have $2,000 or more account equity. Accounts with less than $2,000 will not have access to these features and will be restricted to 1x buying power.

This is only for Equities Trading. Margin Trading for Crypto is not applicable. In addition, PDT checks do not count towards crypto orders or fills.

How Margin Works
Trading on margin allows you to trade and hold securities with a value that exceeds your account equity. This is made possible by funds loaned to you by your broker, who uses your account’s cash and securities as collateral. For example, a Reg T Margin Account holding $10,000 cash may purchase and hold up to $20,000 in marginable securities overnight (Note: some securities may have a higher maintenance margin requirement making the full 2x overnight buying power effectively unavailable). In addition to the 2x buying power afforded to margin accounts, a Reg T Margin Account flagged as a Pattern Day Trader(PDT) with $25,000 or greater equity will further be allowed to use up to 4x intraday buying power. As an example, a PDT account holding $50,000 cash may purchase and hold up to $200,000 in securities intraday; however, to avoid receiving a margin call the next morning, the securities held would need to be reduced to $100,000 or less depending on the maintenance margin requirement by the end of the day.

Initial Margin
Initial margin denotes the percentage of the trade price of a security or basket of securities that an account holder must pay for with available cash in the margin account, additions to cash in the margin account or other marginable securities.

Alpaca applies a minimum initial margin requirement of 50% for marginable securities and 100% for non-marginable securities per Regulation T of the Federal Reserve Board.

Maintenance Margin
Maintenance margin is the amount of cash or marginable securities required to continue holding an open position. FINRA has set the minimum maintenance requirement to at least 25% of the total market value of the securities, but brokers are free to set higher requirements as part of their risk management.

Alpaca uses the following table to calculate the overnight maintenance margin applied to each security held in an account:
Position SideConditionMargin RequirementLONGshare price < $2.50100% of EOD market valueLONGshare price >= $2.5030% of EOD market valueLONG2x Leveraged ETF50% of EOD market valueLONG3x Leveraged ETF75% of EOD market valueSHORTshare price < $5.00Greater of $2.50/share or 100%SHORTshare price >= $5.00Greater of $5.00/share or 30%
Margin Calls
If your account does not satisfy its initial and maintenance margin requirements at the end of the day, you will receive a margin call the following morning. We will contact you and advise you of the call amount that you will need to satisfy either by depositing new funds or liquidating some or all of your positions to reduce your margin requirement sufficiently.

We may contact you prior to the end of the day and ask you to liquidate your positions immediately in the event that your account equity is materially below your maintenance requirement. Furthermore, although we will make every effort to contact you so that you can determine how to best resolve your margin call, we reserve the right to liquidate your holdings in the event we cannot get ahold of you and your account equity is in danger of turning negative.

Calculating and tracking your margin requirement at all times is helpful to avoid receiving a margin call. We strongly recommend doing so if you plan to aggressively use overnight leverage. Please use a 50% initial requirement and refer to the maintenance margin table above. In the future, we will provide real-time estimated initial and maintenance margin values as part of the Account API to help users better manage their risk.

Margin Interest Rate
We are pleased to offer a competitive and low annual margin interest rate of 4.75% for elite users and 6.25% for non-elite users (check “Alpaca Securities Brokerage Fee Schedule” on Important Disclosures for the latest rate).

The rate is charged only on your account’s end of day (overnight) debit balance using the following calculation:

daily_margin_interest_charge = (settlement_date_debit_balance * rate[non-elite: 0.0625 | elite: 0.0475])) / 360

Interest will accrue daily and post to your account at the end of each month. Note that if you have a settlement date debit balance as of the end of day Friday, you will incur interest charges for 3 days (Fri, Sat, Sun).

As an example, if you are a regular trader and deposited $10,000 into your account and bought $15,000 worth of securities that you held at the end of the day, you would be borrowing $5,000 overnight and would incur a daily interest expense of ($5000 * 0.0625) / 360 = $0.87.

On the other hand, if you deposited $10,000 and bought $15,000 worth of stock that you liquidated the same day, you would not incur any interest expense. In other words, this allows you to make use of the additional buying power for intraday trading without any cost.

Stock Borrow Rates
Alpaca currently only supports opening short positions in easy to borrow (“ETB”) securities. Any open short order in a stock that changes from ETB to hard to borrow (“HTB”) overnight will be automatically cancelled prior to market open.

Note: Support for HTB securities is not yet available, but we are actively working towards supporting HTB in the future.

In addition, Alpaca has introduced $0 borrow fees on all ETB (easy-to-borrow) shares for Trading API users.

Please note that stock borrow availability changes daily, and we update our assets table each morning, so please use our API to check each stock’s borrow status daily. It is infrequent but names can go from ETB → HTB and vice versa.
While we do not currently support opening short positions in HTB securities, we will not force you to close out a position in a stock that has gone from ETB to HTB unless the lender has called the stock. If a stock you hold short has gone from ETB to HTB, you will incur a daily stock borrow fee for that stock. We do not currently provide HTB rates via our API, so please contact us in these cases.

If you hold an HTB short at any time during the day, you will incur a daily stock borrow fee:

Daily stock borrow fee = Daily HTB stock borrow fee

Where,

Daily HTB stock borrow fee = Σ((each stock’s HTB short $ market value _ that stock’s HTB rate) / 360)

Please note that if you hold HTB short positions as of a Friday settlement date, you will incur stock borrow fees for 3 days (Fri, Sat, Sun). HTB stock borrow fees are charged in the nearest round lot (100 shares), regardless of the actual number of shares shorted. This is because stocks are borrowed in round lots.

Concentrated Margin Requirements
Accounts concentrated into a single position will see an increased maintenance margin rate on the symbol in which the account is concentrated.

Concentration is defined as a single security accounting for 70% of the market value of equities and the account is carrying a margin balance of $100,000 or more.

The Maintenance Margin Rate on the concentrated position will increase to 50%.

Margin trading involves significant risk and is not suitable for all investors. Before considering a margin loan, it is crucial that you carefully consider how borrowing fits with your investment objectives and risk tolerance.
When trading on margin, you assume higher market risk, and potential losses can exceed the collateral value in your account. Alpaca may sell any securities in your account, without prior notice, to satisfy a margin call. Alpaca may also change its “house” maintenance margin requirements at any time without advance written notice. You are not entitled to an extension of time on a margin call. Please review the Firm’s Margin Disclosure Statement before investing.

Updated4 days ago
Fractional TradingPlacing OrdersAsk AI
