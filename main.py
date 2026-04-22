
from sys import exit
import pygame
import intro

pygame.init()

# the display for the game
size = (1000, 600)
screen = pygame.display.set_mode(size)
pygame.display.set_caption('A Certain Text Based Adventure')
clock = pygame.time.Clock()

test_surface = pygame.surface.Surface((150, 200))
test_surface.fill((255,255,255))

while True:
    # searches for inputs from player
    for event in pygame.event.get():
        # quits the game if you press x on the window
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    # draws elements

    screen.blit(test_surface, (200,100))

    # updates the game
    pygame.display.update()
    clock.tick(60)