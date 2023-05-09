
# Juego de Snake para dos jugadores

En esta carpeta se encuentar los archivos a la práctica complementaria consistente en la realización de un juego de ejecución distribuida, en nuestro caso hemos creado un juego basado en el tradicional *snake* con modificaciones para que dos jugadores puedan participar e interactuar simultámente. 

<br>

## snake_sala.py

Este archivo se encarga de crear una sala común que recibe los *comandos* enviados por los jugadores. Estos pueden ser de movimiento `up`, `down`, `left`, `right`, `go`, o de colisión: `eat` (con la manzana), `collide` (con la otra serpiente). 

## snake_player.py
