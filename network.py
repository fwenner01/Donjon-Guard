import socket
import pickle

class Network:

    def __init__(self, server, port):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = server
        self.port = port
        self.addr = (self.server, self.port)
        self.p = self.connect()

    def get_p(self):
        return self.p

    def connect(self):
        try:
            self.client.connect(self.addr)
            return int(self.client.recv(2048).decode())
        except:
            pass
    
    def set_name(self, name):
        try:
            self.client.send(str.encode("set_name," + name))
        except:
            pass
    
    def set_deck(self, deck):
        message = "set_deck"
        try:
            for i in range(len(deck)):
                deck[i] = deck[i].replace("\n", "")
                message += "," + deck[i]
            self.client.send(str.encode(message))
        except:
            pass
    
    def get_world(self):
        try:
            self.client.send(str.encode("get_world"))
            world = self.client.recv(2048 * 8)
            return pickle.loads(world)
        except:
            pass
    
    def place_unit(self, unit, x, y):
        try:
            self.client.send(str.encode("place_unit," + unit + "," + str(x) + "," + str(y)))
        except:
            pass
    
    def move_unit(self, unit, x, y):
        try:
            self.client.send(str.encode("move_unit," + str(unit) + "," + str(x) + "," + str(y)))
        except:
            pass
    
    def attack_unit(self, unit, x, y):
        try:
            self.client.send(str.encode("attack_unit," + str(unit) + "," + str(x) + "," + str(y)))
        except:
            pass
    
    def use_card(self, card_pos, x, y):
        try:
            self.client.send(str.encode("use_card," + str(card_pos) + "," + str(x) + "," + str(y)))
        except:
            pass
    
    def use_ability(self, unit, x, y, name):
        try:
            self.client.send(str.encode("use_ability," + str(unit) + "," + str(x) + "," + str(y) + "," + name))
        except:
            pass
    
    def send_type(self, text):
        try:
            self.client.send(str.encode("send_type," + text))
        except:
            pass
    
    def end_turn(self):
        try:
            self.client.send(str.encode("end_turn"))
        except:
            pass