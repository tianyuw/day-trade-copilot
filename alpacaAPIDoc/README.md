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
