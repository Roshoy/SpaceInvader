import pygame
from Main.Engine import Engine
from Main.menu import Menu
pygame.init()
screen = pygame.display.set_mode((1200, 800))
# comment

menu = Menu(screen, "Space Invaders Deluxe")
menu.run()

#engine = Engine(screen)
#engine.run_single()
