import pygame
from Main.enemy import Enemy
import random
from Main.vector import Vector
from Main.missile_wrapper import MissileWrapper


class EnemiesWrapper(pygame.sprite.Group):

    def __init__(self, screen):
        super().__init__(self.enemy_prefab((random.randrange(0, screen.get_width(), 1), -30)))
        self.screen = screen
        self.timer = 0
        self.new_enemy_spawn_interval = 1500
        self.new_enemies_number = 2
        self.max_enemies = 10

    def update(self, d_time, players: pygame.sprite.Group, missile_wrapper: MissileWrapper):
        for e in self.sprites():
            if e.life > 0:
                missile_wrapper.enemy_hit(e)
        for e in self.sprites():
            if e.life > 0:
                missile_wrapper.enemy_aoe_hit(e)
                missile_wrapper.add_from_enemy(e.shoot())
            if e.state is Enemy.State.DEAD:
                self.remove(e)

        if len(players.sprites()) > 1:
            for e in self.sprites():
                dps = [Vector(p.rect.center[0] - e.rect.center[0], p.rect.center[1] - e.rect.center[1]).magnitude()
                       for p in players.sprites()]
                min_dp = min(dps)
                for i in range(len(dps)):
                    if min_dp == dps[i]:
                        e.update(d_time, players.sprites()[i].rect.center)
        elif len(players.sprites()) == 1:
            super().update(d_time, players.sprites()[0].rect.center)

        if len(self.sprites()) < self.max_enemies:
            self.timer += d_time
            if self.timer > self.new_enemy_spawn_interval:
                self.add([self.enemy_prefab((random.randrange(0, self.screen.get_width(), 1), -30))
                          for i in range(self.new_enemies_number)])
                self.timer = 0

    def enemy_prefab(self, pos):
        return Enemy(pygame.Rect(pos[0], pos[1], 30, 30), random.randrange(4, 7, 1))
