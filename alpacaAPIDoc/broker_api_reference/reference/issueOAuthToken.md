---
source_view: https://docs.alpaca.markets/reference/issueOAuthToken
source_md: https://docs.alpaca.markets/reference/issueOAuthToken.md
scraped_at_utc: 2026-01-27T04:30:48Z
---
# Issue an OAuth token

The operation issues an OAuth code which can be used in the OAuth code flow.


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
    "/v1/oauth/token": {
      "post": {
        "summary": "Issue an OAuth token",
        "tags": [
          "OAuth"
        ],
        "description": "The operation issues an OAuth code which can be used in the OAuth code flow.\n",
        "requestBody": {
          "required": true,
          "content": {
            "application/json": {
              "schema": {
                "title": "OAuthTokenRequest",
                "type": "object",
                "example": {
                  "client_id": "7a3c52a910e1dc2abbb14da2b6b8e711",
                  "client_secret": "bbb14da2b6b8e7117a3c52a910e1dc2a",
                  "redirect_uri": "http://localhost",
                  "scope": "general",
                  "account_id": "0d18ae51-3c94-4511-b209-101e1666416b"
                },
                "properties": {
                  "client_id": {
                    "type": "string",
                    "description": "OAuth client ID"
                  },
                  "client_secret": {
                    "type": "string",
                    "description": "OAuth client secret"
                  },
                  "redirect_uri": {
                    "type": "string",
                    "description": "redirect URI for the OAuth flow"
                  },
                  "scope": {
                    "type": "string",
                    "description": "scopes requested by the OAuth flow"
                  },
                  "account_id": {
                    "type": "string",
                    "format": "uuid",
                    "description": "end-user account ID"
                  }
                },
                "required": [
                  "client_id",
                  "client_secret",
                  "redirect_uri",
                  "scope",
                  "account_id"
                ],
                "description": "This model is used for both the Issue and Authorize OAuth token routes",
                "x-stoplight": {
                  "id": "a9yeydszevnuj"
                },
                "x-readme-ref-name": "OAuthTokenRequest"
              }
            }
          }
        },
        "responses": {
          "200": {
            "description": "Success.",
            "content": {
              "application/json": {
                "schema": {
                  "description": "",
                  "type": "object",
                  "x-examples": {
                    "example-1": {
                      "access_token": "87586f14-c3f4-4912-b107-f75bc17ff87a",
                      "token_type": "Bearer",
                      "scope": "general"
                    }
                  },
                  "properties": {
                    "access_token": {
                      "type": "string",
                      "description": "OAuth token"
                    },
                    "token_type": {
                      "type": "string",
                      "description": "Always `Bearer`",
                      "enum": [
                        "Bearer"
                      ],
                      "example": "Bearer"
                    },
                    "scope": {
                      "type": "string",
                      "description": "Token’s scope"
                    }
                  },
                  "required": [
                    "access_token",
                    "token_type",
                    "scope"
                  ],
                  "x-stoplight": {
                    "id": "7ljatwc79gihj"
                  },
                  "x-readme-ref-name": "IssueOAuthTokenResponse"
                },
                "examples": {
                  "example-1": {
                    "value": {
                      "access_token": "87586f14-c3f4-4912-b107-f75bc17ff87a",
                      "token_type": "Bearer",
                      "scope": "general"
                    }
                  }
                }
              }
            }
          },
          "401": {
            "description": "Client does not exist, you do not have access to the client, or “client_secret” is incorrect.\n",
            "content": {
              "application/json": {
                "schema": {
                  "type": "string"
                }
              }
            }
          },
          "422": {
            "description": "Redirect URI or scope is invalid.\n",
            "content": {
              "application/json": {
                "schema": {
                  "type": "string"
                }
              }
            }
          }
        },
        "operationId": "issueOAuthToken"
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
