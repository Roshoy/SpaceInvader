import sys
import pygame
import random
from Main.vector import Vector
from Main.Player import Player
from Main.enemy import Enemy
from Main.star import Star
from Main.missile_wrapper import MissileWrapper


pygame.init()
screen = pygame.display.set_mode((1600,800))

block = pygame.Rect(0, 0, 30, 30)

stars = [Star(screen) for x in range(200)]

player1 = Player(block, 9, (0, 255, 0), (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_RETURN))
player2 = Player(block, 9, (0, 155, 155), (pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d, pygame.K_TAB))
enemies = [Enemy(pygame.Rect(900, 0, 30, 30))]
players = [player1, player2]
timer = 0

hits = 0

missile_wraper = MissileWrapper()

while True:
    d_time = pygame.time.Clock().tick(60)
    if len(enemies) < 8:
        timer += d_time
        if timer > 1500:
            enemies.append(Enemy(pygame.Rect(random.randrange(0, screen.get_width(), 1), -30, 30, 30)))
            timer = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)
        # if event.type == pygame.KEYDOWN and event.key == player1.controls[4]:
        #     missile_wraper.add_from_player(player1.shoot())
        # if event.type == pygame.KEYDOWN and event.key == player1.controls[4]:
        #     missile_wraper.add_from_player(player2.shoot())
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            pass
            #missile_wraper.add_from_player(player.shoot())
        if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0] == 1:
            #missile_wraper.add_from_player(player.shoot())
            pass
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            sys.exit(0)

    screen.fill((0, 0, 0))
    #player.update2(pygame.mouse.get_pos(), d_time, screen)
    missile_wraper.add_from_player(player1.shoot())
    missile_wraper.add_from_player(player2.shoot())
    player1.update22(screen, d_time)
    player2.update22(screen, d_time)
    for s in stars:
        s.update(screen)
        s.draw(screen)

    missile_wraper.update(screen)

    for e in enemies:
        dp1 = Vector(player1.center[0] - e.center[0], player1.center[1] - e.center[1])
        dp2 = Vector(player2.center[0] - e.center[0], player2.center[1] - e.center[1])
        if dp1.magnitude() > dp2.magnitude():
            missile_wraper.add_from_enemy(e.update(player2.center, d_time, screen))
        else:
            missile_wraper.add_from_enemy(e.update(player1.center, d_time, screen))
        e.draw(screen)


    enemies = [e for e in enemies if not missile_wraper.enemy_hit(e)]
    missile_wraper.player_hit(player1)
    missile_wraper.player_hit(player2)
    missile_wraper.draw(screen)
    player1.draw(screen)
    player2.draw(screen)
    #pygame.draw.rect(screen, (0, 255, 0), player)
    pygame.display.flip()
