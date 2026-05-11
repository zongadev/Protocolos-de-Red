import sqlite3

DB_NAME = "sensores.db"

def conectar():
    """Establece conexión con la base de datos y permite acceso por nombres de columna."""
    conn = sqlite3.connect(DB_NAME, timeout=10)
    # Importante: Permite manejar las filas como diccionarios
    conn.row_factory = sqlite3.Row
    return conn

def crear_tabla():
    """Crea la tabla lectura_sensores con todos los campos requeridos."""
    with conectar() as conn:
        # Activa el modo WAL para evitar el error 'database is locked'
        conn.execute('PRAGMA journal_mode=WAL;')
        
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS lectura_sensores (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                co2 INTEGER,
                temp NUMERIC,
                hum NUMERIC,
                fecha TEXT,
                lugar TEXT,
                altura NUMERIC,
                presion NUMERIC,
                presion_nm NUMERIC,
                temp_ext NUMERIC
            );
        """)
        conn.commit()

# --- FUNCIONES CRUD ---

def crear_sensor(datos):
    """Inserta una nueva lectura completa en la base de datos."""
    with conectar() as conn:
        cursor = conn.cursor()
        sql = """
            INSERT INTO lectura_sensores 
            (co2, temp, hum, fecha, lugar, altura, presion, presion_nm, temp_ext)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        parametros = (
            datos.get('co2'),
            datos.get('temp'),
            datos.get('hum'),
            datos.get('fecha'),
            datos.get('lugar'),
            datos.get('altura'),
            datos.get('presion'),
            datos.get('presion_nm'),
            datos.get('temp_ext')
        )
        cursor.execute(sql, parametros)
        return cursor.lastrowid

def obtener_sensores():
    """Retorna todas las lecturas registradas."""
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM lectura_sensores")
        # Convertimos a lista de diccionarios para que Flask pueda usar jsonify
        return [dict(fila) for fila in cursor.fetchall()]

def obtener_sensor_por_id(id_buscado):
    """Retorna una lectura específica por su ID."""
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM lectura_sensores WHERE id = ?", (id_buscado,))
        fila = cursor.fetchone()
        return dict(fila) if fila else None

def actualizar_sensor(id_buscado, datos):
    """Modifica una lectura existente."""
    with conectar() as conn:
        cursor = conn.cursor()
        sql = """
            UPDATE lectura_sensores
            SET co2 = ?, temp = ?, hum = ?, fecha = ?, lugar = ?, 
                altura = ?, presion = ?, presion_nm = ?, temp_ext = ?
            WHERE id = ?
        """
        parametros = (
            datos.get('co2'), datos.get('temp'), datos.get('hum'), 
            datos.get('fecha'), datos.get('lugar'), datos.get('altura'), 
            datos.get('presion'), datos.get('presion_nm'), datos.get('temp_ext'), 
            id_buscado
        )
        cursor.execute(sql, parametros)
        return cursor.rowcount > 0

def eliminar_sensor(id_buscado):
    """Borra una lectura de la base de datos."""
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM lectura_sensores WHERE id = ?", (id_buscado,))
        return cursor.rowcount > 0