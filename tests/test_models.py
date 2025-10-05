import pytest
from datetime import date

from models import FilterParams


def test_time_normalization_and_pair_required():
    p = FilterParams(start_time="9:3", end_time="16:00")
    assert p.start_time == "09:03"
    assert p.end_time == "16:00"

    # missing partner should raise
    with pytest.raises(ValueError):
        FilterParams(start_time="09:30")


def test_invalid_time_format_raises():
    with pytest.raises(ValueError):
        FilterParams(start_time="9", end_time="16:00")
    with pytest.raises(ValueError):
        FilterParams(start_time="24:00", end_time="25:00")


def test_days_accepts_single_and_list_and_normalizes():
    p1 = FilterParams(days="Mon")
    assert p1.days == ["mon"]

    p2 = FilterParams(days=2)
    assert p2.days == [2]

    p3 = FilterParams(days=["Tue", "wed", 4])
    assert p3.days == ["tue", "wed", 4]


def test_invalid_day_name_raises():
    with pytest.raises(ValueError):
        FilterParams(days=["Funday"])
    with pytest.raises(ValueError):
        FilterParams(days=[-1])


def test_weeks_accepts_single_and_list_and_rejects_out_of_range():
    p1 = FilterParams(weeks=1)
    assert p1.weeks == [1]

    p2 = FilterParams(weeks=[1, 3, 5])
    assert p2.weeks == [1, 3, 5]

    with pytest.raises(ValueError):
        FilterParams(weeks=[0])
    with pytest.raises(ValueError):
        FilterParams(weeks=[6])


def test_date_consistency_and_to_filter_kwargs():
    p = FilterParams(start_date=date(2025, 7, 1), end_date=date(2025, 7, 31))
    kwargs = p.to_filter_kwargs()
    assert kwargs["start_date"] == "2025-07-01"
    assert kwargs["end_date"] == "2025-07-31"

    # end_date before start_date should raise
    with pytest.raises(ValueError):
        FilterParams(start_date=date(2025, 7, 10), end_date=date(2025, 7, 1))


def test_to_filter_kwargs_only_includes_set_values():
    p = FilterParams(days=["mon"], weeks=[1])
    kwargs = p.to_filter_kwargs()
    assert "days" in kwargs and kwargs["days"] == ["mon"]
    assert "weeks" in kwargs and kwargs["weeks"] == [1]
    assert "start_time" not in kwargs and "end_time" not in kwargs
    assert "start_date" not in kwargs and "end_date" not in kwargs

