import pygame
from player2pos import get_player2_pos
from images import images

class Unit:

    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y
        self.alive = True
        self.attack = unit_data[self.name]["attack"]
        self.defense = unit_data[self.name]["defense"]
        self.max_health = unit_data[self.name]["health"]
        self.health = self.max_health
        self.s_move = unit_data[self.name]["straight_movement"]
        self.d_move = unit_data[self.name]["diagonal_movement"]
        self.s_attack = unit_data[self.name]["straight_attack"]
        self.d_attack = unit_data[self.name]["diagonal_attack"]
        self.original_s_move = self.s_move
        self.original_d_move = self.d_move
        self.original_s_attack = self.s_attack
        self.original_d_attack = self.d_attack
        self.moves = 1
        self.actions = 1
        self.equipment = False
        self.active_ability = ""
        self.special = ""
    
    def move(self, x, y):
        self.x = x
        self.y = y
        self.moves -= 1

    def draw(self, screen, p):
        image = images[self.name]
        if p == 0:
            sx = self.x * 32
            sy = self.y * 32
        else:
            pos = get_player2_pos(self.x, self.y)
            sx = pos[0] * 32
            sy = pos[1] * 32
        screen.blit(image, (sx, sy))

unit_data = {
    "Knight": {
        "attack": 6,
        "defense": 3,
        "health": 5,
        "straight_movement": 3,
        "diagonal_movement": 0,
        "straight_attack": 1,
        "diagonal_attack": 0
    },
    "Fairy": {
        "attack": 2,
        "defense": 1,
        "health": 10,
        "straight_movement": 3,
        "diagonal_movement": 3,
        "straight_attack": 1,
        "diagonal_attack": 1
    },
    "Minotaur": {
        "attack": 4,
        "defense": 1,
        "health": 10,
        "straight_movement": 6,
        "diagonal_movement": 0,
        "straight_attack": 1,
        "diagonal_attack": 0
    },
    "Golem": {
        "attack": 2,
        "defense": 3,
        "health": 15,
        "straight_movement": 3,
        "diagonal_movement": 0,
        "straight_attack": 1,
        "diagonal_attack": 0
    },
    "Monkey": {
        "attack": 2,
        "defense": 1,
        "health": 5,
        "straight_movement": 10,
        "diagonal_movement": 10,
        "straight_attack": 1,
        "diagonal_attack": 1
    },
    "Ninja": {
        "attack": 6,
        "defense": 1,
        "health": 10,
        "straight_movement": 0,
        "diagonal_movement": 6,
        "straight_attack": 0,
        "diagonal_attack": 1
    },
    "Archer": {
        "attack": 4,
        "defense": 1,
        "health": 5,
        "straight_movement": 3,
        "diagonal_movement": 0,
        "straight_attack": 3,
        "diagonal_attack": 3
    }
}