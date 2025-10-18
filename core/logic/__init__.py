from typing import List, Any

import pandas as pd

from core.constants import rPROFIT
from core.logic.alert_data.utils import *

from core.logic.plotting.pnl import plot_trading_pnl
import plotly.graph_objects as go


async def db_data_to_df(data: List[Any]) -> pd.DataFrame:
    """
    Fetches all data using the provided DataService and returns a pandas DataFrame.
    """
    # If data is a list of Pydantic/Beanie models, convert to dicts using aliases
    if data and hasattr(data[0], 'model_dump'):
        # Use by_alias=True so fields with aliases (e.g. alias 'name') are present
        records = [item.model_dump(by_alias=True) for item in data]
    else:
        records = data

    df = pd.DataFrame.from_records(records)

    # Normalize "Name"/"name" column variants because code in different modules
    # may check for either k.NAME ("Name") or k.NAME.lower() ("name"). Ensure both
    # exist so downstream processing doesn't KeyError unexpectedly.
    if 'name' in df.columns and 'Name' not in df.columns:
        df['Name'] = df['name']
    elif 'Name' in df.columns and 'name' not in df.columns:
        df['name'] = df['Name']

    df.to_csv('all_data.csv', index=False)  # Save to CSV for inspection
    return df


async def filtered_data_chart(
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
    fig = plot_trading_pnl(profit_df.index, profit_df[rPROFIT], title=f"Filtered PnL for {name}")
    return fig
