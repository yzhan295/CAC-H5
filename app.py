from flask import Flask
from flask import render_template
from flask import jsonify
import my_can_bus
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
    return jsonify({'ok': True, 'ac_temp': my_can_bus.ac_temp, 'gear_d_pos': my_can_bus.gear_d_pos})


@app.route('/ac_temp_add')
def ac_temp_add():
    my_can_bus.ac_temp_add()
    return jsonify({'ok': True})


@app.route('/ac_temp_minus')
def ac_temp_minus():
    my_can_bus.ac_temp_minus()
    return jsonify({'ok': True})


@app.route('/ac_front_power_on_off')
def ac_front_power_on_off():
    my_can_bus.ac_front_power_on_off()
    return jsonify({'ok': True})


if __name__ == '__main__':
    receive_can_message_thread = threading.Thread(target=my_can_bus.receive_can_message)
    receive_can_message_thread.start()
    app.run(host='0.0.0.0', port=8888, debug=True)