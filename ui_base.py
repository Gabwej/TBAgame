from tools import Button

class Base:
    def __init__(self):
        # fix so text comes from other file
        self.buttons = [
            Button((20, 400, 270, 80), "Button A", self.go_to_a),
            Button((310, 400, 270, 80), "Button B", self.go_to_b),
            Button((20, 500, 270, 80), "Button C", self.go_to_c),
            Button((310, 500, 270, 80), "Button D", self.go_to_d)
        ]

    def go_to_a(self):
        return StateA()

    def go_to_b(self):
        return StateB()

    def go_to_c(self):
        return StateC()

    def go_to_d(self):
        return StateD()

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

class StateC:
    def __init__(self):
        self.buttons = [
            Button((500, 200, 200, 80), "Button C Back", self.go_back)
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

class StateD:
    def __init__(self):
        self.buttons = [
            Button((500, 200, 200, 80), "Button D Back", self.go_back)
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