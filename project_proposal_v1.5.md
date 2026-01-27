# 项目提案：Day Trade Copilot (v1.5 - Implementation-Accurate Specification)

> 说明：v1.5 这份文档不是“理想目标蓝图”，而是**以当前仓库真实代码实现为准**的规格快照（包含已实现/部分实现/未实现的边界）。内容尽量细到可以直接对照代码与接口行为。

---

## 1. 项目概览 (Executive Summary)
Day Trade Copilot 是一个面向日内交易/0DTE 交易的智能辅助系统，核心目标是把“分钟级行情流”变成一个可解释、可回放、可追踪的决策闭环：

**L1 量化触发 (Quant Trigger) → L2 多模态 LLM 分析 (AI Analysis) → L3 状态机编排 + 持仓管理 (FSM + Position Mgmt) → SQLite 事件与交易落库 (Ledger)**。

### 1.1 当前版本定位
当前项目已经具备两条可用主链路：

1. **Realtime Tracking（实时监控页）**
   - 多标的 watchlist（上限 10）分钟级更新。
   - 盘中通过 WebSocket 接收分钟 K 线与 AI 推送；盘外进入只读快照（上一交易日）模式。

2. **Replay Dashboard（回放控制台）**
   - 基于历史分钟线 WebSocket 回放，前端可播放/暂停/重置。
   - 回放过程中同样会触发 LLM 分析与持仓管理（用于策略复盘与验证）。

### 1.2 v1.5 “核心升级点”（相对 v1.4 文档描述的真实落地）
以下是以当前代码为准可确认的“落地升级点”：

* **统一的 WS Autopilot 触发逻辑**：realtime 与 playback 两条 WS 都使用同一套触发与状态机逻辑（watch/follow-up/quant signal/position management）。
* **SQLite 端到端持久化骨架已落地**：`trades.db` 中 `trades` + `trade_events` 两张表支持 active trade 恢复、AI 历史查询与事件时间线。
* **LLM 分析已支持多模态 + 期权链上下文**：后端会生成图表（PNG base64）、文本上下文与期权链信息，强制模型输出结构化 JSON（包含 `trade_plan`）。
* **盘外（Off-hours）前端体验已实现**：tracking 列表页会展示 Off Hours banner，并改为拉取上一交易日的 5m bars 作为迷你图；盘外不再打开 WS 扫描。
* **LLM 调试落盘能力可用**：通过环境变量可把每次 LLM 请求/响应 JSON + 图表 PNG 落盘，便于回溯与 prompt 迭代。

---

## 2. 核心工作流与算法细节 (Core Workflow & Algorithms)

### 2.1 Level 1：量化触发 (Quant Trigger)
系统在 WS 流上对每根 1m bar 计算指标，并以“触发原因”驱动后续 LLM：

#### A. `ZScoreMomentum`（Z-Score 动量策略）
* **统计基准**：默认以过去 30 个交易日的 daily close 计算 `daily_mean / daily_std`。
* **实时计算**：对每根 1m bar close：
  1. `z = (close - daily_mean) / daily_std`
  2. `ema5(z)`，其中 `k = 2 / (5 + 1)`
  3. `z_score_diff = ema5(z)_t - ema5(z)_{t-1}`
* **信号逻辑（阈值穿越）**：只有在“跨越阈值”的那一根才产生 `signal`：
  - LONG：`diff > 0.006 && prev_diff <= 0.006`
  - SHORT：`diff < -0.006 && prev_diff >= -0.006`

> 备注：这意味着持续高动量不会每根都触发，主要捕捉“突破阈值的瞬间”。

#### B. `MACD`（辅助指标）
* **计算参数**：fast=12, slow=26, signal=9。
* **输出字段**：`macd_dif / macd_dea / macd_hist`。
* **信号逻辑**：DIF 与 DEA 的金叉/死叉会生成 `signal=long|short`，但当前系统在多数链路中主要以 `ZScoreMomentum.signal` 作为最终信号源，并把 MACD 作为上下文信息提供给 LLM。

#### C. Realtime 与 Playback 的指标一致性策略
* **Realtime**：WS 启动时会回填一段历史 1m bars 做指标 warmup，随后边 stream 边更新（每根 bar 都带上 `bar.indicators`）。
* **Playback**：以 start 时间为基准，先拉取 start 前的 daily bars 初始化 ZScore，再在回放的分钟线上逐根更新，尽量保证与“当时那一刻”的指标一致。

