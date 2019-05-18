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

    def player_prefab(self, t=1):
        if t == 1:
            return Player(pygame.Rect(0, 0, 40, 40), 9)
        else:
            return SecondPlayer(pygame.Rect(0, 0, 40, 40), 9)

    def run_single(self):
        player1 = self.player_prefab()
        buff = list(player1.controls)
        buff[4] = -1
        player1.controls = tuple(buff)
        enemies_wrapper = EnemiesWrapper(self.screen)

        player_hud = PlayerHud((self.screen.get_width(), self.screen.get_height()), player1.max_life,
                               player1.rockets_count)
        player_hud.align_right()
        huds = pygame.sprite.Group(player_hud)

        player = pygame.sprite.Group(player1)
        missile_wrapper = MissileWrapper()
        clock = pygame.time.Clock()
        while True:
            d_time = clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    sys.exit(0)

            if player1.shoot_trigger():
                missile_wrapper.add_from_player(player1.shoot())
            player.update(d_time, True)

            missile_wrapper.update(self.screen)

            enemies_wrapper.update(d_time, player, missile_wrapper)
            missile_wrapper.player_hit(player1)

            if player1.state is Player.State.DEAD:
                return
            huds.update(player1.points, player1.life, player1.rockets_count)
            self.screen.fill((0, 0, 0))
            for s in self.stars:
                s.update(self.screen)
                s.draw(self.screen)
            enemies_wrapper.draw(self.screen)
            missile_wrapper.draw(self.screen)
            player.draw(self.screen)
            huds.draw(self.screen)
            pygame.display.flip()
        #pygame.mouse.set_visible(True)

    def run_multi(self):

        player1 = self.player_prefab()
        player2 = self.player_prefab(2)
        players = pygame.sprite.Group(player1, player2)

        player1_hud = PlayerHud((self.screen.get_width(), self.screen.get_height()), player1.max_life,
                               player1.rockets_count)
        player1_hud.align_right()
        player2_hud = PlayerHud((self.screen.get_width(), self.screen.get_height()), player1.max_life,
                                player1.rockets_count)

        huds = pygame.sprite.Group(player1_hud, player2_hud)

        enemies_wrapper = EnemiesWrapper(self.screen)

        missile_wrapper = MissileWrapper()
        clock = pygame.time.Clock()
        while True:
            d_time = clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    sys.exit(0)

            if player1.shoot_trigger():
                missile_wrapper.add_from_player(player1.shoot())
            if player2.shoot_trigger():
                missile_wrapper.add_from_player(player2.shoot())
            players.update(d_time, False, self.screen)

            missile_wrapper.update(self.screen)
            enemies_wrapper.update(d_time, players, missile_wrapper)

            missile_wrapper.player_hit(player1)
            missile_wrapper.player_hit(player2)
            for p in players.sprites():
                if p.state is Player.State.DEAD:
                    players.remove(p)
                    if len(players.sprites()) == 0:
                        return

            player1_hud.update(player1.points, player1.life, player1.rockets_count)
            player2_hud.update(player2.points, player2.life, player2.rockets_count)

            self.screen.fill((0, 0, 0))
            for s in self.stars:
                s.update(self.screen)
                s.draw(self.screen)
            enemies_wrapper.draw(self.screen)
            missile_wrapper.draw(self.screen)
            players.draw(self.screen)
            huds.draw(self.screen)
            pygame.display.flip()



