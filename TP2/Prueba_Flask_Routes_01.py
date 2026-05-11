from flask import Flask,jsonify
import basedatos as db
from datetime import date

app = Flask(__name__)

sensors = db.obtener_sensores()

@app.route('/')
def index():
    return "Hola"

@app.route("/sensors", methods=['GET'])
def get():
    return jsonify ({'Sensors':sensors})

@app.route("/sensors/<int:id>", methods=['GET'])
def get_measure(id):
    return jsonify ({'Sensors':sensors[id]})

@app.route("/sensors", methods=['POST'])
def create():
    co2= input("Ingrese el nivel de CO2")
    temp= input("Ingrese la temperatura")
    hum= input("Ingrese el nivel de humedad")
    today= date.today().isoformat()
    sensor = [{"co2":co2,"temp":temp,"hum":hum,"date":date}]
    db.crear_sensor(co2,temp,hum,today)
    return jsonify ({'Created'})

@app.route("/sensors/<int:id>", methods=['PUT'])
def sensor_update(id):
    sensors[id]['fecha'] = "22/9/2021"
    return jsonify ({'Sensor':sensors[id]})

@app.route("/sensors/<int:id>", methods=['DELETE'])
def sensor_delete(id):
    sensors.remove(sensors[id])
    return jsonify ({'result':True})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
