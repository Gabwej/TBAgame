
# our base for custom effects for attacks
class Effect:
    def __init__(self, icon=None):
        self.icon = icon

    def apply(self, user, target):
        pass

    def tick(self, target):
        pass


# classic attacks that only do damage
class DamageEffect(Effect):
    def __init__(self, amount, icon=None):
        super().__init__(icon)
        self.amount = amount

    def apply(self, user, target):
        damage, logs = target.take_damage(
            self.amount,
            attacker=user,
            can_crit=True
        )

        return damage, logs


# special selfheal type attack
class HealEffect(Effect):
    def __init__(self, amount, icon=None):
        super().__init__(icon)
        self.amount = amount

    def apply(self, user, target):
        healed = min(self.amount, target.max_hp - target.hp)
        target.hp += healed

        if hasattr(user, "stats"):
            user.stats["total_healing"] += healed

        return 0, [f"{target.name} heals {healed} HP!"]


# This attack gives stacks of poison (that will later do things in the status effect stage in battles)
class PoisonEffect(Effect):
    def __init__(self, amount, icon=None):
        super().__init__(icon)
        self.amount = amount

    def apply(self, user, target):
        target.status_effects["poison"] = target.status_effects.get("poison", 0) + self.amount
        return 0, [f"{target.name} is poisoned!"]

    def tick(self, target):
        stacks = target.status_effects.get("poison", 0)
        if stacks > 0:
            # does scaling damage based on number of stacks
            damage = int(stacks ** 1.5)
            target.take_damage(damage, ignore_defense=True)
            target.status_effects["poison"] -= 1


# The classic burn effect! this one is higher damage but gets effected by defense
class BurnEffect(Effect):
    def __init__(self, amount, icon=None):
        super().__init__(icon)
        self.amount = amount

    def apply(self, user, target):
        target.status_effects["burn"] = target.status_effects.get("burn", 0) + self.amount
        return 0, [f"{target.name} is burning!"]

    def tick(self, target):
        stacks = target.status_effects.get("burn", 0)
        if stacks > 0:
            # here is the damage calculation (fix later if issues arise)
            damage = max(1, target.max_hp * 0.1)
            target.take_damage(damage, defense_mult=0.5)
            target.status_effects["burn"] -= 1


# the annoying bleed! small damage that is a linear damage curve
class BleedEffect(Effect):
    def __init__(self, amount, icon=None):
        super().__init__(icon)
        self.amount = amount

    def apply(self, user, target):
        target.status_effects["bleed"] = target.status_effects.get("bleed", 0) + self.amount
        return 0, [f"{target.name} starts bleeding!"]

    def tick(self, target):
        stacks = target.status_effects.get("bleed", 0)
        if stacks > 0:
            damage = int(target.max_hp * 0.05 * stacks)
            target.take_damage(damage, ignore_defense=True)
            target.status_effects["bleed"] -= 1


# generally weaker damage but also makes you weaker
class WitherEffect(Effect):
    def __init__(self, amount, icon=None):
        super().__init__(icon)
        self.amount = amount

    def apply(self, user, target):
        target.status_effects["wither"] = target.status_effects.get("wither", 0) + self.amount

        target.defense_debuff += self.amount
        target.attack_debuff += self.amount

        return 0, [f"{target.name} is withering!"]

    def tick(self, target):
        stacks = target.status_effects.get("wither", 0)
        if stacks > 0:
            target.take_damage(max(1, stacks // 2), ignore_defense=True)
            target.status_effects["wither"] -= 1

        target.defense_debuff = max(0, target.defense_debuff - 1)
        target.attack_debuff = max(0, target.attack_debuff - 1)


# the stun effects

class StunEffect(Effect):
    def __init__(self, amount, icon=None):
        super().__init__(icon)
        self.amount = amount

    def apply(self, user, target):
        target.status_effects["stun"] = self.amount
        return 0, [f"{target.name} is stunned!"]


class FreezeEffect(Effect):
    def __init__(self, turns=1):
        self.turns = turns

    def apply(self, user, target):
        target.status_effects["freeze"] = self.turns
        return 0, [f"{target.name} is frozen!"]


# the buff effect

class BuffEffect(Effect):
    def __init__(self, stat, amount, turns, icon=None):
        super().__init__(icon)
        self.amount = amount
        self.stat = stat
        self.turns = turns

    def apply(self, user, target):
        user.add_buff(self.stat, self.amount, self.turns)
        return 0, [f"{user.name} gains +{self.amount} {self.stat} for {self.turns} turns!"]

