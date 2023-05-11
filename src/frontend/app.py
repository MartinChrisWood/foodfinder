from flask import Flask, render_template, request
import pandas as pd

pc_data = pd.read_csv("../../data/shef_pc_coords_lookup.csv")
pc_list = pc_data["postcode"].to_list()


foodbanks = pd.DataFrame(
    [
        ["London", 51.5072, -0.1275, "green"],
        ["Birmingham", 52.4800, -1.9025, "green"],
        ["Manchester", 53.4794, -2.2453, "blue"],
        ["Liverpool", 53.4075, -2.9919, "blue"],
        ["Portsmouth", 50.8058, -1.0872, "blue"],
        ["Southampton", 50.9025, -1.4042, "gray"],
        ["Nottingham", 52.9533, -1.1500, "gray"],
    ],
    columns=["Name", "lat", "long", "color"],
)

app = Flask(__name__)


@app.route("/")
def index():
    return render_template(
        "index.html", pc_list=pc_list, foodbanks="", df=pd.DataFrame()
    )


@app.route("/search", methods=["POST"])
def search():
    query_type = request.form["query_type"]
    postcode = request.form["pcode"]
    range = request.form["range_val"]
    days = {
        x: (1 if x in request.form.keys() else 0)
        for x in ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
    }
    # foodbanks = query_backend( above parameters)
    print(f"{query_type, days, postcode, range }")
    # return f"{query_type, days, postcode, range }"
    return render_template(
        "index.html",
        pc_list=pc_list,
        foodbanks=foodbanks.to_html(classes="data"),
        df=foodbanks,
    )


if __name__ == "__main__":
    app.run(debug=True)
