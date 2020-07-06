import pygame
from images import images

class Card:

    def __init__(self, name):
        self.name = name
        self.type = card_data[self.name]["type"]
        self.cost = card_data[self.name]["cost"]
        self.stat_boosts = {}
        if "stat_boosts" in card_data[self.name].keys():
            for i in card_data[self.name]["stat_boosts"].keys():
                self.stat_boosts[i] = card_data[self.name]["stat_boosts"][i]
        if "only" in card_data[self.name]:
            self.only = card_data[self.name]["only"]
        else:
            self.only = None

    def draw(self, screen, pos):
        base = images["Card_Base"].copy()
        image = images[self.name]
        base.blit(image, (25, 15))
        cost = images[self.cost]
        base.blit(cost, (70, 120))
        font = pygame.font.SysFont("Courier New", 11)
        title = font.render(self.name, 0, (0, 0, 0))
        base.blit(title, (0, 0))
        for i in range(card_data[self.name]["text"][0]):
            text = font.render(card_data[self.name]["text"][i + 1], 0, (0, 0, 0))
            base.blit(text, (3, 70 + (i * 13)))
        if "only" in card_data[self.name]:
            only = font.render(card_data[self.name]["only"], 0, (0, 0, 0))
            base.blit(only, (0, 135))
        if type(pos) == tuple:
            screen.blit(base, (pos[0], pos[1]))
        else:
            screen.blit(base, (110 * pos + 40, 645))

card_data = {
    "Sword": {
        "type": "equipment",
        "text": [3, "", "Equip to unit", "Attack: +1"],
        "cost": 3,
        "stat_boosts": {
            "Attack": 1
        }
    },
    "Broadsword": {
        "type": "equipment",
        "text": [3, "", "Equip to unit", "Attack: +3"],
        "cost": 6,
        "stat_boosts": {
            "Attack": 3
        }
    },
    "Shield": {
        "type": "equipment",
        "text": [3, "", "Equip to unit", "Defense: +1"],
        "cost": 3,
        "stat_boosts": {
            "Defense": 1
        }
    },
    "Speedy Amulet": {
        "type": "equipment",
        "text": [3, "", "Equip to unit", "Movement: +1"],
        "cost": 3,
        "stat_boosts": {
            "Max_Move": 1
        }
    },
    "Potion": {
        "type": "utility",
        "text": [3, "", "Use on unit", "Health: +1"],
        "cost": 2,
        "stat_boosts": {
            "Health": 1
        }
    },
    "Potion+": {
        "type": "utility",
        "text": [3, "", "Use on unit", "Health: +3"],
        "cost": 4,
        "stat_boosts": {
            "Health": 3
        }
    },
    "Meat": {
        "type": "utility",
        "text": [3, "Use on unit", "Able to move", "twice"],
        "cost": 2,
        "stat_boosts": {
            "Moves": 1
        }
    },
    "Healing Spell": {
        "type": "ability",
        "text": [3, "", "Heal another", "unit 3 health"],
        "cost": 1,
        "only": "Fairy"
    },
    "Double Attack": {
        "type": "ability",
        "text": [3, "Allow another", "unit to attack", "twice"],
        "cost": 1,
        "only": "Fairy"
    },
    "Iron Wall": {
        "type": "ability",
        "text": [4, "Make another", "unit", "invincible", "next turn"],
        "cost": 1,
        "only": "Golem"
    },
    "Rally": {
        "type": "ability",
        "text": [3, "All units", "Attack +1", "this turn"],
        "cost": 1,
        "only": "Knight"
    },
    "Final Charge": {
        "type": "ability",
        "text": [3, "Use with", "1 Health", "Attack +5"],
        "cost": 1,
        "only": "Monkey"
    },
    "Superb Arrow": {
        "type": "ability",
        "text": [3, "", "Attack range", "+3"],
        "cost": 1,
        "only": "Archer"
    },
    "Stronghold": {
        "type": "building",
        "text": [3, "Place on", "space with", "unit"],
        "cost": 3,
    }
}

