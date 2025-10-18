"""
Pydantic models used across the API.

This file defines `FilterParams`, a validated container for filtering
options accepted by the FastAPI endpoints. The model mirrors the keys used by
`logic.alert_data.filters.filter_alert_data` and validates/normalizes them so
route handlers can pass the values directly to the filtering utilities.
"""

from datetime import date
from typing import List, Optional, Union
import re

from pydantic import BaseModel, Field, field_validator, model_validator


_DAY_NAME_TO_NUM_KEYS = {
    "monday",
    "mon",
    "tuesday",
    "tue",
    "tues",
    "wednesday",
    "wed",
    "thursday",
    "thu",
    "thur",
    "thurs",
    "friday",
    "fri",
    "saturday",
    "sat",
    "sunday",
    "sun",
}

_TIME_RE = re.compile(r"^(\d{1,2}):(\d{2})$")


class FilterParams(BaseModel):
    """Validated filter parameters for alert/data endpoints.

    Fields
    - start_time / end_time: Strings in "HH:MM" (24-hour) format. Both must be
      provided together if time filtering is desired. Values are normalized to
      zero-padded "HH:MM" strings (e.g. "9:5" -> "09:05").
    - days: Optional list of weekday names (e.g. "mon", "monday", "Wed") or
      integers 0..6 where Monday=0 and Sunday=6. String names are normalized to
      lowercase.
    - weeks: Optional list of integers in 1..5 indicating week-of-month.
    - start_date / end_date: Optional dates. If both provided, end_date must be
      on/after start_date.

    Example
    -------
    p = FilterParams(start_time="9:30", end_time="16:00", days=["mon", "tue"], weeks=[1,2])
    """
    name: Optional[str] = Field(None, description="Strategy name to filter by")
    start_time: Optional[str] = Field(None, description="Start time in HH:MM (24h) format")
    end_time: Optional[str] = Field(None, description="End time in HH:MM (24h) format")
    days: Optional[List[Union[str, int]]] = Field(
        None, description="List of weekday names or ints (Mon=0..Sun=6)"
    )
    weeks: Optional[List[int]] = Field(None, description="List of weeks of month (1..5)")
    start_date: Optional[date] = Field(None, description="Start calendar date (inclusive)")
    end_date: Optional[date] = Field(None, description="End calendar date (inclusive)")

    @field_validator("start_time", "end_time", mode="before")
    def _validate_time_format(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return None
        m = _TIME_RE.match(v.strip())
        if not m:
            raise ValueError("time must be in HH:MM format (e.g. '9:30' or '09:30')")
        hh = int(m.group(1))
        mm = int(m.group(2))
        if hh < 0 or hh > 23 or mm < 0 or mm > 59:
            raise ValueError("hour must be 0..23 and minute 0..59")
        # normalize to zero-padded HH:MM
        return f"{hh:02d}:{mm:02d}"

    @field_validator("days", mode="before")
    def _validate_days(cls, v):
        if v is None:
            return None
        if isinstance(v, (str, int)):
            v = [v]
        if not isinstance(v, (list, tuple)):
            raise TypeError("days must be a list of weekday names or integers")

        normalized = []
        for item in v:
            if isinstance(item, int):
                if item < 0 or item > 6:
                    raise ValueError("weekday integers must be between 0 (Mon) and 6 (Sun)")
                normalized.append(item)
            else:
                s = str(item).strip().lower()
                if s not in _DAY_NAME_TO_NUM_KEYS:
                    raise ValueError(f"unrecognized weekday name: {item!r}")
                normalized.append(s)
        return normalized

    @field_validator("weeks", mode="before")
    def _validate_weeks(cls, v):
        if v is None:
            return None
        if isinstance(v, int):
            v = [v]
        if not isinstance(v, (list, tuple)):
            raise TypeError("weeks must be a list of integers 1..5")
        normalized = []
        for item in v:
            try:
                n = int(item)
            except Exception:
                raise ValueError("weeks must contain integers")
            if n < 1 or n > 5:
                raise ValueError("weeks must be integers between 1 and 5 (inclusive)")
            normalized.append(n)
        return normalized

    @model_validator(mode="after")
    def _check_time_and_date_consistency(cls, values):
        st = values.start_time
        et = values.end_time
        if (st is not None) != (et is not None):
            raise ValueError("Both start_time and end_time must be provided together.")
        sd = values.start_date
        ed = values.end_date
        if sd and ed and ed < sd:
            raise ValueError("end_date must be on or after start_date.")
        return values

    def to_filter_kwargs(self) -> dict:
        """Return a dict suitable for passing to `filter_alert_data`.

        This method avoids callers having to check for None values when building
        the kwargs for the filter function.
        """
        out: dict = {}
        if self.start_time is not None and self.end_time is not None:
            out["start_time"] = self.start_time
            out["end_time"] = self.end_time
        if self.days is not None:
            out["days"] = self.days
        if self.weeks is not None:
            out["weeks"] = self.weeks
        if self.start_date is not None and self.end_date is not None:
            # pydantic date values are date objects; filter accepts strings or timestamps
            out["start_date"] = str(self.start_date)
            out["end_date"] = str(self.end_date)
        return out
