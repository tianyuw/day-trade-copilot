---
source: https://docs.alpaca.markets/docs/fully-paid-securities-lending
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

Fully Paid Securities Lending
What is the Alpaca Fully Paid Securities Lending Program?

Our program offers you the ability to earn additional income from the securities you already own by lending them to Alpaca, while you continue to retain full ownership. Once you activate Fully Paid Securities Lending, you'll receive monthly payments if we borrow your shares.

How does the program work?

Once enrolled in the program, Alpaca facilitates the lending of your eligible fully paid securities to borrowers, typically for short selling or trade settlements. These borrowers pay an interest rate based on current market conditions directly to Alpaca, and in turn, you will receive monthly interest payments based on the value of the loaned securities.

What are the benefits of enrolling in the program?

Lending your securities can provide you with additional income.
The income generated from securities lending can be reinvested into other opportunities, creating the potential for additional growth.
Lending your securities helps support market liquidity by enabling short sellers to execute their strategies, which can contribute to a more efficient market overall.
When you lend your securities, you maintain ownership of the underlying assets, allowing you to benefit from any potential appreciation or dividends, even while generating income from the loan.

What are the risks of enrolling in the program?

Risks:
There is no assurance that your securities will be lent or that a market for lending them exists.
When securities are borrowed for a short sale, there is a possibility that their market price will decline.
When you lend your securities, you will temporarily lose voting rights, as they are transferred to the borrower during the loan period.
Income earned from lending your securities may have tax consequences, which could affect your overall returns.
Securities lending is not protected by the Securities Investor Protection Corporation (SIPC), which means the loaned assets are not covered by SIPC.

What are the eligibility requirements?

One of the following criteria must be met in order to be eligible to participate.

$2,500 in account balance

$20,000 reported income

$20,000 in liquid assets

At least 1 year of trading experience

What account types are eligible for the program?

All account types with US equities that have been fully paid for or that are in excess of any margin debit.

What types of investments are eligible for the program?

All US equities that have been fully paid for or that are in excess of any margin debit will be eligible to loan

Can I choose which stocks to lend out?

You cannot choose specific stocks to lend. By enabling Fully Paid Securities Lending, all of your stocks, ADRs, and ETFs will be considered for lending.

Will Alpaca lend out all eligible shares?

There is no guarantee that all eligible shares in an account will be loaned through the Fully Paid Securities Lending Program. This may occur if there isn’t a favorable market rate for Alpaca to lend your shares.

How are lending rates determined?

Lending rates are determined by market conditions, based on the supply and demand for individual securities.

When is interest earned on lent securities paid out?

Monthly interest will be posted to your cash balance on the last settlement date of the following month.

What is the potential income from lending out securities?

When your securities are lent out, interest accumulates daily and is automatically credited to your account on a monthly basis. The interest you receive depends on the demand for the loaned shares. Here’s an example of how your earnings are calculated.

Shares on loan
2,000
Market price
$20
Market value
$40,000
Annualized lending interest rate
9.00%
Daily accrual ($40,000 x 9.00% / 360 days_)
$10.00
Your hypothetical monthly income
($10.00 x 30 days)
$300.00

Disclaimer: Interest accrual is based on a 360-day financial year, a standard billing practice. Actual earnings may vary.

Can I still sell a security while it is out on loan?

Yes, you can sell a security at any time. However, once the loan is closed, which may happen concurrently with the sale of the asset, you will no longer receive loan interest.

How will dividends be handled within the Securities Lending Fully Paid Program?

The borrower will be entitled to the dividend, and the customer will be entitled to a “payment-in-lieu” which will be a cash payment grossed up for the respective tax rate of the customer.

Will SIPC coverage be impacted?

The investments and cash in your Alpaca investing account are generally protected by SIPC insurance. However, stocks on loan are not covered by SIPC. Instead, cash collateral is used to safeguard your loaned stocks. We strive to maintain cash equivalent to at least 100% of the value of your loaned stocks at a third-party bank. In the event that Alpaca files for bankruptcy and is unable to return your stocks, this bank would compensate you in cash for the value of your loaned securities. Additionally, any cash held at this third-party bank would be covered under FDIC insurance, but only up to the $250,000 limit.

Will I continue to have voting rights for shares on loan?

Usually, company shareholders can exercise voting power on matters like new policy proposals, board appointments, or corporate actions. However, when your shares in a company are on loan, you will not have shareholder voting rights. However, you can unenroll from the program at any time to restore your voting rights.

How and where is the collateral held for loans in the Program?

Currently it is held in cash at our bank BMO. This is subject to change at a future date.

How does lending stock affect the calculation of my margin and excess liquidity?

Lending stock through the Fully Paid Securities Lending Program does not affect the calculation of your margin or excess liquidity. Your borrowing capacity remains determined by your stock positions.

Does the Fully Paid Securities Lending Program still provide benefits if I have written call options on my shares?

If the stock is fully paid, the Program will benefit you the same whether or not it has call options written against it.

What occurs with stock on loan if it is later delivered to fulfill a call assignment or put exercise?

The loan will end on T+1 of the transaction (trade, assignment, or exercise) that closed or reduced the position.

Is Pattern Day Trading still available while opted into the Program?

Yes, we will support Pattern Day Trading while users are opted into the program.

How does Short Stock Buy-Ins & Close-Outs work?

When a user holds a short stock position, the clearing broker is obligated to deliver shares by the settlement date. If these shares cannot be borrowed, or are recalled by the lender, or if a "fail to deliver" occurs with the clearinghouse, a close-out may be initiated. If we are unable to borrow shares for delivery by the settlement date (T+1), a close-out will be initiated on T+2 at approximately 9:30 AM ET. Lenders can recall shares at any time. If we cannot replace these recalled shares, a buy-in will be executed by the lender. If we have a net short settlement obligation with the clearinghouse and cannot obtain the shares, a close-out will be initiated prior to the open of regular trading hours on the day following the settlement day.

Please read Important Risk Disclosures With Respect To Participating In Fully Paid Securities Lending Transactions carefully before deciding whether to participate in lending Fully Paid Securities or agreeing to enter into a Master Securities Lending Agreement with Alpaca Securities LLC.

These disclosures describe important characteristics of, and risks associated with engaging in, securities-lending transactions.

All investments involve risk and the past performance of a security, or financial product does not guarantee future results or returns. There is no guarantee that any investment strategy will achieve its objectives. Please note that diversification does not assure a profit, or protect against loss. There is always the potential of losing money when you invest in securities, or other financial products. Investors should consider their investment objectives and risks carefully before investing.

Updated4 days ago
Instant Funding24/5 TradingAsk AI
