# 项目提案：Day Trade Copilot (v1.4 - Detailed Specification)

## 1. 项目概览 (Executive Summary)
Day Trade Copilot 是一个专为日内交易者（Day Trader）设计的智能辅助系统，旨在捕捉高胜率的动量突破（Momentum Breakout）机会。系统融合了传统量化金融的筛选效率与生成式 AI (Gemini 3 Pro) 的深度推理能力，构建了一个“**量化筛选 (L1) -> AI 验证 (L2) -> 状态追踪 (L3)**”的闭环系统。

*   **核心价值**: 解决人工盯盘精力有限、情绪干扰决策、执行不够果断的三大痛点。
*   **v1.4 核心升级**: 引入**全链路数据库持久化 (End-to-End Persistence)**，利用 SQLite 作为单一事实来源 (Source of Truth)，彻底解决了系统重启、网络重连导致的状态丢失问题，确保交易生命周期的完整性与可追溯性。

---

## 2. 核心工作流与算法细节 (Core Workflow & Algorithms)

### 2.1 第一层：量化筛选 (Level 1: Quant Filter)
量化层充当系统的“守门员”，负责从实时行情流中过滤掉 99% 的无效波动，仅将具备统计显著性的潜在机会输送给 AI。

*   **核心算法**: `ZScoreMomentum` (Z-Score 动量策略)
    *   **设计理念**: 寻找价格偏离度（Z-Score）的剧烈变化（Momentum），识别趋势启动的瞬间。
    *   **数据基准**: 使用过去 **30 个交易日** 的日线数据 (Daily Bars) 计算该标的的统计特征：
        *   `daily_mean`: 30 日收盘价均值。
        *   `daily_std`: 30 日收盘价标准差。
    *   **实时计算**: 对每一根 1 分钟 K 线 (Realtime 1m Bar)：
        1.  计算当前价格的标准化得分: `raw_z_score = (close_price - daily_mean) / daily_std`。
        2.  对 Z-Score 进行平滑处理，计算 5 周期指数移动平均: `z_score_ema5 = EMA(raw_z_score, span=5)`。
        3.  计算动量差值 (Velocity): `z_score_diff = z_score_ema5_current - z_score_ema5_prev`。
    *   **信号触发阈值**:
        *   **LONG (做多)**: 当 `z_score_diff > 0.006` 时触发。
        *   **SHORT (做空)**: 当 `z_score_diff < -0.006` 时触发。

### 2.2 第二层：AI 深度验证 (Level 2: AI Verification)
一旦量化层发出信号，系统生成一个包含多模态上下文的 Prompt，调用 **Gemini 3 Flash Preview** 进行深度推理。

*   **Prompt 结构设计**:
    1.  **Persona (角色设定)**: "你是一位拥有 20 年经验的华尔街资深日内交易员，擅长 0DTE 期权与动量突破交易..."
    2.  **Market Context (市场数据)**:
        *   **OHLCV Data**: 过去 300 分钟的 1m 数据摘要。
        *   **Indicators**: 最新一根 K 线的 EMA9, EMA21, VWAP, Bollinger Bands (Upper/Lower/Mid), MACD (Line/Signal/Hist)。
        *   **Market Sentiment**: 大盘指数 (SPY/QQQ) 的当前趋势（用于顺势过滤）。
    3.  **Visual Context (视觉图表)**:
        *   系统动态生成一张 matplotlib 图片，包含 K 线、均线系统、支撑压力位，直观展示形态。
    4.  **Option Chain (期权链)**:
        *   提供最近到期日 (Nearest Expiration) 的 ATM (平值) 及上下 5 档 Strike 的 Call/Put 报价 (Bid/Ask/Last)。

