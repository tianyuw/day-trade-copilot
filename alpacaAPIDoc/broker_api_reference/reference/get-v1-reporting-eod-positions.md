---
source_view: https://docs.alpaca.markets/reference/get-v1-reporting-eod-positions
source_md: https://docs.alpaca.markets/reference/get-v1-reporting-eod-positions.md
scraped_at_utc: 2026-01-27T04:30:48Z
---
# Retrieve EOD Positions

This API retrieves a comprehensive list of end-of-day positions for all accounts. End-of-day (EOD) positions are typically accessible after 4:00 am Eastern Time (ET) on the following day, providing a comprehensive view of the day's closing positions across all accounts.
This API currently only supports retrieving EOD positions for the last trading date.

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
    "/v1/reporting/eod/positions": {
      "get": {
        "summary": "Retrieve EOD Positions",
        "tags": [
          "Reporting"
        ],
        "responses": {
          "200": {
            "description": "Successful response containing the end-of-day positions for the specified accounts.",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "asof": {
                      "type": "string",
                      "format": "date",
                      "description": "The date of the snapshot in the 'YYYY-MM-DD' format."
                    },
                    "positions": {
                      "type": "object",
                      "description": "A detailed map of account IDs to their respective positions.",
                      "additionalProperties": {
                        "type": "array",
                        "items": {
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
                    },
                    "next_page_token": {
                      "type": "string",
                      "description": "Use this token in your next API call to paginate through the dataset and retrieve the next page of results. A null token indicates there are no more data to fetch.\n",
                      "nullable": true,
                      "example": "MTAwMA==",
                      "x-readme-ref-name": "NextPageToken"
                    }
                  }
                }
              }
            }
          },
          "422": {
            "description": "This can be returned if the asof param does not match the latest snap available at Alpaca."
          }
        },
        "operationId": "get-v1-reporting-eod-positions",
        "description": "This API retrieves a comprehensive list of end-of-day positions for all accounts. End-of-day (EOD) positions are typically accessible after 4:00 am Eastern Time (ET) on the following day, providing a comprehensive view of the day's closing positions across all accounts.\nThis API currently only supports retrieving EOD positions for the last trading date.",
        "parameters": [
          {
            "name": "account_id",
            "in": "query",
            "schema": {
              "type": "string",
              "format": "uuid"
            },
            "description": "Filter the results by account_id (optional)."
          },
          {
            "name": "asset",
            "in": "query",
            "schema": {
              "type": "string"
            },
            "description": "Filter the results by asset ID or symbol (optional)."
          },
          {
            "name": "asof",
            "in": "query",
            "schema": {
              "type": "string",
              "format": "date"
            },
            "description": "The positions date in 'YYYY-MM-DD' format. It's recommended to provide this parameter when the 'page' parameter is specified, to ensure precise data retrieval based on the desired date.\nOnly previous trading date is supported."
          },
          {
            "name": "page_token",
            "in": "query",
            "required": false,
            "description": "Used for pagination, this token retrieves the next page of results. It is obtained from the response of the preceding page when additional pages are available.",
            "schema": {
              "type": "string",
              "example": "MA=="
            }
          },
          {
            "name": "limit",
            "in": "query",
            "schema": {
              "type": "integer"
            },
            "description": "The number of accounts to display per page (default=1000, max=10000)."
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
