from multiprocessing.connection import Client
import os

# Función que lee la ruta del archivo y lo transforma en binario para poder ser enviado
def read_file(file_path):
    with open(file_path, 'rb') as f:
        file_data = f.read()
    file_name = os.path.basename(file_path)
    return {'name': file_name, 'data': file_data}

# Función que recibe los datos del archivo y lo escribe en un directorio local
def write_file(file_data, file_path):
    with open(file_path, 'wb') as f:
        f.write(file_data['data'])

# Enviar mensaje a todos los usuarios
def send_msg_all(username, msg, clients, timestamp):
    print(f'[{timestamp}] {username}: {msg}')
    for client, client_info in clients.items():
        with Client(address=(client_info['address'], client_info['port']),
                    authkey=client_info['authkey']) as conn:
            if not client == username:
                conn.send(('msg', (username, msg), timestamp))
            else:
                conn.send(('msg', (0, msg), timestamp))

# Enviar mensaje privado a un usuario específico
def send_msg_private(sender, recipient, msg, clients, timestamp):
    print(f'[{timestamp}] {sender} a {recipient}: {msg}')
    if recipient in clients:
        client_info = clients[recipient]
        with Client(address=(client_info['address'], client_info['port']),
                    authkey=client_info['authkey']) as conn:
            conn.send(('msg', (f'{sender} (privado)', msg), timestamp))
    else:
        print(f"Error: Usuario {recipient} no encontrado.")

# Enviar estado de conexión a todos los usuarios
def send_status_all(username, status, clients, timestamp):
    if status == "conection":
        msg = f'[{timestamp}] {username} se ha conectado.'
        msg_user = f'[{timestamp}] Te has conectado'
    else:
        msg = f'[{timestamp}] {username} se ha desconectado.'
        msg_user = f'[{timestamp}] Te has desconectado'

    print(msg)

    for client, client_info in clients.items():
        with Client(address=(client_info['address'], client_info['port']),
                    authkey=client_info['authkey']) as conn:
            if not client == username:
                conn.send(('status', msg, timestamp))
            else:
                conn.send(('status', msg_user, timestamp))

# Enviar archivo a todos los usuarios
def send_file_all(username, file_data, clients, timestamp):
    print(f'[{timestamp}] {username} envió el archivo "{file_data["name"]}"')
    for client, client_info in clients.items():
        with Client(address=(client_info['address'], client_info['port']),
                    authkey=client_info['authkey']) as conn:
            if not client == username:
                conn.send(('file', (username, file_data), timestamp))
            else:
                msg = f'Se ha enviado el archivo "{file_data["name"]}".'
                conn.send(('msg', (1, msg), timestamp))

# Enviar archivo privado a un usuario específico
def send_file_private(sender_username, receiver_username, file_data, clients, timestamp):
    print(f'[{timestamp}] {sender_username} envió el archivo "{file_data["name"]}" a {receiver_username}')
    client_info = clients.get(receiver_username)
    if client_info:
        with Client(address=(client_info['address'], client_info['port']),
                    authkey=client_info['authkey']) as conn:
            conn.send(('file', (sender_username, file_data), timestamp))
    else:
        print(f"Error: Usuario {receiver_username} no encontrado")
