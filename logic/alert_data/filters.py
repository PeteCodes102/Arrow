import json
from typing import Iterable, Mapping, Sequence, Hashable

import numpy as np
import pandas as pd

from constants import *

from datetime import time

# ==> Filter by Time of Day e.g. 0930 - 1630

def _parse_hhmm(s: str) -> time:
    """Parse 'HH:MM' (e.g., '9:30', '16:00') into datetime.time."""
    s = s.strip()
    # Allow '9:30', '09:30' etc.
    hour_str, minute_str = s.split(":")
    return time(int(hour_str), int(minute_str))


def filter_by_time_of_day(
    df: pd.DataFrame,
    start_hhmm: str,
    end_hhmm: str) -> pd.DataFrame:
    """
    Keep rows whose timestamp's clock time is within [start_hhmm, end_hhmm].
    - If the window crosses midnight (e.g., 22:00 -> 02:00), it is handled correctly.
    - Works with tz-aware or tz-naive indexes. No mutation of the index.

    Examples:
        9:30 -> 16:00 (RTH window)
        22:00 -> 02:00 (overnight window)
    """
    if not isinstance(df.index, pd.DatetimeIndex):
        raise TypeError("DataFrame index must be a DatetimeIndex")

    start_t = _parse_hhmm(start_hhmm)
    end_t = _parse_hhmm(end_hhmm)

    # Extract wall-clock times as an array; this does not alter tz.
    times = df.index.time  # ndarray of datetime.time
    times_np = np.array(times, dtype=object)

    if start_t <= end_t:
        mask = (times_np >= start_t) & (times_np <= end_t)
    else:
        # Window wraps past midnight: time >= start OR time <= end
        mask = (times_np >= start_t) | (times_np <= end_t)

    return df.loc[mask]

# ==> Filter by day of the week, e.g. mon - wed

_DAY_NAME_TO_NUM = {
    "monday": 0, "mon": 0,
    "tuesday": 1, "tue": 1, "tues": 1,
    "wednesday": 2, "wed": 2,
    "thursday": 3, "thu": 3, "thur": 3, "thurs": 3,
    "friday": 4, "fri": 4,
    "saturday": 5, "sat": 5,
    "sunday": 6, "sun": 6,
}

def filter_by_days_of_week(
    df: pd.DataFrame,
    days: Sequence[str | int]
    ) -> pd.DataFrame:
    """
    Keep rows whose weekday is in `days`.
    - Accepts names ('monday', 'Mon', 'thu', etc.) or integers (Mon=0 ... Sun=6).
    - Works with tz-aware or tz-naive indexes.

    Example:
        filter_by_days_of_week(df, ['mon', 'tue', 'wed'])
        filter_by_days_of_week(df, [0,1,2])
    """
    if not isinstance(df.index, pd.DatetimeIndex):
        raise TypeError("DataFrame index must be a DatetimeIndex")

    wanted: set[int] = set()
    for d in days:
        if isinstance(d, int):
            if d < 0 or d > 6:
                raise ValueError("Weekday integers must be in 0..6 (Mon=0 ... Sun=6).")
            wanted.add(d)
        else:
            key = str(d).strip().lower()
            if key not in _DAY_NAME_TO_NUM:
                raise ValueError(f"Unrecognized day name: {d!r}")
            wanted.add(_DAY_NAME_TO_NUM[key])

    wday = df.index.weekday  # ndarray[int] Mon=0..Sun=6
    mask = np.isin(wday, list(wanted))
    return df.loc[mask]


# ==> Filter by Week of the month e.g. 1st week and 3rd week

def filter_by_weeks_of_month(
    df: pd.DataFrame,
    weeks: Iterable[int]
    ) -> pd.DataFrame:
    """
    Keep rows whose timestamp falls in the given 'week-of-month' numbers.

    Definition:
      week_of_month = 1 for days 1..7, 2 for 8..14, 3 for 15..21, 4 for 22..28, 5 for 29..31.
    (Some months have part of a 5th week; you can include 5 if desired.)

    Example:
        filter_by_weeks_of_month(df, [1, 2, 3, 4])
        filter_by_weeks_of_month(df, [1])  # first week only
    """
    if not isinstance(df.index, pd.DatetimeIndex):
        raise TypeError("DataFrame index must be a DatetimeIndex")

    weeks = set(int(w) for w in weeks)
    if not weeks:
        raise ValueError("Provide at least one week number (1..5).")
    if any(w < 1 or w > 5 for w in weeks):
        raise ValueError("Week numbers must be between 1 and 5 (inclusive).")

    day = df.index.day
    wom = ((day - 1) // 7) + 1  # 1..5
    mask = np.isin(wom, list(weeks))
    return df.loc[mask]


# ==> Filter by start date and end date
def filter_by_date_range(
    df: pd.DataFrame,
    start_date: str | pd.Timestamp,
    end_date: str | pd.Timestamp
    ) -> pd.DataFrame:
    """
    Keep rows whose *calendar date* lies between start_date and end_date, inclusive.
    - Interprets inputs as dates (not times). This avoids tz comparison issues.
    - Works with tz-aware or tz-naive indexes.

    Example:
        filter_by_date_range(df, "2025-07-01", "2025-07-31")
    """
    if not isinstance(df.index, pd.DatetimeIndex):
        raise TypeError("DataFrame index must be a DatetimeIndex")

    s = pd.to_datetime(start_date).normalize()
    e = pd.to_datetime(end_date).normalize()

    if e < s:
        raise ValueError("end_date must be on/after start_date")

    # Compare on normalized dates so tz-aware vs tz-naive is a non-issue.
    idx_dates = pd.DatetimeIndex(df.index.normalize())
    mask = (idx_dates >= s) & (idx_dates <= e)
    return df.loc[mask]

def filter_alert_data(df: pd.DataFrame, **kwargs) -> pd.DataFrame:
  output = df.copy()

  if 'start_time' in kwargs and 'end_time' in kwargs:
    # use regex to check the format matches HH:MM
    start_time = kwargs['start_time']
    end_time = kwargs['end_time']
    output = filter_by_time_of_day(df, start_hhmm=start_time, end_hhmm=end_time)

  if 'days' in kwargs:
    days = kwargs['days']
    output = filter_by_days_of_week(df, days=days)

  if 'weeks' in kwargs:
    weeks = kwargs['weeks']
    output = filter_by_weeks_of_month(df, weeks=weeks)

  if 'start_date' in kwargs and 'end_date' in kwargs:
    start_date = kwargs['start_date']
    end_date = kwargs['end_date']
    output = filter_by_date_range(df, start_date=kwargs['start_date'], end_date=kwargs['end_date'])

  return output