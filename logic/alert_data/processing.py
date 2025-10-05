"""
Utilities for parsing and preparing alert JSON produced by trading strategies.

This module provides small, well-documented functions to:
- split incoming alert rows by strategy name,
- extract JSON payloads stored in a text `Description` column,
- normalize and index timestamps,
- trim event streams to closed trades,
- flip trade-side signals (buy <-> sell), and
- compute per-trade profit and cumulative profit.

The functions are designed to be small, testable, and to avoid mutating caller data
unless explicitly documented. They use constants defined in the project's
`constants.py` module for column names and tokens.
"""

import json
from typing import Any, Dict, Iterable, Mapping, Optional, Hashable

import numpy as np
import pandas as pd

from constants import (
    NAME,
    DESCRIPTION,
    TIME,
    TIMESTAMP,
    DATETIME_FORMAT,
    BUY,
    SELL,
    EXIT,
    PRICE,
    PROFIT,
    rPROFIT,
    TRADE_TYPE,
    QUANTITY,
    AlgoDict,
)


# ==> Split the Data by the Strategy's name
def split_data_by_name(df: pd.DataFrame) -> Dict[Hashable, pd.DataFrame]:
    """Split a DataFrame into a mapping of strategy name -> DataFrame.

    The input DataFrame is grouped by the column named by the project constant
    `NAME`. Each group's DataFrame is .copy()'d before being returned to avoid
    accidental mutation of the original.

    Parameters
    ----------
    df : pd.DataFrame
        Input alert rows. Must contain the column `NAME`.

    Returns
    -------
    Dict[Hashable, pd.DataFrame]
        Mapping from each unique name to a DataFrame containing rows for that
        name.

    Raises
    ------
    KeyError
        If the `NAME` column is not present in ``df``.
    """
    if NAME not in df.columns:
        raise KeyError(f"Expected column {NAME!r} in DataFrame")

    grouped_data = df.groupby(NAME)
    return {name: group.copy() for name, group in grouped_data}


# ==> Extract JSON from 'Description' column
def extract_json_from_description(df: pd.DataFrame) -> pd.DataFrame:
    """Extract and normalize JSON payloads stored in the `DESCRIPTION` column.

    Each row of ``df`` is expected to contain a JSON string in the column named
    by the project constant `DESCRIPTION`. This function decodes those strings,
    normalizes them into a flat table using ``pd.json_normalize`` and attaches
    the original `NAME` and `TIME` values as columns.

    Parameters
    ----------
    df : pd.DataFrame
        Source DataFrame. Must contain ``DESCRIPTION`` and ``NAME`` columns. The
        ``TIME`` column is used to populate a timestamp column in the result.

    Returns
    -------
    pd.DataFrame
        A new DataFrame with the normalized JSON fields plus the original
        ``NAME`` and a ``TIMESTAMP`` column taken from ``TIME``.

    Notes
    -----
    - Malformed JSON strings are treated as empty objects and do not raise an
      exception; this keeps pipeline processing robust.
    """
    if DESCRIPTION not in df.columns or NAME not in df.columns:
        raise KeyError(f"Expected columns {DESCRIPTION!r} and {NAME!r} in DataFrame")

    json_records: list[Dict[str, Any]] = []
    for idx, row in df.iterrows():
        raw = row.get(DESCRIPTION, "")
        try:
            obj = json.loads(raw) if isinstance(raw, str) and raw.strip() else {}
        except json.JSONDecodeError:
            # Malformed JSON -> treat as empty dict to avoid failing the whole batch
            obj = {}
        json_records.append(obj)

    json_df = pd.json_normalize(json_records)

    # Attach name and timestamp columns from the original DataFrame.
    json_df[NAME] = df[NAME].values
    # Use TIME column if present, otherwise fall back to existing TIMESTAMP column
    if TIME in df.columns:
        json_df[TIMESTAMP] = df[TIME].values
    else:
        # If no TIME column, try to use an existing TIMESTAMP column or index
        if TIMESTAMP in df.columns:
            json_df[TIMESTAMP] = df[TIMESTAMP].values
        else:
            json_df[TIMESTAMP] = df.index.astype(str)

    return json_df


# ==> Set Timestamp as Index and Format Timestamp Col
def format_timestamp_column_and_set_as_index(
    df: pd.DataFrame, col_name: str = TIMESTAMP
) -> pd.DataFrame:
    """Return a copy of ``df`` indexed by a parsed timestamp column.

    The function will:
      * copy the input DataFrame to avoid mutating the caller,
      * parse ``col_name`` into datetime,
      * set the resulting datetime index on the returned DataFrame,
      * write a formatted timestamp string back into ``col_name`` using the
        project's ``DATETIME_FORMAT``, and
      * sort the DataFrame by the new index.

    Parameters
    ----------
    df : pd.DataFrame
        Input table containing a timestamp-like column.
    col_name : str
        Column to parse as datetime (default: project constant ``TIMESTAMP``).

    Returns
    -------
    pd.DataFrame
        A new DataFrame indexed by datetime with a formatted timestamp column.

    Raises
    ------
    KeyError
        When ``col_name`` is not present in ``df``.
    """
    if col_name not in df.columns:
        raise KeyError(f"Missing timestamp column {col_name!r}")

    out = df.copy()
    timestamp_col = out[col_name]
    out.index = pd.to_datetime(timestamp_col)
    out[col_name] = out.index.strftime(DATETIME_FORMAT)
    out.sort_index(inplace=True)
    return out


