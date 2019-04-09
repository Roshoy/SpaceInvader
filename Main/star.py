import pygame
import random


class Star:

    def __init__(self, screen):
        size = random.randrange(10, 30, 2)/10.0
        self.rect = pygame.Rect(random.randrange(0, screen.get_width(), 1), random.randrange(0,screen.get_height(), 1), size, size)
        self.vy = random.randrange(100, 500, 2)/100.0
        self.color = (random.randrange(0,256,1),random.randrange(0,256,1),random.randrange(0,256,1))

    def update(self, screen):
        self.rect.y += self.vy
        if self.rect.y > screen.get_height() + 10:
            self.reset()

    def reset(self):
        self.rect.y = random.randrange(-30, 0, 1)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self)