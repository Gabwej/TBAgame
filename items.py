import random

class Item:
    def __init__(self, item_id, name, description, use_text):
        self.item_id = item_id
        self.name = name
        self.description = description
        self.use_text = use_text

    def use(self, user, target, battle, stats=None):
        return 0,[]

class Potion(Item):
    def __init__(self):
        super().__init__(
            "Potion",
            "Potion",
            "Heals a moderate amount of HP.",
            "You drink a potion."
        )

    def use(self, user, target, battle, stats=None):
        heal = 50 + int(25 * (pygame.time.get_ticks() % 2))  # simple 50–75 variation
        user.hp = min(user.max_hp, user.hp + heal)

        if stats:
            stats.total_healing += heal

        return 0, [f"{user.name} heals {heal} HP!"]

class Cleanse(Item):
    def __init__(self):
        super().__init__(
            "Cleanse",
            "Cleanse",
            "Removes all negative effects and debuffs.",
            "A purifying aura surrounds you."
        )

    def use(self, user, target, battle, stats=None):
        for key in user.status_effects:
            user.status_effects[key] = 0

        user.attack_debuff = 0
        user.defense_debuff = 0

        return 0, [f"{user.name} is cleansed of all effects!"]

class EscapeRope(Item):
    def __init__(self):
        super().__init__(
            "Escape Rope",
            "Escape Rope",
            "Allows you to flee from battle.",
            "You prepare to escape..."
        )

    def use(self, user, target, battle, stats=None):
        battle.escape_unlocked = True
        return 0, ["Escape route is now available!"]

class Bomb(Item):
    def __init__(self):
        super().__init__(
            "Bomb",
            "Bomb",
            "Deals damage and applies burn.",
            "You throw a bomb!"
        )

    def use(self, user, target, battle, stats=None):
        damage = target.take_damage(50)
        target.status_effects["burn"] += 3

        return damage, [
            f"{target.name} takes {damage} damage!",
            f"{target.name} is burning!"
        ]

class MysteryVial(Item):
    def __init__(self):
        super().__init__(
            "Mystery Vial",
            "Mystery Vial",
            "Applies a random status effect.",
            "You throw a strange vial!"
        )

    def use(self, user, target, battle, stats=None):
        effects = ["poison", "burn", "bleed", "wither", "stun", "freeze"]
        effect = random.choice(effects)

        stacks = random.randint(3, 6)

        if effect in ["stun"]:
            target.status_effects["stun"] = max(target.status_effects["stun"], 2)

        if effect in ["freeze"]:
            target.status_effects["freeze"] = max(target.status_effects["freeze"], 2)

        else:
            target.status_effects[effect] += stacks

        return 0, [f"{target.name} is affected by {effect}!"]

class AdrenalineShot(Item):
    def __init__(self):
        super().__init__(
            "Adrenaline Shot",
            "Adrenaline Shot",
            "Grants temporary attack boost.",
            "You inject adrenaline!"
        )

    def use(self, user, target, battle, stats=None):
        user.add_buff("attack", 10, 3)

        return 0, [f"{user.name} gains +10 attack for 3 turns!"]

