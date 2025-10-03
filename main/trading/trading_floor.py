from typing import List
import asyncio
from agents import add_trace_processor
from dotenv import load_dotenv

import os
import sys

root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from main.trading.traders import Trader
from main.utils.tracers import LogTracer
from main.markets.market import is_market_open
import main.utils.constants as constants

load_dotenv(override=True)

RUN_EVERY_N_SECONDS = constants.RUN_EVERY_N_SECONDS
RUN_EVEN_WHEN_MARKET_IS_CLOSED = constants.RUN_EVEN_WHEN_MARKET_IS_CLOSED
USE_MANY_MODELS = constants.USE_MANY_MODELS

names = ["Warren", "George", "Ray", "Cathie"]
lastnames = ["Patience", "Bold", "Systematic", "Crypto"]

if USE_MANY_MODELS:
    model_names = constants.MANY_MODELS_NAMES
    short_model_names = constants.MANY_MODELS_SHORT_NAMES
else:
    model_names = [constants.DEFAULT_MODEL_NAME] * 4
    short_model_names = [constants.DEFAULT_MODEL_SHORT_NAME] * 4


def create_traders() -> List[Trader]:
    traders = []
    for name, lastname, model_name in zip(names, lastnames, model_names):
        traders.append(Trader(name, lastname, model_name))
    return traders

# Cooperative cancellation for external controllers (e.g., Gradio UI)
STOP_EVENT: asyncio.Event = asyncio.Event()

def request_stop() -> None:
    """Signal the trading loop to stop at the soonest safe point."""
    STOP_EVENT.set()

def reset_stop() -> None:
    """Clear the stop flag before starting a new run."""
    try:
        STOP_EVENT.clear()
    except Exception:
        # In rare cases if STOP_EVENT was not initialized, recreate it
        globals()["STOP_EVENT"] = asyncio.Event()


async def run_every_n_minutes():
    add_trace_processor(LogTracer())
    traders = create_traders()
    try:
        while not STOP_EVENT.is_set():
            if RUN_EVEN_WHEN_MARKET_IS_CLOSED or is_market_open():
                await asyncio.gather(*[trader.run() for trader in traders])
            else:
                print("Market is closed, skipping run")
            # Wait either until next tick or until stop requested
            try:
                await asyncio.wait_for(STOP_EVENT.wait(), timeout=RUN_EVERY_N_SECONDS)
            except asyncio.TimeoutError:
                # timeout means continue next cycle
                pass
    finally:
        return


if __name__ == "__main__":
    print(f"Starting scheduler to run every {RUN_EVERY_N_SECONDS} seconds")
    asyncio.run(run_every_n_minutes())
