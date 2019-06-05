import pygame
from Main.vector import Vector
from Main.simple_missiles import PlayerMissile
from Main.spaceship import SpaceShip
from Main.rocket import Rocket
from Main.missile import Missile
from Main.sound_manager import SoundManager

from enum import Enum


class Player(SpaceShip):

    class State(Enum):
        FORWARD = 0
        TURNLEFT = 1
        TURNRIGHT = 2
        EXPLODING = 3
        DEAD = 4
        LEFT = 5
        RIGHT = 6

    shot_interval = 200
    tag = "player"
    missile_size = (8, 24)
    max_life = 10
    stat_size = (40, 40)

    def __init__(self, rect, speed, controls=
            (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_LEFTBRACKET, pygame.K_RIGHTBRACKET)):
        super().__init__(rect, speed)
        # move_dir = Vector(0, 0)
        self.velocity = Vector(0, 0)
        self.precision = 5
        self.controls = controls
        self.acceleration = self.speed * 2.0
        self.state = None
        self.set_state(self.State.FORWARD)
        self.points = 0
        self.rockets_count = 5

    @classmethod
    def init(cls):
        cls.frame_sets = dict()
        cls.add_frames("player_forward", 2, cls.State.FORWARD, (cls.stat_size[0], cls.stat_size[1] * 3 / 2))
        cls.add_frames("player_left", 4, cls.State.TURNLEFT, (cls.stat_size[0], cls.stat_size[1] * 3 / 2))
        cls.add_frames("player_right", 4, cls.State.TURNRIGHT, (cls.stat_size[0], cls.stat_size[1] * 3 / 2))
        cls.add_frames("explosion", 5, cls.State.EXPLODING, (cls.stat_size[0] * 1.5, cls.stat_size[1] * 1.5))
        cls.add_frames("player_left_3", 1, cls.State.LEFT, (cls.stat_size[0], cls.stat_size[1] * 3 / 2))
        cls.add_frames("player_left_4", 1, cls.State.LEFT, (cls.stat_size[0], cls.stat_size[1] * 3 / 2))
        cls.add_frames("player_right_3", 1, cls.State.RIGHT, (cls.stat_size[0], cls.stat_size[1] * 3 / 2))
        cls.add_frames("player_right_4", 1, cls.State.RIGHT, (cls.stat_size[0], cls.stat_size[1] * 3 / 2))

    def missile_prefab(self):
        return PlayerMissile(self.rect.center, self, Vector(0, -1))

    def rocket_prefab(self):
        return Rocket(pygame.Rect(self.rect.center, (12, 24)), self)

    def shoot(self):
        res = super().shoot()
        if res and (pygame.key.get_pressed()[self.controls[5]] or pygame.mouse.get_pressed()[2]):
            if self.rockets_count > 0:
                self.rockets_count -= 1
                return self.rocket_prefab()
            else:
                return False
        if res:
            SoundManager.sound_laser_shot()
        return res

    def shoot_trigger(self):
        if self.controls[4] != -1 and \
                (pygame.key.get_pressed()[self.controls[4]] or pygame.key.get_pressed()[self.controls[5]]):
            return True
        elif self.controls[4] == -1 and (pygame.mouse.get_pressed()[0] or pygame.mouse.get_pressed()[2]):
            return True
        return False

    def set_state(self, new_state):
        if self.state is new_state:
            return
        self.state = new_state
        if self.state is not self.State.DEAD:
            self.set_frame_set(self.state)

    def get_hit(self, missile: Missile):
        left_hp = super().get_hit(missile)
        if left_hp == 0:
            SoundManager.sound_player_explosion()
        return left_hp

    def move_keyboard(self, screen):
        acc = self.acceleration / self.speed / 20
        move_dir = self.velocity / self.speed
        if move_dir[0] > 0:
            move_dir[0] -= acc / 3
        elif move_dir[0] < 0:
            move_dir[0] += acc / 3

        if move_dir[1] > 0:
            move_dir[1] -= acc / 3
        elif move_dir[1] < 0:
            move_dir[1] += acc / 3
