# Backend Tests

## 运行方式

在 `backend` 目录下运行：

```bash
../backend/.venv/bin/python -m pytest
```

测试默认会联网，并且会调用 Alpaca 历史数据与在线 LLM。

## 必需环境变量

测试启动时会进行 fail fast 校验（缺失直接失败）：

- `GOOGLE_API_KEY`
- `ALPACA_API_KEY`
- `ALPACA_SECRET_KEY`

环境变量通常放在 `backend/.env`，测试会自动加载。

## Timestamp LLM Backtest

数据文件：

- `tests/fixtures/llm_backtest_cases.json`

运行后会生成报告：

- `test_reports/llm_backtest_report.json`

### Case 格式

每个 case 是一个 JSON object：

- `id`: 唯一标识
- `symbol`: 例如 `SPY`
- `time_pst`: 例如 `2026-01-23 09:35`（America/Los_Angeles）
  - 或者使用 `current_time_utc_iso`: 例如 `2026-01-23T17:35:00Z`
- `mode`: `playback` 或 `realtime`（回测通常用 `playback`）
- `expect`: 断言条件

### expect DSL

当前支持：

- `{ "action_any": true }`
- `{ "action_is": "buy_long" }`
- `{ "action_not": "buy_long" }`
- `{ "action_in": ["ignore", "follow_up"] }`
- `{ "confidence_gte": 0.6 }`
- `{ "confidence_lte": 0.3 }`

## Option Chain Prompt 测试

`tests/test_options_service.py` 会在 `realtime` / `playback` 两种模式下触发一次 `AnalysisService.analyze_signal`，通过 stub 捕获发送给 LLM 的 user prompt，并断言 prompt 中包含 Option Chain 段落以及 Nearest Expiration 日期正确。

