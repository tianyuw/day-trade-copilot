# Proposal: 用 trades.db 持久化 AI 结果与持仓状态（解决 tracking/detail 状态丢失）

## 背景与现状

当前系统已经有一个 SQLite 数据库 `trades.db`（由后端 `Ledger` 管理），但 UI 上的关键状态仍主要依赖 **后端内存** 与 **WebSocket 生命周期**：

- tracking 列表页的 `IN_POSITION` 置顶/高亮依赖 `/ws/realtime` 推送的 `state` 消息；而 `state` 又来自后端每个 symbol 的内存 `SymbolSession`。页面切换导致 WS 重连时，session 重新初始化，高亮会丢失。
- detail 页右侧 AI output 依赖 `/api/ai/history/{symbol}`；当前实现是进程内存里的 `analysis_history`/`position_history`，服务重启或 WS 没写入历史时，历史消息无法恢复。

相关代码参考：
- `SymbolSession`/状态机： [trade_session.py](file:///Users/tianyuwang/Projects/day-trade-copilot/backend/app/trade_session.py)
- 现有 SQLite ledger： [ledger.py](file:///Users/tianyuwang/Projects/day-trade-copilot/backend/app/ledger.py)
- tracking/list WebSocket 与 session 初始化： [main.py](file:///Users/tianyuwang/Projects/day-trade-copilot/backend/app/main.py#L663-L990)
- `/api/ai/history/{symbol}` 当前返回内存： [main.py](file:///Users/tianyuwang/Projects/day-trade-copilot/backend/app/main.py#L289-L299)
- 前端 tracking/detail 消费 state/history： [tracking page.tsx](file:///Users/tianyuwang/Projects/day-trade-copilot/frontend/app/tracking/page.tsx)、[detail page.tsx](file:///Users/tianyuwang/Projects/day-trade-copilot/frontend/app/tracking/%5Bsymbol%5D/page.tsx)

## 核心问题（为什么会丢）

1. **`IN_POSITION` 高亮是“会话态”**  
   tracking 页开着时，WS 连着，后端内存 `SymbolSession` 持有 `trade`/`state`，因此会持续推送 `IN_POSITION`。  
   一旦跳转到 detail 或返回 tracking，WS 断开重连，后端会重新 `SymbolSession(symbol, mode="realtime")`，默认 `SCAN` 且无 trade，因此高亮消失。

2. **AI 历史是“进程内存态”**  
   `/api/ai/history/{symbol}` 当前读的是 `analysis_history`/`position_history` 两个 dict（进程内存）。重启后为空；另外 WS 自动产生的结果也不一定写入该 dict（已经在部分路径补了，但仍不可跨重启）。

3. **`trades.db` 目前没有完整覆盖自动流程**  
   DB 里确实有 `trades` 与 `trade_events` 两张表，但：
   - WS 自动分析/自动仓管产生的结果不一定写入 `trade_events`（需要确保每次 LLM/仓管调用都 append event）。
   - WS 自动进入 `IN_POSITION` 的时候，`trades` 表未必 upsert，因此 DB 无法在下次连接时恢复 active trade。
   - `trades` 表目前也没有显式 `state` 字段；只能基于 `contracts_remaining/exit_time` 推断是否仍在仓位中，而这又依赖每次仓管决策能同步回写 `contracts_remaining`。

## 结论：需要数据库，但不一定需要“新数据库”

建议 **复用现有 `trades.db`（SQLite）**，把“会话态/内存态”改造成“可恢复的持久化态”，至少覆盖：

- 每一次 LLM analysis call 的输入/输出（用于 detail 页回放）
- 每一次 position management call 的输入/输出（用于 detail 页回放 + 更新持仓剩余合约数）
- 每个 symbol 的 active trade（用于 tracking 进入即高亮，并在 WS 重连后恢复）

SQLite 对当前单机/单用户/本地开发非常合适：部署简单、无需额外服务；并发量也足够支撑“分钟级 bars + 低频 LLM 调用”场景。

## 方案设计

### 1) 数据模型（Schema）建议

现有表（简化）：
- `trades`：交易汇总（trade_id PK，symbol，contracts_remaining，entry/exit 等）
- `trade_events`：事件流水（trade_id + timestamp + event_type + payload_json）

建议进行“最小侵入的增量扩展”：

**A. trade_events 增加 symbol 列（推荐）**
- 目的：detail 页按 symbol 拉历史时，不必先知道 trade_id；也便于 “today only” 查询。
- 迁移：`ALTER TABLE trade_events ADD COLUMN symbol TEXT;`
- 写入：所有 `append_event` 必须写入 symbol（从调用上下文拿 symbol）。
- 回填（可选）：用 `trade_id -> trades.symbol` join 回填旧数据。

**B. trades 增加 state 列（可选，但很有价值）**
- 目的：明确记录状态机关键态（SCAN/IN_POSITION/CLOSED...），让 tracking 能“零推断”直接显示。
- 如果不加 state，也可以用推断：`contracts_remaining > 0 AND exit_time IS NULL` 视为 active。

**C. 明确 event_type 分类**
- `llm_analysis_result`：LLM analysis 返回
- `position_mgmt_result`：position manage 返回
- 可保留现有 `order_*` 等

### 2) 写入策略（保证数据不再丢）

在所有产生结果的路径里，统一写 DB：

**LLM analysis 结果写入**
- `ledger.append_event(trade_id, event_type="llm_analysis_result", symbol=sym, analysis_id=..., bar_time=..., payload=result)`
- 若结果包含 `trade_plan.trade_id` 且进入 `IN_POSITION`（或 ENTRY_PENDING），必须：
  - `ledger.upsert_trade(...)` 写入/更新 trade 基本信息（contracts_total/remaining/option/entry_time）

**Position management 结果写入**
- `ledger.append_event(trade_id, event_type="position_mgmt_result", symbol=sym, bar_time=..., payload=result)`
- 同步回写 `trades.contracts_remaining`；如果 close_all 或 remaining==0，同时写 `exit_time/exit_premium`（可由结果中提取）并把 `state` 标记为 CLOSED（如果采用 state 列）。

这样即使：
- 服务重启
- WS 断开重连
- 用户在 tracking/detail 来回跳转

依然能从 DB 恢复 “当前在仓位的 symbol” 与 “历史 AI 消息时间线”。

### 3) 读取/API 设计（前端可稳定恢复）

**A. 替换 `/api/ai/history/{symbol}` 的数据源**
- 改成查询 DB：
  - `trade_events WHERE symbol = ? AND event_type IN (...) ORDER BY timestamp ASC`
  - 支持 query：`since`（默认当天 00:00 ET）、`limit`、`trade_id`（可选）
- 返回结构保持兼容：`analysis` + `positions`，或统一为 `events`（前端更容易按时间线渲染）

**B. 新增一个轻量的“活跃状态”接口（用于 tracking 首屏）**
- `GET /api/trades/active?symbols=...`
- 返回 per-symbol：
  - `in_position`（推断或 state）
  - `trade_id`
  - `contracts_total/remaining`
  - `option`/`option_symbol`
  - `updated_at`

tracking 页加载时先调用它，直接把 IN_POSITION 高亮做出来；WS 连接上后再用实时 state 覆盖。

**C. WS 初始化时从 DB 恢复 session（推荐）**
- `/ws/realtime` accept 后：
  - 批量查 DB 的 active trades，填充到每个 `SymbolSession.trade/state`
  - 立即发送 `state` 消息（保证“刚进 tracking 就高亮”）

### 4) 前端配合点

- tracking/list：
  - 首屏：先 `GET /api/trades/active` 填充 `sessionBySymbol`，避免 “WS 还没来 state 就全是 SCAN” 的闪烁。
- tracking/detail：
  - `GET /api/ai/history/{symbol}` 必须 DB-backed，才能跨刷新、跨重启恢复历史消息。

## 兼容性与迁移策略

推荐按以下顺序滚动升级（每步可单独上线）：

1. **后端写入完善**：WS 与 REST 全部统一 `append_event` + 必要的 `upsert_trade`（不改前端即可开始积累数据）
2. **`/api/ai/history/{symbol}` 改为查 DB**：前端 detail 历史立即可用
3. **新增 `/api/trades/active` + tracking 首屏预加载**：解决返回 tracking 后不高亮
4. （可选）加 `trade_events.symbol` 列与 backfill：查询更快更稳

## trade.db 是否“能记录所有 trade / 知道哪个 ticker IN_POSITION”？

**现在：部分能，但不可靠**
- `trades.db` 的 `trades` 表能记录 trade（当且仅当对应路径调用了 `upsert_trade`）。
- `IN_POSITION` 当前是“内存状态机”概念；DB 没有直接 state 字段，且 WS 自动流程过去未完整回写 trades，因此无法稳定回答“哪个 symbol 正在 IN_POSITION”。

**按本 proposal 落地后：可以可靠回答**
- 通过 `trades.contracts_remaining > 0 AND exit_time IS NULL`（或 `trades.state == IN_POSITION`）即可直接得出 active symbol。

## 风险与注意事项

- JSON payload 体积：`trade_events.payload_json` 可能较大（LLM 输出）。建议：
  - 对 payload 做轻量裁剪（保留 UI 需要字段）
  - 或增加 `payload_summary` 列以加速列表渲染
- 多用户/多会话：如果未来要多人共享同一后端，建议把 symbol/session 与 user 维度纳入 schema（`user_id`），或迁移到 Postgres。
- “日界线”与市场时区：建议所有存储用 UTC，查询支持按 ET 当天过滤。

## 建议的最小落地目标（MVP）

1. 所有 LLM analysis / position manage 的结果进入 `trade_events`（带 symbol）
2. active trade 信息进入 `trades` 且随仓管更新 `contracts_remaining`
3. `/api/ai/history/{symbol}` 改为 DB 查询
4. tracking 首屏用 `/api/trades/active` 或 WS 初始化恢复，确保 `IN_POSITION` 高亮不再丢

