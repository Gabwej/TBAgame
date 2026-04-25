from tools import Button, Panel


# This is the intro to the game, which includes an easy menu, quick backstory and character select screen
class Intro:
    def __init__(self):
        self.buttons = [
            Button((365, 400, 270, 80), "Start", self.go_to_a),
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
        for button in self.buttons:
            button.draw(screen)

        for panel in self.panels:
            panel.update()
            panel.draw(screen)