---
source_view: https://docs.alpaca.markets/reference/deleteorderbyorderid-1
source_md: https://docs.alpaca.markets/reference/deleteorderbyorderid-1.md
scraped_at_utc: 2026-01-22T23:02:18Z
---
# Delete Order by ID

Attempts to cancel an Open Order. If the order is no longer cancelable, the request will be rejected with status 422; otherwise accepted with return status 204.

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
    "/v2/orders/{order_id}": {
      "delete": {
        "tags": [
          "Orders"
        ],
        "summary": "Delete Order by ID",
        "parameters": [],
        "responses": {
          "204": {
            "description": "No Content"
          },
          "422": {
            "description": "The order status is not cancelable."
          }
        },
        "operationId": "deleteOrderByOrderID",
        "description": "Attempts to cancel an Open Order. If the order is no longer cancelable, the request will be rejected with status 422; otherwise accepted with return status 204."
      },
      "parameters": [
        {
          "schema": {
            "type": "string",
            "format": "uuid"
          },
          "name": "order_id",
          "in": "path",
          "required": true,
          "description": "order id"
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
