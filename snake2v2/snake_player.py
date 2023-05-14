from multiprocessing.connection import Client
import traceback
import pygame
import sys

BLACK = pygame.Color(0, 0, 0)
YELLOW = pygame.Color(255,255,0)
GREEN = pygame.Color(0,255,0)
colores = ["green","yellow"]

LEFT_PLAYER = 0
RIGHT_PLAYER = 1
PLAYER_COLOR = [GREEN, YELLOW]
SIDES = ["left", "right"]
SIZE = (720, 480)
X = 0
Y = 1

APPLE_COLOR = pygame.Color(255, 255, 255) # BLANCO
APPLE_SIZE = 10
FPS = 15


# Objeto para crear un jugador junto con sus propiedades
class Player():
    
    # Función para inicializar las variables de Player
    def __init__(self, side):
        self.side = side
        if side == LEFT_PLAYER:
            self.pos = [100, 50]
            self.body = [[100, 50], [90, 50], [80, 50], [70, 50]]
        else:
            self.pos = [100, 250]
            self.body = [[100, 250], [90, 250], [80, 250], [70, 250]]
        self.direction = "right"
        self.change_to = self.direction

    # Función para obtener la posición de la cabeza de Player
    def get_pos(self):
        return self.pos

    # Función para obtener el lado de Player
    def get_side(self):
        return self.side

    # Función para cambiar la posición de la cabeza de Player
    def set_pos(self, pos):
        self.pos = pos

    # Función para obtener la lista de posiciones que ocupa el cuerpo de Player
    def get_body(self):
        return self.body
    
    # Función para cambiar la lista de posiciones que ocupa el cuerpo de Player
    def set_body(self, body):
        self.body = body

    # Función 'str' para el objeto Player
    def __str__(self):
        return f"P<{SIDES[self.side], self.pos}>"
    
    
# Objeto para crear la manzanan del juego junto con sus propiedades
class Apple():
    
    # Función para inicializar las variables de Apple
    def __init__(self):
        self.pos = [None, None]
        self.spawn = True
           
    # Función para obtener la posición de Apple         
    def get_pos(self):
        return self.pos

    # Función para cambiar la posición de Apple
    def set_pos(self, pos):
        self.pos = pos

    # Función para obtener el valor de la variable 'spawn' de Apple
    def get_spawn(self):
        return self.spawn
    
    # Función para cambiar el valor de la variable 'spawn' de Apple
    def set_spawn(self, spawn):
        self.spawn = spawn

    # Función 'str' para el objeto Apple
    def __str__(self):
        return f"A<{self.pos}>"


# Objeto para crear el juego con dos Players y un Apple
class Game():
    
    # Función para inicializar las variables de Game
    def __init__(self):
        self.players = [Player(i) for i in range(2)]
        self.apple = Apple()
        self.score = [0,0]
        self.running = True

    # Función para obtener el objeto Player de Game según su lado
    def get_player(self, side):
        return self.players[side]
    
    # Función para cambiar la posición de la cabeza de un Player según su lado
    def set_pos_player(self, side, pos):
        self.players[side].set_pos(pos)

    # Función para cambiar el cuerpo de un Player según su lado
    def set_body_player(self, side, body):
        self.players[side].set_body(body)

    # Función para obtener el objeto Apple de Game
    def get_apple(self):
        return self.apple

    # Función para cambiar la posición del objeto Apple de Game
    def set_apple_pos(self, pos):
        self.apple.set_pos(pos)

    # Funcíon para obtener el marcador de Game
    def get_score(self):
        return self.score

    # Función para cambiar el marcador de Game
    def set_score(self, score):
        self.score = score

    # Función para actualizar el Game según la información recibida de la sala
    def update(self, gameinfo):
        self.set_pos_player(LEFT_PLAYER, gameinfo['pos_left_player'])
        self.set_pos_player(RIGHT_PLAYER, gameinfo['pos_right_player'])
        self.set_body_player(LEFT_PLAYER, gameinfo['body_left_player'])
        self.set_body_player(RIGHT_PLAYER, gameinfo['body_right_player'])
        self.set_apple_pos(gameinfo['pos_apple'])
        self.set_score(gameinfo['score'])
        self.running = gameinfo['is_running']

    # Función que nos dice si el juego se encuentra en ejecución
    def is_running(self):
        return self.running

    # Función que sirve para detener la ejecución del juego
    def stop(self):
        self.running = False

    # Función 'str' para el objeto Game
    def __str__(self):
        return f"G<{self.players[RIGHT_PLAYER]}:{self.players[LEFT_PLAYER]}:{self.apple}>"


