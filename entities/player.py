from entities.base import Entity
from systems.currency import Currency

# this is out player base, which is then turned into the active player based on input (CharacterSelect)
class Player(Entity):
    def __init__(
            self,
            name,
            hp,
            attack,
            defense,
            sprite=None,
            crit_chance=0.1,
            crit_multiplier=1.5,
            dodge_chance=0.05
    ):
        super().__init__(
            name,
            hp,
            attack,
            defense,
            sprite,
            crit_chance,
            crit_multiplier,
            dodge_chance
        )
        self.currency = Currency()

        self.inventory = {}

        self.stats = {
            "total_damage": 0,
            "total_healing": 0,
            "battles_won": 0,
            "events": 0
        }

    def add_item(self, item, count=1):
        if item.item_id in self.inventory:
            self.inventory[item.item_id]["count"] += count
        else:
            self.inventory[item.item_id] = {
                "item": item,
                "count": count
            }

    def remove_item(self, item_id, count=1):
        if item_id in self.inventory:
            self.inventory[item_id]["count"] -= count

            if self.inventory[item_id]["count"] <= 0:
                del self.inventory[item_id]

    def get_item(self, item_id):
        return self.inventory.get(item_id, None)