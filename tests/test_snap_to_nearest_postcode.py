"""Test snapping a point to nearest postcodes"""

import pytest
from src.backend.utils import snap_to_nearest_postcode
from shapely.geometry import Point

# test a city centre, suburban and rural postcode
test_conf = [
    {'point': Point(-1.470599, 53.379244), 'result': "S1 2HJ"},
    {'point': Point(-1.422872, 53.401068), 'result': "S9 2AG"},
    {'point': Point(-1.59391, 53.36835), 'result': "S10 4QX"},
]


@pytest.mark.parametrize("config", test_conf)
def test_snap_to_nearest_postcode(config):
    """Test snapping to postcodes"""

    closest = snap_to_nearest_postcode(config["point"])
    assert closest["postcode"] == config["result"]
