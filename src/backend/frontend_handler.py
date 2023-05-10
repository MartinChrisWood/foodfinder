# define
from datetime import datetime
from shapely.geometry import Point


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
