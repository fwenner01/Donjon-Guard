import pygame

images = {}

image_data = {
    "Cursor": ["assets/sprite_270.png", (32, 32)],
    "Arrow_L": ["assets/arrowleft.png", (32, 32)],
    "Arrow_R": ["assets/arrowright.png", (32, 32)],
    "Arrow_U": ["assets/arrowup.png", (32, 32)],
    "Arrow_D": ["assets/arrowdown.png", (32, 32)],
    "Button": ["assets/button.png", (60, 30)],
    "Card_Background": ["assets/woodbackground.png", (1120, 200)],
    "Card_Base": ["assets/paperbackground.png", (100, 150)],
    "Event_Background": ["assets/paperbackground.png", (250, 100)],
    "Sword": ["assets/sprite_132.png", (50, 50)],
    "Broadsword": ["assets/sprite_136.png", (50, 50)],
    "Shield": ["assets/sprite_172.png", (50, 50)],
    "Speedy Amulet": ["assets/sprite_094.png", (50, 50)],
    "Potion": ["assets/sprite_098.png", (50, 50)],
    "Potion+": ["assets/sprite_099.png", (50, 50)],
    "Meat": ["assets/sprite_096.png", (50, 50)],
    "Healing Spell": ["assets/sprite_250.png", (50, 50)],
    "Double Attack": ["assets/sprite_255.png", (50, 50)],
    "Iron Wall": ["assets/sprite_177.png", (50, 50)],
    "Rally": ["assets/sprite_257.png", (50, 50)],
    "Final Charge": ["assets/sprite_253.png", (50, 50)],
    "Superb Arrow": ["assets/sprite_159.png", (50, 50)],
    "Stronghold": ["assets/sprite_078.png", (50, 50)],
    "Grass": ["assets/sprite_050.png", (32, 32)],
    "Tree": ["assets/sprite_057.png", (32, 32)],
    "Chest": ["assets/sprite_084.png", (32, 32)],
    "Water": ["assets/sprite_070.png", (32, 32)],
    "Shop": ["assets/sprite_077.png", (32, 32)],
    "Dirt": ["assets/sprite_051.png", (32, 32)],
    "Weeds": ["assets/sprite_053.png", (32, 32)],
    "Bridge": ["assets/sprite_059.png", (32, 32)],
    "Cave": ["assets/sprite_067.png", (32, 32)],
    "Knight": ["assets/sprite_195.png", (32, 32)],
    "Fairy": ["assets/sprite_206.png", (32, 32)],
    "Minotaur": ["assets/sprite_223.png", (32, 32)],
    "Golem": ["assets/sprite_227.png", (32, 32)],
    "Monkey": ["assets/sprite_203.png", (32, 32)],
    "Ninja": ["assets/sprite_193.png", (32, 32)],
    "Archer": ["assets/sprite_192.png", (32, 32)],
    "Cost": ["assets/sprite_110.png", "assets/sprite_111.png", "assets/sprite_112.png", "assets/sprite_113.png", "assets/sprite_114.png", "assets/sprite_115.png", "assets/sprite_116.png", "assets/sprite_117.png", "assets/sprite_118.png", "assets/sprite_119.png"]
}

for i in image_data.keys():
    if i == "Cost":
        for j in range(len(image_data[i])):
            images[j] = pygame.image.load(image_data[i][j])
            images[j] = pygame.transform.scale(images[j], (32, 32))
    else:
        images[i] = pygame.image.load(image_data[i][0])
        images[i] = pygame.transform.scale(images[i], image_data[i][1])
