""" test open_times parsing

PyTest functions
"""

import pandas as pd
from src.backend.open_times import parse_open_times, parse_opening_str

open_str = "Tuesday 11.00 – 13.00\nFriday 11.00 – 13.00"
open_df = pd.DataFrame({"Name": ["Hillsborough"], "Opening": [open_str]})
out_str = [
    {"id": "bla", "day": "Friday", "start": "11.00", "end": "13.00"},
    {"id": "bla", "day": "Tuesday", "start": "11.00", "end": "13.00"},
]
out_df = pd.DataFrame(
    {
        "id": ["Hillsborough", "Hillsborough"],
        "day": ["Friday", "Tuesday"],
        "start": ["11.00", "11.00"],
        "end": ["13.00", "13.00"],
    }
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
