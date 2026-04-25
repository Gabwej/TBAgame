import pygame
from button import Button

class Intro:
    def __init__(self):
        self.buttons = [
            Button((200, 200, 200, 80), "Button A", self.go_to_a),
            Button((500, 200, 200, 80), "Button B", self.go_to_b)
        ]

    def go_to_a(self):
        return StateA()

    def go_to_b(self):
        return StateB()

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


class StateA:
    def __init__(self):
        self.buttons = [
            Button((200, 200, 200, 80), "Button A Back", self.go_back)
        ]

    def go_back(self):
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

class StateB:
    def __init__(self):
        self.buttons = [
            Button((500, 200, 200, 80), "Button B Back", self.go_back)
        ]

    def go_back(self):
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