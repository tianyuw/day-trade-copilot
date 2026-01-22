# 项目提案：Day Trade Copilot (v1.3)

## 1. 项目概览
Day Trade Copilot 是一个智能股票监控系统，旨在通过实时分析 1 分钟 K 线图来辅助交易者。系统采用**“量化筛选 + AI 验证”**的双层架构：首先利用高效的多种量化指标算法实时扫描潜在的突破点位，一旦检测到信号，立即调用 **gemini-3-flash-preview** 的多模态能力进行深度验证，确认突破的真实性和有效性，从而提供高胜率的可执行交易信号。

*v1.3 版本核心变更：引入了基于 Pine Script 思路重写的量化筛选算法（当前实现为 ZScoreMomentum / z_score_diff 阈值信号）作为一级过滤器，将 AI 的角色从“每分钟巡检”转变为“按需验证”，显著降低成本并提高信号质量。*

## 2. 核心工作流

### 2.1 第一层：量化筛选 (Quant Filter)
- **核心算法**: 基于 Pine Script 思路重写的量化筛选算法（当前实现：`ZScoreMomentum`，用 `z_score_diff` 阈值穿越生成 long/short 信号）。
  - **逻辑**: 综合计算价格、成交量及波动率等统计特征，识别潜在的趋势突破信号。（具体算法细节见后文专章）
- **运行机制**: 对给定的股票列表，系统实时运行该算法，持续监控每一分钟的 K 线收盘状态。
- **触发**: 只有当算法检测到明确的“潜在突破信号”时，才会激活第二层 AI 验证。

### 2.2 第二层：AI 深度验证 (AI Verification)
一旦量化层发出信号，系统立即向 **gemini-3-flash-preview** 发起请求，进行多模态验证。
- **输入数据**:
  1. **市场数据**: 过去约 300 分钟的 1m OHLCV（用于计算指标与形态上下文），并在 Prompt 中重点展示最近 60 分钟的价格行为摘要。
  2. **技术指标**: 基于上述 1m 数据计算的 EMA9, EMA21, VWAP, Bollinger Bands, MACD（并提供最新一根 bar 的关键数值）。
  3. **视觉数据**: 生成的当日盘中完整的 K 线图图片，叠加指标、压力位（Resistance）和支撑位（Support）及量化算法标记出的突破点位。
  4. **期权链数据 (Option Chain)**: 用于在 `buy_long/buy_short` 时选择合约（到期日、行权价）并校验点差/流动性约束。

#### 2.2.1 期权链数据获取（新需求：同时支持实时与历史）
为满足 **Replay Dashboard（历史回放）** 与 **Real-time Ticker Tracking（实时追踪）** 两类场景，系统需要同时支持：
- **实时期权链（Real-time Option Chain）**：用于实时追踪页给 LLM/用户提供最新的到期日与行权价候选集合，并能拿到最新 bid/ask（用于点差与流动性过滤）。
- **历史期权链（Historical Option Chain）**：用于回放页在某个历史时间点构造“当时可交易的到期日/行权价候选集合”，用于让 LLM 选择合约并生成 `trade_plan`。

基于 Alpaca Options Data API（见 `alpacaAPIDoc/options_api.md`），可用的数据能力包括：
- **链快照/实时链（REST Snapshot）**：`GET /v1beta1/options/snapshots/{underlying_symbol_or_symbols}` 获取期权合约最新 trade/quote/greeks/IV（用于实时链的报价层）。
- **历史数据（REST Historical）**：
  - `GET /v1beta1/options/bars`：期权合约 1Min 历史 OHLCV。
  - `GET /v1beta1/options/quotes`：期权合约历史 bid/ask（用于“历史时间点”的点差评估）。
  - `GET /v1beta1/options/trades`：期权合约历史成交（可选，用于更真实的成交/流动性评估）。
- **实时数据（WebSocket）**：`wss://stream.data.alpaca.markets/v1beta1/options` 订阅 quotes/trades（用于对选定的一小批合约做实时更新）。

工程落地需要额外补齐的关键点（实现约束）：
- **合约列表来源（到期日/行权价宇宙）**：快照/历史 bars/quotes 都要求传入“期权合约 symbols”。因此系统必须具备“从 underlying -> 枚举 option contract symbols（按到期日/行权价/看涨看跌）”的能力；该能力将作为 Option Chain 的元数据层（contracts universe）。
- **输出格式（给 LLM 的 option_chain 结构）**：至少包含 `right(call/put)`, `expiration`, `strike`, `symbol`, `bid`, `ask`, `spread`, `mid`（可选 greeks/IV/OI/volume）。
- **过滤规则（默认）**：只保留**最近到期日（nearest expiration）**的一组合约，并在该到期日下保留**接近 ATM 的若干档 strike 的所有报价**（calls + puts）。

项目后端将新增以下 Options 相关 API（供前端与分析服务复用）：
- `GET /api/options/contracts?underlying=...`：枚举可交易合约（到期日/行权价/put-call/symbol）。
- `GET /api/options/chain?underlying=...&asof=...&strikes_around_atm=N`：返回最近到期日 + ATM 附近若干档 strikes 的 calls/puts 报价集合。
- `GET /api/options/quotes?symbols=...&start=...&end=...`：回放/历史点差评估用的历史 bid/ask。
- `GET /api/options/bars?symbols=...&start=...&end=...`：回放/研究用的期权 1m bars。
- **验证任务**:
  - 产出结构化 `action`：`buy_long / buy_short / ignore / follow_up / check_when_condition_meet`。
  - 若 `action = follow_up`：按 LLM 指示在**下一根 1m K 线收盘**继续验证（再次调用 LLM）。
  - 若 `action = check_when_condition_meet`：按 `watch_condition` 设置本地触发器（`trigger_price` 为**标的（underlying）价格**，非期权价格），**条件触发时**再次调用 LLM 继续验证。
  - 若 `action = buy_long | buy_short`：为节省 LLM call，“期权交易计划”在**同一次**点位验证响应中一并产出，用于直接下 Alpaca paper trading 订单 （在Enable Alpaca Paper Trading Auth Trading时）。

