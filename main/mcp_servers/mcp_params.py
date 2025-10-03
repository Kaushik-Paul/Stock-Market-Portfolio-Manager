import os
from dotenv import load_dotenv

import os
import sys
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from main.markets.market import is_paid_polygon, is_realtime_polygon

load_dotenv(override=True)

brave_env = {"BRAVE_API_KEY": os.getenv("BRAVE_API_KEY")}
polygon_api_key = os.getenv("POLYGON_API_KEY")

# The MCP server for the Trader to read Market Data

if is_paid_polygon or is_realtime_polygon:
    market_mcp = {
        "command": "uvx",
        "args": ["--from", "git+https://github.com/polygon-io/mcp_polygon@v0.1.0", "mcp_polygon"],
        "env": {"POLYGON_API_KEY": polygon_api_key},
    }
else:
    market_module = "main.mcp_servers.market_server"
    market_mcp = {"command": sys.executable, "args": ["-m", market_module]}

# The full set of MCP servers for the trader: Accounts, Push Notification and the Market

accounts_module = "main.mcp_servers.accounts_server"
email_module = "main.mcp_servers.email_server"

trader_mcp_server_params = [
    {"command": sys.executable, "args": ["-m", accounts_module]},
    {"command": sys.executable, "args": ["-m", email_module]},
    market_mcp,
]

# The full set of MCP servers for the researcher: Fetch, Brave Search and Memory

def researcher_mcp_server_params(name: str):
    return [
        {"command": "uvx", "args": ["mcp-server-fetch"]},
        {
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-brave-search"],
            "env": brave_env,
        },
        {
            "command": "npx",
            "args": ["-y", "mcp-memory-libsql"],
            "env": {"LIBSQL_URL": f"file:./main/memory/{name}.db"},
        },
    ]
