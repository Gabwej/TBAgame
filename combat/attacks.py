from combat.effects import *
from entities.base import Buff

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
        self.damage_dealt = 0
        logs.append(f"{user.name} used {self.name}!")

        # play sound if exists
        if self.sound:
            self.sound.play()

        for effect in self.effects:
            damage, effect_logs = effect.apply(user, target, self)

            total_damage += damage
            self.damage_dealt += damage
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
    "Slash": Attack(
        name="Slash",
        description="Put in some power? (10 dmg). \n0 cooldown, 0 cast time",
        effects=[
            DamageEffect(10, scaling=0.8),
        ],
        icon=Assets.icons[16][12],
        sound=None  # sound, maybe later
    ),
    "Heavy Slash": Attack(
        name="Heavy Slash",
        description="Overhead baby. (25 dmg) \n3 cooldown, 0 cast time",
        effects=[
            DamageEffect(25),
        ],
        cooldown=3,
        icon=Assets.icons[16][13],
        sound=None  # sound, maybe later
    ),
    "Flesh Wound": Attack(
        name="Flesh Wound",
        description="This but a... (2 bleed) \n1 cooldown, 0 cast time",
        effects=[
            BleedEffect(2),
        ],
        cooldown=1,
        start_cooldown=1,
        icon=Assets.icons[6][1],
        sound=None  # sound, maybe later
    ),
    "Defencive Stance": Attack(
        name="Defencive Stance",
        description="Lock arms and pray. (10 def) \n4 cooldown, 0 cast time",
        effects=[
            BuffEffect("defense", 10, 2),
        ],
        cooldown=4,
        start_cooldown=2,
        icon=Assets.icons[20][0],
        sound=None  # sound, maybe later
    ),
    "Quick Shot": Attack(
        name="Quick Shot",
        description="If only you aimed... (10 dmg) \n0 cooldown, 0 cast time",
        effects=[
            DamageEffect(10, scaling=0.8),
        ],
        icon=Assets.icons[16][0],
        sound=None  # sound, maybe later
    ),
    "Piercing Shot": Attack(
        name="Piercing Shot",
        description="Very sharp. (5 dmg, 3 bleed) \n2 cooldown, 0 cast time",
        effects=[
            DamageEffect(5,1.0),
            BleedEffect(3),
        ],
        cooldown=2,
        cannot_miss=True,  #  ignores dodge
        icon=Assets.icons[16][2],
        sound=None  # sound, maybe later
    ),
    "Heavy Shot": Attack(
        name="Heavy Shot",
        description="Uses blunt arrows? (25 dmg, 1 stun). \n3 cooldown, 0 cast time",
        effects=[
            DamageEffect(25, 1.5),
            StunEffect(1),
        ],
        cooldown=3,
        start_cooldown=2,
        icon=Assets.icons[16][1],
        sound=None  # sound, maybe later
    ),
    "Pocket Walnuts": Attack(
        name="Pocket Walnuts",
        description="Eat some pocket loot. (15 hp, 5 atk) \n3 cooldown, 0 cast time",
        effects=[
            HealEffect(15),
            BuffEffect("attack", 5, 3),
        ],
        cooldown=3,
        start_cooldown=1,
        cannot_miss=True,  #  ignores dodge
        icon=Assets.icons[22][0],
        sound=None  # sound, maybe later
    ),
    "Stick Slap": Attack(
        name="Stick Slap",
        description="Bonk em! (5 dmg) \n0 cooldown, 0 cast time",
        effects=[
            DamageEffect(5, scaling=0.8),
        ],
        cannot_miss=True,  #  ignores dodge
        icon=Assets.icons[23][10],
        sound=None  # sound, maybe later
    ),
    "Fireball": Attack(
        name="Fireball",
        description="I cast fireball! (15 dmg, 2 burn). \n1 cooldown, 1 cast time",
        effects=[
            DamageEffect(15, 1.3),
            BurnEffect(2),
        ],
        cooldown=1,
        cast_time=1,
        icon=Assets.icons[0][8],
        sound=None  # sound, maybe later
    ),
    "Magic Missile": Attack(
        name="Magic Missile",
        description="I cast: (3x shots 5-10 dmg) \n3 cooldown, 1 cast time",
        effects=[
            DamageEffect(10, 0.4),
            DamageEffect(7, 0.4),
            DamageEffect(5, 0.5),
        ],
        cooldown=3,
        start_cooldown=2,
        cast_time=1,
        cannot_miss=False,  #  ignores dodge
        icon=Assets.icons[11][2],
        sound=None  # sound, maybe later
    ),
    "Simple Heal": Attack(
        name="Simple Heal",
        description="Channel the spirits. (20 hp, 5 def) \n5 cooldown, 0 cast time",
        effects=[
            HealEffect(20),
            BuffEffect("defense", 5, 3)
        ],
        cooldown=5,
        start_cooldown=2,
        icon=Assets.icons[21][1],
        sound=None  # sound, maybe later
    ),
    "Simple Stab": Attack(
        name="Simple Stab",
        description="Stab em! (10 dmg, 1 bleed) \n0 cooldown, 0 cast time",
        effects=[
            DamageEffect(10, 1.0),
            BleedEffect(1),
        ],
        icon=Assets.icons[13][13],
        sound=None  # sound, maybe later
    ),
    "Coated Stab": Attack(
        name="Coated Stab",
        description="Like stab but bad. (10 dmg, 2 poison) \n2 cooldown, 0 cast time",
        effects=[
            DamageEffect(10, 0.9),
            PoisonEffect(2),
        ],
        cooldown=2,
        icon=Assets.icons[12][12],
        sound=None  # sound, maybe later
    ),
    "Smoke Bomb": Attack(
        name="Smoke Bomb",
        description="Hey whats this? (10 dmg, 2 stun) \n3 cooldown, 0 cast time",
        effects=[
            DamageEffect(10, 0.5),
            StunEffect(2),
        ],
        cooldown=3,
        start_cooldown=2,
        cast_time=0,
        cannot_miss=True,
        icon=Assets.icons[25][11],
        sound=None  # sound, maybe later
    ),
    "Bri'ish Stab": Attack(
        name="Bri'ish Stab",
        description="Do em like the torieys! (20 dmg, 4 poison) \n6 cooldown, 2 cast time",
        effects=[
            DamageEffect(20, 1.5),
            PoisonEffect(4),
        ],
        cooldown=6,
        start_cooldown=3,
        cast_time=2,
        icon=Assets.icons[5][13],
        sound=None  # sound, maybe later
    ),
    "Bite": Attack(
        name="Bite",
        description="You bite. (7 dmg) \n0 cooldown, 0 cast time",
        effects=[
            DamageEffect(7, 1),
        ],
        icon=Assets.icons[23][11],
        sound=None  # sound, maybe later
    ),
    "Evil Bite": Attack(
        name="Evil Bite",
        description="Like Bite but evil. (15 dmg, 2 bleed) \n2 cooldown, 0 cast time",
        effects=[
            DamageEffect(15, 1.3),
            BleedEffect(2),
        ],
        cooldown=0,
        start_cooldown=0,
        cast_time=0,
        icon=Assets.icons[20][11],
        sound=None  # sound, maybe later
    ),
    "Vampire Bite": Attack(
        name="Vampire Bite",
        description="Call me dracula. (35 dmg, 25% lifesteal) \n4 cooldown, 1 cast time",
        effects=[
            DamageEffect(35, 0.9),
            LifeStealEffect(0.25),
        ],
        cooldown=4,
        start_cooldown=1,
        cast_time=1,
        icon=Assets.icons[21][11],
        sound=None  # sound, maybe later
    ),
    "Cross Slash": Attack(
        name="Cross Slash",
        description="Perfect symetry. (20 dmg, 2 bleed) \n3 cooldown, 1 cast time",
        effects=[
            DamageEffect(20, 1.4),
            BleedEffect(2),
        ],
        cooldown=3,
        cast_time=1,
        cannot_miss=True,  #  ignores dodge
        icon=Assets.icons[16][12],
        sound=None  # sound, maybe later
    ),
    "Cold Touch": Attack(
        name="Cold Touch",
        description="Freezing man. (3 atk, 2 Freeze) \n5 cooldown, 1 cast time",
        effects=[
            FreezeEffect(2),
            BuffEffect("attack", 3, 4),
        ],
        cooldown=5,
        start_cooldown=2,
        cast_time=1,
        cannot_miss=True,
        icon=Assets.icons[4][5],
        sound=None  # sound, maybe later
    ),
    "Brittle Bones": Attack(
        name="Brittle Bones",
        description="Drink some milk. (10 dmg, 3 Wither) \n2 cooldown, 0 cast time",
        effects=[
            DamageEffect(10, 0.5),
            WitherEffect(3),
        ],
        cooldown=2,
        start_cooldown=4,
        icon=Assets.icons[15][6],
        sound=None  # sound, maybe later
    ),
    "Pibble Throw": Attack(
        name="Pibble Throw",
        description="Rock put. (20 dmg, 1 stun) \n2 cooldown, 1 cast time",
        effects=[
            DamageEffect(20),
            StunEffect(1),
        ],
        cooldown=2,
        cast_time=1,
        cannot_miss=False,  # ignores dodge
        icon=Assets.icons[16][15],
        sound=None  # sound, maybe later
    ),
    "Piercing Blood": Attack(
        name="Piercing Blood",
        description="Call me Choso? (30 dmg, 5 bleed) \n4 cooldown, 1 cast time",
        effects=[
            DamageEffect(30, 0.9),
            BleedEffect(5),
        ],
        cooldown=4,
        start_cooldown=1,
        cast_time=1,
        cannot_miss=True,  #  ignores dodge
        icon=Assets.icons[21][7],
        sound=None  # sound, maybe later
    ),
    "Empty Lilac": Attack(
        name="Empty Lilac",
        description="I am the honored one! (100 dmg, 4 bleed, 1 stun) \n10 cooldown, 3 cast time",
        effects=[
            DamageEffect(100, 2),
            BleedEffect(4),
            StunEffect(1),
        ],
        cooldown=10,
        start_cooldown=5,
        cast_time=3,
        cannot_miss=True,  #  ignores dodge
        icon=Assets.icons[19][0],
        sound=None  # sound, maybe later
    ),
    "Golem Summon": Attack(
        name="Golem Summon",
        description="He protecc. (20 def) \n6 cooldown, 2 cast time",
        effects=[
            BuffEffect("defense", 20, 2),
        ],
        cooldown=6,
        start_cooldown=3,
        cast_time=2,
        icon=Assets.icons[16][6],
        sound=None  # sound, maybe later
    ),
    "Alchemist Blade": Attack(
        name="Alchemist Blade",
        description="In order to create something.. (40 dmg, 50% lifesteal, 15 hp) \n6 cooldown, 2 cast time",
        effects=[
            HealEffect(15),
            DamageEffect(30, scaling=1.3),
            LifeStealEffect(0.5),  # 30% of damage dealt returned as HP
        ],
        cooldown=6,
        start_cooldown=3,
        cast_time=2,
        cannot_miss=True,  #  ignores dodge
        icon=Assets.icons[3][13],
        sound=None  # sound, maybe later
    ),
    "Ultra Blast": Attack(
        name="Ultra Blast",
        description="Very vague.. (30 dmg, 3 burn) \n4 cooldown, 0 cast time",
        effects=[
            DamageEffect(30),
            BurnEffect(3),
        ],
        cooldown=4,
        start_cooldown=2,
        icon=Assets.icons[2][14],
        sound=None # sound, maybe later
    ),
    "Back Stab": Attack(
        name="Back Stab",
        description="Hit em from behind! (2 bleed, 4 poison) \n4 cooldown, 1 cast time",
        effects=[
            PoisonEffect(4),
            BleedEffect(2),
        ],
        cooldown=4,
        start_cooldown=2,
        cast_time=1,
        icon=Assets.icons[22][9],
        sound=None  # sound, maybe later
    ),
    "Roundhouse Kick": Attack(
        name="Roundhouse Kick",
        description="Im up down, left, right! (35 dmg, 2 stun) \n4 cooldown, 1 cast time",
        effects=[
            DamageEffect(35, 1.1),
            StunEffect(2),
        ],
        cooldown=4,
        start_cooldown=1,
        cast_time=1,
        icon=Assets.icons[11][6],
        sound=None  # sound, maybe later
    ),
    "Black Flash": Attack(
        name="Black Flash",
        description="Reach full potential. (10 dmg, 40 atk, 10 def) \n10 cooldown, 2 cast time",
        effects=[
            DamageEffect(10, 0.5),
            BuffEffect("attack", 40, 3),
            BuffEffect("defense", 10, 3),
        ],
        cooldown=10,
        start_cooldown=5,
        cast_time=2,
        cannot_miss=True,  #  ignores dodge
        icon=Assets.icons[2][0],
        sound=None  # sound, maybe later
    ),
    "Trash Talk": Attack(
        name="Trash Talk",
        description="Rude dude.. (5 wither, 1 stun) \n3 cooldown, 1 cast time",
        effects=[
            WitherEffect(2),
            StunEffect(1),
        ],
        cooldown=3,
        start_cooldown=0,
        cast_time=1,
        cannot_miss=True,  #  ignores dodge
        icon=Assets.icons[21][8],
        sound=None  # sound, maybe later
    ),
    "Acid Ocean": Attack(
        name="Acid Ocean",
        description="Call upon the waves (11 poison) \n10 cooldown, 3 cast time",
        effects=[
            PoisonEffect(11),
        ],
        cooldown=10,
        start_cooldown=5,
        cast_time=3,
        cannot_miss=True,  #  ignores dodge
        icon=Assets.icons[12][5],
        sound=None  # sound, maybe later
    ),
    "Wombo Combo": Attack(
        name="Wombo Combo",
        description="Im left, Im right (5 atk, 4 wither, 3x 10 dmg) \n4 cooldown, 1 cast time",
        effects=[
            BuffEffect("attack", 5, 3),
            WitherEffect(4),
            DamageEffect(10, 0.6),
            DamageEffect(10, 0.5),
            DamageEffect(10, 0.3),
        ],
        cooldown=4,
        start_cooldown=2,
        cast_time=1,
        cannot_miss=True,  #  ignores dodge
        icon=Assets.icons[16][5],
        sound=None  # sound, maybe later
    ),
}