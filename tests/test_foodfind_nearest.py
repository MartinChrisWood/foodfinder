import pytest

from src.backend.frontend_handler import foodfind_nearest

# 1. test default function just monday
# 2. changes start postcode
# 3. changes day to search
test_conf = [
    {
        "method": "postcode",
        "postcode": "S1 1AD",
        "days": {"Monday": True},
        "result": "S10 2FD",
    },  # noqa E501
    {
        "method": "postcode",
        "postcode": "S10 1BS",
        "days": {"Monday": True},
        "result": "S10 2FD",
    },  # noqa E501
    {
        "method": "postcode",
        "postcode": "S1 1AD",
        "days": {"Tuesday": True},
        "result": "S6 3BS",
    },  # noqa E501
]


@pytest.mark.parametrize("config", test_conf)
def test_foodfind_nearest(config):
    """Test snapping to postcodes"""

    closest = foodfind_nearest(
        method=config["method"],
        postcode=config["postcode"],
        days=config["days"],
    )
    assert closest["postcode"].iloc[0] == config["result"]
