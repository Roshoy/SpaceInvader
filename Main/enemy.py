from Main.vector import Vector
import pygame
import random
from Main.missile import Missile


class Enemy(pygame.Rect):
    def __init__(self, rect, speed=5):
        super().__init__(rect)
        self.move_dir = Vector(0, 1)
        self.velocity = Vector(0, speed)
        self.speed = speed
        self.restraining = random.randrange(100, 200, 1)
        self.missile_prefab = (8, 8)
        self.missiles = []
        self.shot_interval = 500
        self.shot_timer = 0

    def shoot(self):
        new_missile = Missile(pygame.Rect(self.center, self.missile_prefab), self.velocity.normalized())
        #self.missiles.append(new_missile)
        return new_missile

    def update(self, player_pos, d_time, screen):
        self.move_dir.v = [player_pos[i] - self.center[i] for i in range(len(player_pos))]
        vel_magni = self.move_dir.magnitude()
        if vel_magni > self.restraining:
            self.move_dir = self.move_dir.normalized()
            self.velocity = self.velocity + self.move_dir*self.speed/18.0
        vel_magni = self.velocity.magnitude()
        if vel_magni != 0:
            self.velocity = self.velocity * self.speed / vel_magni
        self.x += self.velocity[0]
        self.y += self.velocity[1]
        if self.shot_timer >= self.shot_interval:
            self.shot_timer = 0
            return self.shoot()
        else:
            self.shot_timer += d_time
        return False
        #self.missiles = [x for x in self.missiles if x.update(screen)]

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), self)

