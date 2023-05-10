# %%
# define
from datetime import datetime, timedelta
from shapely.geometry import Point
import geopandas as gpd
import pandas as pd


def foodfind_nearest(
    place_from=Point(53.2251, 1.2813),
    dist_range=None,
    days={
        "Monday": True,
        "Tuesday": True,
        "Wednesday": True,
        "Thursday": True,
        "Friday": True,
        "Saturday": True,
        "Sunday": True,
    },
    num_results=20,
):
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
    return None


def foodfind_asap(
    od_matrix,
    foodbank_table,
    post_code: str = "S1 1AA",
    # place_from=Point(53.2251, 1.2813),
    dist_range: float = 5000,     # 5km
    time_stamp: datetime = datetime.now(),
    time_window: int = 1,     # today plus tomorrow
    # num_results: int = 20
) -> gpd.GeoDataFrame:
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

    days = [time_stamp.strftime("%A"),
            (time_stamp + timedelta(days=time_window)).strftime("%A")]

    foodbanks_nearby = od_matrix[(od_matrix["postcode"]==post_code) &
                                 (od_matrix["distance"]<=dist_range)].sort_values("distance")
    
    timely_foodbanks = foodbank_table[foodbank_table["opening"].str.contains("|".join(days))]
    timely_foodbanks_nearby = pd.merge(foodbanks_nearby[["ID", "distance"]], timely_foodbanks, on="ID")
    
    #foodbanks_nearby = foodbank_table[foodbank_table["ID"].isin(foodbanks_nearby)]

    #foodbanks_nearby = foodbanks_nearby[foodbanks_nearby["opening"].str.contains("|".join(days))]
    return timely_foodbanks_nearby

# %%
od_matrix = pd.read_csv("../data/foodbank_postcode_od.csv")
foodbank_table = pd.read_csv("../data/foodbank_coords.csv")

foodfind_asap(od_matrix, foodbank_table)
