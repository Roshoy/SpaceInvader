import sys
import pygame
import random
import math

pygame.init()
screen = pygame.display.set_mode((1000,600))

block = pygame.Rect(0,0,30,30)

class Vector:
    v = []

    def __init__(self, *args):
        for a in args:
            self.v.append(a)

    def __len__(self):
        return len(self.v)

    def __contains__(self, x):
        return x in self.v

    def __iter__(self):
        for x in self.v:
            yield x

    def __getitem__(self, item):
        return self.v[item]

    def __setitem__(self, key, value):
        self.v[key] = value

    def magnitude(self):
        return math.sqrt(sum([v**2 for v in self.v]))

    def __truediv__(self, other):
        nv = Vector()
        nv.v = [x/other for x in self.v]
        return nv

    def __mul__(self, other):
        nv = Vector()
        nv.v = [x*other for x in self.v]
        return nv

    def normalized(self):
        return self/self.magnitude()

    def __add__(self, other):
        nv = Vector()
        nv.v = [self.v[i] + other.v[i] for i in range(len(self.v))]
        return nv

    def __sub__(self, other):
        nv = Vector()
        if len(other) != len(self):
            print("Wyjątek! Zly wymiar wektora")
            return Vector()
        nv.v = [self.v[i] - other.v[i] for i in range(len(self))]
        return nv


class Star:

    def __init__(self):
        size = random.randrange(10, 30, 2)/10.0
        self.rect = pygame.Rect(random.randrange(0, screen.get_width(), 1), random.randrange(0,screen.get_height(), 1), size, size)
        self.vy = random.randrange(100, 500, 2)/100.0
        self.color = (random.randrange(0,256,1),random.randrange(0,256,1),random.randrange(0,256,1))

    def update(self):
        self.rect.y += self.vy
        if self.rect.y > screen.get_height() + 10:
            self.reset()

    def reset(self):
        self.rect.y = random.randrange(-30, 0, 1)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self)


class Missile(pygame.Rect):
    def __init__(self, rect):
        super().__init__(rect)
        self.speed = 7

    def update(self):
        self.move_ip(0, -self.speed)
        print(self.y)
        if self.y < -self.height:
            return False
        return True


class Enemy(pygame.Rect):
    def __init__(self, rect, speed=5):
        super().__init__(rect)
        self.move_dir = Vector(0, 1)
        self.velocity = Vector(0, speed)
        self.speed = speed
        self.restraining = random.randrange(100, 200, 1)

    def update(self, player_pos):
        self.move_dir = self.move_dir - player_pos
        vel_magni = self.move_dir.magnitude()
        if vel_magni > self.restraining:
            self.move_dir = self.move_dir.normalize()
            self.velocity = [self.velocity[i] + self.move_dir[i]*self.speed/18.0 for i in range(2)]
        vel_magni = math.sqrt(self.velocity[0] ** 2 + self.velocity[1] ** 2)
        if vel_magni == 0:
            vel_magni = 1
        self.velocity = [x * self.speed / vel_magni for x in self.velocity]
        self.x += self.velocity[0]
        self.y += self.velocity[1]


    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), self)


class Player(pygame.Rect):
    def __init__(self, rect, speed):
        self.speed = speed
        self.move_dir = [0, 0]
        self.missile_prefab = (10,30)
        self.missiles = []
        super().__init__(rect)
        self.velocity = [0, 0]
        self.precision = 5

    def shoot(self):
        new_missile = Missile(pygame.Rect((self.x + self.width/2, self.y), self.missile_prefab))
        self.missiles.append(new_missile)
        print(len(self.missiles))

    def update2(self, screen):

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
        self.missiles = [x for x in self.missiles if x.update()]

    def update2(self, mouse_pos):
        self.move_dir = [mouse_pos[i] - self.center[i] for i in range(2)]
        vel_magni = math.sqrt(self.move_dir[0] ** 2 + self.move_dir[1] ** 2)
        if vel_magni < self.precision:
            self.x = mouse_pos[0] - self.width/2
            self.y = mouse_pos[1] - self.height/2
            self.move_dir = [0, 0]
            self.velocity = [0, 0]
        else:
            self.move_dir = [i / vel_magni for i in self.move_dir]
            self.velocity = [self.velocity[i] + self.move_dir[i] * self.speed * 2.0 for i in range(2)]
            vel_magni = math.sqrt(self.velocity[0] ** 2 + self.velocity[1] ** 2)
            if vel_magni == 0:
                vel_magni = 1
            self.velocity = [x * self.speed / vel_magni for x in self.velocity]
            self.x += self.velocity[0]
            self.y += self.velocity[1]
        self.missiles = [x for x in self.missiles if x.update()]

    def update(self, mouse_pos):
        self.x = mouse_pos[0] - self.width / 2
        self.y = mouse_pos[1] - self.height / 2


stars = [Star() for x in range(200)]

player = Player(block, speed=5)
enemies = []
enemies.append(Enemy(pygame.Rect(900, 0, 30, 30)))

enemies.append(Enemy(pygame.Rect(0, 500, 30, 30)))
timer = 0

while True:
    d_time = pygame.time.Clock().tick(60)
    timer += d_time
    if timer > 2000 and len(enemies) < 3:
        enemies.append(Enemy(pygame.Rect(random.randrange(0,screen.get_width(),1),-30, 30,30)))
        timer = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            player.shoot()
        if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0] == 1:
            player.shoot()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            sys.exit(0)

    screen.fill((0, 0, 0))
    player.update2(pygame.mouse.get_pos())

    for s in stars:
        s.update()
        s.draw(screen)

    for e in enemies:
        e.update(player.center)
        e.draw(screen)

    for m in player.missiles:
        enemies = [e for e in enemies if not e.colliderect(m)]
        pygame.draw.rect(screen, (0, 255, 0), m)

    pygame.draw.rect(screen, (0, 255, 0), player)
    pygame.display.flip()

