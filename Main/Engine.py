import sys
from Main.Player import *
from Main.enemy import Enemy
from Main.star import Star
from Main.rocket import Rocket
from Main.missile_wrapper import MissileWrapper
from Main.enemies_wrapper import EnemiesWrapper
from Main.simple_missiles import *
from Main.hud import PlayerHud


class Engine:
    
    
    def __init__(self, screen):
        self.screen = screen
        self.stars = [Star(screen) for x in range(300)]
        EnemyMissile.init()
        PlayerMissile.init()
        Rocket.init()
        Enemy.init()
        Player.init()
        SecondPlayer.init()
        self.clock = pygame.time.Clock()
        self.enemies_wrapper = None
        self.missile_wrapper = None
        self.player1 = None
        self.player2 = None
        self.huds = None
        self.player = None
        
    def player_prefab(self, t=1):
        if t == 1:
            return Player(pygame.Rect(0, 0, 40, 40), 9)
        else:
            return SecondPlayer(pygame.Rect(0, 0, 40, 40), 9)

    def init_single(self):
        player1 = self.player_prefab()
        buff = list(player1.controls)
        buff[4] = -1
        player1.controls = tuple(buff)
        self.enemies_wrapper = EnemiesWrapper(self.screen)

        player_hud = PlayerHud((self.screen.get_width(), self.screen.get_height()), player1.max_life,
                               player1.rockets_count)
        player_hud.align_right()
        self.huds = pygame.sprite.Group(player_hud)
        self.player = pygame.sprite.Group(player1)
        self.missile_wrapper = MissileWrapper()

    def run_single(self):
        self.init_single()
        while True:
            d_time = self.clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return -1

            if self.player.sprites()[0].shoot_trigger():
                self.missile_wrapper.add_from_player(self.player.sprites()[0].shoot())
            self.player.update(d_time, True)

            self.missile_wrapper.update(self.screen)

            self.enemies_wrapper.update(d_time, self.player, self.missile_wrapper)
            self.missile_wrapper.player_hit(self.player.sprites()[0])

            if self.player.sprites()[0].state is Player.State.DEAD:
                return self.player.sprites()[0].points
            self.huds.update(self.player.sprites()[0].points, self.player.sprites()[0].life,
                             self.player.sprites()[0].rockets_count)
            self.screen.fill((0, 0, 0))
            for s in self.stars:
                s.update(self.screen)
                s.draw(self.screen)
            self.enemies_wrapper.draw(self.screen)
            self.missile_wrapper.draw(self.screen)
            self.player.draw(self.screen)
            self.huds.draw(self.screen)
            pygame.display.flip()
        #pygame.mouse.set_visible(True)

    def init_multi(self):
        player1 = self.player_prefab()
        player2 = self.player_prefab(2)
        self.player = pygame.sprite.Group(player1, player2)

        player1_hud = PlayerHud((self.screen.get_width(), self.screen.get_height()), self.player.sprites()[0].max_life,
                                self.player.sprites()[0].rockets_count)
        player1_hud.align_right()
        player2_hud = PlayerHud((self.screen.get_width(), self.screen.get_height()), self.player.sprites()[1].max_life,
                                self.player.sprites()[1].rockets_count)

        self.huds = pygame.sprite.Group(player1_hud, player2_hud)

        self.enemies_wrapper = EnemiesWrapper(self.screen)

        self.missile_wrapper = MissileWrapper()

    def run_multi(self):
        self.init_multi()

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

            for p in self.player.sprites():
                if p.state is Player.State.DEAD:
                    self.player.remove(p)
                    if len(self.player.sprites()) == 0:
                        return self.huds.sprites()[0].points, self.huds.sprites()[1].points

            self.huds.sprites()[0].update(self.player.sprites()[0].points, self.player.sprites()[0].life,
                                          self.player.sprites()[0].rockets_count)
            if len(self.player.sprites()):
                self.huds.sprites()[1].update(self.player.sprites()[1].points, self.player.sprites()[1].life,
                                              self.player.sprites()[1].rockets_count)

            self.screen.fill((0, 0, 0))
            for s in self.stars:
                s.update(self.screen)
                s.draw(self.screen)
            self.enemies_wrapper.draw(self.screen)
            self.missile_wrapper.draw(self.screen)
            self.player.draw(self.screen)
            self.huds.draw(self.screen)
            pygame.display.flip()



