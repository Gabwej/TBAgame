
from ui.tools import Button, Panel, ImageObject


def build_game_over_text(player, result):
    if result == "lose":
        intro = "All great adventures must come to an end eventually...\nYou died!"
    elif result == "win":
        intro = "Victory!\nYou overcame every challenge!"
    elif result == "???":
        intro = "???\n"
    else:
        intro = "The journey ends..."

    return (
        f"{intro}\n\n"
        "These were your stats:\n\n"
        f"Character played as: {player.name}\n"
        f"Total damage done: {player.stats.get("total_damage", 0)}\n"
        f"Total health healed: {player.stats.get("total_healing", 0)}\n"
        f"Battles won: {player.stats.get("battles_won", 0)}\n"
        f"Events experienced: {player.stats.get("events", 0)}\n"
    )

class EndScreen:
    def __init__(self, player, result):
        self.player = player
        self.result = result
        self.buttons = [
            Button((365, 500, 270, 80), "QUIT", self.quit_game, ),
        ]

        self.panels = [
            Panel((395, 20, 210, 60), text="GAME OVER", radius=12, typewriter=False),
            Panel(
                (65, 100, 870, 350),
                text=build_game_over_text(self.player, self.result),
                radius=12
            )
            ]

        self.images = [
            ImageObject("graphics/Summer8.png", (0, 0), (1000, 600))
        ]


    def quit_game(self):
        return exit()

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