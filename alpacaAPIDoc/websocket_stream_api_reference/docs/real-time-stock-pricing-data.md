---
source: https://docs.alpaca.markets/docs/real-time-stock-pricing-data
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

Real-time Stock Data
This API provides stock market data on a websocket stream. This helps receive the most up to date market information that could help your trading strategy to act upon certain market movements. If you wish to access the latest pricing data, using the stream provides much better accuracy and performance than polling the latest historical endpoints.

You can find the general description of the real-time WebSocket Stream here. This page focuses on the stock stream.

URL
The URL for the stock stream is

wss://stream.data.alpaca.markets/{version}/{feed}
Sandbox URL:

wss://stream.data.sandbox.alpaca.markets/{version}/{feed}
Substitute
{version}/{feed} to one of the followings:

v2/sip is the SIP (Securities Information Processor) feed

v2/iex is the IEX (Investors Exchange) feed

v2/delayed_sip is a 15-minute delayed SIP feed

v1beta1/boats is the BOATS (Blue Ocean ATS) feed

v1beta1/overnight is the derived Alpaca overnight feed

These feeds are described here.

Any attempt to access a data feed not available for your subscription will result in an error during authentication.

Channels
You can subscribe to the channels described in this section. For example
JSON

{"action":"subscribe","trades":["AAPL"],"quotes":["AMD","CLDR"],"bars":["*"]}
Trades
SchemaAttributeTypeNotes
Tstringmessage type, always “t”
Sstringsymbol
iinttrade ID
xstringexchange code where the trade occurred
pnumbertrade price
sinttrade size
carray
<string>trade condition
tstringRFC-3339 formatted timestamp with nanosecond precision
zstringtape
ExampleJSON

{
 "T": "t",
 "i": 96921,
 "S": "AAPL",
 "x": "D",
 "p": 126.55,
 "s": 1,
 "t": "2021-02-22T15:51:44.208Z",
 "c": ["@", "I"],
 "z": "C"
}
Quotes
SchemaAttributeTypeNotes
Tstringmessage type, always “q”
Sstringsymbol
axstringask exchange code
apnumberask price
asintask size in round lots
bxstringbid exchange code
bpnumberbid price
bsintbid size in round lots
carray
<string>quote condition
tstringRFC-3339 formatted timestamp with nanosecond precision
zstringtape
ExampleJSON

{
 "T": "q",
 "S": "AMD",
 "bx": "U",
 "bp": 87.66,
 "bs": 1,
 "ax": "Q",
 "ap": 87.68,
 "as": 4,
 "t": "2021-02-22T15:51:45.335689322Z",
 "c": ["R"],
 "z": "C"
}
Bars
There are three separate channels where you can stream trade aggregates (bars).

Minute Bars (
bars)
Minute bars are emitted right after each minute mark. They contain the trades from the previous minute. Trades from pre-market and aftermarket are also aggregated and sent out on the bars channel.

Note: Understanding which trades are excluded from minute bars is crucial for accurate data analysis. For more detailed information on how minute bars are calculated and excluded trades, please refer to this article Stock Minute Bars.

Daily Bars (
dailyBars)
Daily bars are emitted right after each minute mark after the market opens. The daily bars contain all trades until the time they were emitted.

Updated Bars (
updatedBars)
Updated bars are emitted after each half-minute mark if a “late” trade arrived after the previous minute mark. For example if a trade with a timestamp of
16:49:59.998 arrived right after
16:50:00, just after
16:50:30 an updated bar with
t set to
16:49:00 will be sent containing that trade, possibly updating the previous bar’s closing price and volume.

SchemaAttributeTypeDescription
Tstringmessage type: “b”, “d” or “u”
Sstringsymbol
onumberopen price
hnumberhigh price
lnumberlow price
cnumberclose price
vintvolume
vwnumbervolume-weighted average price
nintnumber of trades
tstringRFC-3339 formatted timestamp
ExampleJSON

{
 "T": "b",
 "S": "SPY",
 "o": 388.985,
 "h": 389.13,
 "l": 388.975,
 "c": 389.12,
 "v": 49378,
 "n": 461,
 "vw": 389.062639,
 "t": "2021-02-22T19:15:00Z"
}
Trade Corrections
These messages indicate that a previously sent trade was incorrect and they contain the corrected trade.

Subscription to trade corrections and cancel/errors is automatic when you subscribe to the trade channel.

