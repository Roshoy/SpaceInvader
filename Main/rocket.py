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
        self.bomb_explosion_sound = pygame.mixer.Sound("../Sounds/bomb_explosion.wav")
        self.rocket_shot_sound = pygame.mixer.Sound("../Sounds/rocket_shot.wav")
        self.rocket_shot_sound.play(0, 0, 1)

    @classmethod
    def init(cls):
        cls.frame_sets = dict()
        cls.add_frames("rocket", 1, cls.State.ALIVE, cls.stat_size)
        cls.add_frames("explosion", 5, cls.State.EXPLODING, (cls.radius*2, cls.radius*2))

    def set_state(self, new_state):
        if self.state is new_state:
            return
        if new_state is self.State.EXPLODING:
            self.rocket_shot_sound.stop()
            self.bomb_explosion_sound.play(0, 0, 1)
            self.rect = pygame.Rect(self.rect.left + self.stat_size[0] - self.radius, self.rect.top - self.radius,
                                    self.radius * 2, self.radius * 2)
        super().set_state(new_state)



    def update(self, screen):
        if self.state is self.State.EXPLODING:
            self.active = False
        return super().update(screen)