*   **LLM 响应 Schema (Structured Output)**:
    系统强制要求 LLM 返回严格的 JSON 格式：
    ```json
    {
      "action": "buy_long | buy_short | ignore | follow_up | check_when_condition_meet",
      "confidence": 0.85, // 置信度 0.0 - 1.0
      "reasoning": "价格强势突破 VWAP，伴随 RVOL > 2.0，且 QQQ 同步拉升...",
      "pattern_name": "Bull Flag Breakout",
      "watch_condition": { // 仅 action=check_when_condition_meet 时非空
         "trigger_price": 150.5,
         "direction": "above"
      },
      "trade_plan": { // 仅 action=buy_* 时非空
         "direction": "long",
         "option": { "symbol": "NVDA240126C00500000", "strike": 500, "expiration": "2024-01-26", "right": "call" },
         "contracts": 1,
         "risk": {
            "stop_loss_premium": 0.85, // 期权止损价
            "time_stop_minutes": 20    // 时间止损
         },
         "take_profit_premium": 2.5    // 目标止盈价
      }
    }
    ```

### 2.3 第三层：交易编排与状态机 (Level 3: Orchestration FSM)
系统通过一个严密的有限状态机 (Finite State Machine) 管理每个 Symbol 的交易生命周期。

*   **状态流转图**:
    1.  **SCAN (扫描态)**: 默认状态。持续运行 `ZScoreMomentum`。
        *   *Trigger*: `z_score_diff` 突破阈值 -> 转入 `ENTRY_CANDIDATE`。
    2.  **ENTRY_CANDIDATE (候选态)**: 锁定当前 Bar，准备 AI 请求。
        *   *Action*: 构建 Prompt，调用 AI。 -> 转入 `AI_VERIFY`。
    3.  **AI_VERIFY (验证态)**: 等待 AI 响应。
        *   *Result = buy_***: -> 转入 `PLAN_READY`。
        *   *Result = ignore*: -> 回到 `SCAN`。
        *   *Result = follow_up*: -> 转入 `FOLLOW_UP_PENDING`。
        *   *Result = check_condition*: -> 转入 `WATCH_PENDING`。
    4.  **FOLLOW_UP_PENDING (跟进态)**:
        *   *Action*: 等待**下一根 1m Bar 收盘**。
        *   *Trigger*: Bar Close -> 自动回到 `AI_VERIFY` (带上最新数据再次验证)。
    5.  **WATCH_PENDING (观察态)**:
        *   *Action*: 本地监控价格是否触及 `trigger_price`。
        *   *Trigger*: 价格触及 -> 立即回到 `AI_VERIFY`。
        *   *Trigger*: 超过 `expiry_minutes` 未触及 -> 回到 `SCAN`。
    6.  **PLAN_READY (就绪态)**: 交易计划已生成。
        *   *Action*: 检查 `Auto Trading` 开关。
        *   *True*: -> 转入 `ENTRY_PENDING` (提交订单)。
        *   *False*: -> 仅 UI 提示，回到 `SCAN`。
    7.  **ENTRY_PENDING (入场中)**:
        *   *Action*: 提交 Alpaca Limit Order (Price = Ask + 0.03)。
        *   *Trigger*: Order Filled -> 转入 `IN_POSITION`。
        *   *Trigger*: Timeout (1 min) -> Cancel Order -> 回到 `SCAN`。
    8.  **IN_POSITION (持仓中)**:
        *   *Action*: 每分钟 K 线收盘 -> 优先检查 **Hard Exit** (硬止损/止盈) -> 若未触发则调用 AI 进行 **Position Management** (持仓管理)。
        *   *Hard Exit Logic*:
            *   若 Option Bid Price <= Stop Loss Premium -> 立即触发 `close_all` (Simulated 模式下直接输出平仓信号；Paper/Live 需后续实现自动下单)。
            *   若 Option Bid Price >= Take Profit Premium -> 立即触发 `close_all`。
            *   *Trigger*: 触发硬止损/止盈后，立即转入 `SCAN` 状态，并从**当前 K 线**开始重新寻找入场机会 (AI_VERIFY)。
        *   *AI Logic*: 若未触发硬止损/止盈，AI 决定 `hold` / `close` / `adjust_stop`。
        *   *Trigger*: AI 决定 Close 或 止损触发 -> 转入 `EXIT_PENDING` (或直接平仓回到 `SCAN`)。
    9.  **EXIT_PENDING (离场中)**:
        *   *Action*: 提交 Alpaca Market Order (Close Position)。
        *   *Trigger*: Order Filled (Contracts=0) -> 转入 `CLOSED`。
    10. **CLOSED (结束态)**:
        *   *Action*: 结算 PnL，记录日志。 -> 回到 `SCAN`。

