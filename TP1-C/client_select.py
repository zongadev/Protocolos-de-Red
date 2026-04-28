from gc import enable
import socket
import os
import threading
import struct
import traceback

HOST = '127.0.0.1'   # Cambiar IP si el servidor está en otra máquina
PORT = 1000         # Puerto del servidor


def enviar_archivo():
    file_name = input("Ingrese el nombre del archivo a enviar:")
    file_size = os.path.getsize(file_name)
    #lo mandas por chunks
    sock.sendall(file_size.to_bytes(8, byteorder='big'))

    with open(file_name,"rb") as f:
        while chunk := f.read(1024):
            sock.sendall(chunk)

    len_msg = struct.unpack(">I", sock.recv(4))[0]
    print(sock.recv(len_msg))

if __name__ == "__main__":
    try:
        print("Creando socket...")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)  # Tiempo máximo de espera para recibir datos

        print(f"Conectando a servidor en {HOST}:{PORT}...")
        sock.connect((HOST, PORT))
        op = 'Y'
        while (op=='Y'):
            print("Ingrese el nombre del archivo a enviar:")
            file_name = input()
            file_size = os.path.getsize(file_name)

            sock.sendall(struct.pack(">I", len(file_name)))
            sock.sendall(file_name.encode())

            sock.sendall(file_size.to_bytes(8, byteorder='big'))

            with open(file_name,"rb") as f:
                while chunk := f.read(1024):
                    sock.sendall(chunk)

            print(sock.recv(1024))
            op = input("Desea continuar enviando archivos? (Y/N)")
            while (op not in ['Y','N']):
                op = input()

    except ConnectionRefusedError:
        print("No se pudo conectar al servidor. Verifique si está activo.")
    except Exception as e:
        print(f"Ocurrió un error: {e}")
        traceback.print_exc()
    finally:
        sock.close()
        print("Paso 6: Socket cerrado. Cliente finalizado.")

