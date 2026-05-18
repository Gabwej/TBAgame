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

class MusicManager:
    _current = None
    _volume = 1.0
    _target_volume = 1.0
    _fading = False
    _fade_speed = 0.02

    @classmethod
    def init(cls):
        pygame.mixer.init()

    @classmethod
    def play_loop(cls, path, volume=1.0):

        if cls._current == path:
            return

        cls._current = path
        cls._fading = False

        pygame.mixer.music.load(path)
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play(-1)

    @classmethod
    def fade_to(cls, path, volume=1.0, fade_time=800):

        # fade out current music, then switches :O
        pygame.mixer.music.fadeout(fade_time)

        cls._current = path

        def switch():
            pygame.mixer.music.load(path)
            pygame.mixer.music.set_volume(volume)
            pygame.mixer.music.play(-1)

        pygame.time.set_timer(pygame.USEREVENT + 1, fade_time, loops=1)

        cls._pending_switch = switch

    @classmethod
    def handle_event(cls, event):

        # called from main game loop
        if event.type == pygame.USEREVENT + 1:
            if hasattr(cls, "_pending_switch"):
                cls._pending_switch()
                del cls._pending_switch