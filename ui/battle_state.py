from combat.battle import Battle


class BattleState:
    def __init__(self, player, enemy):
        self.battle = Battle(player, enemy)

        self.buttons = []

    def handle_input(self, event):
        return None

    def update(self):
        pass

    def draw(self, screen):
        screen.fill((0, 0, 50))

        import pygame
        font = pygame.font.Font(None, 30)

        log = self.battle.get_current_log()

        text = font.render(log, True, (255, 255, 255))
        screen.blit(text, (50, 50))

    def next_log(self):
        self.battle.next_log()

    def player_attack(self, attack):
        self.battle.player_attack(attack)