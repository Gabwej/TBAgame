
from sys import exit
import pygame
from intro import Intro
from images import load_all_sprites, Assets
from ui_base import Base

pygame.init()

# the display for the game (not to be meddled with)
size = (1000, 600)
screen = pygame.display.set_mode(size)
pygame.display.set_caption('A Certain Text Based Adventure')
clock = pygame.time.Clock()

load_all_sprites()

current_state = Intro()
# current_state = Base()
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