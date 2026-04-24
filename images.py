import pygame

def sheetfixer(name):

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

    return sprites