### 2.3 第三层：交易生命周期编排 (Trade Orchestration)
目前系统的 AI 只负责“入场点是否成立”。要让 LLM 真正“完成一笔交易”，需要把 AI 的职责扩展为：从**入场计划 → 持仓管理 → 出场计划 → 复盘结算**的闭环，并且用明确的状态机与结构化输出把它工程化。

- **核心原则**:
  1) **LLM 决策，系统 paper trading 执行（需开关开启）**：仅当 Settings 中启用 “Enable Alpaca Paper Trading Auto Trading” 时，系统才会根据 LLM 的交易计划自动提交 Alpaca paper trading 订单；否则只提示信号、不下单。开启后，系统使用 Alpaca paper trading API 真实下单，并以订单回报与成交记录作为结算与复盘事实来源。
  2) **一致性与可追溯**：每一笔交易都有 `trade_id`，每次 AI 决策都有 `analysis_id`，所有更新都附带“基于哪些事实做出改变”。

- **交易状态机 (FSM)**:
  - `SCAN`：量化引擎持续扫描（当前实现：ZScoreMomentum / z_score_diff 阈值穿越生成 long/short 信号）。
  - `ENTRY_CANDIDATE`：量化信号出现，生成候选入场窗口（bar 时间戳 + 方向 long/short + 触发参考价位）。
  - `AI_VERIFY`：调用 LLM 做“点位验证”，输出 `action`；若为 `buy_long/buy_short`，同一次响应中一并输出期权交易计划（合约 + 止盈/止损/时间止损）。
  - `FOLLOW_UP_PENDING`：若 `action = follow_up`，等待下一根 1m K 线收盘后回到 `AI_VERIFY`（循环验证）。
  - `WATCH_PENDING`：若 `action = check_when_condition_meet`，等待 `watch_condition` 条件触发后回到 `AI_VERIFY`（循环验证）。
  - `PLAN_READY`：仅当 `action = buy_long | buy_short`，且该次 AI_VERIFY 响应中已包含期权交易计划，进入可执行态。
  - `ENTRY_PENDING`：仅当启用 “Enable Alpaca Paper Trading Auto Trading” 时，系统才向 Alpaca paper trading 提交期权入场限价单，这里的限价单默认为 ask_price + 0.03，尽量保证立马成交；若从下单到**下一根 1m K 线收盘**仍未成交，则撤单并结束，放弃该入场点并继续寻找下一个入场点。未启用时不下单，停留在提示/观察态。
  - `IN_POSITION`：入场单成交后进入持仓，自行挂止盈止损单；每根 1m K 线收盘时系统向 LLM 发起一次“卖出点位判断”请求，LLM 输出持仓管理动作（hold/全平/部分平仓/调整止盈止损/更新时间止损等）；若启用 “Enable Alpaca Paper Trading Auto Trading”，系统按该动作自动提交对应的 Alpaca paper trading 平仓/改单；同时系统持续监控止盈/止损/时间止损等硬规则，触发时进入 `EXIT_PENDING`。
  - `EXIT_PENDING`：当 `contracts_remaining == 0`（所有合约均已平仓）时进入平仓结算流程；平仓可能由 LLM 动作（close_all / close_partial 直到清零）或止盈/止损/时间止损等规则触发导致。系统按触发条件使用不同的平仓订单类型（见下方执行模型）。**PnL 仅在启用 Alpaca paper trading 且有真实成交回报（fills）时计算**；Replay 回放模式不计算 PnL。
  - `CLOSED`：平仓完成，订单回报、成交与结算记录均已落库。

- **并发与冲突规则（实现约束）**：
  - **每个 symbol 严格串行（per-symbol sequential）**：系统按 1m bar 收盘逐根处理，同一 symbol 同一时刻只会有一个活跃候选入场点，因此不会出现多个 `ENTRY_CANDIDATE` 并存。
  - **FOLLOW_UP_PENDING / WATCH_PENDING 的定位**：它们是对 `AI_VERIFY` 的“额外触发点位”，用于决定何时再次进入 `AI_VERIFY`，并不与 `SCAN` 停止/互斥。
  - **同一根 K 线多触发合并**：若同一根 1m bar 收盘同时满足 `SCAN` 信号与 `WATCH_PENDING` 触发条件，系统只调用 LLM **一次**，并以该次 `AI_VERIFY` 的结果更新状态机（避免重复推理与 UI 重复事件）。

- **交易记录与事件落库（新需求）**：
  - **目标**：为交易闭环提供“事实账本”，支撑后续复盘、回测对齐、以及 UI 的交易时间线展示。
  - **数据模型**：
    - `trades`：每笔交易一行，主键 `trade_id`；包含 `symbol`、`mode(realtime|replay)`、`execution(paper|simulated)`、期权合约信息（`option_symbol/right/expiration/strike`）、`contracts_total`、`contracts_remaining`、入场/出场时间与 premium；**PnL 汇总字段仅在 `execution=paper` 时写入**，Replay/Simulated 保持为空。
    - `trade_events`：每次状态变化/LLM 决策/下单或模拟成交/风控触发一条事件；包含 `trade_id`、`timestamp`、`event_type`、`analysis_id`（可选）、`bar_time`（可选）以及结构化 `payload`。
      - `event_type` 最小枚举（建议）：
        - `signal_detected`：量化层触发入场候选点（SCAN → ENTRY_CANDIDATE）。
        - `ai_verify_requested`：发起点位验证请求（进入 AI_VERIFY）。
        - `ai_verify_result`：点位验证结果返回（action + trade_plan/null）。
        - `entry_submitted`：提交入场订单（paper trading）或生成模拟入场（replay）。
        - `entry_filled`：入场成交（paper fills）或模拟成交确认（replay）。
        - `position_mgmt_requested`：每根 1m 收盘发起持仓管理决策请求（IN_POSITION）。
        - `position_mgmt_result`：持仓管理决策返回（hold/close/adjust 等）。
        - `exit_submitted`：提交平仓订单（paper trading）或生成模拟平仓（replay）。
        - `exit_filled`：平仓成交（paper fills）或模拟平仓确认（replay）。
        - `risk_triggered`：止盈/止损/时间止损等规则触发（可附 `payload.trigger_type`）。
        - `trade_closed`：交易结束并写入最终状态（CLOSED）。
  - **Replay 策略**：回放模式同样写入落库，但 `mode=replay` 且 `execution=simulated`，便于与 realtime/paper 的交易记录并存对比。

