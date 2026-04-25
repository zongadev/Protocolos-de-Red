from gc import enable
import socket
import os
import threading
import struct

HOST = '127.0.0.1'   # Cambiar IP si el servidor está en otra máquina
PORT = 6667          # Puerto del servidor

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
def escuchar():
    data = sock.recv(1024)
    if data:
        print("Servidor: ",data.decode('utf-8'))

if __name__ == "__main__":
    try:
        print("Creando socket...")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)  # Tiempo máximo de espera para recibir datos

        print(f"Conectando a servidor en {HOST}:{PORT}...")
        sock.connect((HOST, PORT))
        threading.Thread(target=escuchar, daemon=True).start()
        print("Elija una opcion")
        print("(1)- Enviar \n (2)- Salir")
        op = input()
        while (op not in ['1','2']):
            op = input()
        while op!= 2:
            if((op==1)):
                threading.Thread(target=enviar_archivo, daemon=True).start()
            if(op==2):
                break 

    except ConnectionRefusedError:
        print("No se pudo conectar al servidor. Verifique si está activo.")
    except Exception as e:
        print(f"Ocurrió un error: {e}")
    finally:
        sock.close()
        print("Paso 6: Socket cerrado. Cliente finalizado.")

