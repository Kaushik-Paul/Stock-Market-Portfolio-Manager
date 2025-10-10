# Stock Market Portfolio Manager

[![Live Website](https://img.shields.io/badge/Live_Website-6c63ff?logo=rocket&logoColor=white&labelColor=5a52d3)](https://projects.kaushikpaul.co.in/stock-market-agent)

An AI-driven, educational stock trading simulator with four autonomous trader personas. Watch them research, make decisions, execute trades, and track portfolio performance in a modern Gradio dashboard.

This project showcases:
- Multiple AI traders with distinct strategies
- Periodic research/trading loops
- MCP-based tools for accounts, market data, email, and research
- Persistent state and logs with SQLite
- A polished, responsive UI with live charts and tables

## Live Demo
- Visit: https://projects.kaushikpaul.co.in/stock-market-agent

## Features
- __AI-Powered Trading Bots__: Four autonomous traders with unique strategies inspired by famous investors - Warren (Value), George (Macro), Ray (Systematic), and Cathie (Crypto ETFs)
- __Real-time Market Intelligence__: Agents perform live web research using Brave Search to analyze company performance before making trading decisions
- __Professional-Grade Data__: Integrates with Polygon API for real-time and historical market data with automatic fallback to simulated data
- __Interactive Dashboard__: Beautiful Gradio interface with live portfolio tracking, transaction history, and real-time logs
- __Smart Trading Logic__: Each agent makes independent decisions based on technical analysis, news sentiment, and market trends
- __Persistent Performance Tracking__: SQLite database maintains complete trading history and portfolio performance
- __Email Notifications__: Get alerts for important trading events and portfolio milestones via Mailjet
- __Research Capabilities__: Built-in web search and data analysis tools for comprehensive market research
- __Configurable Strategies__: Easily customize trading parameters and risk profiles for each agent
- __No-Code Operation__: Simple web interface with one-click start/stop controls

> ⚠️ **IMPORTANT FINANCIAL DISCLAIMER**  
> This application is for educational and demonstration purposes only. The AI agents' trading decisions are simulated and should not be considered financial advice. The stock market involves substantial risk of loss, and past performance is not indicative of future results.  
>  
> **Never invest money you cannot afford to lose.** Always conduct your own market research and consult with a qualified financial advisor before making any investment decisions. The author of this project is not responsible for any financial loss or damage resulting from the use of this application.

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
- OpenRouter API key (required for AI models)
- Optional external services:
  - Polygon API (for real market data instead of simulated data)
  - Brave Search API (for web research capabilities)
  - Mailjet API (for email notifications)

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
# ——— Required API Keys ———

# OpenRouter API (Required for AI models)
# Get your API key from https://openrouter.ai/keys
OPENROUTER_API_KEY=your_openrouter_key

# ——— Market Data (Polygon) ———
# Get your API key from https://polygon.io/
# If not provided, the app will use simulated market data
POLYGON_API_KEY=your_polygon_key
# Set to "paid" or "realtime" for live market data, or leave empty for EOD data
POLYGON_PLAN=paid

# ——— Research (Brave Search) ———
# Required for web research functionality
# Get your API key from https://api.search.brave.com/app/keys
BRAVE_API_KEY=your_brave_api_key

# ——— Email Notifications (Mailjet) ———
# Optional: For email alerts and notifications
# Get your API keys from https://app.mailjet.com/account/api_keys
MAILJET_API_KEY=your_mailjet_key
MAILJET_API_SECRET=your_mailjet_secret
# Sender and recipient email addresses
FROM_EMAIL=your_sender@example.com
TO_EMAIL=your_recipient@example.com

# ——— Advanced Configuration ———
# Uncomment and set these only if using a custom LiteLLM configuration
# OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
# LITELLM_MODEL=openrouter/your-model-name

# ——— Development Settings ———
# Set to "true" to enable debug logging
DEBUG=false
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

- __Live Site__: https://projects.kaushikpaul.co.in/stock-market-agent
- __General guidance__:
  - Set environment variables for any external tools you enable
  - Run `python -m main.app` under a process manager (systemd, pm2, supervisor) or a container
  - Ensure Node.js/npx present if research MCP servers are enabled
  - Persist `main/memory/` for state across restarts
  - Expose the Gradio service behind a reverse proxy (e.g., Nginx) with TLS

## Troubleshooting
- __No Polygon key__: Prices fall back to random; set `POLYGON_API_KEY` for real data. Free tier provides delayed data.
- __Missing OpenRouter API key__: Get a key from [OpenRouter](https://openrouter.ai/keys) and set `OPENROUTER_API_KEY` in your `.env` file.
- __Model access issues__: Ensure your OpenRouter account has access to the model specified in `main/utils/constants.py`.
- __Brave Search failures__: Set `BRAVE_API_KEY` and ensure `npx` is available. Check your daily quota at [Brave Search API](https://api.search.brave.com/app/brave-usage).
- __Email errors__: Verify `MAILJET_API_KEY` and `MAILJET_API_SECRET`. Check sender/recipient settings in `main/mcp_servers/email_server.py`.
- __Node/npx not found__: Install Node.js (v16+) and ensure `npx` is on your PATH. On Ubuntu/Debian: `sudo apt install nodejs npm`
- __uv/uvx warnings__: `uvx` is only ensured in hosted environments. For local development, you can safely ignore these warnings.
- __Port conflicts__: If the app fails to start, check if port 7860 is in use. Change the port in `main/app.py` if needed.
- __Database issues__: If you encounter database errors, try deleting the `main/memory/` directory (backup first if needed).
- __Slow performance__: Reduce the number of active traders or increase the `RUN_EVERY_N_SECONDS` value in `main/utils/constants.py`.

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
This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

## Acknowledgements
- Polygon, Brave Search MCP, MCP community
- Gradio, Plotly
- openai-agents and related tooling
