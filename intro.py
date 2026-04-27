from tools import Button, Panel, ImageObject, Sounds
from images import Assets


# This is the intro to the game, which includes an easy menu, quick backstory and character select screen
class Intro:
    def __init__(self):
        self.buttons = [
            Button((365, 400, 270, 80), "Start", self.go_to_a),
        ]

        self.panels = [
            Panel((65, 100, 870, 100), text="A Certain Text Based Adventure", typewriter=False, size=62, radius=12),
        ]

        self.images = [
            ImageObject("graphics/landscape1.png", (0, 0), (1000, 600), ),
            ImageObject(Assets.sprites["player"][4], (237, 360), (128, 128)),
            ImageObject(Assets.sprites["monster2"][6], (635, 360), (128, 128)),
        ]

    def go_to_a(self):
        return Background()

    def handle_input(self, event):
        for button in self.buttons:
            new_state = button.handle_event(event)
            if new_state:
                return new_state

    def update(self):
        pass

    def draw(self, screen):
        screen.fill((0, 0, 50))

        for image in self.images:
            image.draw(screen)

        for panel in self.panels:
            panel.update()
            panel.draw(screen)

        for button in self.buttons:
            button.draw(screen)


class Background:
    def __init__(self):
        self.buttons = [
            Button((365, 400, 270, 80), "Next", self.to_character_picker, ),
        ]

        self.panels = [
            Panel((65, 100, 870, 200), text="Long before time had a name this land was full of mystical beings. "
                                            "\nYou are on a journey through this vast kingdom where you hope to find your life's purpose",
                  radius=12)
        ]

        self.images = [
            ImageObject("graphics/landscape1.png", (0, 0), (1000, 600))
        ]

    def to_character_picker(self):
        return CharacterPicker()

    def handle_input(self, event):
        for button in self.buttons:
            new_state = button.handle_event(event)
            if new_state:
                return new_state

    def update(self):
        pass

    def draw(self, screen):
        screen.fill((0, 0, 50))

        for image in self.images:
            image.draw(screen)

        for panel in self.panels:
            panel.update()
            panel.draw(screen)

        for button in self.buttons:
            button.draw(screen)


class CharacterPicker:
    def __init__(self):
        self.buttons = [
            Button((365, 460, 270, 80), "Start Game", self.start_game, locked=True),
            Button((80, 350, 150, 80), "Warrior", lambda: self.select_panel(1, (95, 158, 160)), ),
            Button((310, 350, 150, 80), "Ranger", lambda: self.select_panel(2, (60, 179, 113)), ),
            Button((540, 350, 150, 80), "Mage", lambda: self.select_panel(3, (100, 149, 237)), ),
            Button((770, 350, 150, 80), "Rouge", lambda: self.select_panel(4, (143, 188, 143)), ),
        ]

        self.panels = [
            # make panel color change when pressing button?
            Panel((335, 40, 330, 60), text="Pick your character!", radius=12),
            Panel((80, 120, 150, 210), radius=12, ),
            Panel((310, 120, 150, 210), radius=12),
            Panel((540, 120, 150, 210), radius=12),
            Panel((770, 120, 150, 210), radius=12)
        ]

        self.images = [
            ImageObject("graphics/landscape1.png", (0, 0), (1000, 600))
        ]

        self.sprites = [
            ImageObject(Assets.sprites["player"][4], (91, 161), (128, 128)),
            ImageObject(Assets.sprites["player"][1], (321, 161), (128, 128)),
            ImageObject(Assets.sprites["player"][2], (551, 161), (128, 128)),
            ImageObject(Assets.sprites["player"][0], (781, 161), (128, 128)),
        ]

    def start_game(self):
        return Intro()

    def select_panel(self, index, color):
        default_color = (255, 228, 181)
        default_outline = (222, 184, 135)

        for panel in self.panels[1:]:
            panel.color = default_color
            panel.outline = default_outline

        outline = (
            max(0, color[0] - 30),
            max(0, color[1] - 30),
            max(0, color[2] - 30),
        )

        self.panels[index].color = color
        self.panels[index].outline = outline

        self.selected_color = color
        self.selected_outline = outline
        self.buttons[0].locked = False

    # add return color here later for battle ui

    def handle_input(self, event):
        for button in self.buttons:
            new_state = button.handle_event(event)
            if new_state:
                return new_state

    def update(self):
        pass

    def draw(self, screen):
        screen.fill((0, 0, 50))

        for image in self.images:
            image.draw(screen)

        for panel in self.panels:
            panel.update()
            panel.draw(screen)

        for sprite in self.sprites:
            sprite.draw(screen)

        for button in self.buttons:
            button.draw(screen)
