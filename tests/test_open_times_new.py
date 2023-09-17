import pytest

from src.backend.parse_open_times import (
    parse_times_line,
    parse_times_entry
)

TEST_LINES = [
    "Tuesday 11.00-13.00",
    "Tuesday to Friday 11.00-13.00",
    "Thursday to Tuesday, 9.00 - 14.00"
]

TEST_DATA = [
    """Wednesday 13.00 - 15.00
    Friday 13.00 - 15.00""",
    """Tuesday 11.00 – 13.00
    Friday 11.00 – 13.00"""
]

TEST_LINES_OUTPUTS = [
    [{'day': 2, 'open': '11.00', 'close': '13.00'}],
    [{'day': 2, 'open': '11.00', 'close': '13.00'},
     {'day': 3, 'open': '11.00', 'close': '13.00'},
     {'day': 4, 'open': '11.00', 'close': '13.00'},
     {'day': 5, 'open': '11.00', 'close': '13.00'}],
    [{'day': 4, 'open': '9.00', 'close': '14.00'},
     {'day': 5, 'open': '9.00', 'close': '14.00'},
     {'day': 6, 'open': '9.00', 'close': '14.00'},
     {'day': 0, 'open': '9.00', 'close': '14.00'},
     {'day': 1, 'open': '9.00', 'close': '14.00'},
     {'day': 2, 'open': '9.00', 'close': '14.00'}]
]


def test_parse_times_line():
    # Assert line function runs as expected
    time_out = parse_times_line(TEST_LINES[0])
    print(time_out)
    assert sorted(time_out) == sorted(TEST_LINES_OUTPUTS[0])
    assert time_out[0] == TEST_LINES_OUTPUTS[0][0]

    # Check a range of dates process as expected
    time_out = parse_times_line(TEST_LINES[1])
    print(time_out)
    assert time_out[0]['day'] == 2
    assert time_out[3]['day'] == 5
    assert len(time_out) == 4

    # Check handling of weirdly ordered days
    time_out = parse_times_line(TEST_LINES[2])
    print(time_out)
    assert len(time_out) == 6


def test_parse_times_entry():
    time_out = parse_times_entry(TEST_DATA[0])
    print(time_out)
    assert len(time_out) == 2
    time_out = parse_times_entry(TEST_DATA[1])
    print(time_out)
    assert len(time_out) == 2