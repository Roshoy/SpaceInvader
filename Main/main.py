import pygame
from Main.Engine import Engine
from Main.menu import Menu
pygame.init()
screen = pygame.display.set_mode((800, 600))

menu = Menu(screen, "Main menu")
menu.run()

#engine = Engine(screen)
#engine.run_single()
