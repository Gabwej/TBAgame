import random

class Attack:
    def __init__(self, name, effects):
        self.name = name
        self.effects = effects

    def use(self, user, target):
        total_damage = 0
        logs = []

        logs.append(f"{user.name} used {self.name}!")

        for effect in self.effects:
            damage, effect_logs = effect.apply(user, target, stats)

            total_damage += damage
            logs.extend(effect_logs)

            if not target.is_alive():
                logs.append(f"{target.name} was defeated!")
                break

        return total_damage, logs

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
        damage, logs = target.take_damage(
            self.amount,
            attacker=user,
            can_crit=True
        )

        return damage, logs

# special selfheal type attack
class HealEffect(Effect):
    def __init__(self, amount):
        self.amount = amount

    def apply(self, user, target):
        healed = min(self.amount, target.max_hp - target.hp)
        target.hp += healed

        if stats:
            stats,total_healing += healed

        return 0, [f"{target.name} heals {healed} HP!"]

# This attack gives stacks of poison (that will later do things in the status effect stage in battles)
class PoisonEffect(Effect):
    def __init__(self, stacks):
        self.stacks = stacks

    def apply(self, user, target):
        target.status_effects["poison"] = target.status_effects.get("poison", 0) + self.stacks
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
    def __init__(self, stacks):
        self.stacks = stacks

    def apply(self, user, target):
        target.status_effects["burn"] = target.status_effects.get("burn", 0) + self.stacks
        return 0, [f"{target.name} is burning!"]

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
        return 0, [f"{target.name} starts bleeding!"]

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

        target.defense_debuff += self.stacks
        target.attack_debuff += self.stacks

        return 0, [f"{target.name} is withering!"]

    def tick(self, target):
        stacks = target.status_effects.get("wither", 0)
        if stacks > 0:
            target.take_damage(max(1, stacks // 2), ignore_defense=True)
            target.status_effects["wither"] -= 1

        target.defense_debuff = max(0, target.defense_debuff - 1)
        target.attack_debuff = max(0, target.attack_debuff - 1)

# the stun effets

class StunEffect(Effect):
    def __init__(self, turns=1):
        self.turns = turns

    def apply(self, user, target):
        target.status_effects["stun"] = self.turns
        return 0, [f"{target.name} is stunned!"]

class FreezeEffect(Effect):
    def __init__(self, turns=1):
        self.turns = turns

    def apply(self, user, target):
        target.status_effects["freeze"] = self.turns
        return 0, [f"{target.name} is frozen!"]

# the buff effect

class BuffEffect(Effect):
    def __init__(self, stat, amount, turns):
        self.stat = stat
        self.amount = amount
        self.turns = turns

    def apply(self, user, target):
        user.add_buff(self.stat, self.amount, self.turns)
        return 0, [f"{user.name} gains +{self.amount} {self.stat} for {self.turns} turns!"]

# this is the base class for all entities, the stats the player and enemies have in common
class Entity:
    def __init__(self, name, hp, attack, defense, sprite=None,
                 crit_chance=0.1, crit_multiplier=1.5, dodge_chance=0.05):
        self.name = name

        self.max_hp = hp
        self.hp = hp

        self.attack = attack
        self.defense = defense
        self.attack_debuff = 0
        self.defense_debuff = 0

        self.crit_chance = crit_chance
        self.crit_multiplier = crit_multiplier
        self.dodge_chance = dodge_chance

        self.status_effects = {
            "burn": 0,
            "poison": 0,
            "bleed": 0,
            "freeze": 0,
            "stun": 0,
            "wither": 0
        }
        self.buffs = []

        self.sprite = sprite

    def post_battle_cleanup(self):
        self.buffs = []
        self.attack_debuff = 0
        self.defense_debuff = 0

        for effect in self.status_effects:
            self.status_effects[effect] = max(0, self.status_effects[effect] - 5)

    def post_battle_heal(self):
        heal_amount = int(self.max_hp * 0.05)
        self.hp = min(self.max_hp, self.hp + heal_amount)
        return heal_amount

    def add_buff(self, stat, amount, turns):
        self.buffs.append(Buff(stat, amount, turns))

    def get_attack(self):
        bonus = sum(b.amount for b in self.buffs if b.stat == "attack")
        return max(0, self.attack - self.attack_debuff + bonus)

    def get_defense(self):
        bonus = sum(b.amount for b in self.buffs if b.stat == "defense")
        return max(0, self.defense - self.defense_debuff + bonus)

    def take_damage(self, amount, ignore_defense=False, defense_mult=1.0,
                    can_crit=False, attacker=None, stats=None):

        logs = []

        # checks if you dodged
        if attacker and random.random() < self.dodge_chance:
            logs.append(f"{self.name} dodged the attack!")
            return 0, logs

        # checks defense
        if ignore_defense:
            damage = amount
        else:
            damage = max(0, amount - self.get_defense() * defense_mult)

        # checks if hit is a crit
        if can_crit and attacker:
            if random.random() < attacker.crit_chance:
                damage = int(damage * attacker.crit_multiplier)
                logs.append("Critical hit!")

        self.hp = max(0, self.hp - damage)

        # updates total damage
        if stats:
            stats.toal_damage += damage

        logs.append(f"{self.name} takes {damage} damage!")

        return damage, logs

    # This goes through each effect and removes one stack when called
    def process_status(self):
        logs = []
        disabled = None


        if self.status_effects.get("stun", 0) > 0:
            self.status_effects["stun"] -= 1
            logs.append(f"{self.name} is stunned!")
            disabled = "stunned"


        if self.status_effects.get("freeze", 0) > 0:
            self.status_effects["freeze"] -= 1

            damage, _ = self.take_damage(2, ignore_defense=True)
            logs.append(f"{self.name} is frozen and takes {damage} damage!")
            disabled = "frozen"

            if not self.is_alive():
                return logs, disabled


        if self.status_effects.get("poison", 0) > 0:
            stacks = self.status_effects["poison"]

            damage, _ = self.take_damage(int(stacks ** 1.5), ignore_defense=True)
            logs.append(f"{self.name} takes {damage} poison damage!")

            self.status_effects["poison"] -= 1

            if not self.is_alive():
                return logs, disabled


        if self.status_effects.get("burn", 0) > 0:
            stacks = self.status_effects["burn"]

            damage, _ = self.take_damage(
                max(1, int(self.max_hp * 0.1)),
                defense_mult=0.5
            )
            logs.append(f"{self.name} takes {damage} burn damage!")

            self.status_effects["burn"] -= 1

            if not self.is_alive():
                return logs, disabled


        if self.status_effects.get("bleed", 0) > 0:
            stacks = self.status_effects["bleed"]

            damage, _ = self.take_damage(
                int(self.max_hp * 0.05 * stacks),
                ignore_defense=True
            )
            logs.append(f"{self.name} bleeds for {damage} damage!")

            self.status_effects["bleed"] -= 1

            if not self.is_alive():
                return logs, disabled


        if self.status_effects.get("wither", 0) > 0:
            stacks = self.status_effects["wither"]

            damage, _ = self.take_damage(
                max(1, stacks // 2),
                ignore_defense=True
            )
            logs.append(f"{self.name} takes {damage} wither damage!")

            self.status_effects["wither"] -= 1

            # decay debuffs
            self.attack_debuff = max(0, self.attack_debuff - 1)
            self.defense_debuff = max(0, self.defense_debuff - 1)

            if not self.is_alive():
                return logs, disabled

        expired = []

        for buff in self.buffs:
            if buff.tick():
                expired.append(buff)

        for buff in expired:
            self.buffs.remove(buff)
            logs.append(f"{self.name}'s buffs wear off.")

        return logs, disabled



# this is out player base, which is then turned into the active player based on input (CharacterSelect)
class Player(Entity):
    def __init__(self, name, hp, attack, defense, sprite=None):
        super().__init__(name, hp, attack, defense, sprite)

        self.inventory = {}

    def add_item(self, item, count=1):
        if item.item_id in self.inventory:
            self.inventory[item.item_id]["count"] += count
        else:
            self.inventory[item.item_id] = {
                "item": item,
                "count": count
            }

    def remove_item(self, item_id, count=1):
        if item_id in self.inventory:
            self.inventory[item_id]["count"] -= count

            if self.inventory[item_id]["count"] <= 0:
                del self.inventory[item_id]

    def get_item(self, item_id):
        return self.inventory.get(item_id, None)


# our enemy base which gets used for the active enemy
class Enemy(Entity):
    def __init__(self, name, hp, attack, defense, sprite=None):
        super().__init__(name, hp, attack, defense, sprite)


class Buff:
    def __init__(self, stat, amount, turns):
        self.stat = stat          # "attack" or "defense"
        self.amount = amount
        self.turns = turns

    def tick(self):
        self.turns -= 1
        return self.turns <= 0