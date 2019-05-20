import pygame
from Main.game import Game

pygame.mixer.pre_init(44100, -16, 8, 1024)
pygame.mixer.init()
pygame.init()

game = Game()
game.run()