- **LLM 在一笔交易里要做的事情**:
  1) **点位验证 + 期权交易计划 (Verify + Option Plan)**：输出 `buy_long/buy_short/ignore/follow_up/check_when_condition_meet`；若为 `buy_long/buy_short`，在同一次响应中输出期权交易计划（合约 + 止盈/止损/时间止损），用于直接下 Alpaca paper trading 订单。
  2) **持仓管理 (Position Management)**：入场单成交后，每根 1m K 线收盘调用一次 LLM，输出“是否是好的卖出点位”以及要采取的卖出/调整动作（例如 hold / close_all / close_partial / tighten_stop / update_time_stop / adjust_take_profit）。

- **降频优化的事件触发器（可选，未来用于减少每分钟调用）**:
  - **价格触发**：接近止损/止盈阈值（例如距离 < 0.15R 或 < 0.2%）。
  - **结构触发**：跌破/突破 VWAP、EMA 失守、MACD 反向翻转、量能衰竭等。
  - **时间触发**：0DTE 接近特定时刻（例如 10:00/11:00/13:30 PST）或持仓超过 `max_hold_minutes`。
  - **波动触发**：瞬时波动/点差扩大（提示流动性风险，可能提前锁利）。

- **利润计算（仅 paper trading）**:
  - **期权 PnL（以 Alpaca paper trading 成交回报为准）**：系统以 Alpaca paper trading 的成交回报（fills）为唯一真相来源，计算 `pnl_option_usd`；公式仅作为说明：`pnl_option_usd = (exit_premium - entry_premium) * contracts * 100`（做空相反；买 call/put 都适用）。
  - **标准化指标**：同样基于成交回报计算的 `pnl_option_usd`：`R_multiple = pnl_option_usd / (abs(entry_premium - stop_premium) * contracts * 100)`，并记录最大回撤、持仓时长。

- **Alpaca Paper Trading 执行模型**:
  - **入场成交**：系统提交期权限价单，默认限价为 `ask_price + 0.03` 以提高立刻成交的概率，成交价以 Alpaca paper trading 回报为准。
  - **出场成交（按触发条件选择订单类型）**:
    - **LLM 输出 close_all / close_partial**：系统使用 market order 立即卖出（平仓或部分平仓）。
    - **止盈触发**：系统使用 limit order（以 `take_profit_premium` 为目标价）尝试卖出。
    - **止损 / 时间止损触发**：系统使用 market stop order 立即执行风控平仓。
  - **注意**：paper trading 是近似模拟，成交与滑点等假设与实盘可能不同。

### 2.4 LLM 结构化输出 Schema（面向“完整交易”）
为了让 LLM 真正完成“点位验证→入场→出场→结算”的闭环，同时尽量减少 LLM call，需要把输出从单一的 `action` 扩展为“点位验证（buy 时同时包含交易计划）/持仓管理（close 时包含结算与复盘）”两类结构化消息。

#### 2.4.1 点位验证 + 交易计划（同一次 call；buy_long/buy_short 时返回 trade_plan）
**（新需求 / 工程约束）后端响应 Schema 需要同步扩展**：`/api/analyze` 的响应模型 `LLMAnalysisResponse` 必须新增 `trade_plan` 字段，用于在 `action = buy_long | buy_short` 时承载完整期权交易计划，作为 Trade Orchestration 的输入。除 `buy_long/buy_short` 外，`trade_plan` 必须为 `null`。
**A) buy_long（同次返回 trade_plan）**
```jsonc
{
  "analysis_id": "anl_01JXK0F8K0QWQJ7H3P4ZK8S3Q4",
  "timestamp": "2026-01-20T17:38:00Z",
  "symbol": "NVDA",
  "action": "buy_long", // buy_long | buy_short | ignore | follow_up | check_when_condition_meet
  "confidence": 0.86,
  "reasoning": "Breakout confirmed with reclaim + expansion; risk is defined; momentum favors continuation.",
  "pattern_name": "Bull Flag Breakout",
  "breakout_price": 347.5,
  "watch_condition": null,
  "trade_plan": {
    "trade_id": "trd_01JXK0F8M7R9Q7Z6N0H3Q8A2B1",
    "direction": "long", // long | short
    "option": {
      "right": "call", // call | put
      "expiration": "2026-01-23",
      "strike": 350
    },
    "contracts": 1,
    "risk": {
      "stop_loss_premium": 0.85,
      "time_stop_minutes": 15
    },
    "take_profit_premium": 2.1
  }
}
```

**B) buy_short（同次返回 trade_plan）**
```jsonc
{
  "analysis_id": "anl_01JXK0G2Q2F3W0K3H8N2F7M1Z9",
  "timestamp": "2026-01-20T18:12:00Z",
  "symbol": "TSLA",
  "action": "buy_short",
  "confidence": 0.78,
  "reasoning": "Failed reclaim + rejection at VWAP; downside momentum building; risk/reward acceptable for a quick scalp.",
  "pattern_name": "VWAP Rejection",
  "breakout_price": 231.2,
  "watch_condition": null,
  "trade_plan": {
    "trade_id": "trd_01JXK0G2V8W5X1R0K2P9C3D7E6",
    "direction": "short",
    "option": {
      "right": "put",
      "expiration": "2026-01-23",
      "strike": 230
    },
    "contracts": 1,
    "risk": {
      "stop_loss_premium": 0.9,
      "time_stop_minutes": 12
    },
    "take_profit_premium": 2.0
  }
}
```

