
from sys import exit
import pygame
from images import sheetfixer
from tools import Button
from intro import Intro, Background

pygame.init()

# the display for the game (not to be meddled with)
size = (1000, 600)
screen = pygame.display.set_mode(size)
pygame.display.set_caption('A Certain Text Based Adventure')
clock = pygame.time.Clock()

# module changes image grids into individual sprites and stores them in different lists (15 items each)
char_sprites = sheetfixer('graphics/player_sprites.png')
monster_sprites1 = sheetfixer('graphics/monster_sprites_1.png')
monster_sprites2 = sheetfixer('graphics/monster_sprites_2.png')
monster_sprites3 = sheetfixer('graphics/monster_sprites_3.png')

current_state = Intro()
print(current_state, type(current_state))

# this is the loop that is actively updating everything every frame
while True:
    # searches for inputs from player (event loop)
    for event in pygame.event.get():
        # quits the game if you press x on the window
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        # changes the state of the game if a valuable input is detected
        new_state = current_state.handle_input(event)
        if new_state:
            current_state = new_state

    # draws elements

    current_state.update()
    current_state.draw(screen)

    # updates the game
    pygame.display.update()
    clock.tick(60)