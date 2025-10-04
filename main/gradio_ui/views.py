import gradio as gr
import pandas as pd
import plotly.express as px

import os
import sys
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from main.accounts.accounts import Account
from main.utils.database import read_log
from main.utils.util import Color

# Map log types to colors
MAPPER = {
    "trace": Color.WHITE,
    "agent": Color.CYAN,
    "function": Color.GREEN,
    "generation": Color.YELLOW,
    "response": Color.MAGENTA,
    "account": Color.RED,
}


class Trader:
    def __init__(self, name: str, lastname: str, model_name: str):
        self.name = name
        self.lastname = lastname
        self.model_name = model_name
        self.account = Account.get(name)

    def reload(self):
        self.account = Account.get(self.name)

    def get_title(self) -> str:
        return (
            f"<div style='text-align: center;font-size:34px;'>{self.name}"
            f"<span style='color:#ccc;font-size:24px;'> ({self.model_name}) - {self.lastname}</span></div>"
        )

    def get_strategy(self) -> str:
        return self.account.get_strategy()

    def get_portfolio_value_df(self) -> pd.DataFrame:
        df = pd.DataFrame(self.account.portfolio_value_time_series, columns=["datetime", "value"])
        df["datetime"] = pd.to_datetime(df["datetime"])
        return df

    def get_portfolio_value_chart(self):
        df = self.get_portfolio_value_df()
        fig = px.line(df, x="datetime", y="value")
        
        # Get theme colors based on current theme
        text_color = "#0b1220"  # Default light theme text
        grid_color = "rgba(0,0,0,0.1)"  # Default light theme grid
        
        # Try to detect dark theme
        try:
            import js
            if js.document.documentElement.classList.contains('dark'):
                text_color = "#f8fafc"
                grid_color = "rgba(255,255,255,0.1)"
        except:
            pass
            
        margin = dict(l=40, r=20, t=20, b=40)
        fig.update_layout(
            height=300,
            margin=margin,
            xaxis_title=None,
            yaxis_title=None,
            paper_bgcolor="var(--panel-bg, #ffffff)",
            plot_bgcolor="var(--panel-bg, #f8f9fa)",
            font=dict(color=text_color),
            xaxis=dict(
                showgrid=True,
                gridcolor=grid_color,
                tickformat="%m/%d",
                tickangle=45,
                tickfont=dict(size=8, color=text_color),
                linecolor=grid_color,
                zerolinecolor=grid_color
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor=grid_color,
                tickfont=dict(size=8, color=text_color),
                tickformat=",.0f",
                linecolor=grid_color,
                zerolinecolor=grid_color
            ),
            hoverlabel=dict(
                bgcolor="var(--panel-bg, #ffffff)",
                font_size=12,
                font_family="Manrope, sans-serif"
            )
        )
        
        # Update line color for better visibility
        fig.update_traces(
            line=dict(color='#3b82f6', width=2.5),
            hovertemplate='%{y:$,.0f}<extra></extra>'
        )
        
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
        return (
            f"<div style='text-align: center;background-color:{color};'>"
            f"<span style='font-size:32px'>${portfolio_value:,.0f}</span>"
            f"<span style='font-size:24px'>&nbsp;&nbsp;&nbsp;{emoji}&nbsp;${pnl:,.0f}</span></div>"
        )

    def get_logs(self, previous=None) -> str:
        logs = read_log(self.name, last_n=13)
        response = ""
        for log in logs:
            timestamp, log_type, message = log
            color = MAPPER.get(log_type, Color.WHITE).value
            response += f"<span style='color:{color}'>{timestamp} : [{log_type}] {message}</span><br/>"
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
        self.log = None

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
                    elem_classes=["dataframe-fix"],
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
