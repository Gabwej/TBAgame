import pygame

class Button:
    def __init__(self, rect, text, action, font):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.action = action
        self.font = font

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.action()

    def draw(self, screen):
        pygame.draw.rect(screen, 'corn silk', self.rect)

        text_surface = self.font.render(self.text, True, 'saddle brown')
        text_rect = text_surface.get_rect(center=self.rect.center)