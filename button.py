import pygame

# this is the blueprint for my buttons, I can create any shape with text
# and unique actions that effect the game state
class Button:
    def __init__(self, rect, text, action,
                 color= (255,248,220),
                 text_color = (139,69,19),
                 outline_color = (222,184,135)):

        self.rect = pygame.Rect(rect)
        self.text = text
        self.action = action
        self.font = pygame.font.Font('graphics/RetroByte.ttf', 32)
        self.hovered = False

        # makes color correcting easier
        self.color = color
        self.text_color = text_color
        self.outline_color = outline_color

# this makes my buttons send the next game state if clicked
    def handle_event(self, event):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.hovered = True
        else:
            self.hovered = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return self.action()

    def draw(self, screen):
        if self.hovered:
            color = (
                min(self.color[0] + 35, 255),
                min(self.color[1] + 35, 255),
                min(self.color[2] + 35, 255))


        else:
            color = self.color

        pygame.draw.rect(
            screen,
            color,
            self.rect,
            border_radius=12
        )

        pygame.draw.rect(
            screen,
            self.outline_color,
            self.rect,
            width=5,
            border_radius=12
        )

        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)

        screen.blit(text_surface, text_rect)