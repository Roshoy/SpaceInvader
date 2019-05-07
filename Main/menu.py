import sys
import pygame
from Main.button import Button
from Main.star import Star
from Main.Engine import Engine


class Menu:
    buttons = []

    def __init__(self, screen, title):
        self.buttons.append(Button(pygame.Rect(400, 200, 200, 100), "Single player mode"))
        self.buttons.append(Button(pygame.Rect(200, 200, 200, 100), "Multiplayer mode"))
        self.screen = screen
        self.stars = [Star(screen) for x in range(200)]
        self.menu_font = pygame.font.SysFont(None, 40)
        self.menu_title = self.menu_font.render(title, True, (255, 255, 255))
        self.menu_title_dest = (self.screen.get_width() / 2  - self.menu_title.get_size()[0] / 2,
                                100 - self.menu_title.get_size()[1] / 2)

    def run(self):

        while True:
            pygame.time.Clock().tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    sys.exit(0)

            self.screen.fill((0, 0, 0))
            for s in self.stars:
                s.update(self.screen)
                s.draw(self.screen)

            self.screen.blit(self.menu_title, self.menu_title_dest)

            for b in self.buttons:
                if b.collidepoint(pygame.mouse.get_pos()):
                    b.highlight()
                    (b1, b2, b3) = pygame.mouse.get_pressed()
                    if b1 | b2 | b3:
                        #screen = pygame.display.set_mode((800, 600))
                        engine = Engine(self.screen)
                        if b.text == "Single player mode":
                            engine.run_single()
                        else:
                            engine.run_multi()
                else:
                    b.unhighlight()
                b.draw(self.screen)
            pygame.display.flip()
