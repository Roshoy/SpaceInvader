import pygame


class PlayerHud(pygame.sprite.DirtySprite):
    rocket_icon = pygame.image.load("../Textures/rocket.png")
    health_icon = pygame.image.load("../Textures/health.png")

    def __init__(self, size, max_life, rockets, points_color):
        super().__init__()
        self.image = pygame.Surface(size, pygame.SRCALPHA, 32)
        self.rect = ((0, 0), size)
        self.anything_changed = True

        self.points_dest = (0, 0)
        self.life_dest = (0, 0)
        self.max_life_dest = (0, 0)
        self.rocket_dest = (0, 0)
        self.rocket_icon_dest = (0, 0)
        self.health_icon_dest = (0, 0)

        # POINTS
        self.points = 0
        self.points_color = points_color
        self.points_font = pygame.font.SysFont(None, 45, False, True)
        self.points_text = self.points_font.render('{:10d}'.format(self.points), True, self.points_color)
        ###
        # LIFE
        self.life = max_life
        self.life_len = len(str(max_life))
        max_life_color = (255, 20, 20)
        max_life_font = pygame.font.SysFont(None, 45, False, True)
        self.max_life_text = max_life_font.render(str(max_life), True, points_color)
        self.life_color = max_life_color  # (max_life_color[0], max_life_color[1], max_life_color[2])
        self.life_font = pygame.font.SysFont(None, 40, False, True)
        self.life_text = self.life_font.render(str(max_life)+" / ", True, points_color)

        ###
        # ROCKETS
        self.rocket_color = (90, 90, 90)
        self.rockets = rockets
        self.rocket_font = pygame.font.SysFont(None, 40, False, True)
        self.rocket_font = self.life_font
        self.rocket_text = self.rocket_font.render(str(rockets), True, points_color)
        self.rocket_icon = pygame.transform.scale(self.rocket_icon,
                                                  (int(self.rocket_text.get_height() * self.rocket_icon.get_width() /
                                                   self.rocket_icon.get_height()), self.rocket_text.get_height()))
        self.health_icon = pygame.transform.scale2x(self.health_icon)
        self.align_left()

    def align_left(self):
        self.points_dest = (self.image.get_width() / 20, self.image.get_height() / 20)
        self.life_dest = (self.image.get_width() / 20, self.image.get_height() * 19 / 20 - self.life_text.get_height())
        self.max_life_dest = (self.life_dest[0] + self.life_text.get_width(), self.life_dest[1])
        self.rocket_dest = (self.life_dest[0], self.life_dest[1] - 8 - self.rocket_text.get_height())
        self.rocket_icon_dest = (self.life_dest[0] - 16 - self.rocket_icon.get_width(),
                                 int(self.rocket_dest[1] + self.rocket_text.get_height()/2 -
                                     self.rocket_icon.get_height()/2))
        self.health_icon_dest = (self.life_dest[0] - 16 - self.health_icon.get_width(),
                                 int(self.life_dest[1] + self.max_life_text.get_height()/2 -
                                     self.health_icon.get_height()/2))

    def align_right(self):
        self.points_dest = (self.image.get_width() * 19 / 20 - self.points_text.get_width(),
                            self.image.get_height() / 20)
        self.life_dest = (self.image.get_width() * 19 / 20 - self.life_text.get_width() - self.max_life_text.get_width()
                          , self.image.get_height() * 19 / 20 - self.life_text.get_height())
        self.max_life_dest = (self.life_dest[0] + self.life_text.get_width(), self.life_dest[1])
        self.rocket_dest = (self.image.get_width() * 19 / 20 - self.rocket_text.get_width(),
                            self.life_dest[1] - 8 - self.rocket_text.get_height())
        self.rocket_icon_dest = (self.image.get_width() * 19 / 20 + 16,
                                 int(self.rocket_dest[1] + self.rocket_text.get_height() / 2 -
                                     self.rocket_icon.get_height() / 2))
        self.health_icon_dest = (self.image.get_width() * 19 / 20 + 16,
                                 int(self.life_dest[1] + self.max_life_text.get_height() / 2 -
                                     self.health_icon.get_height() / 2))

    def update(self, points, life, rockets):
        if points != self.points:
            self.points = points
            self.anything_changed = True
            self.points_text = self.points_font.render('{:10d}'.format(self.points), True, self.points_color)
        if life != self.life:
            self.life = life
            self.anything_changed = True
            self.life_text = self.life_font.render(('{:'+str(self.life_len)+'d}').format(life) +
                                                   " / ", True, self.points_color)
        if rockets != self.rockets:
            self.rockets = rockets
            self.anything_changed = True
            self.rocket_text = self.rocket_font.render(str(rockets), True, self.points_color)

        if self.anything_changed:
            self.anything_changed = False
            self.image.fill((0, 0, 0, 0))
            self.image.blit(self.points_text, self.points_dest)
            self.image.blit(self.life_text, self.life_dest)
            self.image.blit(self.max_life_text, self.max_life_dest)
            self.image.blit(self.rocket_text, self.rocket_dest)
            self.image.blit(self.rocket_icon, self.rocket_icon_dest)
            self.image.blit(self.health_icon, self.health_icon_dest)
