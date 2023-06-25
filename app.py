import os

import pandas as pd

from datetime import datetime, timedelta
from shapely.geometry import Point
from flask import Flask, render_template, request, redirect, url_for

from src.backend.frontend_handler import foodfind_asap, foodfind_nearest
from src.coordinates import get_coords_from_coords, get_coords_from_postcode, PC_LIST
from src.display import html_table


MAP_CENTRE = [53.4, -1.4]
MAP_ZOOM = 11


app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")


@app.route("/", methods=["GET", "POST"])
def index():
    # Handle case, no search
    if request.method == "GET":
        return render_template(
            "index.html",
            pc_list=PC_LIST,
            foodbanks="",
            df=pd.DataFrame(),
            map_zoom=MAP_ZOOM,
            marker=MAP_CENTRE,
        )
    
    # Handle case, search posted
    if request.method == "POST":
        query_type = request.form["query_type"]
        query_location = request.form["query_location"]
        map_zoom = MAP_ZOOM

        if query_location == "postcode":
            postcode = request.form["pcode"].replace(" ", "")
            map_zoom = MAP_ZOOM + 2
            marker = get_coords_from_postcode(postcode)
        
        elif query_location == "coords":
            map_zoom = MAP_ZOOM + 2
            marker = get_coords_from_coords(request.form["coords"])
            print(marker)

        else:
            pass # For now, opportunity for better work here in future
        
        # Handle case, something wrong with location
        if not marker:
            return redirect(url_for("index"))

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
        # query_backend( above parameters)
        if query_type == "nearest":
            if query_location == "postcode":
                foodbanks = foodfind_nearest(
                    method="postcode", postcode=postcode, dist_range=range * 1000, days=days
                )
            else:
                print("Looking for nearest")
                foodbanks = foodfind_nearest(
                    method="place_from",
                    place_from=Point(marker[1], marker[0]),
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
                    method="place_from", place_from=Point(marker[1], marker[0]), dist_range=range * 1000
                )

        foodbanks["color"] = "cyan"  # based on days to opening
        msk_today = foodbanks.opening.str.contains(datetime.now().strftime("%A"))
        msk_tomorrow = foodbanks.opening.str.contains(
            (datetime.now() + timedelta(days=1)).strftime("%A")
        )
        foodbanks.loc[msk_today | msk_tomorrow, "color"] = "blue"

        return render_template(
            "index.html",
            pc_list=PC_LIST,
            foodbanks=html_table(foodbanks),
            df=foodbanks,
            map_zoom=map_zoom,
            marker=marker,
        )        


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True)
