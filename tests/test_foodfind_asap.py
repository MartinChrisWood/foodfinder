"""Test foodfind_asap function in frontend_handler.py"""

from datetime import datetime
import pytest
from src.backend.frontend_handler import foodfind_asap

# test for closest foodbank ID given date and starting postcode
mock_data = [
    {"timestamp": datetime(2023, 5, 11, 12, 10, 23, 442020), "postcode": "S1 1AA", "nearest_on_date": 15},
    {"timestamp": datetime(2023, 6, 11, 12, 10, 23, 442020), "postcode": "S1 1AA", "nearest_on_date": 31},
    {"timestamp": datetime(2023, 5, 11, 12, 10, 23, 442020), "postcode": "S9 1EA", "nearest_on_date": 17},
    # same closest as above as Tuesday next availability from Sunday
    {"timestamp": datetime(2023, 6, 11, 12, 10, 23, 442020), "postcode": "S9 1EA", "nearest_on_date": 17},

]

@pytest.mark.parametrize("config", mock_data)
def test_foodfind_asap(config):
    """Test filtering to closest foodbank by distance and availability"""

    found = foodfind_asap(method="postcode",
                          time_stamp=config["timestamp"],
                          postcode=config["postcode"])
    # assert that top hit is correct
    assert found.loc[0, "ID"] == config["nearest_on_date"]

