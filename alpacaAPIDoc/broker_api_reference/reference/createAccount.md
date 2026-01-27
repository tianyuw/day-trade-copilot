---
source_view: https://docs.alpaca.markets/reference/createaccount
source_md: https://docs.alpaca.markets/reference/createaccount.md
scraped_at_utc: 2026-01-27T04:30:48Z
---
# Create an Account

Submit an account application with KYC information. This will create a trading account for the end user. The account status may or may not be ACTIVE immediately and you will receive account status updates on the event API. 

# OpenAPI definition

```json
{
  "openapi": "3.0.0",
  "x-stoplight": {
    "id": "y5xqkgq9w6jde"
  },
  "info": {
    "title": "Broker API",
    "description": "Open brokerage accounts, enable stock, options and crypto trading. Manage the ongoing user experience and brokerage customer lifecycle with the Alpaca Broker API",
    "version": "1.1.1",
    "contact": {
      "name": "Alpaca Support",
      "email": "support@alpaca.markets",
      "url": "https://alpaca.markets/support"
    },
    "termsOfService": "https://s3.amazonaws.com/files.alpaca.markets/disclosures/library/TermsAndConditions.pdf"
  },
  "servers": [
    {
      "url": "https://broker-api.sandbox.alpaca.markets",
      "description": "Sandbox endpoint"
    },
    {
      "url": "https://broker-api.alpaca.markets",
      "description": "Production endpoint"
    }
  ],
  "tags": [
    {
      "name": "Accounts"
    }
  ],
  "components": {
    "securitySchemes": {
      "BasicAuth": {
        "type": "http",
        "scheme": "basic"
      }
    }
  },
  "paths": {
    "/v1/accounts": {
      "post": {
        "tags": [
          "Accounts"
        ],
        "summary": "Create an Account",
        "requestBody": {
          "required": true,
          "content": {
            "application/json": {
              "schema": {
                "type": "object",
                "title": "AccountCreationRequest",
                "description": "Represents the fields required to create a new account",
                "properties": {
                  "account_type": {
                    "type": "string",
                    "title": "AccountType",
                    "description": "Possible values are:\n\n- trading\n- custodial\n- donor_advised\n- ira",
                    "enum": [
                      "trading",
                      "custodial",
                      "donor_advised",
                      "ira"
                    ],
                    "example": "trading",
                    "x-readme-ref-name": "AccountType"
                  },
                  "account_sub_type": {
                    "type": "string",
                    "title": "AccountSubType",
                    "description": "IRA Account only\n\nPossible values are:\n\n- traditional\n- roth",
                    "enum": [
                      "traditional",
                      "roth"
                    ],
                    "example": "traditional",
                    "x-readme-ref-name": "AccountSubType"
                  },
                  "contact": {
                    "type": "object",
                    "description": "Contact is the model for the account owner contact information.\n",
                    "x-stoplight": {
                      "id": "qcig9irpj9334"
                    },
                    "properties": {
                      "email_address": {
                        "type": "string",
                        "format": "email",
                        "example": "john.doe@example.com"
                      },
                      "phone_number": {
                        "type": "string",
                        "example": "+15556667788",
                        "description": "Phone number should include the country code, format: “+15555555555”"
                      },
                      "street_address": {
                        "type": "array",
                        "description": "The user's street address. If multiple lines in address, pass in as additional array elements. Maximum of 3 objects in array",
                        "items": {
                          "type": "string",
                          "example": "20 N San Mateo Dr",
                          "x-stoplight": {
                            "id": "10wajx98hc79a"
                          },
                          "x-readme-ref-name": "StreetAddress"
                        }
                      },
                      "unit": {
                        "type": "string",
                        "x-stoplight": {
                          "id": "yybrq2o2nb5gy"
                        },
                        "description": "The specific apartment number if applicable"
                      },
                      "city": {
                        "type": "string",
                        "example": "San Mateo"
                      },
                      "state": {
                        "type": "string",
                        "example": "CA",
                        "description": "Required if the country or country_of_tax_residence (in the identity model below) is 'USA'."
                      },
                      "country": {
                        "type": "string",
                        "example": "USA",
                        "description": "country code in ISO 3166-1 alpha-3 format, representing the country the person/entity resides in."
                      },
                      "postal_code": {
                        "type": "string",
                        "example": "94401"
                      }
                    },
                    "required": [
                      "email_address",
                      "phone_number",
                      "street_address",
                      "city"
                    ],
                    "x-readme-ref-name": "Contact"
                  },
                  "identity": {
                    "type": "object",
                    "description": "Identity is the model to provide account owner’s identity information.\n",
                    "example": {
                      "given_name": "John",
                      "family_name": "Doe",
                      "date_of_birth": "1990-01-01",
                      "tax_id": "666-55-4321",
                      "tax_id_type": "USA_SSN",
                      "country_of_citizenship": "AUS",
                      "country_of_birth": "AUS",
                      "country_of_tax_residence": "USA",
                      "funding_source": [
                        "employment_income"
                      ]
                    },
                    "x-stoplight": {
                      "id": "oi43k8rpw570e"
                    },
                    "properties": {
                      "given_name": {
                        "type": "string",
                        "example": "John",
                        "description": "The first/given name of the user."
                      },
                      "family_name": {
                        "type": "string",
                        "example": "Doe",
                        "description": "The last name (surname) of the user."
                      },
                      "middle_name": {
                        "type": "string",
                        "x-stoplight": {
                          "id": "p03brcsyyjbcq"
                        },
                        "description": "The middle name of the user."
                      },
                      "date_of_birth": {
                        "type": "string",
                        "format": "date",
                        "example": "1990-01-01",
                        "description": "The date of birth in \"YYYY-MM-DD\" format."
                      },
                      "tax_id": {
                        "type": "string",
                        "example": "666-55-4321",
                        "description": "Required if tax_id_type is set."
                      },
                      "tax_id_type": {
                        "type": "string",
                        "title": "TaxIdType",
                        "enum": [
                          "USA_SSN",
                          "USA_ITIN",
                          "ARG_AG_CUIT",
                          "AUS_TFN",
                          "AUS_ABN",
                          "BOL_NIT",
                          "BRA_CPF",
                          "CHL_RUT",
                          "COL_NIT",
                          "CRI_NITE",
                          "DEU_TAX_ID",
                          "DOM_RNC",
                          "ECU_RUC",
                          "FRA_SPI",
                          "GBR_UTR",
                          "GBR_NINO",
                          "GTM_NIT",
                          "HND_RTN",
                          "HUN_TIN",
                          "IDN_KTP",
                          "IND_PAN",
                          "ISR_TAX_ID",
                          "ITA_TAX_ID",
                          "JPN_TAX_ID",
                          "MEX_RFC",
                          "NIC_RUC",
                          "NLD_TIN",
                          "PAN_RUC",
                          "PER_RUC",
                          "PRY_RUC",
                          "SGP_NRIC",
                          "SGP_FIN",
                          "SGP_ASGD",
                          "SGP_ITR",
                          "SLV_NIT",
                          "SWE_TAX_ID",
                          "URY_RUT",
                          "VEN_RIF",
                          "NATIONAL_ID",
                          "PASSPORT",
                          "PERMANENT_RESIDENT",
                          "DRIVER_LICENSE",
                          "OTHER_GOV_ID",
                          "NOT_SPECIFIED"
                        ],
                        "description": "Required if `tax_id` is set.\n\nAn Enum of the various kinds of Tax ID formats Alpaca supports.\n\nPossible Values are:\n\n\n- **USA_SSN**\nUSA Social Security Number\n\n- **USA_ITIN**\nUSA Individual Taxpayer Identification Number\n\n- **ARG_AR_CUIT**\nArgentina CUIT\n\n- **AUS_TFN**\nAustralian Tax File Number\n\n- **AUS_ABN**\nAustralian Business Number\n\n- **BOL_NIT**\nBolivia NIT\n\n- **BRA_CPF**\nBrazil CPF\n\n- **CHL_RUT**\nChile RUT\n\n- **COL_NIT**\nColombia NIT\n\n- **CRI_NITE**\nCosta Rica NITE\n\n- **DEU_TAX_ID**\nGermany Tax ID (Identifikationsnummer)\n\n- **DOM_RNC**\nDominican Republic RNC\n\n- **ECU_RUC**\nEcuador RUC\n\n- **FRA_SPI**\nFrance SPI (Reference Tax Number)\n\n- **GBR_UTR**\nUK UTR (Unique Taxpayer Reference)\n\n- **GBR_NINO**\nUK NINO (National Insurance Number)\n\n- **GTM_NIT**\nGuatemala NIT\n\n- **HND_RTN**\nHonduras RTN\n\n- **HUN_TIN**\nHungary TIN Number\n\n- **IDN_KTP**\nIndonesia KTP\n\n- **IND_PAN**\nIndia PAN Number\n\n- **ISR_TAX_ID**\nIsrael Tax ID (Teudat Zehut)\n\n- **ITA_TAX_ID**\nItaly Tax ID (Codice Fiscale)\n\n- **JPN_TAX_ID**\nJapan Tax ID (Koijin Bango)\n\n- **MEX_RFC**\nMexico RFC\n\n- **NIC_RUC**\nNicaragua RUC\n\n- **NLD_TIN**\nNetherlands TIN Number\n\n- **PAN_RUC**\nPanama RUC\n\n- **PER_RUC**\nPeru RUC\n\n- **PRY_RUC**\nParaguay RUC\n\n- **SGP_NRIC**\nSingapore NRIC\n\n- **SGP_FIN**\nSingapore FIN\n\n- **SGP_ASGD**\nSingapore ASGD\n\n- **SGP_ITR**\nSingapore ITR\n\n- **SLV_NIT**\nEl Salvador NIT\n\n- **SWE_TAX_ID**\nSweden Tax ID (Personnummer)\n\n- **URY_RUT**\nUruguay RUT\n\n- **VEN_RIF**\nVenezuela RIF\n\n- **NATIONAL_ID**\nNational ID number, if a tax ID number is not available\n\n- **PASSPORT**\nPassport number, if a tax ID number is not available\n\n- **PERMANENT_RESIDENT**\nPermanent resident number, if a tax ID number is not available\n\n- **DRIVER_LICENSE**\nDrivers license number, if a tax ID number is not available\n\n- **OTHER_GOV_ID**\nOther government issued identifier, if a tax ID number is not available\n\n- **NOT_SPECIFIED**\nOther Tax IDs",
                        "example": "USA_SSN",
                        "x-stoplight": {
                          "id": "ulm45kpr2peox"
                        },
                        "x-readme-ref-name": "TaxIdType"
                      },
                      "country_of_citizenship": {
                        "type": "string",
                        "description": "[ISO 3166-1 alpha-3](https://www.iso.org/iso-3166-country-codes.html).\n",
                        "example": "USA"
                      },
                      "country_of_birth": {
                        "type": "string",
                        "description": "[ISO 3166-1 alpha-3](https://www.iso.org/iso-3166-country-codes.html).\n",
                        "example": "USA"
                      },
                      "country_of_tax_residence": {
                        "type": "string",
                        "description": "[ISO 3166-1 alpha-3](https://www.iso.org/iso-3166-country-codes.html).\n",
                        "example": "USA"
                      },
                      "funding_source": {
                        "type": "array",
                        "description": "Can be one or more of the following: `employment_income`, `investments`, `inheritance`, `business_income`, `savings`, `family`.",
                        "items": {
                          "type": "string",
                          "enum": [
                            "employment_income",
                            "investments",
                            "inheritance",
                            "business_income",
                            "savings",
                            "family"
                          ]
                        }
                      },
                      "liquidity_needs": {
                        "type": "string",
                        "description": "The user's ability to quickly and easily convert all or part of their investments in this account to cash without significant loss in value. This field is deprecated. Please use the top level `liquidity_needs` field.\n",
                        "enum": [
                          "very_important",
                          "important",
                          "somewhat_important",
                          "does_not_matter"
                        ],
                        "deprecated": true
                      },
                      "investment_experience_with_stocks": {
                        "type": "string",
                        "description": "The user's level of expertise and familiarity with investing in US Equities.\n",
                        "enum": [
                          "none",
                          "1_to_5_years",
                          "over_5_years"
                        ]
                      },
                      "investment_experience_with_options": {
                        "type": "string",
                        "description": "The user's level of expertise and familiarity with investing in Options.\n",
                        "enum": [
                          "none",
                          "1_to_5_years",
                          "over_5_years"
                        ]
                      },
                      "risk_tolerance": {
                        "type": "string",
                        "description": "The user's investment risk tolerance. This field is deprecated. Please use the top level `risk_tolerance` field.\n",
                        "enum": [
                          "conservative",
                          "moderate",
                          "significant_risk"
                        ],
                        "deprecated": true
                      },
                      "investment_objective": {
                        "type": "string",
                        "description": "The user's investment objective. This field is deprecated. Please use the top level `investment_objective` field.\n",
                        "enum": [
                          "generate_income",
                          "preserve_wealth",
                          "market_speculation",
                          "growth",
                          "balance_preserve_wealth_with_growth"
                        ],
                        "deprecated": true
                      },
                      "investment_time_horizon": {
                        "type": "string",
                        "description": "The expected period of time the user plan to invest to achieve his/her financial goal(s). This field is deprecated. Please use the top level `investment_time_horizon` field.\n",
                        "enum": [
                          "less_than_1_year",
                          "1_to_2_years",
                          "3_to_5_years",
                          "6_to_10_years",
                          "more_than_10_years"
                        ],
                        "deprecated": true
                      },
                      "annual_income_min": {
                        "type": "number",
                        "description": "The lower bound of the user's annual income."
                      },
                      "annual_income_max": {
                        "type": "number",
                        "description": "The upper bound of the user's annual income."
                      },
                      "liquid_net_worth_min": {
                        "type": "number",
                        "description": "The lower bound of the user's liquid net worth."
                      },
                      "liquid_net_worth_max": {
                        "type": "number",
                        "description": "The upper bound of the user's liquid net worth."
                      },
                      "total_net_worth_min": {
                        "type": "number",
                        "description": "The lower bound of the user's total net worth."
                      },
                      "total_net_worth_max": {
                        "type": "number",
                        "description": "The upper bound of the user's total net worth."
                      },
                      "visa_type": {
                        "type": "string",
                        "x-stoplight": {
                          "id": "y5a5r7inu02w8"
                        },
                        "description": "Only used to collect visa types for users residing in the USA."
                      },
                      "visa_expiration_date": {
                        "type": "string",
                        "x-stoplight": {
                          "id": "q7b33k53b5alk"
                        },
                        "description": "Required if `visa_type` is set.",
                        "format": "date"
                      },
                      "date_of_departure_from_usa": {
                        "type": "string",
                        "x-stoplight": {
                          "id": "yasik2wcmshea"
                        },
                        "format": "date",
                        "description": "Required if `visa_type` = B1 or B2"
                      },
                      "permanent_resident": {
                        "type": "boolean",
                        "x-stoplight": {
                          "id": "jlvzbu3cevmju"
                        },
                        "description": "Only used to collect permanent residence status in the USA."
                      },
                      "marital_status": {
                        "type": "string",
                        "description": "The marital status of the user.\n",
                        "enum": [
                          "SINGLE",
                          "MARRIED",
                          "DIVORCED",
                          "WIDOWED"
                        ]
                      },
                      "number_of_dependents": {
                        "type": "integer",
                        "description": "The number of dependents the user has.\n"
                      }
                    },
                    "required": [
                      "given_name",
                      "family_name",
                      "date_of_birth",
                      "tax_id_type",
                      "country_of_tax_residence",
                      "funding_source"
                    ],
                    "x-readme-ref-name": "Identity"
                  },
                  "disclosures": {
                    "type": "object",
                    "description": "Disclosures fields denote if the account owner falls under\neach category defined by FINRA rule. The client has to ask\nquestions for the end user and the values should reflect\ntheir answers.\nIf one of the answers is true (yes), the account goes into\nACTION_REQUIRED status.\n",
                    "example": {
                      "is_control_person": false,
                      "is_affiliated_exchange_or_finra": false,
                      "is_politically_exposed": false,
                      "immediate_family_exposed": false
                    },
                    "x-stoplight": {
                      "id": "h3ui3575tdh6q"
                    },
                    "properties": {
                      "employment_status": {
                        "type": "string",
                        "enum": [
                          "unemployed",
                          "employed",
                          "student",
                          "retired"
                        ],
                        "description": "One of the following: `employed`, `unemployed`, `retired`, or `student`."
                      },
                      "employer_name": {
                        "type": "string",
                        "description": "The name of the employer if the user is employed."
                      },
                      "employer_address": {
                        "type": "string",
                        "description": "The employer's address if the user is employed."
                      },
                      "employment_position": {
                        "type": "string",
                        "description": "The user's position if they are employed."
                      },
                      "employment_sector": {
                        "type": "string",
                        "description": "The industry sector of employment.\nIf the `employment_status` is `unemployed` or `student`, set this property to `not_employed`.\nIf the `employment_status` is `retired`, set this to `self_employed`.\n",
                        "enum": [
                          "agriculture",
                          "business_management",
                          "computers_and_it",
                          "construction",
                          "education",
                          "finance",
                          "government",
                          "healthcare",
                          "hospitality",
                          "manufacturing",
                          "marketing",
                          "media",
                          "other",
                          "science",
                          "self_employed",
                          "transportation",
                          "not_employed"
                        ]
                      },
                      "is_control_person": {
                        "type": "boolean",
                        "description": "Whether user holds a controlling position in a publicly traded company, member of the board of directors or has policy making abilities in a publicly traded company."
                      },
                      "is_affiliated_exchange_or_finra": {
                        "type": "boolean",
                        "description": "Whether user is affiliated with any exchanges or FINRA."
                      },
                      "is_politically_exposed": {
                        "type": "boolean",
                        "description": "Whether the user is politically exposed."
                      },
                      "immediate_family_exposed": {
                        "type": "boolean",
                        "description": "If your user’s immediate family member (sibling, husband/wife, child, parent) is either politically exposed or holds a control position."
                      },
                      "context": {
                        "type": "array",
                        "description": "Array of annotations describing the rational for marking `is_control_person`, `is_affiliated_exchange_or_finra`, and/or `immediate_family_exposed` as true",
                        "nullable": true,
                        "items": {
                          "title": "DisclosureContextAnnotation",
                          "type": "object",
                          "properties": {
                            "context_type": {
                              "type": "string",
                              "enum": [
                                "CONTROLLED_FIRM",
                                "IMMEDIATE_FAMILY_EXPOSED",
                                "AFFILIATE_FIRM"
                              ],
                              "description": "Specifies the type of disclosure annotation. Valid types are FINRA affiliations, for users affiliated with or employed by a FINRA member firm, a Stock Exchange Member, FINRA, Registered Investment Advisor, or a Municipal Securities Broker/Dealer; Company control relationships, for senior executives, and 10% or greater shareholders, of a publicly traded company; and immediate family members of politically exposed individuals."
                            },
                            "company_name": {
                              "type": "string",
                              "description": "Required for FINRA affiliations and controlled firms."
                            },
                            "company_street_address": {
                              "type": "string",
                              "description": "Required for FINRA affiliations and controlled firms."
                            },
                            "company_city": {
                              "type": "string",
                              "description": "Required for FINRA affiliations and controlled firms."
                            },
                            "company_state": {
                              "type": "string",
                              "description": "Required if and only if `company_country` is `USA`."
                            },
                            "company_country": {
                              "type": "string",
                              "description": "Required for FINRA affiliations and controlled firms."
                            },
                            "company_compliance_email": {
                              "type": "string",
                              "description": "Required for FINRA affiliations and controlled firms."
                            },
                            "given_name": {
                              "type": "string",
                              "description": "Required for immediate family members of politically exposed persons."
                            },
                            "family_name": {
                              "type": "string",
                              "description": "Required for immediate family members of politically exposed persons."
                            }
                          },
                          "required": [
                            "context_type"
                          ],
                          "x-stoplight": {
                            "id": "rf62uwbtfdfpk"
                          },
                          "x-readme-ref-name": "DisclosureContextAnnotation"
                        }
                      }
                    },
                    "required": [
                      "is_control_person",
                      "is_affiliated_exchange_or_finra",
                      "is_politically_exposed",
                      "immediate_family_exposed"
                    ],
                    "x-readme-ref-name": "Disclosures"
                  },
                  "agreements": {
                    "type": "array",
                    "description": "The client must present the Alpaca Account and Margin Agreements to the end user, and confirm they have read and agreed to the agreement.",
                    "items": {
                      "type": "object",
                      "x-stoplight": {
                        "id": "ucn8nh8ei4mag"
                      },
                      "properties": {
                        "agreement": {
                          "type": "string",
                          "title": "AgreementType",
                          "description": "- margin_agreement: Alpaca Margin Agreement\n- account_agreement: Alpaca Account Agreement\n- customer_agreement: Alpaca Customer Agreement\n- crypto_agreement: Alpaca Crypto agreement\n- options_agreement: Alpaca Option agreement\n- custodial_customer_agreement: Alpaca Custodial Customer agreement\n",
                          "enum": [
                            "margin_agreement",
                            "account_agreement",
                            "customer_agreement",
                            "crypto_agreement",
                            "options_agreement"
                          ],
                          "example": "customer_agreement",
                          "x-stoplight": {
                            "id": "pw9nog92a1hgz"
                          },
                          "x-readme-ref-name": "AgreementType"
                        },
                        "signed_at": {
                          "type": "string",
                          "example": "2019-09-11T18:09:33Z",
                          "format": "date-time",
                          "description": "The timestamp the agreement was signed."
                        },
                        "ip_address": {
                          "type": "string",
                          "format": "ipv4",
                          "example": "185.13.21.99",
                          "description": "The ip_address the signed agreements were sent from by the user."
                        },
                        "revision": {
                          "type": "string",
                          "description": "The agreement revision.\nThe format is XX.YYYY.MM where XX is an incrementing revision number, YYYY is the year and MM is the month.\nIf the revision is not specified in a POST or PATCH request, the active revision will be used, which will align with the [Alpaca Documents Library](https://alpaca.markets/disclosures).\n"
                        }
                      },
                      "required": [
                        "agreement",
                        "signed_at",
                        "ip_address"
                      ],
                      "x-readme-ref-name": "Agreement"
                    }
                  },
                  "documents": {
                    "type": "array",
                    "items": {
                      "type": "object",
                      "description": "The request to upload a document for an owner of the account",
                      "example": {
                        "document_type": "identity_verification",
                        "document_sub_type": "passport",
                        "content": "/9j/Cg==",
                        "mime_type": "image/jpeg"
                      },
                      "title": "OwnerDocumentUploadRequest",
                      "x-examples": {
                        "example-1": {
                          "document_type": "identity_verification",
                          "document_sub_type": "passport",
                          "content": "/9j/Cg==",
                          "mime_type": "image/jpeg"
                        }
                      },
                      "x-stoplight": {
                        "id": "s4kbyizjyxroo"
                      },
                      "properties": {
                        "document_type": {
                          "description": "The type of the owner document",
                          "type": "string",
                          "enum": [
                            "account_approval_letter",
                            "address_verification",
                            "cip_result",
                            "company_formation",
                            "date_of_birth_verification",
                            "entity_operating_document",
                            "entity_registration",
                            "hio_declaration_form",
                            "identity_verification",
                            "limited_trading_authorization",
                            "pep_declaration_form",
                            "tax_id_verification",
                            "w8ben",
                            "w9"
                          ],
                          "example": "identity_verification",
                          "x-stoplight": {
                            "id": "8u8j8gn6uuzk8"
                          },
                          "x-readme-ref-name": "OwnerDocumentType"
                        },
                        "document_sub_type": {
                          "type": "string",
                          "example": "passport",
                          "description": "The specific type of document, e.g. passport. This is a free-form property."
                        },
                        "content": {
                          "type": "string",
                          "format": "base64",
                          "example": "/9j/Cg==",
                          "description": "The base64 string encoding of the document contents. This property is required unless content_data is provided."
                        },
                        "content_data": {
                          "type": "object",
                          "x-examples": {
                            "Example 1": {
                              "additional_conditions": "None",
                              "country_citizen": "Australia",
                              "date": "2021-06-14",
                              "date_of_birth": "1970-01-01",
                              "foreign_tax_id": "123 456 789",
                              "ftin_not_required": false,
                              "full_name": "John Doe",
                              "ip_address": "127.0.0.1",
                              "mailing_address_city_state": "Adelaide, South Australia",
                              "mailing_address_country": "Australia",
                              "mailing_address_street": "51 Main St",
                              "paragraph_number": "15",
                              "percent_rate_withholding": 5,
                              "permanent_address_city_state": "Adelaide, South Australia",
                              "permanent_address_country": "Australia",
                              "permanent_address_street": "20 Main St",
                              "reference_number": "abc123",
                              "residency": "Australia",
                              "revision": "10-2021",
                              "tax_id_ssn": "123-00-456",
                              "timestamp": "2021-06-14T09:31:05Z",
                              "income_type": "interest",
                              "signer_full_name": "Mr. Signing User"
                            }
                          },
                          "description": "Use this property (instead of the content property) to upload W-8 BEN data in JSON format.",
                          "properties": {
                            "additional_conditions": {
                              "type": "string",
                              "description": "Any additional conditions to specify"
                            },
                            "country_citizen": {
                              "type": "string",
                              "description": "The country that the applicant is a citizen of"
                            },
                            "date": {
                              "type": "string",
                              "format": "date",
                              "description": "date signed"
                            },
                            "date_of_birth": {
                              "type": "string",
                              "format": "date",
                              "description": "date of birth of applicant"
                            },
                            "foreign_tax_id": {
                              "type": "string",
                              "description": "Applicant's tax id in their home country"
                            },
                            "ftin_not_required": {
                              "type": "boolean",
                              "description": "Required if foreign_tax_id and tax_id_ssn are empty."
                            },
                            "full_name": {
                              "type": "string",
                              "description": "Full name of applicant"
                            },
                            "ip_address": {
                              "type": "string",
                              "description": "IP address of applicant when signed"
                            },
                            "mailing_address_city_state": {
                              "type": "string",
                              "description": "Mailing city/state of applicant"
                            },
                            "mailing_address_country": {
                              "type": "string",
                              "description": "Mailing country for applicant"
                            },
                            "mailing_address_street": {
                              "type": "string",
                              "description": "Mailing street address for applicant"
                            },
                            "paragraph_number": {
                              "type": "string"
                            },
                            "percent_rate_withholding": {
                              "type": "integer"
                            },
                            "permanent_address_city_state": {
                              "type": "string",
                              "description": "Permanent city/state of applicant"
                            },
                            "permanent_address_country": {
                              "type": "string",
                              "description": "Permanent country of residence of applicant"
                            },
                            "permanent_address_street": {
                              "type": "string",
                              "description": "Permanent street address of applicant"
                            },
                            "reference_number": {
                              "type": "string"
                            },
                            "residency": {
                              "type": "string",
                              "description": "Country of residency of applicant"
                            },
                            "revision": {
                              "type": "string",
                              "description": "Revision of the W8BEN form"
                            },
                            "tax_id_ssn": {
                              "type": "string",
                              "description": "TaxID/SSN of applicant"
                            },
                            "timestamp": {
                              "type": "string",
                              "format": "time",
                              "description": "Timestamp when form data was gathered"
                            },
                            "income_type": {
                              "type": "string",
                              "description": "Income type of applicant"
                            },
                            "signer_full_name": {
                              "type": "string",
                              "description": "Full name of signing user"
                            }
                          },
                          "required": [
                            "country_citizen",
                            "date",
                            "date_of_birth",
                            "full_name",
                            "ip_address",
                            "permanent_address_city_state",
                            "permanent_address_country",
                            "permanent_address_street",
                            "revision",
                            "timestamp",
                            "signer_full_name"
                          ],
                          "x-stoplight": {
                            "id": "8cjul4ni6pe66"
                          },
                          "x-readme-ref-name": "W8benDocument"
                        },
                        "mime_type": {
                          "type": "string",
                          "example": "image/jpeg",
                          "description": "This field is required if content is specified. ENUM: application/pdf, image/png, or image/jpeg. If document_type is w8ben then application/json is also accepted"
                        }
                      },
                      "required": [
                        "document_type",
                        "content"
                      ],
                      "x-readme-ref-name": "OwnerDocumentUploadRequest"
                    }
                  },
                  "trusted_contact": {
                    "type": "object",
                    "description": "This model input is optional. However, the client should\nmake reasonable effort to obtain the trusted contact information.\nSee more details in [FINRA Notice 17-11](https://www.finra.org/sites/default/files/Regulatory-Notice-17-11.pdf)\n\nOnly one of the following is required:\n\n* email_address\t\n* phone_number\t\n* street_address\t\n",
                    "properties": {
                      "given_name": {
                        "type": "string",
                        "example": "Jane"
                      },
                      "family_name": {
                        "type": "string",
                        "example": "Doe"
                      },
                      "email_address": {
                        "type": "string",
                        "format": "email",
                        "description": "at least one of `email_address`, `phone_number` or\n`street_address` is required\n",
                        "example": "jane.doe@example.com"
                      },
                      "phone_number": {
                        "type": "string",
                        "description": "at least one of `email_address`, `phone_number` or\n`street_address` is required\n"
                      },
                      "street_address": {
                        "type": "array",
                        "items": {
                          "type": "string"
                        },
                        "description": "at least one of `email_address`, `phone_number` or\n`street_address` is required\n"
                      },
                      "city": {
                        "type": "string",
                        "description": "required if `street_address` is set\n"
                      },
                      "state": {
                        "type": "string",
                        "description": "required if `street_address` is set\n"
                      },
                      "postal_code": {
                        "type": "string",
                        "description": "required if `street_address` is set\n"
                      },
                      "country": {
                        "type": "string",
                        "description": "[ISO 3166-1 alpha-3](https://www.iso.org/iso-3166-country-codes.html).\nrequired if `street_address` is set\n"
                      }
                    },
                    "required": [
                      "given_name",
                      "family_name"
                    ],
                    "example": {
                      "given_name": "Jane",
                      "family_name": "Doe",
                      "email_address": "jane.doe@example.com"
                    },
                    "x-stoplight": {
                      "id": "fyme2rvoeickd"
                    },
                    "x-readme-ref-name": "TrustedContact"
                  },
                  "enabled_assets": {
                    "type": "array",
                    "description": "Will default to `us_equity`. Alpaca has the ability to update the default value upon request.",
                    "items": {
                      "type": "string",
                      "description": "This represents the category to which the asset belongs to. It serves to identify the nature of the financial instrument, with options including \"us_equity\" for U.S. equities, \"us_option\" for U.S. options, and \"crypto\" for cryptocurrencies.",
                      "enum": [
                        "us_equity",
                        "us_option",
                        "crypto"
                      ],
                      "x-stoplight": {
                        "id": "0stvwzkbv2e0u"
                      },
                      "x-readme-ref-name": "AssetClass"
                    }
                  },
                  "beneficiaries": {
                    "type": "array",
                    "description": "IRA Account only. A user can submit max 6 beneficiaries.",
                    "items": {
                      "type": "object",
                      "description": "Beneficiary of an account",
                      "properties": {
                        "given_name": {
                          "type": "string",
                          "example": "Jane"
                        },
                        "middle_name": {
                          "type": "string",
                          "example": "P"
                        },
                        "family_name": {
                          "type": "string",
                          "example": "Doe"
                        },
                        "date_of_birth": {
                          "type": "string",
                          "example": "1970-01-01"
                        },
                        "tax_id": {
                          "type": "string",
                          "example": "xxx-xx-xxxx"
                        },
                        "tax_id_type": {
                          "type": "string",
                          "example": "USA_SSN"
                        },
                        "relationship": {
                          "type": "string",
                          "example": "spouse"
                        },
                        "type": {
                          "type": "string",
                          "example": "primary"
                        },
                        "share_pct": {
                          "type": "string",
                          "example": "100"
                        }
                      },
                      "required": [
                        "given_name",
                        "middle_name",
                        "family_name",
                        "date_of_birth",
                        "tax_id",
                        "tax_id_type",
                        "relationship",
                        "type",
                        "share_pct"
                      ],
                      "example": {
                        "given_name": "Jane",
                        "middle_name": "P",
                        "family_name": "Doe",
                        "date_of_birth": "1970-01-01",
                        "tax_id": "xxx-xx-xxxx",
                        "tax_id_type": "USA_SSN",
                        "relationship": "spouse",
                        "type": "primary",
                        "share_pct": "100"
                      },
                      "x-readme-ref-name": "Beneficiary"
                    }
                  },
                  "trading_configurations": {
                    "title": "AccountConfigurations",
                    "type": "object",
                    "description": "Represents additional configuration settings for an account",
                    "properties": {
                      "dtbp_check": {
                        "type": "string",
                        "description": "both, entry, or exit. Controls Day Trading Margin Call (DTMC) checks.",
                        "example": "both",
                        "enum": [
                          "both",
                          "entry",
                          "exit"
                        ]
                      },
                      "trade_confirm_email": {
                        "type": "string",
                        "description": "all or none. If none, emails for order fills are not sent.",
                        "enum": [
                          "all",
                          "none"
                        ]
                      },
                      "suspend_trade": {
                        "type": "boolean",
                        "description": "If true, new orders are blocked."
                      },
                      "no_shorting": {
                        "type": "boolean",
                        "description": "If true, account becomes long-only mode."
                      },
                      "fractional_trading": {
                        "type": "boolean",
                        "description": "If true, account is able to participate in fractional trading"
                      },
                      "max_margin_multiplier": {
                        "type": "string",
                        "description": "Can be \"1\" or \"2\""
                      },
                      "max_options_trading_level": {
                        "type": "integer",
                        "description": "The desired maximum options trading level. 0=disabled, 1=Covered Call/Cash-Secured Put, 2=Long Call/Put, 3=Spreads/Straddles.",
                        "enum": [
                          0,
                          1,
                          2,
                          3
                        ]
                      },
                      "pdt_check": {
                        "type": "string",
                        "example": "entry"
                      },
                      "ptp_no_exception_entry": {
                        "type": "string",
                        "x-stoplight": {
                          "id": "b2q93748qni2e"
                        },
                        "description": "If set to true then Alpaca will accept orders for PTP symbols with no exception. Default is false."
                      },
                      "disable_overnight_trading": {
                        "type": "boolean",
                        "description": "If true, overnight trading is disabled."
                      }
                    },
                    "x-readme-ref-name": "AccountConfigurations"
                  },
                  "cash_interest": {
                    "type": "object",
                    "description": "The configuration of the account's USD cash interest program when creating an account.\nIf cash_interest is not provided and there is a default APR tier defined, that tier will be used.\nTo enroll the account in a non-default APR tier, provide the cash_interest object with the desired apr_tier_name. The status should not be specified on enrollment.\nThe response will contain a status of PENDING_CHANGE. An event showing the status change to ACTIVE will be generated when the enrollment is complete.\n",
                    "properties": {
                      "USD": {
                        "type": "object",
                        "properties": {
                          "apr_tier_name": {
                            "type": "string",
                            "description": "The unique name of the APR tier for a specific program",
                            "example": "gold"
                          },
                          "status": {
                            "type": "string",
                            "description": "The status of the account within a cash interest program. One of:\n- **ACTIVE**\nThe account is enrolled and eligible for idle cash to be swept at the end of day (EOD).\n- **INACTIVE**\nThe account is not enrolled due to it either not being eligible (e.g. the updated Alpaca Customer Agreement has not been signed), an APR tier needs to be assigned, or they have been unenrolled.\n- **PENDING_CHANGE**\nAn enrollment, APR Tier change, or unenrollment is in progress\n",
                            "example": "ACTIVE"
                          }
                        },
                        "x-readme-ref-name": "AccountCashInterestProgram"
                      }
                    },
                    "x-readme-ref-name": "AccountCashInterestPost"
                  },
                  "fpsl": {
                    "type": "object",
                    "description": "The account's Fully Paid Securities Lending (FPSL) configuration.\nTo enroll the account for a market, specify the tier_id. The status should not be specified on enrollment.\nCurrently only the US market is supported.\n",
                    "properties": {
                      "US": {
                        "type": "object",
                        "properties": {
                          "tier_id": {
                            "type": "string",
                            "format": "uuid",
                            "example": "61e69015-8549-4bfd-b9c3-01e75843f47d",
                            "description": "The id of the FPSL tier for this market"
                          }
                        },
                        "x-readme-ref-name": "AccountFPSLItemPost"
                      }
                    },
                    "x-readme-ref-name": "AccountFPSLPost"
                  },
                  "risk_tolerance": {
                    "type": "string",
                    "description": "The user's investment risk tolerance. This field should be used instead of the deprecated `risk_tolerance` under identity.\n",
                    "enum": [
                      "conservative",
                      "moderate",
                      "significant_risk"
                    ]
                  },
                  "investment_objective": {
                    "type": "string",
                    "description": "The user's investment objective. This field should be used instead of the deprecated `investment_objective` under identity.\n",
                    "enum": [
                      "generate_income",
                      "preserve_wealth",
                      "market_speculation",
                      "growth",
                      "balance_preserve_wealth_with_growth"
                    ]
                  },
                  "investment_time_horizon": {
                    "type": "string",
                    "description": "The expected period of time the user plan to invest to achieve his/her financial goal(s). This field should be used instead of the deprecated `investment_time_horizon` under identity.\n",
                    "enum": [
                      "less_than_1_year",
                      "1_to_2_years",
                      "3_to_5_years",
                      "6_to_10_years",
                      "more_than_10_years"
                    ]
                  },
                  "liquidity_needs": {
                    "type": "string",
                    "description": "The user's ability to quickly and easily convert to cash all or a portion of the investments in this account without experiencing significant loss in value. This field should be used instead of the deprecated `liquidity_needs` under identity.\n",
                    "enum": [
                      "very_important",
                      "important",
                      "somewhat_important",
                      "does_not_matter"
                    ]
                  }
                },
                "required": [
                  "contact",
                  "identity",
                  "disclosures",
                  "agreements"
                ],
                "x-readme-ref-name": "AccountCreationRequest"
              }
            }
          }
        },
        "responses": {
          "200": {
            "description": "OK",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "description": "Represents high level account info. Used when returning entire account information would not be useful like the getAllAccounts operation",
                  "x-examples": {
                    "example-1": {
                      "id": "0d18ae51-3c94-4511-b209-101e1666416b",
                      "account_number": "9034005019",
                      "status": "APPROVED",
                      "currency": "USD",
                      "created_at": "2019-09-30T23:55:31.185998Z",
                      "last_equity": "1500.65"
                    }
                  },
                  "x-stoplight": {
                    "id": "mg5a9g65p0k72"
                  },
                  "properties": {
                    "id": {
                      "type": "string",
                      "format": "uuid",
                      "description": "UUID that identifies the account for later reference"
                    },
                    "account_number": {
                      "type": "string",
                      "description": "A human-readable account number that can be shown to the end user",
                      "nullable": true
                    },
                    "account_type": {
                      "type": "string",
                      "title": "AccountType",
                      "description": "Possible values are:\n\n- trading\n- custodial\n- donor_advised\n- ira",
                      "enum": [
                        "trading",
                        "custodial",
                        "donor_advised",
                        "ira"
                      ],
                      "example": "trading",
                      "x-readme-ref-name": "AccountType"
                    },
                    "status": {
                      "type": "string",
                      "example": "ACTIVE",
                      "enum": [
                        "INACTIVE",
                        "ONBOARDING",
                        "SUBMITTED",
                        "SUBMISSION_FAILED",
                        "ACTION_REQUIRED",
                        "ACCOUNT_UPDATED",
                        "APPROVAL_PENDING",
                        "APPROVED",
                        "REJECTED",
                        "ACTIVE",
                        "ACCOUNT_CLOSED"
                      ],
                      "description": "Designates the current status of this account\n\nPossible Values:\n- **INACTIVE**\nAccount not set to trade given asset.\n- **ONBOARDING**\nAn application is expected for this user, but has not been submitted yet.\n- **SUBMITTED**\nThe application has been submitted and in process.\n- **SUBMISSION_FAILED**\nUsed to display if failure on submission\n- **ACTION_REQUIRED**\nThe application requires manual action.\n- **ACCOUNT_UPDATED**\nUsed to display when Account has been modified by user\n- **APPROVAL_PENDING**\nInitial value. The application approval process is in process.\n- **APPROVED**\nThe account application has been approved, and waiting to be ACTIVE\n- **REJECTED**\nThe account application is rejected for some reason\n- **ACTIVE**\nThe account is fully active. Trading and funding are processed under this status.\n- **ACCOUNT_CLOSED**\nThe account is closed.\n",
                      "x-stoplight": {
                        "id": "zxsbg55ojatc8"
                      },
                      "x-readme-ref-name": "AccountStatus"
                    },
                    "crypto_status": {
                      "type": "string",
                      "example": "ACTIVE",
                      "enum": [
                        "INACTIVE",
                        "ONBOARDING",
                        "SUBMITTED",
                        "SUBMISSION_FAILED",
                        "ACTION_REQUIRED",
                        "ACCOUNT_UPDATED",
                        "APPROVAL_PENDING",
                        "APPROVED",
                        "REJECTED",
                        "ACTIVE",
                        "ACCOUNT_CLOSED"
                      ],
                      "description": "Designates the current status of this account\n\nPossible Values:\n- **INACTIVE**\nAccount not set to trade given asset.\n- **ONBOARDING**\nAn application is expected for this user, but has not been submitted yet.\n- **SUBMITTED**\nThe application has been submitted and in process.\n- **SUBMISSION_FAILED**\nUsed to display if failure on submission\n- **ACTION_REQUIRED**\nThe application requires manual action.\n- **ACCOUNT_UPDATED**\nUsed to display when Account has been modified by user\n- **APPROVAL_PENDING**\nInitial value. The application approval process is in process.\n- **APPROVED**\nThe account application has been approved, and waiting to be ACTIVE\n- **REJECTED**\nThe account application is rejected for some reason\n- **ACTIVE**\nThe account is fully active. Trading and funding are processed under this status.\n- **ACCOUNT_CLOSED**\nThe account is closed.\n",
                      "x-stoplight": {
                        "id": "zxsbg55ojatc8"
                      },
                      "x-readme-ref-name": "AccountStatus"
                    },
                    "currency": {
                      "title": "Currency",
                      "x-stoplight": {
                        "id": "go8dbrpz277wf"
                      },
                      "type": "string",
                      "description": "\"USD\" // US Dollar\n\"JPY\" // Japanese Yen\n\"EUR\" // Euro\n\"CAD\" // Canadian Dollar\n\"GBP\" // British Pound Sterling\n\"CHF\" // Swiss Franc\n\"TRY\" // Turkish Lira\n\"AUD\" // Australian Dollar\n\"CZK\" // Czech Koruna\n\"SEK\" // Swedish Krona\n\"DKK\" // Danish Krone\n\"SGD\" // Singapore Dollar\n\"HKD\" // Hong Kong Dollar\n\"HUF\" // Hungarian Forint\n\"NZD\" // New Zealand Dollar\n\"NOK\" // Norwegian Krone\n\"PLN\" // Poland Złoty",
                      "x-readme-ref-name": "Currency"
                    },
                    "created_at": {
                      "type": "string",
                      "format": "date-time",
                      "description": "Timestamp (RFC3339) of account creation."
                    },
                    "last_equity": {
                      "type": "string",
                      "format": "decimal",
                      "description": "EOD equity calculation (cash + long market value + short market value)"
                    },
                    "enabled_assets": {
                      "x-stoplight": {
                        "id": "44f1cfyta748h"
                      },
                      "type": "array",
                      "description": "Assets the user has enabled and is able to trade once status and/or crypto_status are ACTIVE",
                      "items": {
                        "type": "string",
                        "description": "This represents the category to which the asset belongs to. It serves to identify the nature of the financial instrument, with options including \"us_equity\" for U.S. equities, \"us_option\" for U.S. options, and \"crypto\" for cryptocurrencies.",
                        "enum": [
                          "us_equity",
                          "us_option",
                          "crypto"
                        ],
                        "x-stoplight": {
                          "id": "0stvwzkbv2e0u"
                        },
                        "x-readme-ref-name": "AssetClass"
                      }
                    },
                    "contact": {
                      "type": "object",
                      "description": "Contact is the model for the account owner contact information.\n",
                      "x-stoplight": {
                        "id": "qcig9irpj9334"
                      },
                      "properties": {
                        "email_address": {
                          "type": "string",
                          "format": "email",
                          "example": "john.doe@example.com"
                        },
                        "phone_number": {
                          "type": "string",
                          "example": "+15556667788",
                          "description": "Phone number should include the country code, format: “+15555555555”"
                        },
                        "street_address": {
                          "type": "array",
                          "description": "The user's street address. If multiple lines in address, pass in as additional array elements. Maximum of 3 objects in array",
                          "items": {
                            "type": "string",
                            "example": "20 N San Mateo Dr",
                            "x-stoplight": {
                              "id": "10wajx98hc79a"
                            },
                            "x-readme-ref-name": "StreetAddress"
                          }
                        },
                        "unit": {
                          "type": "string",
                          "x-stoplight": {
                            "id": "yybrq2o2nb5gy"
                          },
                          "description": "The specific apartment number if applicable"
                        },
                        "city": {
                          "type": "string",
                          "example": "San Mateo"
                        },
                        "state": {
                          "type": "string",
                          "example": "CA",
                          "description": "Required if the country or country_of_tax_residence (in the identity model below) is 'USA'."
                        },
                        "country": {
                          "type": "string",
                          "example": "USA",
                          "description": "country code in ISO 3166-1 alpha-3 format, representing the country the person/entity resides in."
                        },
                        "postal_code": {
                          "type": "string",
                          "example": "94401"
                        }
                      },
                      "required": [
                        "email_address",
                        "phone_number",
                        "street_address",
                        "city"
                      ],
                      "x-readme-ref-name": "Contact"
                    },
                    "identity": {
                      "type": "object",
                      "description": "Identity is the model to provide account owner’s identity information.\n",
                      "example": {
                        "given_name": "John",
                        "family_name": "Doe",
                        "date_of_birth": "1990-01-01",
                        "tax_id": "666-55-4321",
                        "tax_id_type": "USA_SSN",
                        "country_of_citizenship": "AUS",
                        "country_of_birth": "AUS",
                        "country_of_tax_residence": "USA",
                        "funding_source": [
                          "employment_income"
                        ]
                      },
                      "x-stoplight": {
                        "id": "oi43k8rpw570e"
                      },
                      "properties": {
                        "given_name": {
                          "type": "string",
                          "example": "John",
                          "description": "The first/given name of the user."
                        },
                        "family_name": {
                          "type": "string",
                          "example": "Doe",
                          "description": "The last name (surname) of the user."
                        },
                        "middle_name": {
                          "type": "string",
                          "x-stoplight": {
                            "id": "p03brcsyyjbcq"
                          },
                          "description": "The middle name of the user."
                        },
                        "date_of_birth": {
                          "type": "string",
                          "format": "date",
                          "example": "1990-01-01",
                          "description": "The date of birth in \"YYYY-MM-DD\" format."
                        },
                        "tax_id": {
                          "type": "string",
                          "example": "666-55-4321",
                          "description": "Required if tax_id_type is set."
                        },
                        "tax_id_type": {
                          "type": "string",
                          "title": "TaxIdType",
                          "enum": [
                            "USA_SSN",
                            "USA_ITIN",
                            "ARG_AG_CUIT",
                            "AUS_TFN",
                            "AUS_ABN",
                            "BOL_NIT",
                            "BRA_CPF",
                            "CHL_RUT",
                            "COL_NIT",
                            "CRI_NITE",
                            "DEU_TAX_ID",
                            "DOM_RNC",
                            "ECU_RUC",
                            "FRA_SPI",
                            "GBR_UTR",
                            "GBR_NINO",
                            "GTM_NIT",
                            "HND_RTN",
                            "HUN_TIN",
                            "IDN_KTP",
                            "IND_PAN",
                            "ISR_TAX_ID",
                            "ITA_TAX_ID",
                            "JPN_TAX_ID",
                            "MEX_RFC",
                            "NIC_RUC",
                            "NLD_TIN",
                            "PAN_RUC",
                            "PER_RUC",
                            "PRY_RUC",
                            "SGP_NRIC",
                            "SGP_FIN",
                            "SGP_ASGD",
                            "SGP_ITR",
                            "SLV_NIT",
                            "SWE_TAX_ID",
                            "URY_RUT",
                            "VEN_RIF",
                            "NATIONAL_ID",
                            "PASSPORT",
                            "PERMANENT_RESIDENT",
                            "DRIVER_LICENSE",
                            "OTHER_GOV_ID",
                            "NOT_SPECIFIED"
                          ],
                          "description": "Required if `tax_id` is set.\n\nAn Enum of the various kinds of Tax ID formats Alpaca supports.\n\nPossible Values are:\n\n\n- **USA_SSN**\nUSA Social Security Number\n\n- **USA_ITIN**\nUSA Individual Taxpayer Identification Number\n\n- **ARG_AR_CUIT**\nArgentina CUIT\n\n- **AUS_TFN**\nAustralian Tax File Number\n\n- **AUS_ABN**\nAustralian Business Number\n\n- **BOL_NIT**\nBolivia NIT\n\n- **BRA_CPF**\nBrazil CPF\n\n- **CHL_RUT**\nChile RUT\n\n- **COL_NIT**\nColombia NIT\n\n- **CRI_NITE**\nCosta Rica NITE\n\n- **DEU_TAX_ID**\nGermany Tax ID (Identifikationsnummer)\n\n- **DOM_RNC**\nDominican Republic RNC\n\n- **ECU_RUC**\nEcuador RUC\n\n- **FRA_SPI**\nFrance SPI (Reference Tax Number)\n\n- **GBR_UTR**\nUK UTR (Unique Taxpayer Reference)\n\n- **GBR_NINO**\nUK NINO (National Insurance Number)\n\n- **GTM_NIT**\nGuatemala NIT\n\n- **HND_RTN**\nHonduras RTN\n\n- **HUN_TIN**\nHungary TIN Number\n\n- **IDN_KTP**\nIndonesia KTP\n\n- **IND_PAN**\nIndia PAN Number\n\n- **ISR_TAX_ID**\nIsrael Tax ID (Teudat Zehut)\n\n- **ITA_TAX_ID**\nItaly Tax ID (Codice Fiscale)\n\n- **JPN_TAX_ID**\nJapan Tax ID (Koijin Bango)\n\n- **MEX_RFC**\nMexico RFC\n\n- **NIC_RUC**\nNicaragua RUC\n\n- **NLD_TIN**\nNetherlands TIN Number\n\n- **PAN_RUC**\nPanama RUC\n\n- **PER_RUC**\nPeru RUC\n\n- **PRY_RUC**\nParaguay RUC\n\n- **SGP_NRIC**\nSingapore NRIC\n\n- **SGP_FIN**\nSingapore FIN\n\n- **SGP_ASGD**\nSingapore ASGD\n\n- **SGP_ITR**\nSingapore ITR\n\n- **SLV_NIT**\nEl Salvador NIT\n\n- **SWE_TAX_ID**\nSweden Tax ID (Personnummer)\n\n- **URY_RUT**\nUruguay RUT\n\n- **VEN_RIF**\nVenezuela RIF\n\n- **NATIONAL_ID**\nNational ID number, if a tax ID number is not available\n\n- **PASSPORT**\nPassport number, if a tax ID number is not available\n\n- **PERMANENT_RESIDENT**\nPermanent resident number, if a tax ID number is not available\n\n- **DRIVER_LICENSE**\nDrivers license number, if a tax ID number is not available\n\n- **OTHER_GOV_ID**\nOther government issued identifier, if a tax ID number is not available\n\n- **NOT_SPECIFIED**\nOther Tax IDs",
                          "example": "USA_SSN",
                          "x-stoplight": {
                            "id": "ulm45kpr2peox"
                          },
                          "x-readme-ref-name": "TaxIdType"
                        },
                        "country_of_citizenship": {
                          "type": "string",
                          "description": "[ISO 3166-1 alpha-3](https://www.iso.org/iso-3166-country-codes.html).\n",
                          "example": "USA"
                        },
                        "country_of_birth": {
                          "type": "string",
                          "description": "[ISO 3166-1 alpha-3](https://www.iso.org/iso-3166-country-codes.html).\n",
                          "example": "USA"
                        },
                        "country_of_tax_residence": {
                          "type": "string",
                          "description": "[ISO 3166-1 alpha-3](https://www.iso.org/iso-3166-country-codes.html).\n",
                          "example": "USA"
                        },
                        "funding_source": {
                          "type": "array",
                          "description": "Can be one or more of the following: `employment_income`, `investments`, `inheritance`, `business_income`, `savings`, `family`.",
                          "items": {
                            "type": "string",
                            "enum": [
                              "employment_income",
                              "investments",
                              "inheritance",
                              "business_income",
                              "savings",
                              "family"
                            ]
                          }
                        },
                        "liquidity_needs": {
                          "type": "string",
                          "description": "The user's ability to quickly and easily convert all or part of their investments in this account to cash without significant loss in value. This field is deprecated. Please use the top level `liquidity_needs` field.\n",
                          "enum": [
                            "very_important",
                            "important",
                            "somewhat_important",
                            "does_not_matter"
                          ],
                          "deprecated": true
                        },
                        "investment_experience_with_stocks": {
                          "type": "string",
                          "description": "The user's level of expertise and familiarity with investing in US Equities.\n",
                          "enum": [
                            "none",
                            "1_to_5_years",
                            "over_5_years"
                          ]
                        },
                        "investment_experience_with_options": {
                          "type": "string",
                          "description": "The user's level of expertise and familiarity with investing in Options.\n",
                          "enum": [
                            "none",
                            "1_to_5_years",
                            "over_5_years"
                          ]
                        },
                        "risk_tolerance": {
                          "type": "string",
                          "description": "The user's investment risk tolerance. This field is deprecated. Please use the top level `risk_tolerance` field.\n",
                          "enum": [
                            "conservative",
                            "moderate",
                            "significant_risk"
                          ],
                          "deprecated": true
                        },
                        "investment_objective": {
                          "type": "string",
                          "description": "The user's investment objective. This field is deprecated. Please use the top level `investment_objective` field.\n",
                          "enum": [
                            "generate_income",
                            "preserve_wealth",
                            "market_speculation",
                            "growth",
                            "balance_preserve_wealth_with_growth"
                          ],
                          "deprecated": true
                        },
                        "investment_time_horizon": {
                          "type": "string",
                          "description": "The expected period of time the user plan to invest to achieve his/her financial goal(s). This field is deprecated. Please use the top level `investment_time_horizon` field.\n",
                          "enum": [
                            "less_than_1_year",
                            "1_to_2_years",
                            "3_to_5_years",
                            "6_to_10_years",
                            "more_than_10_years"
                          ],
                          "deprecated": true
                        },
                        "annual_income_min": {
                          "type": "number",
                          "description": "The lower bound of the user's annual income."
                        },
                        "annual_income_max": {
                          "type": "number",
                          "description": "The upper bound of the user's annual income."
                        },
                        "liquid_net_worth_min": {
                          "type": "number",
                          "description": "The lower bound of the user's liquid net worth."
                        },
                        "liquid_net_worth_max": {
                          "type": "number",
                          "description": "The upper bound of the user's liquid net worth."
                        },
                        "total_net_worth_min": {
                          "type": "number",
                          "description": "The lower bound of the user's total net worth."
                        },
                        "total_net_worth_max": {
                          "type": "number",
                          "description": "The upper bound of the user's total net worth."
                        },
                        "visa_type": {
                          "type": "string",
                          "x-stoplight": {
                            "id": "y5a5r7inu02w8"
                          },
                          "description": "Only used to collect visa types for users residing in the USA."
                        },
                        "visa_expiration_date": {
                          "type": "string",
                          "x-stoplight": {
                            "id": "q7b33k53b5alk"
                          },
                          "description": "Required if `visa_type` is set.",
                          "format": "date"
                        },
                        "date_of_departure_from_usa": {
                          "type": "string",
                          "x-stoplight": {
                            "id": "yasik2wcmshea"
                          },
                          "format": "date",
                          "description": "Required if `visa_type` = B1 or B2"
                        },
                        "permanent_resident": {
                          "type": "boolean",
                          "x-stoplight": {
                            "id": "jlvzbu3cevmju"
                          },
                          "description": "Only used to collect permanent residence status in the USA."
                        },
                        "marital_status": {
                          "type": "string",
                          "description": "The marital status of the user.\n",
                          "enum": [
                            "SINGLE",
                            "MARRIED",
                            "DIVORCED",
                            "WIDOWED"
                          ]
                        },
                        "number_of_dependents": {
                          "type": "integer",
                          "description": "The number of dependents the user has.\n"
                        }
                      },
                      "required": [
                        "given_name",
                        "family_name",
                        "date_of_birth",
                        "tax_id_type",
                        "country_of_tax_residence",
                        "funding_source"
                      ],
                      "x-readme-ref-name": "Identity"
                    },
                    "disclosures": {
                      "type": "object",
                      "description": "Disclosures fields denote if the account owner falls under\neach category defined by FINRA rule. The client has to ask\nquestions for the end user and the values should reflect\ntheir answers.\nIf one of the answers is true (yes), the account goes into\nACTION_REQUIRED status.\n",
                      "example": {
                        "is_control_person": false,
                        "is_affiliated_exchange_or_finra": false,
                        "is_politically_exposed": false,
                        "immediate_family_exposed": false
                      },
                      "x-stoplight": {
                        "id": "h3ui3575tdh6q"
                      },
                      "properties": {
                        "employment_status": {
                          "type": "string",
                          "enum": [
                            "unemployed",
                            "employed",
                            "student",
                            "retired"
                          ],
                          "description": "One of the following: `employed`, `unemployed`, `retired`, or `student`."
                        },
                        "employer_name": {
                          "type": "string",
                          "description": "The name of the employer if the user is employed."
                        },
                        "employer_address": {
                          "type": "string",
                          "description": "The employer's address if the user is employed."
                        },
                        "employment_position": {
                          "type": "string",
                          "description": "The user's position if they are employed."
                        },
                        "employment_sector": {
                          "type": "string",
                          "description": "The industry sector of employment.\nIf the `employment_status` is `unemployed` or `student`, set this property to `not_employed`.\nIf the `employment_status` is `retired`, set this to `self_employed`.\n",
                          "enum": [
                            "agriculture",
                            "business_management",
                            "computers_and_it",
                            "construction",
                            "education",
                            "finance",
                            "government",
                            "healthcare",
                            "hospitality",
                            "manufacturing",
                            "marketing",
                            "media",
                            "other",
                            "science",
                            "self_employed",
                            "transportation",
                            "not_employed"
                          ]
                        },
                        "is_control_person": {
                          "type": "boolean",
                          "description": "Whether user holds a controlling position in a publicly traded company, member of the board of directors or has policy making abilities in a publicly traded company."
                        },
                        "is_affiliated_exchange_or_finra": {
                          "type": "boolean",
                          "description": "Whether user is affiliated with any exchanges or FINRA."
                        },
                        "is_politically_exposed": {
                          "type": "boolean",
                          "description": "Whether the user is politically exposed."
                        },
                        "immediate_family_exposed": {
                          "type": "boolean",
                          "description": "If your user’s immediate family member (sibling, husband/wife, child, parent) is either politically exposed or holds a control position."
                        },
                        "context": {
                          "type": "array",
                          "description": "Array of annotations describing the rational for marking `is_control_person`, `is_affiliated_exchange_or_finra`, and/or `immediate_family_exposed` as true",
                          "nullable": true,
                          "items": {
                            "title": "DisclosureContextAnnotation",
                            "type": "object",
                            "properties": {
                              "context_type": {
                                "type": "string",
                                "enum": [
                                  "CONTROLLED_FIRM",
                                  "IMMEDIATE_FAMILY_EXPOSED",
                                  "AFFILIATE_FIRM"
                                ],
                                "description": "Specifies the type of disclosure annotation. Valid types are FINRA affiliations, for users affiliated with or employed by a FINRA member firm, a Stock Exchange Member, FINRA, Registered Investment Advisor, or a Municipal Securities Broker/Dealer; Company control relationships, for senior executives, and 10% or greater shareholders, of a publicly traded company; and immediate family members of politically exposed individuals."
                              },
                              "company_name": {
                                "type": "string",
                                "description": "Required for FINRA affiliations and controlled firms."
                              },
                              "company_street_address": {
                                "type": "string",
                                "description": "Required for FINRA affiliations and controlled firms."
                              },
                              "company_city": {
                                "type": "string",
                                "description": "Required for FINRA affiliations and controlled firms."
                              },
                              "company_state": {
                                "type": "string",
                                "description": "Required if and only if `company_country` is `USA`."
                              },
                              "company_country": {
                                "type": "string",
                                "description": "Required for FINRA affiliations and controlled firms."
                              },
                              "company_compliance_email": {
                                "type": "string",
                                "description": "Required for FINRA affiliations and controlled firms."
                              },
                              "given_name": {
                                "type": "string",
                                "description": "Required for immediate family members of politically exposed persons."
                              },
                              "family_name": {
                                "type": "string",
                                "description": "Required for immediate family members of politically exposed persons."
                              }
                            },
                            "required": [
                              "context_type"
                            ],
                            "x-stoplight": {
                              "id": "rf62uwbtfdfpk"
                            },
                            "x-readme-ref-name": "DisclosureContextAnnotation"
                          }
                        }
                      },
                      "required": [
                        "is_control_person",
                        "is_affiliated_exchange_or_finra",
                        "is_politically_exposed",
                        "immediate_family_exposed"
                      ],
                      "x-readme-ref-name": "Disclosures"
                    },
                    "documents": {
                      "description": "The documents associated with the primary owner of the account",
                      "type": "array",
                      "x-stoplight": {
                        "id": "w22zyoy6wxhbd"
                      },
                      "items": {
                        "type": "object",
                        "description": "A document associated with an owner of the account",
                        "properties": {
                          "id": {
                            "type": "string",
                            "format": "uuid"
                          },
                          "document_type": {
                            "description": "The type of the owner document",
                            "type": "string",
                            "enum": [
                              "account_approval_letter",
                              "address_verification",
                              "cip_result",
                              "company_formation",
                              "date_of_birth_verification",
                              "entity_operating_document",
                              "entity_registration",
                              "hio_declaration_form",
                              "identity_verification",
                              "limited_trading_authorization",
                              "pep_declaration_form",
                              "tax_id_verification",
                              "w8ben",
                              "w9"
                            ],
                            "example": "identity_verification",
                            "x-stoplight": {
                              "id": "8u8j8gn6uuzk8"
                            },
                            "x-readme-ref-name": "OwnerDocumentType"
                          },
                          "document_sub_type": {
                            "description": "The sub-type of the document. This is a free-form property.",
                            "type": "string"
                          },
                          "mime_type": {
                            "type": "string"
                          },
                          "created_at": {
                            "type": "string",
                            "format": "date-time"
                          }
                        },
                        "required": [
                          "id",
                          "document_type",
                          "created_at"
                        ],
                        "example": {
                          "id": "0d18ae51-3c94-4511-b209-101e1666416b",
                          "document_type": "identity_verification",
                          "document_sub_type": "passport",
                          "mime_type": "image/jpeg",
                          "created_at": "2019-09-30T23:55:31.185998Z"
                        },
                        "x-stoplight": {
                          "id": "6jkqogvv3l151"
                        },
                        "x-readme-ref-name": "OwnerDocument"
                      }
                    },
                    "agreements": {
                      "type": "array",
                      "x-stoplight": {
                        "id": "6igg6t87mkteb"
                      },
                      "items": {
                        "type": "object",
                        "x-stoplight": {
                          "id": "ucn8nh8ei4mag"
                        },
                        "properties": {
                          "agreement": {
                            "type": "string",
                            "title": "AgreementType",
                            "description": "- margin_agreement: Alpaca Margin Agreement\n- account_agreement: Alpaca Account Agreement\n- customer_agreement: Alpaca Customer Agreement\n- crypto_agreement: Alpaca Crypto agreement\n- options_agreement: Alpaca Option agreement\n- custodial_customer_agreement: Alpaca Custodial Customer agreement\n",
                            "enum": [
                              "margin_agreement",
                              "account_agreement",
                              "customer_agreement",
                              "crypto_agreement",
                              "options_agreement"
                            ],
                            "example": "customer_agreement",
                            "x-stoplight": {
                              "id": "pw9nog92a1hgz"
                            },
                            "x-readme-ref-name": "AgreementType"
                          },
                          "signed_at": {
                            "type": "string",
                            "example": "2019-09-11T18:09:33Z",
                            "format": "date-time",
                            "description": "The timestamp the agreement was signed."
                          },
                          "ip_address": {
                            "type": "string",
                            "format": "ipv4",
                            "example": "185.13.21.99",
                            "description": "The ip_address the signed agreements were sent from by the user."
                          },
                          "revision": {
                            "type": "string",
                            "description": "The agreement revision.\nThe format is XX.YYYY.MM where XX is an incrementing revision number, YYYY is the year and MM is the month.\nIf the revision is not specified in a POST or PATCH request, the active revision will be used, which will align with the [Alpaca Documents Library](https://alpaca.markets/disclosures).\n"
                          }
                        },
                        "required": [
                          "agreement",
                          "signed_at",
                          "ip_address"
                        ],
                        "x-readme-ref-name": "Agreement"
                      }
                    },
                    "trusted_contact": {
                      "type": "object",
                      "description": "This model input is optional. However, the client should\nmake reasonable effort to obtain the trusted contact information.\nSee more details in [FINRA Notice 17-11](https://www.finra.org/sites/default/files/Regulatory-Notice-17-11.pdf)\n\nOnly one of the following is required:\n\n* email_address\t\n* phone_number\t\n* street_address\t\n",
                      "properties": {
                        "given_name": {
                          "type": "string",
                          "example": "Jane"
                        },
                        "family_name": {
                          "type": "string",
                          "example": "Doe"
                        },
                        "email_address": {
                          "type": "string",
                          "format": "email",
                          "description": "at least one of `email_address`, `phone_number` or\n`street_address` is required\n",
                          "example": "jane.doe@example.com"
                        },
                        "phone_number": {
                          "type": "string",
                          "description": "at least one of `email_address`, `phone_number` or\n`street_address` is required\n"
                        },
                        "street_address": {
                          "type": "array",
                          "items": {
                            "type": "string"
                          },
                          "description": "at least one of `email_address`, `phone_number` or\n`street_address` is required\n"
                        },
                        "city": {
                          "type": "string",
                          "description": "required if `street_address` is set\n"
                        },
                        "state": {
                          "type": "string",
                          "description": "required if `street_address` is set\n"
                        },
                        "postal_code": {
                          "type": "string",
                          "description": "required if `street_address` is set\n"
                        },
                        "country": {
                          "type": "string",
                          "description": "[ISO 3166-1 alpha-3](https://www.iso.org/iso-3166-country-codes.html).\nrequired if `street_address` is set\n"
                        }
                      },
                      "required": [
                        "given_name",
                        "family_name"
                      ],
                      "example": {
                        "given_name": "Jane",
                        "family_name": "Doe",
                        "email_address": "jane.doe@example.com"
                      },
                      "x-stoplight": {
                        "id": "fyme2rvoeickd"
                      },
                      "x-readme-ref-name": "TrustedContact"
                    },
                    "cash_interest": {
                      "type": "object",
                      "description": "The configuration and status of the account's USD cash interest program\n",
                      "properties": {
                        "USD": {
                          "type": "object",
                          "properties": {
                            "apr_tier_name": {
                              "type": "string",
                              "description": "The unique name of the APR tier for a specific program",
                              "example": "gold"
                            },
                            "status": {
                              "type": "string",
                              "description": "The status of the account within a cash interest program. One of:\n- **ACTIVE**\nThe account is enrolled and eligible for idle cash to be swept at the end of day (EOD).\n- **INACTIVE**\nThe account is not enrolled due to it either not being eligible (e.g. the updated Alpaca Customer Agreement has not been signed), an APR tier needs to be assigned, or they have been unenrolled.\n- **PENDING_CHANGE**\nAn enrollment, APR Tier change, or unenrollment is in progress\n",
                              "example": "ACTIVE"
                            }
                          },
                          "x-readme-ref-name": "AccountCashInterestProgram"
                        }
                      },
                      "x-readme-ref-name": "AccountCashInterestResponse"
                    },
                    "fpsl": {
                      "type": "object",
                      "description": "The account's Fully Paid Securities Lending (FPSL) configuration.\nThis is only returned for accounts that have FPSL enabled.\n",
                      "properties": {
                        "US": {
                          "type": "object",
                          "properties": {
                            "tier_id": {
                              "type": "string",
                              "format": "uuid",
                              "example": "61e69015-8549-4bfd-b9c3-01e75843f47d",
                              "description": "The id of the FPSL tier for this market"
                            },
                            "status": {
                              "type": "string",
                              "description": "The status of the account for this FPSL market. One of:\n- **ACTIVE**\nThe account is successfully enrolled for FPSL for this market.\n- **INACTIVE**\nThe account is not enrolled for FPSL for this market due to it either not being eligible, an FPSL tier has not been assigned, or it has been unenrolled.\n",
                              "example": "ACTIVE"
                            }
                          },
                          "x-readme-ref-name": "AccountFPSLItem"
                        }
                      },
                      "x-readme-ref-name": "AccountFPSLResponse"
                    }
                  },
                  "required": [
                    "id",
                    "account_number",
                    "status",
                    "currency",
                    "created_at",
                    "last_equity"
                  ],
                  "x-readme-ref-name": "Account"
                }
              }
            }
          },
          "400": {
            "description": "The post body is not well formed.",
            "content": {
              "application/json": {
                "schema": {
                  "type": "string"
                }
              }
            }
          },
          "409": {
            "description": "There is already an existing account registered with the same email address."
          },
          "422": {
            "description": "One of the input values is not a valid value.",
            "content": {
              "application/json": {
                "schema": {
                  "type": "string"
                }
              }
            }
          }
        },
        "operationId": "createAccount",
        "description": "Submit an account application with KYC information. This will create a trading account for the end user. The account status may or may not be ACTIVE immediately and you will receive account status updates on the event API. "
      }
    }
  },
  "security": [
    {
      "BasicAuth": []
    }
  ],
  "x-readme": {
    "explorer-enabled": true,
    "proxy-enabled": false
  }
}
```
