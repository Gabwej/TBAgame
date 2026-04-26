from tools import Button, Panel, ImageObject, Sounds
from images import Assets

# this is the base for the rest of the games ui
class Base:
    def __init__(self):
        # fix so text comes from other file
        self.buttons = [
            Button((20, 400, 270, 80), "Button A", self.go_to_a),
            Button((310, 400, 270, 80), "Button B", self.go_to_b),
            Button((20, 500, 270, 80), "Button C", self.go_to_c),
            Button((310, 500, 270, 80), "Button D", self.go_to_d),
            Button((665, 500, 270, 80), "Button E", self.go_to_d, locked=True),
        ]

        self.panels = [
            Panel((0, 380, 600, 220), color= (139,69,19), outline=(160,82,45)),
            Panel((600, 0, 400, 600), text="This is an example text of how longer texts look here"
                                           "\n \nLook at that, how cool \nYou can even just do one for just one page break"),
        ]

        self.images = [
            ImageObject("graphics/landscape1.png", (0, 0), (600, 400)),
            ImageObject(Assets.sprites["player"][0], (20, 240), (128, 128)),
            ImageObject(Assets.sprites["monster3"][7], (440, 240), (128, 128)),
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
        for image in self.images:
            image.draw(screen)

        for panel in self.panels:
            panel.update()
            panel.draw(screen)

        for button in self.buttons:
            button.draw(screen)


class StateA:
    def __init__(self):
        self.buttons = [
            Button((20, 400, 270, 80), "Button A", self.go_back),
            Button((310, 400, 270, 80), "Button B", self.go_to_b),
            Button((20, 500, 270, 80), "Button C", self.go_to_c),
            Button((310, 500, 270, 80), "Button D", self.go_to_d),
            Button((665, 500, 270, 80), "Button E", self.go_to_d, locked=True),
        ]

        self.panels = [
            Panel((0, 380, 600, 220), color=(139, 69, 19), outline=(160, 82, 45)),
            Panel((600, 0, 400, 600), text="This is an example text of how longer texts look here"
                                           "\n \nLook at that, how cool \nYou can even just do one for just one page break", typewriter=False),
        ]

        self.images = [
            ImageObject("graphics/landscape1.png", (0, 0), (600, 400)),
            ImageObject(Assets.sprites["player"][14], (237, 360)),
            ImageObject(Assets.sprites["monster2"][6], (635, 360)),
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
        for image in self.images:
            image.draw(screen)

        for panel in self.panels:
            panel.update()
            panel.draw(screen)

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
        for image in self.images:
            image.draw(screen)

        for panel in self.panels:
            panel.update()
            panel.draw(screen)

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
        for image in self.images:
            image.draw(screen)

        for panel in self.panels:
            panel.update()
            panel.draw(screen)

        for button in self.buttons:
            button.draw(screen)

class StateD:
    def __init__(self):
        self.buttons = [
            Button((500, 200, 200, 80), "Button D Back", self.go_back)
        ]

    def go_back(self):
        pass


    def handle_input(self, event):
        for button in self.buttons:
            new_state = button.handle_event(event)
            if new_state:
                return new_state

    def update(self):
        return Base()
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

class StateE:
    def __init__(self):
        self.buttons = [
            Button((500, 200, 200, 80), "Button E Back", self.go_back)
        ]

    def go_back(self):
        return Base()

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