---
source_view: https://docs.alpaca.markets/reference/deleteallorders-1
source_md: https://docs.alpaca.markets/reference/deleteallorders-1.md
scraped_at_utc: 2026-01-22T23:02:18Z
---
# Delete All Orders

Attempts to cancel all open orders. A response will be provided for each order that is attempted to be cancelled. If an order is no longer cancelable, the server will respond with status 500 and reject the request.

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
      "name": "Orders"
    }
  ],
  "paths": {
    "/v2/orders": {
      "delete": {
        "tags": [
          "Orders"
        ],
        "summary": "Delete All Orders",
        "parameters": [],
        "responses": {
          "207": {
            "description": "Multi-Status with body.\n\nan array of objects that include the order id and http status code for each status request.",
            "content": {
              "application/json": {
                "schema": {
                  "type": "array",
                  "items": {
                    "title": "CanceledOrderResponse",
                    "type": "object",
                    "x-examples": {
                      "example-1": {
                        "id": "d56ba3ea-6d04-48ce-8175-817e242ee608",
                        "status": 200
                      }
                    },
                    "description": "Represents the result of a request to cancel and order",
                    "properties": {
                      "id": {
                        "type": "string",
                        "format": "uuid",
                        "description": "orderId"
                      },
                      "status": {
                        "type": "integer",
                        "description": "http response code",
                        "example": 200
                      }
                    },
                    "x-readme-ref-name": "CanceledOrderResponse"
                  }
                }
              }
            }
          },
          "500": {
            "description": "Failed to cancel order."
          }
        },
        "operationId": "deleteAllOrders",
        "description": "Attempts to cancel all open orders. A response will be provided for each order that is attempted to be cancelled. If an order is no longer cancelable, the server will respond with status 500 and reject the request."
      }
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
