from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)
pc_list = ["S10 2TN", "S10 2RE", "S10 2GR"]
foodbanks = pd.DataFrame(
    [
        ["London", 51.5072, -0.1275],
        ["Birmingham", 52.4800, -1.9025],
        ["Manchester", 53.4794, -2.2453],
        ["Liverpool", 53.4075, -2.9919],
        ["Portsmouth", 50.8058, -1.0872],
        ["Southampton", 50.9025, -1.4042],
        ["Nottingham", 52.9533, -1.1500],
    ],
    columns=["Name", "Long", "Lat"],
)


# %%
# %%
@app.route("/")
def index():
    return render_template("index.html", pc_list=pc_list, foodbanks=None)


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
        "index.html", pc_list=pc_list, foodbanks=foodbanks.to_html(classes="data")
    )


if __name__ == "__main__":
    app.run(debug=True)
