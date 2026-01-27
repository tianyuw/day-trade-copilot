---
source_view: https://docs.alpaca.markets/reference/patch-patch-v1-trading-accounts-account_id-account-configurations
source_md: https://docs.alpaca.markets/reference/patch-patch-v1-trading-accounts-account_id-account-configurations.md
scraped_at_utc: 2026-01-27T04:30:48Z
---
# Update Trading Configurations for an Account

You can also set the margin settings for your users’ account by passing a PATCH request. By default any account with funds under $2,000 is set a margin multiplier of 1.0, and accounts with over $2,000 are set to 2.0.

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
      "name": "Trading"
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
    "/v1/trading/accounts/{account_id}/account/configurations": {
      "parameters": [
        {
          "schema": {
            "type": "string"
          },
          "name": "account_id",
          "in": "path",
          "required": true
        }
      ],
      "patch": {
        "summary": "Update Trading Configurations for an Account",
        "tags": [
          "Trading"
        ],
        "operationId": "patch-PATCH-v1-trading-accounts-account_id-account-configurations",
        "responses": {
          "200": {
            "description": "Response will contain the account configuration settings for the account.",
            "content": {
              "application/json": {
                "schema": {
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
                }
              }
            }
          }
        },
        "description": "You can also set the margin settings for your users’ account by passing a PATCH request. By default any account with funds under $2,000 is set a margin multiplier of 1.0, and accounts with over $2,000 are set to 2.0.",
        "requestBody": {
          "content": {
            "application/json": {
              "schema": {
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
```
