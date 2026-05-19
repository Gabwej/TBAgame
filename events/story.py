EVENTS = [

{
    "type": "dialog",

    "text": "You slowly wake up on unfamiliar ground...",

    "background": "graphics/summer3.png",

    "encounter_sprite": None,

    "options": [
        {
            "text": "Open your eyes",

            "result": "The forest comes into focus. The air feels unusually still.",

            "effects": [
                {"type": "item", "item": "potion", "amount": 1},
                {"type": "item", "item": "cleanse", "amount": 1},
                {"type": "item", "item": "bomb", "amount": 1},
                {"type": "item", "item": "escape_rope", "amount": 1},
                {"type": "item", "item": "mystery_vial", "amount": 1},
                {"type": "item", "item": "adrenaline_shot", "amount": 1},
            ],

            "next": 1
        }
    ]
},

{
    "type": "dialog",

    "text": "You gather your strength and stand up.",

    "background": "graphics/summer3.png",

    "options": [
        {
            "text": "Look around",

            "result": "Trees stretch endlessly in every direction.",

            "effects": [
                {"type": "stat", "stat": "defense", "value": 1}
            ],

            "next": 2
        },

        {
            "text": "Stay still",

            "result": "You wait... but nothing changes.",

            "effects": [],

            "next": 2
        }
    ]
},

{
    "type": "dialog",

    "text": "An old man appears between the trees.",

    "background": "graphics/summer1.png",

    "encounter_sprite": ("player", 14),

    "options": [
        {
            "text": "Approach him",

            "result": "He studies you silently. 'You are not from here.' he utters with a sturdy voice",

            "effects": [
            ],

            "next_pool": [3, 4]
        },

        {
            "text": "Hide",

            "result": "He notices you anyway. 'No need to fear me.' he says",

            "effects": [
                {"type": "stat", "stat": "attack", "value": 1}
            ],

            "next": 3
        }
    ]
},

{
    "type": "battle",

    "enemy": "Slime",

    "background": "graphics/ocean1.png",

    "encounter_sprite": None,

    "next": 5
},

{
    "type": "dialog",

    "text": "The old man disappears without a trace.",

    "background": "graphics/landscape3.png",

    "options": [
        {
            "text": "Continue forward",

            "result": "The forest feels slightly less hostile.",

            "effects": [
                {"type": "heal", "value": 5}
            ],

            "next": 5
        }
    ]
},

{
    "type": "dialog",

    "text": "The forest grows darker after your encounter.",

    "background": "graphics/summer4.png",

    "options": [
        {
            "text": "Push deeper",

            "result": "Something watches you from the trees...",

            "effects": [],

            "next": 6
        }
    ]
},

{
    "type": "battle",

    "enemy": "Goblin grunt",

    "background": "graphics/landscape5.png",

    "encounter_sprite": None,

    "next": 7
},

{
    "type": "dialog",

    "text": "The path ahead splits into unknown regions.",

    "background": "graphics/ocean2.png",

    "options": [
        {
            "text": "Take the left path",

            "result": "Wind carries strange whispers.",

            "effects": [],

            "next_pool": [3]
        },

        {
            "text": "Take the right path",

            "result": "You feel something familiar ahead...",

            "effects": [],
            "next_pool": [6]
        }
    ]
}

]