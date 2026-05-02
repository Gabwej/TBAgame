
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

def load_icon_sheet(name, cols, rows, size):
    sheet = pygame.image.load(name).convert_alpha()

    icons = []

    for row in range(rows):
        row_icons = []
        for col in range(cols):
            x = col * size
            y = row * size

            icon = sheet.subsurface((x, y, size, size)).copy()
            row_icons.append(icon)

        icons.append(row_icons)

    return icons

class Assets:
    sprites = {}
    icons = None

# this module stores all the image files
def load_all_sprites():

    Assets.sprites =  {
        "player": sheetfixer('graphics/player_sprites.png', flip_mode=5),
        "monster1": sheetfixer('graphics/monster_sprites_1.png', flip_mode="all"),
        "monster2": sheetfixer('graphics/monster_sprites_2.png', flip_mode="all"),
        "monster3": sheetfixer('graphics/monster_sprites_3.png', flip_mode="all"),

    }

    Assets.icons = load_icon_sheet(
        'graphics/icons32x32.png',
        cols=16,
        rows=28,
        size=32
    )