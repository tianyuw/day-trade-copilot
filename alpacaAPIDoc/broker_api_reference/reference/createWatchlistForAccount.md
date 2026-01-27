---
source_view: https://docs.alpaca.markets/reference/createwatchlistforaccount
source_md: https://docs.alpaca.markets/reference/createwatchlistforaccount.md
scraped_at_utc: 2026-01-27T04:30:48Z
---
# Create a New Watchlist for an Account

Returns the watchlist object

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
      "name": "Watchlist"
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
    "/v1/trading/accounts/{account_id}/watchlists": {
      "parameters": [
        {
          "schema": {
            "type": "string",
            "format": "uuid"
          },
          "name": "account_id",
          "in": "path",
          "required": true,
          "description": "Unique identifier of an account."
        }
      ],
      "post": {
        "summary": "Create a New Watchlist for an Account",
        "tags": [
          "Watchlist"
        ],
        "operationId": "createWatchlistForAccount",
        "description": "Returns the watchlist object",
        "responses": {
          "200": {
            "description": "Newly created watchlist",
            "content": {
              "application/json": {
                "schema": {
                  "title": "Watchlist",
                  "type": "object",
                  "description": "Represents a set of securities observed by a user.",
                  "properties": {
                    "id": {
                      "type": "string",
                      "format": "uuid",
                      "description": "Unique identifier of the watchlist itself.\n"
                    },
                    "account_id": {
                      "type": "string",
                      "format": "uuid",
                      "description": "Unique identifier of the account that owns this watchlist.\n"
                    },
                    "created_at": {
                      "type": "string",
                      "format": "date-time",
                      "description": "When watchlist was created"
                    },
                    "updated_at": {
                      "type": "string",
                      "format": "date-time",
                      "description": "When watchlist was last updated"
                    },
                    "name": {
                      "type": "string",
                      "pattern": "^[a-zA-Z0-9]+$",
                      "description": "User friendly Name of watchlist"
                    },
                    "assets": {
                      "type": "array",
                      "description": "The contents of the watchlist, in the order as registered",
                      "items": {
                        "title": "Asset",
                        "type": "object",
                        "description": "Assets are sorted by asset class, exchange and symbol. Some assets are not tradable with Alpaca. These assets will be marked with the flag tradable=false",
                        "x-stoplight": {
                          "id": "2bnou9t588bau"
                        },
                        "properties": {
                          "id": {
                            "type": "string",
                            "example": "904837e3-3b76-47ec-b432-046db621571b",
                            "format": "uuid",
                            "description": "Asset ID"
                          },
                          "class": {
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
                          "exchange": {
                            "type": "string",
                            "title": "Exchange",
                            "example": "NASDAQ",
                            "description": "Represents the exchange where an asset is traded.\n\nFor Stocks:\n- AMEX\n- ARCA\n- BATS\n- NYSE\n- NASDAQ\n- NYSEARCA\n- OTC\n\nFor Crypto:\n- CRYPTO",
                            "enum": [
                              "AMEX",
                              "ARCA",
                              "BATS",
                              "NYSE",
                              "NASDAQ",
                              "NYSEARCA",
                              "OTC"
                            ],
                            "x-stoplight": {
                              "id": "og9z1j3oimssn"
                            },
                            "x-readme-ref-name": "Exchange"
                          },
                          "symbol": {
                            "type": "string",
                            "example": "AAPL",
                            "description": "The symbol of the asset"
                          },
                          "name": {
                            "type": "string",
                            "example": "Apple Inc. Common Stock",
                            "description": "The official name of the asset"
                          },
                          "status": {
                            "type": "string",
                            "enum": [
                              "active",
                              "inactive"
                            ],
                            "description": "active or inactive",
                            "example": "active"
                          },
                          "tradable": {
                            "type": "boolean",
                            "example": true,
                            "description": "Asset is tradable on Alpaca or not"
                          },
                          "marginable": {
                            "type": "boolean",
                            "example": true,
                            "description": "Asset is marginable or not"
                          },
                          "shortable": {
                            "type": "boolean",
                            "example": true,
                            "description": "Asset is shortable or not"
                          },
                          "easy_to_borrow": {
                            "type": "boolean",
                            "example": true,
                            "description": "Asset is easy-to-borrow or not (filtering for easy_to_borrow = True is the best way to check whether the name is currently available to short at Alpaca)."
                          },
                          "fractionable": {
                            "type": "boolean",
                            "example": true,
                            "description": "Asset is fractionable or not"
                          },
                          "min_order_size": {
                            "type": "string",
                            "x-stoplight": {
                              "id": "8oxfe2lh08pa5"
                            },
                            "description": "Minimum order size.  Field available for crypto only."
                          },
                          "min_trade_increment": {
                            "type": "string",
                            "x-stoplight": {
                              "id": "9x4innaekt0bo"
                            },
                            "description": "Amount a trade quantity can be incremented by. Field available for crypto only."
                          },
                          "price_increment": {
                            "type": "string",
                            "x-stoplight": {
                              "id": "y3hwtbjswugep"
                            },
                            "description": "Amount the price can be incremented by. Field available for crypto only."
                          },
                          "maintenance_margin_requirement": {
                            "type": "number",
                            "x-stoplight": {
                              "id": "w0vp53j3weqge"
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
                              "id": "o1v8vair7lg7a"
                            },
                            "description": "Supported values `ptp_no_exception`, `ptp_with_exception`, `ipo`, `has_options`, `options_late_close`, `fractional_eh_enabled`, `overnight_tradable`, `overnight_halted`.\nWe will include unique characteristics of the asset here.\nNote: `overnight_tradable` and `overnight_halted` are only available when overnight trading is enabled.",
                            "items": {
                              "x-stoplight": {
                                "id": "8q7bxjwl5evxu"
                              },
                              "type": "string",
                              "enum": [
                                "ptp_no_exception",
                                "ptp_with_exception",
                                "ipo",
                                "has_options",
                                "options_late_close",
                                "fractional_eh_enabled",
                                "overnight_tradable",
                                "overnight_halted"
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
                          "fractionable",
                          "maintenance_margin_requirement",
                          "margin_requirement_long",
                          "margin_requirement_short"
                        ],
                        "x-readme-ref-name": "Asset"
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
            }
          }
        },
        "requestBody": {
          "content": {
            "application/json": {
              "schema": {
                "title": "CreateWatchlistRequest",
                "type": "object",
                "description": "This model represents the fields you can specify when Creating or Updating/Replacing a Watchlist",
                "properties": {
                  "name": {
                    "type": "string",
                    "description": "The watchlist name"
                  },
                  "symbols": {
                    "type": "array",
                    "description": "The new list of symbol names to watch",
                    "items": {
                      "type": "string",
                      "example": "[\"AAPL\", \"TSLA\"]"
                    }
                  }
                },
                "required": [
                  "name",
                  "symbols"
                ],
                "x-stoplight": {
                  "id": "8vevle6of8odv"
                },
                "x-readme-ref-name": "CreateWatchlistRequest"
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
