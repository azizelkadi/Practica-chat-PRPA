
# Juego de Snake para dos jugadores

En esta carpeta se encuentar los archivos a la práctica complementaria consistente en la realización de un juego de ejecución distribuida, en nuestro caso hemos creado un juego basado en el tradicional *snake* con modificaciones para que dos jugadores puedan participar e interactuar simultámente. 

<br>

## snake_sala.py

Este archivo se encarga de crear una sala común que recibe los *comandos* enviados por los jugadores. Estos comandos pueden estar relacionados con tareas de movimiento `up`, `down`, `left`, `right`, `go`, o de colisión: `eat` (con la manzana), `collide` (con la otra serpiente). 

Para ello, es crucial crear 3 objetos distintos:
- `Player`. Guarda la información referente al lado del jugador (`side`), la posición de la cabeza de la serpiente (`pos`), una lista con las posiciones que constituyen el cuerpo de la serpiente en ese instante (`body`), la dirección en la que avanza la serpiente (`direction`) y la dirección a la que quiere cambiar (`change_to`). Esta última es muy importante para simular el movimiento del juego tradicional pues no queremos que se puedan realizar cambios buscos (e.g. `RIGTH -> LEFT`).

## snake_player.py
