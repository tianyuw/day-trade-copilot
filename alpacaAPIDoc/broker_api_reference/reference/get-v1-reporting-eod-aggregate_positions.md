---
source_view: https://docs.alpaca.markets/reference/get-v1-reporting-eod-aggregate_positions
source_md: https://docs.alpaca.markets/reference/get-v1-reporting-eod-aggregate_positions.md
scraped_at_utc: 2026-01-27T04:30:48Z
---
# Retrieve Aggregate Positions

This API endpoint provides reporting data to partners for aggregate common stock and crypto positions across their account base. Partners can view historical snapshots of their holding across their entire account base. Please note that this API utilizes an 8:00 pm (EST) cutoff which aligns with the end of the Securities extended hours trading session as well as Alpaca’s 24 hour Crypto trading window. Additionally, the endpoint supports indexing to help the partner efficiently filter by key information including date and symbol while being able to include or remove firm accounts.

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
      "name": "Reporting"
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
    "/v1/reporting/eod/aggregate_positions": {
      "get": {
        "summary": "Retrieve Aggregate Positions",
        "tags": [
          "Reporting"
        ],
        "responses": {
          "200": {
            "description": "Array of objects, each object pertains to the date specified in the request and a unique asset. See parameters below. Notes: Returns an empty array for non-trading days, assets with no positions are omitted.",
            "content": {
              "application/json": {
                "schema": {
                  "type": "array",
                  "items": {
                    "type": "object",
                    "x-examples": {
                      "Example 1": {
                        "symbol": "AAPL",
                        "cusip": "037833100",
                        "long_qty": "1",
                        "short_qty": "0",
                        "long_market_value": "148.4700",
                        "short_market_value": "0",
                        "num_accounts": "1",
                        "asset_type": "us_equity",
                        "closing_price": "148.4700"
                      }
                    },
                    "properties": {
                      "symbol": {
                        "type": "string",
                        "description": "Symbol of asset"
                      },
                      "cusip": {
                        "type": "string",
                        "description": "Cusip (9 digits, can start with 0’s)",
                        "format": "decimal"
                      },
                      "long_qty": {
                        "type": "string",
                        "description": "Aggregate number of shares that the partner is long",
                        "format": "decimal"
                      },
                      "short_qty": {
                        "type": "string",
                        "description": "Aggregate number of shares that the partner is short",
                        "format": "decimal"
                      },
                      "long_market_value": {
                        "type": "string",
                        "description": "Aggregate notional dollar amount of the partner’s long positions",
                        "format": "decimal"
                      },
                      "short_market_value": {
                        "type": "string",
                        "description": "Aggregate notional dollar amount of the partner’s short positions",
                        "format": "decimal"
                      },
                      "num_accounts": {
                        "type": "integer",
                        "description": "Number of accounts that have a position in this asset (either long or short)",
                        "format": "decimal"
                      },
                      "asset_type": {
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
                      "closing_price": {
                        "type": "string",
                        "description": "EOD asset price per share at session close",
                        "format": "decimal"
                      }
                    },
                    "title": "",
                    "x-readme-ref-name": "AggregatePositionResponse"
                  }
                }
              }
            }
          }
        },
        "operationId": "get-v1-reporting-eod-aggregate_positions",
        "description": "This API endpoint provides reporting data to partners for aggregate common stock and crypto positions across their account base. Partners can view historical snapshots of their holding across their entire account base. Please note that this API utilizes an 8:00 pm (EST) cutoff which aligns with the end of the Securities extended hours trading session as well as Alpaca’s 24 hour Crypto trading window. Additionally, the endpoint supports indexing to help the partner efficiently filter by key information including date and symbol while being able to include or remove firm accounts.",
        "parameters": [
          {
            "name": "date",
            "in": "query",
            "required": true,
            "schema": {
              "type": "string",
              "format": "date"
            },
            "description": "“YYYY-MM-DD” format"
          },
          {
            "name": "symbols",
            "in": "query",
            "schema": {
              "type": "string"
            },
            "description": "Comma-separated symbols. If populated, then only the specified symbols will be returned. If null, then all symbols will be included in the response."
          },
          {
            "name": "firm_accounts",
            "in": "query",
            "schema": {
              "type": "string"
            },
            "description": "Defaults to True which includes firm accounts. Passing False will exclude all firm accounts."
          }
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
