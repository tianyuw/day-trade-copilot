# Alpaca Trading API Reference（索引）

此文件由 `alpacaAPIDoc/trading_openapi.yaml` 自动提取生成，便于快速查找每个 REST 端点。

## Account Activities

| Method | Path | Summary | Reference |
|---|---|---|---|
| GET | /v2/account/activities | Get account activities of one type | [getAccountActivities](https://docs.alpaca.markets/reference/getAccountActivities) |
| GET | /v2/account/activities/{activity_type} | Get account activities of one type | [getAccountActivitiesByActivityType](https://docs.alpaca.markets/reference/getAccountActivitiesByActivityType) |

## Account Configurations

| Method | Path | Summary | Reference |
|---|---|---|---|
| GET | /v2/account/configurations | Account Configurations | [getAccountConfig](https://docs.alpaca.markets/reference/getAccountConfig) |
| PATCH | /v2/account/configurations | Account Configurations | [patchAccountConfig](https://docs.alpaca.markets/reference/patchAccountConfig) |

## Accounts

| Method | Path | Summary | Reference |
|---|---|---|---|
| GET | /v2/account | Get account | [getAccount](https://docs.alpaca.markets/reference/getAccount) |

## Calendar

| Method | Path | Summary | Reference |
|---|---|---|---|
| GET | /v2/calendar | Get Market Calendar info | [getCalendar](https://docs.alpaca.markets/reference/getCalendar) |

## Clock

| Method | Path | Summary | Reference |
|---|---|---|---|
| GET | /v2/clock | Get Market Clock info | [getClock](https://docs.alpaca.markets/reference/getClock) |

## Orders

| Method | Path | Summary | Reference |
|---|---|---|---|
| DELETE | /v2/orders | All Orders | [deleteAllOrders](https://docs.alpaca.markets/reference/deleteAllOrders) |
| GET | /v2/orders | All Orders | [getAllOrders](https://docs.alpaca.markets/reference/getAllOrders) |
| POST | /v2/orders | Order | [postOrder](https://docs.alpaca.markets/reference/postOrder) |
| DELETE | /v2/orders/{order_id} | Order by Order ID | [deleteOrderByOrderID](https://docs.alpaca.markets/reference/deleteOrderByOrderID) |
| GET | /v2/orders/{order_id} | Order by Order ID | [getOrderByOrderID](https://docs.alpaca.markets/reference/getOrderByOrderID) |
| PATCH | /v2/orders/{order_id} | Order | [patchOrderByOrderId](https://docs.alpaca.markets/reference/patchOrderByOrderId) |

## Portfolio History

| Method | Path | Summary | Reference |
|---|---|---|---|
| GET | /v2/account/portfolio/history | Account Portfolio History | [getAccountPortfolioHistory](https://docs.alpaca.markets/reference/getAccountPortfolioHistory) |

## Positions

| Method | Path | Summary | Reference |
|---|---|---|---|
| DELETE | /v2/positions | All Positions | [deleteAllOpenPositions](https://docs.alpaca.markets/reference/deleteAllOpenPositions) |
| GET | /v2/positions | All Open Positions | [getAllOpenPositions](https://docs.alpaca.markets/reference/getAllOpenPositions) |
| DELETE | /v2/positions/{symbol_or_asset_id} | Position | [deleteOpenPosition](https://docs.alpaca.markets/reference/deleteOpenPosition) |
| GET | /v2/positions/{symbol_or_asset_id} | Open Position | [getOpenPosition](https://docs.alpaca.markets/reference/getOpenPosition) |

## Watchlists

| Method | Path | Summary | Reference |
|---|---|---|---|
| GET | /v2/watchlists | Watchlists | [getWatchlists](https://docs.alpaca.markets/reference/getWatchlists) |
| POST | /v2/watchlists | Watchlist | [postWatchlist](https://docs.alpaca.markets/reference/postWatchlist) |
| DELETE | /v2/watchlists/{watchlist_id} | Delete Watchlist By Id | [deleteWatchlistById](https://docs.alpaca.markets/reference/deleteWatchlistById) |
| GET | /v2/watchlists/{watchlist_id} | Get Watchlist by ID | [getWatchlistById](https://docs.alpaca.markets/reference/getWatchlistById) |
| POST | /v2/watchlists/{watchlist_id} | Add Asset to Watchlist | [addAssetToWatchlist](https://docs.alpaca.markets/reference/addAssetToWatchlist) |
| PUT | /v2/watchlists/{watchlist_id} | Update Watchlist By Id | [updateWatchlistById](https://docs.alpaca.markets/reference/updateWatchlistById) |
| DELETE | /v2/watchlists/{watchlist_id}/{symbol} | Symbol from Watchlist | [removeAssetFromWatchlist](https://docs.alpaca.markets/reference/removeAssetFromWatchlist) |
| DELETE | /v2/watchlists:by_name | Delete Watchlist By Name | [deleteWatchlistByName](https://docs.alpaca.markets/reference/deleteWatchlistByName) |
| GET | /v2/watchlists:by_name | Get Watchlist by Name | [getWatchlistByName](https://docs.alpaca.markets/reference/getWatchlistByName) |
| POST | /v2/watchlists:by_name | Add Asset to Watchlist By Name | [addAssetToWatchlistByName](https://docs.alpaca.markets/reference/addAssetToWatchlistByName) |
| PUT | /v2/watchlists:by_name | Update Watchlist By Name | [updateWatchlistByName](https://docs.alpaca.markets/reference/updateWatchlistByName) |
