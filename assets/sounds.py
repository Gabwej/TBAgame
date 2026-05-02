import pygame

class Sounds:
    hover = None
    press = None


def load_sounds():
    Sounds.hover = pygame.mixer.Sound("../sounds/hover.mp3")
    Sounds.press = pygame.mixer.Sound("../sounds/press.mp3")

    Sounds.hover.set_volume(0.1)
    Sounds.press.set_volume(0.1)


class SoundManager:
    sounds = {}

    @classmethod
    def load(cls):
        cls.sounds = {
            "hover": pygame.mixer.Sound("sounds/hover.mp3"),
            "press": pygame.mixer.Sound("sounds/press.mp3"),
        }

        # volumes
        cls.sounds["hover"].set_volume(0.1)
        cls.sounds["press"].set_volume(0.1)

    @classmethod
    def play(cls, name):
        if name in cls.sounds:
            cls.sounds[name].play()