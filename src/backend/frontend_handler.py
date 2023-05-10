"""Functions for handling front end requests"""
from datetime import datetime

import geopandas as gpd
import pandas as pd
from shapely.geometry import Point
from utils import snap_to_nearest_postcode, convert_to_geodataframe

# set the valid methods for filtering/searching and other constants
VALID_METHODS = {"postcode", "place_from"}
OD_MATRIX_PATH = "data/foodbank_postcode_od.csv"
FOODBANKS_PATH = "data/foodbank_coords.csv"


def foodfind_nearest(
    method: str,
    postcode: str = "S1 1AD",
    place_from: type[Point] = Point(-1.470599, 53.379244),
    dist_range: float = 5000,
    days: dict = {
        "Monday": True,
        "Tuesday": True,
        "Wednesday": True,
        "Thursday": True,
        "Friday": True,
        "Saturday": True,
        "Sunday": True,
    },
    num_results: int = 20,
) -> gpd.GeoDataFrame:
    """Find nearest food bank open on selected days.

    Args:
        place_from (_type_, optional): Location from which the user searches.
            Defaults to central Sheffield = Point(53.2251,1.2813).
        dist_range (_type_, optional): Possible restriction on distance willing
            to travel (km). Defaults to None.
        days (dict, optional): _description_. Defaults to {"Monday" : True,
            'Tuesday': True, 'Wednesday': True, 'Thursday': True,
            'Friday': True, 'Saturday': True, 'Sunday': True}.
        num_results (int, optional): _description_. Defaults to 20.

    Returns:
        Geopandas dataframe: _description_
    """

    # capture error when incorrect method is provided
    if method not in VALID_METHODS:
        raise ValueError(
            f"{method} is not a valid method. Expecting one of {VALID_METHODS}"
        )

    # handle snapping a place to the nearest post code
    if method == "place_from":
        postcode = snap_to_nearest_postcode(place_from)["postcode"]

    # read od matrix and foodbanks
    od_matrix = pd.read_csv(OD_MATRIX_PATH)
    foodbanks_df = pd.read_csv(FOODBANKS_PATH)

    # filter to near by foodbanks and sort by distance
    near_foodbanks = od_matrix[
        (od_matrix.postcode == postcode) & (od_matrix.distance <= dist_range)
    ].drop(columns=['postcode']).sort_values('distance')

    # limit number of results
    near_foodbanks = near_foodbanks.reset_index(drop=True).iloc[0:num_results]

    # merge on foodbank information
    foodbanks_df = foodbanks_df.merge(near_foodbanks, on="ID", how="right")

    # convert to geodataframe
    foodbanks_gdf = convert_to_geodataframe(foodbanks_df, crs="EPSG:4326")

    return foodbanks_gdf


def foodfind_asap(
    place_from=Point(53.2251, 1.2813),
    dist_range=None,
    time_stamp=datetime.now(),
    num_results=20,
):
    """Find nearby food band that is open now or asap.

    Args:
        place_from (Point, optional): Location from which the user searches.
            Defaults to central Sheffield = Point(53.2251,1.2813).
        dist_range (Float, optional): Possible restriction on distance willing
            to travel (km). Defaults to None.
        time_stamp (datetime, optional): Current/selected time point to find
            the first available foodbank. Defaults to datetime.now().
        num_results (int, optional): _description_. Defaults to 20.

    Returns:
        Geopandas dataframe: _description_
    """
    return None


if __name__ == "__main__":
    result = foodfind_nearest(
        method="place_from",
        place_from=Point(-1.470599, 53.379244),
        num_results=10
    )
    print(result)
