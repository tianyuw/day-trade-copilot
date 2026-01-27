---
source: https://docs.alpaca.markets/docs/instant-funding-1
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

Instant Funding
Frequently Asked Instant Funding Questions

Generic Questions
Is instant funding equivalent to granting a loan?
In a way yes. It allows you to give your customers instant buying power before the actual funds reach Alpaca.

Is Instant Funding available for all international partners?
Instant Funding as an Alpaca Broker API product is available in the international countries listed here.

Can Instant Funding be tested in sandbox first?
Yes, you can test Instant Funding on sandbox. To get started, kindly reach out to your sales representative or customer success manager, who will enable this feature for you.

How long does activating the instant funding service need? Is there any procedure to be done on the partner side?
Commercials discussion will need to happen with the sales team & a pricing amendment will need to be signed by the partner. Additional technical configurations would also need to be done by the Alpaca technical team, and the partner will need to integrate with the instant funding endpoints.

Is the partner required to keep a deposit with Alpaca?
Yes, a deposit will be required. Commercials discussion will need to happen with the sales team.

Can the partner withdraw this deposit amount in case of emergency to settle instant funding transfers in case settlement funds don’t arrive to Alpaca on time?
The deposit should be left untouched in your DP account and it cannot be used for settlement. Any prefunding should happen from the RF firm account that will be provided to the partner, described under the accounts section below.

Will the partner or their customers be considered the debtors to Alpaca?
The partner

Do our customers need to sign a new contract with Alpaca to use the instant funding service?
No, the contract will be signed between Alpaca and the partner.

Accounts
What are each of these accounts used for and who creates them: SI, RF, FW?
These will be set up by Alpaca when you confirm you will be moving forward with Instant Funding.

SI: Instant Funding account - Instant funding transfers and reconciliations will be created with this as the source account.

RF: Reconciliation Facilitation account - Partners are able to pre-fund this account to be used in the event that the amount sent for Instant Funding settlement is not sufficient, so they can complete settlement without any issues.

FW: Firm Withdraw account - The account is used to hold partner funds that the partner can choose to withdraw or journal to another firm account type. Excess funds in the SI account after a settlement completes will also be swept into this FW account.

Why can the equity of an account with an unsettled memopost go negative?
First, a general reminder on the trading details endpoint response fields:

Irrelevant to memoposts

long_market_value: Open long positions market value

short_market_value: Open short positions market value

Includes unsettled memoposts.

buying_power: Total cash buying power available for the customer to trade on their account.

cash: Total tradable cash that is available for a customer to trade on their account.

memoposts: Total amount of pending memoposts on the account. AKA, this is the total amount of cash in the customer's account that is available for trading due to memoposts executed but not yet settled or cancelled.

Does not include unsettled memoposts.

cash_withdrawable: The cash that is available for the user to withdraw.

equity: This is an account's total equity. Formula to calculate equity and account for memoposts is:
equity = cash + long_market_value + short_market_value - memoposts

Second, the logic for calculating equity:

When you create a new instant funding transfer to an account:

buying_power,
cash, &
memoposts will increase by the same amount

cash_withdrawable,
long_market_value, &
short_market_value will not change

equity will not change

The last point is the key point here. Since the memopost is ONLY an extension of
buying_power, it affects any field that shows tradable cash, but it does not affect fields that show settled cash only.

Since
memoposts are added to
cash, and
equity includes
cash, the formula to calculate equity has to adjust by removing the value of the memoposts.

Third, A practical example:

Account has 0 in
cash, 0
buying_power, 0
cash_withdrawable, 0
long_market_value, 0
equity, & 0
memoposts

They deposit 100$ on the app and you memopost 100$ into their account to offer them the instant experience. You will see the below on the account:

buying_power = 100

cash = 100

memoposts = 100

cash_withdrawable = 0

long_market_value = 0

equity = 0

Notice
equity here, it is still 0

Then, when does the negative equity happen?

If a customer uses the buying power to buy stock, and the price of the stock shifts causing a loss, that loss would cause a negative equity value. Similarly, if the customer makes profit, the equity value will show a positive value.

How to validate this?

You can test in sandbox and monitor the values.