# ==> Filterable, Clean JSON DataFrame Pipe
def clean_filterable_json_df_pipe(df: pd.DataFrame) -> pd.DataFrame:
    """Create a normalized, time-indexed DataFrame ready for trade processing.

    Steps performed (in order):
    1. Extract JSON payloads from the ``DESCRIPTION`` column.
    2. Normalize the timestamps and set them as the DataFrame index.
    3. Trim the result so the first row is an entry signal and the last row is
       a subsequent exit (prevents open trades from contaminating results).

    Parameters
    ----------
    df : pd.DataFrame
        Raw alerts DataFrame.

    Returns
    -------
    pd.DataFrame
        Processed DataFrame ready for P&L or plotting operations.
    """
    json_df = extract_json_from_description(df)
    fmt_ts_df = format_timestamp_column_and_set_as_index(json_df)
    return trim_to_closed_trades(fmt_ts_df)


# ==> Trim Data to Closed Trades
def trim_to_closed_trades(
    df: pd.DataFrame,
    signal_col: str = TRADE_TYPE,
    entry_values: Iterable[str] = (BUY, SELL),
    exit_value: str = EXIT,
    *,
    sort_by_index: bool = True,
) -> pd.DataFrame:
    """Return a slice of ``df`` that contains only complete (entry->exit) trades.

    The function will find the first row whose ``signal_col`` matches one of
    ``entry_values`` and the last row after that first entry which matches
    ``exit_value``. The returned DataFrame contains rows from that first entry
    through the last exit, inclusive.

    If no entry or no subsequent exit exists this function returns an empty
    DataFrame (same columns as ``df``).
    """
    if signal_col not in df.columns:
        raise KeyError(f"Column {signal_col!r} not found in DataFrame.")

    work = df.sort_index() if sort_by_index else df.copy()

    s_norm = work[signal_col].astype(str).str.strip().str.lower()
    entry_set = {e.strip().lower() for e in entry_values}
    exit_norm = exit_value.strip().lower()

    # Use numpy positions to avoid ambiguous pandas boolean-indexing warnings
    entry_positions = np.flatnonzero(s_norm.isin(entry_set).to_numpy())
    if entry_positions.size == 0:
        return work.iloc[0:0].copy()

    first_pos = int(entry_positions[0])
    first_entry_idx = work.index[first_pos]

    post = s_norm.iloc[first_pos:]
    # compare using numpy arrays to avoid static-analysis confusion
    exit_positions = np.flatnonzero(post.to_numpy() == exit_norm)
    if exit_positions.size == 0:
        return work.iloc[0:0].copy()

    last_pos = int(exit_positions[-1])
    last_exit_idx = post.index[last_pos]
    return work.loc[first_entry_idx:last_exit_idx]


def apply_flips(
    df: pd.DataFrame,
    *,
    signal_col: str = TRADE_TYPE,
    buy_token: str = BUY,
    sell_token: str = SELL,
    strip_whitespace: bool = True,
) -> pd.DataFrame:
    """Return a copy of ``df`` where buy/sell entry tokens are flipped.

    Use-cases: quickly compute the mirrored performance of a strategy by
    switching longs to shorts and vice versa while keeping exit tokens
    unchanged. The function preserves the original token's common casing
    pattern (upper/lower/title).
    """
    if signal_col not in df.columns:
        raise KeyError(f"Column {signal_col!r} not found in DataFrame.")

    work = df.copy()

    buy_l = buy_token.lower()
    sell_l = sell_token.lower()

    def _match_case(template: str, new_word: str) -> str:
        if template.isupper():
            return new_word.upper()
        if template.islower():
            return new_word.lower()
        if template.istitle():
            return new_word.title()
        return new_word

    def _flip_token(x: Any) -> Any:
        if pd.isna(x):
            return x
        s = str(x)
        t = s.strip() if strip_whitespace else s
        t_l = t.lower()
        if t_l == buy_l:
            return _match_case(t, sell_token)
        if t_l == sell_l:
            return _match_case(t, buy_token)
        # keep exits and unknown values as-is (trimmed if requested)
        return t


    work[signal_col] = work[signal_col].map(_flip_token)
    return work


