import pygame
from Main.missile import Missile


class PlayerMissile(Missile):
    stat_size = (8, 24)
    tag = "player"

    def __init__(self, pos, player, direction):
        super().__init__(pygame.Rect(pos, self.stat_size), player, direction)


class EnemyMissile(Missile):
    stat_size = (16, 16)
    tag = "enemy"

    def __init__(self, pos, direction):
        super().__init__(pygame.Rect(pos, self.stat_size), self.tag, direction)
