import pygame
from Main.Engine import Engine


pygame.init()
screen = pygame.display.set_mode((800, 600))

engine = Engine(screen)
engine.run_single()