def add_trade_profit(
    df: pd.DataFrame,
    *,
    price_col: str = PRICE,
    signal_col: str = TRADE_TYPE,
    entry_values: Mapping[str, int] | None = None,
    exit_value: str = EXIT,
    qty_col: Optional[str] = QUANTITY,
    multiplier: float = 1.0,
    delta: float = 1.0,
    fee_per_trade: float = 0.0,
    fee_per_unit: float = 0.0,
    sort_by_index: bool = True,
) -> pd.DataFrame:
    """Compute per-trade profit and running profit for a simple 1-position model.

    The function scans ``df`` in index order. When it encounters an entry token
    (one of ``entry_values``) it records the entry price and quantity; when it
    later encounters ``exit_value`` it computes the profit for the completed
    trade and writes that value into the ``PROFIT`` column for the exit row.
    A cumulative sum of ``PROFIT`` is written into ``rPROFIT``.

    Parameters
    ----------
    df : pd.DataFrame
        Time-indexed DataFrame containing at least ``price_col`` and ``signal_col``.
    price_col : str
        Column name for the trade price.
    signal_col : str
        Column name for the trade signal tokens.
    entry_values : Mapping[str, int] | None
        Mapping from entry token to direction, e.g. {"buy": +1, "sell": -1}.
        When None the function defaults to the project's BUY/SELL mapping.
    exit_value : str
        Token that indicates an exit row.
    qty_col : Optional[str]
        Column name for the quantity; when None a quantity of 1.0 is assumed.
    multiplier : float
        Per-unit multiplier applied to (exit_price - entry_price) * qty.
    delta : float
        Final scalar applied to each trade's P&L (default 1.0).
    fee_per_trade : float
        Flat fee subtracted once per closed trade.
    fee_per_unit : float
        Fee applied per unit (qty) for the closed trade.
    sort_by_index : bool
        If True, the DataFrame is processed in ascending time order.

    Returns
    -------
    pd.DataFrame
        Copy of ``df`` with two added columns: ``PROFIT`` (NaN except on exit
        rows) and ``rPROFIT`` (running cumulative profit).
    """
    if price_col not in df.columns:
        raise KeyError(f"Missing price column {price_col!r}")
    if signal_col not in df.columns:
        raise KeyError(f"Missing signal column {signal_col!r}")
    if qty_col is not None and qty_col not in df.columns:
        raise KeyError(f"Missing qty column {qty_col!r}")

    if entry_values is None:
        entry_values = {BUY: +1, SELL: -1}

    work = df.sort_index() if sort_by_index else df.copy()
    sig = work[signal_col].astype(str).str.strip().str.lower()
    entry_dir_map = {k.strip().lower(): int(v) for k, v in entry_values.items()}
    exit_token = exit_value.strip().lower()

    prices = work[price_col].astype(float).to_numpy()
    qtys = (
        work[qty_col].astype(float).to_numpy()
        if qty_col
        else np.ones(len(work), dtype=float)
    )
    profits = np.full(len(work), np.nan, dtype=float)

    in_pos = False
    entry_price = np.nan
    entry_qty = 0.0
    direction = 0  # +1 long, -1 short

    for i, token in enumerate(sig.to_numpy()):
        if not in_pos:
            if token in entry_dir_map:
                in_pos = True
                direction = entry_dir_map[token]
                entry_price = prices[i]
                entry_qty = float(qtys[i])
            # exits without a position are ignored
        else:
            # already in a position
            if token in entry_dir_map:
                # additional entries while in a position: ignore (simple model)
                continue
            if token == exit_token:
                exit_price = prices[i]
                qty = entry_qty
                pnl = (exit_price - entry_price) * direction * (qty * multiplier)
                pnl -= (fee_per_trade + qty * fee_per_unit)
                profits[i] = pnl * delta

                # reset position state
                in_pos = False
                entry_price = np.nan
                entry_qty = 0.0
                direction = 0

    out = work.copy()
    out[PROFIT] = profits
    out[rPROFIT] = out[PROFIT].cumsum()
    return out


def _process_and_split_data(df: pd.DataFrame) -> AlgoDict:
    """Internal helper: process input alerts and return a mapping of algorithm -> rows.

    This wraps the higher-level pipeline (`clean_filterable_json_df_pipe`) and
    collects every algorithm's processed DataFrame into a dictionary. Errors in
    individual algorithm groups are caught and logged; processing continues for
    other groups.
    """
    split_data = split_data_by_name(df)
    output_dict: AlgoDict = {}
    for name, group in split_data.items():
        try:
            output_dict[name] = clean_filterable_json_df_pipe(group)
        except Exception as e:  # pragma: no cover - best-effort logging
            print(f"Error processing {name}: {e}")
    return output_dict


def process_and_split_data(df: pd.DataFrame) -> AlgoDict:
    """Public wrapper around ``_process_and_split_data``.

    Kept as a separate function to provide a stable public API for callers and
    to allow easier unit-testing.
    """
    return _process_and_split_data(df)
