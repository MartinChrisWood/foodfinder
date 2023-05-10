""" test open_times parsing

PyTest functions
"""
from datetime import datetime
import pandas as pd
from src.backend.open_times import (
    parse_open_times,
    parse_opening_str,
    sort_by_time_to_open,
)

open_str = "Tuesday 11.00 – 13.00\nFriday 11.00 – 13.00"
open_df = pd.DataFrame(
    {
        "Name": ["Hillsborough", "Crookes"],
        "Opening": [open_str, "Tuesday 14.00 – 15.00"],
    }
)
out_str = [
    {"id": "bla", "day": "Friday", "start": "11.00", "end": "13.00"},
    {"id": "bla", "day": "Tuesday", "start": "11.00", "end": "13.00"},
]
out_df = pd.DataFrame(
    {
        "id": ["Hillsborough", "Hillsborough", "Crookes"],
        "day": ["Friday", "Tuesday", "Tuesday"],
        "start": ["11.00", "11.00", "14.00"],
        "end": ["13.00", "13.00", "15.00"],
    }
)
time_to_open = pd.Series(
    [
        pd.Timedelta("0 days 00:00:00"),
        pd.Timedelta("0 days 01:30:00"),
        pd.Timedelta("2 days 22:30:00"),
    ],
    name="time_to_open",
)


def test_parse_open_str():
    test_str = parse_opening_str(open_str, "bla")
    assert test_str == out_str


def test_parse_open_df():
    test_df = parse_open_times(open_df)
    pd.testing.assert_frame_equal(
        test_df,
        out_df,
    )


def test_sort_by_time():
    time_now = datetime(2023, 5, 9, 12, 30, 0, 0)
    test_df = sort_by_time_to_open(out_df, time_now)
    pd.testing.assert_series_equal(
        test_df.time_to_open,
        time_to_open,
    )
