import random
import pygame

class Item:
    def __init__(self, item_id, name, description, use_text):
        self.item_id = item_id.lower()
        self.name = name
        self.description = description
        self.use_text = use_text

    def use(self, user, target, battle, stats=None):
        return 0, []


class Potion(Item):
    def __init__(self):
        super().__init__(
            "potion",
            "Potion",
            "Heals a moderate amount of HP.\n\n(50-75 hp)",
            "You drink a potion."
        )

    def use(self, user, target=None, battle=None, stats=None):

        heal = 50 + random.randint(0, 25)

        user.hp = min(user.max_hp, user.hp + heal)

        if stats:
            stats.total_healing += heal

        return 0, [f"{user.name} heals {heal} HP!"]


class Cleanse(Item):
    def __init__(self):
        super().__init__(
            "cleanse",
            "Cleanse",
            "Removes all negative effects and debuffs.",
            "A purifying aura surrounds you."
        )

    def use(self, user, target=None, battle=None, stats=None):

        if not hasattr(user, "status_effects"):
            return 0, [f"{user.name} has nothing to cleanse."]

        for key in user.status_effects:
            user.status_effects[key] = 0

        user.attack_debuff = 0
        user.defense_debuff = 0

        return 0, [f"{user.name} is cleansed of all effects!"]


class EscapeRope(Item):
    def __init__(self):
        super().__init__(
            "escape_rope",
            "Escape",
            "Allows you to flee from battle.\nShould only be used when you cant escape normally!",
            "Joestar Secret Technique initialized."
        )

    def use(self, user, target=None, battle=None, stats=None):
        if battle:
            battle.pending_end = "run"
            battle.waiting_for_continue = True

        return 0, ["You run for your life!"]


class Bomb(Item):
    def __init__(self):
        super().__init__(
            "bomb",
            "Bomb",
            "Deals damage and applies burn.\n\n(50 dmg, 2 burn)",
            "You throw a bomb!"
        )

    def use(self, user, target, battle=None, stats=None):
        damage = 50
        if target:
            target.take_damage(damage)

            if hasattr(target, "status_effects"):
                target.status_effects["burn"] = (
                    target.status_effects.get("burn", 0) + 3
                )

        return damage, [
            f"{target.name} takes {damage} damage!",
            f"{target.name} is burning!"
        ]


class MysteryVial(Item):
    def __init__(self):
        super().__init__(
            "mystery_vial",
            "Vial",
            "A concoction of strange liquids, best to not drink it.\n('Random effect' 2-5)",
            "You throw the strange vial!"
        )

    def use(self, user, target, battle=None, stats=None):

        effects = ["poison", "burn", "bleed", "wither", "stun", "freeze"]
        effect = random.choice(effects)

        stacks = random.randint(2, 5)

        if not hasattr(target, "status_effects"):
            return 0, [f"{target.name} is unaffected."]

        if effect == "stun":
            target.status_effects["stun"] = max(
                target.status_effects.get("stun", 0), 2
            )

        elif effect == "freeze":
            target.status_effects["freeze"] = max(
                target.status_effects.get("freeze", 0), 2
            )

        else:
            target.status_effects[effect] = (
                target.status_effects.get(effect, 0) + stacks
            )

        return 0, [f"{target.name} is affected by {effect}!"]


class AdrenalineShot(Item):
    def __init__(self):
        super().__init__(
            "adrenaline_shot",
            "Thrill",
            "Grants a temporary buff to attack and defense \n(10 atk:4, 10 def:4)",
            "You inject adrenaline!"
        )

    def use(self, user, target=None, battle=None, stats=None):

        if hasattr(user, "add_buff"):
            user.add_buff("attack", 10, 4)
            user.add_buff("defense", 10, 4)

            return 0, [f"{user.name} gains +10 attack and defense for 4 turns!"]

        return 0, [f"{user.name} feels nothing happen."]
