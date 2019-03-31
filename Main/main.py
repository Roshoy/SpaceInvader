import sys
import pygame
import random
from vector import Vector

pygame.init()
screen = pygame.display.set_mode((1000,600))

block = pygame.Rect(0,0,30,30)


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
    def __init__(self, rect, direction):
        super().__init__(rect)
        self.speed = 7
        self.active = True
        self.color = (0, 255, 0)
        self.velocity = direction
        self.velocity = self.velocity * self.speed

    def update(self, screen):
        self.move_ip(self.velocity[0], self.velocity[1])
        if not (self.height + screen.get_height() > self.y > -self.height and self.width + screen.get_width() > self.x > -self.width):
            self.active = False
        return self.active

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self)


class Enemy(pygame.Rect):
    def __init__(self, rect, speed=5):
        super().__init__(rect)
        self.move_dir = Vector(0, 1)
        self.velocity = Vector(0, speed)
        self.speed = speed
        self.restraining = random.randrange(100, 200, 1)
        self.missile_prefab = (8, 8)
        self.missiles = []
        self.shot_interval = 1000
        self.shot_timer = 0

    def shoot(self):
        new_missile = Missile(pygame.Rect(self.center, self.missile_prefab), self.velocity.normalized())
        self.missiles.append(new_missile)

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
            self.shoot()
            self.shot_timer = 0
        else:
            self.shot_timer += d_time
        self.missiles = [x for x in self.missiles if x.update(screen)]

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), self)


class Player(pygame.Rect):
    def __init__(self, rect, speed):
        self.speed = speed
        self.move_dir = Vector(0, 0)
        self.missile_prefab = (10,30)
        self.missiles = []
        super().__init__(rect)
        self.velocity = Vector(0,0)
        self.precision = 5
        self.shot_interval = 500
        self.shot_timer = 0.0
        self.can_shoot = True

    def shoot(self):
        if self.can_shoot:
            new_missile = Missile(pygame.Rect((self.x + self.width/2, self.y), self.missile_prefab), Vector(0,-1))
            self.missiles.append(new_missile)
            self.can_shoot = False
            self.shot_timer = 0


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
            self.move_dir = Vector(0,0)
            self.velocity = Vector(0,0)
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
        self.missiles = [x for x in self.missiles if x.update(screen)]

    def update(self, mouse_pos):
        self.x = mouse_pos[0] - self.width / 2
        self.y = mouse_pos[1] - self.height / 2


stars = [Star() for x in range(200)]

player = Player(block, speed=5)
enemies = []
enemies.append(Enemy(pygame.Rect(900, 0, 30, 30)))

timer = 0

hits = 0

while True:
    d_time = pygame.time.Clock().tick(60)
    timer += d_time
    if len(enemies) < 4:
        timer += d_time
        if timer > 2000:
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
    player.update2(pygame.mouse.get_pos(), d_time, screen)

    for s in stars:
        s.update()
        s.draw(screen)


    for m in player.missiles:
        e_count = len(enemies)
        enemies = [e for e in enemies if not( e.colliderect(m) and m.active)]
        if e_count != len(enemies):
            m.active = False
        m.draw(screen)

    for e in enemies:
        e.update(player.center, d_time, screen)
        for m in e.missiles:
            if m.colliderect(player):
                hits += 1
                print("Trafiony po raz: " + str(hits))
            m.draw(screen)
        e.draw(screen)



    pygame.draw.rect(screen, (0, 255, 0), player)
    pygame.display.flip()

