from Main.vector import Vector
import pygame
import random
from Main.missile import Missile
from Main.animation import Animation
from enum import Enum


class SpaceShip(pygame.sprite.Sprite, Animation):
    tag = ""
    shot_interval = 500
    missile_size = (1, 1)
    texture = None
    max_life = 1

    class State(Enum):
        ALIVE = 0
        EXPLODING = 1
        DEAD = 2

    def __init__(self, rect, speed):
        pygame.sprite.Sprite.__init__(self)
        Animation.__init__(self)
        self.rect = rect
        #self.move_dir = Vector(0, 1)
        self.velocity = Vector(0, 1) * speed
        self.speed = speed
        self.acceleration = 1
        self.shot_timer = 0
        self.can_shoot = False
        self.life = self.max_life

    #    self.state = self.State.ALIVE
    #   textures

    def missile_prefab(self):
        return Missile(pygame.Rect(self.rect.center, self.missile_size), self.velocity.normalized())

    def set_state(self, state):
        pass

    def shoot(self):
        if self.can_shoot:
            self.can_shoot = False
            self.shot_timer = 0
            return self.missile_prefab()
        return False

    def get_hit(self, missile: Missile):
        self.life -= missile.damage
        if self.life <= 0:
            self.set_state(self.State.EXPLODING)

    def update(self, *args):
        self.rect.move_ip(self.velocity[0], self.velocity[1])
        if self.shot_timer >= self.shot_interval:
            self.can_shoot = True
        else:
            self.shot_timer += args[0]

