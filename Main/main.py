import pygame
from Main.menu import Menu

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.mixer.pre_init(44100, -16, 8, 256)
pygame.mixer.init()
pygame.init()
pygame.mixer.music.load('../Sounds/battle.wav')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.5)
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

menu = Menu(screen, "Space Invaders Deluxe")
menu.run()