---

### 2.2 Level 2：LLM 多模态分析 (AI Analysis)
当 autopilot 判定需要分析（trigger_reason 不为空）时，会构建一个包含图表与文本上下文的请求，向 LLM 发起分析。

#### A. 触发原因（TriggerReason）
在 WS 推送的 `bar` 消息里会携带本根 bar 的 `analysis_trigger_reason`：
* `quant_signal`：量化信号触发（主要来自 ZScoreMomentum 阈值穿越）。
* `follow_up`：上一轮 LLM 返回 `follow_up`，进入“等待下一根 bar 验证”的流程。
* `watch_condition`：上一轮 LLM 返回 `check_when_condition_meet` 并设置了价格触发条件，本根 bar 触发该条件。
* `position_management`：当处于持仓状态时，每根 bar 都会先触发持仓管理（见 2.3）。

#### B. Prompt 结构（真实实现）
LLM 请求由三部分组成：

1. **System Prompt（系统指令）**
   - 统一的系统提示词来自 `llm_prompts.get_llm_system_prompt()`。
   - 系统提示词会被动态插入“Nearby Level Filter”（见下文）。

2. **User Text（文本上下文）**
   文本上下文包含：
   - 时间戳（按 PST 显示的可读时间）
   - Daily 60 天 close 序列摘要（用于趋势感知）
   - 前一交易日 High/Low/Close
   - 盘中 Open、Pre-market High/Low、Day High/Low、Current Price
   - 最新指标：EMA9/EMA21/VWAP、布林带、MACD
   - 最近 60 分钟逐分钟 OHLCV 列表（文本版）
   - **Option Chain（最近到期日，ATM 周围 N 档）**
   - **Benchmark Context**：默认拉取 `QQQ, SPY` 的 daily SMA20/50/100/200 与最近 20 分钟价格动作（文本版）

3. **Chart Image（图表 base64 PNG）**
   - 图表基于最近 60 分钟 bars 绘制（蜡烛 + EMA/VWAP/BB + MACD 面板）。
   - 该图会随请求一起发给 Gemini（多模态）。

#### C. Nearby Level Filter（动态规则插入）
系统会根据“最新 1m close 与关键支撑/压力位距离”动态追加规则，要求 LLM 在 reasoning 中点名 level 与距离百分比：

* 候选 level：`day_high/day_low`、`premarket_high/premarket_low`、`prev_day_high/prev_day_low`。
* 阈值：距离 < `0.5% * close` 时插入对应 buy_long/buy_short 限制。
* 例外：若最新 bar 本身就是 day high 或 day low，则两段都不插入（避免在极值 bar 上强行约束）。

#### D. LLM 输出 Schema（强约束）
LLM 分析输出是严格 JSON，对应字段（简化描述）：

```json
{
  "analysis_id": "string",
  "timestamp": "ISO8601",
  "symbol": "NVDA",
  "action": "buy_long | buy_short | ignore | follow_up | check_when_condition_meet",
  "confidence": 0.0,
  "reasoning": "string",
  "pattern_name": "string | null",
  "breakout_price": 0.0,
  "watch_condition": { "trigger_price": 0.0, "direction": "above|below", "expiry_minutes": 15 } | null,
  "trade_plan": {
    "trade_id": "trd_...",
    "direction": "long|short",
    "option": { "right": "call|put", "expiration": "YYYY-MM-DD", "strike": 0.0 },
    "contracts": 1,
    "risk": { "stop_loss_premium": 0.85, "time_stop_minutes": 20 },
    "take_profit_premium": 2.5,
    "option_symbol": "OCC_SYMBOL | null"
  } | null
}
```

关键约束：
* 当 action 是 `buy_long/buy_short` 时，`trade_plan` 必须非空，并且 `trade_plan.direction` 与 action 必须一致。
* 其他 action 必须 `trade_plan = null`。

#### E. analysis_id：稳定 ID + 内存缓存（当前真实边界）
* 返回给前端的 `analysis_id` 是一个稳定 hash：由 `symbol + bar_time + model_hint + prompt_hash` 生成。
* 后端对 `analysis_id` 做 **in-flight 去重** 与 **TTL 缓存**（默认 6 小时，可用环境变量调整）。
* 重要边界：`GET /api/analysis/{analysis_id}` 只查**内存缓存**，服务重启后该接口无法命中；若要跨重启查历史，应使用 DB 事件聚合接口（见 3.3 / 4.1）。

