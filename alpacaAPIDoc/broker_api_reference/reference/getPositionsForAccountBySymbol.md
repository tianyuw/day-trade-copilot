---
source_view: https://docs.alpaca.markets/reference/getpositionsforaccountbysymbol
source_md: https://docs.alpaca.markets/reference/getpositionsforaccountbysymbol.md
scraped_at_utc: 2026-01-27T04:30:48Z
---
# Get an Open Position for account by Symbol or AssetId

Retrieves the account’s open position for the given symbol or asset_id.

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
    "/v1/trading/accounts/{account_id}/positions/{symbol_or_asset_id}": {
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
        },
        {
          "schema": {
            "type": "string"
          },
          "name": "symbol_or_asset_id",
          "in": "path",
          "required": true,
          "description": "The symbol or asset_id "
        }
      ],
      "get": {
        "summary": "Get an Open Position for account by Symbol or AssetId",
        "responses": {
          "200": {
            "description": "The requested Position object",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "x-examples": {
                    "example-1": {
                      "asset_id": "93f58d0b-6c53-432d-b8ce-2bad264dbd94",
                      "symbol": "AAPL",
                      "exchange": "NASDAQ",
                      "asset_class": "us_equity",
                      "asset_marginable": false,
                      "qty": "4",
                      "qty_available": "4",
                      "avg_entry_price": "172.08",
                      "side": "long",
                      "market_value": "688.32",
                      "cost_basis": "688.32",
                      "unrealized_pl": "0",
                      "unrealized_plpc": "0",
                      "unrealized_intraday_pl": "0",
                      "unrealized_intraday_plpc": "0",
                      "current_price": "172.08",
                      "lastday_price": "168.88",
                      "change_today": "0.0189483657034581"
                    }
                  },
                  "x-stoplight": {
                    "id": "b2tmookzpqlzr"
                  },
                  "properties": {
                    "asset_id": {
                      "type": "string",
                      "example": "904837e3-3b76-47ec-b432-046db621571b",
                      "format": "uuid",
                      "description": "Asset ID (For options this represents the option contract ID)"
                    },
                    "symbol": {
                      "type": "string",
                      "example": "AAPL",
                      "description": "Asset symbol"
                    },
                    "exchange": {
                      "type": "string",
                      "example": "NASDAQ",
                      "description": "Exchange name of the asset"
                    },
                    "asset_class": {
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
                    },
                    "asset_marginable": {
                      "type": "boolean",
                      "description": "Indicates if this asset is marginable"
                    },
                    "avg_entry_price": {
                      "type": "string",
                      "example": "100.0",
                      "description": "Average entry price of the position"
                    },
                    "qty": {
                      "type": "string",
                      "example": "5",
                      "description": "The number of shares"
                    },
                    "qty_available": {
                      "type": "string",
                      "example": "5",
                      "description": "Total number of shares available minus open orders / locked for options covered call"
                    },
                    "side": {
                      "type": "string",
                      "example": "long",
                      "enum": [
                        "long",
                        "short"
                      ]
                    },
                    "market_value": {
                      "type": "string",
                      "format": "decimal",
                      "example": "600.0",
                      "description": "Total market value of the position"
                    },
                    "cost_basis": {
                      "type": "string",
                      "format": "decimal",
                      "example": "500.0",
                      "description": "Total cost basis"
                    },
                    "unrealized_pl": {
                      "type": "string",
                      "format": "decimal",
                      "example": "100.0",
                      "description": "Unrealized profit/loss"
                    },
                    "unrealized_plpc": {
                      "type": "string",
                      "format": "decimal",
                      "example": "0.20",
                      "description": "Unrealized profit/loss percent (by a factor of 1)"
                    },
                    "unrealized_intraday_pl": {
                      "type": "string",
                      "format": "decimal",
                      "example": "10.0",
                      "description": "Unrealized profit/loss for the day"
                    },
                    "unrealized_intraday_plpc": {
                      "type": "string",
                      "format": "decimal",
                      "example": "0.0084",
                      "description": "Unrealized interday profit/loss percent (by a factor of 1)"
                    },
                    "current_price": {
                      "type": "string",
                      "format": "decimal",
                      "example": "120.0",
                      "description": "Current asset price per share"
                    },
                    "lastday_price": {
                      "type": "string",
                      "format": "decimal",
                      "example": "119.0",
                      "description": "Last day’s asset price per share based on the closing value of the last trading day"
                    },
                    "change_today": {
                      "type": "string",
                      "format": "decimal",
                      "example": "0.0084",
                      "description": "Percent change from last day price (by a factor of 1)"
                    },
                    "swap_rate": {
                      "type": "string",
                      "format": "decimal",
                      "description": "The latest swap rate. This is only returned for LCT accounts.",
                      "example": "1.50",
                      "x-stoplight": {
                        "id": "t02dt3rtisrkx"
                      }
                    },
                    "avg_entry_swap_rate": {
                      "type": "string",
                      "format": "decimal",
                      "description": "The average swap rate of the position. This is only returned for LCT accounts.",
                      "example": "1.40",
                      "x-stoplight": {
                        "id": "a0kh9eu3byvfp"
                      }
                    },
                    "usd": {
                      "title": "USDPosition",
                      "description": "Position values in USD. This is returned for LCT (non-USD) accounts only.",
                      "type": "object",
                      "properties": {
                        "avg_entry_price": {
                          "type": "string",
                          "format": "decimal",
                          "description": "Average entry price of the position in USD",
                          "example": "71.43"
                        },
                        "market_value": {
                          "type": "string",
                          "format": "decimal",
                          "description": "Total market value of the position in USD",
                          "example": "400.00"
                        },
                        "cost_basis": {
                          "type": "string",
                          "format": "decimal",
                          "description": "Total cost basis in USD",
                          "example": "333.33"
                        },
                        "unrealized_pl": {
                          "type": "string",
                          "format": "decimal",
                          "description": "Unrealized profit/loss in USD",
                          "example": "66.67"
                        },
                        "unrealized_plpc": {
                          "type": "string",
                          "format": "decimal",
                          "description": "Unrealized profit/loss percent (by a factor of 1)",
                          "example": "0.2"
                        },
                        "unrealized_intraday_pl": {
                          "type": "string",
                          "format": "decimal",
                          "description": "Unrealized profit/loss in USD for the day",
                          "example": "6.67"
                        },
                        "unrealized_intraday_plpc": {
                          "type": "string",
                          "format": "decimal",
                          "description": "Unrealized interday profit/loss percent (by a factor of 1)",
                          "example": "0.0084"
                        },
                        "current_price": {
                          "type": "string",
                          "format": "decimal",
                          "description": "Current asset price per share in USD",
                          "example": "80.0"
                        },
                        "lastday_price": {
                          "type": "string",
                          "format": "decimal",
                          "description": "Last day’s asset price per share based on the closing value of the last trading day in USD",
                          "example": "79.33"
                        },
                        "change_today": {
                          "type": "string",
                          "format": "decimal",
                          "description": "Percent change from last day price (by a factor of 1)",
                          "example": "0.67"
                        }
                      },
                      "x-readme-ref-name": "USDPosition"
                    }
                  },
                  "required": [
                    "asset_id",
                    "symbol",
                    "exchange",
                    "asset_class",
                    "avg_entry_price",
                    "qty",
                    "qty_available",
                    "side",
                    "market_value",
                    "cost_basis",
                    "unrealized_pl",
                    "unrealized_plpc",
                    "unrealized_intraday_pl",
                    "unrealized_intraday_plpc",
                    "current_price",
                    "lastday_price",
                    "change_today"
                  ],
                  "x-readme-ref-name": "Position"
                }
              }
            }
          },
          "404": {
            "description": "Account doesn't have a position for this symbol or asset_id "
          }
        },
        "operationId": "getPositionsForAccountBySymbol",
        "description": "Retrieves the account’s open position for the given symbol or asset_id.",
        "tags": [
          "Trading"
        ]
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
