import os

import pandas as pd

from flask import Flask, session, render_template, request


pc_data = pd.read_csv("../../data/shef_pc_coords_lookup.csv")
pc_list = pc_data["postcode"].to_list()


foodbanks = pd.DataFrame(
    [
        ["London", 51.5072, -0.1275, "green"],
        ["Birmingham", 52.4800, -1.9025, "green"],
        ["Manchester", 53.4794, -2.2453, "blue"],
        ["Liverpool", 53.4075, -2.9919, "blue"],
        ["Portsmouth", 50.8058, -1.0872, "blue"],
        ["Southampton", 50.9025, -1.4042, "cyan"],
        ["Nottingham", 52.9533, -1.1500, "cyan"],
    ],
    columns=["Name", "lat", "long", "color"],
)


def html_table(df):
    df_out = df.assign(Rank=range(len(df)))
    df_out["Rank"] = df_out["Rank"] + 1
    # df_out['color'] =  based on days to open
    df_html = df_out[["Rank", "Name"]].to_html(
        classes="table table-striped table-bordered table-sm table-hover", index=False
    )
    return df_html


app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route("/")
def index():
    return render_template(
        "index.html", pc_list=pc_list, foodbanks="", df=pd.DataFrame()
    )


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/search", methods=["POST"])
def search():
    if request.form:
        session['form'] = request.form
    query_type = request.form["query_type"]
    query_location = request.form["query_location"]
    postcode = request.form["pcode"]
    coords = request.form["coords"]
    # check valid location input

    range = request.form["range_val"]
    days = {
        x: (1 if x in request.form.keys() else 0)
        for x in ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
    }
    # foodbanks = query_backend( above parameters)
    print(request.form)
    if session.get("form"):
        print(session['form'])
    print(f"{query_type, query_location, postcode, coords, range, days}")
    return render_template(
        "index.html",
        pc_list=pc_list,
        foodbanks=html_table(foodbanks),
        df=foodbanks,
    )


if __name__ == "__main__":
    app.run(debug=True)