---

### 2.3 Level 3：交易编排与状态机 (Orchestration FSM + Position Mgmt)
系统对每个 symbol 维护一个 `SymbolSession`（内存态），其状态机枚举如下：

* `SCAN`：默认扫描态
* `AI_VERIFY`：正在等待/执行 LLM 分析（analysis inflight）
* `FOLLOW_UP_PENDING`：等待下一根 bar 做二次验证
* `WATCH_PENDING`：等待触发价格条件（watch_condition）
* `ENTRY_PENDING`：已产生买入计划（但当前实现中不会真实提交订单）
* `IN_POSITION`：持仓状态（当前实现为“模拟持仓”，用 contracts_remaining 表示剩余手数）
* `EXIT_PENDING` / `CLOSED`：为未来扩展预留，当前在主链路中主要通过把 contracts_remaining 置 0 并回到 SCAN 来代表结束

#### A. 状态流转（真实实现逻辑）
1. `SCAN` → `AI_VERIFY`
   - 触发条件：`quant_signal` / `follow_up` / `watch_condition`
2. `AI_VERIFY` →
   - `follow_up`：进入 `FOLLOW_UP_PENDING`，并“armed”
   - `check_when_condition_meet`：进入 `WATCH_PENDING`，并追加一个 watch（含 expiry）
   - `buy_long/buy_short`：标记为 `ENTRY_PENDING`，随后立刻构建 ActiveTrade 并进入 `IN_POSITION`
   - `ignore`：回到 `SCAN`
3. `WATCH_PENDING`
   - 每根 bar 会检查是否触发价格条件；超时会自动清空 watch 并回到 `SCAN`
4. `IN_POSITION`
   - 每根 bar 会优先触发一次 Position Management（LLM）来决定 hold / close_all / close_partial / 调整风险参数
   - 目前“硬止损/止盈”并未在 WS autopilot 中做本地强制检查（见 8.2）

#### B. Position Management（持仓管理）
持仓管理请求包含：
* 当前持仓（direction、contracts_total/remaining、entry_time、risk：stop_loss/take_profit/time_stop 等）
* 最近 300 分钟 OHLCV（或由后端自行拉取）
* 图表（最近 60 分钟）与文本上下文（与分析类似）

支持的决策动作：
* `hold`
* `close_all`
* `close_partial`（需要指定 contracts_to_close）
* `tighten_stop`（更新 `stop_loss_premium`）
* `adjust_take_profit`
* `update_time_stop`（注意：是“增量 minutes”，不是绝对值替换）

#### C. Time Stop（硬风控：时间止损）
当前版本在 autopilot 内置了一个明确的硬规则：
* 如果设置了 `time_stop_minutes`，并且 `bar_time - entry_time >= time_stop_minutes`，则直接生成 `close_all` 决策并推送到前端，同时把 contracts_remaining 置 0，状态回到 `SCAN`。

---

## 3. 数据库持久化架构 (SQLite Ledger / trades.db)
当前版本已经有一个可工作的 SQLite “账本”骨架，但并非所有状态机细节都持久化（详见 3.4）。

### 3.1 数据库位置与初始化
* DB 文件默认在：`backend/trades.db`
* 后端启动时会自动运行 schema 初始化与兼容迁移（仅 `ALTER TABLE ADD COLUMN` 级别）。

### 3.2 当前真实 Schema

#### A. `trades`（交易快照表）
用于记录“一个 trade_id 的最新快照”，便于恢复 active trade：

```sql
CREATE TABLE IF NOT EXISTS trades (
  trade_id TEXT PRIMARY KEY,
  symbol TEXT NOT NULL,
  mode TEXT NOT NULL,              -- realtime | playback
  execution TEXT NOT NULL,         -- simulated | paper | live（当前主链路多为 simulated）
  state TEXT,                      -- IN_POSITION / CLOSED 等（并非强约束枚举）
  option_symbol TEXT,
  option_right TEXT,
  option_expiration TEXT,
  option_strike REAL,
  contracts_total INTEGER,
  contracts_remaining INTEGER,
  entry_time TEXT,
  entry_premium REAL,
  exit_time TEXT,
  exit_premium REAL,
  pnl_option_usd REAL,
  extra_json TEXT,                 -- JSON：direction / risk / take_profit_premium 等
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
);
```

