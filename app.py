from flask import Flask, render_template, request
from markupsafe import escape


app = Flask(__name__)

@app.route("/")
def home():
    return "<p>Index page</p>"


@app.route("/hello")
def hello_world():
    return render_template("hello.html")


@app.route("/name/<name>")
def hello(name):
    return f"Hello, {escape(name)}!"


@app.route("/upload", methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        fav_color = request.form.get("fav_color")
        fav_num = request.form.get("fav_num")
        return f"{fav_color}, {fav_num}"
    
    return render_template("form.html")
