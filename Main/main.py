import pygame
from Main.menu import Menu


pygame.mixer.pre_init(44100, -16, 8, 1024)
pygame.mixer.init()
pygame.init()
pygame.mixer.music.load('../Sounds/battle.wav')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.1)
screen = pygame.display.set_mode((1000, 800))#, pygame.FULLSCREEN)
#screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
#while True:
#    pass
menu = Menu(screen, "Space Invaders Deluxe")
menu.run()