#### B. `trade_events`（事件日志表）
用于记录 AI 分析/仓管/下单等事件，供 UI 时间线回放与历史查询：

```sql
CREATE TABLE IF NOT EXISTS trade_events (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  trade_id TEXT NOT NULL,
  symbol TEXT,
  timestamp TEXT NOT NULL,
  event_type TEXT NOT NULL,
  analysis_id TEXT,
  bar_time TEXT,
  payload_json TEXT
);
CREATE INDEX IF NOT EXISTS idx_trade_events_trade_id ON trade_events(trade_id);
CREATE INDEX IF NOT EXISTS idx_trade_events_ts ON trade_events(timestamp);
CREATE INDEX IF NOT EXISTS idx_trade_events_symbol_ts ON trade_events(symbol, timestamp);
```

### 3.3 当前事件类型（真实使用情况）
当前代码中明确写入 DB 的事件（以 event_type 为准）：
* `llm_analysis_result`：每次分析结果
* `position_mgmt_result`：每次持仓管理结果

同时，在历史查询接口中，允许筛选这些类型（即便某些类型可能来自其他链路）：
* `ai_verify_result`
* `position_mgmt_requested`

### 3.4 状态恢复机制（当前真实能力）
Realtime WS 建立连接后会：
1. 从 `trades` 表查询 active trade（条件：`contracts_remaining > 0` 且 `exit_time IS NULL/''`）
2. 解析 `extra_json`，恢复 `direction/risk/take_profit` 等字段
3. 为对应 symbol 的 session 构建 `ActiveTrade` 并设置为 `IN_POSITION`
4. 通过 WS 向前端推送 `state` 消息，使 tracking 卡片/详情页进入“持仓态”高亮

### 3.5 当前持久化的真实边界（重要）
以下内容**仍然是内存态**，服务重启后无法完全恢复：
* `WATCH_PENDING` 的 watch 列表（触发价/过期时间）
* `FOLLOW_UP_PENDING` 的 armed 状态
* analysis in-flight 状态、manage in-flight 状态
* `/api/analysis/{analysis_id}` 内存缓存（TTL 过期或服务重启即丢失）
* “期权 synthetic OCO”跟踪表（进程内 dict，未入库）

---

## 4. API 与 WebSocket 协议 (Backend Contract)

### 4.1 HTTP API（当前真实接口清单）

#### A. 健康检查 / 市场状态
* `GET /api/health`
* `GET /api/market/status`
  - 返回字段：`server_time/session/is_open/next_open/next_close/last_rth_open/last_rth_close`
  - 其中 `session` 会按 ET 的 pre_market/regular/after_hours/closed 计算，并优先参考 Alpaca clock（若可用）

#### B. 行情数据（Stocks）
* `GET /api/stocks/bars?symbols=...&timeframe=...&start=...&end=...&limit=...`
* `GET /api/stocks/snapshots?symbols=...`
* `GET /api/stocks/prev_close?symbols=...&asof=...`
* `GET /api/stocks/symbols?q=...`（用于前端添加 symbol 的建议列表）

#### C. 期权数据（Options）
* `GET /api/options/contracts?underlying=...`
* `GET /api/options/chain?underlying=...&asof=...&strikes_around_atm=...&feed=...`
* `GET /api/options/quotes?symbols=...`
* `GET /api/options/bars?symbols=...&timeframe=...&start=...&end=...&limit=...`

#### D. AI 分析与历史
* `POST /api/analyze`：单次分析（也会写入 `trade_events`；若包含 trade_plan 会 upsert trade）
* `GET /api/analysis/{analysis_id}`：从内存 TTL cache 读取（服务重启后不可用）
* `GET /api/ai/history/{symbol}?since=...&limit=...`：从 `trade_events` 聚合当天/指定区间的 analysis + position 事件
* `POST /api/ai/verify`：通过 OpenRouter 进行简化 schema 的“验证”调用（与主分析链路不同）
* `POST /api/ai/position_manage`：单次持仓管理（主要给回放/测试或外部调用）

