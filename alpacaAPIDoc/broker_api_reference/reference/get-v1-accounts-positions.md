---
source_view: https://docs.alpaca.markets/reference/get-v1-accounts-positions
source_md: https://docs.alpaca.markets/reference/get-v1-accounts-positions.md
scraped_at_utc: 2026-01-27T04:30:48Z
---
# Bulk Fetch All Accounts Positions

Retrieves a list of the account’s open positions.
This endpoint is deprecated and will be removed in the future. Please use the [GET /v1/reporting/eod/positions endpoint](https://docs.alpaca.markets/reference/get-v1-reporting-eod-positions-1) instead.


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
    "/v1/accounts/positions": {
      "get": {
        "summary": "Bulk Fetch All Accounts Positions",
        "deprecated": true,
        "tags": [
          "Trading"
        ],
        "responses": {
          "200": {
            "description": "The response contains two fields:\n\nasof: the timestamp for which the positions are returned. It is always the last market close\n\npositions: an account-id to position list map, contains the requested page’s accounts\nThe positions map is empty for the last page.\n\nNote: when fetching bulk positions, which can take multiple minutes depending on the number of accounts managed have, a market close can happen, and after that a new set of results might be returned. To make sure results are consistent, please always check that the as_of field didn’t change during the whole fetching process.",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "as_of": {
                      "type": "string",
                      "x-stoplight": {
                        "id": "4nvwcf6eps5vb"
                      },
                      "format": "date-time"
                    },
                    "positions": {
                      "type": "object",
                      "x-stoplight": {
                        "id": "yluo5l5ya9i7u"
                      }
                    }
                  }
                },
                "examples": {
                  "Example 1": {
                    "value": {
                      "as_of": "2022-08-04T16:00:00-04:00",
                      "positions": {
                        "000c8a47-7487-430b-94e1-e628a71cd123": [
                          {
                            "asset_id": "b0b6dd9d-8b9b-48a9-ba46-b9d54906e415",
                            "symbol": "AAPL",
                            "exchange": "NASDAQ",
                            "asset_class": "us_equity",
                            "asset_marginable": true,
                            "qty": "0.079145874",
                            "avg_entry_price": "172.34",
                            "side": "long",
                            "market_value": "13.14850404762",
                            "cost_basis": "13.63999992516",
                            "unrealized_pl": "-0.49149587754",
                            "unrealized_plpc": "-0.0360334223047464",
                            "unrealized_intraday_pl": "0",
                            "unrealized_intraday_plpc": "0",
                            "current_price": "166.13",
                            "lastday_price": "166.13",
                            "change_today": "0",
                            "qty_available": "0.079145874"
                          }
                        ]
                      }
                    }
                  }
                }
              }
            }
          }
        },
        "operationId": "get-v1-accounts-positions",
        "description": "Retrieves a list of the account’s open positions.\nThis endpoint is deprecated and will be removed in the future. Please use the [GET /v1/reporting/eod/positions endpoint](https://docs.alpaca.markets/reference/get-v1-reporting-eod-positions-1) instead.\n",
        "parameters": [
          {
            "name": "page",
            "in": "query",
            "schema": {
              "type": "integer"
            },
            "description": "The number of the page of the results to be fetched."
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
