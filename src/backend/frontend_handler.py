"""Functions for handling front end requests"""
from datetime import datetime, timedelta

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
    ].drop(columns=['postcode']).sort_values('distance').reset_index(drop=True)

    # merge on foodbank information
    foodbanks_df = near_foodbanks.merge(foodbanks_df, on="ID", how="left")

    # filter further to requested days - lower casing all the strings
    requested_days = [
        day.lower() for day, value in days.items() if value is True
    ]
    foodbanks_df = foodbanks_df[
        (
            foodbanks_df[
                "opening"
            ].str.lower().str.contains("|".join(requested_days))
        )
        | (foodbanks_df["opening"].str.lower().str.contains("all"))
    ]

    # convert to geodataframe and limit results
    foodbanks_gdf = convert_to_geodataframe(foodbanks_df, crs="EPSG:4326")
    foodbanks_gdf = foodbanks_gdf.reset_index(drop=True)
    foodbanks_gdf = foodbanks_gdf.iloc[0:num_results]

    return foodbanks_gdf


def foodfind_asap(
    od_matrix,
    foodbank_table,
    post_code: str = "S1 1AA",
    dist_range: float = 5000,     # 5km
    time_stamp: datetime = datetime.now(),
    num_results: int = 20
) -> pd.DataFrame:
    """Find nearby food band that is open now or asap.

    Args:
        od_matrix (pandas.DataFrame): Origin-Destination matrix data
            (commonly "foodbank_postcode_od.csv")
        foodbank_table (pandas.DataFrame): Foodbank admin data
            (commonly "foodbank_coords.csv")
        post_code (string, optional): Postcode from which the user searches.
            Defaults to "S1 1AA" (central Sheffield).
        dist_range (Float, optional): Possible restriction on distance willing
            to travel (km). Defaults to 5km.
        time_stamp (datetime, optional): Current/selected time point to find
            the first available foodbank. Defaults to datetime.now().
        num_results (int, optional): _description_. Defaults to 20.

    Returns:
        pandas dataframe: _description_
    """

    foodbanks_nearby = od_matrix[(od_matrix["postcode"]==post_code) &
                                 (od_matrix["distance"]<=dist_range)]
    
    foodbanks_nearby = pd.merge(foodbanks_nearby[["ID", "distance"]], foodbank_table, on="ID")
    
    days = []
    
    for x in range(1,7):
        days.append((time_stamp + timedelta(days=x)).strftime("%A"))

    df = foodbanks_nearby[foodbanks_nearby["opening"].str.contains(time_stamp.strftime("%A"))].sort_values("distance")
    for day in days:
        df2 = foodbanks_nearby[foodbanks_nearby["opening"].str.contains(day)].sort_values("distance")
        df = pd.concat([df, df2])

    return df.reset_index(drop=True).head(num_results)

od_matrix = pd.read_csv("../../data/foodbank_postcode_od.csv")
foodbank_table = pd.read_csv("../../data/foodbank_coords.csv")

foodfind_asap(od_matrix, foodbank_table)

if __name__ == "__main__":
    result = foodfind_nearest(
        method="place_from",
        place_from=Point(-1.470599, 53.379244),
        num_results=3,
        dist_range=5000,
        days={
            "Monday": False,
            "Tuesday": False,
            "Wednesday": False,
            "Thursday": True,
            "Friday": False,
            "Saturday": False,
            "Sunday": False,
        }
    )
    print(result[['ID', 'distance', 'name', 'opening']])
