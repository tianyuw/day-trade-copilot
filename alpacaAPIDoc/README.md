# Alpaca API Docs（项目内离线参考）

本目录用于存放 Alpaca 官方文档的离线快照，便于在项目内直接检索。

## Trading API

运行脚本会生成/刷新以下文件：

- `trading_openapi.yaml`：Trading API 的 OpenAPI 规范（若官方维护）
- `trading_api_reference_index.md`：从 OpenAPI 提取的端点索引（按 tag 分组，带 Reference 链接）
- `trading_api_overview.md`：Trading API Overview 页面文本快照
- `trading_api_reference_pages.md`：Reference 页面快照目录（operationId → 本地文件）
- `trading_reference/*.md`：抓取的 `docs.alpaca.markets/reference/{slug}.md`（ReadMe 导出 Markdown，含 OpenAPI JSON）

生成方式（使用后端虚拟环境）：

```bash
./backend/.venv/bin/python alpacaAPIDoc/scrape_trading_api.py
```

## Historical API（Market Data）

运行脚本会生成/刷新以下文件：

- `historical_api_reference/historical_openapi.yaml`：Market Data API 的 OpenAPI 规范（来自 `alpacahq/alpaca-docs`）
- `historical_api_reference/historical_openapi_reference_index.md`：从 OpenAPI 提取的端点索引（按 tag 分组，带 Reference 链接）
- `historical_api_reference/historical_api_overview.md`：Historical API Overview 页面文本快照
- `historical_api_reference/historical_api_docs_pages.md`：Historical API 文档子页面快照目录
- `historical_api_reference/historical_api_reference_pages.md`：Reference 页面快照目录（slug → 本地文件）
- `historical_api_reference/historical_api_reference_index.md`：从本地 Reference 快照提取的端点索引（优先反映当前 Reference 结构，带本地 Snapshot 链接）
- `historical_api_reference/reference/*.md`：抓取的 `docs.alpaca.markets/reference/{slug}.md`
- `historical_api_reference/docs/*.md`：抓取的 `docs.alpaca.markets/docs/*`（Historical API 相关）

生成方式（使用后端虚拟环境）：

```bash
./backend/.venv/bin/python alpacaAPIDoc/scrape_historical_api.py
```

## WebSocket Stream（Market Data）

运行脚本会生成/刷新以下文件：

- `websocket_stream_api_reference/websocket_stream_overview.md`：WebSocket Stream（Market Data）概览页文本快照（source: `/docs/streaming-market-data`）
- `websocket_stream_api_reference/websocket_stream_docs_pages.md`：相关文档页面快照目录
- `websocket_stream_api_reference/docs/*.md`：抓取的 `docs.alpaca.markets/docs/*`（stocks/crypto/options/news 的实时 stream 说明）

生成方式（使用后端虚拟环境）：

```bash
./backend/.venv/bin/python alpacaAPIDoc/scrape_websocket_stream_api.py
```
