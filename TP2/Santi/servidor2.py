from flask import Flask, jsonify, request
import database2 as db

app = Flask(__name__)

# Asegura que la tabla exista al arrancar
db.crear_tabla()

@app.route("/")
def index():
    # Mantenemos tu interfaz visual de Bootstrap
    return """
    <!doctype html>
    <html lang="es">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Flask Sensores Pro</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body class="bg-light">
    <nav class="navbar navbar-dark bg-dark mb-4">
        <div class="container">
            <span class="navbar-brand mb-0 h1">Servidor Flask - Sistema de Lecturas</span>
        </div>
    </nav>
    <div class="container">
        <div class="alert alert-success">Servidor activo en el puerto 5001. Base de datos: lectura_sensores</div>
        <div class="row g-4">
            <div class="col-md-6">
                <div class="card shadow-sm">
                    <div class="card-header bg-primary text-white">Login por POST</div>
                    <div class="card-body">
                        <form action="/login" method="post">
                            <div class="mb-3">
                                <label class="form-label">Nombre</label>
                                <input type="text" name="nombre" class="form-control" placeholder="javier">
                            </div>
                            <div class="mb-3">
                                <label class="form-label">Clave</label>
                                <input type="password" name="clave" class="form-control" placeholder="abc">
                            </div>
                            <button type="submit" class="btn btn-primary">Ingresar</button>
                        </form>
                    </div>
                </div>
            </div>
            <div class="col-md-6">
                <div class="card shadow-sm">
                    <div class="card-header bg-success text-white">Accesos rápidos</div>
                    <div class="card-body">
                        <a href="/login_get?nombre=javier&clave=abc" class="btn btn-outline-primary mb-2 w-100">Probar Login GET</a>
                        <a href="/sensors" class="btn btn-outline-success mb-2 w-100">Ver JSON (Todas las lecturas)</a>
                    </div>
                </div>
            </div>
        </div>
    </div>
    </body>
    </html>
    """

# --- RUTAS DE LOGIN (Requisito: Comparar GET vs POST) ---

@app.route("/login", methods=["POST"])
def login_post():
    # Uso de request.form para datos ocultos en el cuerpo
    nombre = request.form.get("nombre")
    clave = request.form.get("clave")
    return jsonify({"metodo": "POST", "usuario": nombre, "info": "Clave enviada de forma segura en el body"}), 200

@app.route("/login_get", methods=["GET"])
def login_get():
    # Uso de request.args para datos visibles en la URL
    nombre = request.args.get("nombre")
    clave = request.args.get("clave")
    return jsonify({"metodo": "GET", "usuario": nombre, "clave_expuesta": clave}), 200

# --- CRUD DE SENSORES (Con todos los campos nuevos) ---

@app.route("/sensors", methods=["GET"])
def listar_sensores():
    sensores = db.obtener_sensores()
    return jsonify({"sensors": sensores}), 200

@app.route("/sensors", methods=["POST"])
def crear_sensor():
    if not request.is_json:
        return jsonify({"error": "Debe enviar JSON"}), 415

    data = request.get_json()
    
    # Mapeamos todos los campos requeridos
    nuevo_sensor = {
        "co2": data.get("co2"),
        "temp": data.get("temp"),
        "hum": data.get("hum"),
        "fecha": data.get("fecha"),
        "lugar": data.get("lugar"),
        "altura": data.get("altura"),
        "presion": data.get("presion"),
        "presion_nm": data.get("presion_nm"),
        "temp_ext": data.get("temp_ext")
    }

    id_generado = db.crear_sensor(nuevo_sensor)
    nuevo_sensor["id"] = id_generado

    return jsonify({"mensaje": "Lectura creada", "sensor": nuevo_sensor}), 201

@app.route("/sensors/<int:id>", methods=["GET"])
def consultar_sensor(id):
    sensor = db.obtener_sensor_por_id(id)
    if not sensor:
        return jsonify({"error": "Sensor no encontrado"}), 404
    return jsonify({"sensor": sensor}), 200

@app.route("/sensors/<int:id>", methods=["PUT"])
def modificar_sensor(id):
    if not request.is_json:
        return jsonify({"error": "Debe enviar JSON"}), 415

    sensor_existente = db.obtener_sensor_por_id(id)
    if not sensor_existente:
        return jsonify({"error": "Sensor no encontrado"}), 404

    data = request.get_json()

    # Actualizamos campos permitiendo mantener los valores viejos si no se envían nuevos
    sensor_actualizado = {
        "co2": data.get("co2", sensor_existente["co2"]),
        "temp": data.get("temp", sensor_existente["temp"]),
        "hum": data.get("hum", sensor_existente["hum"]),
        "fecha": data.get("fecha", sensor_existente["fecha"]),
        "lugar": data.get("lugar", sensor_existente["lugar"]),
        "altura": data.get("altura", sensor_existente["altura"]),
        "presion": data.get("presion", sensor_existente["presion"]),
        "presion_nm": data.get("presion_nm", sensor_existente["presion_nm"]),
        "temp_ext": data.get("temp_ext", sensor_existente["temp_ext"])
    }

    db.actualizar_sensor(id, sensor_actualizado)
    sensor_actualizado["id"] = id
    
    return jsonify({"mensaje": "Actualizado correctamente", "sensor": sensor_actualizado}), 200

@app.route("/sensors/<int:id>", methods=["DELETE"])
def eliminar_sensor(id):
    if db.eliminar_sensor(id):
        return jsonify({"mensaje": "Sensor eliminado", "result": True}), 200
    return jsonify({"error": "No se pudo eliminar o no existe"}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)