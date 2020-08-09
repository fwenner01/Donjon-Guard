import pygame
import os.path
from images import images
from card import *
pygame.init()

SCREEN_WIDTH = 1120
SCREEN_HEIGHT = 800

screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
pygame.display.set_caption("Deck Editor")
font = pygame.font.SysFont("Bazooka", 20)

class Display:

    def __init__(self):
        self.MAX_CARDS = 15
        self.MAX_TREASURE = 3
        self.cards = []
        self.get_cards()
        self.deck = []
        self.treasure = []
    
    def get_cards(self):
        for i in card_data.keys():
            self.cards.append(Card(i))
    
    def draw(self):
        screen.fill((0, 0, 0))
        for i, c in enumerate(self.cards):
            num = 0
            x = int(i % 7) * 150
            y = int(i / 7) * 160
            c.draw(screen, (x, y))
            if c.name in self.treasure:
                pygame.draw.rect(screen, (255, 0, 0), (x, y, 100, 150), 1)
            pygame.draw.rect(screen, (255, 255, 255), (x + 100, y, 50, 50), 1)
            pygame.draw.rect(screen, (255, 255, 255), (x + 100, y + 50, 50, 50), 1)
            for j in self.deck:
                if j == c.name:
                    num += 1
            text = font.render("+", 0, (255, 255, 255))
            screen.blit(text, (x + 120, y + 20))
            text = font.render("-", 0, (255, 255, 255))
            screen.blit(text, (x + 120, y + 70))
            text = font.render(str(num), 0, (255, 255, 255))
            screen.blit(text, (x + 120, y + 120))
        text = font.render("Deck: " + str(len(self.deck)) + "/" + str(self.MAX_CARDS), 0, (255, 255, 255))
        screen.blit(text, (950,780))
        text = font.render("Treasure: " + str(len(self.treasure)) + "/" + str(self.MAX_TREASURE), 0, (255, 0, 0))
        screen.blit(text, (1030,780))
        text = font.render("Press 'S' to save and 'L' to load ", 0, (255, 255, 255))
        screen.blit(text, (10,780))
            
    
    def get_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    self.save()
                if event.key == pygame.K_l:
                    self.load()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for i, c in enumerate(self.cards):
                    if pos[0] > (int(i % 7) * 150) + 100 and pos[0] < (int(i % 7) * 150) + 150 and pos[1] > int(i / 7) * 160 and pos[1] < (int(i / 7) * 160) + 50:
                        self.add_card(c)
                    elif pos[0] > (int(i % 7) * 150) + 100 and pos[0] < (int(i % 7) * 150) + 150 and pos[1] > (int(i / 7) * 160) + 50 and pos[1] < (int(i / 7) * 160) + 100:
                        self.minus_card(c)
                    elif pos[0] > (int(i % 7) * 150) and pos[0] < (int(i % 7) * 150) + 100 and pos[1] > int(i / 7) * 160 and pos[1] < (int(i / 7) * 160) + 150:
                        self.add_treasure(c)
    
    def save(self):
        if len(self.deck) < self.MAX_CARDS or len(self.treasure) < self.MAX_TREASURE:
            return
        name = ""
        pressed = False
        while pressed == False:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and len(name) > 0:
                        pressed = True
                    elif event.key == pygame.K_BACKSPACE and len(name) > 0:
                        name = name[:-1]
                    elif len(name) < 10:
                        name += event.unicode
            screen.fill((0, 0, 0))
            text = font.render("Deck name: ", 0, (255, 255, 255))
            screen.blit(text, (10, 10))
            text = font.render(name, 0, (255, 255, 255))
            screen.blit(text, (100, 10))
            pygame.display.flip()
        
        file = open("decks/" + name + ".txt", "w")
        for i in self.deck:
            file.write(i + "\n")
        for i in self.treasure:
            file.write(i + "\n")
    
    def load(self):
        name = ""
        pressed = False
        while pressed == False:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and len(name) > 0:
                        pressed = True
                    elif event.key == pygame.K_BACKSPACE and len(name) > 0:
                        name = name[:-1]
                    elif len(name) < 10:
                        name += event.unicode
            screen.fill((0, 0, 0))
            text = font.render("Deck name: ", 0, (255, 255, 255))
            screen.blit(text, (10, 10))
            text = font.render(name, 0, (255, 255, 255))
            screen.blit(text, (100, 10))
            pygame.display.flip()
    
        if os.path.exists("decks/" + name + ".txt"):
            file = open("decks/" + name + ".txt", "r")
            self.deck = []
            self.treasure = []
            self.deck = file.readlines()
            for i in range(len(self.deck)):
                self.deck[i] = self.deck[i].replace("\n", "")
            for i in range(self.MAX_TREASURE):
                self.treasure.append(self.deck[len(self.deck) - i - 1])
                del self.deck[len(self.deck) - i - 1]
        
    
    def add_card(self, c):
        if len(self.deck) < self.MAX_CARDS:
            self.deck.append(c.name)
    
    def minus_card(self, c):
        if c.name in self.deck:
            self.deck.remove(c.name)
    
    def add_treasure(self, c):
        if c.name in self.treasure:
            self.treasure.remove(c.name)
        elif len(self.treasure) < self.MAX_TREASURE:
            self.treasure.append(c.name)


def main():
    display = Display()
    run = True
    while run:
        display.draw()
        display.get_input()
        pygame.display.flip()

main()