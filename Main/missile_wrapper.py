from Main.missile import Missile
import pygame
from Main.Player import Player
from Main.enemy import Enemy
from Main.rocket import Rocket
from Main.vector import Vector

class MissileWrapper:
    def __init__(self):
        self.enemy_missiles = []
        self.player_missiles = []
        self.hits = 0
        self.player_rockets = []

    def player_hit(self, player: Player):
        for m in self.enemy_missiles:
            if m.colliderect(player) and m.state is Missile.State.ALIVE:
                m.active = False
                m.set_state(Missile.State.EXPLODING)
                self.hits += 1
                print("Trafiony po raz: " + str(self.hits))
                return True
        return False

    def enemy_hit(self, enemy: Enemy):
        for m in self.player_missiles:
            if m.colliderect(enemy) and m.state is Missile.State.ALIVE:
                m.set_state(Missile.State.DEAD)
                return True
        for r in self.player_rockets:
            if r.colliderect(enemy) and r.state is Missile.State.ALIVE:
                r.set_state(Missile.State.EXPLODING)
                return True
            elif Vector(r.center[0] - enemy.center[0], r.center[1] - enemy.center[1]).magnitude() < r.radius and\
                r.state is Missile.State.EXPLODING and r.active:
                return True
        return False

    def clear_inactive(self):
        self.enemy_missiles = [m for m in self.enemy_missiles if m.state is not Missile.State.DEAD]
        self.player_missiles = [m for m in self.player_missiles if m.state is not Missile.State.DEAD]
        self.player_rockets = [m for m in self.player_rockets if m.state is not Missile.State.DEAD]

    def update(self, screen):
        self.clear_inactive()
        for m in self.enemy_missiles:
            m.update(screen)
        for m in self.player_missiles:
            m.update(screen)
        for m in self.player_rockets:
            m.update(screen)

    def draw(self, screen):
        for m in self.enemy_missiles:
            m.draw(screen)
        for m in self.player_missiles:
            m.draw(screen)
        for m in self.player_rockets:
            m.draw(screen)

    def add_from_enemy(self, enemy_shot):
        if enemy_shot:
            self.enemy_missiles.append(enemy_shot)

    def add_from_player(self, player_shot):
        if player_shot:
            if isinstance(player_shot, Rocket):
                self.player_rockets.append(player_shot)
            else:
                self.player_missiles.append(player_shot)