**C) ignore（不返回 trade_plan）**
```jsonc
{
  "analysis_id": "anl_01JXK0H9S3C8P6N7W2Z1K5T4Y0",
  "timestamp": "2026-01-20T18:25:00Z",
  "symbol": "AAPL",
  "action": "ignore",
  "confidence": 0.62,
  "reasoning": "Signal is too close to major resistance; volume is below average; breakout quality is low.",
  "pattern_name": "Weak Breakout Attempt",
  "breakout_price": 204.4,
  "watch_condition": null,
  "trade_plan": null
}
```

**D) follow_up（下一根 1m 收盘再验证）**
```jsonc
{
  "analysis_id": "anl_01JXK0J1B6Y5T2M9Q4R8V1A7C3",
  "timestamp": "2026-01-20T18:31:00Z",
  "symbol": "AMD",
  "action": "follow_up",
  "confidence": 0.7,
  "reasoning": "Setup is close, but needs one more 1m close to confirm breakout hold; re-check next bar close.",
  "pattern_name": "Breakout Hold Check",
  "breakout_price": 176.8,
  "watch_condition": null,
  "trade_plan": null
}
```

**E) check_when_condition_meet（挂 watch_condition，触发后再验证）**（`watch_condition.trigger_price` 为标的（underlying）价格，非期权价格）
```jsonc
{
  "analysis_id": "anl_01JXK0K8D9H1Q0W3S6T5U4V2X1",
  "timestamp": "2026-01-20T18:40:00Z",
  "symbol": "META",
  "action": "check_when_condition_meet",
  "confidence": 0.73,
  "reasoning": "Structure is constructive, but entry only makes sense if price breaks above the trigger with strength.",
  "pattern_name": "Range Break",
  "breakout_price": 349.8,
  "watch_condition": {
    "trigger_price": 349.8,
    "direction": "above",
    "expiry_minutes": 30
  },
  "trade_plan": null
}
```

#### 2.4.2 持仓管理决策（默认按触发调用；action=close 时同一次输出结算与复盘）
> 注：Replay 回放模式不计算 PnL；因此下方示例中的 `position.pnl` 仅在 `execution=paper`（Alpaca paper trading）时由系统侧基于 fills 计算并写入。
**A) hold（继续持有，不做任何改单/下单）**
```jsonc
{
  "trade_id": "trd_01JXK0F8M7R9Q7Z6N0H3Q8A2B1",
  "analysis_id": "mgmt_01JXK1A9M1C2B3N4V5X6Z7Q8W9",
  "timestamp": "2026-01-20T17:44:00Z",
  "symbol": "NVDA",
  "bar_time": "2026-01-20T17:44:00Z",
  "position": {
    "direction": "long",
    "option": { "right": "call", "expiration": "2026-01-23", "strike": 350 },
    "contracts_total": 2,
    "contracts_remaining": 2,
    "orders": { "entry_order_id": "ord_entry_...", "exit_order_id": null },
    "entry": { "time": "2026-01-20T17:39:12Z", "premium": 1.22 },
    "mark": { "time": "2026-01-20T17:44:00Z", "premium": 1.35 },
    "pnl": { "pnl_option_usd": 26.0, "max_drawdown_usd": 18.0, "minutes_in_trade": 5 },
    "risk": { "stop_loss_premium": 0.85, "take_profit_premium": 2.1, "time_stop_minutes": 15 }
  },
  "decision": {
    "action": "hold", // hold | close_all | close_partial | tighten_stop | adjust_take_profit | update_time_stop
    "reasoning": "Trend/momentum still intact; no reversal signal on this 1m close.",
    "exit": null,
    "adjustments": null,
    "close_outcome": null
  }
}
```

**B) tighten_stop（收紧止损，更新 stop_loss_premium）**
```jsonc
{
  "trade_id": "trd_01JXK0F8M7R9Q7Z6N0H3Q8A2B1",
  "analysis_id": "mgmt_01JXK1B4P0K9R8S7T6U5V4W3X2",
  "timestamp": "2026-01-20T17:47:00Z",
  "symbol": "NVDA",
  "bar_time": "2026-01-20T17:47:00Z",
  "position": {
    "direction": "long",
    "option": { "right": "call", "expiration": "2026-01-23", "strike": 350 },
    "contracts_total": 2,
    "contracts_remaining": 2,
    "orders": { "entry_order_id": "ord_entry_...", "exit_order_id": null },
    "entry": { "time": "2026-01-20T17:39:12Z", "premium": 1.22 },
    "mark": { "time": "2026-01-20T17:47:00Z", "premium": 1.52 },
    "pnl": { "pnl_option_usd": 60.0, "max_drawdown_usd": 18.0, "minutes_in_trade": 8 },
    "risk": { "stop_loss_premium": 0.85, "take_profit_premium": 2.1, "time_stop_minutes": 15 }
  },
  "decision": {
    "action": "tighten_stop",
    "reasoning": "Price advanced; reduce downside by tightening stop to protect gains.",
    "exit": null,
    "adjustments": { "new_stop_loss_premium": 1.05, "new_take_profit_premium": null, "new_time_stop_minutes": null },
    "close_outcome": null
  }
}
```

