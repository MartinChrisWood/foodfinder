import pytest

from src.backend.parse_open_times import parse_times_line

TEST_INPUTS = [
    "Tuesday 11.00-13.00",
    "Tuesday to Friday 11.00-13.00",
    "Thursday to Tuesday, 9.00 - 14.00"
]

TEST_OUTPUTS = [
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
    time_out = parse_times_line(TEST_INPUTS[0])
    print(time_out)
    assert sorted(time_out) == sorted(TEST_OUTPUTS[0])
    assert time_out[0] == TEST_OUTPUTS[0][0]

    # Check a range of dates process as expected
    time_out = parse_times_line(TEST_INPUTS[1])
    print(time_out)
    assert time_out[0]['day'] == 2
    assert time_out[3]['day'] == 5
    assert len(time_out) == 4

    # Check handling of weirdly ordered days
    time_out = parse_times_line(TEST_INPUTS[2])
    print(time_out)
    assert len(time_out) == 6