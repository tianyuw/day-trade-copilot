# 项目提案：Day Trade Copilot (v1.3)

## 1. 项目概览
Day Trade Copilot 是一个智能股票监控系统，旨在通过实时分析 1 分钟 K 线图来辅助交易者。系统采用**“量化筛选 + AI 验证”**的双层架构：首先利用高效的多种量化指标算法实时扫描潜在的突破点位，一旦检测到信号，立即调用 **Gemini 3 Pro** 的多模态能力进行深度验证，确认突破的真实性和有效性，从而提供高胜率的可执行交易信号。

*v1.3 版本核心变更：引入了 Pine Script 量化算法作为一级过滤器，将 AI 的角色从“每分钟巡检”转变为“按需验证”，显著降低成本并提高信号质量。*

## 2. 核心工作流

### 2.1 第一层：量化筛选 (Quant Filter)
- **核心算法**: 基于 Pine Script 逻辑的多种量化策略组合。
  - **逻辑**: 综合计算价格、成交量及波动率等统计特征，识别潜在的趋势突破信号。（具体算法细节见后文专章）
- **运行机制**: 对给定的股票列表，系统实时运行该算法，持续监控每一分钟的 K 线收盘状态。
- **触发**: 只有当算法检测到明确的“潜在突破信号”时，才会激活第二层 AI 验证。

### 2.2 第二层：AI 深度验证 (AI Verification)
一旦量化层发出信号，系统立即向 **Gemini 3 Pro** 发起请求，进行多模态验证。
- **输入数据**:
  1. **市场数据**: 过去 30 分钟的 OHLCV 序列。
  2. **技术指标**: 过去 30 分钟的 EMA9, EMA21, Volume, VWAP, Bollinger Bands 序列。
  3. **期权链数据 (Option Chain)**: 当前时刻所有相关期权合约的完整数据快照（包括 Strike Price, Expiration Date, Bid/Ask, Volume, Open Interest, Delta, Gamma, Theta, Vega）。这将使 LLM 能够基于真实的流动性和定价来选择最佳合约。
  4. **视觉数据**: 生成的当日盘中完整的 K 线图图片，叠加指标、压力位（Resistance）和支撑位（Support）及量化算法标记出的突破点位。
- **验证任务**: 确认该点位是否是合适的0DTE买点，买入的确信度有多大。同时给出具体的理由。也给出具体的操作计划，计划应该包括: 买call还是put，行权价，期权止损价格，止盈价格。

### 2.3 结构化预测输出与风控
LLM 必须返回严格的 **JSON 格式** 数据。
**示例 JSON Payload**:
```json
{
  "is_valid_buy_point": true,
  "confidence": 0.92,
  "reasoning": "Volume surge confirms the Z-score breakout; price is closing above upper Bollinger Band.",
  "action_plan": {
    "option_type": "call",
    "strike_price": 346.00,
    "option_stop_loss": 1.20,
    "option_take_profit": 2.50,
    "underlying_trigger_price": 345.50
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

#### B. K线回放控制台 (Replay Console)
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
    - **右侧：AI 智囊 (AI Copilot)**:
      - **对话流**: 玻璃面板容器。AI 的分析结果以对话气泡形式呈现，模拟打字机效果。
      - **内容**: 实时同步显示对左侧当前 K 线形态的分析、趋势预测及操作建议。
      - **动态反馈**: 当检测到关键信号时，窗口边缘闪烁特定颜色（如金色表示高确信度机会）。

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

