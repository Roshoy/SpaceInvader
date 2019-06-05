from Main.missile import Missile
import pygame
from Main.Player import Player
from Main.enemy import Enemy
from Main.rocket import Rocket
from Main.vector import Vector
from Main.sound_manager import SoundManager


class MissileWrapper:
    def __init__(self):
        self.enemy_missiles = pygame.sprite.Group()
        self.player_missiles = pygame.sprite.Group()
        self.hits = 0
        self.player_rockets = pygame.sprite.Group()

    def player_hit(self, player: Player):
        if player.state is Player.State.EXPLODING or player.state is Player.State.DEAD:
            return
        for m in pygame.sprite.spritecollide(player, self.enemy_missiles, False):
            if m.state is Missile.State.ALIVE:
                player.get_hit(m)
                m.active = False
                m.set_state(Missile.State.EXPLODING)
                self.hits += 1

                SoundManager.sound_player_hit()

    def enemy_hit(self, enemy: Enemy):
        for m in pygame.sprite.spritecollide(enemy, self.player_missiles, False):
            if m.state is Missile.State.ALIVE:
                if 0 >= enemy.get_hit(m):
                    m.owner.points += enemy.points
                m.set_state(Missile.State.DEAD)

        for m in pygame.sprite.spritecollide(enemy, self.player_rockets, False):
            if m.state is Missile.State.ALIVE:
                if 0 >= enemy.get_hit(m):
                    m.owner.points += enemy.points
                m.set_state(Missile.State.EXPLODING)

    def enemy_aoe_hit(self, enemy: Enemy):
        for r in self.player_rockets.sprites():
            if Vector(r.rect.center[0] - enemy.rect.center[0], r.rect.center[1] - enemy.rect.center[1]).magnitude() <\
                    r.radius and r.state is Missile.State.EXPLODING and r.active:
                if 0 >= enemy.get_hit(r):
                    r.owner.points += enemy.points
                return True
        return False

    def clear_inactive(self):
        [self.enemy_missiles.remove(m) for m in self.enemy_missiles.sprites() if m.state is Missile.State.DEAD]
        [self.player_missiles.remove(m) for m in self.player_missiles.sprites() if m.state is Missile.State.DEAD]
        [self.player_rockets.remove(m) for m in self.player_rockets.sprites() if m.state is Missile.State.DEAD]

    def update(self, screen):
        self.clear_inactive()
        for m in self.enemy_missiles:
            m.update(screen)
        for m in self.player_missiles:
            m.update(screen)
        for m in self.player_rockets:
            m.update(screen)

    def draw(self, screen):
        self.enemy_missiles.draw(screen)
        self.player_missiles.draw(screen)
        self.player_rockets.draw(screen)

    def add_from_enemy(self, enemy_shot):
        if enemy_shot:
            self.enemy_missiles.add(enemy_shot)

    def add_from_player(self, player_shot):
        if player_shot:
            if isinstance(player_shot, Rocket):
                self.player_rockets.add(player_shot)
            else:
                self.player_missiles.add(player_shot)
