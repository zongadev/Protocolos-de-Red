import database2 as db
import random
import time
from datetime import datetime

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

        # Guardar en la base de datos
        id_generado = db.crear_sensor(lectura)
        
        print(f"[{i+1}/{cantidad_capturas}] Guardado ID: {id_generado} | CO2: {lectura['co2']} | Temp: {lectura['temp']}°C")
        
        # Esperar el intervalo configurado (excepto en la última vuelta)
        if i < cantidad_capturas - 1:
            time.sleep(intervalo_segundos)

    print("--- Simulación finalizada con éxito ---")

if __name__ == "__main__":
    # Aquí puedes configurar la cantidad e intervalo
    n = int(input("¿Cuántas capturas quieres generar?: "))
    t = int(input("¿Cada cuántos segundos?: "))
    
    simular_sensores(cantidad_capturas=n, intervalo_segundos=t)