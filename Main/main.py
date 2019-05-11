import pygame
from Main.Engine import Engine
from Main.menu import Menu
pygame.init()
screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
# comment

menu = Menu(screen, "Space Invaders Deluxe")
menu.run()

#while true:
    ##events


#engine = Engine(screen)
#engine.run_single()
