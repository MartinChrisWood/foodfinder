""" Utility script to generate a postcode/foodbank OD matrix """


import os
import toml
import numpy as np
import pandas as pd
import geopandas as gpd


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


def main():

    # Load config
    with open(CONFIG_FILEPATH, "r") as f:
        config = toml.load(f)

    # read foodbank data
    # TODO: change this temporary usecols list to required subset
    foodbank_df = pd.read_csv(
        os.path.join(
            config["DATA_DIR"], config["FOODBANK_FILENAME"],
        ),
        usecols=["postcode", "lat", "long"],
    )

    # TODO: change this temporary preprocessing step to match required columns
    foodbank_df["ID"] = np.arange(0, len(foodbank_df))
    foodbank_df = foodbank_df[["ID", "postcode", "lat", "long"]]

    # read postcode data
    postcode_df = pd.read_csv(
        os.path.join(
            config["DATA_DIR"], config["POSTCODE_FILENAME"],
        ),
        usecols=["postcode", "lat", "long"],
    )

    # convert to geopandas dataframe
    foodbank_gdf = convert_to_geodataframe(foodbank_df)
    postcode_gdf = convert_to_geodataframe(postcode_df)

    # convert CRS to calculate correct distances
    foodbank_gdf = foodbank_gdf.to_crs("EPSG:27700")
    postcode_gdf = postcode_gdf.to_crs("EPSG:27700")

    # create cross product of geometries (all possible co-ord pairs)
    combined_gdf = foodbank_gdf[["ID", "postcode", "geometry"]].merge(
        postcode_gdf[["postcode", "geometry"]],
        how="cross",
        suffixes=["_foodbank", "_post_code"]
    )

    # get distances between foodbanks and post codes
    foodbank_coords = gpd.GeoSeries(combined_gdf["geometry_foodbank"])
    post_code_coords = gpd.GeoSeries(combined_gdf["geometry_post_code"])
    combined_gdf["distance"] = foodbank_coords.distance(post_code_coords)

    # export lookup
    out_df = combined_gdf[["ID", "postcode_post_code", "distance"]]
    out_df = out_df.rename(columns={"postcode_post_code": "postcode"})
    out_df.to_csv(
        os.path.join(
            config["DATA_DIR"], config["OD_FILENAME"]
        ),
        index=False,
    )


# pipeline configuration file
CONFIG_FILEPATH = "pipeline.toml"

if __name__ == "__main__":
    main()
