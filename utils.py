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
    for client, client_info in clients.items(): #recorremos todos los clientes que hay conectados -> obtenemos nombre del cliente e informacion suya
        with Client(address=(client_info['address'], client_info['port']),
                    authkey=client_info['authkey']) as conn: # abrimos una conexion con el cliente en la dirección y en el puerto dados
            if not client == username: #distinguimos el caso en el que el cliente es el propio usuario que manda el mensaje (remitente) o no lo es
                conn.send(('msg', (username, msg), timestamp)) #los mensajes enviados siempre son una tupla de 3 elementos. El primer elemento siempre es el tipo de dato que se envía
            else: #si coinciden ambos, mandamos un 0 en lugar del nombre del usuario remitente para distinguir entre los mensajes enviados y recibidos
                conn.send(('msg', (0, msg), timestamp))

# Enviar mensaje privado a un usuario específico
def send_msg_private(sender, recipient, msg, clients, timestamp):
    print(f'[{timestamp}] {sender} a {recipient}: {msg}')
    if recipient in clients: #si el receptor es uno de los clientes conectados
        client_info = clients[recipient] #obtenemos el diccionario con la info del receptor
        with Client(address=(client_info['address'], client_info['port']),
                    authkey=client_info['authkey']) as conn: #establecemos conexión con el receptor para mandarle el mensaje
            conn.send(('msg', (f'{sender} (privado)', msg), timestamp))
    else: #si no lo está -> mandamos un mensaje de error
        print(f"Error: Usuario {recipient} no encontrado.")

# Enviar estado de conexión a todos los usuarios
def send_status_all(username, status, clients, timestamp): #se ejecutará cuando un usuario cambie su estado
    if status == "conection":
        msg = f'[{timestamp}] {username} se ha conectado.' #mensaje que se enviará a todos los clientes del chat
        msg_user = f'[{timestamp}] Te has conectado' #mensaje que se enviará al usuario
    else:
        msg = f'[{timestamp}] {username} se ha desconectado.'
        msg_user = f'[{timestamp}] Te has desconectado'

    print(msg) #se loguea el mensaje en la pantalla donde se esté ejecutando el servidor

    for client, client_info in clients.items(): #recorremos todos los clientes que están conectados, obtenemos su información y establecemos conexion
        with Client(address=(client_info['address'], client_info['port']),
                    authkey=client_info['authkey']) as conn:
            if not client == username: #si el cliente actual no coincide con el que estamos analizando -> enviamos msg
                conn.send(('status', msg, timestamp))
            else: #si el cliente actual coincide con el que estamos analizando -> enviamos msg_user
                conn.send(('status', msg_user, timestamp))

# Enviar archivo a todos los usuarios
def send_file_all(username, file_data, clients, timestamp): #usuario envía a todos un archivo
    print(f'[{timestamp}] {username} envió el archivo "{file_data["name"]}"')
    for client, client_info in clients.items(): #recorremos todos los clientes que están conectados, obtenemos su información y establecemos conexion
        with Client(address=(client_info['address'], client_info['port']),
                    authkey=client_info['authkey']) as conn:
            if not client == username: #si el usuario remitente no es el cliente actual -> mandamos el archivo 
                conn.send(('file', (username, file_data), timestamp))
            else: #si el usuario remitente es el cliente actual -> se le mostrará un mensaje de que el archivo fue enviado
                msg = f'Se ha enviado el archivo "{file_data["name"]}".'
                conn.send(('msg', (1, msg), timestamp))

# Enviar archivo privado a un usuario específico
def send_file_private(sender_username, receiver_username, file_data, clients, timestamp):
    print(f'[{timestamp}] {sender_username} envió el archivo "{file_data["name"]}" a {receiver_username}')
    client_info = clients.get(receiver_username) #comprobamos si el receptor es un cliente conectado. Si está conectado -> obtenemos su informacion directamente. Si no -> se evaúa a None
    if client_info: #el receptor está conectado
        with Client(address=(client_info['address'], client_info['port']),
                    authkey=client_info['authkey']) as conn: #establecemos conexion con el receptor y le mandamos el archivo
            conn.send(('file', (sender_username, file_data), timestamp))
    else: #si no está conectado, client_info es None, por lo que si no encuentra el usuario -> lanzamos mensaje error
        print(f"Error: Usuario {receiver_username} no encontrado")