Suggestions on how to handle this:

If you are showing the equity value on the UI and want to avoid showing a negative value to your users, you can simply add the memoposts value you get from the API to the equity value you get, and that would avoid the issue to begin with.

Transfers & Settlement
How are instant funding deadlines managed? Which schedule does Alpaca follow?
Instant funding deadlines follow the US trading holiday schedule. In other words, you would not see an instant funding transfer due on a weekend or on a US trading holiday.

What is the payment due date for instant funding transfers?
The payment due date for instant funding transfers will be on T+1 by 1 PM ET.

It’s also important to note that instant funding transfers created after 8 pm on T+0 will be considered as next day, meaning that the system date is considered as T+1 and the transfer will be due for settlement on T+2 by 1 PM ET.

The system_date field that is returned via the Instant Funding API will be the source of truth for determining the date that the instant funding transfer was created on and the deadline field that is returned will be the source of truth for determining the date settlement is expected.

When an instant funding transfer is not settled by 1:00 PM ET on T+1 at and a customer has not yet bought any stock, how will Alpaca handle this transfer?
A late payment interest charge will be booked on T+1 at 1 PM ET, but the transfer will not be cancelled immediately.

By 8 PM ET on T+1, if the transfer is still not settled, it will then be canceled and the account’s buying power will be decreased.

What happens if a customer uses the buying power allocated to their account after an instant funding transfer, but the transfer is not settled by 8 PM ET on T+1?
Instant funding transfers will be automatically canceled at 8 PM ET on T+1 if payment is still not received. If the instant funding transfer has been used to purchase any asset, the cash balance in the customer account at T+1 will be used to offset the instant funding transfer. Should this result in a negative balance on the account, Alpaca will issue a margin call on T+2 to cover the negative balance. On T+3 if the debit balance has not been addressed, positions in the account will be sold to cover. Daily interest will be charged at the margin interest rate until the account no longer has a negative balance. Late payment interest will be charged on the instant funding transfer at 1 PM ET on T+1 if it is not settled by then.

If there is an unexpected event that prevents settlement funds from arriving to Alpaca on time, or there is a bank holiday, how should we settle instant funding transfers?
For this purpose we have introduced the RF account (detailed here). You can hold funds there and journal into the SI account as needed to ensure timely settlement even in the event of bank holidays. If the instant funding transfers still cannot be settled, the scenarios explained here & here would apply.

What is a late instant funding transfer? What is a debit balance?
An instant funding transfer is considered late if it is not settled by 1 PM ET on T+1. In this case, a late payment interest of 1 day will be charged (fed rate + 8%).

The transfer will then be canceled at 8 PM ET. If there is sufficient cash balance in the customer account, that would be used to offset the outstanding amount of the transfer. If there is not, the account would then fall into a debit balance and margin interest will be charged (at the rate documented here) on this until the balance is no longer negative.

In case of a margin call, what positions would be sold out?
Selected assets will be liquidated based on the discretion of our broker dealer operations team.

Will interest accrued for late payments be deducted directly from the account?
Interest for late payments will be accrued and invoiced to you on a monthly basis.

How is a debit balance settled?
A partner can settle a debit balance on an account by journaling funds from the RF account to the customer’s account directly. The partner can also collect the needed funds locally from their customer before initiating this journal.

Can instant funding be enabled in parallel with aggregate funding?
Yes, you can be on both instant funding and aggregate funding at the same time.

If a partner is on both instant funding and aggregate funding, can a customer that exceeds the pre-determined limit fund the excess amount they require using aggregate funding?
Yes. The funding flow would depend on the APIs you are using to fund the account. Under aggregate funding, you would use the Journal API to move funds from your firm account to the customer account. Under Instant Funding, you would use the Instant Funding API to create an instant funding transfer.

Do we (the partner) decide which instant funding transfers are going to be settled?
You would use the Create Settlement API to do the reconciliation. In this API, you will need to specify the transfer ID that you are looking to reconcile - this means that the decision lies with the partner on the transfers to be reconciled.

Does Alpaca have the ability to waive interest charges due to a technical issue on Alpaca's end or BMO events?
This is something that would need to be taken care of on a case by case basis. Your PM or CSM would be the best person to address this if such a case arises in the future.

