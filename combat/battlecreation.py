from combat.attacks import ATTACKS
from combat.battle import Battle

from entities.enemy import Enemy
from entities.entity_list import ENEMIES

from ui.battle_base import BattleBase

# this is lwk the lifeblood of the battle system, cant have fights without seamless and easy battle creation
# imports all the important enemy data for the fight to properly work
def start_event_battle(player, enemy_name, return_ui):

    enemy_data = ENEMIES[enemy_name]

    enemy = Enemy(

        name=enemy_data["name"],

        hp=enemy_data["hp"],

        attack=enemy_data["attack"],

        defense=enemy_data["defense"],

        sprite=enemy_data["sprite"],

        crit_chance=enemy_data.get(
            "crit_chance",
            0.1
        ),

        crit_multiplier=enemy_data.get(
            "crit_multiplier",
            1.5
        ),

        dodge_chance=enemy_data.get(
            "dodge_chance",
            0.05
        ),

        tier=enemy_data.get(
            "tier",
            1
        ),

        description=enemy_data.get(
            "description",
            ""
        )
    )

    enemy.attacks = [

        ATTACKS[name].copy()

        for name in enemy_data["attacks"]
    ]

    battle = Battle(player, enemy)

    # IMPORTANT
    battle.return_ui = return_ui

    battle.mode = "battle"

    return BattleBase(battle)