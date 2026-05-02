from ui.tools import Button, Panel, ImageObject
from assets.images import Assets
from ui.intro import Intro

# this is the base for the rest of the games ui
class Base:
    def __init__(self):
        self.hover_panel = None
        self.current_hover_data = None


        # fix so text comes from other file
        self.buttons = [
            # the fight button, makes this button attack[0] and buttonD attack[3), ButtonE comes back and brings you to previous state
            Button((20, 400, 270, 80), "Button A", self.go_to_attack, hover_panel_data={
            "text": "This is the longest text i could possibly add, any longer than this and it becomes kinda weird tbh",
            }),
            # inventory button, locks buttons A-D and E comes back, creates buttons (will make ui)
            Button((310, 400, 270, 80), "Attack B", lambda: None),
            # simple check button, updates info panel to enemy info, locks A-D and E is back
            Button((20, 500, 270, 80), "Button C", lambda: None),
            # run button (locked = True) for difficult monsters until half health and stunned or escape rope
            Button((310, 500, 270, 80), "Button D", lambda: None, locked=True),
            # next button, only visible when needed (in battle next and during dialog at needed point)
            Button((665, 500, 270, 80), "Button E", lambda: None, locked=True),
            # debuff button (only here when anything has an effect, otherwise invisible)
            # on hover puts up panels for enemy and player showing turn count, not done
            Button((240, 310, 120, 60), "Debuffs", lambda: None, hover_panel_data={
            "text": "debuff stuff", "rect": (665, 500, 270, 80)
            } ),
        ]

        # REMOVE, test
        test_btn = Button((100, 100, 200, 80), "ICON TEST", lambda: None)
        test_btn.icon = Assets.icons[27][11]

        self.buttons.append(test_btn)

        self.panels = [
            Panel((0, 380, 600, 220), color=(139, 69, 19), outline=(160, 82, 45)),
            Panel((600, 0, 400, 600), text="This is an example text of how longer texts look here"
                                           "\n \nLook at that, how cool \nYou can even just do one for just one page break"),
        ]

        self.images = [
            ImageObject("graphics/landscape1.png", (0, 0), (600, 400)),
            ImageObject(Assets.sprites["player"][0], (20, 240), (128, 128)),
            ImageObject(Assets.sprites["monster3"][7], (440, 240), (128, 128)),
        ]

    def go_to_attack(self):
        return AttackPanel()

    def handle_input(self, event):
        for button in self.buttons:
            new_state = button.handle_event(event)
            if new_state:
                return new_state

    def update(self):

        pass

    def update_hover_panel(self):
        new_hover_data = None

        # find hovered button
        for button in self.buttons:
            data = button.get_hover_panel()
            if data:
                new_hover_data = data
                break  # first hovered wins

        # if hover changed → recreate panel
        if new_hover_data != self.current_hover_data:
            self.current_hover_data = new_hover_data

            if new_hover_data:
                rect = new_hover_data.get("rect", (20, 250, 560, 120))

                self.hover_panel = Panel(
                    rect,
                    color=new_hover_data.get("color", (240, 230, 200)),
                    text=new_hover_data.get("text", ""),
                    text_color=new_hover_data.get("text_color", (128, 0, 0)),
                    radius=new_hover_data.get("radius", 10),
                    typewriter=new_hover_data.get("typewriter", True)
                )
            else:
                self.hover_panel = None

        # update panel (typewriter effect)
        if self.hover_panel:
            self.hover_panel.update()

    def draw(self, screen):
        screen.fill((0, 0, 50))
        for image in self.images:
            image.draw(screen)

        for panel in self.panels:
            panel.update()
            self.update_hover_panel()
            panel.draw(screen)

        for button in self.buttons:
            button.draw(screen)

        if self.hover_panel:
            self.hover_panel.draw(screen)


class AttackPanel:
    def __init__(self):
        self.buttons = [
            Button((20, 400, 270, 80), "Attack1", lambda: None),
            Button((310, 400, 270, 80), "Attack2", lambda: None),
            Button((20, 500, 270, 80), "Attack3", lambda: None),
            Button((310, 500, 270, 80), "Attack4", lambda: None),
            Button((665, 500, 270, 80), "Next", self.battle.next_log, locked=True),
        ]

        self.panels = [
            Panel((0, 380, 600, 220), color=(139, 69, 19), outline=(160, 82, 45)),
            Panel((600, 0, 400, 600), text="This is an example text of how longer texts look here"
                                           "\n \nLook at that, how cool \nYou can even just do one for just one page break",
                  typewriter=False),
        ]

        self.images = [
            ImageObject("../graphics/landscape1.png", (0, 0), (600, 400)),
            ImageObject(Assets.sprites["player"][14], (237, 360)),
            ImageObject(Assets.sprites["monster2"][6], (635, 360)),
        ]


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
