EVENTS = [

    # 0
    {
        "type": "dialog",
        "text": (
            "You wake up laying in a large field of flowers.\n"
            "You are unsure how you ended up here.\n\n"
            "The sky is clear and the smell of pollen fills your lungs.\n"
            "You could lay here all day."
        ),
        "background": "graphics/summer2.png",
        "encounter_sprite": None,
        "options": [
            {
                "text": "Stand up",
                "result": (
                    "No use laying here.\n"
                    "You decide to get up and start walking."
                ),
                "next": 1
            },
            {
                "text": "Look around",
                "result": (
                    "The field stretches as far as your eyes can see.\n"
                    "You spot a forest a ways away.\n\n"
                    "You decide to walk there."
                ),
                "next": 2
            }
        ]
    },

    # 1
    {
        "type": "dialog",
        "text": (
            "You stumble upon a green pile of goo lying in the field of flowers.\n"
            "What will you do?"
        ),
        "background": "graphics/summer2.png",
        "encounter_sprite": ("monster3", 14),
        "options": [
            {
                "text": "Poke it",
                "result": (
                    "It did not like that.\n"
                    "The goo starts moving on its own and hurls itself at you!"
                ),
                "next": 3
            },
            {
                "text": "Ignore it",
                "result": (
                    "You decide not to meddle with it.\n"
                    "Maybe it's for the best.\n\n"
                    "Better to be safe than sorry."
                ),
                "effects": [
                    {"type": "stat", "stat": "defense", "value": 1}
                ],
                "next": 4
            },
            {
                "text": "Attack it",
                "result": (
                    "You hack off a lump that starts wiggling on the ground.\n"
                    "You pick it up and put it in a vial.\n\n"
                    "At the same time the goo starts moving on its own and hurls itself at you!"
                ),
                "effects": [
                    {"type": "item", "item": "mystery_vial", "amount": 1}
                ],
                "next": 3
            }
        ]
    },

    # 2
    {
        "type": "dialog",
        "text": (
            "After walking for a while the terrain becomes more hilly.\n"
            "Suddenly you see something small scurry between some trees.\n\n"
            "What will you do?"
        ),
        "background": "graphics/landscape3.png",
        "encounter_sprite": None,
        "options": [
            {
                "text": "Call out",
                "result": (
                    "You loudly call out to whatever that was to come out.\n"
                    "You seem to get no answer at first, but all of a sudden someone reveals themself."
                ),
                "next": 5
            },
            {
                "text": "Avoid it",
                "result": (
                    "You decide to continue walking as if nothing happened.\n"
                    "You could swear that someone was watching you, staring daggers at you."
                ),
                "effects": [
                    {"type": "damage", "value": 2}
                ],
                "next": 6
            }
        ]
    },

    # 3
    {
        "type": "battle",
        "enemy": "Slime",
        "background": "graphics/summer2.png",
        "encounter_sprite": ("monster3", 14),
        "next": 7
    },

    # 4
    {
        "type": "dialog",
        "text": (
            "You continue on your journey.\n"
            "The only question on your mind is where to go next."
        ),
        "background": "graphics/summer2.png",
        "encounter_sprite": None,
        "options": [
            {
                "text": "To the sea",
                "result": (
                    "You want to hear the waves.\n"
                    "You decide to go north without guarantees for your destination."
                ),
                "next": 8
            },
            {
                "text": "To the woods",
                "result": (
                    "You saw some trees far in the distance.\n"
                    "Why not go there?"
                ),
                "next": 2
            },
            {
                "text": "Follow the wind",
                "result": (
                    "You decide to follow the path of least resistance.\n\n"
                    "You feel like nothing can stop you."
                ),
                "effects": [
                    {"type": "stat", "stat": "max_hp", "value": 3}
                ],
                "next": 6
            }
        ]
    },

    # 5
    {
        "type": "dialog",
        "text": (
            "A halfling appears before you!\n"
            "'What do you want?' he says with an angry expression.\n"
            "He says that he was out hunting and that your presence scared the wildlife.\n\n"
            "What will you do?"
        ),
        "background": "graphics/landscape3.png",
        "encounter_sprite": ("monster1", 0),
        "options": [
            {
                "text": "Apologise",
                "result": (
                    "You say that you're sorry and that it won't happen again.\n"
                    "'Fair enough,' he says.\n"
                    "'Just be careful since you didn't know, but the west is halfling territory.\n"
                    "You should leave while you have the chance.'\n\n"
                    "You decide to listen to him and leave."
                ),
                "next": 6
            },
            {
                "text": "Attack",
                "result": (
                    "You don't like his attitude.\n"
                    "So you decide to attack him!\n"
                    "But his wits are well trained and he scores an early hit on you!"
                ),
                "effects": [
                    {"type": "damage", "value": 10}
                ],
                "next": 9
            }
        ]
    },

    # 6
    {
        "type": "dialog",
        "text": (
            "You are unsure where you should go now.\n"
            "You walk around for a while but find nothing of importance.\n"
            "You've gotten lost.\n\n"
            "'Time to stick to one direction!' you think to yourself.\n"
            "But which one?"
        ),
        "background": "graphics/landscape4.png",
        "encounter_sprite": None,
        "options": [
            {
                "text": "Go north",
                "result": (
                    "You don't know where you're going except north.\n"
                    "As you're walking you start to feel a breeze."
                ),
                "next": 1
            },
            {
                "text": "Go west",
                "result": (
                    "You go west.\n"
                    "Maybe civilisation is that way?"
                ),
                "next": 2
            },
            {
                "text": "Go south",
                "result": (
                    "You go south.\n"
                    "You feel an elemental presence lead you."
                ),
                "next": 8
            },
            {
                "text": "Go east",
                "result": (
                    "You go east.\n"
                    "Towards the mountains, you mutter to yourself as you see the silhouettes in the distance."
                ),
                "next": 10
            }
        ]
    },

    # 7
    {
        "type": "dialog",
        "text": "You come out victorious against the blob!",
        "background": "graphics/summer2.png",
        "encounter_sprite": None,
        "options": [
            {
                "text": "Continue",
                "result": (
                    "You continue walking across the field.\n"
                    "But as you are walking you discover some acid still stuck on you after the battle..."
                ),
                "effects": [
                    {"type": "damage", "value": 5}
                ],
                "next": 4
            }
        ]
    },

    # 8
    {
        "type": "dialog",
        "text": (
            "You arrive at a beach.\n"
            "The sand glistens in the sun."
        ),
        "background": "graphics/ocean2.png",
        "encounter_sprite": None,
        "options": [
            {
                "text": "Look around",
                "result": (
                    "You discover an old boat.\n"
                    "Someone left supplies behind."
                ),
                "effects": [
                    {"type": "item", "item": "potion", "amount": 1}
                ],
                "next": 11
            },
            {
                "text": "Follow the shore",
                "result": (
                    "You keep moving along the waterline.\n"
                    "The wind feels colder here."
                ),
                "next_pool": [12, 13]
            }
        ]
    },

    # 9
    {
        "type": "battle",
        "enemy": "Halfling bowman",
        "background": "graphics/landscape3.png",
        "encounter_sprite": ("monster1", 0),
        "next": 7
    },

    # 10
    {
        "type": "dialog",
        "text": (
            "The trees grow thicker as you head east.\n"
            "Something ancient stirs nearby."
        ),
        "background": "graphics/landscape6.png",
        "encounter_sprite": ("monster2", 13),
        "options": [
            {
                "text": "Approach the tree",
                "result": "The bark creaks ominously as it awakens.",
                "next": 14
            },
            {
                "text": "Back away",
                "result": "You keep your distance, but the forest feels hostile.",
                "effects": [
                    {"type": "damage", "value": 2}
                ],
                "next": 6
            }
        ]
    },

    # 11
    {
        "type": "dialog",
        "text": (
            "The boat is old, but the supplies are still usable.\n"
            "A strange mark is carved into the wood."
        ),
        "background": "graphics/ocean3.png",
        "encounter_sprite": None,
        "options": [
            {
                "text": "Take the supplies",
                "result": "You gather what you can carry.",
                "effects": [
                    {"type": "item", "item": "bomb", "amount": 1},
                    {"type": "item", "item": "escape_rope", "amount": 1}
                ],
                "next": 12
            },
            {
                "text": "Leave them",
                "result": "You decide not to disturb the boat.",
                "next_pool": [12, 13]
            }
        ]
    },

    # 12
    {
        "type": "dialog",
        "text": (
            "A thick mist rolls in from the sea.\n"
            "You hear something dragging itself through the sand."
        ),
        "background": "graphics/ocean4.png",
        "encounter_sprite": ("monster3", 6),
        "options": [
            {
                "text": "Investigate",
                "result": "An undead creature lunges from the fog!",
                "next": 15
            },
            {
                "text": "Run",
                "result": "You move faster, but the fog still scratches at your skin.",
                "effects": [
                    {"type": "damage", "value": 3}
                ],
                "next": 13
            }
        ]
    },

    # 13
    {
        "type": "dialog",
        "text": (
            "The shoreline curves endlessly.\n"
            "You can either keep following it or head inland."
        ),
        "background": "graphics/ocean5.png",
        "encounter_sprite": None,
        "options": [
            {
                "text": "Keep following",
                "result": "The sea remains beside you.",
                "next_pool": [8, 11, 12]
            },
            {
                "text": "Head inland",
                "result": "You leave the coast behind.",
                "next": 6
            }
        ]
    },

    # 14
    {
        "type": "battle",
        "enemy": "Treant",
        "background": "graphics/landscape2.png",
        "encounter_sprite": ("monster2", 13),
        "next": 16
    },

    # 15
    {
        "type": "battle",
        "enemy": "Zombie",
        "background": "graphics/ocean4.png",
        "encounter_sprite": ("monster3", 6),
        "next": 7
    },

    # 16
    {
        "type": "dialog",
        "text": (
            "Beyond the treant's clearing, the world opens up again.\n"
            "You feel like you've pushed deeper than before."
        ),
        "background": "graphics/summer6.png",
        "encounter_sprite": None,
        "options": [
            {
                "text": "Continue deeper",
                "result": "The path ahead is unknown, but it is yours to choose.",
                "next_pool": [1, 4, 6, 8, 10, 12, 13]
            }
        ]
    }
]