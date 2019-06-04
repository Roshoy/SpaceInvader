import pygame
from Main.game import Game
from Main.sound_manager import SoundManager

pygame.mixer.pre_init(44100, -16, 8, 1024)
pygame.mixer.init()
pygame.init()
temp = pygame.image.load("../Textures/color_template.png")
arr = pygame.PixelArray(temp)
for x in arr:
    print(temp.unmap_rgb(x[0]), temp.unmap_rgb(x[1]), temp.unmap_rgb(x[2]), temp.unmap_rgb(x[3]))
arr.replace((64, 24, 12), (12, 15, 64))
for x in arr:
    print(temp.unmap_rgb(x[0]), temp.unmap_rgb(x[1]), temp.unmap_rgb(x[2]), temp.unmap_rgb(x[3]))

sound_manager = SoundManager()
game = Game()
game.run()