---

## 3. 数据库持久化架构 (Persistence Architecture)

为了保证系统健壮性，v1.4 引入了基于 **SQLite** 的全量持久化方案。

### 3.1 数据库 Schema 定义

#### A. `trades` 表 (活跃交易状态)
存储当前系统的“状态快照”。这是恢复 `IN_POSITION` 高亮的关键。
```sql
CREATE TABLE trades (
    trade_id TEXT PRIMARY KEY,      -- UUID, e.g., "trd_..."
    symbol TEXT NOT NULL,           -- e.g., "NVDA"
    state TEXT NOT NULL,            -- FSM State: "IN_POSITION", "SCAN", etc.
    mode TEXT DEFAULT 'realtime',   -- "realtime" | "replay"
    execution TEXT DEFAULT 'paper', -- "paper" | "simulated"
    
    -- 仓位详情
    direction TEXT,                 -- "long" | "short"
    option_symbol TEXT,             -- Alpaca OCC Symbol
    contracts_total INTEGER,        -- 初始手数
    contracts_remaining INTEGER,    -- 剩余手数
    entry_price REAL,               -- 标的入场价
    entry_premium REAL,             -- 期权入场权利金
    entry_time TEXT,                -- ISO8601 Timestamp
    
    -- 动态风控参数 (JSON)
    extra_json TEXT,                -- 存储 risk (stop_loss, take_profit) 等动态调整参数

    -- 结算信息 (仅 CLOSED 后完整)
    exit_premium REAL,
    exit_time TEXT,
    pnl_realized REAL,              -- 已实现盈亏 (USD)
    pnl_percent REAL,               -- 盈亏百分比
    
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
);
-- 索引
CREATE INDEX idx_trades_symbol_state ON trades(symbol, state);
```

#### B. `trade_events` 表 (全量事件日志)
存储系统发生的所有动作，用于 Detail 页的时间线回放。
```sql
CREATE TABLE trade_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    trade_id TEXT,                  -- 关联的主 Trade (可选，SCAN 阶段可能无 trade_id)
    symbol TEXT NOT NULL,           -- 冗余字段，便于快速查询
    event_type TEXT NOT NULL,       -- 枚举值 (见下文)
    timestamp TEXT NOT NULL,        -- 事件发生时间
    bar_time TEXT,                  -- 关联的 K 线时间
    payload_json TEXT,              -- 完整的 JSON 数据包 (Analysis Result, Order Info)
    
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
-- 索引
CREATE INDEX idx_events_symbol_time ON trade_events(symbol, timestamp);
```

### 3.2 关键 Event Types 枚举
*   `signal_detected`: 量化引擎触发信号。
*   `ai_verify_requested`: 向 LLM 发送请求。
*   `llm_analysis_result`: LLM 返回分析结果 (包含 confidence, reasoning, plan)。
*   `watch_condition_set`: 设置价格监视器。
*   `watch_condition_triggered`: 价格触及监视器。
*   `order_submitted`: 向 Alpaca 提交订单。
*   `order_filled`: 订单成交。
*   `position_mgmt_requested`: 发起持仓管理请求。
*   `position_mgmt_result`: 持仓管理结果 (hold/close)。
*   `risk_triggered`: 硬风控触发 (止损/时间到期)。

### 3.3 状态恢复机制 (Recovery Mechanism)
当后端服务重启或 WebSocket 重新连接时：
1.  **Frontend**: 发起 WebSocket 连接。
2.  **Backend (WebSocket Endpoint)**:同时解析 `extra_json` 恢复最新的止损/止盈参数，确保硬风控 (Hard Exit) 逻辑重启后立即生效。
    *   接收连接 (`connect`).
    *   **DB Query**: `SELECT * FROM trades WHERE state IN ('IN_POSITION', 'ENTRY_PENDING', 'EXIT_PENDING')`.
    *   **Session Restore**: 为查询到的每个 Symbol 重新初始化内存中的 `SymbolSession` 对象，并将状态机指针拨到对应的 `state`，加载 `trade_id` 和 `contracts` 信息。
    *   **Push State**: 立即通过 WebSocket 向前端推送最新的 `state` 消息。
