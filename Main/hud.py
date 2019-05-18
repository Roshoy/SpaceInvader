import pygame


class PlayerHud(pygame.sprite.DirtySprite):
    rocket_icon = pygame.image.load("../Textures/rocket.png")
    def __init__(self, size, max_life, rockets):
        super().__init__()
        self.image = pygame.Surface(size, pygame.SRCALPHA, 32)
        self.rect = ((0, 0), size)
        self.anything_changed = True
        # POINTS
        self.points = 0
        self.points_color = (40, 40, 255)
        self.points_font = pygame.font.SysFont(None, 45, False, True)
        self.points_text = self.points_font.render(str(self.points), True, self.points_color)
        ###
        # LIFE
        self.life = max_life
        max_life_color = (255, 20, 20)
        max_life_font = pygame.font.SysFont(None, 45, True, True)
        self.max_life_text = max_life_font.render(str(max_life), True, max_life_color)
        self.life_color = max_life_color  # (max_life_color[0], max_life_color[1], max_life_color[2])
        self.life_font = pygame.font.SysFont(None, 40, False, True)
        self.life_text = self.life_font.render(str(max_life)+" / ", True, self.life_color)
        ###
        # ROCKETS
        self.rockets = rockets
        self.rocket_font = pygame.font.SysFont(None, 40, False, True)

        self.rocket_font = self.life_font
        self.rocket_text = self.rocket_font.render(str(rockets), True, self.points_color)
        self.rocket_icon = pygame.transform.scale(self.rocket_icon,
                                                  (int(self.rocket_text.get_height() * self.rocket_icon.get_width() /
                                                   self.rocket_icon.get_height()), self.rocket_text.get_height()))

    def update(self, points, life, rockets):

        if points != self.points:
            self.anything_changed = True
            self.points_text = self.points_font.render(str(points), True, self.points_color)
        if life != self.life:
            self.anything_changed = True
            self.life_text = self.life_font.render(str(life) + " / ", True, self.life_color)
        if rockets != self.rockets:
            self.anything_changed = True
            self.rocket_text = self.rocket_font.render(str(rockets), True, self.points_color)

        if self.anything_changed:
            self.anything_changed = False
            self.image.fill((0, 0, 0, 0))
            self.image.blit(self.points_text, (self.image.get_width() / 20, self.image.get_height() / 20))
            life_dest = (self.image.get_width() / 20, self.image.get_height() * 19 / 20 - self.life_text.get_height())
            self.image.blit(self.life_text, life_dest)
            max_life_dest = (life_dest[0] + self.life_text.get_width(), life_dest[1])
            self.image.blit(self.max_life_text, max_life_dest)
            rocket_dest = (life_dest[0], life_dest[1] - 8 - self.rocket_text.get_height())
            self.image.blit(self.rocket_text, rocket_dest)
            rocket_icon_dest = (life_dest[0] - 16 - self.rocket_icon.get_width(),
                                int(rocket_dest[1] + self.rocket_text.get_height()/2 - self.rocket_icon.get_height()/2))
            self.image.blit(self.rocket_icon, rocket_icon_dest)


    # def draw(self, screen: pygame.Surface):
    #     screen.blit(self.points_text, (screen.get_width()/20, screen.get_height()/20))
    #     screen.blit(self.life_text, (screen.get_width()/20,
    #                                  screen.get_height() * 19 / 20 - self.life_text.get_height()))
    #     screen.blit(self.max_life_text, (screen.get_width() / 20 + self.life_text.get_width(),
    #                                      screen.get_height() * 19 / 20 - self.life_text.get_height()))