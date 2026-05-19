from assets.sounds import MusicManager
from ui.tools import Button, Panel, ImageObject
from assets.images import get_sprite
from combat.battlecreation import start_event_battle

from events.event_manager import EventManager

# this is the ui for event (duh). I decided to keep it the same as the one I designed for battle since
# it keeps consistency, and it took a while to make (you know what they say:
# Better not follow a seagull when looking for a dessert, or something?)
class EventUI:

    def __init__(self, player):

        self.manager = EventManager(player)

        self.buttons = []
        self.panels = []
        self.images = []

        self.build_ui()

        MusicManager.play_loop("sounds/theme.mp3")

    def build_ui(self):

        self.build_images()
        self.build_panels()
        self.build_buttons()

    def build_images(self):

        event = self.manager.get_event()

        # This gets the background for the current event, otherwise it defaults to summer5
        background = event.get(
            "background",
            "graphics/summer5.png"
        )

        # same here, get sprite, otherwise None
        encounter_sprite = event.get(
            "encounter_sprite",
            None
        )

        # this converts the images to objects that can be put on the window (after draw ofc)
        self.images = [
            # background
            ImageObject(
                background,
                (0, 0),
                (600, 400)
            ),

            # player
            ImageObject(
                get_sprite(
                    self.manager.player.sprite
                ),
                (20, 240),
                (128, 128)
            )
        ]

        # optional encounter sprite
        if encounter_sprite:

            self.images.append(
                ImageObject(
                    get_sprite(encounter_sprite),
                    (440, 240),
                    (128, 128)
                )
            )

    # uses my panels from tools, same as images
    def build_panels(self):

        self.panels = [

            # bottom button area
            Panel(
                (0, 380, 600, 220),
                color=(139, 69, 19),
                outline=(160, 82, 45)
            ),

            # text panel
            Panel(
                (600, 0, 400, 600),

                text=self.manager.current_text
            )
        ]

    # ditto, but buttons
    def build_buttons(self):

        self.buttons = []

        positions = [
            (20, 400, 270, 80),
            (310, 400, 270, 80),
            (20, 500, 270, 80),
            (310, 500, 270, 80),
        ]

        event = self.manager.get_event()

        options = event.get("options", [])

        # choice buttons
        for i in range(4):

            if i < len(options):

                option = options[i]

                button = Button(
                    positions[i],

                    option["text"],

                    lambda idx=i:
                    self.choose_option(idx),

                    locked=(
                        self.manager.phase != "intro"
                    )
                )

            else:

                button = Button(
                    positions[i],

                    "None",

                    lambda: None,

                    locked=True
                )

            self.buttons.append(button)

        # next button
        next_button = Button(
            (665, 500, 270, 80),

            "Next",

            self.next_event,

            locked=(
                self.manager.phase != "result"
            )
        )

        self.buttons.append(next_button)

    # switches mode
    def choose_option(self, index):

        self.manager.choose_option(index)

        self.build_ui()

    def after_battle_run(self):

        event = self.manager.get_event()

        self.manager.event_index = event["next"]

        self.manager.load_event()

        MusicManager.fade_to(
            "sounds/theme.mp3",
            volume=1.0
        )
        self.build_ui()

    def next_event(self):

        self.manager.next_event()

        event = self.manager.get_event()

        if event["type"] == "battle":
            return start_event_battle(
                self.manager.player,
                event["enemy"],
                self,
                event.get("background")
            )

        self.build_ui()

    def after_battle_win(self):

        event = self.manager.get_event()

        # moves you to the next event after battle
        self.manager.event_index = event["next"]

        # changes back music to theme music
        MusicManager.fade_to("sounds/theme.mp3", volume=1.0)

        self.manager.load_event()

        self.build_ui()


    def handle_input(self, event):

        for button in self.buttons:

            result = button.handle_event(event)

            if result:
                return result


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