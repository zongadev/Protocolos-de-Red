# Socket_Servidor_Select.py
# Servidor con Select()

import datetime
import select
import socket
import sys
import queue
import struct
import os
import time
# Creando un socket TCP/IP 
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.setblocking(0)

# Hago Bind del socket al puerto
dir_servidor = ('localhost', 1000)
print('iniciando en {} port {}'.format(*dir_servidor),
      file=sys.stderr)
servidor.bind(dir_servidor)

# Escucho conexiones entrantes
servidor.listen(5)

# Sockect que espero leer. aka todos los sockets
entradas = [servidor]

# Sockets que espero enviar
salidas = []

# Cola de mensajes salientes
cola_mensajes = {}

# Diccionario de tiempos
tiempos_conectado = {}


try:
    while entradas:
        
        # Espero a que al menos uno de los sockets este listo para ser procesado

        print('esperando el próximo evento', file=sys.stderr)
        readable, writable, exceptional = select.select(entradas,
                                                        salidas,
                                                        entradas)

        if not (readable or writable or exceptional):
            print('  tiempo excedido....',
                file=sys.stderr)
            continue
        # Manejo entradas
        for s in readable:

            if s is servidor:
                # Un socket "leíble" está listo para aceptar conexiones
                con, dir_cliente = s.accept()
                print('  conexión desde: ', dir_cliente,
                    file=sys.stderr)
                con.setblocking(0)
                entradas.append(con)
                tiempos_conectado[con]=time.perf_counter()
                # Le asigno a la conexión una cola en la cuál quiero enviar
                cola_mensajes[con] = queue.Queue()

            else:
                # leer tamaño del nombre
                raw = s.recv(4)
                if raw:
                    name_len = struct.unpack(">I", raw)[0]
                    # leer nombre exacto
                    file_name = s.recv(name_len).decode()
                    
                    print('  Se espera recibir el archivo {!r} desde {}'.format(
                        file_name, s.getpeername()), file=sys.stderr,
                    )
                    file_name_to_create= f"{file_name}_{s.getpeername()}"
                    file_size=s.recv(8)
                    file_size = struct.unpack(">Q",file_size)[0] #big endian, entero sin signo.
                    recibido =0
                    with open(file_name_to_create, "wb") as f:
                        while recibido <file_size:
                            restante = file_size- recibido
                            capacidad_lectura = min(1024, restante)
                    
                            chunk = s.recv(capacidad_lectura)
                            if not chunk:
                                break
                
                            f.write(chunk)
                            recibido += len(chunk)
                    print(f"Archivo {file_name_to_create} guardado exitosamente")
                    
                    ahora = datetime.datetime.now()
                    tiempo = time.perf_counter() - tiempos_conectado[s]
                    respuesta=f"Se guardo exitosamente el archivo \n FECHA: {ahora.strftime('%Y-%m-%d %H:%M')}, tiempo conectado: {tiempo:.2f} s\n"

                    cola_mensajes[s].put(respuesta.encode())
                    # Agrego un canal de salida para la respuesta
                    if s not in salidas:
                        salidas.append(s)
                else:
                    # Si está vacío lo interpreto como una conexión a cerrar
                    print('  cerrando...', dir_cliente,
                        file=sys.stderr)
                    # dejo de escuchar en la conexión
                    if s in salidas:
                        salidas.remove(s)
                    entradas.remove(s)
                    del tiempos_conectado[con]
                    s.close()

                    # Rremueve mensaje de la cola
                    del cola_mensajes[s]

        # Administro salidas
        for s in writable:
            try:
                next_msg = cola_mensajes[s].get_nowait()
            except queue.Empty:
                # No hay mensaje en espera. Dejo de controlar para posibles escrituras

                print('  ', s.getpeername(), 'cola vacía',
                    file=sys.stderr)
                salidas.remove(s)
            else:
                print(' enviando {!r} a {}'.format(next_msg, s.getpeername()), file=sys.stderr)
                s.send(next_msg)

    # Administro condiciones excepcionales"
        for s in exceptional:
            print('excepción en', s.getpeername(),
                file=sys.stderr)
            # Dejo de escuchar en las conexiones
            entradas.remove(s)
            if s in salidas:
                salidas.remove(s)
            s.close()

            # Remuevo cola de mensajes
            del cola_mensajes[s]
except KeyboardInterrupt:
    print("Apagando servidor...")

finally:
    for s in entradas:
        s.close()
        entradas.remove(s)
        del cola_mensajes[s]