{"action":"subscribe","trades":["AAPL"]}
[{"T":"subscription","trades":["AAPL"],"quotes":[],"bars":[],"updatedBars":[],"dailyBars":[],"statuses":[],"lulds":[],
"corrections":["AAPL"],"cancelErrors":["AAPL"]}]
SchemaAttributeTypeDescription
Tstringmessage type, always “c”
Sstringsymbol
xstringexchange code
oiintoriginal trade id
opnumberoriginal trade price
osintoriginal trade size
ocarray
<string>original trade conditions
ciintcorrected trade id
cpnumbercorrected trade price
csintcorrected trade size
ccarray
<string>corrected trade conditions
tstringRFC-3339 formatted timestamp
zstringtape
ExampleJSON

{
 "T": "c",
 "S": "EEM",
 "x": "M",
 "oi": 52983525033527,
 "op": 39.1582,
 "os": 440000,
 "oc": [
 " ",
 "7"
 ],
 "ci": 52983525034326,
 "cp": 39.1809,
 "cs": 440000,
 "cc": [
 " ",
 "7"
 ],
 "z": "B",
 "t": "2023-04-06T14:25:06.542305024Z"
}
Trade Cancels/Errors
These messages indicate that a previously sent trade was canceled.

Subscription to trade corrections and cancel/errors is automatic when you subscribe to the trade channel.

{"action":"subscribe","trades":["AAPL"]}
[{"T":"subscription","trades":["AAPL"],"quotes":[],"bars":[],"updatedBars":[],"dailyBars":[],"statuses":[],"lulds":[],
"corrections":["AAPL"],"cancelErrors":["AAPL"]}]
SchemaAttributeTypeDescription
Tstringmessage type, always “x”
Sstringsymbol
iinttrade id
xstringtrade exchange
pnumbertrade price
sinttrade size
astringaction (“C” for cancel, “E” for error)
tstringRFC-3339 formatted timestamp
zstringtape
ExampleJSON

{
 "T": "x",
 "S": "GOOGL",
 "i": 465,
 "x": "D",
 "p": 105.31,
 "s": 300,
 "a": "C",
 "z": "C",
 "t": "2023-04-06T13:15:42.83540958Z"
}
LULDs
Limit Up - Limit Down messages provide upper and lower limit price bands to securities.

SchemaAttributeTypeDescription
Tstringmessage type, always “l”
Sstringsymbol
unumberlimit up price
dnumberlimit down price
istringindicator
tstringRFC-3339 formatted timestamp
zstringtape
ExampleJSON

{
 "T": "l",
 "S": "IONM",
 "u": 3.24,
 "d": 2.65,
 "i": "B",
 "t": "2023-04-06T13:34:45.565004401Z",
 "z": "C"
}
Trading Status
Identifies the trading status applicable to the security and reason for the trading halt if any. The status messages can be accessed from any {source} depending on your subscription.

To enable market data on a production environment please reach out to our sales team.

SchemaAttributeTypeDescription
Tstringmessage type, always “s”
Sstringsymbol
scstringstatus code
smstringstatus message
rcstringreason code
rmstringreason message
tstringRFC-3339 formatted timestamp
zstringtape
ExampleJSON

