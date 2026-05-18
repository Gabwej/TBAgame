import pygame
from ui.ending import EndScreen
from ui.tools import Button, Panel, ImageObject
from assets.images import  get_sprite, resolve_icon


class BattleBase:
    def __init__(self, battle):
        self.battle = battle

        self.mode = "main"

        self.hover_panel = None
        self.current_hover_data = None

        self.buttons = []
        self.panels = []

        background = self.battle.background or "graphics/summer5.png"

        self.images = [
            ImageObject(background, (0, 0), (600, 400)),
            ImageObject(get_sprite(self.battle.player.sprite), (20, 240), (128, 128)),
            ImageObject(get_sprite(self.battle.enemy.sprite), (440, 240), (128, 128)),
        ]

        self.build_buttons()
        self.build_panels()

    def build_buttons(self):
        if self.mode == "main":
            self.buttons = [
                Button((20, 400, 270, 80), "Attack", self.open_attack),
                Button((310, 400, 270, 80), "Inventory", self.inventory_mode),
                Button((20, 500, 270, 80), "Check", self.check_mode),
                Button((310, 500, 270, 80), "Run", self.run_action, locked=True),
                Button((665, 500, 270, 80), "Next", self.next_log,
                       locked=not self.battle.waiting_for_continue),
            ]


        elif self.mode == "attack":
            self.buttons = []
            positions = [
                (20, 400, 270, 80),
                (310, 400, 270, 80),
                (20, 500, 270, 80),
                (310, 500, 270, 80),
            ]
            for i, attack in enumerate(self.battle.player.attacks):
                text = (
                    f"{attack.name} ({attack.current_cooldown})"
                    if attack.current_cooldown > 0
                    else attack.name
                )
                btn = Button(
                    positions[i],
                    text,
                    lambda idx=i: self.use_attack(idx),
                    locked=not attack.is_ready()
                )
                btn.hover_data = attack.description
                self.buttons.append(btn)

            # fill empty slots if fewer than 4 attacks
            while len(self.buttons) < 4:
                self.buttons.append(
                    Button(
                        positions[len(self.buttons)],
                        "None",
                        lambda: None,
                        locked=True
                    )
                )
            # back button

            self.buttons.append(
                Button(
                    (665, 500, 270, 80),
                    "Back",
                    self.back_to_main
                )
            )

        elif self.mode == "inventory":
            self.buttons = [
                Button((20, 400, 270, 80), "Did", lambda: None, locked=True),
                Button((310, 400, 270, 80), "Not", lambda: None, locked=True),
                Button((20, 500, 270, 80), "Have", lambda: None, locked=True),
                Button((310, 500, 270, 80), "Time...", lambda: None, locked=True),
                Button((665, 500, 270, 80), "Back", self.back_to_main, locked=False),
            ]

        elif self.mode == "check":
            self.buttons = [
                Button((20, 400, 270, 80), "Check", lambda: None, locked=True),
                Button((310, 400, 270, 80), "Over", lambda: None, locked=True),
                Button((20, 500, 270, 80), "There", lambda: None, locked=True),
                Button((310, 500, 270, 80), "Please", lambda: None, locked=True),
                Button((665, 500, 270, 80), "Back", self.back_to_main, locked=False),
            ]

        elif self.mode == "run":
            self.buttons = [
                Button((20, 400, 270, 80), "None", lambda: None, locked=True),
                Button((310, 400, 270, 80), "None", lambda: None, locked=True),
                Button((20, 500, 270, 80), "None", lambda: None, locked=True),
                Button((310, 500, 270, 80), "None", lambda: None, locked=True),
                # should not be locked later, actual run action!
                Button((665, 500, 270, 80), "Escape!", lambda: None, locked=True),
            ]

    def build_panels(self):

        battle_text = self.battle.get_current_log()

        if not battle_text:
            battle_text = "Choose an action."

        if self.mode == "main":
            self.panels = [
                Panel((0, 380, 600, 220),
                      color=(139, 69, 19),
                      outline=(160, 82, 45)),

                Panel(
                    (600, 0, 400, 600),
                    text=battle_text
                )
            ]

            # try a known icon

        elif self.mode == "attack":
            self.panels = [
                Panel((0, 380, 600, 220),
                      color=(139, 69, 19),
                      outline=(160, 82, 45)),

                Panel(
                    (600, 0, 400, 600),
                    text=battle_text
                )
            ]

        elif self.mode == "inventory":
            self.panels = [
                Panel((0, 380, 600, 220),
                      color=(139, 69, 19),
                      outline=(160, 82, 45)),

                Panel(
                    (600, 0, 400, 600),
                    text="Inventory not implemented."
                )
            ]

        elif self.mode == "check":
            self.panels = [
                Panel((0, 380, 600, 220),
                      color=(139, 69, 19),
                      outline=(160, 82, 45)),

                Panel(
                    (600, 0, 400, 600),
                    text=
                    f"--- Enemy ---\n"
                    f"{self.battle.enemy.name}\n"
                    f"{self.battle.enemy.description}\n\n"
                    f"HP: {self.battle.enemy.hp}/{self.battle.enemy.max_hp}\n"
                    f"ATK: {self.battle.enemy.attack}\n\n"
                    f"--- PLAYER ---\n"
                    f"HP: {self.battle.player.hp}/{self.battle.player.max_hp}\n"
                    f"ATK: {self.battle.player.attack}\n"
                    f"DEF: {self.battle.player.defense}"
                )

            ]

        elif self.mode == "run":
            self.panels = [
                Panel((0, 380, 600, 220),
                      color=(139, 69, 19),
                      outline=(160, 82, 45)),

                Panel(
                    (600, 0, 400, 600),
                    text="You used the Joestar Secret Technique!"
                )
            ]



    def open_attack(self):
        self.mode = "attack"
        self.build_buttons()
        self.build_panels()

    def back_to_main(self):
        self.mode = "main"
        self.build_buttons()
        self.build_panels()

    def inventory_mode(self):
        self.mode = "inventory"
        self.build_buttons()
        self.build_panels()

    def check_mode(self):
        self.mode = "check"
        self.build_buttons()
        self.build_panels()

    def run_action(self):
        self.mode = "run"
        self.build_buttons()
        self.build_panels()

    def use_attack(self, index):
        self.battle.player_attack(self.battle.player.attacks[index])

        self.mode = "main"

        self.build_buttons()
        self.build_panels()

        return None

    def next_log(self):
        self.battle.next_log()
        self.build_panels()
        self.refresh_buttons()

    def input_blocked_by_logs(self):
        return self.battle.waiting_for_continue

    def refresh_buttons(self):

        # MAIN MODE
        if self.mode == "main":

            waiting = self.battle.waiting_for_continue

            # Attack
            self.buttons[0].locked = waiting

            # Inventory
            self.buttons[1].locked = waiting

            # Check
            self.buttons[2].locked = waiting

            # Run
            self.buttons[3].locked = waiting

            # Next
            self.buttons[4].locked = not waiting

        # ATTACK MODE
        elif self.mode == "attack":

            for i, btn in enumerate(self.buttons[:4]):

                if i >= len(self.battle.player.attacks):
                    btn.locked = True
                    btn.icon = None
                    continue

                atk = self.battle.player.attacks[i]

                btn.text = f"{atk.name}" if atk.is_ready() else f"CD: ({atk.current_cooldown})"

                btn.icon = resolve_icon(atk.icon_id)

                btn.locked = (
                        not atk.is_ready()
                        or self.battle.turn != "player"
                        or self.battle.waiting_for_continue
                )

            self.buttons[4].locked = False


        else:

            self.buttons[4].locked = False

    def update_hover(self):

        mouse_pos = pygame.mouse.get_pos()

        hovered_data = None

        for button in self.buttons:

            if not hasattr(button, "hover_data"):
                continue

            if button.rect.collidepoint(mouse_pos):
                hovered_data = button.hover_data
                break

        if hovered_data is None:
            self.hover_panel = None
            self.current_hover_data = None
            return

        if hovered_data == self.current_hover_data:
            return

        self.current_hover_data = hovered_data

        self.hover_panel = Panel(
            (620, 260, 360, 220),
            text=hovered_data
        )

    def handle_input(self, event):
        for button in self.buttons:
            new_state = button.handle_event(event)
            if new_state:
                return new_state


    def update(self):
        self.refresh_buttons()
        self.update_hover()

        if self.battle.battle_over:
            if hasattr(self.battle, "return_ui"):
                if self.battle.result == "win":
                    self.battle.return_ui.after_battle_win()
                    return self.battle.return_ui

                elif self.battle.result == "lose":
                    return EndScreen(
                        self.battle.player,
                        "lose"
                    )

            else:
                if self.battle.result == "win":
                    return EndScreen(
                        self.battle.player,
                        "win"
                    )

                elif self.battle.result == "lose":
                    return EndScreen(
                        self.battle.player,
                        "lose"
                    )


    def draw(self, screen):
        screen.fill((0, 0, 50))

        for image in self.images:
            image.draw(screen)

        for panel in self.panels:
            panel.update()
            panel.draw(screen)

        for button in self.buttons:
            button.draw(screen)

        if self.hover_panel:
            self.hover_panel.update()
            self.hover_panel.draw(screen)