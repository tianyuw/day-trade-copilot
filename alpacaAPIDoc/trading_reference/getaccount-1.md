---
source_view: https://docs.alpaca.markets/reference/getaccount-1
source_md: https://docs.alpaca.markets/reference/getaccount-1.md
scraped_at_utc: 2026-01-22T23:02:18Z
---
# Get Account

Returns your account details.

# OpenAPI definition

```json
{
  "openapi": "3.0.0",
  "info": {
    "title": "Trading API",
    "description": "Alpaca's Trading API is a modern platform for algorithmic trading.",
    "version": "2.0.1",
    "contact": {
      "name": "Alpaca Support",
      "email": "support@alpaca.markets",
      "url": "https://alpaca.markets/support"
    },
    "termsOfService": "https://s3.amazonaws.com/files.alpaca.markets/disclosures/library/TermsAndConditions.pdf"
  },
  "servers": [
    {
      "url": "https://paper-api.alpaca.markets",
      "description": "Paper"
    },
    {
      "url": "https://api.alpaca.markets",
      "description": "Live"
    }
  ],
  "tags": [
    {
      "name": "Accounts"
    }
  ],
  "paths": {
    "/v2/account": {
      "get": {
        "summary": "Get Account",
        "tags": [
          "Accounts"
        ],
        "responses": {
          "200": {
            "description": "OK",
            "content": {
              "application/json": {
                "schema": {
                  "title": "Account",
                  "type": "object",
                  "description": "The account API serves important information related to an account, including account status, funds available for trade, funds available for withdrawal, and various flags relevant to an account’s ability to trade. An account maybe be blocked for just for trades (trades_blocked flag) or for both trades and transfers (account_blocked flag) if Alpaca identifies the account to engaging in any suspicious activity. Also, in accordance with FINRA’s pattern day trading rule, an account may be flagged for pattern day trading (pattern_day_trader flag), which would inhibit an account from placing any further day-trades. Please note that cryptocurrencies are not eligible assets to be used as collateral for margin accounts and will require the asset be traded using cash only.\n",
                  "x-examples": {
                    "example-1": {
                      "account_blocked": false,
                      "account_number": "010203ABCD",
                      "buying_power": "262113.632",
                      "cash": "-23140.2",
                      "created_at": "2019-06-12T22:47:07.99658Z",
                      "currency": "USD",
                      "daytrade_count": 0,
                      "balance_asof": "2023-09-27",
                      "daytrading_buying_power": "262113.632",
                      "equity": "103820.56",
                      "id": "e6fe16f3-64a4-4921-8928-cadf02f92f98",
                      "initial_margin": "63480.38",
                      "last_equity": "103529.24",
                      "last_maintenance_margin": "38000.832",
                      "long_market_value": "126960.76",
                      "maintenance_margin": "38088.228",
                      "multiplier": "4",
                      "pattern_day_trader": false,
                      "portfolio_value": "103820.56",
                      "regt_buying_power": "80680.36",
                      "options_buying_power": "40340.18",
                      "short_market_value": "0",
                      "shorting_enabled": true,
                      "sma": "0",
                      "status": "ACTIVE",
                      "trade_suspended_by_user": false,
                      "trading_blocked": false,
                      "transfers_blocked": false,
                      "options_approved_level": 2,
                      "options_trading_level": 1,
                      "intraday_adjustments": "0",
                      "pending_reg_taf_fees": "0"
                    }
                  },
                  "properties": {
                    "id": {
                      "type": "string",
                      "description": "Account Id.\n",
                      "format": "uuid"
                    },
                    "account_number": {
                      "type": "string",
                      "description": "Account number."
                    },
                    "status": {
                      "type": "string",
                      "title": "AccountStatus",
                      "enum": [
                        "ONBOARDING",
                        "SUBMISSION_FAILED",
                        "SUBMITTED",
                        "ACCOUNT_UPDATED",
                        "APPROVAL_PENDING",
                        "ACTIVE",
                        "REJECTED"
                      ],
                      "description": "An enum representing the various possible account status values.\n\nMost likely, the account status is ACTIVE unless there is any problem. The account status may get in ACCOUNT_UPDATED when personal information is being updated from the dashboard, in which case you may not be allowed trading for a short period of time until the change is approved.\n\n- ONBOARDING\n  The account is onboarding.\n- SUBMISSION_FAILED\n  The account application submission failed for some reason.\n- SUBMITTED\n  The account application has been submitted for review.\n- ACCOUNT_UPDATED\n  The account information is being updated.\n- APPROVAL_PENDING\n  The final account approval is pending.\n- ACTIVE\n  The account is active for trading.\n- REJECTED\n  The account application has been rejected.",
                      "x-examples": {
                        "example-1": "ACTIVE"
                      },
                      "example": "ACTIVE",
                      "x-readme-ref-name": "AccountStatus"
                    },
                    "currency": {
                      "type": "string",
                      "description": "USD\n",
                      "example": "USD"
                    },
                    "cash": {
                      "description": "Cash Balance\n",
                      "type": "string"
                    },
                    "portfolio_value": {
                      "description": "Total value of cash + holding positions (This field is deprecated. It is equivalent to the equity field.)",
                      "type": "string"
                    },
                    "non_marginable_buying_power": {
                      "description": "Current available non-margin dollar buying power",
                      "type": "string",
                      "x-stoplight": {
                        "id": "z0ydzt6yqegll"
                      }
                    },
                    "accrued_fees": {
                      "description": "The fees collected.",
                      "type": "string",
                      "x-stoplight": {
                        "id": "b1gospbwoz961"
                      }
                    },
                    "pending_transfer_in": {
                      "description": "Cash pending transfer in.",
                      "type": "string",
                      "x-stoplight": {
                        "id": "83ckvzqu3jewp"
                      }
                    },
                    "pending_transfer_out": {
                      "description": "Cash pending transfer out.",
                      "type": "string",
                      "x-stoplight": {
                        "id": "gkxijaueofvdg"
                      }
                    },
                    "pattern_day_trader": {
                      "type": "boolean",
                      "description": "Whether or not the account has been flagged as a pattern day trader"
                    },
                    "trade_suspended_by_user": {
                      "type": "boolean",
                      "description": "User setting. If true, the account is not allowed to place orders."
                    },
                    "trading_blocked": {
                      "type": "boolean",
                      "description": "If true, the account is not allowed to place orders.\n"
                    },
                    "transfers_blocked": {
                      "type": "boolean",
                      "description": "If true, the account is not allowed to request money transfers."
                    },
                    "account_blocked": {
                      "type": "boolean",
                      "description": "If true, the account activity by user is prohibited."
                    },
                    "created_at": {
                      "type": "string",
                      "description": "Timestamp this account was created at\n",
                      "format": "date-time"
                    },
                    "shorting_enabled": {
                      "type": "boolean",
                      "description": "Flag to denote whether or not the account is permitted to short"
                    },
                    "long_market_value": {
                      "description": "Real-time MtM value of all long positions held in the account\n",
                      "type": "string"
                    },
                    "short_market_value": {
                      "description": "Real-time MtM value of all short positions held in the account",
                      "type": "string"
                    },
                    "equity": {
                      "description": "Cash + long_market_value + short_market_value",
                      "type": "string"
                    },
                    "last_equity": {
                      "description": "Equity as of previous trading day at 16:00:00 ET",
                      "type": "string"
                    },
                    "multiplier": {
                      "description": "Buying power multiplier that represents account margin classification; valid values 1 (standard limited margin account with 1x buying power), 2 (reg T margin account with 2x intraday and overnight buying power; this is the default for all non-PDT accounts with $2,000 or more equity), 4 (PDT account with 4x intraday buying power and 2x reg T overnight buying power)",
                      "type": "string"
                    },
                    "buying_power": {
                      "description": "Current available $ buying power; If multiplier = 4, this is your daytrade buying power which is calculated as (last_equity - (last) maintenance_margin) * 4; If multiplier = 2, buying_power = max(equity – initial_margin,0) * 2; If multiplier = 1, buying_power = cash",
                      "type": "string"
                    },
                    "initial_margin": {
                      "description": "Reg T initial margin requirement (continuously updated value)",
                      "type": "string"
                    },
                    "maintenance_margin": {
                      "description": "Maintenance margin requirement (continuously updated value)",
                      "type": "string"
                    },
                    "sma": {
                      "type": "string",
                      "description": "Value of special memorandum account (will be used at a later date to provide additional buying_power)"
                    },
                    "daytrade_count": {
                      "type": "integer",
                      "description": "The current number of daytrades that have been made in the last 5 trading days (inclusive of today)"
                    },
                    "balance_asof": {
                      "type": "string",
                      "example": "2021-04-01",
                      "description": "The date of the snapshot for `last_*` fields"
                    },
                    "last_maintenance_margin": {
                      "description": "Your maintenance margin requirement on the previous trading day",
                      "type": "string"
                    },
                    "daytrading_buying_power": {
                      "description": "Your buying power for day trades (continuously updated value)",
                      "type": "string"
                    },
                    "regt_buying_power": {
                      "description": "Your buying power under Regulation T (your excess equity - equity minus margin value - times your margin multiplier)\n",
                      "type": "string"
                    },
                    "options_buying_power": {
                      "description": "Your buying power for options trading\n",
                      "type": "string"
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
                      "description": "Pending regulatory fees for the account.\n"
                    }
                  },
                  "required": [
                    "id",
                    "status"
                  ],
                  "x-readme-ref-name": "Account"
                },
                "example": {
                  "id": "1d9eed04-be39-4e01-9b84-a48ac5bbafcf",
                  "admin_configurations": {},
                  "user_configurations": null,
                  "account_number": "PALPACA_123",
                  "status": "ACTIVE",
                  "crypto_status": "ACTIVE",
                  "currency": "USD",
                  "buying_power": "245432.61",
                  "regt_buying_power": "245432.61",
                  "daytrading_buying_power": "0",
                  "options_buying_power": "122716.305",
                  "effective_buying_power": "245432.61",
                  "non_marginable_buying_power": "122086.5",
                  "bod_dtbp": 0,
                  "cash": "122086.5",
                  "accrued_fees": "0",
                  "pending_transfer_in": "0",
                  "portfolio_value": "123346.11",
                  "pattern_day_trader": true,
                  "trading_blocked": false,
                  "transfers_blocked": false,
                  "account_blocked": false,
                  "created_at": "2023-01-01T18:20:20.272275Z",
                  "trade_suspended_by_user": false,
                  "multiplier": "2",
                  "shorting_enabled": true,
                  "equity": "123346.11",
                  "last_equity": "122011.09751111286868",
                  "long_market_value": "1259.61",
                  "short_market_value": "0",
                  "position_market_value": "1259.61",
                  "initial_margin": "629.8",
                  "maintenance_margin": "377.88",
                  "last_maintenance_margin": "480.73",
                  "sma": "123369.74",
                  "daytrade_count": 0,
                  "balance_asof": "2023-09-27",
                  "crypto_tier": 1,
                  "options_trading_level": 2,
                  "intraday_adjustments": "0",
                  "pending_reg_taf_fees": "0"
                }
              }
            }
          }
        },
        "operationId": "getAccount",
        "parameters": [],
        "description": "Returns your account details."
      }
    }
  },
  "components": {
    "securitySchemes": {
      "API_Key": {
        "name": "APCA-API-KEY-ID",
        "type": "apiKey",
        "in": "header",
        "description": ""
      },
      "API_Secret": {
        "name": "APCA-API-SECRET-KEY",
        "type": "apiKey",
        "in": "header",
        "description": ""
      }
    }
  },
  "security": [
    {
      "API_Key": [],
      "API_Secret": []
    }
  ],
  "x-readme": {
    "explorer-enabled": true,
    "proxy-enabled": false
  }
}
```
