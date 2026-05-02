from entities.base import Entity

# our enemy base which gets used for the active enemy
class Enemy(Entity):
    def __init__(self, name, hp, attack, defense, sprite=None, tier=1, description=""):
        super().__init__(name, hp, attack, defense, sprite)

        self.tier = tier
        self.description = description
        self.attacks = []
        self.money_drop = (5, 10)

