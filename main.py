from sys import exit
import pygame
from assets.images import load_all_sprites
from ui.intro import Intro
from assets.sounds import SoundManager, MusicManager

pygame.init()
pygame.mixer.init()

# the display for the game (not to be meddled with)
screen = pygame.display.set_mode((1000, 600))
pygame.display.set_caption('A Certain Text Based Adventure')
clock = pygame.time.Clock()

load_all_sprites()
SoundManager.load()
MusicManager.play_loop("sounds/theme.mp3")

current_state = Intro()

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

        MusicManager.handle_event(event)

    new_state = current_state.update()
    if new_state:
        current_state = new_state

    # draws elements
    current_state.draw(screen)

    # updates the game
    pygame.display.update()
    clock.tick(60)
