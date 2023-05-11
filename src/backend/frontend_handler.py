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

# %%
od_matrix = pd.read_csv("../../data/foodbank_postcode_od.csv")
foodbank_table = pd.read_csv("../../data/foodbank_coords.csv")

foodfind_asap(od_matrix, foodbank_table)
