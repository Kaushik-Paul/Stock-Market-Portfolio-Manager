import gradio as gr
import pandas as pd
import plotly.express as px

import os
import sys
import asyncio
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from main.accounts.accounts import Account
from main.utils.util import css, js, Color
from main.utils.database import read_log
from main.trading.trading_floor import (
    names,
    lastnames,
    short_model_names,
    run_every_n_minutes,
    request_stop,
    reset_stop,
)
from main.prompts.reset import reset_traders

mapper = {
    "trace": Color.WHITE,
    "agent": Color.CYAN,
    "function": Color.GREEN,
    "generation": Color.YELLOW,
    "response": Color.MAGENTA,
    "account": Color.RED,
}

# Additional modern CSS inspired by example_gradio_app.py
MODERN_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;700;800&family=Manrope:wght@400;700;800&display=swap');
html, body {
  background: radial-gradient(1000px 600px at 20% -10%, rgba(59,130,246,.12), transparent 60%),
              radial-gradient(800px 500px at 80% 0%, rgba(236,72,153,.10), transparent 55%),
              #f8fafc;
  color: #0b1220;
  font-family: Manrope, Inter, Helvetica, Arial, sans-serif;
}
.gradio-container { max-width: 100% !important; width: 100% !important; margin: 0 auto !important; padding: 0 16px; }
.brand { display:block; text-align:center; font-family: Space Grotesk, Manrope, Inter, sans-serif; font-weight: 800; font-size: 40px; letter-spacing: .3px; background: linear-gradient(90deg,#06b6d4 0%,#a78bfa 45%,#fb7185 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-shadow: 0 0 0 rgba(0,0,0,0), 0 6px 26px rgba(6,182,212,.28), 0 10px 46px rgba(167,139,250,.28), 0 14px 60px rgba(251,113,133,.22); background-size: 200% 200%; animation: brandGlow 8s ease-in-out infinite; }
@keyframes brandGlow { 0% { background-position: 0% 50%; } 50% { background-position: 100% 50%; } 100% { background-position: 0% 50%; } }
.subtitle { margin: 8px auto 12px; font-weight: 500; letter-spacing: 0.03em; line-height: 1.6; max-width: 900px; text-align: center; font-size: 1.05rem; color: #334155; }
.center-row { display: flex; justify-content: center; gap: 10px; margin: 0 auto; width: fit-content; }
#run-btn, #run-btn button { background: linear-gradient(90deg,#06b6d4,#a78bfa,#fb7185); color: white; padding: 10px 14px; font-size: 14px; border-radius: 12px; border: none; width: 120px; box-shadow: 0 10px 30px rgba(6,182,212,.25), 0 2px 8px rgba(0,0,0,.06); transition: transform .15s ease, box-shadow .2s ease; }
#run-btn button:hover { transform: translateY(-1px); box-shadow: 0 14px 36px rgba(6,182,212,.32), 0 3px 10px rgba(0,0,0,.08); }
#reset-btn, #reset-btn button { background: #ffffff; color: #2563eb; padding: 10px 14px; font-size: 14px; border-radius: 12px; border: 1px solid rgba(2,6,23,.12); width: 120px; box-shadow: 0 6px 18px rgba(2,6,23,.06); }
#stop-btn, #stop-btn button { background: linear-gradient(90deg,#ef4444,#f97316); color: white; padding: 8px 12px; font-size: 13px; border-radius: 10px; border: none; box-shadow: 0 8px 22px rgba(239,68,68,.2); width: 100px; }
.disclaimer { background: #ffffff; border: 1px solid rgba(2,6,23,.08); border-radius: 14px; padding: 14px 18px; max-width: 900px; margin: 16px auto 0; display: flex; align-items: flex-start; gap: 12px; box-shadow: 0 12px 28px rgba(2,6,23,.08); position: relative; overflow: hidden; }
.disclaimer:before { content:""; position:absolute; inset:-1px; background: linear-gradient(120deg, rgba(6,182,212,.25), rgba(167,139,250,.22), rgba(251,113,133,.22)); filter: blur(24px); opacity: .35; pointer-events:none; }
.disclaimer .icon { width: 28px; height: 28px; border-radius: 9999px; background: #facc15; display: inline-flex; align-items: center; justify-content: center; color: #0b1220; font-weight: 800; }
.disclaimer .text { color: #334155; line-height: 1.55; }
.topbar { display: flex; align-items: center; justify-content: space-between; padding: 10px 12px; margin: 0 auto 12px; max-width: 800px; background: rgba(255, 255, 255, 0.8); border-radius: 12px; box-shadow: 0 2px 12px rgba(0,0,0,0.04); }
.note { color: #475569; font-size: 13px; text-align: center; margin: 6px auto 4px; max-width: 500px; line-height: 1.5; font-weight: 500; opacity: 0.9; }
.center-note { text-align: center; color: #475569; font-size: 13px; margin: 4px 0 8px; line-height: 1.5; font-weight: 500; opacity: 0.9; }
#stop-btn button:disabled { cursor: not-allowed !important; opacity: .7 !important; }
/* Soft glow for panels */
.gr-box, .gr-panel { box-shadow: 0 16px 40px rgba(30,64,175,.08), 0 2px 10px rgba(2,6,23,.04) !important; border-radius: 14px !important; }
/* Plot container polish */
.wrap, .container { backdrop-filter: saturate(110%) blur(2px); }
/* Feature chips */
.features { display:flex; flex-wrap:wrap; gap:10px; align-items:center; justify-content:center; margin: 6px auto 4px; }
.chip { padding:6px 10px; border-radius:9999px; background: linear-gradient(90deg, rgba(6,182,212,.08), rgba(167,139,250,.10)); color:#0b1220; border:1px solid rgba(2,6,23,.08); box-shadow: 0 6px 18px rgba(2,6,23,.06); font-size: 13px; }
"""


class Trader:
    def __init__(self, name: str, lastname: str, model_name: str):
        self.name = name
        self.lastname = lastname
        self.model_name = model_name
        self.account = Account.get(name)

    def reload(self):
        self.account = Account.get(self.name)

    def get_title(self) -> str:
        return f"<div style='text-align: center;font-size:34px;'>{self.name}<span style='color:#ccc;font-size:24px;'> ({self.model_name}) - {self.lastname}</span></div>"

    def get_strategy(self) -> str:
        return self.account.get_strategy()

    def get_portfolio_value_df(self) -> pd.DataFrame:
        df = pd.DataFrame(self.account.portfolio_value_time_series, columns=["datetime", "value"])
        df["datetime"] = pd.to_datetime(df["datetime"])
        return df

    def get_portfolio_value_chart(self):
        df = self.get_portfolio_value_df()
        fig = px.line(df, x="datetime", y="value")
        margin = dict(l=40, r=20, t=20, b=40)
        fig.update_layout(
            height=300,
            margin=margin,
            xaxis_title=None,
            yaxis_title=None,
            paper_bgcolor="#bbb",
            plot_bgcolor="#dde",
        )
        fig.update_xaxes(tickformat="%m/%d", tickangle=45, tickfont=dict(size=8))
        fig.update_yaxes(tickfont=dict(size=8), tickformat=",.0f")
        return fig

    def get_holdings_df(self) -> pd.DataFrame:
        """Convert holdings to DataFrame for display"""
        holdings = self.account.get_holdings()
        if not holdings:
            return pd.DataFrame(columns=["Symbol", "Quantity"])

        df = pd.DataFrame(
            [{"Symbol": symbol, "Quantity": quantity} for symbol, quantity in holdings.items()]
        )
        return df

    def get_transactions_df(self) -> pd.DataFrame:
        """Convert transactions to DataFrame for display"""
        transactions = self.account.list_transactions()
        if not transactions:
            return pd.DataFrame(columns=["Timestamp", "Symbol", "Quantity", "Price", "Rationale"])

        return pd.DataFrame(transactions)

    def get_portfolio_value(self) -> str:
        """Calculate total portfolio value based on current prices"""
        portfolio_value = self.account.calculate_portfolio_value() or 0.0
        pnl = self.account.calculate_profit_loss(portfolio_value) or 0.0
        color = "green" if pnl >= 0 else "red"
        emoji = "⬆" if pnl >= 0 else "⬇"
        return f"<div style='text-align: center;background-color:{color};'><span style='font-size:32px'>${portfolio_value:,.0f}</span><span style='font-size:24px'>&nbsp;&nbsp;&nbsp;{emoji}&nbsp;${pnl:,.0f}</span></div>"

    def get_logs(self, previous=None) -> str:
        logs = read_log(self.name, last_n=13)
        response = ""
        for log in logs:
            timestamp, type, message = log
            color = mapper.get(type, Color.WHITE).value
            response += f"<span style='color:{color}'>{timestamp} : [{type}] {message}</span><br/>"
        response = f"<div style='height:250px; overflow-y:auto;'>{response}</div>"
        if response != previous:
            return response
        return gr.update()


class TraderView:
    def __init__(self, trader: Trader):
        self.trader = trader
        self.portfolio_value = None
        self.chart = None
        self.holdings_table = None
        self.transactions_table = None

    def make_ui(self):
        with gr.Column():
            gr.HTML(self.trader.get_title())
            with gr.Row():
                self.portfolio_value = gr.HTML(self.trader.get_portfolio_value)
            with gr.Row():
                self.chart = gr.Plot(
                    self.trader.get_portfolio_value_chart, container=True, show_label=False
                )
            with gr.Row(variant="panel"):
                self.log = gr.HTML(self.trader.get_logs)
            with gr.Row():
                self.holdings_table = gr.Dataframe(
                    value=self.trader.get_holdings_df,
                    label="Holdings",
                    headers=["Symbol", "Quantity"],
                    row_count=(5, "dynamic"),
                    col_count=2,
                    max_height=300,
                    elem_classes=["dataframe-fix-small"],
                )
            with gr.Row():
                self.transactions_table = gr.Dataframe(
                    value=self.trader.get_transactions_df,
                    label="Recent Transactions",
                    headers=["Timestamp", "Symbol", "Quantity", "Price", "Rationale"],
                    row_count=(5, "dynamic"),
                    col_count=5,
                    elem_classes=["dataframe-fix"]
                )

        timer = gr.Timer(value=120)
        timer.tick(
            fn=self.refresh,
            inputs=[],
            outputs=[
                self.portfolio_value,
                self.chart,
                self.holdings_table,
                self.transactions_table,
            ],
            show_progress="hidden",
            queue=False,
        )
        log_timer = gr.Timer(value=0.5)
        log_timer.tick(
            fn=self.trader.get_logs,
            inputs=[self.log],
            outputs=[self.log],
            show_progress="hidden",
            queue=False,
        )

    def refresh(self):
        self.trader.reload()
        return (
            self.trader.get_portfolio_value(),
            self.trader.get_portfolio_value_chart(),
            self.trader.get_holdings_df(),
            self.trader.get_transactions_df(),
        )


# Main UI construction
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
        os._exit(0)

async def auto_stop_after_duration(seconds: int):
    global stop_requested, auto_stop_task
    try:
        await asyncio.sleep(seconds)
        if not stop_requested:
            # Signal cooperative stop to trading loop
            stop_requested = True
            try:
                request_stop()
            except Exception:
                pass
            # Stop trading without killing the app
            await stop_trading(kill_app=False)
            # Update UI to show auto-stopped state
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
            gr.Markdown("This session will run for up to 10 minutes unless you stop it early.", elem_classes=["center-note"])
            reset_status = gr.HTML(visible=False)

        # Traders dashboard (hidden until Run is clicked)
        with gr.Column(visible=False) as dashboard_group:
            with gr.Row(elem_classes=["topbar"]):
                gr.Markdown("Session runs for up to 10 minutes. Click Stop to end early.", elem_classes=["note"])
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
                return gr.update(value="<div class='single-card'>✅ Traders have been reset successfully.</div>", visible=True)
            except Exception as e:
                return gr.update(value=f"<div class='single-card'>❌ Reset failed: {str(e)}</div>", visible=True)

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


if __name__ == "__main__":
    ui = create_ui()
    ui.launch()
