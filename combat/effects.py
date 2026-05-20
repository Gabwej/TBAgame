from assets.images import Assets


# our base for custom effects for attacks
class Effect:
    def __init__(self, icon=None):
        self.icon = icon

    def apply(self, user, target, attack):
        pass

    def tick(self, target):
        pass


# classic attacks that only do damage
class DamageEffect(Effect):
    def __init__(self, amount, scaling=1.0, icon=None):
        super().__init__(icon)

        self.amount = amount
        self.scaling = scaling

    def apply(self, user, target, attack):

        scaled_damage = self.amount + int(user.get_attack() * self.scaling)

        damage, logs = target.take_damage(
            scaled_damage,
            attacker=user,
            can_crit=True,
            cannot_miss=attack.cannot_miss
        )

        return damage, logs


# special selfheal type attack
class HealEffect(Effect):
    def __init__(self, amount, icon_id=(21, 1)):
        super().__init__(icon_id)
        self.amount = amount

    def apply(self, user, target, attack):
        healed = min(self.amount, user.max_hp - user.hp)

        user.hp = min(user.max_hp, user.hp + healed)

        if hasattr(user, "stats"):
            user.stats["total_healing"] += healed

        return 0, [f"{user.name} heals {healed} HP!"]


# This attack gives stacks of poison (that will later do things in the status effect stage in battles)
class PoisonEffect(Effect):
    def __init__(self, amount, icon_id=(22, 8)):
        super().__init__(icon_id)
        self.amount = amount

    def apply(self, user, target, attack):
        target.status_effects["poison"] = target.status_effects.get("poison", 0) + self.amount
        return 0, [f"{target.name} is poisoned!"]

    def tick(self, target):
        stacks = target.status_effects.get("poison", 0)
        if stacks > 0:
            # does scaling damage based on number of stacks
            damage = int(stacks ** 1.5)
            target.take_damage(damage, ignore_defense=True, cannot_miss=True, damage_type="poison")
            target.status_effects["poison"] -= 1


# The classic burn effect! this one is higher damage but gets effected by defense
class BurnEffect(Effect):
    def __init__(self, amount, icon_id=(0, 0)):
        super().__init__(icon_id)
        self.amount = amount

    def apply(self, user, target, attack):
        target.status_effects["burn"] = target.status_effects.get("burn", 0) + self.amount
        return 0, [f"{target.name} is burning!"]

    def tick(self, target):
        stacks = target.status_effects.get("burn", 0)
        if stacks > 0:
            # here is the damage calculation (fix later if issues arise)
            damage = max(1, target.max_hp * 0.1)
            target.take_damage(damage, defense_mult=0.5, cannot_miss=True, damage_type="burn")
            target.status_effects["burn"] -= 1


# the annoying bleed! small damage that is a linear damage curve
class BleedEffect(Effect):
    def __init__(self, amount, icon_id=(13,4)):
        super().__init__(icon_id)
        self.amount = amount

    def apply(self, user, target, attack):
        target.status_effects["bleed"] = target.status_effects.get("bleed", 0) + self.amount
        return 0, [f"{target.name} starts bleeding!"]

    def tick(self, target):
        stacks = target.status_effects.get("bleed", 0)
        if stacks > 0:
            damage = int(target.max_hp * 0.05 * stacks)
            target.take_damage(damage, ignore_defense=True, cannot_miss=True, damage_type="bleed")
            target.status_effects["bleed"] -= 1


# generally weaker damage but also makes you weaker
class WitherEffect(Effect):
    def __init__(self, amount, icon_id=(16, 6)):
        super().__init__(icon_id)
        self.amount = amount

    def apply(self, user, target, attack):
        target.status_effects["wither"] = target.status_effects.get("wither", 0) + self.amount

        target.defense_debuff += self.amount
        target.attack_debuff += self.amount

        return 0, [f"{target.name} is withering!"]

    def tick(self, target):
        stacks = target.status_effects.get("wither", 0)
        if stacks > 0:
            target.take_damage(max(1, stacks // 2), ignore_defense=True, cannot_miss=True)
            target.status_effects["wither"] -= 1

        target.defense_debuff = max(0, target.defense_debuff - 1)
        target.attack_debuff = max(0, target.attack_debuff - 1)

class BuffEffect(Effect):
    def __init__(self, stat, amount, turns, icon_id=None):
        super().__init__(icon_id)
        self.stat = stat
        self.amount = amount
        self.turns = turns

    def apply(self, user, target, attack):
        user.add_buff(self.stat, self.amount, self.turns)
        return 0, [f"{user.name} gains +{self.amount} {self.stat} for {self.turns} turns!"]

# the stun effects

class StunEffect(Effect):
    def __init__(self, amount, icon_id=(23, 9)):
        super().__init__(icon_id)
        self.amount = amount

    def apply(self, user, target, attack):
        target.status_effects["stun"] = self.amount
        return 0, [f"{target.name} is stunned!"]


class FreezeEffect(Effect):
    def __init__(self, amount, icon_id=(4, 15)):
        super().__init__(icon_id)
        self.amount = amount

    def apply(self, user, target, attack):
        target.status_effects["freeze"] = self.amount
        return 0, [f"{target.name} is frozen!"]


class LifeStealEffect(Effect):
    def __init__(self, percent, icon_id=None):
        super().__init__(icon_id)
        self.percent = percent

    def apply(self, user, target, attack):
        # lifesteal depends on previous damage dealt in SAME attack
        # so we store it temporarily on the attack

        if not hasattr(attack, "damage_dealt"):
            return 0, []

        heal = int(attack.damage_dealt * self.percent)

        user.hp = min(user.max_hp, user.hp + heal)

        if hasattr(user, "stats"):
            user.stats["total_healing"] += heal

        return 0, [f"{user.name} steals {heal} HP!"]

class ConditionalEffect(Effect):
    def __init__(self, condition, effect, fail_text=None):
        super().__init__(effect.icon)
        self.condition = condition  # function(user, target) -> bool
        self.effect = effect
        self.fail_text = fail_text

    def apply(self, user, target, attack):
        if self.condition(user, target):
            return self.effect.apply(user, target, attack)

        if self.fail_text:
            return 0, [self.fail_text]

        return 0, []

    def target_has_status(status):
        return lambda user, target: target.status_effects.get(status, 0) > 0

    def user_hp_below(percent):
        return lambda user, target: user.hp / user.max_hp <= percent

    def target_hp_below(percent):
        return lambda user, target: target.hp / target.max_hp <= percent

    def always():
        return lambda user, target: True