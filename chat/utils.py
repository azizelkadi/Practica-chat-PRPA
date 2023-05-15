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
    # Obtenemos nombre del cliente e informacion suya
    for client, client_info in clients.items():
        # Sbrimos una conexion con el cliente en la dirección y en el puerto dados
        with Client(address=(client_info['address'], client_info['port']), authkey=client_info['authkey']) as conn:
            # Distinguimos el caso en el que el cliente es el propio usuario que manda el mensaje (remitente) o no lo es
            if not client == username:
                # Los mensajes enviados siempre son una tupla de 3 elementos
                conn.send(('msg', (username, msg), timestamp))
            else:
                # Si coinciden ambos, mandamos un 0 en lugar del nombre del usuario remitente para distinguir entre los mensajes enviados y recibidos
                conn.send(('msg', (0, msg), timestamp))

# Enviar mensaje privado a un usuario específico
def send_msg_private(sender, recipient, msg, clients, timestamp):
    print(f'[{timestamp}] {sender} a {recipient}: {msg}')
    # Si el receptor es uno de los clientes conectados
    if recipient in clients: 
        # Obtenemos el diccionario con la información del receptor
        client_info = clients[recipient] 
        # Establecemos conexión con el receptor para mandarle el mensaje
        with Client(address=(client_info['address'], client_info['port']), authkey=client_info['authkey']) as conn: 
            conn.send(('msg', (f'{sender} (privado)', msg), timestamp))
    # Mandamos un mensaje de error en caso contrario
    else:
        msg_error = f"Error: Usuario {recipient} no encontrado."
        print(msg_error)
        send_msg_private('Server', sender, msg_error + ' Usa /a para ver los usuarios conectados.', clients, timestamp)


# Enviar estado de conexión a todos los usuarios, se ejecutará cuando un usuario cambie su estado
def send_status_all(username, status, clients, timestamp): 
    if status == "conection":
        # Mensaje que se enviará a todos los clientes del chat
        msg = f'[{timestamp}] {username} se ha conectado.'
        # Mensaje que se enviará al usuario
        msg_user = f'[{timestamp}] Te has conectado'
    else:
        msg = f'[{timestamp}] {username} se ha desconectado.'
        msg_user = f'[{timestamp}] Te has desconectado'

    print(msg)

    # Recorremos todos los clientes que están conectados, obtenemos su información y establecemos conexion
    for client, client_info in clients.items():
        with Client(address=(client_info['address'], client_info['port']), authkey=client_info['authkey']) as conn:
            if not client == username:
                conn.send(('status', msg, timestamp))
            else:
                conn.send(('status', msg_user, timestamp))

# Enviar archivo a todos los usuarios
def send_file_all(username, file_data, clients, timestamp):
    print(f'[{timestamp}] {username} envió el archivo "{file_data["name"]}"')
    # Recorremos todos los clientes que están conectados, obtenemos su información y establecemos conexion
    for client, client_info in clients.items(): 
        with Client(address=(client_info['address'], client_info['port']), authkey=client_info['authkey']) as conn:
            # Si el usuario remitente no es el cliente actual -> mandamos el archivo 
            if not client == username:
                conn.send(('file', (username, file_data), timestamp))
            # Si el usuario remitente es el cliente actual -> se le avisará de que el archivo fue enviado
            else:
                msg = f'Se ha enviado el archivo "{file_data["name"]}".'
                conn.send(('msg', (1, msg), timestamp))

# Enviar archivo privado a un usuario específico
def send_file_private(sender, receiver, file_data, clients, timestamp):
    print(f'[{timestamp}] {sender} envió el archivo "{file_data["name"]}" a {receiver}')
    # Somprobamos si el receptor es un cliente conectado.
    client_info = clients.get(receiver)
    # El receptor está conectado -> enviamos archivo
    if client_info:
        with Client(address=(client_info['address'], client_info['port']), authkey=client_info['authkey']) as conn: #establecemos conexion con el receptor y le mandamos el archivo
            conn.send(('file', (sender, file_data), timestamp))
    # Si no está conectado -> lanzamos mensaje error
    else:
        msg_error = f"Error: Usuario {receiver} no encontrado."
        print(msg_error)
        send_msg_private('Server', sender, msg_error + ' Usa /a para ver los usuarios conectados.', clients, timestamp)
