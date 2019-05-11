from Main.vector import Vector
import pygame
import random
from Main.missile import Missile
from Main.spaceship import SpaceShip
from enum import Enum
from Main.animation import Animation


class Enemy(SpaceShip):

    class State(Enum):
        ALIVE = 0
        EXPLODING = 1
        DEAD = 2

    tag = "enemy"
    missile_size = (16, 16)

    def __init__(self, rect, speed=5):
        super().__init__(rect, speed)
        self.restraining = random.randrange(100, 200, 1)
        self.explosion_anim = Animation(tuple([int(i*1.5) for i in self.size]), 3)
        self.explosion_anim.add_frames("explosion", 5)
        self.fly_anim = Animation(self.size)
        self.fly_anim.add_frames(self.tag, 1)
        self.state = self.State.ALIVE
        self.animation = self.fly_anim

    def move_auto(self, player_pos):
        self.move_dir.v = [player_pos[i] - self.center[i] for i in range(len(player_pos))]
        vel_magni = self.move_dir.magnitude()
        if vel_magni > self.restraining:
            self.move_dir = self.move_dir.normalized()
            self.velocity = self.velocity + self.move_dir * self.speed / 18.0
        vel_magni = self.velocity.magnitude()
        if vel_magni != 0:
            self.velocity = self.velocity * self.speed / vel_magni

    def set_state(self, new_state):
        self.state = new_state
        if self.state is self.State.ALIVE:
            self.animation = self.fly_anim
        elif self.state is self.State.EXPLODING:
            self.animation = self.explosion_anim

    def update(self, player_pos, d_time):
        if self.state is self.state.ALIVE:
            self.move_auto(player_pos)
            super().update(d_time)
            self.animation.animate_circular()
        elif self.state is self.state.EXPLODING:
            if self.animation.animate_serial():
                self.set_state(self.State.DEAD)

