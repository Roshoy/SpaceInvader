import pygame
from Main.missile import Missile
from Main.animation import Animation
from Main.vector import Vector


class Rocket(Missile):
    radius = 150
    damage = 10
    stat_size = (12, 24)
    tag = "rocket"

    def __init__(self, rect, direction=Vector(0, -1)):
        super().__init__(rect, direction)
        self.set_state(self.State.ALIVE)

    @classmethod
    def init(cls):
        cls.frame_sets = dict()
        cls.add_frames(cls.tag, 1, cls.State.ALIVE, cls.stat_size)
        cls.add_frames("explosion", 5, cls.State.EXPLODING, (cls.radius*2, cls.radius*2))

    def set_state(self, new_state):
        if new_state is self.State.EXPLODING:
            self.rect.left += self.stat_size[0] - self.radius
            self.rect.top -= self.radius
        super().set_state(new_state)



    def update(self, screen):
        if self.state is self.State.EXPLODING:
            self.active = False
        return super().update(screen)

