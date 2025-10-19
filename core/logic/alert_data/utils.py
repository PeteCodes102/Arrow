import pandas as pd

from core.logic.alert_data.filters import *
from core.constants import *
from core.logic.alert_data.processing import extract_json_from_description, format_timestamp_column_and_set_as_index, \
    trim_to_closed_trades, process_and_split_data, add_trade_profit, apply_flips, clean_filterable_json_df_pipe

# load trading view alert data
def load_data_from_csv(file_path: str) -> pd.DataFrame:
    """
  Loads data from a CSV file into a pandas DataFrame.

  Args:
    file_path: The path to the CSV file.

  Returns:
    A pandas DataFrame containing the data from the CSV file.
  """
    data = pd.read_csv(file_path)
    data.dropna(inplace=True)
    return data


def load_data_from_csv_util(file_path: str) -> pd.DataFrame:
    """
    Loads data from a CSV file into a pandas DataFrame.

    Args:
        file_path (str): The path to the CSV file.
    Returns:
        pd.DataFrame: A pandas DataFrame containing the data from the CSV file.
    """
    master_df = load_data_from_csv(file_path)
    return extract_json_from_description(master_df)



def get_filtered_split_data(df: pd.DataFrame, **kwargs) -> AlgoDict:
    """
    Split the input DataFrame by strategy name, apply filters, and return filtered splits.

    Parameters:
        df (pd.DataFrame): Raw alerts DataFrame.
        **kwargs: Filter parameters for filter_alert_data.

    Returns:
        AlgoDict: Dictionary mapping strategy name to filtered DataFrame.
    """

    split_data = process_and_split_data(df)
    return filter_split_data(split_data, **kwargs)


def filter_split_data(split_data: dict[str, pd.DataFrame], **kwargs) -> dict[str, pd.DataFrame]:
    """
    Apply filter_alert_data to each split DataFrame in the input dictionary.
    Errors in individual splits are caught and logged; processing continues for others.

    Parameters:
        split_data (dict[str, pd.DataFrame]): Mapping of strategy name to DataFrame.
        **kwargs: Filter parameters for filter_alert_data.

    Returns:
        dict[str, pd.DataFrame]: Dictionary mapping strategy name to filtered DataFrame.
    """

    output_dict = {}
    for name, df in split_data.items():
        try:
            output_dict[name] = filter_alert_data(df, **kwargs)
        except Exception as e:
            print(f"Error processing {name}: {e}")
    return output_dict


# pipe to plot PnL over time
def add_profit_and_fmt(df: pd.DataFrame, delta: float, multiplier: float) -> pd.DataFrame:
    """
    Compute per-trade profit and return only exit trades for plotting or analysis.

    Parameters:
        df (pd.DataFrame): DataFrame containing trade signals and prices.
        delta (float): Scalar applied to each trade's P&L.
        multiplier (float): Per-unit multiplier for profit calculation.

    Returns:
        pd.DataFrame: DataFrame containing only exit trades with profit columns.
    """

    df = df.copy()
    profit_df = add_trade_profit(df, delta=delta, multiplier=multiplier)

    return profit_df[profit_df[TRADE_TYPE] == EXIT]


# pipe to make filtered df
def apply_filters_and_profit(df: pd.DataFrame, delta: float, multiplier: float, flip: bool, **kwargs) -> pd.DataFrame:
    """
    Apply filtering, optional trade-side flipping, and profit calculation to a DataFrame.

    Parameters:
        df (pd.DataFrame): Raw alerts DataFrame.
        delta (float): Scalar applied to each trade's P&L.
        multiplier (float): Per-unit multiplier for profit calculation.
        flip (bool): If True, flip buy/sell signals before profit calculation.
        **kwargs: Filter parameters for filter_alert_data.

    Returns:
        pd.DataFrame: DataFrame containing only exit trades with profit columns.
    """

    df = df.copy()
    filterable_json_df = clean_filterable_json_df_pipe(df)
    filtered_df = filter_alert_data(filterable_json_df, **kwargs)

    if flip:
        filtered_df = apply_flips(filtered_df)

    return add_profit_and_fmt(filtered_df, multiplier=multiplier, delta=delta)


def get_profit_df_by_name(master_df: pd.DataFrame, name: str, delta: float, multiplier: float = 4.0, flip: bool = False,
                          **kwargs) -> pd.DataFrame:
    """
    Get the profit DataFrame for a specific strategy name after filtering and processing.

    Parameters:
        master_df (pd.DataFrame): Raw alerts DataFrame containing all strategies.
        name (str): Strategy name to select.
        delta (float): Scalar applied to each trade's P&L.
        multiplier (float, optional): Per-unit multiplier for profit calculation. Default is 4.0.
        flip (bool, optional): If True, flip buy/sell signals before profit calculation. Default is False.
        **kwargs: Filter parameters for filter_alert_data.

    Returns:
        pd.DataFrame: DataFrame containing only exit trades with profit columns for the selected strategy.

    Raises:
        ValueError: If the specified name is not found in the data.
    """
    split_data = process_and_split_data(master_df)
    print(f"Available names in data: {list(split_data.keys())}")
    if name not in split_data:
        raise ValueError(f"Name '{name}' not found in data.")

    df = split_data[name]

    return apply_filters_and_profit(df, delta=delta, multiplier=multiplier, flip=flip, **kwargs)
