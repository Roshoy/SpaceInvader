import pygame
from Main.menu import Menu

#test coment

pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

menu = Menu(screen, "Space Invaders Deluxe")
menu.run()


