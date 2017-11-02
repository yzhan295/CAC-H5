from flask import Flask
from flask import render_template
from flask import jsonify
# import my_can_bus
import threading

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/index_pad')
def index_phone():
    return render_template('index_pad.html')


@app.route('/query_vehicle_data')
def query_vehicle_data():
    return jsonify({'ok': True})


if __name__ == '__main__':
    # app.run(debug=True)
    # receive_can_message_thread = threading.Thread(target=my_can_bus.receive_can_message)
    # receive_can_message_thread.start()
    app.run(host='0.0.0.0', port=8888, debug=True)