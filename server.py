import socket
import pickle
from _thread import *
import json
from world import World
import random

class Server:

    def __init__(self):
        self.server = input("Enter IP: ") #"192.168.0.26"
        self.port = int(input("Enter port: ")) #5555
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.game = Game()
        self.pids = [0, 1]

    def start(self):
        try:
            self.s.bind((self.server, self.port))
        except socket.error as e:
            str(e)
        self.s.listen(2)
        print("Waiting for connections")

    def connect_players(self):
        p = 0
        while p < 2:
            conn, addr = self.s.accept()
            print("Connected to:", addr)

            r = int(random.random() * len(self.pids))
            start_new_thread(self.game.threaded_client, (conn, self.pids[r]))
            del self.pids[r]

            p += 1
        self.game.main()

class Game:

    def __init__(self):
        self.world = World()
        map_name = "map1"
        file = open("maps/" + map_name + ".txt", "r")
        d = json.load(file)
        self.world.set_map(d)
    
    def threaded_client(self, conn, p):
        conn.send(str.encode(str(p)))

        def set_name(message):
            self.world.players[p].name = message[1]

        def set_deck(message):
            deck = []
            for i in range(1, len(message)):
                deck.append(message[i])
            self.world.players[p].load_deck(deck)

        def get_world(message):
            conn.sendall(pickle.dumps(self.world))
    
        def place_unit(message):
            self.world.players[p].add_unit(message[1], int(message[2]), int(message[3]))
            if len(self.world.players[p].units) == self.world.TOTAL_UNITS:
                self.world.ready[p] = True
        
        def move_unit(message):
            self.world.players[p].units[int(message[1])].move(int(message[2]), int(message[3]))
            self.world.events.append(self.world.players[p].name + " moved their " + self.world.players[p].units[int(message[1])].name)
            for i in self.world.treasure[p]:
                if i[0] == self.world.players[p].units[int(message[1])].x and i[1] == self.world.players[p].units[int(message[1])].y:
                    self.world.pickup_treasure(p, (self.world.players[p].units[int(message[1])].x, self.world.players[p].units[int(message[1])].y))
        
        def attack_unit(message):
            self.world.attack(p, self.world.players[p].units[int(message[1])], int(message[2]), int(message[3]))
        
        def use_card(message):
            self.world.use_card(p, int(message[1]), int(message[2]), int(message[3]))
        
        def use_ability(message):
            self.world.use_ability(p, int(message[2]), int(message[3]), message[4])
            self.world.players[p].units[int(message[1])].active_ability = ""
        
        def send_type(message):
            self.world.events.append(self.world.players[p].name + ": " + message[1])
        
        def end_turn(message):
            self.world.change_turn()

        methods = {
            "set_name": set_name,
            "set_deck": set_deck,
            "get_world": get_world,
            "place_unit": place_unit,
            "move_unit": move_unit,
            "attack_unit": attack_unit,
            "use_card": use_card,
            "use_ability": use_ability,
            "send_type": send_type,
            "end_turn": end_turn
        }

        while True:
            try:
                message = conn.recv(2048 * 8).decode()
                if not message:
                    break
                else:
                    message = message.split(",")
                    if message[0] in methods:
                        methods[message[0]](message)
            except:
                pass
        
        print("Lost connection")
        conn.close()

    
    def main(self):
        self.world.phase = "unit_select"
        run = True
        while run:
            if self.world.phase == "unit_select":
                if self.world.ready[0] == True and self.world.ready[1] == True:
                    self.world.phase = "main"

server = Server()
server.start()
server.connect_players()