import sys
import pygame
from Main.button import Button
from Main.star import Star
from Main.Engine import Engine
from Main.animation import Animation

class Menu:
    buttons = []

    def __init__(self, screen: pygame.Surface, title):
        self.width = screen.get_width()
        self.height = screen.get_height()
        self.buttons.append(Button(pygame.Rect(self.width/2 - 220, self.height/4, 200, 100), "Single player mode"))
        self.buttons.append(Button(pygame.Rect(self.width/2 + 20, self.height/4, 200, 100), "Multiplayer mode"))
        self.screen = screen
        self.stars = [Star(screen) for x in range(200)]
        self.menu_font = pygame.font.SysFont(None, 40)
        self.menu_title = self.menu_font.render(title, True, (255, 255, 255))
        self.menu_title_dest = (self.screen.get_width() / 2 - self.menu_title.get_size()[0] / 2,
                                100 - self.menu_title.get_size()[1] / 2)

    def run(self):
        clock = pygame.time.Clock()
        while True:
            clock.tick(60)
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

                        engine = Engine(self.screen)
                        if b.text == "Single player mode":
                            game_result = engine.run_single()
                            #self.buttons.append(Button(pygame.Rect(self.screen.get_width() / 2 - pygame.Rect(self.screen.get_width()/ 6, self.screen.get_height() / 2, 200, 100), "Single player mode"))
                           ## self.buttons.append(Button(pygame.Rect(self.screen.get_width()) / 2, self.screen.get_height() / 2, 200, 100), "Wynik"))
                            print(game_result)
                            end_game_message = "You score " + game_result.__str__() + " points"
                            if self.buttons.__len__() > 2:
                                self.buttons.pop()
                            self.buttons.append(Button(pygame.Rect(self.width/2 - 200,self.height/2,400,100),end_game_message))
                            self.buttons[2].set_quasi_button()
                            ##if self.buttons.__len__() > 2:
                             ##  pass
                        elif b.text == "Multiplayer mode":
                            engine.run_multi()
                else:
                    b.unhighlight()
                b.draw(self.screen)

            pygame.display.flip()