3.  **Frontend**: 接收到 `state` 消息，UI 立即将对应卡片高亮显示，并恢复“持仓中”的 Dashboard 视图。

---

## 4. 用户界面交互细节 (UI/UX Specifications)

### 4.1 实时追踪页 (Tracking Page)
*   **设计目标**: 提供“上帝视角”，让交易者能一眼监控所有关注标的的状态，并优先处理高价值信息。
*   **核心功能区域**:
    *   **Dashboard Grid**: 采用响应式网格布局，根据屏幕宽度自适应每行显示的卡片数量。
    *   **Smart Ticker Card (智能卡片)**: 每个卡片是一个独立的信息单元，包含：
        *   **头部**: 标的代码 (Symbol)、当前价格、日内涨跌幅 (绿涨红跌)。
        *   **状态栏**: 动态 Badge 显示当前 FSM 状态 (如 `SCAN`, `AI_VERIFY`, `IN_POSITION`)。
        *   **迷你图表**: 显示最近 2 小时的价格走势 Sparkline，辅助判断短期趋势。

*   **智能交互 (Smart Interaction)**:
    *   **自动优先级排序 (Auto-Sort)**: 
        *   **Tier 1 (最高)**: `IN_POSITION` (持仓中) 的卡片会被置顶，方便时刻关注 PnL 和止损。
        *   **其他状态**: `ENTRY_PENDING` / `AI_VERIFY` / `SCAN` 目前不参与排序，保持 Watchlist 的原始顺序。
    *   **平滑动画**: 使用 `Framer Motion` 实现卡片位置交换的平滑过渡，避免突兀跳变造成视觉干扰。
*   **视觉信号系统 (Visual Signals)**:
    *   **呼吸灯 (Pulse)**: 当状态为 `IN_POSITION` 时，卡片背景呈现绿色呼吸效果，提示当前正在持仓中。

*   **非盘中态 (Off-Hours State，仅实时模式触发)**:
    *   **适用范围**: 本项目只针对 **盘中交易 (Regular Trading Hours, RTH)**，因此 **盘前 / 盘后 / 休市** 统一使用同一套 UI 样式与信息层级。
    *   **触发条件**: URL 无 `dev=true` 且当前时间不在 RTH（包含盘前、盘后、周末、节假日）。
    *   **页面级提示 (Global Banner)**:
        *   位置：页面顶部（Header 下方），固定展示，不随滚动消失。
        *   文案：`Off Hours`（或按阶段展示 `Pre-market` / `After-hours` / `Closed`，但视觉样式保持一致）+ `Next RTH Open` 时间（同时显示 ET / PT，默认按用户本地时区高亮）。
        *   倒计时：显示 `Next RTH opens in 2d 11h 24m`（默认到分钟）。
        *   视觉：浅琥珀 Warning 语义，避免“错误感”。建议色值：背景 `#FFFBEB`，文本 `#92400E`，描边 `#FDE68A`。
        *   可访问性：倒计时容器使用 `aria-live="polite"`，频率按分钟更新，避免屏幕阅读器刷屏。
    *   **卡片信息层级调整 (Card Content Reframe)**:
        *   状态栏：不再展示 `SCAN/SCANNING` 等“系统正在扫描”的语义；改为 `OFF HOURS`（中性灰 Badge）。
        *   价格字段：统一展示“上一完整 RTH 交易日”基准信息，避免非盘中价格带来的误导：
            *   `Close`：上一交易日收盘价。
            *   `Open→Close %`：上一交易日收盘相对开盘的涨跌百分比（仅这一项作为休市态的主涨跌指标）。
        *   颜色语义：涨为绿、跌为红，但降低饱和度以强调“回顾数据”属性；建议：涨 `#16A34A`，跌 `#DC2626`，中性 `#64748B`。
    *   **迷你图表规则 (Mini Chart Behavior)**:
        *   数据源：只展示“上一完整交易日”的盘中 **5分钟 K 线**（Regular Trading Hours，09:30–16:00 ET / 06:30–13:00 PT），不包含盘前/盘后。
        *   图表标注：右上角小字 `Prev Session · 5m`（替代任何 SCANNING overlay 文案）。
        *   空态：若无上一交易日数据（如新股/数据缺失），图表区域展示简洁占位：`No prior session data`，不显示扫描态文案。
    *   **交互与一致性 (Interaction & Consistency)**:
        *   点击卡片仍进入详情页；详情页图表默认对齐同一“上一交易日盘中 5m”视图，避免列表与详情产生时间错觉。
        *   `dev=true`（回放/开发模式）不进入休市态，继续按回放逻辑展示实时跳动与状态机。