**C) adjust_take_profit（调整止盈目标，更新 take_profit_premium）**
```jsonc
{
  "trade_id": "trd_01JXK0F8M7R9Q7Z6N0H3Q8A2B1",
  "analysis_id": "mgmt_01JXK1C2F9E8D7C6B5A4Z3Y2X1",
  "timestamp": "2026-01-20T17:50:00Z",
  "symbol": "NVDA",
  "bar_time": "2026-01-20T17:50:00Z",
  "position": {
    "direction": "long",
    "option": { "right": "call", "expiration": "2026-01-23", "strike": 350 },
    "contracts_total": 2,
    "contracts_remaining": 2,
    "orders": { "entry_order_id": "ord_entry_...", "exit_order_id": null },
    "entry": { "time": "2026-01-20T17:39:12Z", "premium": 1.22 },
    "mark": { "time": "2026-01-20T17:50:00Z", "premium": 1.88 },
    "pnl": { "pnl_option_usd": 132.0, "max_drawdown_usd": 18.0, "minutes_in_trade": 11 },
    "risk": { "stop_loss_premium": 1.05, "take_profit_premium": 2.1, "time_stop_minutes": 15 }
  },
  "decision": {
    "action": "adjust_take_profit",
    "reasoning": "Momentum strong; extend take-profit target to let winners run.",
    "exit": null,
    "adjustments": { "new_stop_loss_premium": null, "new_take_profit_premium": 2.4, "new_time_stop_minutes": null },
    "close_outcome": null
  }
}
```

**D) update_time_stop（更新时间止损，延长/缩短 time_stop_minutes）**
```jsonc
{
  "trade_id": "trd_01JXK0F8M7R9Q7Z6N0H3Q8A2B1",
  "analysis_id": "mgmt_01JXK1D7N6M5L4K3J2H1G0F9E8",
  "timestamp": "2026-01-20T17:52:00Z",
  "symbol": "NVDA",
  "bar_time": "2026-01-20T17:52:00Z",
  "position": {
    "direction": "long",
    "option": { "right": "call", "expiration": "2026-01-23", "strike": 350 },
    "contracts_total": 2,
    "contracts_remaining": 2,
    "orders": { "entry_order_id": "ord_entry_...", "exit_order_id": null },
    "entry": { "time": "2026-01-20T17:39:12Z", "premium": 1.22 },
    "mark": { "time": "2026-01-20T17:52:00Z", "premium": 1.73 },
    "pnl": { "pnl_option_usd": 102.0, "max_drawdown_usd": 18.0, "minutes_in_trade": 13 },
    "risk": { "stop_loss_premium": 1.05, "take_profit_premium": 2.4, "time_stop_minutes": 15 }
  },
  "decision": {
    "action": "update_time_stop",
    "reasoning": "Trade is progressing but needs a bit more time; extend time stop.",
    "exit": null,
    "adjustments": { "new_stop_loss_premium": null, "new_take_profit_premium": null, "new_time_stop_minutes": 20 },
    "close_outcome": null
  }
}
```

**E) close_partial（部分平仓；close_outcome 为空，结算以 Alpaca fills 为准）**
```jsonc
{
  "trade_id": "trd_01JXK0F8M7R9Q7Z6N0H3Q8A2B1",
  "analysis_id": "mgmt_01JXK1E3Q2W1E0R9T8Y7U6I5O4",
  "timestamp": "2026-01-20T17:54:00Z",
  "symbol": "NVDA",
  "bar_time": "2026-01-20T17:54:00Z",
  "position": {
    "direction": "long",
    "option": { "right": "call", "expiration": "2026-01-23", "strike": 350 },
    "contracts_total": 2,
    "contracts_remaining": 2,
    "orders": { "entry_order_id": "ord_entry_...", "exit_order_id": null },
    "entry": { "time": "2026-01-20T17:39:12Z", "premium": 1.22 },
    "mark": { "time": "2026-01-20T17:54:00Z", "premium": 1.95 },
    "pnl": { "pnl_option_usd": 146.0, "max_drawdown_usd": 18.0, "minutes_in_trade": 15 },
    "risk": { "stop_loss_premium": 1.05, "take_profit_premium": 2.4, "time_stop_minutes": 20 }
  },
  "decision": {
    "action": "close_partial",
    "reasoning": "Momentum stalling near resistance; take partial profits and reduce exposure.",
    "exit": { "contracts_to_close": 1 },
    "adjustments": { "new_stop_loss_premium": null, "new_take_profit_premium": null, "new_time_stop_minutes": null },
    "close_outcome": null
  }
}
```

**F) close_all（全部平仓；结算由系统基于 Alpaca fills 在交易结束后统一计算）**
```jsonc
{
  "trade_id": "trd_01JXK0F8M7R9Q7Z6N0H3Q8A2B1",
  "analysis_id": "mgmt_01JXK1F9A8S7D6F5G4H3J2K1L0",
  "timestamp": "2026-01-20T17:56:00Z",
  "symbol": "NVDA",
  "bar_time": "2026-01-20T17:56:00Z",
  "position": {
    "direction": "long",
    "option": { "right": "call", "expiration": "2026-01-23", "strike": 350 },
    "contracts_total": 2,
    "contracts_remaining": 2,
    "orders": { "entry_order_id": "ord_entry_...", "exit_order_id": "ord_exit_..." },
    "entry": { "time": "2026-01-20T17:39:12Z", "premium": 1.22 },
    "mark": { "time": "2026-01-20T17:56:00Z", "premium": 1.62 },
    "pnl": { "pnl_option_usd": 80.0, "max_drawdown_usd": 22.0, "minutes_in_trade": 17 },
    "risk": { "stop_loss_premium": 1.05, "take_profit_premium": 2.4, "time_stop_minutes": 20 }
  },
  "decision": {
    "action": "close_all",
    "reasoning": "Reversal signal + momentum breakdown; exit now to protect remaining gains.",
    "exit": { "contracts_to_close": 2 },
    "adjustments": null
  }
}
```

