from entities.player import Player
from combat.attacks import ATTACKS
from assets.images import Assets

CHARACTERS = {

"warrior": {
    "name": "Warrior",
    "hp": 140,
    "attack": 10,
    "defense": 10,

    "crit_chance": 0.05,
    "crit_multiplier": 1.5,
    "dodge_chance": 0.03,

    "attacks": [
        "Slash",
        "Heavy Slash",
        "Flesh Wound",
        "Defensive Stance"
    ],
    "sprite": ("player", 4)
},

"ranger": {
    "name": "Ranger",
    "hp": 110,
    "attack": 12,
    "defense": 6,

    "crit_chance": 0.15,
    "crit_multiplier": 1.7,
    "dodge_chance": 0.08,

    "attacks": [
        "Quick Shot",
        "Piercing Shot",
        "Heavy Shot",
        "Pocket Walnuts"
    ],
    "sprite": ("player", 1)
},

"mage": {
    "name": "Mage",
    "hp": 90,
    "attack": 14,
    "defense": 4,

    "crit_chance": 0.1,
    "crit_multiplier": 1.5,
    "dodge_chance": 0.05,

    "attacks": [
        "Stick Slap",
        "Fireball",
        "Magic Missile",
        "Simple Heal"
    ],
    "sprite": ("player", 2)
},

"rogue": {
    "name": "Rogue",
    "hp": 100,
    "attack": 11,
    "defense": 5,

    "crit_chance": 0.15,
    "crit_multiplier": 1.8,
    "dodge_chance": 0.15,

    "attacks": [
        "Test Attack",
        #"Simple Stab",
        "Coated Stab",
        "Smoke Bomb",
        "Bri'ish Stab"
    ],
    "sprite": ("player",0)
},

}

def create_player(character_id):
    data = CHARACTERS[character_id]

    player = Player(
        name=data["name"],
        hp=data["hp"],
        attack=data["attack"],
        defense=data["defense"],

        crit_chance=data["crit_chance"],
        crit_multiplier=data["crit_multiplier"],
        dodge_chance=data["dodge_chance"],

        sprite = data["sprite"]
    )

    player.attacks = [
        ATTACKS[name].copy()
        for name in data["attacks"]
    ]

    return player