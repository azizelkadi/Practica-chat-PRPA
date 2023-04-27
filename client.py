from multiprocessing.connection import Client, Listener
from multiprocessing import Process
import sys
import os
from utils import read_file, write_file
import datetime

# Función para escuchar las respuestas del servidor
def client_listener(info):
    with Listener(address=(info['address'], info['port']), authkey=info['authkey']) as cl:
        print("Conexión completada.")
        print(f"Escuchando en {info}")
        while True:
            conn = cl.accept()
            data_type, data, timestamp = conn.recv()

            # Es un mensaje
            if data_type == 'msg':
                pid, msg = data
                # No hacer nada
                if pid == 0:
                    pass

                # Mensaje del servidor
                elif pid == 1:
                    print(f'[{timestamp}] {msg}')

                # Mensaje de otro usuario
                else:
                    print(f'[{timestamp}] {pid}: {msg}')

            # Es un archivos
            elif data_type == 'file':
                pid, file_data = data

                # Guardamos archivo
                file_path = os.path.join(info['file_store'], file_data['name'])
                write_file(file_data, file_path)

                # Informar al usuario
                print(f'[{timestamp}] {pid} envió un archivo. Guardado en "{file_path}".')

            # Es un cambio de estado
            elif data_type == 'status':
                print(data)

            # data_type no es ninguno de los esperados
            else:
                print("data_type no válido")


# Función principal del cliente
def user(server_address, info):
    print('Conectando...')
    with Client(address=(server_address, 6000), authkey=b'prpa') as conn:

        # Iniciamos listener
        cl = Process(target=client_listener, args=(info,))
        cl.start()

        # Enviamos información de login al servidor
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        conn.send((info, timestamp))

        connected = True
        while connected:

            # Input del usuario
            value = input("")
            timestamp = datetime.datetime.now().strftime("%H:%M:%S")
            print(f'[{timestamp}] Yo: {value}')

            # Procesamos el envío de archivos
            if value.startswith('/f '):
                parts = value.split(' ', 2)
                
                if len(parts) == 3 and os.path.isfile(parts[2]):
                    file_data = read_file(parts[2])
                    conn.send(('file', (parts[1], file_data), timestamp))
                else:
                    print("Error: No se pudo enviar el archivo.")
            
            # Enviamos mensajes al servidor
            else:
                conn.send(('msg', value, timestamp))
                connected = (value != 'quit')
        
        # Terminamos el proceso que escucha al servidor
        cl.terminate()

    print("Te has desconectado")

# Función principal
if __name__ == '__main__':

    # Variables de configuración por defecto
    server_address = '127.0.0.1'
    client_address = '127.0.0.1'
    client_port = 6001
    file_store = "archivos_recibidos"

    # Obtenemos el puerto en caso de ser proporcionado
    if len(sys.argv) > 1:
        client_port = int(sys.argv[1])
    
    # Pedimos el nombre de usuario
    username = input("Ingresa tu número de usuario: ")

    # Iniciamos el usuario
    info = {
        'address': client_address,
        'port': client_port,
        'username': username,
        'authkey': b'prpa',
        'file_store': file_store
    }
    
    os.makedirs(file_store, exist_ok=True)
    user(server_address, info)
