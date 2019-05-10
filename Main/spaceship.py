from Main.vector import Vector
import pygame
import random
from Main.missile import Missile
from Main.animation import Animation

class SpaceShip(pygame.Rect):
    tag = ""
    shot_interval = 500
    missile_size = (1, 1)
    texture = None

    def __init__(self, rect, speed):
        super().__init__(rect)
        self.move_dir = Vector(0, 1)
        self.velocity = self.move_dir * speed
        self.speed = speed
        self.shot_timer = 0
        self.can_shoot = False
        self.animation = Animation((self.width, self.height))
    #   textures

    def missile_prefab(self):
        return Missile(pygame.Rect(self.center, self.missile_size), self.velocity.normalized(),
                       self.tag)

    def shoot(self):
        if self.can_shoot:
            self.can_shoot = False
            self.shot_timer = 0
            return self.missile_prefab()
        return False

    def update(self, d_time):
        self.move_ip(self.velocity[0], self.velocity[1])
        if self.shot_timer >= self.shot_interval:
            self.can_shoot = True
        else:
            self.shot_timer += d_time

    def draw(self, screen):
        self.animation.draw(screen, self.center)
