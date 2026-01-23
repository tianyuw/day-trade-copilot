---
source_view: https://docs.alpaca.markets/reference/removeassetfromwatchlist-1
source_md: https://docs.alpaca.markets/reference/removeassetfromwatchlist-1.md
scraped_at_utc: 2026-01-22T23:02:18Z
---
# Delete Symbol from Watchlist

Delete one entry for an asset by symbol name

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
      "name": "Watchlists"
    }
  ],
  "paths": {
    "/v2/watchlists/{watchlist_id}/{symbol}": {
      "delete": {
        "tags": [
          "Watchlists"
        ],
        "summary": "Delete Symbol from Watchlist",
        "parameters": [],
        "responses": {
          "200": {
            "content": {
              "application/json": {
                "schema": {
                  "description": "The watchlist API provides CRUD operation for the account’s watchlist. An account can have multiple watchlists and each is uniquely identified by id but can also be addressed by user-defined name. Each watchlist is an ordered list of assets.\n",
                  "type": "object",
                  "x-examples": {
                    "example-1": {
                      "id": "3174d6df-7726-44b4-a5bd-7fda5ae6e009",
                      "account_id": "abe25343-a7ba-4255-bdeb-f7e013e9ee5d",
                      "created_at": "2022-01-31T21:49:05.14628Z",
                      "updated_at": "2022-01-31T21:49:05.14628Z",
                      "name": "Primary Watchlist",
                      "assets": [
                        {
                          "id": "8ccae427-5dd0-45b3-b5fe-7ba5e422c766",
                          "class": "us_equity",
                          "exchange": "NASDAQ",
                          "symbol": "TSLA",
                          "name": "Tesla, Inc. Common Stock",
                          "status": "active",
                          "tradable": true,
                          "marginable": true,
                          "shortable": true,
                          "easy_to_borrow": true,
                          "fractionable": true
                        }
                      ]
                    }
                  },
                  "title": "Watchlist",
                  "properties": {
                    "id": {
                      "type": "string",
                      "format": "uuid",
                      "description": "watchlist id"
                    },
                    "account_id": {
                      "type": "string",
                      "format": "uuid",
                      "description": "account ID"
                    },
                    "created_at": {
                      "type": "string",
                      "format": "date-time"
                    },
                    "updated_at": {
                      "type": "string",
                      "format": "date-time"
                    },
                    "name": {
                      "type": "string",
                      "minLength": 1,
                      "description": "user-defined watchlist name (up to 64 characters)"
                    },
                    "assets": {
                      "type": "array",
                      "description": "the content of this watchlist, in the order as registered by the client",
                      "items": {
                        "description": "The assets API serves as the master list of assets available for trade and data consumption from Alpaca. Assets are sorted by asset class, exchange and symbol. Some assets are only available for data consumption via Polygon, and are not tradable with Alpaca. These assets will be marked with the flag tradable=false.\n",
                        "type": "object",
                        "x-examples": {
                          "example-1": {
                            "id": "b0b6dd9d-8b9b-48a9-ba46-b9d54906e415",
                            "class": "us_equity",
                            "exchange": "NASDAQ",
                            "symbol": "AAPL",
                            "name": "Apple Inc. Common Stock",
                            "status": "active",
                            "tradable": true,
                            "marginable": true,
                            "shortable": true,
                            "easy_to_borrow": true,
                            "fractionable": true
                          }
                        },
                        "title": "Assets",
                        "properties": {
                          "id": {
                            "type": "string",
                            "format": "uuid",
                            "description": "Asset ID"
                          },
                          "class": {
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
                          "cusip": {
                            "type": "string",
                            "nullable": true,
                            "description": "The CUSIP identifier for the asset (US Equities only).\nTo request a specific CUSIP, please reach out to Alpaca support.\n",
                            "example": "987654321"
                          },
                          "exchange": {
                            "title": "Exchange",
                            "type": "string",
                            "description": "Represents the current exchanges Alpaca supports. List is currently:\n\n- AMEX\n- ARCA\n- BATS\n- NYSE\n- NASDAQ\n- NYSEARCA\n- OTC",
                            "enum": [
                              "AMEX",
                              "ARCA",
                              "BATS",
                              "NYSE",
                              "NASDAQ",
                              "NYSEARCA",
                              "OTC"
                            ],
                            "example": "NYSE",
                            "x-readme-ref-name": "Exchange"
                          },
                          "symbol": {
                            "type": "string",
                            "description": "The symbol of the asset",
                            "example": "AAPL"
                          },
                          "name": {
                            "type": "string",
                            "minLength": 1,
                            "description": "The official name of the asset"
                          },
                          "status": {
                            "type": "string",
                            "description": "active or inactive",
                            "example": "active",
                            "enum": [
                              "active",
                              "inactive"
                            ]
                          },
                          "tradable": {
                            "type": "boolean",
                            "description": "Asset is tradable on Alpaca or not"
                          },
                          "marginable": {
                            "type": "boolean",
                            "description": "Asset is marginable or not"
                          },
                          "shortable": {
                            "type": "boolean",
                            "description": "Asset is shortable or not"
                          },
                          "easy_to_borrow": {
                            "type": "boolean",
                            "description": "Asset is easy-to-borrow or not (filtering for easy_to_borrow = True is the best way to check whether the name is currently available to short at Alpaca)."
                          },
                          "fractionable": {
                            "type": "boolean",
                            "description": "Asset is fractionable or not"
                          },
                          "maintenance_margin_requirement": {
                            "type": "number",
                            "x-stoplight": {
                              "id": "kujwjd2dcq9bn"
                            },
                            "deprecated": true,
                            "description": "**deprecated**: Please use margin_requirement_long or margin_requirement_short instead. Note that these fields are of type string.\nShows the margin requirement percentage for the asset (equities only).\n"
                          },
                          "margin_requirement_long": {
                            "type": "string",
                            "description": "The margin requirement percentage for the asset's long positions (equities only)."
                          },
                          "margin_requirement_short": {
                            "type": "string",
                            "description": "The margin requirement percentage for the asset's short positions (equities only)."
                          },
                          "attributes": {
                            "type": "array",
                            "x-stoplight": {
                              "id": "40mjg4fj0ykl8"
                            },
                            "description": "One of `ptp_no_exception`, `ptp_with_exception`, `ipo`, `has_options`, or `options_late_close`. We will include unique characteristics of the asset here.",
                            "items": {
                              "type": "string",
                              "enum": [
                                "ptp_no_exception",
                                "ptp_with_exception",
                                "ipo",
                                "has_options",
                                "options_late_close"
                              ]
                            },
                            "example": [
                              "ptp_no_exception",
                              "ipo"
                            ]
                          }
                        },
                        "required": [
                          "id",
                          "class",
                          "exchange",
                          "symbol",
                          "name",
                          "status",
                          "tradable",
                          "marginable",
                          "shortable",
                          "easy_to_borrow",
                          "fractionable"
                        ],
                        "x-readme-ref-name": "Assets"
                      }
                    }
                  },
                  "required": [
                    "id",
                    "account_id",
                    "created_at",
                    "updated_at",
                    "name"
                  ],
                  "x-readme-ref-name": "Watchlist"
                }
              }
            },
            "description": "Returns the updated watchlist"
          }
        },
        "operationId": "removeAssetFromWatchlist",
        "description": "Delete one entry for an asset by symbol name"
      },
      "parameters": [
        {
          "schema": {
            "type": "string",
            "format": "uuid"
          },
          "name": "watchlist_id",
          "in": "path",
          "required": true,
          "description": "Watchlist ID"
        },
        {
          "schema": {
            "type": "string"
          },
          "name": "symbol",
          "in": "path",
          "required": true,
          "description": "symbol name to remove from the watchlist content"
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
