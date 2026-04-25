from tools import Button, Panel, ImageObject
from images import Assets

# This is the intro to the game, which includes an easy menu, quick backstory and character select screen
class Intro:
    def __init__(self):
        self.buttons = [
            Button((365, 400, 270, 80), "Start", self.go_to_a),
        ]

        self.panels = [
            Panel((65, 100, 870, 100), text= "A Certain Text Based Adventure", typewriter=False, size= 62 ),
        ]

        self.images = [
            ImageObject("graphics/landscape1.png", (0, 0), (1000, 600)),
            ImageObject(Assets.sprites["player"][14], (237, 360), (128, 128)),
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
            Button((365, 400, 270, 80), "Next", self.to_character_picker, locked=True),
        ]

        self.panels = [
            Panel((65, 100, 870, 200), text= "Long before time had a name this land was full of mystical beings. "
            "\nYou are on a journey through this vast kingdom where you hope  to find your life's purpose" )
        ]

        self.images = [
            ImageObject("graphics/landscape1.png", (0, 0), (1000, 600))
        ]

    def to_character_picker(self):
        return Intro()

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