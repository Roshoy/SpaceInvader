import pygame
from Main.missile import Missile
from Main.animation import Animation


class PlayerMissile(Missile):
    stat_size = (8, 24)
    tag = "player"

    def __init__(self, pos, direction):
        super().__init__(pygame.Rect(pos, self.stat_size), direction)


class EnemyMissile(Missile):
    stat_size = (16, 16)
    tag = "enemy"

    def __init__(self, pos, direction):
        super().__init__(pygame.Rect(pos, self.stat_size), direction)