Is it possible to avoid the forced liquidation of customer assets and instead have action taken directly against the partner?
No, we would need to take action on the account of the margin call.

Is it possible to extend the timeframe that is given to an account to resolve their debit balance?
No, we are obligated to remain compliant with timelines published by market regulators.

If an account has remaining cash balance, will this be drawn to pay off the unreconciled instant funding transfers of the specific customer only?
Yes.

Is there a case where the cash balance of a certain customer is used to pay off unsettled instant funding transfers of other customers?
No.

Could you clarify how the below scenario would be handled by Alpaca:
On t+0, the partner uses a credit limit worth USD 100,000 out of the total USD 400,000.

The instant funding transfers of the used USD 100,000 credit cannot be reconciled on t+1 1:00 PM (US ET)

How would the limit be updated on t+1 after 1 PM?

The scenario is illustrated below:
DateActionAmountTotal LimitAmount in UseAmount AvailableNotes(t+0)--400,0000400,000This is the partner’s total available limit(t+0)MEM100,000$400,000100,000300,000When the transfers are done, the remaining limit is reduced(t+1) Before 8PM--400,000100,000300,000As long as the transfers have not been cancelled yet, the remaining limit is not affected. In other words, since the 100k transfers are still not cancelled, the remaining limit available to be used is 300k(t+1) After 8PMMEM-100,000
(cancelled transfer)400,0000400,000As soon as the transfers are cancelled, the available to use limit goes back to 400k
In summary, as long as the transfers are not settled or cancelled yet, the remaining limit would be the partner’s total limit - the amount of executed transfers. As soon as the transfers are settled or cancelled, the remaining limit would reset.

Note: The instant funding transfers are due for settlement at 1PM ET on t+1, but they actually get cancelled at 8PM ET.

What would be the best way for a partner to retrieve the overall cumulative outstanding amount, interest, and unreconciled instant funding transfers to date ?
Call the GET all instant funding endpoint and filter by status.

Are SSE events supported for IF transfers ?
Yes, SSE events for IF transfers can be subscribed to here.

Why do I need to send travel rule information?
Alpaca is a financial institution so it is required by US law for us to collect travel rule information when dealing with the movement of funds. Since instant funding transfers are only an extension of buying power we only require travel rule information upon settlement since that is when the instant funding transfer is converted to actual settled cash. For more information on the travel rule requirements please refer to the FinCEN Advisory as needed.

Limits
Is it possible to increase the predefined correspondent limit?
Broker-Dealer will have to approve and more deposit is likely required, but yes this is possible.

Does the partner have the ability to change the USD 1,000 limit per individual or does this need approval from Alpaca?
The default is set at USD $1,000. The partner can discuss with the sales team regarding the higher limit so that it can be factored into the commercial discussions.

For the individual limit change, is it possible to assign different limit values to different customers? For example, setting the limit of User A to USD 1,000 & USD 5,000 for User B?
This would not be possible as the account limit is set on a correspondent level; all accounts would have the same limit.

Is it possible for a partner to ignore the individual limit? For example, as long as each day the customers use up to the USD 400,000 limit on instant funding, each customer can fund their account with any amount they need.
We are able to support this configuration, whereby the Instant Funding limit is only on a partner level, and not on your individual user account level.

All investments involve risk, and the past performance of a security, or financial product does not guarantee future results or returns. There is no guarantee that any investment strategy will achieve its objectives. Please note that diversification does not ensure a profit, or protect against loss. There is always the potential of losing money when you invest in securities, or other financial products. Investors should consider their investment objectives and risks carefully before investing.

Securities brokerage services are provided by Alpaca Securities LLC ("Alpaca Securities"), member FINRA/SIPC, a wholly-owned subsidiary of AlpacaDB, Inc. Technology and services are offered by AlpacaDB, Inc. This is not an offer, solicitation of an offer, or advice to buy or sell securities or open a brokerage account in any jurisdiction where Alpaca Securities are not registered or licensed, as applicable.

Updated4 days ago
FDIC Sweep ProgramFully Paid Securities LendingAsk AI
