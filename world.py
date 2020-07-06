import pygame
import random
from player import Player
from unit import *
from player2pos import get_player2_pos
from images import *

class World:
    
    def __init__(self):
        self.TOTAL_UNITS = 5
        self.CARDS_ON_SCREEN = 5
        self.STARTING_POWER = 3
        self.EVENTS_ON_SCREEN = 8
        self.players = [Player(), Player()]
        self.ready = [False, False]
        self.map = []
        self.unit_starts = []
        self.treasure = []
        self.phase = "wait" # wait / unit_select / main
        self.turn = 0
        self.events = []

    def draw(self, screen, p):
        #Card Background
        image = images["Card_Background"]
        screen.blit(image, (0, 640))
        #Map
        for y in range(len(self.map)):
            for x in range(len(self.map[0])):
                image = images[tiles[self.map[y][x]]]
                if p == 0:
                    sx = x * 32
                    sy = y * 32
                else:
                    pos = get_player2_pos(x, y)
                    sx = pos[0] * 32
                    sy = pos[1] * 32
                screen.blit(image, (sx, sy))
                pygame.draw.rect(screen, (0, 0, 0), (sx, sy, 32, 32), 1)
        #Units and strongholds
        for i in self.players:
            image = images["Stronghold"].copy()
            image = pygame.transform.scale(image, (32, 32))
            for s in i.strongholds:
                if p == 0:
                    sx = s[0] * 32
                    sy = s[1] * 32
                else:
                    pos = get_player2_pos(s[0], s[1])
                    sx = pos[0] * 32
                    sy = pos[1] * 32
                screen.blit(image, (sx, sy))
            for u in i.units:
                if u.alive is True:
                    u.draw(screen, p)
        #Unit select
        if self.phase == "unit_select":
            for i, u in enumerate(unit_data.keys()):
                image = images[u]
                image = pygame.transform.scale(image, (64, 64))
                screen.blit(image, (65 * i + 5, 700))
    
    def change_turn(self):
        if self.turn == 0:
            self.turn = 1
            self.players[1].power = self.STARTING_POWER + len(self.players[1].strongholds)
            self.players[1].draw_card()
            for u in self.players[0].units:
                u.s_move = u.original_s_move
                u.d_move = u.original_d_move
                u.s_attack = u.original_s_attack
                u.d_attack = u.original_d_attack
                u.moves = 1
                u.actions = 1
                u.active_ability = ""
                u.special = ""
        else:
            self.turn = 0
            self.players[0].power = self.STARTING_POWER + len(self.players[0].strongholds)
            self.players[0].draw_card()
            for u in self.players[1].units:
                u.s_move = u.original_s_move
                u.d_move = u.original_d_move
                u.s_attack = u.original_s_attack
                u.d_attack = u.original_d_attack
                u.moves = 1
                u.actions = 1
                u.active_ability = ""
                u.special = ""
    
    def pickup_treasure(self, p, pos):
        i = int(random.random() * len(self.players[p].treasure))
        card = self.players[p].treasure[i]
        self.players[p].hand.append(card)
        del self.players[p].treasure[i]
        for i in range(len(self.treasure[p])):
            if pos[0] == self.treasure[p][i][0] and pos[1] == self.treasure[p][i][1]:
                self.map[pos[1]][pos[0]] = "0"
                del self.treasure[p][i]
        if len(self.players[p].treasure) == 0:
            print("WIN")
    
    def get_available_card_use(self, p, c):
        a = []
        if self.turn != p or self.players[p].power < c.cost:
            return a
        if c.type == "equipment":
            for u in self.players[p].units:
                if u.equipment is False and u.alive is True:
                    a.append((u.x, u.y))
        elif c.type == "utility":
            for u in self.players[p].units:
                if u.alive is True:
                    a.append((u.x, u.y))
        elif c.type == "building":
            for u in self.players[p].units:
                if u.alive is True:
                    ok = True
                    for s in self.players[p].strongholds:
                        if s[0] == u.x and s[1] == u.y:
                            ok = False
                            break
                    if ok is True and tiles[self.map[u.y][u.x]] == "Grass":
                        a.append((u.x, u.y))
        elif c.type == "ability":
            for u in self.players[p].units:
                if u.alive is True:
                    if c.only == None or c.only == u.name:
                        a.append((u.x, u.y))
        return a
    
    def use_card(self, p, card_pos, x, y):
        card = self.players[p].hand[card_pos]
        if card.type == "equipment" or card.type == "utility":
            for u in self.players[p].units:
                if u.x == x and u.y == y:
                    if card.type == "equipment":
                        u.equipment = True
                    self.players[p].power -= card.cost
                    for stat in card.stat_boosts.keys():
                        if stat == "Attack":
                            u.attack += card.stat_boosts[stat]
                        if stat == "Defense":
                            u.defense += card.stat_boosts[stat]
                        if stat == "Health":
                            u.health += card.stat_boosts[stat]
                            if u.health > u.max_health:
                                u.health = u.max_health
                        if stat == "Move":
                            if u.s_move > 0:
                                u.s_move += card.stat_boosts[stat]
                            if u.d_move > 0:
                                u.d_move += card.stat_boosts[stat]
                        if stat == "Moves":
                            u.moves += 1
                        if stat == "Max_Move":
                            if u.s_move > 0:
                                u.s_move += card.stat_boosts[stat]
                                u.original_s_move += card.stat_boosts[stat]
                            if u.d_move > 0:
                                u.d_move += card.stat_boosts[stat]
                                u.original_d_move += card.stat_boosts[stat]
                    del self.players[p].hand[card_pos]
                    break
        elif card.type == "building":
            for u in self.players[p].units:
                if u.x == x and u.y == y:
                    self.players[p].power -= card.cost
                    self.players[p].strongholds.append((x, y))
                    del self.players[p].hand[card_pos]
                    break
        elif card.type == "ability":
            if card.name == "Rally":
                self.players[p].power -= card.cost
                for u in self.players[p].units:
                    u.special = "Rally"
                del self.players[p].hand[card_pos]
            if card.name == "Final Charge":
                for u in self.players[p].units:
                    if u.x == x and u.y == y:
                        u.special = "Final Charge"
                        self.players[p].power -= card.cost
                        del self.players[p].hand[card_pos]
            if card.name == "Superb Arrow":
                for u in self.players[p].units:
                    if u.x == x and u.y == y:
                        u.s_attack += 3
                        u.d_attack += 3
                        self.players[p].power -= card.cost
                        del self.players[p].hand[card_pos]
            for u in self.players[p].units:
                if u.x == x and u.y == y:
                    self.players[p].power -= card.cost
                    u.active_ability = card.name
                    del self.players[p].hand[card_pos]
                    break
        self.events.append(self.players[p].name + " played " + card.name)
    
    
    def use_ability(self, p, x, y, name):
        for u in self.players[p].units:
            if u.x == x and u.y == y:
                if name == "Healing Spell":
                    u.health += 3
                    if u.health > u.max_health:
                        u.health = u.max_health
                    self.events.append(self.players[p].name + " used " + name + " on their " + u.name)
                elif name == "Double Attack":
                    u.actions += 1
                    self.events.append(self.players[p].name + " used " + name + " on their " + u.name)
                elif name == "Iron Wall":
                    u.special = "Invincible"
                    self.events.append(self.players[p].name + " used " + name + " on their " + u.name)
                break

    
    def get_available_abilities(self, p, u):
        a = []
        if self.turn != p or u.active_ability == "":
            pass
        elif u.active_ability == "Healing Spell":
            a = self.get_available_attacks(p, u, "self")
        elif u.active_ability == "Double Attack":
            a = self.get_available_attacks(p, u, "self")
        elif u.active_ability == "Iron Wall":
            a = self.get_available_attacks(p, u, "self")
        return a

    
    def get_available_attacks(self, p, u, w = "opponent"):
        a = []
        if (u.actions < 1 or self.turn != p) and w == "opponent":
            return a
        if w == "self":
            if p == 0:
                p = 1
            else:
                p = 0
        for y in range(u.y + 1, u.y + u.s_attack + 1):
            if y < 20:
                unit = self.check_for_units(u.x, y)
                if unit is not False and unit != p:
                    a.append((u.x, y))
                elif self.map[y][u.x] in solids:
                    break
        for y in range(u.y - 1, u.y - u.s_attack - 1, -1):
            if y >= 0:
                unit = self.check_for_units(u.x, y)
                if unit is not False and unit != p:
                    a.append((u.x, y))
                elif self.map[y][u.x] in solids:
                    break
        for x in range(u.x + 1, u.x + u.s_attack + 1):
            if x < 35:
                unit = self.check_for_units(x, u.y)
                if unit is not False and unit != p:
                    a.append((x, u.y))
                elif self.map[u.y][x] in solids:
                    break
        for x in range(u.x - 1, u.x - u.s_attack - 1, -1):
            if x >= 0:
                unit = self.check_for_units(x, u.y)
                if unit is not False and unit != p:
                    a.append((x, u.y))
                elif self.map[u.y][x] in solids:
                    break
        for i in range(1, u.d_attack + 1):
            if u.x + i < 35 and u.y - i >= 0:
                unit = self.check_for_units(u.x + i, u.y - i)
                if unit is not False and unit != p:
                    a.append((u.x + i, u.y - i))
                elif self.map[u.y - i][u.x + i] in solids:
                    break
        for i in range(1, u.d_attack + 1):
            if u.x + i < 35 and u.y + i < 20:
                unit = self.check_for_units(u.x + i, u.y + i)
                if unit is not False and unit != p:
                    a.append((u.x + i, u.y + i))
                elif self.map[u.y + i][u.x + i] in solids:
                    break
        for i in range(1, u.d_attack + 1):
            if u.x - i >= 0 and u.y - i >= 0:
                unit = self.check_for_units(u.x - i, u.y - i)
                if unit is not False and unit != p:
                    a.append((u.x - i, u.y - i))
                elif self.map[u.y - i][u.x - i] in solids:
                    break
        for i in range(1, u.d_attack + 1):
            if u.x - i >= 0 and u.y + i < 20:
                unit = self.check_for_units(u.x - i, u.y + i)
                if unit is not False and unit != p:
                    a.append((u.x - i, u.y + i))
                elif self.map[u.y + i][u.x - i] in solids:
                    break
        return a
    
    def get_available_moves(self, p, u):
        a = []
        if u.moves < 1 or self.turn != p:
            return a
        for y in range(u.y + 1, u.y + u.s_move + 1):
            if y < 20:
                if self.map[y][u.x] not in solids and self.check_for_units(u.x, y) is False:
                    a.append((u.x, y))
                else:
                    break
        for y in range(u.y - 1, u.y - u.s_move - 1, -1):
            if y >= 0 :
                if self.map[y][u.x] not in solids and self.check_for_units(u.x, y) is False:
                    a.append((u.x, y))
                else:
                    break
        for x in range(u.x + 1, u.x + u.s_move + 1):
            if x < 35:
                if self.map[u.y][x] not in solids and self.check_for_units(x, u.y) is False:
                    a.append((x, u.y))
                else:
                    break
        for x in range(u.x - 1, u.x - u.s_move - 1, -1):
            if x >= 0:
                if self.map[u.y][x] not in solids and self.check_for_units(x, u.y) is False:
                    a.append((x, u.y))
                else:
                    break
        for i in range(1, u.d_move + 1):
            if u.x + i < 35 and u.y - i >= 0:
                if self.map[u.y - i][u.x + i] not in solids and self.check_for_units(u.x + i, u.y - i) is False:
                    a.append((u.x + i, u.y - i))
                else:
                    break
        for i in range(1, u.d_move + 1):
            if u.x + i < 35 and u.y + i < 20:
                if self.map[u.y + i][u.x + i] not in solids and self.check_for_units(u.x + i, u.y + i) is False:
                    a.append((u.x + i, u.y + i))
                else:
                    break
        for i in range(1, u.d_move + 1):
            if u.x - i >= 0 and u.y - i >= 0:
                if self.map[u.y - i][u.x - i] not in solids and self.check_for_units(u.x - i, u.y - i) is False:
                    a.append((u.x - i, u.y - i))
                else:
                    break
        for i in range(1, u.d_move + 1):
            if u.x - i >= 0 and u.y + i < 20:
                if self.map[u.y + i][u.x - i] not in solids and self.check_for_units(u.x - i, u.y + i) is False:
                    a.append((u.x - i, u.y + i))
                else:
                    break
        for s in self.players[p].strongholds:
            if u.x == s[0] and u.y == s[1]:
                for s2 in self.players[p].strongholds:
                    if u.x != s2[0] or u.y != s2[1]:
                        if self.check_for_units(s2[0], s2[1]) is False:
                            a.append((s2[0], s2[1]))
                break
        if tiles[self.map[u.y][u.x]] == "Cave":
            for y in range(len(self.map)):
                for x in range(len(self.map[0])):
                    if tiles[self.map[y][x]] == "Cave" and (u.x != x or u.y != y):
                        if self.check_for_units(x, y) is False:
                            a.append((x, y))
        return a
    
    def check_for_units(self, x, y):
        for p in range(2):
            for u in self.players[p].units:
                if u.alive is True and u.x == x and u.y == y:
                    return p
        return False

    def attack(self, p, attacker, x, y):
        if p == 0:
            o = 1
        else:
            o = 0
        for i, u in enumerate(self.players[o].units):
            if u.x == x and u.y == y:
                if (attacker.attack - u.defense) > 0 and u.special != "Invincible":
                    atk = attacker.attack
                    df = u.defense
                    if attacker.special == "Rally":
                        atk += + 1
                    if attacker.special == "Final Charge":
                        atk += 5
                    if tiles[self.map[y][x]] == "Weeds":
                        atk += 1
                    if tiles[self.map[u.y][u.x]] == "Dirt":
                        df += 1
                    u.health -= (atk - df)
                if u.health <= 0:
                    self.die(o, i)
                attacker.actions -= 1
                break
    
    def die(self, p, i):
        self.players[p].units[i].alive = False
        for u in self.players[p].units:
            if u.alive is True:
                return
        print("ALL DEAD")

    def set_map(self, d):
        width = len(d["grid"][0])
        height = len(d["grid"])
        self.map = [[0 for x in range(width)] for y in range(height)]
        for y in range(height):
            for x in range(width):
                self.map[y][x] = d["grid"][y][x]
        self.unit_starts = [d["player1_unit_starts"], d["player2_unit_starts"]]
        self.treasure = [d["player1_treasure"], d["player2_treasure"]]

tiles = {
    "0": "Grass",
    "1": "Tree",
    "2": "Chest",
    "3": "Water",
    "4": "Shop",
    "5": "Dirt",
    "6": "Weeds",
    "7": "Bridge",
    "8": "Cave"
}

solids = ["1", "3"]