### 4.2 详情页 (Detail Page)
*   **设计目标**: 提供深度分析环境，展示 AI 决策的全过程上下文 (Context) 和推理逻辑。
*   **双栏布局 (Split Layout)**:
    *   **左侧：交互式图表 (Interactive Chart)**:
        *   **TradingView 内核**: 集成 Lightweight Charts，支持缩放、平移。
        *   **自动指标覆盖**: 根据 AI 使用的数据，自动叠加 EMA9, EMA21, VWAP, Bollinger Bands 等指标。
        *   **交易可视化 (Trade Viz)**:
            *   **决策标记 (Markers)**: 在时间轴上标记每一次 AI 分析的时刻（目前仅显示标记，点击高亮功能待实现）。
    *   **右侧：AI 对话流 (AI Stream)**:
        *   **流式输出**: 模拟打字机效果，实时展示 AI 的推理过程 (Reasoning) 和最终决定 (Decision)。
        *   **结构化卡片**: 将 AI 的 JSON 输出渲染为易读的 UI 组件（如“交易计划卡片”、“风险参数卡片”），而不是原始文本。

### 4.3 回放仪表盘 (Replay Dashboard)
*   **设计目标**: 策略验证与复盘神器。允许用户在收盘后“穿越”回历史时刻，重演市场行情。
*   **核心功能**:
    *   **时间控制 (Time Control)**:
        *   **开始时间选择**: 支持精确到分钟的开始时间设置 (PST)。
        *   **播放/暂停**: 随时暂停回放流，以便仔细观察 AI 的决策逻辑。
    *   **沙盒模拟环境 (Sandbox Simulation)**:
        *   **独立状态机**: 回放模式拥有独立的 FSM 实例，不影响实时交易状态。

### 4.4 开发调试模式 (Dev/Replay Mode)
*   **设计目标**: 解决休市期间无法调试实时交互页面的痛点，支持在收盘时间进行全功能开发。
*   **触发方式**: 在 URL 参数中添加 `?dev=true` (例如 `/tracking?dev=true` 或 `/tracking/NVDA?dev=true`)。
*   **核心逻辑**:
    *   **数据源切换**: 自动从 `/ws/realtime` 切换至 `/ws/playback`。
    *   **环境模拟**: 默认从历史活跃交易日（如 2024-01-12）以 **1倍速 (1x)** 实时回放行情数据，确保 K 线跳动和 AI 分析节奏与实盘完全一致。
    *   **休市旁路**: 强制绕过前端的 "Market Closed" 检查，允许在任何时间建立 WebSocket 连接并渲染图表/AI分析。
*   **UI 标识**: 页面顶部显示 "DEV REPLAY (1x)" 黄色呼吸灯标签，明确当前处于模拟环境。


---

## 5. 技术栈与环境 (Tech Stack)

### Backend
*   **Language**: Python 3.10+
*   **Framework**: FastAPI (Async Web Framework)
*   **AI Client**: Google GenAI SDK (Gemini 1.5/3.0)
*   **Database**: SQLite3 (Native)
*   **Data Processing**: Pandas, NumPy, TA-Lib (Technical Analysis)
*   **Task Queue**: Asyncio (Native Coroutines) - 暂不需要 Celery，利用 Python 异步特性处理 IO 密集型任务。

### Frontend
*   **Framework**: Next.js 14 (App Router)
*   **UI Library**: React, Tailwind CSS, ShadcnUI
*   **State Management**: Zustand (Client State), React Query (Server State)
*   **Charting**: TradingView Lightweight Charts
*   **Animation**: Framer Motion
*   **Icons**: Lucide React

