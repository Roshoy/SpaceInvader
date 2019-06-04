import sys
import pygame
from Main.button import Button


class Menu:

    def __init__(self, screen: pygame.Surface, title, stars, clock):
        self.clock = clock
        self.buttons = []
        self.screen = screen
        self.stars = stars
        self.subtitles = []
        self.subtitle_font = pygame.font.SysFont(None, 30)
        self.menu_font = pygame.font.SysFont(None, 40)
        self.menu_title = self.menu_font.render(title, True, (255, 255, 255))
        self.menu_title_dest = (self.screen.get_width() / 2 - self.menu_title.get_size()[0] / 2,
                                100 - self.menu_title.get_size()[1] / 2)

    def set_title(self, title: str):
        self.menu_title = self.menu_font.render(title, True, (255, 255, 255))
        self.menu_title_dest = (self.screen.get_width() / 2 - self.menu_title.get_size()[0] / 2,
                                100 - self.menu_title.get_size()[1] / 2)

    def update_buttons_pos(self, top):
        if len(self.buttons) == 0:
            return
        dy = top - self.buttons[0].top + 50
        for b in self.buttons:
            b.top += dy
            b.highlight()
            b.unhighlight()

    def add_subtitle(self, title: str):
        text = self.subtitle_font.render(title, True, (255, 255, 255))
        y = self.menu_title.get_size()[1] + self.menu_title_dest[1] + 10

        if len(self.subtitles) > 0:
            i = len(self.subtitles) - 1
            y = self.subtitles[i][0].get_size()[1] + self.subtitles[i][1][1] + 10
        dest = (self.screen.get_width() / 2 - text.get_size()[0] / 2, y)
        self.subtitles.append((text, dest))

    def set_subtitle_text(self, ind, title: str):
        text = self.subtitle_font.render(title, True, (255, 255, 255))
        dest = (self.screen.get_width() / 2 - text.get_size()[0] / 2, self.subtitles[ind][1][1])
        self.subtitles[ind] = (text, dest)
        i = len(self.subtitles) - 1
        y = self.subtitles[i][0].get_size()[1] + self.subtitles[i][1][1]
        self.update_buttons_pos(y)

    def add_button(self, rect: pygame.Rect, title: str):
        if len(self.buttons) > 0:
            i = len(self.buttons) - 1
            rect.top += self.buttons[i].size[1] + self.buttons[i].top + 50
        elif len(self.subtitles) > 0:
            i = len(self.subtitles) - 1
            rect.top = self.subtitles[i][0].get_size()[0] + self.subtitles[i][1][1] + 50
        else:
            rect.top += self.menu_title.get_size()[1] + self.menu_title_dest[1] + 50

        self.buttons.append(Button(rect, title))

    def delay(self, k):
        while True:
            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return -1

            if k < 0:
                return 0
            k -= 1

            self.screen.fill((0, 0, 0))
            for s in self.stars:
                s.update(self.screen)
                s.draw(self.screen)
            for s in self.subtitles:
                self.screen.blit(s[0], s[1])
            self.screen.blit(self.menu_title, self.menu_title_dest)
            for b in self.buttons:
                b.draw(self.screen)
            pygame.display.flip()

    def run(self):
        if self.delay(20) == -1:
            return -1

        while True:

            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return -1

            for x in range(len(self.buttons)):
                if self.buttons[x].collidepoint(pygame.mouse.get_pos()):
                    self.buttons[x].highlight()
                    (b1, b2, b3) = pygame.mouse.get_pressed()
                    if b1 | b2 | b3:
                        if self.buttons[x]:
                            return x
                else:
                    self.buttons[x].unhighlight()

            self.screen.fill((0, 0, 0))
            for s in self.stars:
                s.update(self.screen)
                s.draw(self.screen)

            self.screen.blit(self.menu_title, self.menu_title_dest)
            for s in self.subtitles:
                self.screen.blit(s[0], s[1])
            for b in self.buttons:
                b.draw(self.screen)
            pygame.display.flip()