## 3. 数据基础设施
- **提供商**: [Alpaca Market Data API](https://docs.alpaca.markets/docs/about-market-data-api)
- **技术**: WebSocket & REST API。
- **数据流**:
  - **历史数据 (REST)**: 用于回放模式和初始化计算。
  - **实时数据 (WebSocket)**: 
    - **IEX/SIP Feeds**: 用于驱动第一层量化筛选算法和实时执行监控。

## 4. 系统架构
1. **数据摄取层**: 管理与 Alpaca 的 WebSocket 连接以及 REST API 请求。
2. **量化引擎 (Quant Engine)**: 
   - 实时运行 Python 重写版的量化筛选逻辑。
   - 充当系统的“守门员”，过滤掉绝大多数无效波动。
3. **处理层**:
   - 仅在触发时计算复杂指标、渲染图表。
4. **AI 编排器**: 接收量化引擎的触发信号，调用 Gemini 3 Pro。
5. **Web 应用**: 提供用户交互界面。

## 5. 用户界面 (Web App)

### 5.1 设计理念 (Design Philosophy)
- **视觉风格**: 采用 "Dark Gen-Z" 风格。
  - **主色调**: 深邃黑 (#050505) 背景，营造沉浸式科技感。
  - **配色**: 霓虹蓝 (Neon Blue)、赛博紫 (Cyber Purple) 和 荧光绿 (Highlighter Green) 作为强调色，用于数据和交互反馈。
  - **质感**: 大量使用 **玻璃拟态 (Glassmorphism)** 和 **新拟态 (Neumorphism)**，结合发光效果 (Glow Effects)，打造未来控制台的视觉体验。
  - **交互**: 高频微交互 (Micro-interactions)，按钮悬停发光，数据动态流转。

### 5.2 核心页面设计

#### A. 落地页 (Landing Page)
- **功能**: 品牌展示与快速入口。
- **布局**:
  - **Navigation Bar**: 顶部悬浮玻璃导航栏。包含全息风格 Logo、应用名称 "Day Trade Copilot"。
  - **Hero Section**: 
    - 核心标语 "Master the Market Pulse with AI" (动态渐变文字)。
    - 背景采用动态粒子或 3D 抽象金融数据流。
  - **Call to Action (CTA)**: 
    - 醒目的 "Enter Replay Console" 按钮。
    - 悬停时产生霓虹光晕扩散效果，点击即刻跳转至回放控制台。

#### B. 股票实时追踪页面 (Stock Real-time Tracking Page)
- **页面目的**: 实时监视最多10个股票ticker走势，自动高亮（Highlight）出现合适入场点的ticker，并将其动态排序至列表顶部，方便用户快速捕捉机会。
- **页面布局与组件细节**:
  - **1. 顶部控制区 (Control Header)**:
    - **位置**: 页面顶部固定区域，采用玻璃拟态背景。
    - **组件**:
      - **Add Ticker Card**: 监控 Grid 的最后一个卡片为虚线边框 + 加号按钮。点击后弹出搜索（Search/Typeahead），用户输入或选择 Ticker 即可添加到监控列表（最多 10 个）。
      - **Remove Ticker (Long-Press)**: 长按任意 Ticker 卡片进入“编辑态”，卡片右上角浮现删除按钮；点击即可移除该 Ticker 并退出编辑态。
      - **Market Status Pill**: 顶部右侧显示当前股市状态（Pre-Market / Regular / After-Hours / Closed），并带有状态色与简短文案。
      - **Next Session Countdown**: 在状态旁显示倒计时（例如“距开盘 00:17:32”或“距收盘 01:05:10”）。
      - **System Pulse**: 右上角显示 "AI Monitoring" 呼吸灯指示器 (Neon Green)，表示 WebSocket 连接正常。
  - **2. 监控主列表 (Live Monitor Grid)**:
    - **布局**: 响应式网格布局 (Grid)，桌面端 2-3 列，移动端单列。
    - **核心组件: `StockSignalCard` (智能信号卡片)**:
      - **视觉风格**: 深色磨砂玻璃面板 (Frosted Glass)。默认状态低调，触发信号时激活 **"Focus Mode"**。
      - **信息排布**:
        - **Header (左上)**: Ticker Symbol (大号无衬线字体) + 现价 (实时跳动，涨绿跌红)。
        - **Chart Area (中间)**: 嵌入 **Mini-CandleChart** (最近 30 分钟 K 线缩略图)，叠加 EMA 趋势线，直观展示短期形态。
        - **Signal Badge (右上)**: 动态 AI 状态徽章。
          - *Scanning*: 灰色脉冲动画，文字 "Scanning..."
          - *Signal Detected*: 
            - **LONG**: 绿色霓虹背景 + "BUY LONG" + 确信度 (e.g., "Confidence: 85%")
            - **SHORT**: 红色霓虹背景 + "BUY SHORT" + 确信度
        - **Pattern Info (底部)**: 显示 AI 识别到的形态名称 (e.g., "Bull Flag Breakout")。
      - **交互**: 卡片整体可点击，点击后通过 **Shared Element Transition** 动画无缝展开至 Detail Page（Detail Page 会根据盘前/盘中/盘后/休市显示不同模式）。
- **动态交互逻辑**:
  - **自动置顶 (Auto-Sort)**: 当 AI 算法检测到信号 (Action == 'buy_long' || Action == 'buy_short') 时，该卡片自动以平滑动画 (Layout Animation) 移动到 Grid 的第一个位置。
  - **视觉高亮 (Visual Urgency)**:
    - **信号触发**: 当 AI 检测到 'buy_long' 或 'buy_short' 信号时，卡片边缘出现流动的霓虹光效 (Border Flow)，背景微弱闪烁，模拟"警报"紧迫感。
  - **分析结果复用 (Analysis Reuse)**:
    - **缓存目标**: 当某个 ticker 当天触发过 LLM 分析后，用户从 Tracking Page 点进 Detail Page 时，右侧 AI Copilot 立刻显示该 ticker 的“当日最新分析”，无需等待下一次实时触发。
    - **缓存策略**:
      - 后端为每个 `(symbol, trading_date)` 维护 `latest_analysis_id`（指向当天最新一条 LLM 输出），并对 `analysis_id -> LLMResponse` 做 TTL 缓存。
      - 前端同时将 `analysis_id` 与响应体写入 localStorage（作为短期离线缓存/加速），并在 Detail Page 首屏优先读取展示。
    - **路由承载**: Tracking Page 进入 Detail Page 时，在 URL 上附带 `analysis_id`（如 `/tracking/META?analysis_id=...`），Detail Page 用该 id 直接拉取/展示缓存分析。
- **市场状态与关市处理 (Market Session Handling)**:
  - **状态定义**:
    - **Pre-Market (盘前)**: 开盘前的延长交易时段。
    - **Regular (盘中)**: 正常交易时段。
    - **After-Hours (盘后)**: 收盘后的延长交易时段。
    - **Closed (休市)**: 周末/节假日/当日收盘后至次日盘前的非交易时段。
  - **用户如何被告知当前状态**:
    - **顶部 Market Status Pill**: 始终可见，作为“你现在看到的数据属于哪个时段”的单一真相来源。
    - **状态切换 Toast**: 从盘前→盘中→盘后→休市时弹出短 Toast（例如“已开盘：切换到盘中模式”）。
    - **颜色与语义一致**: Regular 用高亮绿、Pre/After 用蓝紫过渡、Closed 用低饱和灰，降低误判。
  - **不同状态下的页面显示差异**:
    - **Regular (盘中)**:
      - **默认模式**: 全速实时刷新 + AI 信号高亮 + 自动置顶。
      - **Mini-CandleChart**: 使用 1m bars，并在图表右上角显示“LIVE”标记。
    - **Pre-Market / After-Hours (盘前/盘后)**:
      - **视觉提醒**: 顶部加一行细 Banner（“延长交易时段：流动性更薄，滑点风险更高”）。
      - **卡片信息**: 在价格旁增加小标签“PRE/POST”，并展示该时段的涨跌幅（与盘中涨跌幅区分）。
      - **信号策略**: 仍可高亮 buy_long/buy_short，但在 Signal Badge 上附加“EXT”标识，提示信号发生在延长时段。
    - **Closed (休市)**:
      - **主视觉降噪**: 关闭霓虹警报特效与自动置顶，避免“假实时感”；卡片进入“静默模式”。
      - **卡片信息**: 显示 Last Close、当日/前一交易日关键价位摘要（如 Prev High/Low、Close），Mini-CandleChart 切换到“最后交易日盘中缩略图”。
      - **用户引导**: 顶部显示“市场休市”+“距离下一次开盘”倒计时，并提供一键切换到 Replay Console 进行复盘。
  - **通知策略 (Notifications)**:
    - **盘中信号**: 当 buy_long/buy_short 触发时，除卡片高亮外，可触发浏览器通知/声音提示（用户可在设置中关闭）。
    - **休市信号处理**: 休市期间不推送“买入/卖出”类提示；只推送“开盘提醒/自选股异动回顾”类低频通知。
- **技术实现**:
  - **数据流**: 前端维护一个 `tickers` 数组，通过 WebSocket 订阅这 10 个 symbol 的实时 bar 数据。
  - **动画库**: 使用 `Framer Motion` 实现卡片排序的平滑重排 (Reordering) 和进入/退出动画。
  - **组件复用**: `StockSignalCard` 内部复用 `CandleCard` 的绘图逻辑，但简化坐标轴和工具栏，专注于形态展示。

#### C. 股票详情页 (Ticker Detail Page)
- **页面目的**: 聚焦单一 Ticker 的更大 K 线视图与 AI 解读，作为从 Tracking Page 的“发现信号”到“确认与决策”的承接页。
- **布局结构**:
  - **顶部信息条**:
    - **Back**: 返回 Tracking Page。
    - **Symbol + Price**: 股票代码与最新价格（或 last close）。
    - **Market Status Pill + Countdown**: 显示当前 session 与距下一次开/收盘倒计时。
  - **主区域**:
    - **左侧：大图表 (CandleCard)**: 显示更完整的 1m bars，叠加 EMA/关键点位。
    - **右侧：AI Copilot**: 展示 LLM 解释与操作建议，并在进入页面时自动加载“当日最新分析”（复用 tracking 的 analysis_id 或后端 `latest_analysis_id`，避免重复推理）。
- **进入 Detail Page 时的分析加载逻辑**:
  - **优先级**:
    1) URL query 中的 `analysis_id`（来自 Tracking Page 点击进入，确保“所见即所得”）
    2) 本地 localStorage 缓存的 `analysis_id -> analysis`（秒开体验）
    3) 后端接口 `/api/analysis/latest?symbol=...&date=...` 返回 `latest_analysis_id`（兜底，确保跨设备/刷新也能取到当日最新）
  - **显示行为**:
    - 若存在缓存分析：进入页立即渲染成一条 AI 消息气泡（时间戳为分析生成时间），并在后续实时流触发新分析时追加更新。
