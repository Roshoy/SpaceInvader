import pygame
from Main.vector import Vector
from Main.missile import Missile


class Player(pygame.Rect):
    def __init__(self, rect, speed):
        self.speed = speed
        self.move_dir = Vector(0, 0)
        self.missile_prefab = (10, 30)
        self.missiles = []
        super().__init__(rect)
        self.velocity = Vector(0, 0)
        self.precision = 5
        self.shot_interval = 200
        self.shot_timer = 0.0
        self.can_shoot = True

    def shoot(self):
        if self.can_shoot:
            new_missile = Missile(pygame.Rect((self.x + self.width/2, self.y), self.missile_prefab), Vector(0, -1))
            #self.missiles.append(new_missile)
            self.can_shoot = False
            self.shot_timer = 0
            return new_missile
        return False

    def update22(self, screen):

        if self.move_dir[0] > 0:
            self.move_dir[0] -= 0.01
        elif self.move_dir[0] < 0:
            self.move_dir[0] += 0.01

        if self.move_dir[1] > 0:
            self.move_dir[1] -= 0.01
        elif self.move_dir[1] < 0:
            self.move_dir[1] += 0.01

        if pygame.key.get_pressed()[pygame.K_RIGHT] and self.move_dir[0] < 1:
            self.move_dir[0] += 0.05
        if pygame.key.get_pressed()[pygame.K_LEFT] and self.move_dir[0] > -1:
            self.move_dir[0] -= 0.05
        if pygame.key.get_pressed()[pygame.K_UP] and self.move_dir[1] > -1:
            self.move_dir[1] -= 0.05
        if pygame.key.get_pressed()[pygame.K_DOWN] and self.move_dir[1] < 1:
            self.move_dir[1] += 0.05

        if 0 > self.center[0] and self.move_dir[0] < 0:
            self.move_dir[0] = 0
        if self.center[0] > screen.get_width() and self.move_dir[0] > 0:
            self.move_dir[0] = 0
        if 0 > self.center[1] and self.move_dir[1] < 0:
            self.move_dir[1] = 0
        if self.center[1] > screen.get_height() and self.move_dir[1] > 0:
            self.move_dir[1] = 0

        self.move_ip(self.move_dir[0]*self.speed, self.move_dir[1]*self.speed)
        self.missiles = [x for x in self.missiles if x.update(screen)]

    def update2(self, mouse_pos, d_time, screen):
        self.move_dir.v = [mouse_pos[i] - self.center[i] for i in range(2)]
        vel_magni = self.move_dir.magnitude()
        if vel_magni < self.precision:
            self.x = mouse_pos[0] - self.width/2
            self.y = mouse_pos[1] - self.height/2
            self.move_dir = Vector(0, 0)
            self.velocity = Vector(0, 0)
        else:
            self.move_dir = self.move_dir / vel_magni
            self.velocity = self.velocity + self.move_dir * self.speed * 2.0
            vel_magni = self.velocity.magnitude()
            if vel_magni != 0:
                self.velocity = self.velocity * self.speed / vel_magni
            self.x += self.velocity[0]
            self.y += self.velocity[1]
        if self.shot_timer >= self.shot_interval:
            self.can_shoot = True
        else:
            self.shot_timer += d_time
        #self.missiles = [x for x in self.missiles if x.update(screen)]

    def update(self, mouse_pos):
        self.x = mouse_pos[0] - self.width / 2
        self.y = mouse_pos[1] - self.height / 2
