---
source_view: https://docs.alpaca.markets/reference/getOAuthClient
source_md: https://docs.alpaca.markets/reference/getOAuthClient.md
scraped_at_utc: 2026-01-27T04:30:48Z
---
# Get an OAuth client

The endpoint returns the details of OAuth client to display in the authorization page.


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
      "name": "OAuth"
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
    "/v1/oauth/clients/{client_id}": {
      "parameters": [
        {
          "name": "client_id",
          "required": true,
          "in": "path",
          "schema": {
            "type": "string",
            "format": "uuid"
          }
        }
      ],
      "get": {
        "summary": "Get an OAuth client",
        "tags": [
          "OAuth"
        ],
        "description": "The endpoint returns the details of OAuth client to display in the authorization page.\n",
        "parameters": [
          {
            "name": "response_type",
            "in": "query",
            "schema": {
              "type": "string",
              "enum": [
                "code",
                "token"
              ],
              "example": "token"
            },
            "description": "code or token"
          },
          {
            "name": "redirect_uri",
            "in": "query",
            "schema": {
              "type": "string",
              "example": "https://example.com/authorize"
            },
            "description": "Redirect URI of the OAuth flow"
          },
          {
            "name": "scope",
            "in": "query",
            "schema": {
              "type": "string",
              "example": "general"
            },
            "description": "Requested scopes by the OAuth flow"
          }
        ],
        "responses": {
          "200": {
            "description": "Success.",
            "content": {
              "application/json": {
                "schema": {
                  "title": "OathClientResponse",
                  "type": "object",
                  "example": {
                    "client_id": "7a3c52a910e1dc2abbb14da2b6b8e711",
                    "name": "TradingApp",
                    "description": "Sample description",
                    "url": "http://test.com",
                    "terms_of_use": "",
                    "privacy_policy": "",
                    "status": "ACTIVE",
                    "redirect_uri": [
                      "http://localhost"
                    ],
                    "live_trading_approved": true
                  },
                  "x-examples": {
                    "example-1": {
                      "client_id": "7a3c52a910e1dc2abbb14da2b6b8e711",
                      "name": "TradingApp",
                      "description": "Sample description",
                      "url": "http://test.com",
                      "terms_of_use": "",
                      "privacy_policy": "",
                      "status": "ACTIVE",
                      "redirect_uri": [
                        "http://localhost"
                      ],
                      "live_trading_approved": true
                    }
                  },
                  "properties": {
                    "client_id": {
                      "type": "string",
                      "description": "OAuth client id"
                    },
                    "name": {
                      "type": "string",
                      "description": "Broker name (your name)"
                    },
                    "description": {
                      "type": "string"
                    },
                    "url": {
                      "type": "string"
                    },
                    "terms_of_use": {
                      "type": "string",
                      "description": "URL of Terms of Use"
                    },
                    "privacy_policy": {
                      "type": "string",
                      "description": "URL of Privacy Policy"
                    },
                    "status": {
                      "type": "string",
                      "enum": [
                        "ACTIVE",
                        "DISABLED"
                      ],
                      "description": "ACTIVE or DISABLED",
                      "example": "ACTIVE"
                    },
                    "redirect_uri": {
                      "type": "array",
                      "items": {
                        "type": "string"
                      }
                    },
                    "live_trading_approved": {
                      "type": "boolean",
                      "example": true
                    }
                  },
                  "x-stoplight": {
                    "id": "qlcf3oshsqct1"
                  },
                  "x-readme-ref-name": "OathClientResponse"
                },
                "examples": {
                  "example-1": {
                    "value": {
                      "client_id": "7a3c52a910e1dc2abbb14da2b6b8e711",
                      "name": "TradingApp",
                      "description": "Sample description",
                      "url": "http://test.com",
                      "terms_of_use": "",
                      "privacy_policy": "",
                      "status": "ACTIVE",
                      "redirect_uri": [
                        "http://localhost"
                      ],
                      "live_trading_approved": false
                    }
                  }
                }
              }
            }
          },
          "401": {
            "description": "Client does not exist or you do not have access to the client.\n",
            "content": {
              "application/json": {
                "schema": {
                  "type": "string"
                }
              }
            }
          }
        },
        "operationId": "getOAuthClient"
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