#### E. Trades / Ledger 查询
* `GET /api/trades?symbol=...&mode=...&execution=...`
* `GET /api/trades/active?symbols=...`：tracking 列表页启动时用于恢复 UI in_position
* `GET /api/trades/{trade_id}`
* `GET /api/trades/{trade_id}/events`

#### F. Trading（Alpaca 交易代理）
后端提供了 Alpaca trading 的代理接口（account/positions/orders/activities + submit/replace/cancel + OCO 等）。
注意：这套接口存在，但**主链路的 WS autopilot 默认不会自动触发真实下单**（见 8.3）。

### 4.2 WebSocket：消息类型与语义
所有 WS 消息都是 JSON，常见类型：

* `init`：连接建立后，发送当前窗口 bars（用于前端初始化图表）
* `bar`：每根 1m bar 推送（包含 `analysis_trigger_reason` 与 `bar.indicators`）
* `analysis`：当触发 LLM 分析后推送结果（包含 trigger_reason）
* `position`：持仓管理结果推送（包含 trigger_reason=position_management）
* `state`：状态机状态推送（包含是否 in_position、contracts_remaining 等）
* `done`：回放结束标记（playback 模式）
* `error`：错误消息

### 4.3 `/ws/realtime`（实时模式）
关键 query 参数：
* `symbols=...`：逗号分隔
* `analyze=true|false`：是否开启 autopilot（量化触发 → LLM 推送）
* `analysis_window_minutes`：保留的分析窗口长度（默认 300）

### 4.4 `/ws/playback`（回放模式）
关键 query 参数：
* `symbols=...`
* `analyze=true|false`
* `analysis_window_minutes`
* `start=ISO8601`：回放起点
* `speed=0.05..60`：回放速度倍率
* `flow=timer|ack`：推送流控方式
* `limit/cursor`：回放窗口与 cursor

在 `flow=ack` 模式下，前端需要按协议回传 ack 来驱动继续推送，用于更稳定的 UI 节流与暂停控制。

---

## 5. 前端 UI/UX 规格（以当前实现为准）

### 5.1 页面结构
* `/`：Landing（展示入口，不参与交易逻辑）
* `/tracking`：多标的实时追踪（盘中 WS；盘外快照）
* `/tracking/[symbol]`：单标的详情（图表 + AI stream）
* `/dashboard`：回放控制台（WS playback + AI stream）
* `/portfolios`：账户与持仓总览（Account selector + Positions table，提案新增页）

### 5.2 Tracking Page（/tracking）真实交互细节

#### A. Watchlist 管理
* 默认 watchlist：`META, NVDA, TSM, PLTR, AAPL, NFLX, SPY, QQQ`
* 上限 10 个 symbol
* 本地持久化：localStorage key `tracking:watchlist`
* 支持搜索建议：通过后端 `/api/stocks/symbols?q=` 获取建议列表

#### B. 盘中（Regular session）行为
* 连接 WS：`/ws/realtime?symbols=...&analyze=true`
* 接收并渲染：
  - `init`：初始化 bars
  - `bar`：增量 bars（保留最近 500）
  - `analysis`：保存到 localStorage（key `analysis:{analysis_id}`），用于详情页快速恢复
  - `state`：更新每个卡片的状态/持仓标记
* Auto-sort：当前仅对 `in_position && contracts_remaining>0` 的卡片置顶，其余保持 watchlist 原始顺序。

#### C. 盘外（Off-hours）行为
当 `market.session !== "regular"` 时：
* 不建立 WS 连接（wsStatus 保持 closed）
* 顶部展示 Off Hours banner：显示 session 类型 + next open 倒计时 + next open 的 ET/PT 时间
* 卡片状态统一显示 `OFF HOURS`（替代 SCANNING）
* 价格字段改为“上一完整交易日”的回顾数据：
  - 拉取 `1Day` bars（limit=10）取最新一根作为 `Prev Session Open/Close`
  - `Open→Close %` 作为主涨跌指标
* 迷你图表改为：拉取上一交易日 `5Min` bars（start=last_rth_open, end=last_rth_close），并在图表角标标注 `Prev Session · 5m`
* 若无数据则显示 `No prior session data`

### 5.3 Tracking Detail（/tracking/[symbol]）
* 通过 WS `/ws/realtime?symbols={symbol}&analyze=true` 驱动主图与 AI stream。
* 使用共享的控制台骨架组件：左侧图表 + 右侧 AI 消息（TickerConsole）。
* 支持从 localStorage 恢复最近一次分析（analysis_id → 内容），并可通过 `/api/ai/history/{symbol}` 补齐当天事件流。

