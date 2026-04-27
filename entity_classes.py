import pygame

class Attack:
    def __init__(self, name, effects):
        self.name = name
        self.effects = effects

    def use(self, user, target):
        for effect in self.effects:
            effect.apply(user, target)

# our base for custom effects for attacks
class Effect:
    def apply(self, user, target):
        pass

    def tick(self, target):
        pass

# classic attacks that only do damage
class DamageEffect(Effect):
    def __init__(self, amount):
        self.amount = amount

    def apply(self, user, target):
        target.take_damage(self.amount)

# special selfheal type attack
class HealEffect(Effect):
    def __init__(self, amount):
        self.amount = amount

    def apply(self, user, target):
        target.hp = min(target.max_hp, target.hp + self.amount)

# This attack gives stacks of poison (that will later do things in the status effect stage in battles)
class PoisonEffect(Effect):
    def __init__(self, stacks):
        self.stacks = stacks

    def apply(self, user, target):
        target.status_effects["poison"] = target.status_effects.get("poison", 0) + self.stacks

    def tick(self, target):
        stacks = target.status_effects.get("poison", 0)
        if stacks > 0:
            # does scaling damage based on number of stacks
            damage = int(stacks ** 1.5)
            target.take_damage(damage, ignore_defense=True)
            target.status_effects["poison"] -= 1

# The classic burn effect! this one is higher damage but gets effected by defense
class BurnEffect(Effect):
    def __init__(self, stacks):
        self.stacks = stacks

    def apply(self, user, target):
        target.status_effects["burn"] = target.status_effects.get("burn", 0) + self.stacks

    def tick(self, target):
        stacks = target.status_effects.get("burn", 0)
        if stacks > 0:
            # here is the damage calculation (fix later if issues arise)
            damage = max(1,target.max_hp * 0.1)
            target.take_damage(damage, defense_mult=0.5)
            target.status_effects["burn"] -= 1

# the annoying bleed! small damage that is a linear damage curve
class BleedEffect(Effect):
    def __init__(self, stacks):
        self.stacks = stacks

    def apply(self, user, target):
        target.status_effects["bleed"] = target.status_effects.get("bleed", 0) + self.stacks

    def tick(self, target):
        stacks = target.status_effects.get("bleed", 0)
        if stacks > 0:
            damage = int(target.max_hp * 0.05 * stacks)
            target.take_damage(damage, ignore_defense=True)
            target.status_effects["bleed"] -= 1

# generally weaker damage but also makes you weaker
class WitherEffect(Effect):
    def __init__(self, stacks):
        self.stacks = stacks

    def apply(self, user, target):
        target.status_effects["wither"] = target.status_effects.get("wither", 0) + self.stacks

        target.defense_debuff = target.defense_debuff + self.stacks if hasattr(target, "defense_debuff") else self.stacks
        target.attack_debuff = target.attack_debuff + self.stacks if hasattr(target, "attack_debuff") else self.stacks

    def tick(self, target):
        stacks = target.status_effects.get("wither", 0)
        if stacks > 0:
            target.take_damage(max(1, stacks // 2), ignore_defense=True)
            target.status_effects["wither"] -= 1

        target.defense_debuff = max(0, target.defense_debuff - 1)
        target.attack_debuff = max(0, target.attack_debuff - 1)


class StunEffect(Effect):
    def __init__(self, turns=1):
        self.turns = turns

    def apply(self, user, target):
        target.status_effects["stun"] = self.turns

class FreezeEffect(Effect):
    def __init__(self, turns=1):
        self.turns = turns

    def apply(self, user, target):
        target.status_effects["freeze"] = self.turns

# this is the base class for all entities, the stats the player and enemies have in common
class Entity:
    def __init__(self, name, hp, attack, defense, sprite=None, ):
        self.name = name

        self.max_hp = hp
        self.hp = hp

        self.attack = attack
        self.defense = defense
        self.attack_debuff = 0
        self.defense_debuff = 0

        self.status_effects = {
            "burn": 0,
            "poison": 0,
            "bleed": 0,
            "freeze": 0,
            "stun": 0,
            "wither": 0
        }
        self.buffs = {}

        self.sprite = sprite

    def take_damage(self, amount, ignore_defense=False, defense_mult=1.0):
        if ignore_defense:
            damage = amount
        else:
            damage = max(0, amount - self.get_defense() * defense_mult)

        self.hp = max(0, self.hp - damage)
        return damage

    def get_attack(self):
        return max(0, self.attack - self.attack_debuff)

    def get_defense(self):
        return max(0, self.defense - self.defense_debuff)

    def is_alive(self):
        return self.hp > 0

    # This goes through each effect and removes one stack when called
    def process_status(self):
        if self.status_effects.get("stun", 0) > 0:
            self.status_effects["stun"] -= 1
            return "stunned"

        if self.status_effects.get("freeze", 0) > 0:
            self.status_effects["freeze"] -= 1
            return "frozen"

        if self.status_effects["poison"] > 0:
            stacks = self.status_effects["poison"]
            self.take_damage(stacks * stacks)
            self.status_effects["poison"] -= 1

        if self.status_effects["burn"] > 0:
            stacks = self.status_effects["burn"]
            self.take_damage(max(2, stacks - self.defense))
            self.status_effects["burn"] -= 1

        if self.status_effects["bleed"] > 0:
            stacks = self.status_effects["bleed"]
            self.take_damage(int(self.max_hp * 0.05 * stacks))
            self.status_effects["bleed"] -= 1

        if self.status_effects["wither"] > 0:
            stacks = self.status_effects["wither"]
            self.take_damage(max(1, stacks // 2))
            self.status_effects["wither"] -= 1

# this is out player base, which is then turned into the active player based on input (CharacterSelect)
class Player(Entity):
    def __init__(self, name, hp, attack, defense, sprite=None):
        super().__init__(name, hp, attack, defense, sprite)

        self.inventory = []

# our enemy base which gets used for the active enemy
class Enemy(Entity):
    def __init__(self, name, hp, attack, defense, sprite=None):
        super().__init__(name, hp, attack, defense, sprite)