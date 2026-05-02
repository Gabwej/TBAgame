import pygame
from assets.sounds import SoundManager


# this is the blueprint for my buttons, I can create any shape with text
# and unique actions that effect the game state
class Button:
    def __init__(self, rect, text, action,
                 color=(255, 248, 220),
                 text_color=(139, 69, 19),
                 outline_color=(222, 184, 135),
                 locked=False,
                 hover_panel_data=None,
                 ):

        self.rect = pygame.Rect(rect)
        self.text = text
        self.action = action
        self.font = pygame.font.Font('graphics/RetroByte.ttf', 32)
        self.hovered = False
        self.locked = locked
        self.was_hovered = False

        # makes color correcting easier
        self.color = color
        self.text_color = text_color
        self.outline_color = outline_color

        self.hover_panel_data = hover_panel_data
        self.icon = None

    def get_hover_panel(self):
        if self.hovered and self.hover_panel_data and not self.locked:
            return self.hover_panel_data
        return None

    # this makes my buttons send the next game state if clicked
    def handle_event(self, event):
        if not self.locked:
            mouse_over = self.rect.collidepoint(pygame.mouse.get_pos())

            if mouse_over and not self.was_hovered:
                SoundManager.play("hover")

            self.hovered = mouse_over
            self.was_hovered = mouse_over
        else:
            self.hovered = False
            self.was_hovered = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if not self.locked:
                if self.rect.collidepoint(event.pos):
                    SoundManager.play("press")
                    return self.action()

    # this draws all my buttons
    def draw(self, screen):
        if self.hovered:
            color = (
                min(self.color[0] + 35, 255),
                min(self.color[1] + 35, 255),
                min(self.color[2] + 35, 255))

        elif self.locked:
            color = (
                max(0, self.color[0] - 90),
                max(0, self.color[1] - 90),
                max(0, self.color[2] - 90)
            )

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

        text_x_offset = 0

        # draw icon if exists
        if self.icon:
            icon_rect = self.icon.get_rect()
            icon_rect.centery = self.rect.centery
            icon_rect.x = self.rect.x + 10

            screen.blit(self.icon, icon_rect)
            text_x_offset = 16  # 👈 shift text

        # draw text
        text_rect = text_surface.get_rect(center=self.rect.center)
        text_rect.x += text_x_offset

        screen.blit(text_surface, text_rect)


# this makes all my surfaces that are not images
class Panel:
    def __init__(self, rect, color=(255, 228, 181), text="", text_color=(128, 0, 0),
                 typewriter=True, size=32, outline=(222, 184, 135), radius=0):
        self.rect = pygame.Rect(rect)
        self.color = color

        self.text = text
        self.size = size
        self.font = pygame.font.Font('graphics/RetroByte.ttf', size)
        self.text_color = text_color
        self.outline = outline
        self.radius = radius

        self.padding = 20

        self.typewriter = typewriter
        self.visible_chars = 0
        self.speed = 1

        self.icon = None

    def update(self):
        if self.typewriter:
            if self.visible_chars < len(self.text):
                self.visible_chars += self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, border_radius=self.radius)
        pygame.draw.rect(screen, self.outline, self.rect, 5, border_radius=self.radius)

        if self.text and self.font:
            if self.typewriter:
                visible_text = self.text[:self.visible_chars]
            else:
                visible_text = self.text

            self.draw_text(screen, visible_text)

    def draw_text(self, screen, text):
        x = self.rect.x + self.padding
        y = self.rect.y + self.padding

        text_x_offset = 0

        # icon first (layout decision before text)
        if self.icon:
            icon_rect = self.icon.get_rect()
            icon_rect.x = x
            icon_rect.centery = self.rect.y + self.rect.height // 2

            screen.blit(self.icon, icon_rect)
            text_x_offset = 16

        x += text_x_offset

        max_width = self.rect.width - self.padding * 2 - text_x_offset

        final_lines = []

        raw_lines = text.split("\n")

        for raw_line in raw_lines:
            words = raw_line.split(" ")
            words = [word + " " for word in words]
            current_line = ""

            for word in words:
                test_line = current_line + word
                test_surface = self.font.render(test_line, True, self.text_color)

                if test_surface.get_width() > max_width:
                    final_lines.append(current_line)
                    current_line = word + ""
                else:
                    current_line = test_line

            final_lines.append(current_line)

        for line in final_lines:
            rendered_line = self.font.render(line, True, self.text_color)
            screen.blit(rendered_line, (x, y))
            y += self.font.get_height()


# this class implements images easier and gives me the ability to resize images (game changer :O)
class ImageObject:
    def __init__(self, path, rect, size=None, visible=True):
        if isinstance(path, str):
            self.image = pygame.image.load(path).convert_alpha()
        else:
            self.image = path

        if size:
            self.image = pygame.transform.scale(self.image, size)

        self.rect = self.image.get_rect(topleft=rect)

        self.visible = visible

    def draw(self, screen):
        if self.visible:
            screen.blit(self.image, self.rect)
