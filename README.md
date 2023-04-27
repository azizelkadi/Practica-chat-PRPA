# Chat. Práctica obligatoria de programación distribuida.

Autores: Abdelaziz el Kadi Lachehab, [completar]

Práctiga obligatoria en grupo del tema de "Programación distribuida" de la asignatura de PRPA.

<br>

# Características del chat

1. Envío de mensajes a todos los usuarios conectados.
2. Envío de mensajes privados a un usuario específico.
3. Compartir archivos con todos los usuarios conectados.
4. Compartir archivos de manera privada con un usuario específico.

<br>

# Instrucciones

## Iniciar el servidor

Para inicial el servidor, ejecute el archivo `server.py` en la máquina donde quiera alojar el servidor. Por defecto, el servidor se iniciará en la dirección IP `127.0.0.1` y el puerto `6000`.

```
python server.py
```

<br>

## Conectarse como cliente

1. Ejecute el archivo `client.py` en la máquina del cliente que quiera conectarse al chat, indicando el puerto deseado. Por defecto, el cliente se iniciará en la dirección IP `127.0.0.1` y el puerto `6001`.
```
python client.py [client_port]
```

2. Ingrese su nombre de usuario.

3. Ya está conectado al chat. Puede comenzar a enviar mensajes y archivos. Para enviar un mensaje deberá escribirlo en la terminal y pulsar Enter.

<br>

## Uso del chat

- Enviar un mensaje a todos los usuarios:

```[mensaje]```

<br>

- Enviar un mensaje privado a un usuario específico:

```/p [destinatario] [mensaje]```

<br>

- Enviar un archivo:

```/f [destinatario] [ruta_del_archivo]```

Si se indica `all` como destinatario, se enviará el archivo a todos los usuarios conectados.

<br>

- Salir del chat:

```quit```

<br>

- [pendientes de implementar más comandos]
