import random

from events.story import EVENTS
from items.item_list import ITEMS
from ui.new_attack_ui import ChooseAttackEvent


class EventManager:
    def __init__(self, player):

        self.player = player

        # progression
        self.event_index = 0

        # current event state
        self.phase = "intro"
        # intro = choosing
        # result = showing result text

        self.current_text = ""

        self.selected_option = None

        # initialize first event
        self.load_event()

    # self-explanatory, gets event from story
    def get_event(self):
        return EVENTS[self.event_index]

    def load_event(self):
        event = self.get_event()

        self.phase = "intro"
        self.selected_option = None

        self.current_text = event.get("text", "")

    # tells the game that its choice time, locks next button
    def choose_option(self, index):

        if self.phase != "intro":
            return

        event = self.get_event()

        if event["type"] != "dialog":
            return

        options = event.get("options", [])

        if index >= len(options):
            return

        option = options[index]

        self.selected_option = option

        # applies rewards (like healing or stats)if there are any
        reward_text = self.apply_effects(
            option.get("effects", [])
        )

        # builds the result text
        result = option.get("result", "")

        if reward_text:
            result += "\n\n" + reward_text

        self.current_text = result
        self.player.stats["events"] += 1
        self.phase = "result"

    # this function is what is used to go to the next battle or event
    def next_event(self):

        event = self.get_event()

        # NORMAL DIALOG FLOW
        if event["type"] == "dialog":

            if self.phase != "result":
                return

            option = self.selected_option

            if option is None:
                return

            if "next" in option:
                self.event_index = option["next"]

            elif "next_pool" in option:
                self.event_index = random.choice(option["next_pool"])

            else:
                self.event_index += 1

        self.load_event()

    # this is what gives out effects to the player
    def apply_effects(self, effects):

        reward_lines = []

        for effect in effects:
            # Simple heal effect
            if effect["type"] == "heal":

                value = effect["value"]
                self.player.hp = min(
                    self.player.max_hp,
                    self.player.hp + value
                )
                reward_lines.append(
                    f"Healed {value} HP"
                )

            # This code is what gives stats to the players, important! Otherwise choices dont seem to matter
            elif effect["type"] == "stat":

                stat = effect["stat"]
                value = effect["value"]
                current = getattr(self.player, stat)

                setattr(
                    self.player,
                    stat,
                    current + value
                )

                reward_lines.append(
                    f"{stat.upper()} +{value}"
                )


            elif effect["type"] == "item":
                item_id = effect["item"]
                item = ITEMS[item_id]
                amount = effect.get("amount", 1)
                self.player.add_item(item, amount)
                reward_lines.append(
                    f"Obtained {item.name} x{amount}"
                )

        return "\n".join(reward_lines)