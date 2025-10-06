import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
import pandas as pd
from logic.alert_data import filters, helpers, processing, utils
from logic.plotting import pnl

# Utility to load test data
CSV_PATH = os.path.join(os.path.dirname(__file__), '..', 'tv_alerts.csv')

def load_test_df():
    return helpers.load_data_from_csv(CSV_PATH)

# --- FILTERS ---
def test_parse_hhmm():
    t = filters._parse_hhmm('9:30')
    assert t.hour == 9 and t.minute == 30
    t = filters._parse_hhmm('16:00')
    assert t.hour == 16 and t.minute == 0
    with pytest.raises(ValueError):
        filters._parse_hhmm('25:00')

def test_filter_by_time_of_day():
    df = load_test_df()
    df = processing.format_timestamp_column_and_set_as_index(df, col_name='Time')
    filtered = filters.filter_by_time_of_day(df, '09:30', '16:00')
    assert isinstance(filtered, pd.DataFrame)
    assert filtered.index.min().hour >= 9
    assert filtered.index.max().hour <= 16

def test_filter_by_days_of_week():
    df = load_test_df()
    df = processing.format_timestamp_column_and_set_as_index(df, col_name='Time')
    filtered = filters.filter_by_days_of_week(df, ['mon', 'tue', 'wed'])
    assert isinstance(filtered, pd.DataFrame)
    assert all(d in [0,1,2] for d in filtered.index.weekday)

def test_filter_by_weeks_of_month():
    df = load_test_df()
    df = processing.format_timestamp_column_and_set_as_index(df, col_name='Time')
    filtered = filters.filter_by_weeks_of_month(df, [1,2,3,4,5])
    assert isinstance(filtered, pd.DataFrame)
    assert filtered.shape[0] > 0

def test_filter_by_date_range():
    df = load_test_df()
    df = processing.format_timestamp_column_and_set_as_index(df, col_name='Time')
    # Convert comparison dates to UTC
    start = pd.to_datetime('2025-06-01').tz_localize('UTC')
    end = pd.to_datetime('2025-07-31').tz_localize('UTC')
    filtered = filters.filter_by_date_range(df, start, end)
    assert isinstance(filtered, pd.DataFrame)
    assert filtered.index.min() >= start
    assert filtered.index.max() <= end

def test_filter_alert_data():
    df = load_test_df()
    df = processing.format_timestamp_column_and_set_as_index(df, col_name='Time')
    result = filters.filter_alert_data(df, start_time='09:30', end_time='16:00', days=['mon', 'tue'])
    assert isinstance(result, pd.DataFrame)
    assert result.shape[0] > 0

# --- FILTERS EDGE CASES ---
def test_parse_hhmm_invalid_format():
    with pytest.raises(ValueError):
        filters._parse_hhmm('930')  # Missing colon
    with pytest.raises(ValueError):
        filters._parse_hhmm('9:60')  # Invalid minute
    with pytest.raises(ValueError):
        filters._parse_hhmm('24:00')  # Invalid hour

def test_filter_by_time_of_day_midnight_wrap():
    df = load_test_df()
    df = processing.format_timestamp_column_and_set_as_index(df, col_name='Time')
    # Should include times from 22:00 to 02:00 (wraps midnight)
    filtered = filters.filter_by_time_of_day(df, '22:00', '02:00')
    assert isinstance(filtered, pd.DataFrame)
    # All times should be >= 22:00 or <= 02:00
    times = filtered.index.time
    assert all(t >= pd.to_datetime('22:00').time() or t <= pd.to_datetime('02:00').time() for t in times)

def test_filter_by_days_of_week_invalid():
    df = load_test_df()
    df = processing.format_timestamp_column_and_set_as_index(df, col_name='Time')
    with pytest.raises(ValueError):
        filters.filter_by_days_of_week(df, ['nonday'])
    with pytest.raises(ValueError):
        filters.filter_by_days_of_week(df, [7])

def test_filter_by_weeks_of_month_invalid():
    df = load_test_df()
    df = processing.format_timestamp_column_and_set_as_index(df, col_name='Time')
    with pytest.raises(ValueError):
        filters.filter_by_weeks_of_month(df, [0])
    with pytest.raises(ValueError):
        filters.filter_by_weeks_of_month(df, [6])
    with pytest.raises(ValueError):
        filters.filter_by_weeks_of_month(df, [])

def test_filter_by_date_range_invalid():
    df = load_test_df()
    df = processing.format_timestamp_column_and_set_as_index(df, col_name='Time')
    start = pd.to_datetime('2025-07-31').tz_localize('UTC')
    end = pd.to_datetime('2025-06-01').tz_localize('UTC')
    with pytest.raises(ValueError):
        filters.filter_by_date_range(df, start, end)

# --- HELPERS ---
def test_load_data_from_csv():
    df = helpers.load_data_from_csv(CSV_PATH)
    assert isinstance(df, pd.DataFrame)
    assert df.shape[0] > 0

