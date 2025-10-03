import asyncio
import gradio as gr

import os
import sys
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from main.trading.trading_floor import (
    names,
    lastnames,
    short_model_names,
    run_every_n_minutes,
    request_stop,
    reset_stop,
)
from main.prompts.reset import reset_traders
from main.utils.util import css, js
from main.gradio_ui.styles import MODERN_CSS
from main.gradio_ui.views import TraderView, Trader

# Runtime state
trading_task = None
auto_stop_task = None
stop_requested = False


async def stop_trading(kill_app: bool = False, timeout: float = 2.0):
    global trading_task
    try:
        if trading_task and not trading_task.done():
            trading_task.cancel()
            try:
                # Wait briefly for graceful cancellation
                await asyncio.wait_for(trading_task, timeout=timeout)
            except Exception:
                # Timeout or CancelledError or other — proceed to clear task
                pass
    finally:
        trading_task = None
    if kill_app:
        import os

        os._exit(0)


async def auto_stop_after_duration(seconds: int):
    global stop_requested, auto_stop_task
    try:
        await asyncio.sleep(seconds)
        if not stop_requested:
            # Cooperative stop
            stop_requested = True
            try:
                request_stop()
            except Exception:
                pass
            await stop_trading(kill_app=False)
            if auto_stop_task and not auto_stop_task.done():
                auto_stop_task = None
    except asyncio.CancelledError:
        return


def create_ui():
    """Create the main Gradio UI for the trading simulation"""

    traders = [
        Trader(trader_name, lastname, model_name)
        for trader_name, lastname, model_name in zip(names, lastnames, short_model_names)
    ]
    trader_views = [TraderView(trader) for trader in traders]

    with gr.Blocks(
        title="Traders",
        css=css + MODERN_CSS,
        js=js,
        theme=gr.themes.Default(primary_hue="indigo"),
        fill_width=True,
    ) as ui:
        # Intro / Landing section
        with gr.Column(variant="panel", visible=True) as intro_group:
            gr.Markdown("# Stock Market Portfolio Manager", elem_classes=["brand"])
            gr.Markdown(
                "Live dashboard of simulated AI traders with portfolios, logs, and performance.",
                elem_classes=["subtitle"],
            )
            gr.Markdown(
                """
                <div style='text-align:center; max-width: 900px; margin: 4px auto 8px; color:#475569;'>
                    Four autonomous traders — Value, Macro, Systematic and Crypto — compete in real time. Watch live P&L charts, holdings, and execution logs. Reset instantly to rerun strategies with a fresh slate.
                </div>
                """,
                elem_classes=["subtitle"],
            )
            gr.HTML(
                """
                <div class='features'>
                  <div class='chip'>Live AI Traders</div>
                  <div class='chip'>Auto-refresh Charts</div>
                  <div class='chip'>Reset in 1 Click</div>
                  <div class='chip'>10-min Budget Guard</div>
                  <div class='chip'>SQLite Persistence</div>
                  <div class='chip'>Sleek Light UI</div>
                </div>
                """
            )
            gr.HTML(
                """
                <div class='disclaimer'>
                  <div class='icon'>!</div>
                  <div class='text'>
                    <strong>Disclaimer:</strong> This application is for educational and informational purposes only. Do not make financial decisions based on its outputs. The author is not liable for any financial loss.
                  </div>
                </div>
                """
            )
            # Run and Reset buttons in a single centered row
            with gr.Row(elem_classes=["center-row"], variant="default"):
                run_button = gr.Button("Run", variant="primary", elem_id="run-btn")
                reset_button = gr.Button("Reset", variant="secondary", elem_id="reset-btn")
            # Session duration note below buttons
            gr.Markdown(
                "This session will run for up to 10 minutes unless you stop it early.",
                elem_classes=["center-note"],
            )
            reset_status = gr.HTML(visible=False)

        # Traders dashboard (hidden until Run is clicked)
        with gr.Column(visible=False) as dashboard_group:
            with gr.Row(elem_classes=["topbar"]):
                gr.Markdown(
                    "Session runs for up to 10 minutes. Click Stop to end early.",
                    elem_classes=["note"],
                )
                stop_button = gr.Button("Stop", variant="secondary", elem_id="stop-btn")
            with gr.Row():
                for trader_view in trader_views:
                    trader_view.make_ui()

        # Start background loop and toggle visibility
        async def on_run_click():
            global trading_task, auto_stop_task, stop_requested
            stop_requested = False
            # Clear any prior stop signal before starting
            reset_stop()
            if trading_task is None or trading_task.done():
                trading_task = asyncio.create_task(run_every_n_minutes())
            # auto stop after 10 minutes unless stopped
            if auto_stop_task is None or auto_stop_task.done():
                auto_stop_task = asyncio.create_task(auto_stop_after_duration(600))
            return gr.update(visible=False), gr.update(visible=True)

        def on_reset_click():
            try:
                reset_traders()
                return gr.update(
                    value="<div class='single-card'>✅ Traders have been reset successfully.</div>",
                    visible=True,
                )
            except Exception as e:
                return gr.update(
                    value=f"<div class='single-card'>❌ Reset failed: {str(e)}</div>", visible=True
                )

        async def on_stop_click():
            global auto_stop_task, stop_requested
            # 1) Immediate UI update
            yield gr.update(value="Stopped", interactive=False)
            # 2) Cancel timers & background loop
            stop_requested = True
            # Signal cooperative stop to trading loop
            try:
                request_stop()
            except Exception:
                pass
            if auto_stop_task and not auto_stop_task.done():
                try:
                    auto_stop_task.cancel()
                except Exception:
                    pass
            await stop_trading(kill_app=False)
            # 3) Idempotent final state
            yield gr.update(value="Stopped", interactive=False)

        run_button.click(
            fn=on_run_click,
            inputs=[],
            outputs=[intro_group, dashboard_group],
            show_progress="hidden",
        )

        reset_button.click(
            fn=on_reset_click,
            inputs=[],
            outputs=[reset_status],
            show_progress="hidden",
        )

        stop_button.click(
            fn=on_stop_click,
            inputs=[],
            outputs=[stop_button],
            show_progress="hidden",
        )

    return ui
