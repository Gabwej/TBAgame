from entity_classes import Entity


class Battle:
    def __init__(self, player, enemy):
        self.player = player
        self.enemy = enemy

        self.state = "player_start"

        self.log = []
        self.waiting = False

        self.escape_unlocked = False

    def use_item(self, item_id):
        if self.state != "player_action" or self.waiting:
            return

        entry = self.player.get_item(item_id)

        if not entry:
            return

        item = entry["item"]

        damage, logs = item.use(self.player, self.enemy, self, self.stats)

        self.stats.total_damage += damage
        self.log.extend(logs)

        self.player.remove_item(item_id, 1)

        self.waiting = True
        self.state = "enemy_start"

    def add_log(self, text):
        self.log.append(text)

    def get_current_log(self):
        if self.log:
            return self.log[0]
        return ""

    def next_log(self):
        if self.log:
            self.log.pop(0)

        if not self.log:
            self.waiting = False

    def update(self):
        if self.waiting:
            return

        if self.state == "player_start":
            self.player_start()

        elif self.state == "player_action":
            pass

        elif self.state == "enemy_start":
            self.enemy_start()

        elif self.state == "enemy_action":
            self.enemy_action()

        elif self.state == "cleanup":
            self.cleanup()

    def start_battle(self):
        self.add_log(f"{self.enemy.name} appeared!")
        self.add_log(self.enemy.description)
        self.add_log("what will you do?")
        self.waiting = True
        self.state = "player_start"

    def player_start(self):
        logs, disabled = self.player.process_status()
        self.player.reduce_cooldowns()

        for log in logs:
            self.add_log(log)

        if logs:
            self.waiting = True
            return

        if not self.player.is_alive():
            self.state = "cleanup"
            return

        if disabled:
            self.state = "enemy_start"
            return

        self.state = "player_action"

    def player_attack(self, attack):
        if self.state != "player_action" or self.waiting:
            return

        if not self.player.is_alive():
            self.state = "cleanup"
            self.waiting = True
            return

        damage, logs = attack.use(self.player, self.enemy)

        for log in logs:
            self.add_log(log)

        if not self.enemy.is_alive():
            self.state = "cleanup"
            self.waiting = True
            return

        self.waiting = True
        self.state = "enemy_start"

    def enemy_start(self):
        if not self.enemy.is_alive():
            self.state = "cleanup"
            return

        logs, disabled = self.enemy.process_status()

        self.enemy.reduce_cooldowns()

        for log in logs:
            self.add_log(log)

        if logs:
            self.waiting = True
            return

        if not self.enemy.is_alive():
            self.state = "cleanup"
            return

        if disabled:
            self.state = "player_start"
            return

        self.state = "enemy_action"

    def enemy_action(self):
        if not self.enemy.is_alive():
            self.state = "cleanup"
            return

        # this is gonna be weighted or AI later
        attack = self.enemy.attacks[0]

        damage, logs = attack.use(self.enemy, self.player)

        for log in logs:
            self.add_log(log)

        self.waiting = True

        if not self.player.is_alive():
            self.state = "cleanup"
            return

        self.state = "player_start"

    def cleanup(self):
        if not self.enemy.is_alive() and self.player.is_alive():
            self.player.stats["battles_won"] += 1

        if not self.player.is_alive():
            self.add_log("Player died!")
            self.waiting = True
            self.state = "end"
            return

        if not self.enemy.is_alive():
            self.stats.battles_won += 1
            self.add_log(f"{self.enemy.name} has fallen!")
            self.waiting = True

            gold = get_enemy_gold(self.enemy)
            self.player.currency.add(gold)

            self.add_log(f"You gained {gold} gold!")

            healed = self.player.post_battle_heal()
            self.add_log(f"You recovered {healed} HP after the fight!")

            self.player.post_battle_cleanup()

            self.state = "end"
            return
