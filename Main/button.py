import pygame


class Button(pygame.Rect):
    def __init__(self, rect, text):
        super().__init__(rect)
        self.highlighted = False
        self.background_color = (255, 255, 255, 0)
        self.highlight_alpha = 40
        self.background = pygame.Surface(self.size)
        self.background.set_alpha(self.background_color[3])
        self.background.fill(self.background_color)
        self.font = pygame.font.SysFont(None, 25)
        self.highlighted_font = pygame.font.SysFont(None, 30)
        self.text = text
        self.set_state(self.background_color[3], self.font)
        self.quasi_button = 0

    def set_state(self, alpha, font):
        self.background.set_alpha(alpha)
        self.context = font.render(self.text, True, (255, 255, 255))
        self.dest = (self.center[0] - self.context.get_size()[0] / 2, self.center[1] - self.context.get_size()[1] / 2)

    def set_quasi_button(self):
        self.quasi_button = 1

    def highlight(self):
        if self.quasi_button:
            return
        if self.highlighted:
            return
        self.highlighted = True
        self.set_state(self.highlight_alpha, self.highlighted_font)

    def unhighlight(self):
        if not self.highlighted:
            return
        self.highlighted = False
        self.set_state(self.background_color[3], self.font)

    def draw(self, screen):
        screen.blit(self.background, self.topleft)
        screen.blit(self.context, self.dest)
