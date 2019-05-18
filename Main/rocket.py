import pygame
from Main.missile import Missile
from Main.vector import Vector


class Rocket(Missile):
    radius = 150
    damage = 10
    stat_size = (12, 24)
    tag = "rocket"

    def __init__(self, rect, owner, direction=Vector(0, -1)):
        super().__init__(rect, owner, direction)
        self.set_state(self.State.ALIVE)

    @classmethod
    def init(cls):
        cls.frame_sets = dict()
        cls.add_frames("rocket", 1, cls.State.ALIVE, cls.stat_size)
        cls.add_frames("explosion", 5, cls.State.EXPLODING, (cls.radius*2, cls.radius*2))

    def set_state(self, new_state):
        if self.state is new_state:
            return
        if new_state is self.State.EXPLODING:
            self.rect = pygame.Rect(self.rect.left + self.stat_size[0] - self.radius, self.rect.top - self.radius,
                                    self.radius * 2, self.radius * 2)
        super().set_state(new_state)



    def update(self, screen):
        if self.state is self.State.EXPLODING:
            self.active = False
        return super().update(screen)

