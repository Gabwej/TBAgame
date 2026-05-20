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

    def add_item(self, item, amount=1):
        item_id = item.item_id

        if item_id not in self.inventory:
            self.inventory[item_id] = {
                "item": item,
                "amount": 0
            }

        self.inventory[item_id]["amount"] += amount

    def remove_item(self, item_id, amount=1):
        if item_id not in self.inventory:
            return

        self.inventory[item_id]["amount"] -= amount

        if self.inventory[item_id]["amount"] <= 0:
            del self.inventory[item_id]

    def get_item(self, item_id):
        return self.inventory.get(item_id, None)

    def get_inventory_items(self):
        return list(self.inventory.values())

    def reset_after_battle(self):

        # restore hp
        self.hp = self.max_hp

        # clear status effects
        self.status_effects.clear()

        # clear buffs
        self.buffs.clear()

        # reset temporary modifiers
        self.attack_debuff = 0
        self.defense_debuff = 0

        # reset casting
        self.pending_action = None
        self.cast_timer = 0

        # reset attack cooldowns
        for attack in self.attacks:
            attack.current_cooldown = attack.start_cooldown