import pygame
import sys
from Main.menu import Menu
from Main.Engine import Engine
from Main.star import Star
from enum import Enum


class Game:
    class GameState(Enum):
        SINGLE_ON = 0
        MULTI_ON = 1
        SINGLE_INIT = 2
        MULTI_INIT = 3
        MAIN_M = 4
        GAMEOVER_M = 5
        PAUSE_M = 6

    def __init__(self):
        pygame.mixer.music.load('../Sounds/battle.wav')
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.1)
        self.screen = pygame.display.set_mode((1000, 800))  # , pygame.FULLSCREEN)
        self.clock = pygame.time.Clock()
        self.stars = [Star(self.screen) for x in range(300)]
        self.engine = Engine(self.screen, self.stars, self.clock)

        self.main_menu = Menu(self.screen, "Space Invaders Deluxe", self.stars, self.clock)
        self.gameover_menu = Menu(self.screen, "Game Over", self.stars, self.clock)
        self.pause_menu = Menu(self.screen, "Pause", self.stars, self.clock)
        self.points = 0
        self.game_state = self.GameState.MAIN_M
        width = self.screen.get_width()
        self.main_menu.add_button(pygame.Rect(width/2 - 100, 0, 200, 80), "Single player")
        self.main_menu.add_button(pygame.Rect(width/2 - 100, 0, 200, 80), "Multiplayer")
        self.main_menu.add_button(pygame.Rect(width/2 - 100, 0, 200, 80), "Exit")

        self.gameover_menu.add_subtitle(" ")
        self.gameover_menu.add_subtitle(" ")

        self.gameover_menu.add_button(pygame.Rect(width / 2 - 100, 0, 200, 80), "Try Again")
        self.gameover_menu.add_button(pygame.Rect(width / 2 - 100, 0, 200, 80), "Main menu")

        self.pause_menu.add_button(pygame.Rect(width/2 - 100, 0, 200, 80), "Continue")
        self.pause_menu.add_button(pygame.Rect(width/2 - 100, 0, 200, 80), "Main menu")

    def set_gameover_menu_title(self):
        if isinstance(self.points, tuple):
            self.gameover_menu.set_subtitle_text(0, "Player1   " + str(self.points[0]))
            self.gameover_menu.set_subtitle_text(1, "Player2   "+str(self.points[1]))
        else:
            self.gameover_menu.set_subtitle_text(0, "Player1")
            self.gameover_menu.set_subtitle_text(1, str(self.points))

    def run(self):
        self.points = 0
        res = 0
        last_game_single = True
        while True:
            if self.game_state is self.GameState.SINGLE_INIT:
                last_game_single = True
                self.engine.init_single()
                self.game_state = self.GameState.SINGLE_ON
                res = self.engine.run_single()
                if res is -1:
                    self.game_state = self.GameState.PAUSE_M
                else:
                    self.points = res
                    self.game_state = self.GameState.GAMEOVER_M
            elif self.game_state is self.GameState.MULTI_INIT:
                last_game_single = False
                self.engine.init_multi()
                self.game_state = self.GameState.MULTI_ON
                res = self.engine.run_multi()
                if res is -1:
                    self.game_state = self.GameState.PAUSE_M
                else:
                    self.points = res
                    self.game_state = self.GameState.GAMEOVER_M
            elif self.game_state is self.GameState.SINGLE_ON:
                last_game_single = True
                res = self.engine.run_single()
                if res is -1:
                    self.game_state = self.GameState.PAUSE_M
                else:
                    self.points = res
                    self.game_state = self.GameState.GAMEOVER_M
            elif self.game_state is self.GameState.MULTI_ON:
                last_game_single = False
                res = self.engine.run_multi()
                if res is -1:
                    self.game_state = self.GameState.PAUSE_M
                else:
                    self.points = res
                    self.game_state = self.GameState.GAMEOVER_M
            elif self.game_state is self.GameState.MAIN_M:
                res = self.main_menu.run()
                if res == 0:
                    self.game_state = self.GameState.SINGLE_INIT
                elif res == 1:
                    self.game_state = self.GameState.MULTI_INIT
                elif res == 2 or res == -1:
                    sys.exit(0)
            elif self.game_state is self.GameState.GAMEOVER_M:
                self.set_gameover_menu_title()
                res = self.gameover_menu.run()
                if res == 0:
                    if last_game_single:
                        self.game_state = self.GameState.SINGLE_INIT
                    else:
                        self.game_state = self.GameState.MULTI_INIT
                elif res == 1 or res == -1:
                    self.game_state = self.GameState.MAIN_M

            elif self.game_state is self.GameState.PAUSE_M:
                res = self.pause_menu.run()
                if res == 0 or res == -1:
                    if last_game_single:
                        self.game_state = self.GameState.SINGLE_ON
                    else:
                        self.game_state = self.GameState.MULTI_ON
                elif res == 1:
                    self.game_state = self.GameState.MAIN_M