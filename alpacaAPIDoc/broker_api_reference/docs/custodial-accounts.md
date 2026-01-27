---
source: https://docs.alpaca.markets/docs/custodial-accounts
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

Custodial accounts
A custodial account enables an adult to open an account on behalf of a minor, who otherwise does not have the capacity to enter into a legal contract to open a brokerage account. Alpaca currently supports two custodial account types: Uniform Transfers to Minors Act (UTMA) and Uniform Gifts to Minors Act (UGMA). As part of the offering, Alpaca will custody the account, generate monthly custodial account statements, and handle all annual tax reporting. Please be aware that all tax reporting will be based on the minor's information. Furthermore, a minor cannot use or trade in a custodial account as they are only the beneficiary. Custodial accounts do not support shorting, margin, or pattern day trading. Each of the account opening steps are the same as standard brokerage accounts that Alpaca offers, and any KYC checks will be run on the adult. This documentation will serve to highlight any notable differences between the account opening processes.

Custodial Account Object
AttributeNotesaccount_typeDesignate which type of account is to be opened with Alpaca - passing 'custodial' will create a custodial account.contactContact information about the user.identityKYC information about the user.disclosuresRequired disclosures about the user.documentsAny documents that need to be uploaded (eg. passport, visa, …).trusted_contactThe contact information of a trusted contact to the user in case account recovery is needed.minor_identityInformation about the minor that is associated with the account. All fields in this object will be required when account_type is 'custodial'.
Minor identity object
AttributeTypegiven_namestringfamily_namestringemailstringdate_of_birthdatetax_idstringtax_id_typeENUM.TaxIdTypecountry_of_citizenshipstringcountry_of_birthstringcountry_of_tax_residencestringstatestring

Creating a Custodial Account

POST /v1/accounts
The custodian, or adult associated with the account, will submit an account application with the required information and a signed custodian customer agreement. This will create a custodial account for the adult on behalf of the minor, whose information will be submitted in the minor_identity section.

If you utilize Alpaca for KYCaaS, we will perform the necessary checks and approve the account once we have determined the custodian information is legitimate. Please refer to the Events API for account status changes and any KYC updates that require you to take further action.

Note: All account statuses and their definitions can be found here.

Sample Request
JSON

{
 "account_type": "custodial",
 "contact": {
 "email_address": "[email protected]",
 "phone_number": "555-676-7788",
 "street_address": ["20 N San Mateo Dr"],
 "city": "San Mateo",
 "state": "CA",
 "postal_code": "94401",
 "country": "USA"
 },
 "identity": {
 "given_name": "John",
 "family_name": "Doe",
 "date_of_birth": "1990-01-01",
 "tax_id": "676-55-4321",
 "tax_id_type": "USA_SSN",
 "country_of_citizenship": "USA",
 "country_of_birth": "USA",
 "country_of_tax_residence": "USA",
 "funding_source": ["employment_income"],
 "annual_income_min": "30000",
 "annual_income_max": "50000",
 "liquid_net_worth_min": "100000",
 "liquid_net_worth_max": "150000",
 "total_net_worth_min": "10000",
 "total_net_worth_max": "10000",
 "liquidity_needs": "does_not_matter",
 "investment_experience_with_stocks": "over_5_years",
 "investment_experience_with_options": "over_5_years",
 "risk_tolerance": "conservative",
 "investment_objective": "market_speculation",
 "investment_time_horizon": "more_than_10_years",
 "marital_status": "MARRIED",
 "middle_name": "M",
 "number_of_dependents": 5
 },
 "disclosures": {
 "is_control_person": false,
 "is_affiliated_exchange_or_finra": false,
 "is_politically_exposed": false,
 "immediate_family_exposed": false
 },
 "agreements": [

 {
 "agreement": "customer_agreement",
 "signed_at": "2025-09-11T18:13:44Z",
 "ip_address": "185.13.21.99"

 }
 ],
 "documents": [
 {
 "document_type": "identity_verification",
 "document_sub_type": "passport",
 "content": "/9j/Cg==",
 "mime_type": "image/jpeg"
 }
 ],
 "trusted_contact": {
 "given_name": "Jane",
 "family_name": "Doe",
 "email_address": "[email protected]"
 },
 "minor_identity": {
 "given_name": "Jimmy",
 "family_name": "Doe",
 "email": "[email protected]",
 "date_of_birth": "2015-01-01",
 "tax_id": "676-54-4321",
 "tax_id_type": "USA_SSN",
 "country_of_citizenship": "USA",
 "country_of_birth": "USA",
 "country_of_tax_residence": "USA",
 "state": "CA"
 }
}

A copy of the custodian customer agreement and the custodial account disclosure are available upon request - please reach out to Alpaca for more information.

Note: Revisions follow the RR.MM.YYYY format (RR denotes the revision number); the request payload must include the latest customer_agreement (rev ≥ 18) with the revision explicitly specified.

Response model
AttributeTypeNotesidstring/UUIDUUID that identifies the account for later referenceaccount_numberstringA human-readable account number that can be shown to the end userstatusENUM.AccountStatuscurrencystringAlways USDlast_equitystringEOD equity calculation (cash + long market value + short market value)created_atstringRFC3339 format
JSON

{
 "account": {
 "id": "0d18ae51-3c94-4511-b209-101e1666416b",
 "account_number": "9034005019",
 "status": "ACTIVE",
 "currency": "USD",
 "last_equity": "1500.65",
 "created_at": "2019-09-30T23:55:31.185998Z"
 }
}

Error Codes
Error CodeDescription400Bad Request: The body in the request is not valid409Conflict: There is already an existing account registered with the same email address.422Unprocessable Entity: Invalid input value.500Internal Server Error: Some server error occurred. Please contact Alpaca.

Updating an Account

PATCH /v1/accounts/{account_id}
This operation updates custodial account information. In addition to what is listed for traditional brokerage accounts, the minor identity information is modifiable.

Response Parameters
AttributeRequirementcontactOptionalidentityOptionaldisclosuresOptionaldocumentsOptionaltrusted_contactOptionalminor_identityOptional
Minor Identity parameters
AttributeTypeRequirementNotesgiven_namestringOptionalfamily_namestringOptionalemailstringOptionaldate_of_birthdateOptionalRFC3339 formattax_idstringOptionaltax_id_typeENUM.TaxIdTypeRequiredMust be 'USA_SSN'country_of_citizenshipstringRequiredMust be 'USA'country_of_birthstringRequired3 letter country code acceptablecountry_of_tax_residencestringRequiredMust be 'USA'statestringRequiredOnly accepts two letter state codes
Response

If all parameters are valid and updates have been made, it returns with status code 200. The response is the account model.

Error Codes
Error CodeDescription400Bad Request: The body in the request is not valid422Unprocessable Entity: The request body contains an attribute that is not permitted to be updated.500Internal Server Error: Some server error occurred. Please contact Alpaca.
Appendix
**Sample Monthly Statement: **

Updated4 days ago
Tokenization Guide for Authorized ParticipantAbout Trading APIAsk AI
