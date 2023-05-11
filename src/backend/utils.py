import geopandas as gpd
import pandas as pd
from shapely.geometry import Point

# path to postcode lookup file
PC_LOOKUP = "data/shef_pc_coords_lookup.csv"


def convert_to_geodataframe(
    df: pd.DataFrame,
    lat: str = 'lat',
    long: str = 'long',
    crs: str = 'EPSG:4326',
) -> gpd.GeoDataFrame:
    """Convert pandas dataframe to a geopandas dataframe

    Parameters
    ----------
    df : pd.DataFrame
        input pandas dataframe
    lat : str, optional
        latitude column name, by default 'lat'
    long : str, optional
        longitude column name, by default 'long'
    crs : str, optional
        coordinate reference system to use, by default 'EPSG:4326'

    Returns
    -------
    gpd.GeoDataFrame
        output geopandas dataframe
    """
    return gpd.GeoDataFrame(
        df,
        geometry=gpd.points_from_xy(x=df[long], y=df[lat]),
        crs=crs,
    )


def snap_to_nearest_postcode(
    point: type[Point] = Point(-1.470599, 53.379244)
) -> dict:
    """utility function to snap a point to the nearest postcode

    Parameters
    ----------
    point : type[Point]
        point to snap

    Returns
    -------
    dict
        closest postcode dictionary containing the keys 'postcode' (closest
        postcode, as a string), 'lat' (latitude of closest postcode), 'long'
        (longitude of closest postcode), 'geometry' (point object for closest
        postcode in CRS EPSG 27700) and 'distance' (distance between the
        provided oint and the closest postcode)

    Notes
    -----
    ['Find that postcode'](https://findthatpostcode.uk/) could be a useful
    resource. Used to QA results, and very consistent between methods. Also,
    this site offers an API. Could wrap this in as a furture TODO.
    """

    # read in post code lookup, create a geodataframe and convert CRS
    pc_lookup = pd.read_csv(PC_LOOKUP, usecols=["postcode", "lat", "long"])
    pc_lookup = convert_to_geodataframe(pc_lookup)
    pc_lookup = pc_lookup.to_crs("EPSG:27700")

    # convert point to geoseries
    point = gpd.GeoSeries(
        [point]*len(pc_lookup), crs="EPSG:4326"
    ).to_crs("EPSG:27700")

    # calculate distance to all postcodes
    pc_lookup['dist'] = pc_lookup.distance(point)

    # get closest as row within minimum distance and convert to a dict
    closest = pc_lookup.loc[pc_lookup['dist'].argmin(), :].to_dict()

    return closest
