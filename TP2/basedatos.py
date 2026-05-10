import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.join(BASE_DIR, "dbsensores.db")


def conectar():
    return sqlite3.connect(DB_NAME)


def crear_tabla():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Sensor (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            co2 INTEGER,
            temp REAL,
            hum REAL,
            fecha TEXT
        );
    """)

    conn.commit()
    conn.close()


# CREATE
def crear_sensor(data):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO Sensor (co2, temp, hum, fecha)
        VALUES (?, ?, ?, ?)
    """, (
        data.get("co2"),
        data.get("temp"),
        data.get("hum"),
        data.get("fecha")
    ))

    conn.commit()

    nuevo_sensor = {
        "id": cursor.lastrowid,
        "co2": data.get("co2"),
        "temp": data.get("temp"),
        "hum": data.get("hum"),
        "fecha": data.get("fecha")
    }

    conn.close()

    return nuevo_sensor


# READ ALL
def obtener_sensores():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, co2, temp, hum, fecha
        FROM Sensor
    """)

    filas = cursor.fetchall()

    sensores = []

    for fila in filas:
        sensor = {
            "id": fila[0],
            "co2": fila[1],
            "temp": fila[2],
            "hum": fila[3],
            "fecha": fila[4]
        }

        sensores.append(sensor)

    conn.close()

    return sensores


# READ ONE
def obtener_sensor(sensor_id):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, co2, temp, hum, fecha
        FROM Sensor
        WHERE id = ?
    """, (sensor_id,))

    fila = cursor.fetchone()

    conn.close()

    if fila is None:
        return None

    sensor = {
        "id": fila[0],
        "co2": fila[1],
        "temp": fila[2],
        "hum": fila[3],
        "fecha": fila[4]
    }

    return sensor


# UPDATE
def actualizar_sensor(sensor_id, data):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE Sensor
        SET co2 = ?,
            temp = ?,
            hum = ?,
            fecha = ?
        WHERE id = ?
    """, (
        data.get("co2"),
        data.get("temp"),
        data.get("hum"),
        data.get("fecha"),
        sensor_id
    ))

    conn.commit()

    actualizado = {
        "id": sensor_id,
        "co2": data.get("co2"),
        "temp": data.get("temp"),
        "hum": data.get("hum"),
        "fecha": data.get("fecha")
    }

    conn.close()

    return actualizado


# DELETE
def eliminar_sensor(sensor_id):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM Sensor
        WHERE id = ?
    """, (sensor_id,))

    conn.commit()

    eliminado = cursor.rowcount > 0

    conn.close()

    return eliminado