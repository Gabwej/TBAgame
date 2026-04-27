import random

from entity_list import ENEMY_TIERS


class Currency:
    def __init__(self, starting_gold=0):
        self.gold = starting_gold

    def add(self, amount):
        self.gold += amount
        return amount

    def spend(self, amount):
        if self.gold >= amount:
            self.gold -= amount
            return True
        return False

    def can_afford(self, amount):
        return self.gold >= amount


def get_enemy_gold(enemy):
    teir_data = ENEMY_TIERS.get(enemy.teir)

    if not teir_data:
        return 0

    low, high = teir_data["gold_range"]
    return random.randint(low, high)
