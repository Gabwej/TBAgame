import random

class Buff:
    def __init__(self, stat, amount, turns):
        self.stat = stat
        self.amount = amount
        self.turns = turns

    def tick(self):
        self.turns -= 1
        return self.turns <= 0

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

        self.pending_action = None
        self.cast_timer = 0

        self.resistances = {
            "physical": 1.0,
            "burn": 1.0,
            "poison": 1.0,
            "bleed": 1.0,
        }

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

    def is_alive(self):
        return self.hp > 0

    def reduce_cooldowns(self):
        if hasattr(self, "attacks"):
            for attack in self.attacks:
                if attack.current_cooldown > 0:
                    attack.current_cooldown -= 1

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
                    can_crit=False, attacker=None, stats=None, cannot_miss=False, damage_type="physical"):

        logs = []

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

        mult = self.resistances.get(damage_type, 1.0)
        damage = int(damage * mult)

        self.hp = max(0, self.hp - damage)

        # updates total damage
        if hasattr(attacker, "stats") and attacker:
            attacker.stats["total_damage"] += damage

        logs.append(f"{self.name} takes {damage} damage!")

        return damage, logs

    # This goes through each effect and removes one stack when called
    def process_status(self):
        logs = []
        disabled = None

        if self.status_effects.get("stun", 0) > 0:
            self.status_effects["stun"] -= 1
            logs.append(f"{self.name} is stunned!")
            disabled = True

        if self.status_effects.get("freeze", 0) > 0:
            self.status_effects["freeze"] -= 1

            damage, _ = self.take_damage(2, ignore_defense=True)
            logs.append(f"{self.name} is frozen and takes {damage} damage!")
            disabled = True

            if not self.is_alive():
                return logs, disabled

        if self.status_effects.get("poison", 0) > 0:
            stacks = self.status_effects["poison"]

            damage, _ = self.take_damage(int(stacks ** 1.5), ignore_defense=True, damage_type="poison")
            logs.append(f"{self.name} takes {damage} poison damage!")

            self.status_effects["poison"] -= 1

            if not self.is_alive():
                return logs, disabled

        if self.status_effects.get("burn", 0) > 0:
            stacks = self.status_effects["burn"]

            damage, _ = self.take_damage(
                max(1, int(self.max_hp * 0.1)),
                defense_mult=0.5,
                damage_type="burn"
            )
            logs.append(f"{self.name} takes {damage} burn damage!")

            self.status_effects["burn"] -= 1

            if not self.is_alive():
                return logs, disabled

        if self.status_effects.get("bleed", 0) > 0:
            stacks = self.status_effects["bleed"]

            damage, _ = self.take_damage(
                int(self.max_hp * 0.05 * stacks),
                ignore_defense=True,
                damage_type="bleed"
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