# Objeto para crear los sprites de una serpiente del juego
class Snake(pygame.sprite.Sprite):
    
    # Función para inicializar las variables para un objeto Player
    def __init__(self, player):
        super().__init__()
        self.image = pygame.Surface((SIZE[X], SIZE[Y]))  # creamos el tablero
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)  # se establece el color del tablero
        self.player = player
        color = PLAYER_COLOR[self.player.get_side()]
        body = player.body
        
        # Coloreado del píxeles del cuerpo de la serpiente en el tablero creado
        for pos in body:
            pygame.draw.rect(self.image, color, pygame.Rect(pos[0], pos[1], 10, 10))
        self.rect = self.image.get_rect()
        self.update() 

    # Función para actualizar el coloreado de la serpiente según la nueva información
    def update(self):
        player = self.player
        color = PLAYER_COLOR[self.player.get_side()]
        self.image.fill(BLACK)
        for pos in player.body:
            pygame.draw.rect(self.image, color, pygame.Rect(pos[0]%SIZE[X], pos[1]%SIZE[Y], 10, 10))

    # Función 'str' para el objeto Snake
    def __str__(self):
        return f"S<{self.player}>"
    

# Objeto para crear los sprites de la manzana del juego
class AppleSprite(pygame.sprite.Sprite):
    
    # Función para inicializar las variables para un objeto Apple
    def __init__(self, apple):
        super().__init__()
        self.apple = apple
        self.image = pygame.Surface((APPLE_SIZE, APPLE_SIZE))  # cuerpo de Apple
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)
        
        # Coloreamos los píexeles del cuerpo de la manzana
        pygame.draw.rect(self.image, APPLE_COLOR, [0, 0, APPLE_SIZE, APPLE_SIZE])
        self.rect = self.image.get_rect()
        self.update()

    # Función para actualizar el coloreado de la manzana según la nueva información
    def update(self):
        pos = self.apple.get_pos()
        pos = [pos[0]+5, pos[1]+5]
        self.rect.centerx, self.rect.centery = pos


# Objeto que controla el envío de información a la sala y el coloreado en la
#  pantalla de cada uno de los jugadores que están participando en el juego
class Display():
    
    # Función para crear las variables necesarias para el juego
    def __init__(self, game):
        self.game = game  # asignamos el objeto Game

        # Creamos el tablero donde se mostrará la información y el ratio de FPS
        self.screen = pygame.display.set_mode(SIZE)
        self.clock =  pygame.time.Clock()  # FPS
        self.screen.fill(BLACK)

        # Creación de los sprites para los jugadores de Game
        self.snakes = [Snake(self.game.get_player(i)) for i in range(2)]

        # Creación de los sprites de la manzana de Game
        self.apple = AppleSprite(self.game.get_apple())
        
        # Añadimos estos conjuntos de sprites a varios sprite.Group() para su actualización
        self.all_sprites = pygame.sprite.Group()
        self.snake_group = pygame.sprite.Group()
        for snake  in self.snakes:
            self.all_sprites.add(snake)
            self.snake_group.add(snake)
        self.all_sprites.add(self.apple)

        pygame.init()

    # Función para analizar los inputs transmitidos por cada jugador para enviarse a la sala
    def analyze_events(self, side):
        events = []
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    events.append("quit")
                elif event.key == pygame.K_UP:
                    events.append("up")
                elif event.key == pygame.K_DOWN:
                    events.append("down")
                elif event.key == pygame.K_RIGHT:
                    events.append("right")
                elif event.key == pygame.K_LEFT:
                    events.append("left")
            elif event.type == pygame.QUIT:
                events.append("quit")
        if self.snakes[side].player.pos == self.apple.apple.pos: 
            events.append("eat")
        if self.snakes[1-side].player.pos in self.snakes[side].player.body:
            events.append("collide")
        events.append("go")
        return events
    
    # Función para actualizar la información que se muestra por pantalla
    def refresh(self):
        self.all_sprites.update()
        self.screen.fill(BLACK)
        score = self.game.get_score()
        font = pygame.font.Font(None, 74)
        text = font.render(f"{score[LEFT_PLAYER]}", 1, pygame.Color(0,190,0))
        self.screen.blit(text, (250, 10))
        text = font.render(f"{score[RIGHT_PLAYER]}", 1, pygame.Color(190,190,0))
        self.screen.blit(text, (SIZE[X]-250, 10))
        self.all_sprites.draw(self.screen)
        pygame.display.flip()

    # Función que controla el ratio de FPS con el que avanza el juego
    def tick(self):
        self.clock.tick(FPS)

    # Función para salir del juego
    @staticmethod
    def quit():
        pygame.quit()


# Función principal para conectarse a una sala con la que comunicarse
def main(ip_address):
    try:
        with Client((ip_address, 6000), authkey=b'secret password') as conn:
            game = Game()
            side,gameinfo = conn.recv()
            print(f"I am playing {SIDES[side]} with color {colores[side]}.")
            game.update(gameinfo)
            display = Display(game)
            while game.is_running():
                events = display.analyze_events(side)
                for ev in events:
                    conn.send(ev)
                    if ev == 'quit':
                        game.stop()
                conn.send("next")
                gameinfo = conn.recv()
                game.update(gameinfo)
                display.refresh()
                display.tick()
    except:
        traceback.print_exc()
    finally:
        pygame.quit()

if __name__=="__main__":
    ip_address = "127.0.0.1"
    if len(sys.argv)>1:
        ip_address = sys.argv[1]
    main(ip_address)