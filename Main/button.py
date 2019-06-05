import pygame


class TextBox(pygame.sprite.Sprite):
    validChars = "`1234567890-=qwertyuiop[]\\asdfghjkl;'zxcvbnm,./"
    shiftChars = '~!@#$%^&*()_+QWERTYUIOP{}|ASDFGHJKL:"ZXCVBNM<>?'

    def __init__(self, font_size):
        pygame.sprite.Sprite.__init__(self)
        self.text = ""
        self.font = pygame.font.Font(None, font_size)
        self.image = self.font.render("Enter your name", False, [255, 255, 255])
        self.rect = self.image.get_rect()

    def add_chr(self, char, shift_down):
        if char in self.validChars and not shift_down:
            self.text += char
        elif char in self.validChars and shift_down:
            self.text += self.shiftChars[self.validChars.index(char)]
        self.update()

    def update(self):
        old_rect_pos = self.rect.center
        self.image = self.font.render(self.text, False, [255, 255, 255])
        self.rect = self.image.get_rect()
        self.rect.center = old_rect_pos

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

    def set_state(self, alpha, font):
        self.background.set_alpha(alpha)
        self.context = font.render(self.text, True, (255, 255, 255))
        self.dest = (self.center[0] - self.context.get_size()[0] / 2, self.center[1] - self.context.get_size()[1] / 2)

    def highlight(self):
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
