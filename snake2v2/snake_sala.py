from multiprocessing.connection import Listener
from multiprocessing import Process, Manager, Value, Lock
import traceback
import sys
import random

LEFT_PLAYER = 0
RIGHT_PLAYER = 1
SIDESSTR = ["left", "right"]
SIZE = (720, 480)
X = 0
Y = 1
DELTA = 10

class Player():
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

    def get_pos(self):
        return self.pos

    def get_side(self):
        return self.side
    
    def get_body(self):
        return self.body
    
    def set_body(self, body):
        self.body = body
    
    def moveDown(self):
        self.change_to = "down"

    def moveUp(self):
        self.change_to = "up"

    def moveRight(self):
        self.change_to = "right"

    def moveLeft(self):
        self.change_to = "left"

    def go(self):
        if self.change_to == 'up' and self.direction != 'down':
            self.direction = 'up'
        if self.change_to == 'down' and self.direction != 'up':
            self.direction = 'down'
        if self.change_to == 'left' and self.direction != 'right':
            self.direction = 'left'
        if self.change_to == 'right' and self.direction != 'left':
            self.direction = 'right'

    def move(self):
        if self.direction == 'up':
            self.pos[Y] -= DELTA
        if self.direction == 'down':
            self.pos[Y] += DELTA
        if self.direction == 'left':
            self.pos[X] -= DELTA
        if self.direction == 'right':
            self.pos[X] += DELTA
        self.pos[X] %= SIZE[X]
        self.pos[Y] %= SIZE[Y]

    def update(self, player):
        if player.pos in self.body:
            body = self.get_body()
            body = body[:max(body.index(player.pos),1)]
            self.body = body

    def __str__(self):
        return f"P<{SIDESSTR[self.side]}, {self.pos}>"

class Apple():
    def __init__(self, spawn = True):
        self.pos = [random.randrange(1, (SIZE[X]//10)) * 10,
                    random.randrange(1, (SIZE[Y]//10)) * 10]
        self.spawn = spawn
    
    def get_pos(self):
        return self.pos
    
    def get_spawn(self):
        return self.spawn
    
    def update(self, player):
        player.body.insert(0, list(player.pos))
        if player.pos[0] == self.pos[0] and player.pos[1] == self.pos[1]:
            self.spawn = False
        else:
            player.body.pop()
        
    def __str__(self):
        return f"A<{self.pos, self.spawn}>"

class Game():
    def __init__(self, manager):
        self.players = manager.list( [Player(LEFT_PLAYER), Player(RIGHT_PLAYER)] )
        self.apple = manager.list( [ Apple() ] )
        self.score = manager.list( [0,0] )
        self.running = Value('i', 1) # 1 running
        self.lock = Lock()

    def get_player(self, side):
        return self.players[side]

    def get_apple(self):
        return self.apple[0]

    def get_score(self):
        return list(self.score)

    def is_running(self):
        return self.running.value == 1

    def stop(self):
        self.running.value = 0

    def go(self, player):
        self.lock.acquire()
        p = self.players[player]
        p.go()
        self.players[player] = p
        self.lock.release()

    def move(self, player):
        self.lock.acquire()
        p = self.players[player]
        p.move()
        apple = self.apple[0]
        apple.update(p)
        self.players[player] = p
        self.lock.release()

    def moveUp(self, player):
        self.lock.acquire()
        p = self.players[player]
        p.moveUp()
        apple = self.apple[0]
        apple.update(p)
        self.players[player] = p
        self.lock.release()

    def moveDown(self, player):
        self.lock.acquire()
        p = self.players[player]
        p.moveDown()
        apple = self.apple[0]
        apple.update(p)
        self.players[player] = p
        self.lock.release()

    def moveRight(self, player):
        self.lock.acquire()
        p = self.players[player]
        p.moveRight()
        apple = self.apple[0]
        apple.update(p)
        self.players[player] = p
        self.lock.release()

    def moveLeft(self, player):
        self.lock.acquire()
        p = self.players[player]
        p.moveLeft()
        apple = self.apple[0]
        apple.update(p)
        self.players[player] = p
        self.lock.release()

    def apple_interaction(self, side):
        self.lock.acquire()
        apple = self.apple[0]
        player = self.get_player(side)
        apple.update(player)
        if not apple.spawn:
            apple.pos = [random.randrange(1, (SIZE[X]//10)) * 10,
                         random.randrange(1, (SIZE[Y]//10)) * 10]
            self.score[side] += 1            
        apple.spawn = True
        self.apple[0] = apple
        self.lock.release()

    def snakes_interaction(self, side):
        self.lock.acquire()
        player1 = self.players[side]
        n = len(player1.body)
        side2 = 1 - side
        player2 = self.players[side2]
        player1.update(player2)
        self.score[side2] += (n - len(player1.body))
        self.players[side] = player1        
        self.lock.release()

    def get_info(self):
        info = {
            'pos_left_player': self.players[LEFT_PLAYER].get_pos(),
            'pos_right_player': self.players[RIGHT_PLAYER].get_pos(),
            'body_left_player': self.players[LEFT_PLAYER].get_body(),
            'body_right_player': self.players[RIGHT_PLAYER].get_body(),
            'pos_apple': self.apple[0].get_pos(),
            'score': list(self.score),
            'is_running': self.running.value == 1
        }
        return info
    
    def __str__(self):
        return f"G<{self.players[RIGHT_PLAYER]}:{self.players[LEFT_PLAYER]}:{self.apple[0]}:{self.running.value}>"

def player(side, conn, game):
    try:
        print(f"starting player {SIDESSTR[side]}:{game.get_info()}")
        conn.send( (side, game.get_info()) )
        while game.is_running():
            command = ""
            while command != "next":
                command = conn.recv()
                if command == "up":
                    game.moveUp(side)
                elif command == "down":
                    game.moveDown(side)
                elif command == "right":
                    game.moveRight(side)
                elif command == "left":
                    game.moveLeft(side)
                elif command == "go":
                    game.go(side)
                    game.move(side)
                elif command == "eat":
                    game.apple_interaction(side)
                elif command == "collide":
                    game.snakes_interaction(side)
                elif command == "quit":
                    game.stop()
            conn.send(game.get_info())
    except:
        traceback.print_exc()
        conn.close()
    finally:
        print(f"Game ended {game}")

def main(ip_address):
    manager = Manager()
    try:
        with Listener((ip_address, 6000),
                      authkey=b'secret password') as listener:
            n_player = 0
            players = [None, None]
            game = Game(manager)
            while True:
                print(f"accepting connection {n_player}")
                conn = listener.accept()
                players[n_player] = Process(target=player,
                                            args=(n_player, conn, game))
                n_player += 1
                if n_player == 2:
                    players[0].start()
                    players[1].start()
                    n_player = 0
                    players = [None, None]
                    game = Game(manager)

    except Exception as e:
        traceback.print_exc()

if __name__=='__main__':
    ip_address = "127.0.0.1"
    if len(sys.argv)>1:
        ip_address = sys.argv[1]

    main(ip_address)