import pygame
from Main.vector import Vector
from Main.missile import Missile


class Player(pygame.Rect):
    def __init__(self, rect, speed, color, controls =
    (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_RETURN)):
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
        self.color = color
        self.controls = controls
        self.texture = pygame.image.load("../Textures/player_idle.png")
        self.texture = pygame.transform.scale(self.texture, self.size)

    def shoot_trigger(self):
        if  self.controls[4] != -1 and pygame.key.get_pressed()[self.controls[4]]:
            return True
        elif self.controls[4] == -1 and pygame.mouse.get_pressed()[0]:
            return True
        return False

    def shoot(self):
        if self.can_shoot and self.shoot_trigger():
            new_missile = Missile(pygame.Rect((self.x + self.width/2, self.y), self.missile_prefab), Vector(0, -1))
            self.can_shoot = False
            self.shot_timer = 0
            return new_missile
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
        self.move_ip(self.move_dir[0]*self.speed, self.move_dir[1]*self.speed)

    def move_mouse(self, mouse_pos):
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

    def update_keyboard(self, d_time, screen):
        self.move_keyboard(screen)
        if self.shot_timer >= self.shot_interval:
            self.can_shoot = True
        else:
            self.shot_timer += d_time

    def update_mouse(self, mouse_pos, d_time):
        self.move_mouse(mouse_pos)
        if self.shot_timer >= self.shot_interval:
            self.can_shoot = True
        else:
            self.shot_timer += d_time

    def draw(self, screen):
        screen.blit(self.texture, (self.left, self.top))
        #pygame.draw.rect(screen, self.color, self)
