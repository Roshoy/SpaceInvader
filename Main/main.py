import sys
import pygame
import random
from Main.vector import Vector
from Main.Player import Player
from Main.enemy import Enemy
from Main.star import Star
from Main.missile_wrapper import MissileWrapper


pygame.init()
screen = pygame.display.set_mode((1000,600))

block = pygame.Rect(0, 0, 30, 30)

stars = [Star(screen) for x in range(200)]

player = Player(block, speed=9)
enemies = [Enemy(pygame.Rect(900, 0, 30, 30))]

timer = 0

hits = 0

missile_wraper = MissileWrapper()

while True:
    d_time = pygame.time.Clock().tick(60)
    if len(enemies) < 4:
        timer += d_time
        if timer > 2000:
            enemies.append(Enemy(pygame.Rect(random.randrange(0, screen.get_width(), 1), -30, 30, 30)))
            timer = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            missile_wraper.add_from_player(player.shoot())
        if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0] == 1:
            missile_wraper.add_from_player(player.shoot())
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            sys.exit(0)

    screen.fill((0, 0, 0))
    player.update2(pygame.mouse.get_pos(), d_time, screen)

    for s in stars:
        s.update(screen)
        s.draw(screen)

    missile_wraper.update(screen)

    for e in enemies:
        missile_wraper.add_from_enemy(e.update(player.center, d_time, screen))
        e.draw(screen)

    enemies = [e for e in enemies if not missile_wraper.enemy_hit(e)]
    missile_wraper.player_hit(player)
    missile_wraper.draw(screen)
    pygame.draw.rect(screen, (0, 255, 0), player)
    pygame.display.flip()