### 5.4 Replay Dashboard（/dashboard）
* 核心定位：复盘与验证（不是实时交易页）。
* WS：`/ws/playback?...&flow=ack&analyze=true`（默认）
* Transport 控件：Start/Pause/Reset，支持选择回放起点（PT 时区输入框 → 转 RFC3339）。
* UI 渲染：同样复用 TickerConsole（图表 + AI stream），并展示 state/position 决策。

### 5.5 Portfolios（/portfolios）（提案新增页：账户与持仓总览）

#### A. 页面目标（Why）
* 让用户在一个页面里完成三件事：选择账户（paper/live/未来 broker 子账户）→ 读懂账户健康度与当日盈亏 → 以表格方式管理所有持仓。
* 与 `/tracking`、`/dashboard` 保持一致的“科技感高交互（Neumorphism + Glassmorphism）”视觉语言：深色底、玻璃面板、霓虹强调色、微交互反馈。

#### B. 页面结构（上下两段，移动端优先 375×812）

**1) 顶部：Account Selector + Quick Actions（固定头部）**
* 左侧：`Account` 标题 + 下拉选择框（glass pill）。
* 下拉选项（最小可用集合）：
  - `Paper Trading`（对应 `execution=paper`）
  - `Live Trading`（对应 `execution=live`；若 `live_trading_enabled=false` 则置灰并显示锁定标识）
  - `Brokerage Accounts (Coming Soon)`（预留：Alpaca Broker API 的多 account_id 列表）
* 右侧：轻量操作按钮（次要）：`Refresh`、`Transfer / Funding`（若后端未实现则显示 disabled 状态与 tooltip 文案）。
* 状态提示：右上角 `Data: Realtime / Delayed` 小字 + 最近刷新时间；请求失败时展示错误 pill（不使用全屏打断）。

**2) 上半部分：Account Overview（信息卡片网格）**
* 布局：2 列卡片网格（移动端），桌面端 3–4 列自适应；卡片高度统一，支持 skeleton。
* 每张卡片包含：icon（霓虹单色）+ label（10–12px）+ value（18–22px）+ delta（可选，12px）。
* 必须展示的核心指标（与 Alpaca 字段/可计算项对齐）：
  - `Net Account Value`：优先 `account.portfolio_value`，否则回退 `account.equity`。
  - `Total Unrealized Gain`：`Σ positions.unrealized_pl`；同时展示百分比 `Σ unrealized_pl / Σ cost_basis`。
  - `Day's Gain Unrealized`：优先使用 Alpaca position 的当日变动字段（例如 `change_today` + `market_value` 推导），否则以 `Σ (current_price - lastday_price) * qty` 的近似值回退（缺字段时显示 `—`）。
  - `Day's Gain Realized`：优先聚合当日成交/交易活动计算已实现盈亏；若无数据源则显示 `—` 并提供信息提示。
  - `Cash Purchasing Power`：优先 `account.buying_power`；若是现金账户则可展示 `cash`。
  - `Available for Withdrawl`：优先 `account.cash_withdrawable`（或同义字段），缺失则回退 `cash` 并标注 `Estimate`。

**3) 上半部分补强（建议作为可折叠 / 次行模块）**
* `Equity Curve (Today)`：一条极简折线（霓虹渐变 stroke），进入页面时使用 stroke-dasharray 动画“绘制”；右侧显示 `Day Return %`。
* `Exposure`：显示 `Long Market Value / Short Market Value / Net Exposure`，并给出 `Exposure as % of NAV`。
* `Risk & Margin`：
  - `Margin Usage`（进度条：已用/可用 buying power）
  - `Leverage`（若可计算：gross exposure / NAV）
  - `Concentration`（最大单一持仓占比）

**4) 下半部分：Positions Table（持仓表格 + Total 汇总行）**
* 表格上方工具条：
  - `View`（All Positions / Stocks / Options）
  - `Filter by Symbol` 搜索框
  - `Sort`（PnL、Market Value、Day Change、%NAV）
