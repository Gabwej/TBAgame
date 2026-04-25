import pygame

# this is the blueprint for my buttons, I can create any shape with text
# and unique actions that effect the game state
class Button:
    def __init__(self, rect, text, action):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.action = action
        self.font = pygame.font.Font('graphics/RetroByte.ttf', 32)

# this makes my buttons send the next game state if clicked
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return self.action()

    def draw(self, screen):
        pygame.draw.rect(screen, 'corn silk', self.rect)

        text_surface = self.font.render(self.text, True, 'saddle brown')
        text_rect = text_surface.get_rect(center=self.rect.center)

        screen.blit(text_surface, text_rect)