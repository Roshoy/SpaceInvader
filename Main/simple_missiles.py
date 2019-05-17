import pygame
from Main.missile import Missile
from Main.animation import Animation


class PlayerMissile(Missile):
    stat_size = (8, 24)
    tag = "player"

    def __init__(self, pos, player_num, direction):
        super().__init__(pygame.Rect(pos, self.stat_size), self.tag+str(player_num), direction)


class EnemyMissile(Missile):
    stat_size = (16, 16)
    tag = "enemy"

    def __init__(self, pos, direction):
        super().__init__(pygame.Rect(pos, self.stat_size), self.tag, direction)
