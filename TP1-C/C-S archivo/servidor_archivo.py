import socket
import threading
import time
import struct
import datetime

clientes = []
mensajes = []
clientes_lock = threading.Lock()
mensajes_lock = threading.Lock()
apagado = threading.Event()

HOST = '127.0.0.1'
PORT = 6667

    
# ========================
# SERVIDOR TCP
# ========================
def proceso_hijo(conn, addr):
    inicio_cliente = time.perf_counter()
    cliente_id = f"{addr[0]}:{addr[1]}" #addr tiene tanto ip, como puerto. id:puerto
    with clientes_lock:
        clientes.append({
        "id": cliente_id,
        "inicio": inicio_cliente})
        print("Los clientes conectados son:")
        for c in clientes:
            conectado_hace = time.perf_counter() - c["inicio"]
            print(f"     {c['id']} - conectado hace {conectado_hace:.2f} s")
    try:
        conn.send("Servidor: Conectado con cliente\n".encode('utf-8'))
        while not apagado.is_set():
            file_size = conn.recv(1024)
            if file_size:
                tamano = struct.unpack(">Q",file_size)[0] #big endian, entero sin signo.
                print(f"Recibiendo archivo de: {addr}, tamano: {tamano} bytes")
                recibido =0
                nombre_arch = f"recibido_{addr[1]}.bin"
                with open(nombre_arch, "wb") as f:
                    while recibido < tamano:
                        restante = tamano- recibido
                        capacidad_lectura = min(1024, restante)
                
                        chunk = conn.recv(capacidad_lectura)
                        if not chunk:
                            break
            
                        f.write(chunk)
                        recibido += len(chunk)
                print(f"Archivo guardado exitosamente como {nombre_arch}")
                ahora = datetime.datetime.now()
                tiempo_conectado = time.perf_counter() - inicio_cliente
                mensaje = f"Date {ahora.strftime('%Y-%m-%d %H:%M')}, tiempo conectado: {tiempo_conectado:.2f} s\n"
                msg_bytes = mensaje.encode("utf-8")
                conn.sendall(struct.pack(">I", len(msg_bytes))) #envia la longitud del mensaje
                conn.sendall(msg_bytes)

            else:
                break
    except Exception as e:
        print(f"Error con {addr}: {e}")
    finally:
        conn.close()
        cliente_id = f"{addr[0]}:{addr[1]}"
        with clientes_lock:
            for c in clientes:
                if c["id"] == cliente_id:
                    clientes.remove(c)
                    break

def servidor_tcp():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((HOST, PORT))
    sock.listen(5)
    sock.settimeout(1.0)
    print("Servidor TCP escuchando en", (HOST, PORT))
    try:
        while not apagado.is_set():
            try:
                conn, addr = sock.accept()
                threading.Thread(target=proceso_hijo, args=(conn, addr)).start()
            except socket.timeout:
                continue
    finally:
        sock.close()
        print("Servidor apagado.")

# ========================
# MAIN
# ========================
if __name__ == "__main__":
    # Inicia servidor TCP en un hilo
    threading.Thread(target=servidor_tcp, daemon=True).start()
    while 1:
        continue