---
source_view: https://docs.alpaca.markets/reference/suscribetoaccountstatussse
source_md: https://docs.alpaca.markets/reference/suscribetoaccountstatussse.md
scraped_at_utc: 2026-01-27T04:30:48Z
---
# Subscribe to Account Status Events (SSE)

The accounts events API provides streaming of account changes as they occur, via SSE (server sent events). Past events can also be queried.

Events are generated for changes to the following account properties:
- account_blocked
- admin_configurations
- cash_interest
- crypto_status
- kyc_results
- options
- pattern_day_trader
- status
- trading_blocked

Only the changed properties are included in the event payload.

Query Parameter Rules:
- `since` is required if `until` specified
- `since_id` is required if `until_id` specified
- `since_ulid` is required if `until_ulid` specified
- `since`, `since_id` and `since_ulid` can’t be used at the same time

Behavior:
This API supports querying a range of events, starting now or in the past. If the end of the range is in the future or not specified, the connection is kept open and future events are pushed.

To be specific:
- if `since`, `since_id` or `since_ulid` is not specified, this will not return any historic data
- if `until`, `until_id` or `until_ulid` is reached, the stream will end with a status of 200

---

Note for people using the clients generated from this OAS spec. Currently OAS-3 doesn't have full support for representing SSE style responses from an API, so if you are using a generated client and don't specify a `since` and `until` there is a good chance the generated clients will hang waiting for the response to end.

If you require the streaming capabilities we recommend not using the generated clients for this specific usecase until the OAS-3 standards come to a consensus on how to represent this correctly in OAS-3.


# OpenAPI definition

