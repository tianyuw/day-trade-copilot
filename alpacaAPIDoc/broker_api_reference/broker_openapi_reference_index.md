# Alpaca Broker API Reference（OpenAPI 索引）

此文件由 `broker_openapi.yaml` 自动提取生成，便于快速查找每个 REST 端点。

## Accounts

| Method | Path | Summary | Reference |
|---|---|---|---|
| GET | /v1/accounts | Get all accounts | [getAllAccounts](https://docs.alpaca.markets/reference/getAllAccounts) |
| POST | /v1/accounts | Create an account | [createAccount](https://docs.alpaca.markets/reference/createAccount) |
| GET | /v1/accounts/activities | Retrieve account activities | [getAccountActivities](https://docs.alpaca.markets/reference/getAccountActivities) |
| GET | /v1/accounts/activities/{activity_type} | Retrieve specific account activities | [getAccountActivitiesByType](https://docs.alpaca.markets/reference/getAccountActivitiesByType) |
| DELETE | /v1/accounts/{account_id} | Request to close an account | [deleteAccount](https://docs.alpaca.markets/reference/deleteAccount) |
| GET | /v1/accounts/{account_id} | Get an account by Id. | [getAccount](https://docs.alpaca.markets/reference/getAccount) |
| PATCH | /v1/accounts/{account_id} | Update an account | [patchAccount](https://docs.alpaca.markets/reference/patchAccount) |
| GET | /v1/accounts/{account_id}/ach_relationships | Retrieve ACH Relationships for an account | [getAccountACHRelationships](https://docs.alpaca.markets/reference/getAccountACHRelationships) |
| POST | /v1/accounts/{account_id}/ach_relationships | Create an ACH Relationship | [createACHRelationshipForAccount](https://docs.alpaca.markets/reference/createACHRelationshipForAccount) |
| DELETE | /v1/accounts/{account_id}/ach_relationships/{ach_relationship_id} | Delete an existing ACH relationship | [deleteACHRelationshipFromAccount](https://docs.alpaca.markets/reference/deleteACHRelationshipFromAccount) |
| POST | /v1/accounts/{account_id}/documents/upload | Upload a document to an already existing account | [uploadDocToAccount](https://docs.alpaca.markets/reference/uploadDocToAccount) |
| DELETE | /v1/accounts/{account_id}/recipient_banks/{bank_id} | Delete a Bank Relationship for an account | [deleteRecipientBank](https://docs.alpaca.markets/reference/deleteRecipientBank) |
| DELETE | /v1/accounts/{account_id}/transfers/{transfer_id} | Request to close a transfer | [deleteTransfer](https://docs.alpaca.markets/reference/deleteTransfer) |
| GET | /v1/events/accounts/status | Subscribe to account status events (SSE). | [suscribeToAccountStatusSSE](https://docs.alpaca.markets/reference/suscribeToAccountStatusSSE) |
| GET | /v1/trading/accounts/{account_id}/account | Retrieve trading details for an account. | [getTradingAccount](https://docs.alpaca.markets/reference/getTradingAccount) |

## Assets

| Method | Path | Summary | Reference |
|---|---|---|---|
| GET | /v1/assets | Retrieve all assets | [getAssets](https://docs.alpaca.markets/reference/getAssets) |
| GET | /v1/assets/{symbol_or_asset_id} | Retrieve an asset by UUID | [getAssetBySymbolOrId](https://docs.alpaca.markets/reference/getAssetBySymbolOrId) |

## Calendar

| Method | Path | Summary | Reference |
|---|---|---|---|
| GET | /v1/calendar | Query market calendar | [queryMarketCalendar](https://docs.alpaca.markets/reference/queryMarketCalendar) |

## Clock

| Method | Path | Summary | Reference |
|---|---|---|---|
| GET | /v1/clock | Query market clock | [queryMarketClock](https://docs.alpaca.markets/reference/queryMarketClock) |

## Corporate Actions

| Method | Path | Summary | Reference |
|---|---|---|---|
| GET | /v1/corporate_actions/announcements | Retrieving Announcements | [getCorporateAnnouncements](https://docs.alpaca.markets/reference/getCorporateAnnouncements) |

## Documents

| Method | Path | Summary | Reference |
|---|---|---|---|
| GET | /v1/accounts/{account_id}/documents | Return a list of account documents. | [getDocsForAccount](https://docs.alpaca.markets/reference/getDocsForAccount) |
| GET | /v1/accounts/{account_id}/documents/{document_id}/download | Download a document file that belongs to an account. | [downloadDocFromAccount](https://docs.alpaca.markets/reference/downloadDocFromAccount) |
| GET | /v1/documents/{document_id} | Download a document file directly | [downloadDocumentById](https://docs.alpaca.markets/reference/downloadDocumentById) |

## Events

| Method | Path | Summary | Reference |
|---|---|---|---|
| GET | /v1/events/trades | Subscribe to Trade Events (SSE) | [subscribeToTradeSSE](https://docs.alpaca.markets/reference/subscribeToTradeSSE) |
| GET | /v1/events/transfers/status | Subscribe to Transfer Events (SSE) | [subscribeToTransferStatusSSE](https://docs.alpaca.markets/reference/subscribeToTransferStatusSSE) |

## Funding

| Method | Path | Summary | Reference |
|---|---|---|---|
| GET | /v1/accounts/{account_id}/recipient_banks | Retrieve bank relationships for an account | [getRecipientBanks](https://docs.alpaca.markets/reference/getRecipientBanks) |
| POST | /v1/accounts/{account_id}/recipient_banks | Create a Bank Relationship for an account | [createRecipientBank](https://docs.alpaca.markets/reference/createRecipientBank) |
| GET | /v1/accounts/{account_id}/transfers | Return a list of transfers for an account. | [getTransfersForAccount](https://docs.alpaca.markets/reference/getTransfersForAccount) |
| POST | /v1/accounts/{account_id}/transfers | Request a new transfer | [createTransferForAccount](https://docs.alpaca.markets/reference/createTransferForAccount) |

## Journals

| Method | Path | Summary | Reference |
|---|---|---|---|
| GET | /v1/events/journals/status | Subscribe to journal events (SSE). | [subscribeToJournalStatusSSE](https://docs.alpaca.markets/reference/subscribeToJournalStatusSSE) |
| GET | /v1/journals | Return a list of requested journals. | [getAllJournals](https://docs.alpaca.markets/reference/getAllJournals) |
| POST | /v1/journals | Create a Journal. | [createJournal](https://docs.alpaca.markets/reference/createJournal) |
| POST | /v1/journals/batch | Create a Batch Journal Transaction (One-to-Many) | [createBatchJournal](https://docs.alpaca.markets/reference/createBatchJournal) |
| DELETE | /v1/journals/{journal_id} | Cancel a pending journal. | [deleteJournalById](https://docs.alpaca.markets/reference/deleteJournalById) |

## OAuth

| Method | Path | Summary | Reference |
|---|---|---|---|
| POST | /v1/oauth/authorize | Authorize an OAuth Token | [authorizeOAuthToken](https://docs.alpaca.markets/reference/authorizeOAuthToken) |
| GET | /v1/oauth/clients/{client_id} | Get an OAuth client | [getOAuthClient](https://docs.alpaca.markets/reference/getOAuthClient) |
| POST | /v1/oauth/token | Issue an OAuth token. | [issueOAuthToken](https://docs.alpaca.markets/reference/issueOAuthToken) |

## Trading

| Method | Path | Summary | Reference |
|---|---|---|---|
| DELETE | /v1/trading/accounts/{account_id}/orders | Attempts to cancel all open orders. A response will be provided for each order that is attempted to be cancelled. | [deleteAllOrdersForAccount](https://docs.alpaca.markets/reference/deleteAllOrdersForAccount) |
| GET | /v1/trading/accounts/{account_id}/orders | Retrieves a list of orders for the account, filtered by the supplied query parameters. | [getAllOrdersForAccount](https://docs.alpaca.markets/reference/getAllOrdersForAccount) |
| POST | /v1/trading/accounts/{account_id}/orders | Create an order for an account. | [createOrderForAccount](https://docs.alpaca.markets/reference/createOrderForAccount) |
| DELETE | /v1/trading/accounts/{account_id}/orders/{order_id} | Attempts to cancel an open order. | [deleteOrderForAccount](https://docs.alpaca.markets/reference/deleteOrderForAccount) |
| GET | /v1/trading/accounts/{account_id}/orders/{order_id} | Retrieves a single order for the given order_id. | [getOrderForAccount](https://docs.alpaca.markets/reference/getOrderForAccount) |
| PATCH | /v1/trading/accounts/{account_id}/orders/{order_id} | Replaces a single order with updated parameters | [replaceOrderForAccount](https://docs.alpaca.markets/reference/replaceOrderForAccount) |
| DELETE | /v1/trading/accounts/{account_id}/positions | Close All Positions for an Account | [closeAllPositionsForAccount](https://docs.alpaca.markets/reference/closeAllPositionsForAccount) |
| GET | /v1/trading/accounts/{account_id}/positions | List open positions for an account | [getPositionsForAccount](https://docs.alpaca.markets/reference/getPositionsForAccount) |
| DELETE | /v1/trading/accounts/{account_id}/positions/{symbol_or_asset_id} | Close a Position for an Account | [closePositionForAccountBySymbol](https://docs.alpaca.markets/reference/closePositionForAccountBySymbol) |
| GET | /v1/trading/accounts/{account_id}/positions/{symbol_or_asset_id} | Get an Open Position for account by Symbol or AssetId | [getPositionsForAccountBySymbol](https://docs.alpaca.markets/reference/getPositionsForAccountBySymbol) |

## Watchlist

| Method | Path | Summary | Reference |
|---|---|---|---|
| DELETE | /v1/accounts/{account_id}/watchlists/{watchlist_id} | Remove a watchlist | [deleteWatchlistFromAccountById](https://docs.alpaca.markets/reference/deleteWatchlistFromAccountById) |
| GET | /v1/accounts/{account_id}/watchlists/{watchlist_id} | Manage watchlists | [getWatchlistForAccountById](https://docs.alpaca.markets/reference/getWatchlistForAccountById) |
| PUT | /v1/accounts/{account_id}/watchlists/{watchlist_id} | Update an existing watchlist | [replaceWatchlistForAccountById](https://docs.alpaca.markets/reference/replaceWatchlistForAccountById) |
| GET | /v1/trading/accounts/{account_id}/watchlists | Retrieve all watchlists | [getAllWatchlistsForAccount](https://docs.alpaca.markets/reference/getAllWatchlistsForAccount) |
| POST | /v1/trading/accounts/{account_id}/watchlists | Create a new watchlist | [createWatchlistForAccount](https://docs.alpaca.markets/reference/createWatchlistForAccount) |
