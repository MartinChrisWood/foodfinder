from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    pc_list = ["S10 2TN", "S10 2RE", "S10 2TN"]
    range = request.form["travel_range"]
    range = range + 1
    return render_template("index.html", pc_list=pc_list)


if __name__ == "__main__":
    app.run(debug=True)