# --- PROCESSING ---
def test_split_data_by_name():
    df = load_test_df()
    split = processing.split_data_by_name(df)
    assert isinstance(split, dict)
    assert all(isinstance(v, pd.DataFrame) for v in split.values())

def test_extract_json_from_description():
    df = load_test_df()
    result = processing.extract_json_from_description(df)
    assert isinstance(result, pd.DataFrame)
    assert 'contract' in result.columns or 'trade_type' in result.columns

def test_format_timestamp_column_and_set_as_index():
    df = load_test_df()
    result = processing.format_timestamp_column_and_set_as_index(df, col_name='Time')
    assert isinstance(result.index, pd.DatetimeIndex)

def test_clean_filterable_json_df_pipe():
    df = load_test_df()
    result = processing.clean_filterable_json_df_pipe(df)
    assert isinstance(result, pd.DataFrame)
    assert result.index.is_monotonic_increasing

def test_trim_to_closed_trades():
    df = load_test_df()
    df = processing.extract_json_from_description(df)
    # Use 'timestamp' column after normalization
    df = processing.format_timestamp_column_and_set_as_index(df, col_name='timestamp')
    result = processing.trim_to_closed_trades(df)
    assert isinstance(result, pd.DataFrame)

def test_apply_flips():
    df = load_test_df()
    df = processing.extract_json_from_description(df)
    df = processing.format_timestamp_column_and_set_as_index(df, col_name='timestamp')
    result = processing.apply_flips(df)
    assert isinstance(result, pd.DataFrame)

def test_add_trade_profit():
    df = load_test_df()
    df = processing.clean_filterable_json_df_pipe(df)
    result = processing.add_trade_profit(df)
    assert 'profit' in result.columns
    assert 'rProfit' in result.columns

# --- PROCESSING EDGE CASES ---
def test_split_data_by_name_missing_column():
    df = load_test_df().drop(columns=['Name'])
    with pytest.raises(KeyError):
        processing.split_data_by_name(df)

def test_extract_json_from_description_malformed():
    df = load_test_df().copy()
    df.loc[0, 'Description'] = '{bad json}'
    result = processing.extract_json_from_description(df)
    assert isinstance(result, pd.DataFrame)
    # Should not raise, malformed JSON becomes empty dict

def test_format_timestamp_column_and_set_as_index_missing():
    df = load_test_df().drop(columns=['Time'])
    with pytest.raises(KeyError):
        processing.format_timestamp_column_and_set_as_index(df, col_name='Time')

def test_trim_to_closed_trades_no_entry():
    df = load_test_df()
    df = processing.extract_json_from_description(df)
    df = processing.format_timestamp_column_and_set_as_index(df, col_name='timestamp')
    df['trade_type'] = 'exit'  # No entry signals
    result = processing.trim_to_closed_trades(df)
    assert result.empty

def test_apply_flips_missing_signal_col():
    df = load_test_df()
    df = processing.extract_json_from_description(df)
    df = processing.format_timestamp_column_and_set_as_index(df, col_name='timestamp')
    df = df.drop(columns=['trade_type'])
    with pytest.raises(KeyError):
        processing.apply_flips(df)

# --- UTILS ---
def test_utils_clean_filterable_json_df_pipe():
    df = load_test_df()
    result = utils.clean_filterable_json_df_pipe(df)
    assert isinstance(result, pd.DataFrame)

def test_utils_get_filtered_split_data():
    df = load_test_df()
    result = utils.get_filtered_split_data(df, start_time='09:30', end_time='16:00')
    assert isinstance(result, dict)

def test_utils_filter_split_data():
    df = load_test_df()
    split = processing.split_data_by_name(df)
    result = utils.filter_split_data(split, start_time='09:30', end_time='16:00')
    assert isinstance(result, dict)

def test_utils_add_profit_and_fmt():
    df = load_test_df()
    df = processing.clean_filterable_json_df_pipe(df)
    result = utils.add_profit_and_fmt(df)
    assert isinstance(result, pd.DataFrame)


# --- UTILS EDGE CASES ---
def test_utils_filter_split_data_error_handling():
    df = load_test_df()
    split = processing.split_data_by_name(df)
    # Remove required column from one split to trigger error
    for k in split:
        split[k] = split[k].drop(columns=['trade_type'], errors='ignore')
    result = utils.filter_split_data(split, start_time='09:30', end_time='16:00')
    assert isinstance(result, dict)
    # Should skip errored splits and not raise

# --- PLOTTING ---
def test_plot_trading_pnl():
    df = load_test_df()
    df = processing.clean_filterable_json_df_pipe(df)
    pnl_df = processing.add_trade_profit(df)
    dates = pnl_df.index.strftime('%Y-%m-%d %H:%M:%S').tolist()
    pnl_vals = pnl_df['profit'].fillna(0).tolist()
    fig = pnl.plot_trading_pnl(dates, pnl_vals, title='Test PnL')
    assert hasattr(fig, 'to_html')


