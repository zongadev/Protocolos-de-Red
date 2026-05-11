import requests
import geocoder
import requests
import database as db
from flask import Flask, jsonify, request


URL = "http://127.0.0.1:5001/sensors"

def geo_latlon():
    g = geocoder.ip("me")

    if not g.latlng:
        raise Exception("No se pudo obtener la ubicación por IP")

    lat, lon = g.latlng

    url = (
        "https://api.openweathermap.org/data/2.5/weather?"
        f"lat={lat}&lon={lon}"
        f"&appid={OPENWEATHER_API_KEY}"
        "&units=metric"
        "&lang=es"
    )

    response = requests.get(url, timeout=10)
    data = response.json()

    if str(data.get("cod")) not in ["200"]:
        raise Exception(f"Error OpenWeatherMap: {data}")

    main = data["main"]
    weather = data["weather"][0]

    temp_ext = main["temp"]
    presion = main["pressure"]
    humedad_ext = main["humidity"]
    descripcion_clima = weather["description"]

    return {
        "lat": lat,
        "lon": lon,
        "temp_ext": temp_ext,
        "presion": presion,
        "humedad_ext": humedad_ext,
        "descripcion_clima": descripcion_clima
    }

def guardarDatos():
    try:
        clima = geo_latlon()
        lectura ={
            "lugar":"Argentina",
            "altura":14,
            "presion": clima["presion"],
            "presion_nm" : 2,
            "temp_ext": clima["temp_ext"],
        }

        try:
            respuesta = requests.post(URL,json=lectura)
            if respuesta.status_code == 201:
                datos_servidor = respuesta.json()
                id_generado = datos_servidor['sensor']['id']
                print("Exito al guardar los datos")
            else:
                print(f" ERROR: Código {respuesta.status_code} - {respuesta.text}")

        except requests.exceptions.ConnectionError:
            print(f"ERROR")
    except:
        return jsonify({
            "error": "Debe enviar datos en formato JSON"
        }), 415

if __name__ == "__main__":
    guardarDatos()
