import pygame
from Main.animation import Animation
from enum import Enum


class Missile(pygame.sprite.Sprite, Animation):
    damage = 1
    tag = ""
    stat_size = (1, 1)

    class State(Enum):
        ALIVE = 0
        EXPLODING = 1
        DEAD = 2

    def __init__(self, rect, owner, direction):
        pygame.sprite.Sprite.__init__(self)
        Animation.__init__(self)
        rect.left -= self.stat_size[0] / 2
        self.rect = rect
        self.speed = 7
        self.active = True
        self.color = (0, 255, 0)
        self.velocity = direction
        self.velocity = self.velocity * self.speed
        self.owner = owner
        self.state = None
        self.set_state(self.State.ALIVE)

    @classmethod
    def init(cls):
        cls.frame_sets = dict()
        if cls.tag is not "rocket":
            cls.add_frames(cls.tag + "_missile2", 2, cls.State.ALIVE, cls.stat_size)
        else:
            cls.add_frames(cls.tag, 1, cls.State.ALIVE, cls.stat_size)
        cls.add_frames("explosion", 5, cls.State.EXPLODING, tuple([i*1.5 for i in cls.stat_size]))

    def set_state(self, new_state):
        if self.state is new_state:
            return
        self.state = new_state
        if self.state is not self.State.DEAD:
            self.set_frame_set(self.state)

    def update(self, *args):

        if self.state is self.State.ALIVE:
            self.animate_circular()
        else:
            if self.animate_serial():
                self.state = self.State.DEAD
            return self.state

        self.rect.move_ip(self.velocity[0], self.velocity[1])
        if not (self.rect.height + args[0].get_height() > self.rect.y > -self.rect.height and
                self.rect.width + args[0].get_width() > self.rect.x > -self.rect.width):
            self.active = False
            self.state = self.State.DEAD
        return self.state
    #
    # def draw(self, screen):
    #     self.animation.draw(screen, self.center)