- **不同市场状态下的 Detail Page 显示差异**:
  - **Regular (盘中)**:
    - **模式**: 全实时模式（WS 持续更新 bars + AI 可在信号触发时自动推送）。
    - **图表标识**: 图表角落显示 “LIVE”；价格与涨跌幅按盘中实时刷新。
    - **AI 提示语**: 以“实时监控 + 触发即解释”为主，强调执行风险与止损位。
  - **Pre-Market / After-Hours (盘前/盘后)**:
    - **视觉提醒**: 顶部显示细 Banner（“延长交易时段：流动性更薄，滑点风险更高”）。
    - **图表标识**: 显示 “PRE/POST” 标签；涨跌幅口径标注为“延长时段变动”，避免与盘中混淆。
    - **AI 行为**: 允许继续推送，但在输出中附加 “EXT” 语义提示，强调信号可靠性与成交不确定性。
  - **Closed (休市)**:
    - **静态模式**: Detail Page 进入“只读/静默模式”，图表与 AI 对话框不做任何实时更新（不建立 WS 连接，不触发自动分析）。
    - **页面内容**:
      - **Market Closed 卡片**: 显示“市场休市”、下一次开盘时间/倒计时。
      - **Last Session Summary**: 展示上一交易日的 O/H/L/C、涨跌幅、关键事件（如 gap、单日振幅）。
      - **Replay CTA**: 提供一键跳转 Replay Console（建议默认带上当前 symbol）。
    - **用户预期管理**: 在图表区域显示“休市：图表已冻结在最后交易时段”说明，避免用户误以为系统故障。

