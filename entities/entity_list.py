from entities.enemy import Enemy
from combat.attacks import ATTACKS
from assets.images import Assets


# all enemy data goes here
ENEMIES = {

"slime": {
    "name": "Slime",

    "hp": 32,
    "attack": 6,
    "defense": 3,

    "crit_chance": 0.1,
    "crit_multiplier": 1.3,
    "dodge_chance": 0.03,

    "tier": 1,

    "money_drop": (5, 15),

    "attacks": [
        "Bite",
        "Blob",
    ],

    "sprite": Assets.sprites["monster3"][14],

    "description": "A normal slime, quite weak, poison wont work!",


     "resistances": {
       "poison": 0
    }
},


    "Eye": {
    "name": "Eye",

    "hp": 64,
    "attack": 8,
    "defense": 2,

    "crit_chance": 0.15,
    "crit_multiplier": 1.4,
    "dodge_chance": 0.01,

    "tier": 1,

    "money_drop": (5, 13),

    "attacks": [
        "Stare",
        "Body Slam",
    ],

    "sprite": Assets.sprites["monster3"][0],

    "description": "A lonely eye, rather weak",
},

 "Treant": {
    "name": "Treant",

    "hp": 102,
    "attack": 10,
    "defense": 14,

    "crit_chance": 0.1,
    "crit_multiplier": 1.5,
    "dodge_chance": 0.05,

    "tier": 1,

    "money_drop": (5, 10),

    "attacks": [
        "Stick Slap",
        "Natures Gift",
        "Leaf Storm"
    ],

    "sprite": Assets.sprites["monster2"][13],

    "description": "A walking tree. It has done nothing wrong. Weak to fire.",


     "resistances": {
         "burn": 1.5,
     }
},
 "Goblin grunt": {
    "name": "Goblin grunt",

    "hp": 67,
    "attack": 13,
    "defense": 7,

    "crit_chance": 0.1,
    "crit_multiplier": 1.5,
    "dodge_chance": 0.05,

    "tier": 1,

    "money_drop": (10, 15),

    "attacks": [
        "Quick Shot",
        "Body Slam",
        "Punch"
    ],

    "sprite": Assets.sprites["monster1"][5],

    "description": "The weakest rank of goblin. Quite bland actually",
},

"Spore hatchling": {
    "name": "Spore hatchling",

    "hp": 44,
    "attack": 20,
    "defense": 15,

    "crit_chance": 0.1,
    "crit_multiplier": 1.5,
    "dodge_chance": 0.15,

    "tier": 1,

    "money_drop": (5, 15),

    "attacks": [
        "Spore Cloud",
        "Headbutt",
        "stare"
    ],

    "sprite": Assets.sprites["monster3"][10],

    "description": "A newly born virus. Dont be fooled by it's size. Poison resistant.",

    "resistances": {
     "poison": 0.5
    }
},

    "Zombie": {
    "name": "Zombie",

    "hp": 104,
    "attack": 17,
    "defense": 1,

    "crit_chance": 0.1,
    "crit_multiplier": 1.5,
    "dodge_chance": 0.02,

    "tier": 1,

    "money_drop": (5, 20),

    "attacks": [
        "Bite",
        "Vampire Bite",
        "Body Slam"
    ],

    "sprite": Assets.sprites["monster3"][6],

    "description": "A walking undead, Who could have made this? Bleed wont work.",

     "resistances": {
         "bleed": 0
     }
},

    "Elder": {
    "name": "Elder",

    "hp": 40,
    "attack": 5,
    "defense": 15,

    "crit_chance": 0.01,
    "crit_multiplier": 5,
    "dodge_chance": 0.05,

    "tier": 1,

    "money_drop": (5, 15),

    "attacks": [
        "Stick Slap",
    ],

    "sprite": Assets.sprites["player"][14],

    "description": "He looks like my uncle. What did he do to you? ",
},
    "Halfling bowman": {
    "name": "Halfling bowman",

    "hp": 96,
    "attack": 17,
    "defense": 13,

    "crit_chance": 0.1,
    "crit_multiplier": 1.5,
    "dodge_chance": 0.05,

    "tier": 1,

    "money_drop": (5, 15),

    "attacks": [
        "Quick Shot",
        "Punch",
        "Headbutt"
    ],

    "sprite": Assets.sprites["monster1"][0],

    "description": "A weaker halfling. Should not be a problem.",

},
    "Sentient eye": {
    "name": "Sentient eye",

    "hp": 140,
    "attack": 23,
    "defense": 18,

    "crit_chance": 0.1,
    "crit_multiplier": 1.5,
    "dodge_chance": 0.05,

    "tier": 2,

    "money_drop": (15, 25),

    "attacks": [
        "Stare",
        "Ice Cold Gaze",
        "Headbutt"
    ],

    "sprite": Assets.sprites["monster3"][1],

    "description": "A stronger eye with its gaze locked on you! Weak to bleed",

     "resistances": {
        "bleed": 1.5
    }
},

    "Spore adolescent": {
    "name": "Spore adolescent",

    "hp": 130,
    "attack": 24,
    "defense": 21,

    "crit_chance": 0.1,
    "crit_multiplier": 1.5,
    "dodge_chance": 0.05,

    "tier": 2,

    "money_drop": (15, 25),

    "attacks": [
        "Spore Cloud",
        "Ice Cold Gaze",
        "Evil Bite",
        "Natures Gift"
    ],

    "sprite": Assets.sprites["monster3"][11],

    "description": "It has immense strength for its age. Utilizes nature. resistant to poison, weak to burn",

    "resistances": {
        "poison": 0.5,
        "burn": 1.5
    }
},

    "Goblin bandit": {
    "name": "Goblin bandit",

    "hp": 124,
    "attack": 24,
    "defense": 14,

    "crit_chance": 0.1,
    "crit_multiplier": 1.5,
    "dodge_chance": 0.05,

    "tier": 2,

    "money_drop": (15, 25),

    "attacks": [
        "Heavy Slash",
        "Backstab",
        "Trash Talk",
        "Slash"
    ],

    "sprite": Assets.sprites["monster1"][7],

    "description": "A goblin known for its backhanded tactics, watch out! Weak to bleed, burn.",

     "resistances": {
         "burn": 1.5,
         "bleed": 1.5
     }
},

    "Ashen treant": {
    "name": "Ashen treant",

    "hp": 150,
    "attack": 30,
    "defense": 10,

    "crit_chance": 0.1,
    "crit_multiplier": 1.5,
    "dodge_chance": 0.02,

    "tier": 2,

    "money_drop": (15, 25),

    "attacks": [
        "Slash",
        "Heavy Slash",
    ],

    "sprite": Assets.sprites["monster1"][0],

    "description": "Put description here.",

    # optional
    # "resistances": {
    #     "burn": 0.5,
    #     "poison": 1.5
    # }
},



}


# used for random encounters later
ENEMY_TIERS = {
    1: [
        "Slime", "Eye", "Treant", "Goblin grunt", "Spore hatchling", "Zombie", "Elder", "Halfling bowman"
    ],

    2: [
        "Sentient eye", "Spore adolescent", "Goblin bandit", "Ashen Treant"
    ],

    3: [

    ],

    4: [

    ]
}


# This is what creates the enemies you fight
def create_enemy(enemy_id):

    data = ENEMIES[enemy_id]

    enemy = Enemy(
        name=data["name"],
        hp=data["hp"],
        attack=data["attack"],
        defense=data["defense"],

        sprite=data["sprite"],

        crit_chance=data["crit_chance"],
        crit_multiplier=data["crit_multiplier"],
        dodge_chance=data["dodge_chance"],

        tier=data["tier"],
        description=data["description"]
    )

    enemy.money_drop = data["money_drop"]

    # copies attacks so cooldowns are not shared
    enemy.attacks = [
        ATTACKS[name].copy()
        for name in data["attacks"]
    ]

    if "resistances" in data:
        enemy.resistances.update(data["resistances"])

    return enemy