import sys
from Main.Player import *
from Main.enemy import Enemy
from Main.rocket import Rocket
from Main.missile_wrapper import MissileWrapper
from Main.enemies_wrapper import EnemiesWrapper
from Main.simple_missiles import *
from Main.hud import PlayerHud


class Engine:
    def __init__(self, screen, stars, clock):
        self.screen = screen
        self.stars = stars
        EnemyMissile.init()
        PlayerMissile.init()
        Rocket.init()
        Enemy.init()
        Player.init()
        SecondPlayer.init()
        self.clock = clock
        self.enemies_wrapper = None
        self.missile_wrapper = None
        self.player1 = None
        self.player2 = None
        self.huds = None
        self.player = None
        self.player1 = None
        self.player2 = None
        
    def player_prefab(self, t=1):
        if t == 1:
            return Player(pygame.Rect(self.screen.get_width()/2 + 80, self.screen.get_height() - 60, 40, 40), 9)
        else:
            return SecondPlayer(pygame.Rect(self.screen.get_width()/2 - 80, self.screen.get_height() - 65, 40, 40), 9)

    def draw(self): # self.screen.fill((0, 0, 0)) needs to be called before

        for s in self.stars:
            s.update(self.screen)
            s.draw(self.screen)
        self.enemies_wrapper.draw(self.screen)
        self.missile_wrapper.draw(self.screen)
        self.player.draw(self.screen)
        self.huds.draw(self.screen)
        pygame.display.flip()

    def delay(self, sec: int):
        counter_font = pygame.font.SysFont(None, 40, False, True)
        sec *= 1000  # to milliseconds
        first_frame = True
        while sec > 0:
            print("Seconds: " + str(sec))
            d_time = self.clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return -1
            text = counter_font.render(str(sec//1000), True, (255, 255, 255))
            sec -= d_time
            self.screen.fill((0, 0, 0))
            self.screen.blit(text, (self.screen.get_width()/2 - text.get_size()[0]/2,
                                    self.screen.get_height()/2 - text.get_size()[1]/2))
            self.draw()
        return 0

    def init_single(self):
        self.player1 = self.player_prefab()
        buff = list(self.player1.controls)
        buff[4] = -1
        self.player1.controls = tuple(buff)
        self.enemies_wrapper = EnemiesWrapper(self.screen)

        player_hud = PlayerHud((self.screen.get_width(), self.screen.get_height()), self.player1.max_life,
                               self.player1.rockets_count, (255, 0, 0))
        player_hud.align_right()
        self.huds = pygame.sprite.Group(player_hud)
        self.player = pygame.sprite.Group(self.player1)
        self.missile_wrapper = MissileWrapper()

    def run_single(self):
        self.huds.update(self.player1.points, self.player1.life,
                         self.player1.rockets_count)
        if self.delay(4) == -1:
            return -1

        while True:
            d_time = self.clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return -1

            if self.player.sprites()[0].shoot_trigger():
                self.missile_wrapper.add_from_player(self.player1.shoot())
            self.player.update(d_time, True)

            self.missile_wrapper.update(self.screen)

            self.enemies_wrapper.update(d_time, self.player, self.missile_wrapper)
            self.missile_wrapper.player_hit(self.player1)

            if self.player1.state is Player.State.DEAD:
                return self.player1.points
            self.huds.update(self.player1.points, self.player1.life,
                             self.player1.rockets_count)
            self.screen.fill((0, 0, 0))
            self.draw()
        #pygame.mouse.set_visible(True)

    def init_multi(self):
        self.player1 = self.player_prefab()
        self.player2 = self.player_prefab(2)
        self.player = pygame.sprite.Group(self.player1, self.player2)

        player1_hud = PlayerHud((self.screen.get_width(), self.screen.get_height()), self.player1.max_life,
                                self.player1.rockets_count, (255, 0, 0))
        player1_hud.align_right()
        player2_hud = PlayerHud((self.screen.get_width(), self.screen.get_height()), self.player2.max_life,
                                self.player2.rockets_count, (0, 255, 255))

        self.huds = pygame.sprite.Group(player1_hud, player2_hud)

        self.enemies_wrapper = EnemiesWrapper(self.screen)

        self.missile_wrapper = MissileWrapper()

    def run_multi(self):
        if self.player1.state is not Player.State.DEAD:
            self.huds.sprites()[0].update(self.player1.points, self.player1.life,
                                          self.player1.rockets_count)
        if self.player2.state is not Player.State.DEAD:
            self.huds.sprites()[1].update(self.player2.points, self.player2.life,
                                          self.player2.rockets_count)
        if self.delay(4) == -1:
            return -1

        while True:
            d_time = self.clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return -1

            for p in self.player.sprites():
                if p.shoot_trigger():
                    self.missile_wrapper.add_from_player(p.shoot())

            self.player.update(d_time, False, self.screen)

            self.missile_wrapper.update(self.screen)
            self.enemies_wrapper.update(d_time, self.player, self.missile_wrapper)
            for p in self.player.sprites():
                self.missile_wrapper.player_hit(p)

            if self.player1.state is not Player.State.DEAD:
                self.huds.sprites()[0].update(self.player1.points, self.player1.life,
                                              self.player1.rockets_count)
            if self.player2.state is not Player.State.DEAD:
                self.huds.sprites()[1].update(self.player2.points, self.player2.life,
                                              self.player2.rockets_count)

            for p in self.player.sprites():
                if p.state is Player.State.DEAD:
                    self.player.remove(p)
                    if len(self.player.sprites()) == 0:
                        return self.player1.points, self.player2.points
            self.screen.fill((0, 0, 0))
            self.draw()



