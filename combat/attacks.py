from combat.effects import *

class Attack:
    def __init__(
            self,
            name,
            effects,
            cooldown=0,
            start_cooldown=0,
            icon=None,
            description="",
            cast_time=0,
            cannot_miss=False,
            sound=None
    ):
        self.name = name
        self.effects = effects

        self.cooldown = cooldown
        self.start_cooldown = start_cooldown
        self.current_cooldown = start_cooldown

        self.icon = icon
        self.description = description

        self.cast_time = cast_time
        self.current_cast = 0

        self.cannot_miss = cannot_miss

        self.sound = sound

    def use(self, user, target):
        logs = []

        # handle cast time
        if self.cast_time > 0 and self.current_cast < self.cast_time:
            self.current_cast += 1
            logs.append(f"{user.name} is preparing {self.name}...")
            return 0, logs

        # reset cast
        self.current_cast = 0

        total_damage = 0
        logs.append(f"{user.name} used {self.name}!")

        # play sound if exists
        if self.sound:
            self.sound.play()

        for effect in self.effects:
            damage, effect_logs = effect.apply(user, target, self)

            total_damage += damage
            logs.extend(effect_logs)

            if not target.is_alive():
                logs.append(f"{target.name} was defeated!")
                break


        self.current_cooldown = self.cooldown

        return total_damage, logs

    def is_ready(self):
        return self.current_cooldown == 0

    def copy(self):
        return Attack(
            self.name,
            [effect for effect in self.effects],
            cooldown=self.cooldown,
            start_cooldown=self.start_cooldown,
            icon=self.icon,
            description=self.description,
            cast_time=self.cast_time,
            cannot_miss=self.cannot_miss,
            sound=self.sound
        )

# this is gonna be the list of attacks everything uses
from combat.effects import DamageEffect, BurnEffect, PoisonEffect

ATTACKS = {
    "strike": Attack(
        name="Strike",
        effects=[DamageEffect(10)],
        cooldown=1
    ),

    "heavy_strike": Attack(
        name="Heavy Strike",
        effects=[DamageEffect(20)],
        cooldown=2
    ),

    "fireball": Attack(
        name="Fireball",
        effects=[DamageEffect(12), BurnEffect(2)],
        cooldown=2
    ),

    "poison_stab": Attack(
        name="Poison Stab",
        effects=[DamageEffect(8), PoisonEffect(3)],
        cooldown=1
    ),
}