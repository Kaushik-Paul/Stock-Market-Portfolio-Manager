from mcp.server.fastmcp import FastMCP

import os
import sys
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from main.markets.market import get_share_price

mcp = FastMCP("market_server")

@mcp.tool()
async def lookup_share_price(symbol: str) -> float:
    """This tool provides the current price of the given stock symbol.

    Args:
        symbol: the symbol of the stock
    """
    return get_share_price(symbol)

if __name__ == "__main__":
    mcp.run(transport='stdio')