
from sys import exit
import pygame
from images import sheetfixer

pygame.init()

# the display for the game
size = (1000, 600)
screen = pygame.display.set_mode(size)
pygame.display.set_caption('A Certain Text Based Adventure')
clock = pygame.time.Clock()


test_surface = pygame.surface.Surface((150, 200))
test_surface.fill('orange')

# module changes image grids into individual sprites
char_sprites = sheetfixer('graphics/player_sprites.png')
monster_sprites1 = sheetfixer('graphics/monster_sprites_1.png')
monster_sprites2 = sheetfixer('graphics/monster_sprites_2.png')
monster_sprites3 = sheetfixer('graphics/monster_sprites_3.png')

while True:
    # searches for inputs from player
    for event in pygame.event.get():
        # quits the game if you press x on the window
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    # draws elements
    screen.fill('silver')
    screen.blit(test_surface, (100,75))
    rect = char_sprites[1].get_rect()
    rect.center = 178, 178
    screen.blit(char_sprites[1], rect)


    # updates the game
    pygame.display.update()
    clock.tick(60)