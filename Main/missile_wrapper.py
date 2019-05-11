from Main.missile import Missile
import pygame
from Main.Player import Player
from Main.enemy import Enemy

class MissileWrapper:
    def __init__(self):
        self.enemy_missiles = []
        self.player_missiles = []
        self.hits = 0
        self.enemy_missiles_texture = pygame.image.load("../Textures/enemy_missile.png")
        self.player_missiles_texture = pygame.image.load("../Textures/player_missile.png")

    def player_hit(self, player: Player):
        for m in self.enemy_missiles:
            if m.colliderect(player) and m.active:
                m.active = False
                self.hits += 1
                print("Trafiony po raz: " + str(self.hits))
                return True
        return False

    def enemy_hit(self, enemy: Enemy):
        for m in self.player_missiles:
            if m.colliderect(enemy) and m.active:
                m.active = False
                return True
        return False

    def clear_inactive(self):
        self.enemy_missiles = [m for m in self.enemy_missiles if m.active]
        self.player_missiles = [m for m in self.player_missiles if m.active]

    def update(self, screen):
        self.clear_inactive()
        for m in self.enemy_missiles:
            m.update(screen)
        for m in self.player_missiles:
            m.update(screen)

    def draw(self, screen):
        for m in self.enemy_missiles:
            m.draw(screen)
        for m in self.player_missiles:
            m.draw(screen)

    def add_from_enemy(self, enemy_shot):
        if enemy_shot:
            self.enemy_missiles.append(enemy_shot)

    def add_from_player(self, player_shot):
        if player_shot:
            self.player_missiles.append(player_shot)
