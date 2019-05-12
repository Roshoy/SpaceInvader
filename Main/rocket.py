import pygame
from Main.missile import Missile
from Main.animation import Animation
from Main.vector import Vector


class Rocket(Missile):
    radius = 150

    def __init__(self, rect, direction=Vector(0, -1), texture_path="rocket"):
        super().__init__(rect, direction, texture_path)
        self.fly_anim = Animation(self.size, 7)
        self.fly_anim.add_frames(texture_path, 1)
        self.explosion_anim = Animation((self.radius*2, self.radius*2), 5)
        self.explosion_anim.add_frames("explosion", 5)
        self.animation = self.fly_anim

    def update(self, screen):
        if self.state is self.State.EXPLODING:
            self.active = False
        return super().update(screen)

