from entities.base import Entity

# our enemy base which gets used for the active enemy
class Enemy(Entity):
    def __init__(
            self,
            name,
            hp,
            attack,
            defense,
            sprite=None,
            crit_chance=0.1,
            crit_multiplier=1.5,
            dodge_chance=0.05,
            tier=1,
            description=""
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

        self.tier = tier
        self.description = description
        self.attacks = []
        self.money_drop = (5, 10)

