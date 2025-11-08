import pandas as pd
import pytest

import importlib.util
import pathlib

# Load the processing module directly by file path to avoid importing logic.__init__ during pytest collection
_proc_path = pathlib.Path(__file__).resolve().parents[1] / 'core' / 'logic' / 'alert_data' / 'processing.py'
_spec = importlib.util.spec_from_file_location("processing_mod", str(_proc_path))
_processing = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_processing)  # type: ignore[arg-type]
proc = _processing

from core.constants import DESCRIPTION, NAME, TIME, TIMESTAMP, TRADE_TYPE, PRICE, QUANTITY, PROFIT, rPROFIT


def test_extract_json_from_description_handles_malformed_and_empty():
    df = pd.DataFrame(
        {
            DESCRIPTION: ['{"price": 100}', 'not a json', ''],
            NAME: ['algo1', 'algo1', 'algo1'],
            TIME: ['2020-01-01 00:00:00'] * 3,
        }
    )

    out = proc.extract_json_from_description(df)

    # should preserve row count and name/timestamp columns
    assert len(out) == 3
    assert list(out[NAME]) == ['algo1', 'algo1', 'algo1']
    assert TIMESTAMP in out.columns

    # the first row should have a price column equal to 100
    assert 'price' in out.columns
    assert out.loc[0, 'price'] == 100


def test_format_timestamp_column_and_set_as_index_parses_and_formats():
    data = [
        {TIMESTAMP: '2020-01-01 00:00:00', 'x': 1},
        {TIMESTAMP: '2020-02-02 12:34:56', 'x': 2},
    ]
    df = pd.DataFrame(data)

    out = proc.format_timestamp_column_and_set_as_index(df.copy())

    # index should be DatetimeIndex and column TIMESTAMP formatted
    assert isinstance(out.index, pd.DatetimeIndex)
    assert out[TIMESTAMP].iloc[0] == '2020-01-01 00:00:00'
    assert out[TIMESTAMP].iloc[1] == '2020-02-02 12:34:56'


def test_trim_to_closed_trades_basic_selection():
    # Create a signals series with leading exits and trailing open entry
    rows = [
        {'trade_type': 'other'},
        {'trade_type': 'exit'},
        {'trade_type': 'buy'},   # first entry should start here
        {'trade_type': 'hold'},
        {'trade_type': 'exit'},  # last exit after first entry should end here
        {'trade_type': 'buy'},
    ]
    df = pd.DataFrame(rows)

    trimmed = proc.trim_to_closed_trades(df, signal_col='trade_type')

    # trimmed should start at index 2 and end at index 4 (inclusive)
    assert len(trimmed) == 3
    assert trimmed['trade_type'].iloc[0].lower() == 'buy'
    assert trimmed['trade_type'].iloc[-1].lower() == 'exit'


def test_apply_flips_preserves_casing_and_trims():
    df = pd.DataFrame(
        {
            TRADE_TYPE: [' Buy ', 'SELL', 'exit', 'Hold'],
            'other': [1, 2, 3, 4],
        }
    )

    flipped = proc.apply_flips(df, signal_col=TRADE_TYPE)

    # ' Buy ' -> 'Sell' (trimmed and title-cased), 'SELL' -> 'buy' (upper->upper preserved)
    assert flipped[TRADE_TYPE].iloc[0] == 'Sell'
    # Original 'SELL' is all upper, _match_case should return upper for new word
    assert flipped[TRADE_TYPE].iloc[1] == 'BUY'
    # Exits remain unchanged (but trimmed)
    assert flipped[TRADE_TYPE].iloc[2] == 'exit'
    # Unknown values are returned trimmed
    assert flipped[TRADE_TYPE].iloc[3] == 'Hold'


def test_add_trade_profit_basic_with_qty_and_fees():
    # Build a tiny trade stream: buy -> exit -> sell -> exit
    data = [
        {PRICE: 100.0, TRADE_TYPE: 'buy', QUANTITY: 2.0},
        {PRICE: 110.0, TRADE_TYPE: 'exit', QUANTITY: 2.0},
        {PRICE: 200.0, TRADE_TYPE: 'sell', QUANTITY: 1.0},
        {PRICE: 195.0, TRADE_TYPE: 'exit', QUANTITY: 1.0},
    ]
    df = pd.DataFrame(data)

    out = proc.add_trade_profit(
        df,
        price_col=PRICE,
        signal_col=TRADE_TYPE,
        qty_col=QUANTITY,
        multiplier=1.0,
        delta=1.0,
        fee_per_trade=1.0,
        fee_per_unit=0.5,
    )

    # Check profit on first exit: (110-100)*2*1 - (1 + 2*0.5) = 20 - (1+1) = 18
    expected_first = (110.0 - 100.0) * 1 * (2.0 * 1.0) - (1.0 + 2.0 * 0.5)
    assert out[PROFIT].iloc[1] == pytest.approx(expected_first)

    # Check profit on second exit: (195-200)*-1*1 - (1 + 1*0.5) = (-5)*-1 -1.5 = 5 -1.5 = 3.5
    expected_second = (195.0 - 200.0) * (-1) * (1.0 * 1.0) - (1.0 + 1.0 * 0.5)
    assert out[PROFIT].iloc[3] == pytest.approx(expected_second)

    # Check running profit is cumulative
    assert out[rPROFIT].iloc[1] == pytest.approx(expected_first)
    assert out[rPROFIT].iloc[3] == pytest.approx(expected_first + expected_second)
