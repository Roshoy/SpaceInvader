import pygame
from Main.animation import Animation
from enum import Enum

class Missile(pygame.Rect):
    class State(Enum):
        ALIVE = 0
        EXPLODING = 1
        DEAD = 2

    def __init__(self, rect, direction, texture_path):
        super().__init__(rect)
        self.speed = 7
        self.active = True
        self.color = (0, 255, 0)
        self.velocity = direction
        self.velocity = self.velocity * self.speed
        self.animation = Animation(self.size)
        if texture_path is not "rocket":
            self.animation.add_frames(texture_path + "_missile2", 2)
        self.fly_anim = self.animation
        self.explosion_anim = Animation(tuple([i*1.5 for i in self.size]), 2)
        self.explosion_anim.add_frames("explosion", 5)
        self.state = self.State.ALIVE

    def set_state(self, new_state):
        self.state = new_state
        if self.state is self.State.ALIVE:
            self.animation = self.fly_anim
        elif self.state is self.State.EXPLODING:
            self.animation = self.explosion_anim

    def update(self, screen):
        if self.state is self.State.ALIVE:
            self.animation.animate_circular()
        else:
            if self.animation.animate_serial():
                self.state = self.State.DEAD
            return self.state
        self.move_ip(self.velocity[0], self.velocity[1])
        if not (self.height + screen.get_height() > self.y > -self.height and
                self.width + screen.get_width() > self.x > -self.width):
            self.active = False
            self.state = self.State.DEAD
        return self.state

    def draw(self, screen):
        self.animation.draw(screen, self.center)
