import pandas as pd

from core.constants import rPROFIT
from logic.alert_data.utils import get_profit_df_by_name
from logic.plotting.pnl import plot_trading_pnl
import plotly.graph_objects as go


def filtered_data_chart(
    df: pd.DataFrame,
    name: str,
    delta: float,
    flip: bool,
    multiplier: float = 4.0,
    **kwargs
) -> go.Figure:
    """
    Generates a Plotly figure showing the filtered profit and loss (PnL) for a given trading strategy.

    Args:
        df (pd.DataFrame): Input DataFrame containing trading data.
        name (str): Name of the strategy or filter to apply.
        delta (float): Delta value for filtering.
        flip (bool): Whether to flip the trade direction.
        multiplier (float, optional): Multiplier for profit calculation. Defaults to 4.0.
        **kwargs: Additional keyword arguments for profit calculation.

    Returns:
        go.Figure: Plotly figure visualizing the filtered PnL.
    """
    df = df.copy()
    profit_df = get_profit_df_by_name(
        master_df=df,
        name=name,
        delta=delta,
        multiplier=multiplier,
        flip=flip,
        **kwargs
    )
    return plot_trading_pnl(profit_df.index, profit_df[rPROFIT], title=f"Filtered PnL for {name}")