* 表格交互：
  - 行 hover 采用 filter drop-shadow 霓虹高亮；selected 行保持更强对比。
  - 支持行展开（Disclosure）：展示成本细节/最新报价/相关订单（未实现时占位）。
  - 表头 sticky；移动端允许横向滚动，`Symbol` 列固定（sticky left）。
* 推荐列（从“最重要”到“次要”）：
  - `Symbol / Name`（主文本 + 次行显示资产类型：Stock/Option、到期日/行权价）
  - `Qty`（正负号区分 long/short）
  - `Avg Entry`、`Mark/Last`、`Market Value`
  - `Unrealized P/L $`、`Unrealized P/L %`
  - `Day P/L $`、`Day P/L %`
  - `% of NAV`
  - `Actions`（默认仅提供跳转：`Open in Tracking`；交易类动作在 `auto_trade_execution_enabled` 或手动确认后解锁）
* 表格底部汇总：
  - 最后一行固定为 `Total`，聚合本页所有持仓：`Total Market Value / Total Unrealized / Total Day P&L` 等。
  - 建议在 `Total` 上方额外显示一行 `Cash`（与 trading account 字段对齐），从而让用户一眼对上 NAV 的构成。

#### C. 视觉与动效规范（与现有页面一致）
* 背景：深色基底（建议区间 `#05060A`–`#0B1020`），叠加低对比网格/粒子（不影响可读性）。
* 卡片（Neumorphism + Glass）：
  - 背景：`rgba(255,255,255,0.06)`，边框：`rgba(255,255,255,0.10)`
  - 阴影：inset 深阴影 + 轻高光，强调“凹凸”质感
  - Hover：使用 `filter: drop-shadow(...)` 增强霓虹氛围（与 UI 预览一致）
* 颜色语义：
  - 正收益：霓虹绿/青（示例：`#22C55E` 或 `#2EE9A6`）
  - 负收益：霓虹红/玫紫（示例：`#FB7185` 或 `#F43F5E`）
  - 关键强调：蓝紫渐变（示例：`#60A5FA → #A78BFA`）
* 数字动效：关键数值在切换账户/刷新时支持轻量“滚动/计数”过渡（不需要持续动画）。

#### D. 状态与边界（必须覆盖）
* Loading：顶部选择框可交互；卡片与表格使用 skeleton；避免全屏 spinner。
* Empty positions：展示空态卡片（icon + 文案）并引导跳转 `/tracking` 添加关注标的。
* Live 禁用：当 `execution=live` 不可用时，明确展示原因（权限/未配置密钥/开关关闭）。
* 错误容错：部分指标缺失时显示 `—`，但页面保持可用；不要让单字段错误阻塞整页。

#### E. 可访问性（A11y）
* Account dropdown 使用可键盘操作的 listbox 语义（或等价实现），并提供清晰的 focus ring（霓虹描边但对比要足）。
* 表格使用语义化 table（或 grid role）并保证列标题可被读屏关联；排序状态要有 aria 提示。
* 数值变化区域（如 Day P/L）不要高频 `aria-live`；仅在用户触发刷新/切换账户后做一次 polite 更新。

---

## 6. 技术栈与环境 (Tech Stack)

### 6.1 Backend
* **Language**：Python
* **Framework**：FastAPI + Uvicorn
* **Market Data / Trading**：Alpaca（REST + streaming）
* **LLM（主链路）**：Google Generative AI Python SDK（多模态，`response_mime_type=application/json`）
* **LLM（辅助 verify）**：OpenRouter chat completions（简化验证 schema）
* **DB**：SQLite（标准库 sqlite3）
* **数据处理**：Pandas / NumPy
* **图表生成**：matplotlib（生成 PNG 并 base64 注入）

### 6.2 Frontend
* **Framework**：Next.js 14（App Router）
* **UI**：React 18 + Tailwind CSS
* **动画**：Framer Motion
* **图表**：TradingView Lightweight Charts（轻量图）
* **图标**：Lucide React

---

## 7. 配置、运行与调试 (Configuration & Operations)

### 7.1 Backend 环境变量（真实读取项）
后端会从 `backend/.env` 加载环境变量。必需项：
* `ALPACA_PAPER_API_KEY` / `ALPACA_PAPER_SECRET_KEY`（或退化到 `ALPACA_API_KEY/ALPACA_SECRET_KEY`）
* `GOOGLE_API_KEY`（主 LLM 调用必需）

