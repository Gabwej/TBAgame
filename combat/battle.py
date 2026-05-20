import random

from entities import player
from ui.ending import EndScreen


class Battle:
    def __init__(self, player, enemy):
        self.player = player
        self.enemy = enemy

        self.turn = "player"

        self.logs = [
        ]
        self.current_log_index = 0

        self.waiting_for_continue = False

        self.battle_over = False
        self.result = None
        self.pending_end = None
        self.background = None
        self.pending_action_execution = None


    # creates all the logs, aka dialog in the fight (makes smoother ui)
    def add_logs(self, new_logs):
        if isinstance(new_logs, str):
            self.logs.append(new_logs)
        else:
            for log in new_logs:
                if isinstance(log, str):
                    self.logs.append(log)

    def get_current_log(self):
        if not self.logs:
            return ""

        if self.current_log_index < len(self.logs):
            return self.logs[self.current_log_index]

        return ""

    def next_log(self):
        if not self.logs:
            self.waiting_for_continue = False
            return ""

        if self.current_log_index < len(self.logs) - 1:
            self.current_log_index += 1
            return self.get_current_log()

        self.logs = []
        self.current_log_index = 0
        self.waiting_for_continue = False

        if self.pending_end in ("win", "lose"):
            self.battle_over = True
            self.result = self.pending_end
            self.pending_end = None
            return

        if self.pending_end == "run":
            self.battle_over = True
            self.result = "run"
            self.pending_end = None
            return

        # execute delayed action after logs finish
        if self.pending_action_execution:
            action = self.pending_action_execution
            self.pending_action_execution = None

            action()

            return ""

        if not self.battle_over:
            self.advance_turn()

        return ""

    def can_player_act(self):
        return (
                self.turn == "player"
                and not self.waiting_for_continue
                and not self.battle_over
        )

    def use_attack(self, index):
        if self.turn != "player":
            return

        if self.waiting_for_continue:
            return

        if index < 0 or index >= len(self.player.attacks):
            return

        attack = self.player.attacks[index]
        self.player_attack(attack)

    def waiting(self):
        return self.waiting_for_continue or len(self.logs) > 0

    def tick_cooldowns(self):
        for atk in self.player.attacks:
            if atk.current_cooldown > 0:
                atk.current_cooldown -= 1

    def process_cast(self, entity):
        if entity.pending_action is None:
            return False

        # still casting
        if entity.cast_timer > 0:
            entity.cast_timer -= 1

            if entity.cast_timer > 0:
                self.logs.append(
                    f"{entity.name} continues casting {entity.pending_action.name}..."
                )

                self.waiting_for_continue = True
                return True

        attack = entity.pending_action

        entity.pending_action = None
        entity.cast_timer = 0

        target = self.enemy if entity == self.player else self.player

        damage, logs = attack.use(entity, target)

        self.add_logs(logs)

        self.waiting_for_continue = True

        self.check_battle_end()

        return True

    # checks who has the turn
    def start_turn(self, entity):
        logs, disabled = entity.process_status()

        if logs:
            self.add_logs(logs)
            self.waiting_for_continue = True

        return disabled

    def advance_turn(self):
        if self.battle_over:
            return

        # swap turn first
        if self.turn == "player":
            self.turn = "enemy"
            entity = self.enemy

        else:
            self.turn = "player"
            entity = self.player

            self.tick_cooldowns()

        # CASTING HAS PRIORITY
        if self.process_cast(entity):
            return

        # normal status processing
        logs, disabled = entity.process_status()

        if logs:
            self.add_logs(logs)
            self.waiting_for_continue = True

        if disabled:
            self.waiting_for_continue = True
            return

        # if player has no usable attacks
        if entity == self.player:

            available_attacks = [
                atk for atk in self.player.attacks
                if atk.is_ready()
            ]

            if not available_attacks:
                self.logs.append(
                    f"{self.player.name} has no available attacks!"
                )

                self.waiting_for_continue = True

                return

        # enemy acts automatically
        if entity == self.enemy:
            self.enemy_turn()


    # the player action
    def player_attack(self, attack):
        if self.turn != "player":
            return

        if self.waiting_for_continue:
            return

        if not attack.is_ready():
            return

        # START CASTING
        if attack.cast_time > 0:
            self.player.pending_action = attack
            self.player.cast_timer = attack.cast_time
            self.player.cast_timer -= 1

            self.logs.append(
                f"{self.player.name} starts casting {attack.name}!"
            )

            self.player.reduce_cooldowns()

            self.waiting_for_continue = True
            return

        # NORMAL ATTACK

        self.logs.append(
            f"{self.player.name} uses {attack.name}!"
        )

        def execute():

            damage, logs = attack.use(self.player, self.enemy)

            self.add_logs(logs)

            self.waiting_for_continue = True

            self.check_battle_end()

        self.pending_action_execution = execute

        self.waiting_for_continue = True

    # This is the enemies turn

    def run_battle(self):

        if self.waiting_for_continue:
            return

        self.logs.append(
            f"{self.player.name} Fled the battle!"
        )

        self.waiting_for_continue = True
        self.player.reset_after_battle()
        self.pending_end = "run"

    def use_item(self, item_id):
        if self.turn != "player" or self.waiting_for_continue:
            return

        if item_id not in self.player.inventory:
            return

        entry = self.player.inventory[item_id]
        item = entry["item"]

        # 1. use text always first
        self.add_logs([item.use_text])

        # 2. execute item effect properly
        result = item.use(self.player, self.enemy, self)

        # 3. FIX: unpack correctly
        if isinstance(result, tuple):
            damage, logs = result
        else:
            logs = []

        # 4. add effect logs
        if logs:
            self.add_logs(logs)

        # 5. remove item
        self.player.remove_item(item_id, 1)

        self.waiting_for_continue = True

    def enemy_turn(self):
        if self.battle_over:
            return

        # checks if attacks are usable
        available_attacks = [
            attack for attack in self.enemy.attacks
            if attack.is_ready()
        ]

        # safety measure, in case enemy runs out of attacks
        if not available_attacks:
            self.logs.append(f"{self.enemy.name} cannot act!")
            self.waiting_for_continue = True
            return

        # random attack from available
        attack = random.choice(available_attacks)

        if attack.cast_time > 0:
            self.enemy.pending_action = attack
            self.enemy.cast_timer = attack.cast_time + 1

            self.logs.append(
                f"{self.enemy.name} starts casting {attack.name}!"
            )

            self.enemy.reduce_cooldowns()

            self.waiting_for_continue = True
            return

        damage, logs = attack.use(self.enemy, self.player)

        self.add_logs(logs)

        self.waiting_for_continue = True

        self.check_battle_end()


    # End battle phase

    def check_battle_end(self):

        if not self.player.is_alive():
            self.logs.append(f"{self.player.name} was defeated!")
            self.waiting_for_continue = True
            self.pending_end = "lose"
            return

        elif not self.enemy.is_alive():
            self.logs.append(f"{self.enemy.name} was defeated!")
            self.player.stats["battles_won"] += 1
            self.waiting_for_continue = True
            self.player.reset_after_battle()
            self.pending_end = "win"
            return
