"""Functions for handling front end requests"""
from datetime import datetime, timedelta

import geopandas as gpd
import pandas as pd
from shapely.geometry import Point
from src.backend.utils import convert_to_geodataframe, snap_to_nearest_postcode

# set the valid methods for filtering/searching and other constants
VALID_METHODS = {"postcode", "place_from"}
OD_MATRIX_PATH = "data/foodbank_postcode_od.csv"
FOODBANKS_PATH = "data/foodbank_coords.csv"

# read od matrix and foodbanks
OD_MATRIX = pd.read_csv(OD_MATRIX_PATH)
FOODBANKS = pd.read_csv(FOODBANKS_PATH)


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
    """finds and filters to nearest foodbanks, by distance and days available.

    Parameters
    ----------
    method : str
        method to use to interprut starting location. must be one of
        {"postcode", "place_from"}
    postcode : str, optional
        starting postcode, by default "S1 1AD"
    place_from : type[Point], optional
        starting lat/long coordinates, by default Point(-1.470599, 53.379244)
    dist_range : float, optional
        maximum desirable distance in meters, by default 5000
    days : dict, optional
        days of the week showing user availability, by default { "Monday":
        True, "Tuesday": True, "Wednesday": True, "Thursday": True, "Friday":
        True, "Saturday": True, "Sunday": True,}
    num_results : int, optional
        maximum number of results to return, by default 20

    Returns
    -------
    gpd.GeoDataFrame
        nearest foodbanks, sorted by distances, within a users' range and day
        request. Contains columns:
            - 'ID' unique identifier for foodbank
            - 'distance' (distance between start location and
            foodbank in meters)
            - 'name' foodbank name
            - 'address' foodbank address
            - 'postcode' foodank postcode
            - 'phone' foodbank phone number
            - 'email' foodbank email
            - 'website' foodbank website
            - 'opening' foodbank opening/closing times as a string
            - 'referral_required' whether or not a referral is required to use
            the foodbank.
            - 'deliver_option' whether or not a delivery option is available
            - 'lat' foodbank lattitude in CRS EPSG 4326
            - 'long' foodbank longitude in CRS EPSG 4326
            - 'geometry' foodbank geometry in CRS EPSG 4326
        Note: this dataframe will be empty if no foodbanks are found

    Raises
    ------
    ValueError
        when invalid `method` argument is provided.
    """

    # capture error when incorrect method is provided
    if method not in VALID_METHODS:
        raise ValueError(
            f"{method} is not a valid method. Expecting one of {VALID_METHODS}"
        )

    # handle snapping a place to the nearest post code
    if method == "place_from":
        postcode = snap_to_nearest_postcode(place_from)["postcode"]
    
    # filter to near by foodbanks and sort by distance
    near_foodbanks = OD_MATRIX[
        (OD_MATRIX.postcode == postcode) & (OD_MATRIX.distance <= dist_range)
    ].drop(columns=['postcode']).sort_values('distance').reset_index(drop=True)

    # merge on foodbank information
    foodbanks_df = near_foodbanks.merge(FOODBANKS, on="ID", how="left")

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
    method: str,
    postcode: str = "S1 1AA",
    place_from: type[Point] = Point(-1.470599, 53.379244),
    dist_range: float = 5000,     # 5km
    time_stamp: datetime = datetime.now(),
    num_results: int = 20
) -> gpd.GeoDataFrame:
    """finds and filters to nearest foodbanks by distance, and returns
    them sorted by the next 'available'/open foodbank.

    Parameters
    ----------
    method : str
        method to use to interprut starting location. must be one of
        {"postcode", "place_from"}
    postcode : str, optional
        starting postcode, by default "S1 1AD"
    place_from : type[Point], optional
        starting lat/long coordinates, by default Point(-1.470599, 53.379244)
    dist_range : float, optional
        maximum desirable distance in meters, by default 5000
    time_stamp : datetime, optional
        timestamp denoting start time to next open/available foodbank, by
        default `datetime.now()`
    num_results : int, optional
        maximum number of results to return, by default 20

    Returns
    -------
    gpd.GeoDataFrame
        nearest foodbanks, sorted by distances, within a users' range and day
        request. Contains columns:
            - 'ID' unique identifier for foodbank
            - 'distance' (distance between start location and
            foodbank in meters)
            - 'name' foodbank name
            - 'address' foodbank address
            - 'postcode' foodank postcode
            - 'phone' foodbank phone number
            - 'email' foodbank email
            - 'website' foodbank website
            - 'opening' foodbank opening/closing times as a string
            - 'referral_required' whether or not a referral is required to use
            the foodbank.
            - 'deliver_option' whether or not a delivery option is available
            - 'lat' foodbank lattitude in CRS EPSG 4326
            - 'long' foodbank longitude in CRS EPSG 4326
            - 'geometry' foodbank geometry in CRS EPSG 4326
        Note: this dataframe will be empty if no foodbanks are found

    Raises
    ------
    ValueError
        when invalid `method` argument is provided.
    """

    # capture error when incorrect method is provided
    if method not in VALID_METHODS:
        raise ValueError(
            f"{method} is not a valid method. Expecting one of {VALID_METHODS}"
        )

    # handle snapping a place to the nearest post code
    if method == "place_from":
        postcode = snap_to_nearest_postcode(place_from)["postcode"]

    foodbanks_nearby = OD_MATRIX[(OD_MATRIX["postcode"] == postcode) &
                                 (OD_MATRIX["distance"] <= dist_range)]

    foodbanks_nearby = pd.merge(
        foodbanks_nearby[["ID", "distance"]], FOODBANKS, on="ID"
    )

    days = []

    for x in range(1, 7):
        days.append((time_stamp + timedelta(days=x)).strftime("%A"))

    df = foodbanks_nearby[
        foodbanks_nearby["opening"].str.contains(time_stamp.strftime("%A"))
    ].sort_values("distance")
    for day in days:
        df2 = foodbanks_nearby[
            foodbanks_nearby["opening"].str.contains(day)
        ].sort_values("distance")
        df = pd.concat([df, df2])

    out_df = df.reset_index(drop=True).head(num_results)
    foodbanks_gdf = convert_to_geodataframe(out_df, crs="EPSG:4326")

    return foodbanks_gdf