可选项（影响行为）：
* `GOOGLE_MODEL`：Gemini 模型名（默认值在不同模块中存在差异，建议显式配置）
* `OPENROUTER_API_KEY` / `OPENROUTER_MODEL`：仅用于 `/api/ai/verify`
* `ALPACA_FEED`：`iex|sip`
* `ALPACA_OPTIONS_FEED`：`indicative|opra`
* `OPTION_CHAIN_STRIKES_AROUND_ATM`：期权链 ATM 周围档位数（默认 5）
* `BENCHMARK_SYMBOLS`：基准标的（默认 `QQQ,SPY`）
* `ANALYSIS_CACHE_TTL_SECONDS`：分析 cache TTL（默认 21600 秒）
* `STREAM_CHART_WINDOW_MINUTES` / `STREAM_INDICATOR_WARMUP_MINUTES` 等：影响 WS 回填与图表窗口

### 7.2 Trading Settings（当前真实边界）
* 后端提供 `GET/POST /api/settings/trading`（auto_trade_execution_enabled / live_trading_enabled / default_execution）。
* 这些设置是**进程内变量**，不会写入 DB；服务重启会恢复默认值（默认：auto_trade_execution_enabled=false）。

### 7.3 LLM 调试日志落盘
当开启：
* `OUTPUT_DEBUG_LOG=true`
* `DEBUG_LOG_DIR=./logs`（可相对 backend/ 或绝对路径）

系统会把每次 LLM 交换内容写入：
* `logs/llm/<kind>/<YYYY-MM-DD>/*.json`（包含 system_prompt/user_prompt/raw_response/parsed_json/duration 等）
* 同名 `.png`：保存当次发送给模型的图表截图

---

## 8. 已知差距、风险与技术债（v1.5 真实状态）

### 8.1 “完全可恢复”的持久化尚未达成
当前 DB 能恢复 active trade 的核心字段，但无法恢复 watch/follow-up 等“等待态上下文”，因此：
* 服务重启后可以恢复“是否持仓”，但无法恢复“正在等待触发的条件与原因”。

### 8.2 硬止损/止盈未做本地强制执行
当前 autopilot 内置的硬规则只有 **Time Stop**。`stop_loss_premium/take_profit_premium` 主要作为 LLM 决策上下文存在：
* 如果需要严格风控（例如 Bid<=SL 立即 close_all），需要在后端引入“期权报价采样 + 本地规则判定 + 强制平仓”闭环（当前未实现为强制逻辑）。

### 8.3 自动下单默认关闭，且主链路以“模拟持仓”为主
* 虽然后端提供 Alpaca trading 代理接口与前端 Trading 设置 UI，但 WS autopilot 默认不会走“生成 trade_plan → 下单 → 成交 → 更新仓位”的全自动链路。
* 当前 `buy_*` 更接近“生成交易计划 + 进入模拟 IN_POSITION”，并用 Position Management 决策推进 contracts_remaining 变化。

### 8.4 依赖与安装文档存在不一致
* `backend/requirements.txt` 只列出少量依赖，而真实运行还需要 pandas/numpy/matplotlib/google-generativeai/alpaca 等包。
* 当前更像是依赖 `backend/.venv` 环境的“工作副本式”运行方式；如果要面向部署，需要补齐依赖锁定与安装说明。

### 8.5 安全与多用户能力缺失
* 当前 API/WS 未做鉴权（仅本地 CORS 限制），不适合直接暴露公网。
* DB 是单实例文件，未引入用户隔离与权限控制。

---

## 9. Backlog（建议的 v1.6+ 方向，非现状承诺）
以下是按当前差距自然延伸出的可落地路线，仅作为下一步建议：

1. **FSM 全量持久化**：把 watches、follow_up、last_bar_time、以及每次决策的“状态切换事件”结构化写入 DB，做到进程重启后的完全恢复。
2. **硬风控闭环**：引入期权 quote/bars 的实时采样，落地 stop_loss/take_profit 的本地强制规则（优先 simulated，后续接 paper/live）。
3. **分析/仓管事件统一协议**：把所有 AI/仓管请求也写入 `trade_events`（requested/result 配对），并在前端提供可追踪时间线。
4. **依赖与部署清单标准化**：补齐 requirements/lockfile，固化 backend/.env 模板与启动脚本，降低环境漂移。
