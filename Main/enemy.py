from Main.vector import Vector
import pygame
import random
from Main.missile import Missile
from Main.spaceship import SpaceShip


class Enemy(SpaceShip):
    tag = "enemy"
    texture = pygame.image.load("../Textures/enemy.png")
    missile_size = (16, 16)

    def __init__(self, rect, speed=5):
        super().__init__(rect, speed)
        self.restraining = random.randrange(100, 200, 1)
        self.texture = pygame.transform.scale(self.texture, self.size)

    def move_auto(self, player_pos):
        self.move_dir.v = [player_pos[i] - self.center[i] for i in range(len(player_pos))]
        vel_magni = self.move_dir.magnitude()
        if vel_magni > self.restraining:
            self.move_dir = self.move_dir.normalized()
            self.velocity = self.velocity + self.move_dir * self.speed / 18.0
        vel_magni = self.velocity.magnitude()
        if vel_magni != 0:
            self.velocity = self.velocity * self.speed / vel_magni

    def update(self, player_pos, d_time):
        self.move_auto(player_pos)
        super().update(d_time)