#### D. K线回放控制台 (Replay Console)
- **功能**: 沉浸式历史行情复盘与 AI 交互。
- **布局结构**:
  - **1. 顶部控制栏 (Top Command Bar)**:
    - **Ticker Search**: 玻璃质感搜索框，支持模糊匹配股票代码。
    - **Time Selector**: 未来主义风格的时间/日期选择器，精确选择回放起点。
    - **Playback Controls**: 
      - `Start/Stop`: 播放/暂停回放流。图标带呼吸灯效果。
      - `Reset`: 清空当前画布与对话记忆，重置至初始状态。
  - **2. 主工作区 (Main Workspace) - 分屏设计**:
    - **左侧：行情视窗 (Market View)**:
      - **K线图表**: 黑色底色，K线采用高亮红绿配色。
      - **实时指标**: 动态叠加 EMA, Bollinger Bands, Support/Resistance Levels。
      - **交互**: 支持缩放、拖拽，随回放进度自动滚动。
      - **关键 K 线特效 (Key Bar Highlight)**:
        - **视觉交互**: 针对算法识别的"关键柱"（Key Bar），施加瞬时视觉增强。
        - **动画设计**: 柱体执行单次"高亮闪烁"（Flash）或"呼吸"效果，边缘泛起霓虹光晕（Neon Glow）。
        - **持续时间**: 动画持续约 1.5 秒后自动消失，K 线恢复标准红/绿状态，确保图表长期整洁。
    - **右侧：AI 智囊 (AI Copilot)**:
      - **对话流**: 玻璃面板容器。AI 的分析结果以对话气泡形式呈现，模拟打字机效果。
      - **内容**: 实时同步显示对左侧当前 K 线形态的分析、趋势预测及操作建议。
      - **动态反馈**: 当检测到关键信号时，窗口边缘闪烁特定颜色（如金色表示高确信度机会）。

#### E. 设置页 (Settings)
- **页面目的**: 提供全局设置入口（后续可扩展更多选项）；当前仅控制是否开启 Alpaca paper trading 自动下单模式。
- **进入方式**:
  - **全局入口**: Navigation Bar 右侧提供 Settings 图标按钮，任意页面可一键打开。
  - **快捷返回**: 关闭 Settings 后回到打开前的页面与滚动位置。
- **呈现方式**: 采用右侧弹出式 Settings Drawer（非跳转页面），避免中断用户正在看的行情/回放。
- **布局结构**:
  - **Drawer 容器**: 桌面端宽度 420px，移动端全屏；顶部固定栏包含标题“设置”和关闭按钮。
  - **关闭交互**: 右上角关闭按钮、Esc 键、点击遮罩层均可关闭。
  - **设置卡片 (Settings Card)**: 玻璃拟态面板（圆角 16px，内边距 20px，轻微发光描边）。
    - **标题**: “交易设置”。
    - **唯一设置项：Paper Trading 自动下单 (Switch)**:
      - **标题文案**: “启用 Alpaca Paper Trading 自动下单”。
      - **说明文案**: “开启后，系统会根据 LLM 的 buy_long/buy_short/close 建议自动提交 Alpaca paper trading 的股票与期权订单（非实盘）。”
      - **默认值**: 关闭。
      - **开关规格**: 高 28px、宽 48px；关闭态轨道 #2A2A2A、开启态轨道 #2DFFB3；thumb 20px，开启态轻微外发光。
      - **状态提示**:
        - 关闭：灰色文案 “当前：仅提示信号，不会下单”。
        - 开启：绿色文案 “当前：自动下 Alpaca paper trading 订单”。
      - **安全交互**:
        - 从关闭切到开启时弹出确认弹窗（玻璃拟态），主按钮“确认开启”，次按钮“取消”。
        - 弹窗文案明确提示“这将自动提交 paper trading 订单”。
      - **可访问性**: 使用原生 switch 语义；支持键盘 Space/Enter 切换；清晰 focus ring（2px 霓虹蓝外描边）。

## 6. 技术实现细节 (Technical Details)

### 6.1 技术栈 (Tech Stack)
- **Frontend**:
  - **Framework**: React.js / Next.js
  - **Charting Library**: Lightweight Charts (by TradingView) - 高性能，适合实时金融图表。
  - **UI Library**: Tailwind CSS + ShadcnUI
  - **State Management**: Zustand / React Query
- **Backend**:
  - **Language**: Python 3.10+
  - **Web Framework**: FastAPI (高性能异步框架，适合 WebSocket)。
  - **Task Queue**: Celery + Redis (处理耗时的 AI 推理任务)。
  - **Data Processing**: Pandas / TA-Lib (技术指标计算)。
- **Database**:
  - **Time-series**: In-memory (Pandas DataFrame) for realtime window; Optional: TimescaleDB / InfluxDB for persistence.
  - **Cache**: Redis (Strategy Cache, Quant Signals).
  - **Trades & Events**: SQLite（后端本地文件）用于落库 `trades` 与 `trade_events`（作为交易“事实账本”与 UI 时间线数据源）。
