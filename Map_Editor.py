import pygame
import os.path
import json
from images import images
from world import tiles
pygame.init()

SCREEN_WIDTH = 1120
SCREEN_HEIGHT = 800

screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
pygame.display.set_caption("Map Editor")
font = pygame.font.SysFont("Bazooka", 20)

class Display:

    def __init__(self):
        self.WIDTH = 35
        self.HEIGHT = 20
        self.TREASURE = 3
        self.UNITS = 5
        self.map = {
            "grid": [["0" for x in range(self.WIDTH)] for y in range(self.HEIGHT)],
            "player1_unit_starts": [],
            "player2_unit_starts": [],
            "player1_treasure": [],
            "player2_treasure": []
        }
        self.selected = None
        self.paint = False
        self.mx = None
        self.my = None
    
    def draw(self):
        screen.fill((0, 0, 0))
        image = images["Card_Background"]
        screen.blit(image, (0, 640))
        for y in range(self.HEIGHT):
            for x in range(self.WIDTH):
                if self.map["grid"][y][x] == 999:
                    continue
                image = images[tiles[self.map["grid"][y][x]]]
                screen.blit(image, (x * 32, y * 32))
                pygame.draw.rect(screen, (0, 0, 0), (x * 32, y * 32, 32, 32), 1)
        for t in tiles.keys():
            image = images[tiles[t]]
            screen.blit(image, (int(t) * 32, 680))
            if self.selected == t:
                pygame.draw.rect(screen, (255, 0, 0), (int(t) * 32, 680, 32, 32), 1)
        if self.mx != None and self.my != None:
            text = font.render("(" + str(self.mx) + "," + str(self.my) + ")", 0, (255, 255, 255))
            screen.blit(text, (1080, 780))
        text = font.render("Press 'S' to save and 'L' to load", 0, (255, 255, 255))
        screen.blit(text, (10,780))
            
    
    def get_input(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    self.save()
                if event.key == pygame.K_l:
                    self.load()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for t in tiles.keys():
                    if pos[0] > (int(t) * 32) and pos[0] < (int(t) * 32) + 32 and pos[1] > 680 and pos[1] < 680 + 32:
                        self.selected = t
                if pos[1] < 640 and self.selected is not None:
                    self.paint = True
            if event.type == pygame.MOUSEBUTTONUP and self.paint is True:
                self.paint = False
        if self.paint is True:
            pos = pygame.mouse.get_pos()
            if pos[1] < 640:
                self.map["grid"][int(pos[1] / 32)][int(pos[0] / 32)] = self.selected
        pos = pygame.mouse.get_pos()
        if pos[1] < 640:
            self.mx = int(pos[0] / 32)
            self.my = int(pos[1] / 32)
    
    def save(self):
        already_chosen = []
        for p in range(2):
            text = font.render("Choose Player " + str(p + 1) + " treasure", 0, (255, 255, 255))
            screen.blit(text, (10, p * 20 + 10))
            pygame.display.flip()
            for i in range(self.TREASURE):
                selected = False
                while selected is False:
                    for event in pygame.event.get():
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            pos = pygame.mouse.get_pos()
                            if pos[1] < 640:
                                if tiles[self.map["grid"][int(pos[1] / 32)][int(pos[0] / 32)]] == "Chest" and (int(pos[0] / 32), int(pos[1] / 32)) not in already_chosen:
                                    already_chosen.append((int(pos[0] / 32), int(pos[1] / 32)))
                                    pygame.draw.rect(screen, (255, 255, 0), (int(pos[0] / 32) * 32, int(pos[1] / 32) * 32, 32, 32))
                                    pygame.display.flip()
                                    if p == 0:
                                        self.map["player1_treasure"].append((int(pos[0] / 32), int(pos[1] / 32)))
                                    else:
                                        self.map["player2_treasure"].append((int(pos[0] / 32), int(pos[1] / 32)))
                                    selected = True
        already_chosen = []
        for p in range(2):
            text = font.render("Choose Player " + str(p + 1) + " unit starting positions", 0, (255, 255, 255))
            screen.blit(text, (10, p * 20 + 50))
            pygame.display.flip()
            for i in range(self.UNITS):
                selected = False
                while selected is False:
                    for event in pygame.event.get():
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            pos = pygame.mouse.get_pos()
                            if pos[1] < 640:
                                if tiles[self.map["grid"][int(pos[1] / 32)][int(pos[0] / 32)]] == "Grass" and (int(pos[0] / 32), int(pos[1] / 32)) not in already_chosen:
                                    already_chosen.append((int(pos[0] / 32), int(pos[1] / 32)))
                                    pygame.draw.rect(screen, (255, 255, 255), (int(pos[0] / 32) * 32, int(pos[1] / 32) * 32, 32, 32))
                                    pygame.display.flip()
                                    if p == 0:
                                        self.map["player1_unit_starts"].append((int(pos[0] / 32), int(pos[1] / 32)))
                                    else:
                                        self.map["player2_unit_starts"].append((int(pos[0] / 32), int(pos[1] / 32)))
                                    selected = True
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
            text = font.render("Map name: ", 0, (255, 255, 255))
            screen.blit(text, (10, 10))
            text = font.render(name, 0, (255, 255, 255))
            screen.blit(text, (100, 10))
            pygame.display.flip()
        
        file = open("maps/" + name + ".txt", "w")
        json.dump(self.map, file)
    
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
            text = font.render("Map Name: ", 0, (255, 255, 255))
            screen.blit(text, (10, 10))
            text = font.render(name, 0, (255, 255, 255))
            screen.blit(text, (100, 10))
            pygame.display.flip()
    
        if os.path.exists("maps/" + name + ".txt"):
            file = open("maps/" + name + ".txt", "r")
            d = json.load(file)
            self.map["grid"] = d["grid"]


def main():
    display = Display()
    run = True
    while run:
        display.draw()
        display.get_input()
        pygame.display.flip()

main()