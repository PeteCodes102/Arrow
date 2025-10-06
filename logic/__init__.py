import pandas as pd

from constants import rPROFIT, EXIT, TRADE_TYPE
from logic.alert_data.filters import filter_alert_data
from logic.alert_data.processing import add_trade_profit
from logic.plotting.pnl import plot_trading_pnl
import plotly.graph_objects as go


def filtered_data_chart(df: pd.DataFrame, delta: float, multiplier: float = 4.0, **kwargs) -> go.Figure:
  df = df.copy()
  filtered_df = filter_alert_data(df, **kwargs)
  trade_profit = add_trade_profit(filtered_df, multiplier=multiplier, delta=delta)
  profit_df = trade_profit[trade_profit[TRADE_TYPE] == EXIT]
  return plot_trading_pnl(profit_df.index, profit_df[rPROFIT])