from flask import Flask
from flask import render_template
from flask import jsonify

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/query_vehicle_data')
def query_vehicle_data():
    return jsonify({'ok': True})


if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host='0.0.0.0', port=8888, debug=True)