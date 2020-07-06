import random
from card import Card
from unit import Unit

class Player:

    def __init__(self):
        self.TOTAL_CARDS = 15
        self.TOTAL_TREASURE = 3
        self.STARTING_HAND = 5
        self.name = ""
        self.deck = []
        self.hand = []
        self.treasure = []
        self.units = []
        self.strongholds = []
        self.power = 3
    
    def set_name(self, name):
        self.name = name

    def add_unit(self, name, x, y):
        self.units.append(Unit(name, x, y))
    
    def load_deck(self, deck):
        if len(deck) - self.TOTAL_TREASURE != self.TOTAL_CARDS:
            print("WRONG NUMBER OF CARDS IN DECK")
            return
        for i in range(self.TOTAL_CARDS):
            self.deck.append(Card(deck[i]))
        for i in range(self.STARTING_HAND):
            self.draw_card()
        for i in range(self.TOTAL_CARDS, self.TOTAL_CARDS + self.TOTAL_TREASURE):
            self.treasure.append(Card(deck[i]))
    
    def draw_card(self):
        if len(self.deck) > 0:
            i = int(random.random() * len(self.deck))
            card = self.deck[i]
            self.hand.append(card)
            del self.deck[i]
            