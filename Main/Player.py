import pygame
from Main.vector import Vector
from Main.missile import Missile
from Main.spaceship import SpaceShip


class Player(SpaceShip):
    shot_interval = 200
    texture = pygame.image.load("../Textures/player_idle.png")
    tag = "player"
    missile_size = (10, 30)

    def __init__(self, rect, speed, controls=
                 (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_RETURN)):
        super().__init__(rect, speed)
        self.move_dir = Vector(0, 0)
        self.velocity = Vector(0, 0)
        self.precision = 5
        self.controls = controls
        self.texture = pygame.transform.scale(self.texture, self.size)

    def missile_prefab(self):
        return Missile(pygame.Rect(self.center, self.missile_size), Vector(0, -1),
                       self.tag)

    def shoot_trigger(self):
        if self.controls[4] != -1 and pygame.key.get_pressed()[self.controls[4]]:
            return True
        elif self.controls[4] == -1 and pygame.mouse.get_pressed()[0]:
            return True
        return False

    def move_keyboard(self, screen):
        if self.move_dir[0] > 0:
            self.move_dir[0] -= 0.01
        elif self.move_dir[0] < 0:
            self.move_dir[0] += 0.01

        if self.move_dir[1] > 0:
            self.move_dir[1] -= 0.01
        elif self.move_dir[1] < 0:
            self.move_dir[1] += 0.01
#       RIGHT, LEFT, UP, DOWN
        if pygame.key.get_pressed()[self.controls[3]] and self.move_dir[0] < 1:
            self.move_dir[0] += 0.05
        if pygame.key.get_pressed()[self.controls[2]] and self.move_dir[0] > -1:
            self.move_dir[0] -= 0.05
        if pygame.key.get_pressed()[self.controls[0]] and self.move_dir[1] > -1:
            self.move_dir[1] -= 0.05
        if pygame.key.get_pressed()[self.controls[1]] and self.move_dir[1] < 1:
            self.move_dir[1] += 0.05

        if 0 > self.center[0] and self.move_dir[0] < 0:
            self.move_dir[0] = 0
        if self.center[0] > screen.get_width() and self.move_dir[0] > 0:
            self.move_dir[0] = 0
        if 0 > self.center[1] and self.move_dir[1] < 0:
            self.move_dir[1] = 0
        if self.center[1] > screen.get_height() and self.move_dir[1] > 0:
            self.move_dir[1] = 0

        self.velocity = self.move_dir * self.speed

    def move_mouse(self, mouse_pos):
        self.move_dir.v = [mouse_pos[i] - self.center[i] for i in range(2)]
        vel_magni = self.move_dir.magnitude()
        if vel_magni < self.precision:
            self.velocity[0] = mouse_pos[0] - self.center[0]
            self.velocity[1] = mouse_pos[1] - self.center[1]
        else:
            self.move_dir = self.move_dir / vel_magni
            self.velocity = self.velocity + self.move_dir * self.speed * 2.0
            if self.velocity.magnitude() != 0:
                self.velocity = self.velocity.normalized() * self.speed

    def update_keyboard(self, d_time, screen):
        self.move_keyboard(screen)
        super().update(d_time)

    def update_mouse(self, mouse_pos, d_time):
        self.move_mouse(mouse_pos)
        super().update(d_time)