#       RIGHT, LEFT, UP, DOWN
        if pygame.key.get_pressed()[self.controls[3]] and move_dir[0] < 1:
            move_dir[0] += acc
        if pygame.key.get_pressed()[self.controls[2]] and move_dir[0] > -1:
            move_dir[0] -= acc
        if pygame.key.get_pressed()[self.controls[0]] and move_dir[1] > -1:
            move_dir[1] -= acc
        if pygame.key.get_pressed()[self.controls[1]] and move_dir[1] < 1:
            move_dir[1] += acc

        if 0 > self.rect.center[0] and move_dir[0] < 0:
            move_dir[0] = 0
        if self.rect.center[0] > screen.get_width() and move_dir[0] > 0:
            move_dir[0] = 0
        if 0 > self.rect.center[1] and move_dir[1] < 0:
            move_dir[1] = 0
        if self.rect.center[1] > screen.get_height() and move_dir[1] > 0:
            move_dir[1] = 0

        if move_dir.magnitude() > 1:
            move_dir = move_dir.normalized()

        self.velocity = move_dir * self.speed

    def move_mouse(self, mouse_pos):
        move_dir = Vector(0, 0)
        move_dir.v = [mouse_pos[i] - self.rect.center[i] for i in range(2)]
        vel_magni = move_dir.magnitude()
        if vel_magni < self.precision:
            self.set_state(Player.State.FORWARD)
            self.velocity[0] = mouse_pos[0] - self.rect.center[0]
            self.velocity[1] = mouse_pos[1] - self.rect.center[1]
        else:
            move_dir = move_dir / vel_magni
            self.velocity = self.velocity + move_dir * self.acceleration
            if self.velocity.magnitude() != 0:
                self.velocity = self.velocity.normalized() * self.speed

    def update(self, d_time, with_mouse: bool, screen: pygame.Surface = None):
        if self.state is Player.State.EXPLODING:
            if self.animate_serial():
                self.set_state(self.state.DEAD)
            return False
        elif self.velocity.magnitude() > 0.1 and abs(self.velocity[0]) > abs(self.velocity[1]):
            if self.velocity[0] < 0 and self.state is not self.State.LEFT:
                self.set_state(Player.State.TURNLEFT)
            elif self.velocity[0] > 0 and self.state is not self.State.RIGHT:
                self.set_state(Player.State.TURNRIGHT)
        else:
            self.set_state(Player.State.FORWARD)
        super().update(d_time)
        if self.state in (Player.State.FORWARD, Player.State.LEFT, Player.State.RIGHT):
            self.animate_circular()
        elif self.state is Player.State.TURNLEFT or self.state is Player.State.TURNRIGHT:
            if self.animate_serial():
                self.set_state(self.State(self.state.value + 4))

        if with_mouse:
            self.move_mouse(pygame.mouse.get_pos())
        else:
            self.move_keyboard(screen)
        return True
    #
    # def draw(self, screen):
    #     self.animation.draw(screen, (self.center[0], self.top + self.size[1] * 3/4))


class SecondPlayer(Player):

    def __init__(self, rect, speed, controls=
                 (pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d, pygame.K_1, pygame.K_BACKQUOTE)):
        super().__init__(rect, speed, controls)

    @classmethod
    def init(cls):
        super().init()
        temp = pygame.image.load("./Textures/color_template.png")
        arr = pygame.PixelArray(temp)
        for key_set in cls.frame_sets.keys():
            for s in range(len(cls.frame_sets[key_set])):
                pixel_array = pygame.PixelArray(cls.frame_sets[key_set][s])

                for i in range(temp.get_size()[1]):
                    pixel_array.replace(temp.unmap_rgb(arr[0][i]), temp.unmap_rgb(arr[1][i]))
                cls.frame_sets[key_set][s] = pixel_array.make_surface()