{
 "T": "s",
 "S": "AAPL",
 "sc": "H",
 "sm": "Trading Halt",
 "rc": "T12",
 "rm": "Trading Halted; For information requested by NASDAQ",
 "t": "2021-02-22T19:15:00Z",
 "z": "C"
}
Status Codes
Tape A & B (CTA)CodeValue2Trading Halt3Resume5Price Indication6Trading Range Indication7Market Imbalance Buy8Market Imbalance Sell9Market On Close Imbalance BuyAMarket On Close Imbalance SellCNo Market ImbalanceDNo Market On Close ImbalanceEShort Sale RestrictionFLimit Up-Limit Down
Tape C & O (UTP)CodesResumeHTrading HaltQQuotation ResumptionTTrading ResumptionPVolatility Trading Pause
Reason Codes
Tape A & B (CTA)CodeValueDNews Released (formerly News Dissemination)IOrder ImbalanceMLimit Up-Limit Down (LULD) Trading PausePNews PendingXOperationalYSub-Penny Trading1Market-Wide Circuit Breaker Level 1 – Breached2Market-Wide Circuit Breaker Level 2 – Breached3Market-Wide Circuit Breaker Level 3 – Breached
Tape C & O (UTP)CodeValueT1Halt News PendingT2Halt News DisseminationT5Single Stock Trading Pause In AffectT6Regulatory Halt Extraordinary Market ActivityT8Halt ETFT12Trading Halted; For information requested by NASDAQH4Halt Non ComplianceH9Halt Filings Not CurrentH10Halt SEC Trading SuspensionH11Halt Regulatory Concern01Operations Halt, Contact Market OperationsIPO1IPO Issue not yet TradingM1Corporate ActionM2Quotation Not AvailableLUDPVolatility Trading PauseLUDSVolatility Trading Pause – Straddle ConditionMWC1Market Wide Circuit Breaker Halt – Level 1MWC2Market Wide Circuit Breaker Halt – Level 2MWC3Market Wide Circuit Breaker Halt – Level 3MWC0Market Wide Circuit Breaker Halt – Carry over from previous dayT3News and Resumption TimesT7Single Stock Trading Pause/Quotation-Only PeriodR4Qualifications Issues Reviewed/Resolved; Quotations/Trading to ResumeR9Filing Requirements Satisfied/Resolved; Quotations/Trading To ResumeC3Issuer News Not Forthcoming; Quotations/Trading To ResumeC4Qualifications Halt ended; maint. Req. met; ResumeC9Qualifications Halt Concluded; Filings Met; Quotes/Trades To ResumeC11Trade Halt Concluded By Other Regulatory Auth,; Quotes/Trades ResumeR1New Issue AvailableRIssue AvailableIPOQIPO security released for quotationIPOEIPO security – positioning window extensionMWCQMarket Wide Circuit Breaker Resumption
Order imbalances
Order imbalance is a situation resulting from an excess of buy or sell orders for a specific security on a trading exchange, making it impossible to match the orders of buyers and sellers. Order imbalance messages are typically sent during limit-up and limit-down trading halts. You have to subscribe to these messages using the
imbalances JSON key:
JSON

{"action":"subscribe","imbalances":["INAQU"]}
SchemaAttributeTypeNotes
Tstringmessage type, always “i”
Sstringsymbol
pnumberprice
zstringtape
tstringRFC-3339 formatted timestamp with nanosecond precision
ExampleJSON

{
 "T": "i",
 "S": "INAQU",
 "p": 9.12,
 "z": "C",
 "t": "2024-12-13T19:58:09.242138635Z"
}
ExampleShell

$ wscat -c wss://stream.data.alpaca.markets/v2/sip
connected (press CTRL+C to quit)
< [{"T":"success","msg":"connected"}]
> {"action": "auth", "key": "*****", "secret": "*****"}
< [{"T":"success","msg":"authenticated"}]
> {"action": "subscribe", "trades": ["AAPL"], "quotes": ["AMD", "CLDR"], "bars": ["*"],"dailyBars":["VOO"],"statuses":["*"]}
< [{"T":"subscription","trades":["AAPL"],"quotes":["AMD","CLDR"],"bars":["*"],"updatedBars":[],"dailyBars":["VOO"],"statuses":["*"],"lulds":[],"corrections":["AAPL"],"cancelErrors":["AAPL"]}]
< [{"T":"q","S":"AMD","bx":"K","bp":91.95,"bs":2,"ax":"Q","ap":91.98,"as":1,"c":["R"],"z":"C","t":"2023-04-06T11:54:21.670905508Z"}]
< [{"T":"t","S":"AAPL","i":628,"x":"K","p":162.92,"s":3,"c":["@","F","T","I"],"z":"C","t":"2023-04-06T11:54:26.838232225Z"},{"T":"t","S":"AAPL","i":75,"x":"Z","p":162.92,"s":3,"c":["@","F","T","I"],"z":"C","t":"2023-04-06T11:54:26.838562809Z"},{"T":"t","S":"AAPL","i":1465,"x":"P","p":162.91,"s":71,"c":["@","F","T","I"],"z":"C","t":"2023-04-06T11:54:26.83915973Z"}]
< [{"T":"q","S":"AMD","bx":"P","bp":91.9,"bs":1,"ax":"Q","ap":91.98,"as":1,"c":["R"],"z":"C","t":"2023-04-06T11:54:27.924933876Z"}]
Updated3 days ago
WebSocket StreamReal-time Crypto DataAsk AI
