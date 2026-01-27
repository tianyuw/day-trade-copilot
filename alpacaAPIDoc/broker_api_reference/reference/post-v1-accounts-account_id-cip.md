---
source_view: https://docs.alpaca.markets/reference/post-v1-accounts-account_id-cip
source_md: https://docs.alpaca.markets/reference/post-v1-accounts-account_id-cip.md
scraped_at_utc: 2026-01-27T04:30:48Z
---
# Upload CIP information

The customer identification program (CIP) API allows you to submit the CIP results received from your KYC provider.

The minimum requirements to open an individual financial account are delimited and you must verify the true identity of the account holder at account opening:

Name
Date of birth
Address
Identification number (for a U.S. citizen, a taxpayer identification number)

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
      "name": "KYC"
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
    "/v1/accounts/{account_id}/cip": {
      "parameters": [
        {
          "schema": {
            "type": "string"
          },
          "name": "account_id",
          "in": "path",
          "required": true
        }
      ],
      "post": {
        "summary": "Upload CIP information",
        "operationId": "post-v1-accounts-account_id-cip",
        "responses": {
          "200": {
            "description": "OK"
          }
        },
        "description": "The customer identification program (CIP) API allows you to submit the CIP results received from your KYC provider.\n\nThe minimum requirements to open an individual financial account are delimited and you must verify the true identity of the account holder at account opening:\n\nName\nDate of birth\nAddress\nIdentification number (for a U.S. citizen, a taxpayer identification number)",
        "requestBody": {
          "content": {
            "application/json": {
              "schema": {
                "title": "CIPInfo",
                "x-stoplight": {
                  "id": "nmcb0qvan724h"
                },
                "type": "object",
                "description": "Customer Identification Program (CIP) information for an account applicant.",
                "properties": {
                  "id": {
                    "type": "string",
                    "description": "ID of this CIPInfo",
                    "format": "uuid"
                  },
                  "account_id": {
                    "type": "string",
                    "x-stoplight": {
                      "id": "nti69y3rr1e79"
                    },
                    "format": "uuid",
                    "description": "UUID of the Account instance this CIPInfo is for"
                  },
                  "provider_name": {
                    "type": "array",
                    "x-stoplight": {
                      "id": "1e8bkk1u4yiew"
                    },
                    "description": "List of KYC providers this information came from",
                    "items": {
                      "title": "CIPProvider",
                      "x-stoplight": {
                        "id": "1ladh13ciiv0e"
                      },
                      "type": "string",
                      "description": "\"alloy\"   - ALLOY\n\"trulioo\" - TRULIOO\n\"onfido\"  - ONFIDO\n\"veriff\"  - VERIFF\n\"jumio\"   - JUMIO\n\"getmati\" - GETMATI",
                      "x-readme-ref-name": "CIPProvider"
                    }
                  },
                  "created_at": {
                    "type": "string",
                    "x-stoplight": {
                      "id": "64h0di2a6vyej"
                    },
                    "format": "date-time"
                  },
                  "updated_at": {
                    "type": "string",
                    "x-stoplight": {
                      "id": "suqeaf04rzb77"
                    },
                    "format": "date-time"
                  },
                  "kyc": {
                    "type": "object",
                    "x-examples": {
                      "Example 1": {
                        "id": "CBDAD1C4-1047-450E-BAE5-B6C406F509B4",
                        "risk_level": "LOW",
                        "applicant_name": "John Doe",
                        "email_address": "johndoe@example.com",
                        "nationality": "American",
                        "id_number": "jd0000123456789",
                        "date_of_birth": "1970-12-01",
                        "address": "42 Faux St",
                        "postal_code": "94401",
                        "country_of_residency": "USA",
                        "kyc_completed_at": "2021-06-10T15:37:03Z",
                        "ip_address": "127.0.0.1",
                        "check_initiated_at": "2021-06-10T15:37:03Z",
                        "check_completed_at": "2021-06-10T15:37:03Z",
                        "approval_status": "approved",
                        "approved_by": "Jane Doe",
                        "approved_at": "2021-06-10T15:38:03Z"
                      }
                    },
                    "description": "Represents Know Your Customer (KYC) info for a CIPInfo",
                    "properties": {
                      "id": {
                        "type": "string",
                        "description": "Your internal ID of check",
                        "format": "uuid"
                      },
                      "risk_score": {
                        "type": "integer",
                        "description": "Overall risk score returned by KYC provider or assessed",
                        "x-stoplight": {
                          "id": "90qw403hvrt4y"
                        }
                      },
                      "risk_level": {
                        "type": "string",
                        "description": "Overall risk level returned by KYC provider or assessed",
                        "x-stoplight": {
                          "id": "qlzreqji4lhci"
                        }
                      },
                      "risk_categories": {
                        "type": "array",
                        "description": "The list of risk categories returned by the KYC provider or assessed",
                        "x-stoplight": {
                          "id": "qlzreqji4lhci"
                        },
                        "items": {
                          "x-stoplight": {
                            "id": "me5f66krhts26"
                          },
                          "type": "string"
                        }
                      },
                      "applicant_name": {
                        "type": "string",
                        "description": "Given and family name of applicant"
                      },
                      "email_address": {
                        "type": "string",
                        "description": "email address of applicant"
                      },
                      "nationality": {
                        "type": "string",
                        "description": "nationality of applicant"
                      },
                      "date_of_birth": {
                        "type": "string",
                        "description": "DOB of applicant",
                        "format": "date"
                      },
                      "address": {
                        "type": "string",
                        "description": "Concatenated street address, city, state and country of applicant"
                      },
                      "postal_code": {
                        "type": "string",
                        "description": "postal code for `address` field"
                      },
                      "country_of_residency": {
                        "type": "string",
                        "description": "country for `address` field"
                      },
                      "kyc_completed_at": {
                        "type": "string",
                        "description": "Datetime that KYC check was completed at",
                        "format": "date-time"
                      },
                      "ip_address": {
                        "type": "string",
                        "description": "IP address of applicant at time of KYC check"
                      },
                      "check_initiated_at": {
                        "type": "string",
                        "description": "start datetime of KYC check",
                        "format": "date-time"
                      },
                      "check_completed_at": {
                        "type": "string",
                        "description": "completion datetime of KYC check",
                        "format": "date-time"
                      },
                      "approval_status": {
                        "type": "string",
                        "enum": [
                          "approved",
                          "rejected"
                        ],
                        "description": "Approval status of KYC check",
                        "example": "approved"
                      },
                      "approved_by": {
                        "type": "string",
                        "description": "Identifier of who approved KYC check"
                      },
                      "approved_at": {
                        "type": "string",
                        "description": "Reason for approving this KYC check",
                        "format": "date-time"
                      },
                      "approved_reason": {
                        "type": "string",
                        "x-stoplight": {
                          "id": "rw7ke3e65x6xk"
                        },
                        "description": "Datetime that this KYC check was approved"
                      }
                    },
                    "required": [
                      "id"
                    ],
                    "title": "CIPKYCInfo",
                    "x-stoplight": {
                      "id": "1ygvfp2y5nwev"
                    },
                    "x-readme-ref-name": "CIPKYC"
                  },
                  "document": {
                    "type": "object",
                    "x-examples": {
                      "Example 1": {
                        "id": "55B9931A-3BE6-4BC0-9BDD-0B954E4A4632",
                        "result": "clear",
                        "status": "complete",
                        "created_at": "2021-06-10T15:37:03Z",
                        "image_integrity": "clear"
                      }
                    },
                    "properties": {
                      "id": {
                        "type": "string",
                        "description": "Your internal ID of check"
                      },
                      "result": {
                        "title": "CIPResult",
                        "x-stoplight": {
                          "id": "4mte2vkxwqcmd"
                        },
                        "type": "string",
                        "description": "The result of the check. Either `clear` or `consider`.",
                        "x-readme-ref-name": "CIPResult"
                      },
                      "status": {
                        "title": "CIPStatus",
                        "x-stoplight": {
                          "id": "ejcunr8l8s0f2"
                        },
                        "type": "string",
                        "description": "An enum representing the status of the CIPInfo\n\n\"complete\"\n\n\"withdrawn\"",
                        "x-readme-ref-name": "CIPStatus"
                      },
                      "created_at": {
                        "type": "string",
                        "format": "date-time",
                        "description": "Datetime for when this check was done"
                      },
                      "date_of_birth": {
                        "type": "string",
                        "format": "date",
                        "description": "Datetime for when this check was done",
                        "x-stoplight": {
                          "id": "mldoed43bulx0"
                        }
                      },
                      "date_of_expiry": {
                        "type": "string",
                        "format": "date",
                        "description": "Datetime for when this check was done",
                        "x-stoplight": {
                          "id": "zgpwb045porqt"
                        }
                      },
                      "document_numbers": {
                        "type": "array",
                        "x-stoplight": {
                          "id": "ylxi39biyo436"
                        },
                        "description": "Number of the document that was checked",
                        "items": {
                          "x-stoplight": {
                            "id": "n986txzgf0lnx"
                          },
                          "type": "string"
                        }
                      },
                      "document_type": {
                        "type": "string",
                        "x-stoplight": {
                          "id": "n8sxd8t9f3kzq"
                        },
                        "description": "Type of the document that was checked"
                      },
                      "first_name": {
                        "type": "string",
                        "x-stoplight": {
                          "id": "w2punywp6uw0v"
                        },
                        "description": "First name extracted from the document"
                      },
                      "last_name": {
                        "type": "string",
                        "x-stoplight": {
                          "id": "2nutmuuiwgyib"
                        },
                        "description": "Last name extracted from the document"
                      },
                      "gender": {
                        "type": "string",
                        "x-stoplight": {
                          "id": "23ze35btn7pgd"
                        },
                        "description": "Gender info extracted from the document"
                      },
                      "issuing_country": {
                        "type": "string",
                        "x-stoplight": {
                          "id": "0kb0a69x5g5m6"
                        },
                        "description": "Country for which issued the document"
                      },
                      "nationality": {
                        "type": "string",
                        "x-stoplight": {
                          "id": "l39n0f7u9rg3g"
                        },
                        "description": "Nationality extracted from the document"
                      },
                      "age_validation": {
                        "title": "CIPResult",
                        "x-stoplight": {
                          "id": "4mte2vkxwqcmd"
                        },
                        "type": "string",
                        "description": "The result of the check. Either `clear` or `consider`.",
                        "x-readme-ref-name": "CIPResult"
                      },
                      "comprised_document": {
                        "title": "CIPResult",
                        "x-stoplight": {
                          "id": "4mte2vkxwqcmd"
                        },
                        "type": "string",
                        "description": "The result of the check. Either `clear` or `consider`.",
                        "x-readme-ref-name": "CIPResult"
                      },
                      "police_record": {
                        "title": "CIPStatus",
                        "x-stoplight": {
                          "id": "ejcunr8l8s0f2"
                        },
                        "type": "string",
                        "description": "An enum representing the status of the CIPInfo\n\n\"complete\"\n\n\"withdrawn\"",
                        "x-readme-ref-name": "CIPStatus"
                      },
                      "data_comparison": {
                        "title": "CIPResult",
                        "x-stoplight": {
                          "id": "4mte2vkxwqcmd"
                        },
                        "type": "string",
                        "description": "The result of the check. Either `clear` or `consider`.",
                        "x-readme-ref-name": "CIPResult"
                      },
                      "data_comparison_breakdown": {
                        "type": "string",
                        "x-stoplight": {
                          "id": "j5c0hr492lzlv"
                        },
                        "description": "json object representing the results of the various sub-checks\n          done when calculating the result on `data_comparison`. Example: {“date_of_birth”: “clear”,\n          “date_of_expiry”: “clear” “document_numbers”: “clear”, “document_type”: “clear”, “first_name”: “clear”,\n          “gender”: “clear”, “issuing_country”: “clear”, “last_name”: “clear”}"
                      },
                      "image_integrity": {
                        "title": "CIPResult",
                        "x-stoplight": {
                          "id": "4mte2vkxwqcmd"
                        },
                        "type": "string",
                        "description": "The result of the check. Either `clear` or `consider`.",
                        "x-readme-ref-name": "CIPResult"
                      },
                      "image_integrity_breakdown": {
                        "type": "string",
                        "x-stoplight": {
                          "id": "gw6cht7g7zui2"
                        },
                        "description": "json object representing the results of the various sub-checks done\n          when calculating the result on `image_integrity`. Example: example: {“colour_picture”: “clear”,\n          “conclusive_document_quality”: “clear”, “image_quality”: “clear”, “supported_document”: “clear”}"
                      },
                      "visual_authenticity": {
                        "type": "string",
                        "x-stoplight": {
                          "id": "ccsft0oc0p7y7"
                        },
                        "description": "json object representing the the various sub-checks done when determening\n          whether visual (non-textual) elements are correct given the document type. Example: {\n          “digital_tampering”: “clear”, “face_detection”: “clear”, “fonts”: “clear”, “original_document_present”:\n          “clear”, “picture_face_integrity”: “clear”, “security_features”: “clear”, “template”: “clear”}"
                      }
                    },
                    "required": [
                      "id"
                    ],
                    "description": "Represents results of checking a document for CIPInfo\n",
                    "x-stoplight": {
                      "id": "7pizeb1ps42ij"
                    },
                    "x-readme-ref-name": "CIPDocument"
                  },
                  "photo": {
                    "type": "object",
                    "x-examples": {
                      "Example 1": {
                        "id": "0DD13020-F0FD-4B5A-B58F-BC1885E90A6D",
                        "result": "clear",
                        "status": "complete",
                        "created_at": "2021-06-10T15:37:03Z",
                        "face_comparison": "clear"
                      }
                    },
                    "properties": {
                      "id": {
                        "type": "string",
                        "description": "Your internal ID of the check"
                      },
                      "result": {
                        "title": "CIPResult",
                        "x-stoplight": {
                          "id": "4mte2vkxwqcmd"
                        },
                        "type": "string",
                        "description": "The result of the check. Either `clear` or `consider`.",
                        "x-readme-ref-name": "CIPResult"
                      },
                      "status": {
                        "type": "string",
                        "enum": [
                          "complete",
                          "withdrawn"
                        ],
                        "description": "Overall status of the check. Either `complete` or `withdrawn`."
                      },
                      "created_at": {
                        "type": "string",
                        "description": "datetime of when the check happened"
                      },
                      "face_comparison": {
                        "title": "CIPResult",
                        "x-stoplight": {
                          "id": "4mte2vkxwqcmd"
                        },
                        "type": "string",
                        "description": "The result of the check. Either `clear` or `consider`.",
                        "x-readme-ref-name": "CIPResult"
                      },
                      "face_comparison_breakdown": {
                        "type": "string",
                        "x-stoplight": {
                          "id": "nva7tm8q3itop"
                        },
                        "description": "a json object representing the breakdown of sub-checks done in\n          `face_comparison`. Example: {“face_match”:{“result”: “clear”,“properties”:{“score”: “80”}}}"
                      },
                      "image_integrity": {
                        "title": "CIPResult",
                        "x-stoplight": {
                          "id": "4mte2vkxwqcmd"
                        },
                        "type": "string",
                        "description": "The result of the check. Either `clear` or `consider`.",
                        "x-readme-ref-name": "CIPResult"
                      },
                      "image_integrity_breakdown": {
                        "type": "string",
                        "x-stoplight": {
                          "id": "lltcpsijc1bwo"
                        },
                        "description": "a json object representing the breakdown of sub-checks done in\n          `image_integrity`. Example  {“face_detected”:{“result”: “clear”},“source_integrity”: {“result”: “clear”}}"
                      },
                      "visual_authenticity": {
                        "title": "CIPResult",
                        "x-stoplight": {
                          "id": "4mte2vkxwqcmd"
                        },
                        "type": "string",
                        "description": "The result of the check. Either `clear` or `consider`.",
                        "x-readme-ref-name": "CIPResult"
                      },
                      "visual_authenticity_breakdown": {
                        "type": "string",
                        "x-stoplight": {
                          "id": "0712bbbrw15oo"
                        },
                        "description": "a json object representing the breakdown of sub-checks don in\n          `visual_authenticity`. Example {“spoofing_detection”: {“result”: “clear”,“properties”: {“score”: “26”}}}}"
                      }
                    },
                    "required": [
                      "id"
                    ],
                    "description": "Represents the results of checking a Photo for CIPInfo",
                    "x-stoplight": {
                      "id": "hqx4vrzqypp7h"
                    },
                    "x-readme-ref-name": "CIPPhoto"
                  },
                  "identity": {
                    "type": "object",
                    "x-examples": {
                      "Example 1": {
                        "id": "28E1CCE8-1B1A-4472-9AD4-C6C5B7C3A6AF",
                        "result": "clear",
                        "status": "complete",
                        "created_at": "2021-06-10T15:37:03Z",
                        "sources": "clear",
                        "address": "clear",
                        "date_of_birth": "clear"
                      }
                    },
                    "properties": {
                      "id": {
                        "type": "string",
                        "description": "Your internal ID of check"
                      },
                      "result": {
                        "title": "CIPResult",
                        "x-stoplight": {
                          "id": "4mte2vkxwqcmd"
                        },
                        "type": "string",
                        "description": "The result of the check. Either `clear` or `consider`.",
                        "x-readme-ref-name": "CIPResult"
                      },
                      "status": {
                        "title": "CIPStatus",
                        "x-stoplight": {
                          "id": "ejcunr8l8s0f2"
                        },
                        "type": "string",
                        "description": "An enum representing the status of the CIPInfo\n\n\"complete\"\n\n\"withdrawn\"",
                        "x-readme-ref-name": "CIPStatus"
                      },
                      "created_at": {
                        "type": "string",
                        "description": "datetime when identity check happened"
                      },
                      "matched_address": {
                        "title": "CIPResult",
                        "x-stoplight": {
                          "id": "4mte2vkxwqcmd"
                        },
                        "type": "string",
                        "description": "The result of the check. Either `clear` or `consider`.",
                        "x-readme-ref-name": "CIPResult"
                      },
                      "matched_addresses": {
                        "type": "string",
                        "description": "datetime when identity check happened",
                        "x-stoplight": {
                          "id": "1vqeq6vfihjs2"
                        }
                      },
                      "sources": {
                        "title": "CIPResult",
                        "x-stoplight": {
                          "id": "4mte2vkxwqcmd"
                        },
                        "type": "string",
                        "description": "The result of the check. Either `clear` or `consider`.",
                        "x-readme-ref-name": "CIPResult"
                      },
                      "sources_breakdown": {
                        "type": "string",
                        "description": "a json object representing the breakdown of `sources` field. For example:\n          {“total_sources”: {“result”: “clear”,“properties”: {“total_number_of_sources”: “3”}}}",
                        "x-stoplight": {
                          "id": "4aehkpo8da5mr"
                        }
                      },
                      "address": {
                        "title": "CIPResult",
                        "x-stoplight": {
                          "id": "4mte2vkxwqcmd"
                        },
                        "type": "string",
                        "description": "The result of the check. Either `clear` or `consider`.",
                        "x-readme-ref-name": "CIPResult"
                      },
                      "address_breakdown": {
                        "type": "string",
                        "x-stoplight": {
                          "id": "wcctczes53ivy"
                        },
                        "description": "a json object representing the breakdown of the `address` field. For example:\n          {“credit_agencies”: {“result”: “clear”,“properties”:{“number_of_matches”:“1”}}"
                      },
                      "date_of_birth": {
                        "title": "CIPResult",
                        "x-stoplight": {
                          "id": "4mte2vkxwqcmd"
                        },
                        "type": "string",
                        "description": "The result of the check. Either `clear` or `consider`.",
                        "x-readme-ref-name": "CIPResult"
                      },
                      "date_of_birth_breakdown": {
                        "type": "string",
                        "x-stoplight": {
                          "id": "efhx1bwabsdty"
                        },
                        "description": "a json object representing the breakdown of the `date_of_birth` field.\n          For example: example: {“credit_agencies”:{“result”: “clear”,“properties”: {“number_of_matches”: “1”}}"
                      },
                      "tax_id": {
                        "title": "CIPResult",
                        "x-stoplight": {
                          "id": "4mte2vkxwqcmd"
                        },
                        "type": "string",
                        "description": "The result of the check. Either `clear` or `consider`.",
                        "x-readme-ref-name": "CIPResult"
                      },
                      "tax_id_breakdown": {
                        "type": "string",
                        "x-stoplight": {
                          "id": "x5c64geol7p1s"
                        },
                        "description": "a json object representing the breakdown of the `tax_id` field"
                      }
                    },
                    "required": [
                      "id"
                    ],
                    "x-stoplight": {
                      "id": "g8qjr3c8h1npx"
                    },
                    "x-readme-ref-name": "CIPIdentity"
                  },
                  "watchlist": {
                    "type": "object",
                    "x-examples": {
                      "Example 1": {
                        "id": "7572B870-EB4C-46A2-8B88-509194CCEE7E",
                        "result": "clear",
                        "status": "complete",
                        "created_at": "2021-06-10T15:37:03Z",
                        "politically_exposed_person": "clear",
                        "sanction": "clear",
                        "adverse_media": "clear",
                        "monitored_lists": "clear"
                      }
                    },
                    "description": "Represents the result of checking to see if the applicant is in any watchlists for a CIPInfo",
                    "properties": {
                      "id": {
                        "type": "string",
                        "description": "Your internal ID of check"
                      },
                      "result": {
                        "title": "CIPResult",
                        "x-stoplight": {
                          "id": "4mte2vkxwqcmd"
                        },
                        "type": "string",
                        "description": "The result of the check. Either `clear` or `consider`.",
                        "x-readme-ref-name": "CIPResult"
                      },
                      "status": {
                        "title": "CIPStatus",
                        "x-stoplight": {
                          "id": "ejcunr8l8s0f2"
                        },
                        "type": "string",
                        "description": "An enum representing the status of the CIPInfo\n\n\"complete\"\n\n\"withdrawn\"",
                        "x-readme-ref-name": "CIPStatus"
                      },
                      "created_at": {
                        "type": "string",
                        "description": "datetime when check happened"
                      },
                      "records": {
                        "type": "string",
                        "x-stoplight": {
                          "id": "0jk1ut5oct0ml"
                        },
                        "description": "a json object. Example [{“text”: “Record info”}]"
                      },
                      "politically_exposed_person": {
                        "title": "CIPResult",
                        "x-stoplight": {
                          "id": "4mte2vkxwqcmd"
                        },
                        "type": "string",
                        "description": "The result of the check. Either `clear` or `consider`.",
                        "x-readme-ref-name": "CIPResult"
                      },
                      "adverse_media": {
                        "title": "CIPResult",
                        "x-stoplight": {
                          "id": "4mte2vkxwqcmd"
                        },
                        "type": "string",
                        "description": "The result of the check. Either `clear` or `consider`.",
                        "x-readme-ref-name": "CIPResult"
                      },
                      "sanction": {
                        "title": "CIPResult",
                        "x-stoplight": {
                          "id": "4mte2vkxwqcmd"
                        },
                        "type": "string",
                        "description": "The result of the check. Either `clear` or `consider`.",
                        "x-readme-ref-name": "CIPResult"
                      },
                      "monitored_lists": {
                        "title": "CIPResult",
                        "x-stoplight": {
                          "id": "4mte2vkxwqcmd"
                        },
                        "type": "string",
                        "description": "The result of the check. Either `clear` or `consider`.",
                        "x-readme-ref-name": "CIPResult"
                      }
                    },
                    "required": [
                      "id"
                    ],
                    "x-stoplight": {
                      "id": "b6tmg9qshk4f9"
                    },
                    "x-readme-ref-name": "CIPWatchlist"
                  }
                },
                "x-readme-ref-name": "CIPInfo"
              }
            }
          }
        },
        "tags": [
          "KYC"
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
