import pygame
import os.path
from network import Network
from unit import *
from player2pos import get_player2_pos
from images import images
pygame.init()

SCREEN_WIDTH = 1120
SCREEN_HEIGHT = 800

screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
pygame.display.set_caption("Donjon Guard")

class Client():

    def __init__(self):
        self.fps = 30
        self.unit_selected_menu = None
        self.unit_selected = None
        self.unit_player = None
        self.available_moves = []
        self.available_attacks = []
        self.available_abilities = []
        self.available_card_use = []
        self.card_selected = None
        self.hand_pos = 0
        self.place_flicker = 0
        self.font = pygame.font.SysFont("Arial Black", 20)
        self.font2 = pygame.font.SysFont("Arial Black", 12)
        self.event_index = 0
        self.event_length = 0
        self.chat = False
        self.type = ""
        self.n = Network(self.get_IP(), self.get_port())
        self.p = self.n.get_p()
        self.deck_file = "decks/" + self.get_deck_name() + ".txt" #"decks/deck1.txt"
        self.get_name()
        self.world = self.n.get_world()
    
    def main(self):
        clock = pygame.time.Clock()
        run = True
        self.load_deck()
        while run:
            clock.tick(self.fps)
            screen.fill((0, 0, 0))
            self.world = self.n.get_world()
            self.world.draw(screen, self.p)
            if self.world.phase == "wait":
                pass
            elif self.world.phase == "unit_select":
                self.unit_select_input()
                self.unit_select_draw()
            elif self.world.phase == "main":
                self.main_input()
                self.main_draw()
            pygame.display.flip()
    
    def main_draw(self):
        for i, card in enumerate(self.world.players[self.p].hand):
            if i >= self.hand_pos and i < self.hand_pos + self.world.CARDS_ON_SCREEN:
                card.draw(screen, i - self.hand_pos)
        # Card select box
        if self.card_selected is not None and self.card_selected - self.hand_pos >= 0 and self.card_selected - self.hand_pos < self.world.CARDS_ON_SCREEN:
            pygame.draw.rect(screen, (255, 0, 0), (110 * (self.card_selected - self.hand_pos) + 40, 644, 101, 151), 1)
        # Unit cursor and stats
        if self.unit_selected is not None and self.world.players[self.p].units[self.unit_selected].alive is True:
            cursor = images["Cursor"]
            u = self.world.players[self.unit_player].units[self.unit_selected]
            s_pos = self.screen_coords(u.x, u.y)
            sx = s_pos[0]
            sy = s_pos[1]
            screen.blit(cursor, (sx * 32, sy * 32))
            if self.unit_player == self.p:
                whos = " (you)"
            else:
                whos = " (opponent)"
            text = self.font.render(u.name + whos, 0, (255, 255, 255))
            screen.blit(text, (620, 710))
            text = self.font.render("Attack: " + str(u.attack), 0, (255, 255, 255))
            screen.blit(text, (640, 730))
            text = self.font.render("Defense: " + str(u.defense), 0, (255, 255, 255))
            screen.blit(text, (640, 750))
            text = self.font.render("Health: " + str(u.health), 0, (255, 255, 255))
            screen.blit(text, (640, 770))
            self.available_moves = self.world.get_available_moves(self.p, u)
            if self.unit_player == self.p:
                for move in self.available_moves:
                    if self.place_flicker % 20 < 10:
                        pass
                    else:
                        s_pos = self.screen_coords(move[0], move[1])
                        sx = s_pos[0]
                        sy = s_pos[1]
                        pygame.draw.rect(screen, (255, 255, 0), (sx * 32, sy * 32, 32, 32))
                self.available_attacks = self.world.get_available_attacks(self.p, u)
                for attack in self.available_attacks:
                    if self.place_flicker % 20 < 10:
                        pass
                    else:
                        s_pos = self.screen_coords(attack[0], attack[1])
                        sx = s_pos[0]
                        sy = s_pos[1]
                        pygame.draw.rect(screen, (255, 0, 0), (sx * 32, sy * 32, 32, 32))
                self.available_abilities = self.world.get_available_abilities(self.p, u)
                for ability in self.available_abilities:
                    if self.place_flicker % 20 < 10:
                        pass
                    else:
                        s_pos = self.screen_coords(ability[0], ability[1])
                        sx = s_pos[0]
                        sy = s_pos[1]
                        pygame.draw.rect(screen, (255, 0, 255), (sx * 32, sy * 32, 32, 32))
        else:
            self.available_moves = []
            self.available_attacks = []
            self.available_abilities = []
        if self.card_selected is not None:
            self.available_card_use = self.world.get_available_card_use(self.p, self.world.players[self.p].hand[self.card_selected])
        for use in self.available_card_use:
            if self.place_flicker % 20 < 10:
                pass
            else:
                s_pos = self.screen_coords(use[0], use[1])
                sx = s_pos[0]
                sy = s_pos[1]
                pygame.draw.rect(screen, (0, 0, 255), (sx * 32, sy * 32, 32, 32))
        self.place_flicker += 1
        # Hand scroll arrows
        if self.hand_pos > 0:
            arrow_l = images["Arrow_L"]
            screen.blit(arrow_l, (5, 700))
        if self.hand_pos + self.world.CARDS_ON_SCREEN < len(self.world.players[self.p].hand):
            arrow_r = images["Arrow_R"]
            screen.blit(arrow_r, (585, 700))
        if self.event_index > 0:
            arrow_u = images["Arrow_U"]
            screen.blit(arrow_u, (1090, 700))
        if self.event_index + self.world.EVENTS_ON_SCREEN < len(self.world.events):
            arrow_d = images["Arrow_D"]
            screen.blit(arrow_d, (1090, 735))
        # Status
        power = self.font.render("Power: " + str(self.world.players[self.p].power), 0, (150, 150, 0))
        screen.blit(power, (620, 650))
        if self.p == self.world.turn:
            turn = "Turn: You  END"
            button = images["Button"]
            screen.blit(button, (730, 680))
        else:
            turn = "Turn: Opponent"
        turn = self.font.render(turn, 0, (0, 0, 0))
        screen.blit(turn, (620, 680))
        #Event feed
        event_background = images["Event_Background"]
        screen.blit(event_background, (830, 645))
        if self.chat is False:
            pygame.draw.rect(screen, (0, 0, 0), (830, 760, 250, 20), 3)
        else:
            pygame.draw.rect(screen, (0, 0, 0), (830, 760, 250, 20))
            text = self.font2.render(self.type, 0, (0, 0, 200))
            screen.blit(text, (830, 765))
        if self.event_length != len(self.world.events):
            self.event_length = len(self.world.events)
            if len(self.world.events) > self.world.EVENTS_ON_SCREEN:
                self.event_index = len(self.world.events) - self.world.EVENTS_ON_SCREEN
        start = self.event_index
        if self.event_index + self.world.EVENTS_ON_SCREEN > len(self.world.events):
            end = len(self.world.events)
        else:
            end = self.event_index + self.world.EVENTS_ON_SCREEN
        j = 0
        for i in range(start, end):
            if self.world.events[i].find(':') != -1:
                color = (0, 0, 200)
            else:
                color = (0, 0, 0)
            text = self.font2.render(self.world.events[i], 0, color)
            screen.blit(text, (830, (j * 12) + 645))
            j += 1
            
        

    def main_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif self.chat is True:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and len(self.type) > 0:
                        self.n.send_type(self.type)
                        self.type = ""
                        self.chat = False
                    elif event.key == pygame.K_BACKSPACE and len(self.type) > 0:
                        self.type = self.type[:-1]
                    elif len(self.type) < 30:
                        self.type += event.unicode
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.chat = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if self.world.turn == self.p and pos[0] > 730 and pos[0] < 790 and pos[1] > 680 and pos[1] < 710:
                    self.n.end_turn()
                    return
                if self.hand_pos > 0:
                    if pos[0] > 5 and pos[0] < 5 + 32 and pos[1] > 700 and pos[1] < 700 + 32:
                        self.hand_pos -= 1
                if self.hand_pos + self.world.CARDS_ON_SCREEN < len(self.world.players[self.p].hand):
                    if pos[0] > 585 and pos[0] < 585 + 32 and pos[1] > 700 and pos[1] < 700 + 32:
                        self.hand_pos += 1
                if self.event_index + self.world.EVENTS_ON_SCREEN < len(self.world.events):
                    if pos[0] > 1090 and pos[0] < 1090 + 32 and pos[1] > 735 and pos[1] < 735 + 32:
                        self.event_index += 1
                if self.event_index > 0:
                    if pos[0] > 1090 and pos[0] < 1090 + 32 and pos[1] > 700 and pos[1] < 700 + 32:
                        self.event_index -= 1
                if pos[0] > 830 and pos[0] < 830 + 250 and pos[1] > 760 and pos[1] < 760 + 20:
                    self.chat = True
                card_num = len(self.world.players[self.p].hand)
                if card_num > self.world.CARDS_ON_SCREEN:
                    card_num = self.world.CARDS_ON_SCREEN
                for i in range(card_num):
                    if pos[0] > 110 * i + 40 and pos[0] < 110 * i + 40 + 100 and pos[1] > 645 and pos[1] < 645 + 150:
                        old_card_selected = self.card_selected
                        self.card_selected = i + self.hand_pos
                        if self.card_selected == old_card_selected:
                            self.card_selected = None
                            self.available_card_use = []
                        self.unit_selected = None
                        self.available_attacks = []
                        self.available_moves = []
                        self.available_abilities = []
                        return
                for i in self.available_card_use:
                    s_pos = self.screen_coords(i[0], i[1])
                    sx = s_pos[0]
                    sy = s_pos[1]
                    if pos[0] > sx * 32 and pos[0] < sx * 32 + 32 and pos[1] > sy * 32 and pos[1] < sy * 32 + 32:
                        self.n.use_card(self.card_selected, i[0], i[1])
                        self.card_selected = None
                        self.available_card_use = []
                        if self.hand_pos + self.world.CARDS_ON_SCREEN >= len(self.world.players[self.p].hand):
                            self.hand_pos = 0
                        return
                for i in self.available_abilities:
                    s_pos = self.screen_coords(i[0], i[1])
                    sx = s_pos[0]
                    sy = s_pos[1]
                    if pos[0] > sx * 32 and pos[0] < sx * 32 + 32 and pos[1] > sy * 32 and pos[1] < sy * 32 + 32:
                        self.n.use_ability(self.unit_selected, i[0], i[1], self.world.players[self.p].units[self.unit_selected].active_ability)
                        self.available_abilities = []
                for i in self.available_attacks:
                    s_pos = self.screen_coords(i[0], i[1])
                    sx = s_pos[0]
                    sy = s_pos[1]
                    if pos[0] > sx * 32 and pos[0] < sx * 32 + 32 and pos[1] > sy * 32 and pos[1] < sy * 32 + 32:
                        if self.world.players[self.p].units[self.unit_selected].actions > 0:
                            self.n.attack_unit(self.unit_selected, i[0], i[1])
                            self.unit_selected = None
                for i, u in enumerate(self.world.players[self.p].units):
                    s_pos = self.screen_coords(u.x, u.y)
                    sx = s_pos[0]
                    sy = s_pos[1]
                    if pos[0] > sx * 32 and pos[0] < sx * 32 + 32 and pos[1] > sy * 32 and pos[1] < sy * 32 + 32:
                        self.unit_selected = i
                        self.unit_player = self.p
                        self.card_selected = None
                        self.available_card_use = []
                        return
                if self.p == 0:
                    o = 1
                else:
                    o = 0
                for i, u in enumerate(self.world.players[o].units):
                    if u.alive is False:
                        continue
                    s_pos = self.screen_coords(u.x, u.y)
                    sx = s_pos[0]
                    sy = s_pos[1]
                    if pos[0] > sx * 32 and pos[0] < sx * 32 + 32 and pos[1] > sy * 32 and pos[1] < sy * 32 + 32:
                        self.unit_selected = i
                        self.unit_player = o
                        self.card_selected = None
                        self.available_card_use = []
                        return
                for i in self.available_moves:
                    s_pos = self.screen_coords(i[0], i[1])
                    sx = s_pos[0]
                    sy = s_pos[1]
                    if pos[0] > sx * 32 and pos[0] < sx * 32 + 32 and pos[1] > sy * 32 and pos[1] < sy * 32 + 32:
                        if self.world.players[self.p].units[self.unit_selected].moves > 0:
                            self.n.move_unit(self.unit_selected, i[0], i[1])
                self.unit_selected = None
                self.available_moves = []
                self.available_attacks = []
                self.available_abilities = []
    
    def unit_select_draw(self):
        if self.world.ready[self.p]:
            return
        place_pos = self.world.unit_starts[self.p][len(self.world.players[self.p].units)]
        s_pos = self.screen_coords(place_pos[0], place_pos[1])
        sx = s_pos[0]
        sy = s_pos[1]
        if self.place_flicker % 20 < 10:
            pass
        else:
            pygame.draw.rect(screen, (255, 255, 0), (sx * 32, sy * 32, 32, 32))
        self.place_flicker += 1
        for i, u in enumerate(unit_data.keys()):
            if self.unit_selected_menu == u:
                cursor = images["Cursor"].copy()
                cursor = pygame.transform.scale(cursor, (64, 64))
                screen.blit(cursor, (i * 65 + 4, 699)) #65, 65))
        u = self.unit_selected_menu
        if u is not None:
            text = self.font.render(u, 0, (255, 255, 255))
            screen.blit(text, (750, 635))
            text = self.font.render("Attack: " + str(unit_data[u]["attack"]), 0, (255, 255, 255))
            screen.blit(text, (750, 655))
            text = self.font.render("Defense: " + str(unit_data[u]["defense"]), 0, (255, 255, 255))
            screen.blit(text, (750, 675))
            text = self.font.render("Health: " + str(unit_data[u]["health"]), 0, (255, 255, 255))
            screen.blit(text, (750, 695))
            text = self.font.render("Straight Movement: " + str(unit_data[u]["straight_movement"]), 0, (255, 255, 255))
            screen.blit(text, (750, 715))
            text = self.font.render("Diagonal Movement:" + str(unit_data[u]["diagonal_movement"]), 0, (255, 255, 255))
            screen.blit(text, (750, 735))
            text = self.font.render("Straight Attack: " + str(unit_data[u]["straight_attack"]), 0, (255, 255, 255))
            screen.blit(text, (750, 755))
            text = self.font.render("Diagonal Attack:" + str(unit_data[u]["diagonal_attack"]), 0, (255, 255, 255))
            screen.blit(text, (750, 775))

    def unit_select_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if self.world.ready[self.p]:
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                place_pos = self.world.unit_starts[self.p][len(self.world.players[self.p].units)]
                s_pos = self.screen_coords(place_pos[0], place_pos[1])
                sx = s_pos[0] * 32
                sy = s_pos[1] * 32
                if pos[0] > sx and pos[0] < sx + 32 and pos[1] > sy and pos[1] < sy + 32 and self.unit_selected_menu is not "":
                    self.n.place_unit(self.unit_selected_menu, place_pos[0], place_pos[1])
                for i, u in enumerate(unit_data.keys()):
                    if pos[0] > 65 * i + 5 and pos[0] < 65 * i + 64 + 5 and pos[1] > 700 and pos[1] < 764:
                        self.unit_selected_menu = u
        
    def screen_coords(self, x, y):
        if self.p == 0:
            s_pos = (x, y)
        else:
            s_pos = get_player2_pos(x, y)
        return s_pos

    def load_deck(self):
        file = open(self.deck_file, "r")
        deck = file.readlines()
        self.n.set_deck(deck)
    
    def get_IP(self):
        name = ""
        pressed = False
        while pressed == False:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and len(name) > 0:
                        pressed = True
                    elif event.key == pygame.K_BACKSPACE:
                        if len(name) > 0:
                            name = name[:-1]
                    elif len(name) < 20:
                        name += event.unicode
            screen.fill((0, 0, 0))
            text = self.font.render("IP Address: ", 0, (255, 255, 255))
            screen.blit(text, (10, 10))
            text = self.font.render(name, 0, (255, 255, 255))
            screen.blit(text, (160, 10))
            pygame.display.flip()
        
        return name
    
    def get_port(self):
        name = ""
        pressed = False
        while pressed == False:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and len(name) > 0:
                        pressed = True
                    elif event.key == pygame.K_BACKSPACE:
                        if len(name) > 0:
                            name = name[:-1]
                    elif len(name) < 20:
                        name += event.unicode
            screen.fill((0, 0, 0))
            text = self.font.render("Port: ", 0, (255, 255, 255))
            screen.blit(text, (10, 10))
            text = self.font.render(name, 0, (255, 255, 255))
            screen.blit(text, (80, 10))
            pygame.display.flip()
        
        return int(name)
    
    def get_name(self):
        name = ""
        pressed = False
        while pressed == False:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and len(name) > 0:
                        pressed = True
                    elif event.key == pygame.K_BACKSPACE:
                        if len(name) > 0:
                            name = name[:-1]
                    elif len(name) < 10:
                        name += event.unicode
            screen.fill((0, 0, 0))
            text = self.font.render("Player name: ", 0, (255, 255, 255))
            screen.blit(text, (10, 10))
            text = self.font.render(name, 0, (255, 255, 255))
            screen.blit(text, (160, 10))
            pygame.display.flip()
        
        self.n.set_name(name)
    
    def get_deck_name(self):
        name = ""
        pressed = False
        while pressed == False:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and len(name) > 0:
                        if os.path.isfile("decks/" + name + ".txt"):
                            pressed = True
                    elif event.key == pygame.K_BACKSPACE:
                        if len(name) > 0:
                            name = name[:-1]
                    elif len(name) < 10:
                        name += event.unicode
            screen.fill((0, 0, 0))
            text = self.font.render("Deck file: ", 0, (255, 255, 255))
            screen.blit(text, (10, 10))
            text = self.font.render(name, 0, (255, 255, 255))
            screen.blit(text, (120, 10))
            pygame.display.flip()
        
        return name
        

client = Client()
client.main()
