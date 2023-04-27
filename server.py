from multiprocessing.connection import Listener
from multiprocessing import Process, Manager

import traceback

from utils import (send_file_all, 
                   send_file_private, 
                   send_msg_private, 
                   send_msg_all, 
                   send_status_all)

# Proceso del usuario
def serve_user(conn, username, clients):
    connected = True
    while connected:
        try:
            # Recibimos los datos
            data_type, data, timestamp = conn.recv()

            # Los datos son un mensaje
            if data_type == 'msg':

                # Salir del servidor
                if data == "quit":
                    connected = False
                    conn.close()

                # Comando
                elif data.startswith('/'):
                    command = data[1]
                    if command == 'p':
                        parts = data[3:].split(' ', 1)
                        destinatario, msg = parts
                        send_msg_private(username, destinatario, msg, clients, timestamp)
                    elif command == 'u':
                        pass
                    elif command == 't':
                        pass
                    # ... comandos personalizados (quizás podemos añadir)

                # Mensaje a todos
                else:
                    send_msg_all(username, data, clients, timestamp)

            # Los datos son un archivo
            elif data_type == 'file':

                receiver_username, file_data = data

                # Archivo a todos los usuarios
                if receiver_username == "all":
                    send_file_all(username, file_data, clients, timestamp)

                # Archivo privado
                else:
                    send_file_private(username, receiver_username, file_data, clients, timestamp)

        except EOFError:
            print("Conexión cerrada por el usuario")
            connected = False


# Función chat
def chat(ip_address, port):
    print("Iniciando...")
    with Listener(address=(ip_address, port), authkey=b"prpa") as listener:
        m = Manager()
        clients = m.dict()
        while True:
            try:
                # Tratamos de conectar con el cliente
                conn = listener.accept()

                # Recibimos y almacenamos información del usuario
                client_info, timestamp = conn.recv()
                username = client_info["username"]
                clients[username] = client_info

                # Avisamos de la conexión del nuevo usuario
                send_status_all(username, "conection", clients, timestamp)
                
                # Iniciamos el proceso del usuario
                p = Process(target=serve_user, args=(conn, username, clients))
                p.start()

            except Exception as e:
                traceback.print_exc()


if __name__ == "__main__":
    # Variables de conexión
    ip_address = "127.0.0.1"
    port = 600

    # Iniciamos el chat
    chat(ip_address, port)
