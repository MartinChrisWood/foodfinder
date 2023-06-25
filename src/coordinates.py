# Utilities for getting coordinates out of information from the user forms
import re

import pandas as pd


PC_DATA = pd.read_csv("data/shef_pc_coords_lookup.csv")
PC_LIST = PC_DATA['postcode'].str.replace(" ", "").to_list()


def get_coords_from_postcode(postcode):
    """ Helper, getting coordinate pair from postcode. """
    if postcode in PC_LIST:
        ind = PC_LIST.index(postcode)
        return [PC_DATA.lat[ind], PC_DATA.long[ind]]
    # If postcode not viable, return None
    else:
        return None


def get_coords_from_coords(coord_string):
    """ Helper, getting coordinates out of a coordinate string. """
    coords = re.search(
                r"LatLng\(([0-9\.-]+), ([0-9§.-]+)\)", coord_string  # noqa:W605
            )    
    if coords:
        gr = coords.groups()
        return [float(gr[0]), float(gr[1])]
    # If coordinate string not viable, return None
    else:
        return None
