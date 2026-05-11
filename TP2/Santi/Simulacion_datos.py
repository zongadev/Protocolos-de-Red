import database2 as db
import requests
import random
import time
from datetime import datetime

URL = "http://127.0.0.1:5001/sensors"

def simular_sensores(cantidad_capturas=10, intervalo_segundos=2):
    print(f"--- Iniciando simulación: {cantidad_capturas} capturas cada {intervalo_segundos}s ---")
    
    # Aseguramos que la tabla exista
    db.crear_tabla()

    for i in range(cantidad_capturas):
        # Generar datos aleatorios realistas
        lectura = {
            "co2": random.randint(400, 900),          # ppm
            "temp": round(random.uniform(18.0, 28.0), 2), # Celsius
            "hum": round(random.uniform(30.0, 60.0), 2),  # Porcentaje
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "lugar": "Laboratorio Central",
            "altura": 10,
            "presion": 1013,
            "presion_nm": 1015,
            "temp_ext": 15.5
        }
        
       
        
        try:
            respuesta = requests.post(URL,json=lectura)
            if respuesta.status_code == 201:
                datos_servidor = respuesta.json()
                id_generado = datos_servidor['sensor']['id']
                print(f"[{i+1}/{cantidad_capturas}] Guardado ID: {id_generado} | CO2: {lectura['co2']} | Temp: {lectura['temp']}°C")
                print(f"[{i+1}/{cantidad_capturas}] ÉXITO: Guardado ID {id_generado} | CO2: {lectura['co2']}")
            else:
                print(f"[{i+1}/{cantidad_capturas}]  ERROR: Código {respuesta.status_code} - {respuesta.text}")

        except requests.exceptions.ConnectionError:
            print(f"[{i+1}/{cantidad_capturas}] ERROR")
            break 


        if i < cantidad_capturas - 1:
            time.sleep(intervalo_segundos)

    print("--- Simulación finalizada con éxito ---")

if __name__ == "__main__":
    # Aquí puedes configurar la cantidad e intervalo
    n = int(input("¿Cuántas capturas quieres generar?: "))
    t = int(input("¿Cada cuántos segundos?: "))
    
    simular_sensores(cantidad_capturas=n, intervalo_segundos=t)