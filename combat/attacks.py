from combat.effects import *

class Attack:
    def __init__(self, name, effects, cooldown=0, start_cooldown=0, icon = None):
        self.name = name
        self.effects = effects

        self.cooldown = cooldown
        self.start_cooldown = start_cooldown
        self.current_cooldown = 0
        self.icon = icon

    def use(self, user, target):
        total_damage = 0
        logs = []

        logs.append(f"{user.name} used {self.name}!")

        for effect in self.effects:
            damage, effect_logs = effect.apply(user, target)

            total_damage += damage
            logs.extend(effect_logs)

            if not target.is_alive():
                logs.append(f"{target.name} was defeated!")
                break

        if hasattr(user, "stats"):
            user.stats["total_damage"] += total_damage

        self.current_cooldown = self.cooldown

        return total_damage, logs

    def is_ready(self):
        return self.current_cooldown == 0