````json
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
      "name": "Events"
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
    "/v1/events/accounts/status": {
      "get": {
        "summary": "Subscribe to Account Status Events (SSE)",
        "tags": [
          "Events"
        ],
        "description": "The accounts events API provides streaming of account changes as they occur, via SSE (server sent events). Past events can also be queried.\n\nEvents are generated for changes to the following account properties:\n- account_blocked\n- admin_configurations\n- cash_interest\n- crypto_status\n- kyc_results\n- options\n- pattern_day_trader\n- status\n- trading_blocked\n\nOnly the changed properties are included in the event payload.\n\nQuery Parameter Rules:\n- `since` is required if `until` specified\n- `since_id` is required if `until_id` specified\n- `since_ulid` is required if `until_ulid` specified\n- `since`, `since_id` and `since_ulid` can’t be used at the same time\n\nBehavior:\nThis API supports querying a range of events, starting now or in the past. If the end of the range is in the future or not specified, the connection is kept open and future events are pushed.\n\nTo be specific:\n- if `since`, `since_id` or `since_ulid` is not specified, this will not return any historic data\n- if `until`, `until_id` or `until_ulid` is reached, the stream will end with a status of 200\n\n---\n\nNote for people using the clients generated from this OAS spec. Currently OAS-3 doesn't have full support for representing SSE style responses from an API, so if you are using a generated client and don't specify a `since` and `until` there is a good chance the generated clients will hang waiting for the response to end.\n\nIf you require the streaming capabilities we recommend not using the generated clients for this specific usecase until the OAS-3 standards come to a consensus on how to represent this correctly in OAS-3.\n",
        "parameters": [
          {
            "name": "since",
            "in": "query",
            "schema": {
              "type": "string",
              "format": "date"
            },
            "description": "Format: YYYY-MM-DD"
          },
          {
            "name": "until",
            "in": "query",
            "schema": {
              "type": "string",
              "format": "date"
            },
            "description": "Format: YYYY-MM-DD"
          },
          {
            "name": "since_id",
            "in": "query",
            "schema": {
              "type": "integer"
            }
          },
          {
            "name": "until_id",
            "in": "query",
            "schema": {
              "type": "integer"
            }
          },
          {
            "name": "since_ulid",
            "in": "query",
            "schema": {
              "type": "string",
              "format": "ulid"
            }
          },
          {
            "name": "until_ulid",
            "in": "query",
            "schema": {
              "type": "string",
              "format": "ulid"
            }
          },
          {
            "schema": {
              "type": "string"
            },
            "in": "query",
            "name": "id"
          }
        ],
        "responses": {
          "200": {
            "description": "Connected. Events will now start streaming as long as you keep the connection open.",
            "content": {
              "text/event-stream": {
                "schema": {
                  "type": "array",
                  "items": {
                    "description": "Represents a change to certain account properties, sent over the events streaming API.\n",
                    "type": "object",
                    "x-examples": {
                      "example-1": {
                        "account_id": "4db36989-6565-4011-9126-39fe6b3d9bf6",
                        "account_number": "",
                        "at": "2021-06-14T09:59:15.232782Z",
                        "event_id": 122039,
                        "event_ulid": "01F84ZC0H0Q1QN7XPNWX44HF5J",
                        "kyc_results": null,
                        "status_from": "",
                        "status_to": "APPROVED"
                      }
                    },
                    "title": "AccountStatusEvent",
                    "x-stoplight": {
                      "id": "u28ukdg1k63c1"
                    },
                    "properties": {
                      "account_id": {
                        "type": "string",
                        "description": "The unique identifier of the account that was changed",
                        "minLength": 1
                      },
                      "account_number": {
                        "type": "string",
                        "description": "The account number of the account that was changed",
                        "minLength": 1
                      },
                      "at": {
                        "type": "string",
                        "minLength": 1,
                        "description": "timestamp of event"
                      },
                      "event_id": {
                        "type": "integer",
                        "description": "monotonically increasing 64bit integer"
                      },
                      "event_ulid": {
                        "type": "string",
                        "format": "ulid",
                        "description": "lexically sortable, monotonically increasing character array"
                      },
                      "account_blocked": {
                        "type": "boolean",
                        "x-stoplight": {
                          "id": "ubzoqqxv9p34z"
                        },
                        "description": "If true the account was blocked, if false, the account got unblocked"
                      },
                      "admin_configurations": {
                        "title": "AdminConfigurations",
                        "x-stoplight": {
                          "id": "qsosbl2ojvpy5"
                        },
                        "type": "object",
                        "description": "These configurations show account properties that are overriden either by Alpaca Broker Operations or an automated process.\n\nThese values cannot be modified by the Broker Partners.\n\n\nFor the **events** interface we are only broadcasting changes to admin configurations. In case nothing changed for a flag that will not be included in unrelated update events.\n\nDepending on the type of the Admin Configurations the sent event will behave differently. For bool flags we are only sending the new value.\n\nFor example the following payload means, that the disable_shorting flag was set to true from false:\n\n```\n{\n  \"disable_shorting\": false\n}\n```\n\nFor other data types, we are embeding the old and new values into the payload. For example changing the max_margin_multiplier from 4 to 1 will yield this payload:\n\n```\n{\n  \"max_margin_multiplier\": {\n    \"old\": 4,\n    \"new\": 1,\n  }\n}\n```\n\nIntroducing an override value from the default will yield a null value as old. For example restricting the max_margin_multipler to 1 from default will yield the following payload:\n\n```\n{\n  \"max_margin_multiplier\": {\n    \"old\": null,\n    \"new\": 1,\n  }\n}\n```",
                        "properties": {
                          "restrict_to_liquidation_reasons": {
                            "title": "RestrictToLiquidationReasons",
                            "x-stoplight": {
                              "id": "8ve05o357xumy"
                            },
                            "type": "object",
                            "description": "Reasons why the liquidation only flag was set",
                            "properties": {
                              "pattern_day_trading": {
                                "type": "boolean",
                                "x-stoplight": {
                                  "id": "jie5waxje186p"
                                },
                                "description": "Set when the trading account is marked as a PDT, but its equity falls below the $25k treshold"
                              },
                              "ach_return": {
                                "type": "boolean",
                                "x-stoplight": {
                                  "id": "rdalpird93yqd"
                                },
                                "description": "Set when an incoming ACH transfer gets rejected"
                              },
                              "position_to_equity_ratio": {
                                "type": "boolean",
                                "x-stoplight": {
                                  "id": "w38ngiibz57ih"
                                },
                                "description": "Set when the position to equity ration exceeds the maximum limit"
                              },
                              "unspecified": {
                                "type": "boolean",
                                "x-stoplight": {
                                  "id": "8t9456c8yt2u8"
                                },
                                "description": "Default value for unknown reason"
                              }
                            },
                            "x-readme-ref-name": "RestrictToLiquidationReasons"
                          },
                          "outgoing_transfers_blocked": {
                            "type": "boolean",
                            "x-stoplight": {
                              "id": "6asgwwc5og5vt"
                            },
                            "description": "Wire-out transfers blocked for the account if false"
                          },
                          "incoming_transfers_blocked": {
                            "type": "boolean",
                            "x-stoplight": {
                              "id": "9h6kxbeu7892i"
                            },
                            "description": "Deposits are blocked for the account if false"
                          },
                          "disable_shorting": {
                            "type": "boolean",
                            "x-stoplight": {
                              "id": "xpj079uvkjlln"
                            },
                            "description": "If true the account is not allowed to create short position orders"
                          },
                          "pdt_check_mode": {
                            "type": "string",
                            "x-stoplight": {
                              "id": "xpj079uvkjlln"
                            },
                            "description": "PDT check mode"
                          },
                          "disable_fractional": {
                            "type": "boolean",
                            "x-stoplight": {
                              "id": "67vm959kuferk"
                            },
                            "description": "If true, the account cannot create orders for fractional share positions"
                          },
                          "disable_crypto": {
                            "type": "boolean",
                            "x-stoplight": {
                              "id": "h027r16ybjq26"
                            },
                            "description": "If true, the account is not allowed to trade cryptos"
                          },
                          "disable_day_trading": {
                            "type": "boolean",
                            "x-stoplight": {
                              "id": "ypcv5e39wabjv"
                            },
                            "description": "If true, the account is not allowed to day trade (e.g. buy and sell the same security on the same day)"
                          },
                          "allow_instant_ach": {
                            "type": "boolean",
                            "description": "If true, the account is allowed to perform instant ACH"
                          },
                          "disable_algodash_access": {
                            "type": "boolean",
                            "description": "If true, the account is allowed to access algo dash"
                          },
                          "disable_api_key": {
                            "type": "boolean",
                            "description": "If true, the account's API key will be disabled"
                          },
                          "max_margin_multiplier": {
                            "type": "object",
                            "x-stoplight": {
                              "id": "z5ufwctnvy3fy"
                            },
                            "description": "Max margin multipler is set by admin to this value",
                            "properties": {
                              "to": {
                                "type": "string",
                                "description": "New value of margin multiplier"
                              },
                              "from": {
                                "type": "string",
                                "description": "Old value of margin multiplier"
                              }
                            }
                          },
                          "max_options_trading_level": {
                            "type": "object",
                            "description": "Max options trading level is set by admin to this value. It can be 0, 1 or 2.",
                            "properties": {
                              "to": {
                                "type": "string",
                                "description": "New value of max options trading level"
                              },
                              "from": {
                                "type": "string",
                                "description": "New value of max options trading level"
                              }
                            }
                          },
                          "acct_daily_transfer_limit": {
                            "type": "string",
                            "x-stoplight": {
                              "id": "7m2ved3asodk3"
                            },
                            "description": "Override the correspondent level daily transfer limits",
                            "format": "decimal"
                          }
                        },
                        "x-readme-ref-name": "AdminConfigurations"
                      },
                      "cash_interest": {
                        "type": "object",
                        "description": "This property is included when the account's cash interest program had changed due to an enrollment, APR tier change, or unenrollment.\nThe from and to status or APR tier name will be included in the event, depending on the change.\n",
                        "properties": {
                          "currency": {
                            "type": "string",
                            "description": "The currency of the cash interest program that changed.",
                            "example": "USD"
                          },
                          "apr_tier_name_from": {
                            "type": "string",
                            "description": "The APR tier name before the change"
                          },
                          "apr_tier_name_to": {
                            "type": "string",
                            "description": "The APR tier name after the change"
                          },
                          "status_from": {
                            "type": "string",
                            "description": "The cash_interest program status of the account before the change"
                          },
                          "status_to": {
                            "type": "string",
                            "description": "The cash_interest program status of the account after the change"
                          }
                        },
                        "x-readme-ref-name": "AccountCashInterestEvent"
                      },
                      "options": {
                        "type": "object",
                        "description": "This property is included when the account's approved options level changes.\n",
                        "properties": {
                          "approved_level_from": {
                            "type": "integer",
                            "description": "The approved options level before the change"
                          },
                          "approved_level_to": {
                            "type": "integer",
                            "description": "The approved options level after the change"
                          }
                        },
                        "x-readme-ref-name": "OptionsApprovalEvent"
                      },
                      "fspl": {
                        "type": "object",
                        "description": "This property is included when the account's FPSL information had changed due to an enrollment, tier change, or unenrollment.\nThe from and to status or tier id will be included in the event, depending on the change.\n",
                        "properties": {
                          "US": {
                            "type": "object",
                            "properties": {
                              "tier_from": {
                                "type": "string",
                                "description": "The tier id before the change"
                              },
                              "tier_to": {
                                "type": "string",
                                "description": "The tier id after the change"
                              },
                              "status_from": {
                                "type": "string",
                                "description": "The FPSL program status of the account before the change"
                              },
                              "status_to": {
                                "type": "string",
                                "description": "The FPSL program status of the account after the change"
                              }
                            }
                          }
                        },
                        "x-readme-ref-name": "AccountFPSLEvent"
                      },
                      "crypto_status_from": {
                        "type": "string",
                        "x-stoplight": {
                          "id": "7fgoyvh2ttwzz"
                        },
                        "description": "account crypto_status changed from"
                      },
                      "crypto_status_to": {
                        "type": "string",
                        "x-stoplight": {
                          "id": "g15q2jn26klem"
                        },
                        "description": "account crypto_status changed to"
                      },
                      "kyc_results": {
                        "type": "object",
                        "description": "Hold information about the result of KYC. Please see the documentation [here](https://alpaca.markets/docs/api-references/broker-api/events/#kyc-results) for more indepth details",
                        "x-stoplight": {
                          "id": "m6so9tt7secvm"
                        },
                        "properties": {
                          "reject": {
                            "title": "KYCResultType",
                            "x-stoplight": {
                              "id": "mkpd1y7i0tihh"
                            },
                            "type": "string",
                            "description": "IDENTITY_VERIFICATION\tIdentity needs to be verified\n\nTAX_IDENTIFICATION\tTax ID number needs to be verified\n\nADDRESS_VERIFICATION\tAddress needs to be verified\n\nDATE_OF_BIRTH\tDate of birth needs to be verified\n\nINVALID_IDENTITY_PASSPORT\tIdentity needs to be verified via a \ngovernment issued ID. This is commonly used in conjuction with OTHER to describe the exact document needed.\n\nSELFIE_VERIFICATION\tIdentity needs to be verified via a live selfie of the account owner\n\nPEP\tFurther information needs to be submitted if account owner is politically exposed person\n\nFAMILY_MEMBER_PEP\tFurther information needs to be submitted if family member is a politically exposed person\n\nCONTROL_PERSON\tFurther information needs to be submitted if account owner is a control person\n\nAFFILIATED\tFurther information needs to be submitted if account owner is affiliated to finra or an exchange\n\nVISA_TYPE_OTHER\tFurther information needs to be submitted about account owner’s visa\n\nW8BEN_CORRECTION\tIdenfitying information submitted by the user was incorrect so a new, corrected, W8BEN needs to be submitted\nCOUNTRY_NOT_SUPPORTED\tThe account owner’s country of tax residence is not supported by our KYC providers. In this case, we’ll manully perform KYC on the user\n\nWATCHLIST_HIT\tResults from the watchlist screening need further investigation before account opening. No action is needed from the user\n\nOTHER\tA custom message will be sent to describe exactly what is needed from the account owner. The message will be displayed in the additional_information attribute.\n\nOTHER_PARTNER\tA custom message will be sent to relay information relevant only to the partner. The message will be displayed in the additional_information attribute.",
                            "x-readme-ref-name": "KYCResultType"
                          },
                          "accept": {
                            "title": "KYCResultType",
                            "x-stoplight": {
                              "id": "mkpd1y7i0tihh"
                            },
                            "type": "string",
                            "description": "IDENTITY_VERIFICATION\tIdentity needs to be verified\n\nTAX_IDENTIFICATION\tTax ID number needs to be verified\n\nADDRESS_VERIFICATION\tAddress needs to be verified\n\nDATE_OF_BIRTH\tDate of birth needs to be verified\n\nINVALID_IDENTITY_PASSPORT\tIdentity needs to be verified via a \ngovernment issued ID. This is commonly used in conjuction with OTHER to describe the exact document needed.\n\nSELFIE_VERIFICATION\tIdentity needs to be verified via a live selfie of the account owner\n\nPEP\tFurther information needs to be submitted if account owner is politically exposed person\n\nFAMILY_MEMBER_PEP\tFurther information needs to be submitted if family member is a politically exposed person\n\nCONTROL_PERSON\tFurther information needs to be submitted if account owner is a control person\n\nAFFILIATED\tFurther information needs to be submitted if account owner is affiliated to finra or an exchange\n\nVISA_TYPE_OTHER\tFurther information needs to be submitted about account owner’s visa\n\nW8BEN_CORRECTION\tIdenfitying information submitted by the user was incorrect so a new, corrected, W8BEN needs to be submitted\nCOUNTRY_NOT_SUPPORTED\tThe account owner’s country of tax residence is not supported by our KYC providers. In this case, we’ll manully perform KYC on the user\n\nWATCHLIST_HIT\tResults from the watchlist screening need further investigation before account opening. No action is needed from the user\n\nOTHER\tA custom message will be sent to describe exactly what is needed from the account owner. The message will be displayed in the additional_information attribute.\n\nOTHER_PARTNER\tA custom message will be sent to relay information relevant only to the partner. The message will be displayed in the additional_information attribute.",
                            "x-readme-ref-name": "KYCResultType"
                          },
                          "indeterminate": {
                            "title": "KYCResultType",
                            "x-stoplight": {
                              "id": "mkpd1y7i0tihh"
                            },
                            "type": "string",
                            "description": "IDENTITY_VERIFICATION\tIdentity needs to be verified\n\nTAX_IDENTIFICATION\tTax ID number needs to be verified\n\nADDRESS_VERIFICATION\tAddress needs to be verified\n\nDATE_OF_BIRTH\tDate of birth needs to be verified\n\nINVALID_IDENTITY_PASSPORT\tIdentity needs to be verified via a \ngovernment issued ID. This is commonly used in conjuction with OTHER to describe the exact document needed.\n\nSELFIE_VERIFICATION\tIdentity needs to be verified via a live selfie of the account owner\n\nPEP\tFurther information needs to be submitted if account owner is politically exposed person\n\nFAMILY_MEMBER_PEP\tFurther information needs to be submitted if family member is a politically exposed person\n\nCONTROL_PERSON\tFurther information needs to be submitted if account owner is a control person\n\nAFFILIATED\tFurther information needs to be submitted if account owner is affiliated to finra or an exchange\n\nVISA_TYPE_OTHER\tFurther information needs to be submitted about account owner’s visa\n\nW8BEN_CORRECTION\tIdenfitying information submitted by the user was incorrect so a new, corrected, W8BEN needs to be submitted\nCOUNTRY_NOT_SUPPORTED\tThe account owner’s country of tax residence is not supported by our KYC providers. In this case, we’ll manully perform KYC on the user\n\nWATCHLIST_HIT\tResults from the watchlist screening need further investigation before account opening. No action is needed from the user\n\nOTHER\tA custom message will be sent to describe exactly what is needed from the account owner. The message will be displayed in the additional_information attribute.\n\nOTHER_PARTNER\tA custom message will be sent to relay information relevant only to the partner. The message will be displayed in the additional_information attribute.",
                            "x-readme-ref-name": "KYCResultType"
                          },
                          "additional_information": {
                            "type": "string",
                            "description": "Used to display a custom message."
                          },
                          "summary": {
                            "type": "string",
                            "x-stoplight": {
                              "id": "dfz7vejxhvxyk"
                            },
                            "description": "Either `pass` or `fail`. Used to indicate if KYC has completed and passed or not. This field is used for internal purposes only."
                          }
                        },
                        "x-readme-ref-name": "KYCResults"
                      },
                      "pattern_day_trader": {
                        "type": "boolean",
                        "x-stoplight": {
                          "id": "05mrhvc4aaeyy"
                        },
                        "description": "If true the pattern_day_trader flag was set for the account, if false, the flag was reset."
                      },
                      "reason": {
                        "type": "string",
                        "minLength": 1,
                        "deprecated": true
                      },
                      "status_from": {
                        "type": "string",
                        "description": "The account status before the change",
                        "example": "APPROVED"
                      },
                      "status_to": {
                        "type": "string",
                        "description": "The account status after the change",
                        "example": "ACTIVE"
                      },
                      "trading_blocked": {
                        "type": "boolean",
                        "x-stoplight": {
                          "id": "tb42kskazg9zr"
                        },
                        "description": "If true the account cannot trade going forward, if false, the ban has been lifed"
                      }
                    },
                    "required": [
                      "account_id",
                      "at",
                      "event_id",
                      "event_ulid"
                    ],
                    "x-readme-ref-name": "AccountStatusEvent"
                  }
                },
                "examples": {}
              }
            }
          }
        },
        "operationId": "suscribeToAccountStatusSSE"
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
````
