from assets.images import get_sprite, resolve_icon
from ui.tools import Button, Panel, ImageObject

# inactive/unused rn

class ChooseAttackEvent:
    def __init__(
        self,
        player,
        new_attack,
        next_id,
        background=None,
        sprite=None,
        return_ui=None
    ):
        self.player = player
        self.new_attack = new_attack
        self.next_id = next_id
        self.return_ui = return_ui

        self.background = background or "graphics/summer5.png"
        self.sprite = sprite

        self.mode = "choose"   # <-- IMPORTANT (choose / reward)
        self.result_text = ""

        self.buttons = []
        self.panels = []
        self.images = []

        self.build_images()
        self.build_buttons()
        self.build_panels()

    # ---------------- IMAGES ----------------
    def build_images(self):
        self.images = [
            ImageObject(self.background, (0, 0), (600, 400)),
            ImageObject(get_sprite(self.player.sprite), (20, 240), (128, 128)),
        ]

        if self.sprite:
            self.images.append(
                ImageObject(
                    get_sprite(self.sprite),
                    (440, 240),
                    (128, 128)
                )
            )

    # ---------------- PANELS ----------------
    def build_panels(self):

        if self.mode == "choose":
            text = "Choose an attack to replace or discard."

        else:
            text = self.result_text

        self.panels = [
            Panel(
                (0, 380, 600, 220),
                color=(139, 69, 45),
                outline=(160, 82, 45)
            ),
            Panel(
                (600, 0, 400, 600),
                text=text
            )
        ]

    def build_buttons(self):

        self.buttons = []

        if self.mode == "reward":

            self.buttons.append(
                Button(
                    (665, 500, 270, 80),
                    "Next",
                    self.finish
                )
            )
            return

        positions = [
            (20, 400, 270, 80),
            (310, 400, 270, 80),
            (20, 500, 270, 80),
            (310, 500, 270, 80),
        ]

        for i, attack in enumerate(self.player.attacks[:4]):

            btn = Button(
                positions[i],
                attack.name,
                lambda idx=i: self.replace_attack(idx)
            )

            btn.hover_data = attack.description
            btn.icon = resolve_icon(attack.icon_id)

            self.buttons.append(btn)

        while len(self.buttons) < 4:
            self.buttons.append(
                Button(
                    positions[len(self.buttons)],
                    "None",
                    lambda: None,
                    locked=True
                )
            )

        # new attack (discard option)
        new_btn = Button(
            (665, 500, 270, 80),
            self.new_attack.name,
            self.discard_attack
        )

        new_btn.hover_data = self.new_attack.description
        new_btn.icon = resolve_icon(self.new_attack.icon_id)

        self.buttons.append(new_btn)

    def replace_attack(self, index):

        old = self.player.attacks[index]
        self.player.attacks[index] = self.new_attack

        self.result_text = (
            f"You replaced {old.name} with {self.new_attack.name}!"
        )

        self.mode = "reward"
        self.build_buttons()
        self.build_panels()

    def discard_attack(self):

        self.result_text = (
            f"You discarded {self.new_attack.name}."
        )

        self.mode = "reward"
        self.build_buttons()
        self.build_panels()

    def finish(self):
        # go back to world progression
        return self.return_ui.get_next(self.next_id)

    def handle_input(self, event):

        for button in self.buttons:
            new_state = button.handle_event(event)
            if new_state is not None:
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