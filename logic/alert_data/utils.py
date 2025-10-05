from logic.alert_data.processing import *
from logic.alert_data.filters import *

# ==> Filterable, Clean Json DataFrame Pipe
def clean_filterable_json_df_pipe(df: pd.DataFrame) -> pd.DataFrame:

  # copy the data
  df = df.copy()

  # extract the description column and make into its own dataframe
  json_df = extract_json_from_description(df)

  # set the timestamp as the index and format it
  fmt_ts_df = format_timestamp_column_and_set_as_index(json_df)

  return trim_to_closed_trades(fmt_ts_df)

def get_filtered_split_data(df: pd.DataFrame, **kwargs) -> AlgoDict:
  split_data = process_and_split_data(df)
  return filter_split_data(split_data, **kwargs)


def filter_split_data(split_data: dict[str, pd.DataFrame], **kwargs) -> dict[str, pd.DataFrame]:
  output_dict = {}
  for name, df in split_data.items():
    try:
      output_dict[name] = filter_alert_data(df, **kwargs)
    except Exception as e:
      print(f"Error processing {name}: {e}")
  return output_dict

# pipe to plot PnL over time
def add_profit_and_fmt(df: pd.DataFrame) -> pd.DataFrame:
  df = df.copy()
  profit_df = add_trade_profit(df)

  return profit_df[profit_df[TRADE_TYPE] == EXIT]

# pipe to make filtered df
def format_to_ny_timeframe_df(df: pd.DataFrame) -> pd.DataFrame:
  df = df.copy()
  filterable_json_df = clean_filterable_json_df_pipe(df)
  ny_timeframe_df = filter_by_time_of_day(filterable_json_df, '09:30', '12:00')
  return ny_timeframe_df

