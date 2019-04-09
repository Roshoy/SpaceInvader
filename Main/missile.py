import pygame


class Missile(pygame.Rect):
    def __init__(self, rect, direction):
        super().__init__(rect)
        self.speed = 7
        self.active = True
        self.color = (0, 255, 0)
        self.velocity = direction
        self.velocity = self.velocity * self.speed

    def update(self, screen):
        self.move_ip(self.velocity[0], self.velocity[1])
        if not (self.height + screen.get_height() > self.y > -self.height and
                self.width + screen.get_width() > self.x > -self.width):
            self.active = False
        return self.active

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self)
