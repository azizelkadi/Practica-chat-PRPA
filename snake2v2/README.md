
# Juego de Snake para dos jugadores

En esta carpeta se encuentar los archivos a la práctica complementaria consistente en la realización de un juego de ejecución distribuida, en nuestro caso hemos creado un juego basado en el tradicional *snake* con modificaciones para que dos jugadores puedan participar e interactuar simultámente. 

<br> 

## snake_sala.py

Este archivo se encarga de crear una sala común que recibe los *comandos* enviados por los jugadores. Estos comandos pueden estar relacionados con tareas de movimiento `up`, `down`, `left`, `right`, `go`, o de colisión: `eat` (con la manzana), `collide` (con la otra serpiente). 

<br>

Para ello, es crucial crear 3 objetos distintos:

1) `Player`. Guarda la información referente al lado del jugador (`side`), la posición de la cabeza de la serpiente (`pos`), una lista con las posiciones que constituyen el cuerpo de la serpiente en ese instante (`body`), la dirección en la que avanza la serpiente (`direction`) y la dirección a la que quiere cambiar (`change_to`). Esta última es muy importante para simular el movimiento del juego tradicional pues no queremos que se puedan realizar cambios buscos (e.g. `RIGTH -> LEFT`).

Este objeto tiene métodos para acceder y cambiar algunas de sus variables internas. Además, se han creado los siguientes métodos para actualizar la posición del jugador en el tablero según los inputs introducidos:

- `go`. La serpiente debe moverse siempre por lo que este comando siempre será ejecutado cada vez que intercambiemos la información del juego entre la sala y los jugadores. Esta función se encarga de actualizar la dirección de movimiento de la serpietne asegurando que no se produzcan cambios bruscos.

- `move`. Según el comando de movimiento en el tablero actualizamos la posición de la cabeza de la serpiente, con la peculiaridad de que si llegamos a los bordes del tablero en lugar de terminarse el juego, avanzará por el lado opuesto como si vivieramos en un mundo de *posición modular*. Por ejemplo, si un jugador se choca con el lado derecho su cabeza y cuerpo irán apareciendo por el lado izquierdo.

- `update`. Esta función se utiliza para retirar la cola siempre que haya sido comida por el otro usuario. No añadiremos estos bloques a nuestra serpiente para facilitar que puedan mantenerse partidas prolongadas, pero si sumaremos los puntos correspondientes al marcador de la serpiente correspondinete.

<br>

2) `Apple`. Guarda la posición de la manzana `pos` y una variable booleana `spawn` que indica si debe reaparacer en el tablero por haber sido consumida por alguno de los dos jugadores. De igual manera, se tienen varios métodos para acceder a estas variables internas y se tiene una función `update(self,player)` para indicar que ha sido consumida y tener el efecto deseado sobre el cuerpo de la serpiente que ha interactuado con el objeto.

<br> 

3) `Game`. Guarda la lista de los dos jugadores `players`, la manazana del juego `apple`, el marcador `score`, una variable que indica si el juego está en ejecución y un semáforo binario para asegurar la atomicidad de algunas de las operaciones definidas en este objeto. Estas operaciones son `go`, `move`, `moveUp`, `moveDown`, `moveRight`, `moveLeft`, `apple_interaction` para cuando la manzana es comida y `snakes_interaction` para cuando ha habido una colisión entre las serpientes. Además, cuenta con una función `get_info` para transmitir a los jugadores la información global, para lo que es imprescindible que las variables de este objeto sean variables compartias mediante un `Manager`.

<br>

Para la ejecución de la sala común, se espera que dos ususiaros se conecten al servidor mediante la introdución de una dirección IP (en caso de no ser introducida se eligirá `127.0.0.1` por defecto). Tras esto el juego irá avanzando realizando un bucle de varios procesos: la sala manda la información a los jugadores, los jugadores envián comandos a la sala y la sala recalcula la posición de los objetos del tablero para después enviar de nuevo la información actualizada.

## snake_player.py
