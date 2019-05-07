import pygame
from Main.Engine import Engine
from Main.menu import Menu
pygame.init()
screen = pygame.display.set_mode((800, 600))
# comment

menu = Menu(screen, "Space Invaders Deluxe")
menu.run()

#engine = Engine(screen)
#engine.run_single()