### Infrastructure
*   **Market Data**: Alpaca Data API v2 (IEX/SIP)
*   **Trading Execution**: N/A (Current version uses Simulated Paper Trading via internal ledger)

---

## 6. 部署清单 (Deployment Checklist)

1.  **Environment Variables (`.env`)**:
    *   `ALPACA_API_KEY`, `ALPACA_SECRET_KEY` (Paper/Live)
    *   `GEMINI_API_KEY`
    *   `DATABASE_URL` (default: `sqlite:///./trades.db`)
2.  **Database Init**:
    *   系统启动时自动运行 `check_and_migrate_schema()`，确保 `trades.db` 存在且表结构最新。
3.  **Process Management**:
    *   建议使用 `Supervisor` 或 `Docker Compose` 同时守护 Backend (`uvicorn`) 和 Frontend (`next start`)。

---

## 7. Backlog (Future Features)

### 7.1 持仓面板 (Position Panel)
*   **位置**: 实时追踪页 (Tracking Page) - 智能卡片 (Smart Ticker Card)
*   **描述**: 当状态为 `IN_POSITION` 时，卡片展开显示：
    *   持仓数量 (Contracts)
    *   入场价格 (Entry Price)
    *   **实时未实现盈亏 (Unrealized PnL)**: 动态刷新，盈利显示绿色背景，亏损显示红色背景。

### 7.2 高级优先级排序 (Advanced Priority Sorting)
*   **位置**: 实时追踪页 (Tracking Page)
*   **描述**: 扩展当前的 Auto-Sort 逻辑，支持更细粒度的优先级排序：
    *   **Tier 1 (最高)**: `IN_POSITION` (持仓中)。
    *   **Tier 2**: `ENTRY_PENDING` (挂单中) - 等待成交。
    *   **Tier 3**: `AI_VERIFY` (分析中) - 等待 AI 决策。
    *   **Tier 4**: `SCAN` (扫描中) - 默认状态。

### 7.3 视觉信号增强 (Visual Signal Enhancements)
*   **位置**: 实时追踪页 (Tracking Page)
*   **描述**: 增加更多状态的视觉反馈：
    *   **AI 思考中**: 当状态为 `AI_VERIFY` 时，卡片边框呈现黄色呼吸效果。
    *   **高亮闪烁**: 当 AI 输出 `buy` 信号时，卡片瞬间高亮为霓虹绿，并弹出 Notification。
    *   **错误警示**: 当触发硬止损或 API 错误时，卡片显示红色边框并显示错误图标。

### 7.4 增强图表可视化 (Enhanced Chart Visualization)
*   **位置**: 详情页 (Detail Page) - 交互式图表
*   **描述**:
    *   **入场线 (Entry Line)**: 绿色虚线标示 Entry Price。
    *   **止损/止盈线 (SL/TP Lines)**: 红色/绿色区间标示 Stop Loss 和 Take Profit 区域。
    *   **标记交互 (Interactive Markers)**: 点击时间轴上的 AI 分析标记，可高亮右侧对应的聊天记录。

### 7.5 人工干预控制 (Manual Override Controls)
*   **位置**: 详情页 (Detail Page) - 右侧对话流底部
*   **描述**: 提供紧急控制按钮：
    *   **手动平仓 (Close Position)**: 无论 AI 决策如何，强制以市价平仓。
    *   **暂停自动交易 (Pause Auto-Trading)**: 暂停该标的的自动交易逻辑，转为仅监控模式。

### 7.6 增强回放功能 (Enhanced Replay Features)
*   **位置**: 回放仪表盘 (Replay Dashboard)
*   **描述**:
    *   **进度控制 (Timeline Seek)**: 支持进度条拖拽，快速跳转到特定时刻。
    *   **变速播放 (Variable Speed)**: 支持 0.5x - 60x 的多级倍速播放。
    *   **模拟撮合 (Simulated Execution)**: 基于历史 Tick 数据实现真实的限价单/市价单模拟撮合引擎。
    *   **上帝视角 (God Mode)**: 允许在回放时查看“未来”价格走势（半透明显示）。
    *   **复盘报告 (Replay Report)**: 回放结束后自动生成本次回放周期的交易统计报告。
