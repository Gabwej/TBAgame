from assets.images import get_sprite, get_icon
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

        self.icon_id = icon

        self.description = description

        self.cast_time = cast_time
        self.current_cast = 0

        self.cannot_miss = cannot_miss

        self.sound = sound

    def use(self, user, target):
        logs = []

        total_damage = 0
        self.damage_dealt = 0

        logs.append(f"{user.name} used {self.name}!")

        # full attack dodge check
        if not self.cannot_miss:
            import random

            if random.random() < target.dodge_chance:
                logs.append(f"{target.name} dodged the attack!")
                self.current_cooldown = self.cooldown
                return 0, logs

        # play sound if exists
        if self.sound:
            self.sound.play()

        for effect in self.effects:
            damage, effect_logs = effect.apply(user, target, self)

            total_damage += damage
            self.damage_dealt += damage
            logs.extend(effect_logs)

            if not target.is_alive():
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
            icon=self.icon_id,
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
        description="Put in some power?\n(10 dmg). \n\n0 cooldown, 0 cast time",
        effects=[
            DamageEffect(10, scaling=0.8),
        ],
        icon=(16, 12),
        sound=None  # sound, maybe later
    ),
    "Heavy Slash": Attack(
        name="Heavy Slash",
        description="Do you even lift bro?\n(25 dmg)\n\n3 cooldown, 0 cast time",
        effects=[
            DamageEffect(25),
        ],
        cooldown=3,
        icon=(16, 13),
        sound=None  # sound, maybe later
    ),
    "Flesh Wound": Attack(
        name="Flesh Wound",
        description="This but a scratch!\n(4 bleed)\n\n3 cooldown, 0 cast time",
        effects=[
            BleedEffect(4),
        ],
        cooldown=3,
        start_cooldown=1,
        icon=(6, 1),
        sound=None  # sound, maybe later
    ),
    "Defensive Stance": Attack(
        name="Defensive Stance",
        description="Lock arms and pray. \n(10 def:2) \n\n4 cooldown, 0 cast time",
        effects=[
            BuffEffect("defense", 10, 2),
        ],
        cooldown=4,
        start_cooldown=2,
        icon=(20, 0),
        sound=None  # sound, maybe later
    ),
    "Quick Shot": Attack(
        name="Quick Shot",
        description="If only you aimed... \n(10 dmg) \n\n0 cooldown, 0 cast time",
        effects=[
            DamageEffect(10, scaling=0.8),
        ],
        icon=(16, 2),
        sound=None  # sound, maybe later
    ),
    "Piercing Shot": Attack(
        name="Piercing Shot",
        description="Very sharp. \n(5 dmg, 3 bleed) \n\n3 cooldown, 0 cast time",
        effects=[
            DamageEffect(5,1.0),
            BleedEffect(3),
        ],
        cooldown=3,
        cannot_miss=True,  #  ignores dodge
        icon=(16,5),
        sound=None  # sound, maybe later
    ),
    "Heavy Shot": Attack(
        name="Heavy Shot",
        description="Uses blunt arrows? \n(20 dmg, 1 stun). \n\n3 cooldown, 0 cast time",
        effects=[
            DamageEffect(20, 1.5),
            StunEffect(1),
        ],
        cooldown=3,
        start_cooldown=2,
        icon=(16,1),
        sound=None  # sound, maybe later
    ),
    "Pocket Walnuts": Attack(
        name="Pocket Walnuts",
        description="Common floor loot. \n(15 hp, 5 atk) \n\n3 cooldown, 0 cast time",
        effects=[
            HealEffect(15),
            BuffEffect("attack", 5, 3),
        ],
        cooldown=3,
        start_cooldown=1,
        cannot_miss=True,  #  ignores dodge
        icon=(22,0),
        sound=None  # sound, maybe later
    ),
    "Stick Slap": Attack(
        name="Stick Slap",
        description="Bonk em! \n(5 dmg) \n\n0 cooldown, 0 cast time",
        effects=[
            DamageEffect(5, scaling=0.8),
        ],
        cannot_miss=True,  #  ignores dodge
        icon=(23, 10),
        sound=None  # sound, maybe later
    ),
    "Fireball": Attack(
        name="Fireball",
        description="I dont care how small the room is!\n(15 dmg, 2 burn). \n\n1 cooldown, 1 cast time",
        effects=[
            DamageEffect(15, 1.3),
            BurnEffect(2),
        ],
        cooldown=1,
        cast_time=1,
        icon=(0,8),
        sound=None  # sound, maybe later
    ),
    "Magic Missile": Attack(
        name="Magic Missile",
        description="Lightning bolt! Magic missile! \n(3x shots 5-10 dmg) \n\n4 cooldown, 1 cast time",
        effects=[
            DamageEffect(8, 0.4),
            DamageEffect(7, 0.4),
            DamageEffect(5, 0.5),
        ],
        cooldown=4,
        start_cooldown=2,
        cast_time=1,
        cannot_miss=False,  #  ignores dodge
        icon=(11,2),
        sound=None  # sound, maybe later
    ),
    "Simple Heal": Attack(
        name="Simple Heal",
        description="Channel the spirits. \n(20 hp, 5 def) \n\n5 cooldown, 0 cast time",
        effects=[
            HealEffect(20),
            BuffEffect("defense", 5, 3)
        ],
        cooldown=5,
        start_cooldown=2,
        icon=(21,1),
        sound=None  # sound, maybe later
    ),
    "Simple Stab": Attack(
        name="Simple Stab",
        description="Stab em! \n(10 dmg, 1 bleed) \n\n0 cooldown, 0 cast time",
        effects=[
            DamageEffect(10, 1.0),
            BleedEffect(1),
        ],
        icon=(13,13),
        sound=None  # sound, maybe later
    ),
    "Coated Stab": Attack(
        name="Coated Stab",
        description="Like stab but worse. For them... \n(10 dmg, 2 poison) \n\n2 cooldown, 0 cast time",
        effects=[
            DamageEffect(10, 0.9),
            PoisonEffect(2),
        ],
        cooldown=2,
        icon=(12,12),
        sound=None  # sound, maybe later
    ),
    "Smoke Bomb": Attack(
        name="Smoke Bomb",
        description="Hot potato! \n(10 dmg, 2 stun) \n\n3 cooldown, 0 cast time",
        effects=[
            DamageEffect(10, 0.5),
            StunEffect(2),
        ],
        cooldown=3,
        start_cooldown=2,
        cast_time=0,
        cannot_miss=True,
        icon=(25,11),
        sound=None  # sound, maybe later
    ),
    "Bri'ish Stab": Attack(
        name="Bri'ish Stab",
        description="Do em like the torieys! \n(30 dmg, 4 poison) \n\n6 cooldown, 2 cast time",
        effects=[
            DamageEffect(30, 1.5),
            PoisonEffect(4),
        ],
        cooldown=6,
        start_cooldown=3,
        cast_time=2,
        icon=(5,13),
        sound=None  # sound, maybe later
    ),
    "Bite": Attack(
        name="Bite",
        description="You bite. \n(7 dmg) \n\n0 cooldown, 0 cast time",
        effects=[
            DamageEffect(7, 1),
        ],
        icon=(23,11),
        sound=None  # sound, maybe later
    ),
    "Evil Bite": Attack(
        name="Evil Bite",
        description="Like Bite but evil I guess. \n(15 dmg, 2 bleed) \n\n2 cooldown, 0 cast time",
        effects=[
            DamageEffect(15, 1.3),
            BleedEffect(2),
        ],
        cooldown=0,
        start_cooldown=0,
        cast_time=0,
        icon=(20,11),
        sound=None  # sound, maybe later
    ),
    "Vampire Bite": Attack(
        name="Vampire Bite",
        description="Daylight makes me feel like Dracula \n(27 dmg, 25% lifesteal) \n\n4 cooldown, 1 cast time",
        effects=[
            DamageEffect(27, 0.9),
            LifeStealEffect(0.25),
        ],
        cooldown=4,
        start_cooldown=2,
        cast_time=1,
        icon=(21,11),
        sound=None  # sound, maybe later
    ),
    "Cross Slash": Attack(
        name="Cross Slash",
        description="Perfect symetry. \n(30 dmg, 2 bleed) \n\n3 cooldown, 1 cast time",
        effects=[
            DamageEffect(30, 1.2),
            BleedEffect(2),
        ],
        cooldown=3,
        start_cooldown= 2,
        cast_time=1,
        cannot_miss=True,  #  ignores dodge
        icon=(16,12),
        sound=None  # sound, maybe later
    ),
    "Ice Pillar": Attack(
        name="Ice Pillar",
        description="good for offence AND defence. \n(30 dmg, 6 def:4, 1 Freeze) \n\n5 cooldown, 1 cast time",
        effects=[
            DamageEffect(30, 0.9),
            BuffEffect("defense", 6, 4),
            FreezeEffect(1),

        ],
        cooldown=5,
        start_cooldown=3,
        cast_time=1,
        cannot_miss=True,
        icon=(4,5),
        sound=None  # sound, maybe later
    ),
    "Withering Arrow": Attack(
        name="Withering Arrow",
        description="The arrow consumes.. \n(25 dmg, 3 Wither) \n\n2 cooldown, 0 cast time",
        effects=[
            DamageEffect(25, 1.4),
            WitherEffect(3),
        ],
        cooldown=2,
        start_cooldown=4,
        icon=(15,1),
        sound=None  # sound, maybe later
    ),
    "Pebble Throw": Attack(
        name="Pebble Throw",
        description="Go get em buddy! \n(20 dmg, 1 stun) \n\n2 cooldown, 1 cast time",
        effects=[
            DamageEffect(20),
            StunEffect(1),
        ],
        cooldown=2,
        cast_time=1,
        cannot_miss=False,  # ignores dodge
        icon=(16,15),
        sound=None  # sound, maybe later
    ),
    "Piercing Blood": Attack(
        name="Piercing Blood",
        description="As for now hes my brother..\n(30 dmg, 5 bleed) \n\n4 cooldown, 1 cast time",
        effects=[
            DamageEffect(30, 0.9),
            BleedEffect(5),
        ],
        cooldown=4,
        start_cooldown=1,
        cast_time=1,
        cannot_miss=True,  #  ignores dodge
        icon=(21,7),
        sound=None  # sound, maybe later
    ),
    "Hollow Purple": Attack(
        name="Hollow Purple",
        description="Throughout heaven and earth.. \n(100 dmg, 4 bleed, 1 stun) \n\n10 cooldown, 4 cast time",
        effects=[
            DamageEffect(100, 2),
            BleedEffect(4),
            StunEffect(1),
        ],
        cooldown=10,
        start_cooldown=5,
        cast_time=4,
        cannot_miss=True,  #  ignores dodge
        icon=(19,0),
        sound=None  # sound, maybe later
    ),
    "Golem Summon": Attack(
        name="Golem Summon",
        description="He protecc. \n(20 def:5) \n\n6 cooldown, 2 cast time",
        effects=[
            BuffEffect("defense", 20, 5),
        ],
        cooldown=6,
        start_cooldown=3,
        cast_time=2,
        icon=(16,6),
        sound=None  # sound, maybe later
    ),
    "Alchemist Blade": Attack(
        name="Alchemist Blade",
        description="In order to create something.. (40 dmg, 50% lifesteal, 15 hp) \n6 cooldown, 2 cast time",
        effects=[
            HealEffect(15),
            DamageEffect(40, scaling=1.3),
            LifeStealEffect(0.5),
        ],
        cooldown=6,
        start_cooldown=3,
        cast_time=2,
        cannot_miss=True,  #  ignores dodge
        icon=(3,13),
        sound=None  # sound, maybe later
    ),
    "Ultra Blast": Attack(
        name="Ultra Blast",
        description="Very vague.. like cartoony even.. \n(30 dmg, 3 burn) \n\n3 cooldown, 0 cast time",
        effects=[
            DamageEffect(30),
            BurnEffect(3),
        ],
        cooldown=3,
        start_cooldown=2,
        icon=(2,14),
        sound=None # sound, maybe later
    ),
    "Back Stab": Attack(
        name="Back Stab",
        description="Hit em from behind! \n(2 bleed, 4 poison) \n\n3 cooldown, 1 cast time",
        effects=[
            PoisonEffect(6),
            BleedEffect(2),
        ],
        cooldown=3,
        start_cooldown=2,
        cast_time=1,
        icon=(22,9),
        sound=None  # sound, maybe later
    ),
    "Roundhouse Kick": Attack(
        name="Roundhouse Kick",
        description="Up Down Up Down Left Right Left Right. \n(35 dmg, 2 stun) \n\n4 cooldown, 1 cast time",
        effects=[
            DamageEffect(35, 1.1),
            StunEffect(2),
        ],
        cooldown=4,
        start_cooldown=1,
        cast_time=1,
        icon=(11,6),
        sound=None  # sound, maybe later
    ),
    "Black Flash": Attack(
        name="Black Flash",
        description="Unleash the sparks of black, reach full potential. \n(10 dmg, 30 atk:5, 20 hp) \n\n10 cooldown, 2 cast time",
        effects=[
            DamageEffect(10, 0.5),
            BuffEffect("attack", 30, 5),
            HealEffect(20),
        ],
        cooldown=10,
        start_cooldown=5,
        cast_time=2,
        cannot_miss=True,  #  ignores dodge
        icon=(2,0),
        sound=None  # sound, maybe later
    ),
    "Trash Talk": Attack(
        name="Trash Talk",
        description="Bro you have a weapon, use it? \n(10 atk:3, 5 wither, 1 stun) \n\n4 cooldown, 1 cast time",
        effects=[
            BuffEffect("attack", 10, 3),
            WitherEffect(5),
            StunEffect(1),
        ],
        cooldown=4,
        start_cooldown=0,
        cast_time=1,
        cannot_miss=True,  #  ignores dodge
        icon=(21,8),
        sound=None  # sound, maybe later
    ),
    "Acid Ocean": Attack(
        name="Acid Ocean",
        description="Call upon the sulfuric waves! \n(11 poison) \n\n10 cooldown, 2 cast time",
        effects=[
            PoisonEffect(11),
        ],
        cooldown=10,
        start_cooldown=5,
        cast_time=2,
        cannot_miss=True,  #  ignores dodge
        icon=(12,5),
        sound=None  # sound, maybe later
    ),
    "Wombo Combo": Attack(
        name="Wombo Combo",
        description="Im left, im right, im left, im right \n(5 atk, 4 wither, 3x 10 dmg) \n\n4 cooldown, 1 cast time",
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
        icon=(16,5),
        sound=None  # sound, maybe later
    ),
    "Blob": Attack(
        name="Blob",
        description="Throw goo! \n(3 dmg) \n\n0 cooldown, 0 cast time",
        effects=[
            DamageEffect(3, 1.5),
        ],

        icon=(22,12),
        sound=None  # sound, maybe later
    ),
    "Stare": Attack(
        name="Stare",
        description="Mama always told me.. \n(5 dmg, 1 stun) \n\n3 cooldown, 0 cast time",
        effects=[
            DamageEffect(5),
            StunEffect(1),
        ],
        cooldown=3,
        sound=None  # sound, maybe later
    ),
    "Body Slam": Attack(
        name="Body Slam",
        description="No weapon, no problem \n(10 dmg) \n\n0 cooldown, 0 cast time",
        effects=[
            DamageEffect(10, 1.5),
        ],
        sound=None  # sound, maybe later
    ),
    "Natures Gift": Attack(
        name="Natures Gift",
        description="A soothing melody \n(30 hp) \n\n4 cooldown, 0 cast time",
        effects=[
            HealEffect(30),
        ],
        cooldown=4,
        start_cooldown=1,
        icon=(23,5),
        sound=None  # sound, maybe later
    ),
    "Leaf Storm": Attack(
        name="Leaf Storm",
        effects=[
            DamageEffect(5, 0.7),
            DamageEffect(5, 0.4),
            DamageEffect(5, 0.4),
            BleedEffect(2),
        ],
        cooldown=3,
        sound=None  # sound, maybe later
    ),
    "Punch": Attack(
        name="Punch",
        effects=[
            DamageEffect(5, 1.5),
        ],
        sound=None  # sound, maybe later
    ),
    "Spore Cloud": Attack(
        name="Spore Cloud",
        description="Open a window.. \n(3 poison, 1 stun) \n\n3 cooldown, 0 cast time",
        effects=[
            PoisonEffect(3),
            StunEffect(1),
        ],
        cooldown=3,
        icon=(22,12),
        sound=None  # sound, maybe later
    ),
    "Headbutt": Attack(
        name="Headbutt",
        effects=[
            DamageEffect(15),

        ],
    ),
    "Ice Cold Gaze": Attack(
        name="Ice Cold Gaze",
        description="Chills the core \n(2 Freeze, 1 Wither) \n\n4 cooldown, 1 cast time",
        effects=[
            WitherEffect(1),
            FreezeEffect(2),
        ],
        cooldown=4,
        start_cooldown=1,
        cast_time=1,
        cannot_miss=True,
        icon=(22,2),
        sound=None  # sound, maybe later
    ),

    "Test Attack": Attack(
        name="Test Attack",
        description="I really hope no one gets this \n(everything) \n\n10 cooldown, 0 cast time",
        effects=[
            DamageEffect(10),
            BurnEffect(2),
            PoisonEffect(3),
            BleedEffect(2),
            WitherEffect(2),
            FreezeEffect(1),
            StunEffect(1),
            HealEffect(10),
            BuffEffect("attack", 5, 3),
            BuffEffect("defense", 3, 2),
            LifeStealEffect(0.3),  # 30% of damage dealt returned as HP
        ],
        cooldown=10,
        start_cooldown=0,
        cast_time=0,
        cannot_miss=False,  #  ignores dodge
        icon=(0,0),
        sound=None  # sound, maybe later
    ),

}