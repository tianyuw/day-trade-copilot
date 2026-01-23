---
source_view: https://docs.alpaca.markets/reference/getopenposition-1
source_md: https://docs.alpaca.markets/reference/getopenposition-1.md
scraped_at_utc: 2026-01-22T23:02:18Z
---
# Get an Open Position

Retrieves the account’s open position for the given symbol or assetId.

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
      "name": "Positions"
    }
  ],
  "paths": {
    "/v2/positions/{symbol_or_asset_id}": {
      "get": {
        "tags": [
          "Positions"
        ],
        "summary": "Get an Open Position",
        "description": "Retrieves the account’s open position for the given symbol or assetId.",
        "parameters": [],
        "responses": {
          "200": {
            "description": "Successful response",
            "content": {
              "application/json": {
                "schema": {
                  "description": "The positions API provides information about an account’s current open positions. The response will include information such as cost basis, shares traded, and market value, which will be updated live as price information is updated. Once a position is closed, it will no longer be queryable through this API.",
                  "type": "object",
                  "x-examples": {
                    "example-1": {
                      "asset_id": "904837e3-3b76-47ec-b432-046db621571b",
                      "symbol": "AAPL",
                      "exchange": "NASDAQ",
                      "asset_class": "us_equity",
                      "avg_entry_price": "100.0",
                      "qty": "5",
                      "qty_available": "4",
                      "side": "long",
                      "market_value": "600.0",
                      "cost_basis": "500.0",
                      "unrealized_pl": "100.0",
                      "unrealized_plpc": "0.20",
                      "unrealized_intraday_pl": "10.0",
                      "unrealized_intraday_plpc": "0.0084",
                      "current_price": "120.0",
                      "lastday_price": "119.0",
                      "change_today": "0.0084"
                    },
                    "example-2": {
                      "asset_id": "b0b6dd9d-8b9b-48a9-ba46-b9d54906e415",
                      "symbol": "AAPL",
                      "exchange": "NASDAQ",
                      "asset_class": "us_equity",
                      "asset_marginable": false,
                      "qty": "2",
                      "qty_available": "2",
                      "avg_entry_price": "174.78",
                      "side": "long",
                      "market_value": "348.58",
                      "cost_basis": "349.56",
                      "unrealized_pl": "-0.98",
                      "unrealized_plpc": "-0.0028035244307129",
                      "unrealized_intraday_pl": "-0.98",
                      "unrealized_intraday_plpc": "-0.0028035244307129",
                      "current_price": "174.29",
                      "lastday_price": "174.61",
                      "change_today": "-0.0018326556325525"
                    }
                  },
                  "title": "Position",
                  "properties": {
                    "asset_id": {
                      "type": "string",
                      "description": "Asset ID (For options this represents the option contract ID)",
                      "format": "uuid"
                    },
                    "symbol": {
                      "type": "string",
                      "description": "Symbol name of the asset",
                      "example": "AAPL"
                    },
                    "exchange": {
                      "title": "Exchange",
                      "type": "string",
                      "description": "Represents the current exchanges Alpaca supports. List is currently:\n\n- AMEX\n- ARCA\n- BATS\n- NYSE\n- NASDAQ\n- NYSEARCA\n- OTC\n\nCan be empty if not applicable (e.g., for options contracts)",
                      "enum": [
                        "AMEX",
                        "ARCA",
                        "BATS",
                        "NYSE",
                        "NASDAQ",
                        "NYSEARCA",
                        "OTC",
                        null
                      ],
                      "example": "NYSE",
                      "x-readme-ref-name": "ExchangeForPosition"
                    },
                    "asset_class": {
                      "type": "string",
                      "title": "AssetClass",
                      "enum": [
                        "us_equity",
                        "us_option",
                        "crypto"
                      ],
                      "example": "us_equity",
                      "description": "This represents the category to which the asset belongs to. It serves to identify the nature of the financial instrument, with options including \"us_equity\" for U.S. equities, \"us_option\" for U.S. options, and \"crypto\" for cryptocurrencies.",
                      "x-examples": {
                        "example-1": "us_equity"
                      },
                      "x-readme-ref-name": "AssetClass"
                    },
                    "avg_entry_price": {
                      "type": "string",
                      "minLength": 1,
                      "description": "Average entry price of the position"
                    },
                    "qty": {
                      "type": "string",
                      "minLength": 1,
                      "description": "The number of shares"
                    },
                    "qty_available": {
                      "type": "string",
                      "minLength": 1,
                      "description": "Total number of shares available minus open orders / locked for options covered call"
                    },
                    "side": {
                      "type": "string",
                      "minLength": 1,
                      "description": "“long”"
                    },
                    "market_value": {
                      "type": "string",
                      "minLength": 1,
                      "description": "Total dollar amount of the position"
                    },
                    "cost_basis": {
                      "type": "string",
                      "minLength": 1,
                      "description": "Total cost basis in dollar"
                    },
                    "unrealized_pl": {
                      "type": "string",
                      "minLength": 1,
                      "description": "Unrealized profit/loss in dollars"
                    },
                    "unrealized_plpc": {
                      "type": "string",
                      "minLength": 1,
                      "description": "Unrealized profit/loss percent (by a factor of 1)"
                    },
                    "unrealized_intraday_pl": {
                      "type": "string",
                      "minLength": 1,
                      "description": "Unrealized profit/loss in dollars for the day"
                    },
                    "unrealized_intraday_plpc": {
                      "type": "string",
                      "minLength": 1,
                      "description": "Unrealized profit/loss percent (by a factor of 1)"
                    },
                    "current_price": {
                      "type": "string",
                      "minLength": 1,
                      "description": "Current asset price per share"
                    },
                    "lastday_price": {
                      "type": "string",
                      "minLength": 1,
                      "description": "Last day’s asset price per share based on the closing value of the last trading day"
                    },
                    "change_today": {
                      "type": "string",
                      "minLength": 1,
                      "description": "Percent change from last day price (by a factor of 1)"
                    },
                    "asset_marginable": {
                      "type": "boolean"
                    }
                  },
                  "required": [
                    "asset_id",
                    "symbol",
                    "exchange",
                    "asset_class",
                    "avg_entry_price",
                    "qty",
                    "side",
                    "market_value",
                    "cost_basis",
                    "unrealized_pl",
                    "unrealized_plpc",
                    "unrealized_intraday_pl",
                    "unrealized_intraday_plpc",
                    "current_price",
                    "lastday_price",
                    "change_today",
                    "asset_marginable"
                  ],
                  "x-readme-ref-name": "Position"
                }
              }
            }
          }
        },
        "operationId": "getOpenPosition"
      },
      "parameters": [
        {
          "schema": {
            "type": "string"
          },
          "name": "symbol_or_asset_id",
          "in": "path",
          "required": true,
          "description": "symbol or assetId"
        }
      ]
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
