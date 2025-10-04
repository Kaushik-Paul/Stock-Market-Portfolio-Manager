# Stock Market Portfolio Manager

[![Live Website](https://img.shields.io/badge/Live_Website-6c63ff?logo=rocket&logoColor=white&labelColor=5a52d3)](https://projects.kaushikpaul.pp.ua/stock-market-agent)

An AI-driven, educational stock trading simulator with four autonomous trader personas. Watch them research, make decisions, execute trades, and track portfolio performance in a modern Gradio dashboard.

This project showcases:
- Multiple AI traders with distinct strategies
- Periodic research/trading loops
- MCP-based tools for accounts, market data, email, and research
- Persistent state and logs with SQLite
- A polished, responsive UI with live charts and tables

## Live Demo
- Visit: https://projects.kaushikpaul.pp.ua/stock-market-agent

## Features
- __Four autonomous traders__: Warren (Value), George (Macro), Ray (Systematic), Cathie (Crypto ETFs)
- __Gradio dashboard__: Live P&L, holdings, transactions, and log streams
- __Reset anytime__: Reinitialize all traders and strategies in one click
- __Timed sessions__: Auto-stop guard to cap long runs
- __Persistent state__: SQLite database under `main/memory/`
- __MCP tooling__:
  - Accounts Server: trade, balances, holdings (see `main/mcp_servers/accounts_server.py`)
  - Market Server: share price lookup with Polygon fallback (see `main/mcp_servers/market_server.py`)
  - Email Server: send Mailjet emails (see `main/mcp_servers/email_server.py`)
  - Research stack: fetch, Brave Search, and per-trader memory

## Architecture Overview
- __Entrypoint__: `main/app.py` (launches Gradio UI)
- __UI__: 
  - `main/gradio_ui/builder.py` (page, events, timers)
  - `main/gradio_ui/views.py` (trader cards, plots, dataframes)
  - `main/gradio_ui/styles.py` (modern styling + dark mode)
- __Trading loop__:
  - `main/trading/trading_floor.py` (scheduler, cooperative stop, model selection)
  - `main/trading/traders.py` (Agent setup, researcher tool, run cycle)
- __Accounts & persistence__:
  - `main/accounts/accounts.py` (account model, buy/sell, PnL)
  - `main/utils/database.py` (SQLite: accounts, logs, market cache)
- __Market data__:
  - `main/markets/market.py` (Polygon REST, EOD/min snapshot, random fallback)
- __Prompts & strategies__:
  - `main/prompts/templates.py` (trader/researcher instructions)
  - `main/prompts/reset.py` (default strategies for 4 traders)
- __MCP servers__:
  - `main/mcp_servers/*.py` (accounts, market, email)
  - `main/mcp_servers/mcp_params.py` (tooling config per trader/researcher)
- __Config & utilities__:
  - `main/utils/constants.py` (schedule, model names)
  - `main/utils/tracers.py` (Agents tracing -> SQLite logs)
  - `main/utils/util.py` (UI CSS/JS helpers)

## Prerequisites
- Python 3.10–3.12
- pip or uv (recommended)
- Node.js and npx (for MCP servers used by research; see `main/mcp_servers/mcp_params.py`)
- Optional external services:
  - Polygon API (live or EOD prices)
  - Brave Search API (research)
  - Mailjet API (email notifications)

## Quick Start

### 1) Clone
```bash
git clone https://github.com/Kaushik-Paul/Stock-Market-Portfolio-Manager.git
cd Stock-Market-Portfolio-Manager
```

### 2) (Optional) Create a virtual environment
```bash
python3 -m venv .venv
source .venv/bin/activate    # Windows: .venv\Scripts\activate
```

### 3) Install dependencies
- Option A — uv (recommended)
```bash
# install uv if needed
curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH="$HOME/.local/bin:$PATH"

uv sync
```

- Option B — pip
```bash
pip install -r requirements.txt
```

### 4) Create a .env file (at repo root)
These are the environment variables the code reads. Only set what you actually use.

```ini
# ——— Market Data (Polygon) ———
# If absent, app falls back to pseudo-random prices for symbols.
POLYGON_API_KEY=your_polygon_key
# one of: "" (unset), "paid", "realtime"
POLYGON_PLAN=paid

# ——— Research (Brave Search MCP) ———
# Enables @modelcontextprotocol/server-brave-search via npx.
BRAVE_API_KEY=your_brave_api_key

# ——— Email (Mailjet) ———
MAILJET_API_KEY=your_mailjet_key
MAILJET_API_SECRET=your_mailjet_secret

# Note: Model selection is done via LiteLLM-style names in `main/utils/constants.py`.
# If you use an OpenRouter-backed model with LiteLLM, set provider vars as needed in your environment.
# Example (only if your LiteLLM setup requires it):
# OPENROUTER_API_KEY=your_openrouter_key
# OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
```

### 5) Run locally
```bash
python -m main.app
# or
python main/app.py
```
Open the printed local URL (e.g., http://127.0.0.1:7860).

## Usage
1. Click "Run" to start a session (up to 10 mins by default).
2. Watch each trader's live portfolio value, holdings, transactions, and logs.
3. Click "Stop" to end early.
4. Click "Reset" to reinitialize all accounts with default strategies from `main/prompts/reset.py`.

## Configuration

- __Scheduling & models__: `main/utils/constants.py`
  - `RUN_EVERY_N_SECONDS` — cadence for trading loop
  - `RUN_EVEN_WHEN_MARKET_IS_CLOSED` — run regardless of market hours
  - `USE_MANY_MODELS` — toggle per-trader model names vs a default
  - `MANY_MODELS_NAMES`, `MANY_MODELS_SHORT_NAMES`, `DEFAULT_MODEL_NAME`
- __Trader strategies__: `main/prompts/reset.py`
- __Trading loop__: `main/trading/trading_floor.py`
- __MCP servers__: `main/mcp_servers/mcp_params.py`
  - Traders use: Accounts, Email, Market servers
  - Researcher uses: Fetch, Brave Search, and per-trader memory
  - Researcher memory path: `file:./main/memory/{name}.db`
- __Market data__: `main/markets/market.py`
  - If `POLYGON_API_KEY` is set, uses Polygon (EOD for free, min snapshots if paid/realtime)
  - If not set or fails, falls back to a random price for robustness
- __State & logs__: `main/utils/database.py`
  - DB file: `main/memory/accounts.memory`
  - Tables: `accounts`, `logs`, `market`
  - Logs stream into the UI cards

## Deployment

- __Live Site__: https://projects.kaushikpaul.pp.ua/stock-market-agent
- __General guidance__:
  - Set environment variables for any external tools you enable
  - Run `python -m main.app` under a process manager (systemd, pm2, supervisor) or a container
  - Ensure Node.js/npx present if research MCP servers are enabled
  - Persist `main/memory/` for state across restarts
  - Expose the Gradio service behind a reverse proxy (e.g., Nginx) with TLS

## Troubleshooting
- __No Polygon key__: Prices fall back to random; set `POLYGON_API_KEY` for real data.
- __Brave Search failures__: Set `BRAVE_API_KEY` and ensure `npx` is available.
- __Email errors__: Verify `MAILJET_API_KEY` and `MAILJET_API_SECRET`. Sender/recipient are configured in `main/mcp_servers/email_server.py`.
- __Node/npx not found__: Install Node.js and ensure `npx` is on PATH.
- __uv/uvx warnings__: `uvx` is only ensured in hosted environments (when `SPACE_ID` is present). Locally you can ignore.

## Tech Stack
- __Python__: 3.10–3.12
- __UI__: Gradio 5, Plotly, pandas
- __Agents & Tools__: openai-agents, LiteLLM-style model names, MCP (FastMCP, stdio clients)
- __Data__: Polygon API client (optional)
- __Infra__: SQLite for state/logs, dotenv for config

## Security & Privacy
- Do not commit `.env` or credentials.
- Use least-privilege API keys.
- Logs and state are stored locally under `main/memory/`.

## License
MIT — see `LICENSE`.

## Acknowledgements
- Polygon, Brave Search MCP, MCP community
- Gradio, Plotly
- openai-agents and related tooling

## Financial Disclaimer
Do not make financial decisions based on the AI agents' recommendations. This application is for educational and informational purposes only. Always do your own market research. The author of this project is not responsible for any financial loss if used.
