from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/map', methods=['POST'])
def map():
    lat = request.form['lat']
    lng = request.form['lng']
    return render_template('map.html', lat=lat, lng=lng)

if __name__ == '__main__':
    app.run(debug=True)
