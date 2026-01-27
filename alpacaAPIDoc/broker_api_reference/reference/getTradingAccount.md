---
source_view: https://docs.alpaca.markets/reference/gettradingaccount
source_md: https://docs.alpaca.markets/reference/gettradingaccount.md
scraped_at_utc: 2026-01-27T04:30:48Z
---
# Retrieve Trading Details for an Account

As a broker you can view more trading details about your users.

The response is a Trading Account model.

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
    "/v1/trading/accounts/{account_id}/account": {
      "parameters": [
        {
          "name": "account_id",
          "in": "path",
          "required": true,
          "description": "Account identifier.",
          "schema": {
            "type": "string",
            "format": "uuid"
          }
        }
      ],
      "get": {
        "operationId": "getTradingAccount",
        "summary": "Retrieve Trading Details for an Account",
        "tags": [
          "Accounts"
        ],
        "description": "As a broker you can view more trading details about your users.\n\nThe response is a Trading Account model.",
        "responses": {
          "200": {
            "description": "OK",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "x-examples": {
                    "example-1": {
                      "id": "c8f1ef5d-edc0-4f23-9ee4-378f19cb92a4",
                      "account_number": "927584925",
                      "status": "ACTIVE",
                      "currency": "USD",
                      "buying_power": "103556.8572572922",
                      "regt_buying_power": "52921.2982330664",
                      "daytrading_buying_power": "103556.8572572922",
                      "options_buying_power": "26460.65",
                      "cash": "24861.91",
                      "cash_withdrawable": "17861.91",
                      "cash_transferable": "24861.91",
                      "accrued_fees": "0",
                      "pending_transfer_out": "0",
                      "portfolio_value": "28059.3882330664",
                      "pattern_day_trader": true,
                      "trading_blocked": false,
                      "transfers_blocked": false,
                      "account_blocked": false,
                      "created_at": "2021-03-01T13:28:49.270232Z",
                      "trade_suspended_by_user": false,
                      "multiplier": "2",
                      "shorting_enabled": true,
                      "equity": "28059.3882330664",
                      "last_equity": "26977.323677655",
                      "long_market_value": "3197.4782330664",
                      "short_market_value": "0",
                      "initial_margin": "1598.7391165332",
                      "maintenance_margin": "959.24346991992",
                      "last_maintenance_margin": "934.6241032965",
                      "sma": "26758.0590204615",
                      "daytrade_count": 0,
                      "balance_asof": "2021-04-01",
                      "previous_close": "2021-04-01T19:00:00-04:00",
                      "last_long_market_value": "3115.413677655",
                      "last_short_market_value": "0",
                      "last_cash": "23861.91",
                      "last_initial_margin": "1557.7068388275",
                      "last_regt_buying_power": "50839.233677655",
                      "last_daytrading_buying_power": "104433.9158860662",
                      "last_options_buying_power": "25419.62",
                      "last_buying_power": "104433.9158860662",
                      "last_daytrade_count": 0,
                      "clearing_broker": "VELOX",
                      "options_approved_level": 0,
                      "options_trading_level": 0,
                      "intraday_adjustments": "0",
                      "pending_reg_taf_fees": "0"
                    },
                    "example-2": {
                      "id": "56712986-9ff7-4d8f-8e52-077e099e533e",
                      "account_number": "601612064",
                      "status": "ACTIVE",
                      "crypto_status": "PAPER_ONLY",
                      "currency": "USD",
                      "buying_power": "83567.42",
                      "regt_buying_power": "83567.42",
                      "daytrading_buying_power": "0",
                      "options_buying_power": "83567.42",
                      "non_marginable_buying_power": "41783.71",
                      "cash": "83567.42",
                      "cash_withdrawable": "0",
                      "cash_transferable": "41783.71",
                      "accrued_fees": "0",
                      "pending_transfer_out": "0",
                      "pending_transfer_in": "0",
                      "portfolio_value": "83567.42",
                      "pattern_day_trader": false,
                      "trading_blocked": false,
                      "transfers_blocked": false,
                      "account_blocked": false,
                      "created_at": "2022-01-21T21:25:26.713802Z",
                      "trade_suspended_by_user": false,
                      "multiplier": "1",
                      "shorting_enabled": false,
                      "equity": "83567.42",
                      "last_equity": "41783.71",
                      "long_market_value": "0",
                      "short_market_value": "0",
                      "initial_margin": "0",
                      "maintenance_margin": "0",
                      "last_maintenance_margin": "0",
                      "sma": "0",
                      "daytrade_count": 0,
                      "balance_asof": "2022-02-08",
                      "previous_close": "2022-02-08T19:00:00-05:00",
                      "last_long_market_value": "0",
                      "last_short_market_value": "0",
                      "last_cash": "41783.71",
                      "last_initial_margin": "0",
                      "last_regt_buying_power": "41783.71",
                      "last_daytrading_buying_power": "0",
                      "last_options_buying_power": "41783.71",
                      "last_buying_power": "41783.71",
                      "last_daytrade_count": 0,
                      "clearing_broker": "VELOX",
                      "options_approved_level": 2,
                      "options_trading_level": 1,
                      "intraday_adjustments": "0",
                      "pending_reg_taf_fees": "0.01"
                    }
                  },
                  "description": "This is an extended version of the Account model found [in the trading api](https://alpaca.markets/docs/api-references/trading-api/account/#account-entity).\n\nExtra data has been added that would be useful for brokers.",
                  "properties": {
                    "id": {
                      "type": "string",
                      "example": "c8f1ef5d-edc0-4f23-9ee4-378f19cb92a4",
                      "format": "uuid",
                      "description": "The account ID"
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
                    "user_configurations": {
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
                    "account_number": {
                      "type": "string",
                      "example": "927584925",
                      "description": "The account number",
                      "nullable": true
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
                      "type": "string",
                      "example": "USD",
                      "description": "Always USD"
                    },
                    "buying_power": {
                      "type": "string",
                      "example": "12345.6789",
                      "format": "decimal",
                      "description": "Current available cash buying power. If multiplier = 2 then buying_power = max(equity-initial_margin(0) * 2). If multiplier = 1 then buying_power = cash."
                    },
                    "regt_buying_power": {
                      "type": "string",
                      "example": "12345.6789",
                      "format": "decimal",
                      "description": "User’s buying power under Regulation T (excess equity - (equity - margin value) - * margin multiplier)"
                    },
                    "daytrading_buying_power": {
                      "type": "string",
                      "example": "12345.6789",
                      "format": "decimal",
                      "description": "Your buying power for day trades (continuously updated value)"
                    },
                    "effective_buying_power": {
                      "type": "string",
                      "example": "12345.6789",
                      "format": "decimal",
                      "description": "Effective buying power (duplicate of buying power)"
                    },
                    "non_marginable_buying_power": {
                      "type": "string",
                      "example": "12345.6789",
                      "format": "decimal",
                      "description": "Non-marginable buying power (currently used for only crypto trading)"
                    },
                    "options_buying_power": {
                      "type": "string",
                      "example": "12345.6789",
                      "format": "decimal",
                      "description": "Your buying power for options trading"
                    },
                    "bod_dtbp": {
                      "type": "string",
                      "example": "12345.6789",
                      "format": "decimal",
                      "description": "bod_dtbp"
                    },
                    "accrued_fees": {
                      "type": "string",
                      "example": "12345.6789",
                      "format": "decimal",
                      "description": "Accrued fees"
                    },
                    "cash": {
                      "type": "string",
                      "example": "12345.6789",
                      "format": "decimal",
                      "description": "Cash balance"
                    },
                    "cash_withdrawable": {
                      "type": "string",
                      "example": "12345.6789",
                      "format": "decimal",
                      "description": "Cash available for withdrawl"
                    },
                    "cash_transferable": {
                      "type": "string",
                      "example": "12345.6789",
                      "description": "Cash available for transfer (JNLC)"
                    },
                    "pending_transfer_out": {
                      "type": "string",
                      "example": "12345.6789",
                      "description": "Cash pending transfer out"
                    },
                    "portfolio_value": {
                      "type": "string",
                      "example": "12345.6789",
                      "format": "decimal",
                      "description": "Total value of cash + holding positions. (This field is deprecated. It is equivalent to the equity field.)"
                    },
                    "pattern_day_trader": {
                      "type": "boolean",
                      "example": false,
                      "description": "Whether account is flagged as pattern day trader or not"
                    },
                    "trading_blocked": {
                      "type": "boolean",
                      "example": false,
                      "description": "If true, the account is not allowed to place orders."
                    },
                    "transfers_blocked": {
                      "type": "boolean",
                      "example": false,
                      "description": "If true, the account is not allowed to request money transfers."
                    },
                    "account_blocked": {
                      "type": "boolean",
                      "example": false,
                      "description": "If true, the account activity by user is prohibited."
                    },
                    "created_at": {
                      "type": "string",
                      "example": "2021-03-01T13:28:49.270232Z",
                      "description": "Timestamp this account was created at"
                    },
                    "trade_suspended_by_user": {
                      "type": "boolean",
                      "example": false,
                      "description": "If true, the account is not allowed to place orders."
                    },
                    "multiplier": {
                      "type": "string",
                      "format": "decimal",
                      "example": "2",
                      "description": "“1”, “2”, \"3\", or \"4\""
                    },
                    "shorting_enabled": {
                      "type": "boolean",
                      "example": false,
                      "description": "Flag to denote whether or not the account is permitted to short"
                    },
                    "equity": {
                      "type": "string",
                      "example": "12345.6789",
                      "format": "decimal",
                      "description": "cash + long_market_value + short_market_value"
                    },
                    "last_equity": {
                      "type": "string",
                      "example": "12345.6789",
                      "format": "decimal",
                      "description": "Equity as of previous trading day at 16:00:00 ET"
                    },
                    "long_market_value": {
                      "type": "string",
                      "example": "12345.6789",
                      "format": "decimal",
                      "description": "Real-time MtM value of all long positions held in the account"
                    },
                    "short_market_value": {
                      "type": "string",
                      "example": "0",
                      "format": "decimal",
                      "description": "Real-time MtM value of all short positions held in the account"
                    },
                    "position_market_value": {
                      "type": "string",
                      "example": "0",
                      "format": "decimal",
                      "description": "Real-time MtM value of all the positions held in the account"
                    },
                    "initial_margin": {
                      "type": "string",
                      "example": "12345.6789",
                      "format": "decimal",
                      "description": "Reg T initial margin requirement (continuously updated value)"
                    },
                    "maintenance_margin": {
                      "type": "string",
                      "example": "12345.6789",
                      "format": "decimal",
                      "description": "Maintenance margin requirement (continuously updated value)"
                    },
                    "last_maintenance_margin": {
                      "type": "string",
                      "example": "12345.6789",
                      "format": "decimal",
                      "description": "Maintenance margin requirement on the previous trading day"
                    },
                    "sma": {
                      "type": "string",
                      "example": "12345.6789",
                      "format": "decimal",
                      "description": "Value of Special Memorandum Account (will be used at a later date to provide additional buying_power)"
                    },
                    "daytrade_count": {
                      "type": "integer",
                      "example": 0,
                      "description": "The current number of daytrades that have been made in the last 5 trading days (inclusive of today)"
                    },
                    "balance_asof": {
                      "description": "The date of the snapshot for `last_*` fields",
                      "type": "string",
                      "example": "2021-04-01"
                    },
                    "previous_close": {
                      "type": "string",
                      "example": "2021-04-01T19:00:00-04:00",
                      "description": "Previous sessions close time"
                    },
                    "last_long_market_value": {
                      "type": "string",
                      "example": "12345.6789",
                      "description": "Value of all long positions as of previous trading day at 16:00:00 ET"
                    },
                    "last_short_market_value": {
                      "type": "string",
                      "example": "0",
                      "description": "Value of all short positions as of previous trading day at 16:00:00 ET"
                    },
                    "last_cash": {
                      "type": "string",
                      "example": "12345.6789",
                      "description": "Value of all cash as of previous trading day at 16:00:00 ET"
                    },
                    "last_initial_margin": {
                      "type": "string",
                      "example": "12345.6789",
                      "description": "Value of Reg T margin as of previous trading day at 16:00:00 ET"
                    },
                    "last_regt_buying_power": {
                      "type": "string",
                      "example": "12345.6789",
                      "description": "Value of Reg T buying power as of previous trading day at 16:00:00 ET"
                    },
                    "last_daytrading_buying_power": {
                      "type": "string",
                      "example": "12345.6789",
                      "description": "Value of daytrading buying power as of previous trading day at 16:00:00 ET"
                    },
                    "last_options_buying_power": {
                      "type": "string",
                      "example": "12345.6789",
                      "description": "Value of option buying power as of previous trading day at 16:00:00 ET"
                    },
                    "last_buying_power": {
                      "type": "string",
                      "example": "12345.6789",
                      "description": "Value of buying_power as of previous trading day at 16:00:00 ET"
                    },
                    "last_daytrade_count": {
                      "type": "integer",
                      "example": 0,
                      "description": "Value of daytrade count as of previous trading day at 16:00:00 ET"
                    },
                    "clearing_broker": {
                      "type": "string",
                      "example": "Velox",
                      "description": "Clearing broker"
                    },
                    "options_approved_level": {
                      "type": "integer",
                      "example": 3,
                      "description": "The options trading level that was approved for this account.\n0=disabled, 1=Covered Call/Cash-Secured Put, 2=Long Call/Put, 3=Spreads/Straddles.\n",
                      "enum": [
                        0,
                        1,
                        2,
                        3
                      ]
                    },
                    "options_trading_level": {
                      "type": "integer",
                      "example": 3,
                      "description": "The effective options trading level of the account.\nThis is the minimum between account options_approved_level and account configurations max_options_trading_level.\n0=disabled, 1=Covered Call/Cash-Secured Put, 2=Long Call/Put, 3=Spreads/Straddles.\n",
                      "enum": [
                        0,
                        1,
                        2,
                        3
                      ]
                    },
                    "intraday_adjustments": {
                      "type": "string",
                      "example": "0",
                      "description": "The intraday adjustment by non_trade_activities such as fund deposit/withdraw.\n"
                    },
                    "pending_reg_taf_fees": {
                      "type": "string",
                      "example": "0.01",
                      "description": "Pending regulatory fees for the account."
                    },
                    "memoposts": {
                      "type": "string",
                      "example": "100",
                      "description": "Outstanding memopost value"
                    }
                  },
                  "required": [
                    "id",
                    "admin_configurations",
                    "user_configurations",
                    "account_number",
                    "status",
                    "crypto_status",
                    "currency",
                    "buying_power",
                    "regt_buying_power",
                    "daytrading_buying_power",
                    "effective_buying_power",
                    "non_marginable_buying_power",
                    "bod_dtbp",
                    "accrued_fees",
                    "portfolio_value",
                    "pattern_day_trader",
                    "trading_blocked",
                    "transfers_blocked",
                    "account_blocked",
                    "created_at",
                    "trade_suspended_by_user",
                    "multiplier",
                    "shorting_enabled",
                    "equity",
                    "last_equity",
                    "long_market_value",
                    "short_market_value",
                    "position_market_value",
                    "initial_margin",
                    "maintenance_margin",
                    "last_maintenance_margin",
                    "sma",
                    "daytrade_count",
                    "balance_asof",
                    "cash"
                  ],
                  "x-stoplight": {
                    "id": "fib073ib25xrv"
                  },
                  "x-readme-ref-name": "TradeAccount"
                }
              }
            }
          }
        }
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
