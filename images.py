import os

import pygame

# this module changes image grids into individual sprites
def sheetfixer(name, flip_mode=None):

    sheet = pygame.image.load(name).convert_alpha()

    sprite_width = 72
    sprite_height = 72

    sprites = []

    cols = 5
    rows = 3

    for row in range(rows):
        for col in range(cols):
            x = col * sprite_width
            y = row * sprite_height

            sprite = sheet.subsurface((x,y,sprite_width,sprite_height)).copy()
            sprites.append(sprite)

    if flip_mode == "all":
        for i in range (len(sprites)):
            sprites[i] = pygame.transform.flip(sprites[i], True, False)

    elif isinstance(flip_mode, int):
        for i in range (flip_mode, len(sprites)):
            sprites[i] = pygame.transform.flip(sprites[i], True, False)

    return sprites

class Assets:
    sprites = {}

# this module stores all the image files
def load_all_sprites():
    Assets.sprites =  {
        "player": sheetfixer('graphics/player_sprites.png', flip_mode=5),
        "monster1": sheetfixer('graphics/monster_sprites_1.png', flip_mode="all"),
        "monster2": sheetfixer('graphics/monster_sprites_2.png', flip_mode="all"),
        "monster3": sheetfixer('graphics/monster_sprites_3.png', flip_mode="all"),
    }