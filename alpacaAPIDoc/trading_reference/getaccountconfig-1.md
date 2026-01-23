---
source_view: https://docs.alpaca.markets/reference/getaccountconfig-1
source_md: https://docs.alpaca.markets/reference/getaccountconfig-1.md
scraped_at_utc: 2026-01-22T23:02:18Z
---
# Get Account Configurations

gets the current account configuration values

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
      "name": "Account Configurations"
    }
  ],
  "paths": {
    "/v2/account/configurations": {
      "get": {
        "tags": [
          "Account Configurations"
        ],
        "summary": "Get Account Configurations",
        "parameters": [],
        "responses": {
          "200": {
            "description": "Successful response",
            "content": {
              "application/json": {
                "schema": {
                  "title": "AccountConfigurations",
                  "type": "object",
                  "x-examples": {
                    "example-1": {
                      "dtbp_check": "entry",
                      "trade_confirm_email": "all",
                      "suspend_trade": false,
                      "no_shorting": false,
                      "fractional_trading": true,
                      "max_margin_multiplier": "4",
                      "pdt_check": "entry",
                      "disable_overnight_trading": false
                    }
                  },
                  "description": "The account configuration API provides custom configurations about your trading account settings. These configurations control various allow you to modify settings to suit your trading needs.",
                  "properties": {
                    "dtbp_check": {
                      "type": "string",
                      "description": "both, entry, or exit. Controls Day Trading Margin Call (DTMC) checks.",
                      "enum": [
                        "both",
                        "entry",
                        "exit"
                      ]
                    },
                    "trade_confirm_email": {
                      "type": "string",
                      "description": "all or none. If none, emails for order fills are not sent."
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
                      "description": "Can be \"1\", \"2\", or \"4\""
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
                      "example": "entry",
                      "description": "`both`, `entry`, or `exit`. If entry orders will be rejected on entering a position if it could result in PDT being set for the account. exit will reject exiting orders if they would result in PDT being set."
                    },
                    "ptp_no_exception_entry": {
                      "type": "boolean",
                      "x-stoplight": {
                        "id": "8qvrtnzouzp80"
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
        "operationId": "getAccountConfig",
        "description": "gets the current account configuration values"
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
