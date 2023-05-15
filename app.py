from flask import Flask, render_template, request
import pandas as pd
from src.backend.frontend_handler import foodfind_asap, foodfind_nearest
from datetime import datetime, timedelta
from shapely.geometry import Point
import re

MAP_CENTRE = [53.4, -1.4]
MAP_ZOOM = 11
pc_data = pd.read_csv("data/shef_pc_coords_lookup.csv")
pc_list = pc_data["postcode"].to_list()


def html_table(df):
    df_out = df.assign(rank=range(len(df)))
    df_out["rank"] = df_out["rank"] + 1
    df_html = df_out.rename(
        columns={"referral_required": "referral", "delivery_option": "delivery"}
    )[
        [
            "rank",
            "name",
            "address",
            "postcode",
            "opening",
            "referral",
            "delivery",
            "phone",
            "email",
            "website",
        ]
    ].to_html(
        classes="table table-striped table-bordered table-sm table-hover", index=False
    )
    return df_html


app = Flask(__name__)


@app.route("/")
def index():
    return render_template(
        "index.html",
        pc_list=pc_list,
        foodbanks="",
        df=pd.DataFrame(),
        map_centre=MAP_CENTRE,
        map_zoom=MAP_ZOOM,
        marker=[0, 0],
    )


@app.route("/search", methods=["POST"])
def search():
    query_type = request.form["query_type"]
    query_location = request.form["query_location"]
    map_centre = MAP_CENTRE
    map_zoom = MAP_ZOOM
    marker = [0, 0]
    if query_location == "postcode":
        postcode = request.form["pcode"]
        if postcode in pc_list:
            ind = pc_list.index(postcode)
            marker = [pc_data.lat[ind], pc_data.long[ind]]
            map_centre = marker
            map_zoom = MAP_ZOOM + 2

    else:
        coords = re.search(
            r"LatLng\(([0-9\.-]+), ([0-9§.-]+)\)", request.form["coords"]  # noqa:W605
        )
        if coords:
            gr = coords.groups()
            coords = Point(float(gr[1]), float(gr[0]))
            marker = [float(gr[0]), float(gr[1])]
            map_centre = marker
            map_zoom = MAP_ZOOM + 2
        else:
            coords = Point(0, 0)

    # TODO check valid location input and display error?

    range = float(request.form["range_val"])
    days = {
        x: (True if x in request.form.keys() else False)
        for x in [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday",
        ]
    }
    print(days)
    # query_backend( above parameters)
    if query_type == "nearest":
        if query_location == "postcode":
            foodbanks = foodfind_nearest(
                method="postcode", postcode=postcode, dist_range=range * 1000, days=days
            )
        else:
            foodbanks = foodfind_nearest(
                method="place_from",
                place_from=coords,
                dist_range=range * 1000,
                days=days,
            )
    else:
        if query_location == "postcode":
            foodbanks = foodfind_asap(
                method="postcode", postcode=postcode, dist_range=range * 1000
            )
        else:
            foodbanks = foodfind_asap(
                method="place_from", place_from=coords, dist_range=range * 1000
            )

    foodbanks["color"] = "cyan"  # based on days to opening
    msk_today = foodbanks.opening.str.contains(datetime.now().strftime("%A"))
    msk_tomorrow = foodbanks.opening.str.contains(
        (datetime.now() + timedelta(days=1)).strftime("%A")
    )
    foodbanks.loc[msk_today | msk_tomorrow, "color"] = "blue"

    return render_template(
        "index.html",
        pc_list=pc_list,
        foodbanks=html_table(foodbanks),
        df=foodbanks,
        map_centre=map_centre,
        map_zoom=map_zoom,
        marker=marker,
    )


if __name__ == "__main__":
    app.run(debug=True)
