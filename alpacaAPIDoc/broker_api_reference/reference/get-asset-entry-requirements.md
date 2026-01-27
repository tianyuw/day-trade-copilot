---
source_view: https://docs.alpaca.markets/reference/get-asset-entry-requirements
source_md: https://docs.alpaca.markets/reference/get-asset-entry-requirements.md
scraped_at_utc: 2026-01-27T04:30:48Z
---
# Retrieve Entry Requirements for requested assets

Returns all entry-requirements

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
      "name": "Assets"
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
    "/v1/assets/entry-requirements": {
      "get": {
        "tags": [
          "Assets"
        ],
        "summary": "Retrieve Entry Requirements for requested assets",
        "description": "Returns all entry-requirements",
        "responses": {
          "200": {
            "description": "An array of asset entry requirement objects.",
            "content": {
              "application/json": {
                "schema": {
                  "type": "array",
                  "items": {
                    "title": "AssetEntryRequirements",
                    "type": "object",
                    "description": "Defines the necessary conditions that must be met to initiate a position for a specific asset",
                    "required": [
                      "symbol"
                    ],
                    "properties": {
                      "symbol": {
                        "type": "string",
                        "example": "AAPL",
                        "description": "The symbol (or asset id) of the requested asset"
                      },
                      "regt_long": {
                        "type": "string",
                        "format": "decimal",
                        "description": "The percentage of the asset's market value required as Reg T (2x) buying power to open a long position",
                        "example": "0.5"
                      },
                      "regt_short": {
                        "type": "string",
                        "format": "decimal",
                        "description": "The percentage of the asset's market value required as Reg T (2x) buying power to open a short position",
                        "example": "0.5"
                      },
                      "dtbp_long": {
                        "type": "string",
                        "format": "decimal",
                        "description": "The percentage of the asset's market value required as Day Trading (4x) buying power to open a long position",
                        "example": "0.25"
                      },
                      "dtbp_short": {
                        "type": "string",
                        "format": "decimal",
                        "description": "The percentage of the asset's market value required as Day Trading (4x) buying power to open a short position",
                        "example": "0.3"
                      }
                    },
                    "x-readme-ref-name": "AssetEntryRequirements"
                  }
                }
              }
            }
          }
        },
        "operationId": "get-asset-entry-requirements",
        "parameters": [
          {
            "name": "symbols",
            "in": "query",
            "description": "Comma-separated symbols or asset ids. The symbols (or asset ids) for which asset entry requirements are to be requested. Maximum number of symbols allowed is 500.",
            "required": true,
            "schema": {
              "type": "string"
            },
            "example": "AAPL,SPY"
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
