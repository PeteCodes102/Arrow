import plotly.graph_objects as go
import pandas as pd

def plot_trading_pnl(dates, pnl, title):
    """
    Creates a simple, clean Plotly line chart for trading PnL,
    removing large time gaps between trades on the x-axis.

    Parameters:
        dates (list-like): List/Series of trade dates (datetime or str).
        pnl (list-like): List/Series of PnL values (floats/ints).
        title (str): Title for the chart.

    Returns:
        fig (plotly.graph_objects.Figure): The generated Plotly figure.
    """

    # Convert to pandas series (ensures clean handling)
    df = pd.DataFrame({"Date": pd.to_datetime(dates), "PnL": pnl})
    df = df.sort_values("Date")  # ensure time order

    # Create line chart
    fig = go.Figure()

    # Use a range of integers for the x-axis to remove time gaps
    fig.add_trace(go.Scatter(
        x=list(range(len(df))), # Use integer index for x-axis
        y=df["PnL"],
        mode="lines+markers",
        line=dict(color="#1f77b4", width=2),
        marker=dict(size=6),
        name="PnL"
    ))

    # Layout styling
    fig.update_layout(
        title=title,
        xaxis_title="Trade Number", # Update x-axis title
        yaxis_title="PnL",
        template="simple_white",
        hovermode="x unified",
        font=dict(size=14),
        margin=dict(l=40, r=40, t=50, b=40),
        height=500
    )

    return fig

