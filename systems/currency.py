import random

class Currency:
    def __init__(self):
        self.gold = 0

    def add(self, amount):
        self.gold += amount

    def spend(self, amount):
        if self.gold >= amount:
            self.gold -= amount
            return True
        return False

    def reward_from_enemy(self, enemy):
        low, high = enemy.money_drop
        gained = random.randint(low, high)
        self.add(gained)
        return gained