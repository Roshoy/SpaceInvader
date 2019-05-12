import pygame
from Main.vector import Vector
from Main.missile import Missile
from Main.spaceship import SpaceShip
from Main.animation import Animation
from Main.rocket import Rocket
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

    def __init__(self, rect, speed, controls=
                 (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_RETURN, pygame.K_BACKSPACE)):
        super().__init__(rect, speed)
        self.move_dir = Vector(0, 0)
        self.velocity = Vector(0, 0)
        self.precision = 5
        self.controls = controls
        self.forward_anim = Animation((self.size[0], self.size[1]*3/2))
        self.forward_anim.add_frames("player_forward", 2)
        self.turning_left_anim = Animation((self.size[0], self.size[1] * 3 / 2), 5)
        self.turning_left_anim.add_frames("player_left", 4)
        self.turning_right_anim = Animation((self.size[0], self.size[1] * 3 / 2), 5)
        self.turning_right_anim.add_frames("player_right", 4)
        self.explosion_anim = Animation((self.size[0], self.size[1]*3/2), 5)
        self.explosion_anim.add_frames("explosion", 5)
        self.left_anim = Animation((self.size[0], self.size[1]*3/2), 5)
        self.left_anim.add_frames("player_left_3", 1)
        self.left_anim.add_frames("player_left_4", 1)
        self.right_anim = Animation((self.size[0], self.size[1] * 3 / 2), 5)
        self.right_anim.add_frames("player_right_3", 1)
        self.right_anim.add_frames("player_right_4", 1)
        self.state = Player.State.FORWARD
        self.animation = self.forward_anim

    def missile_prefab(self):
        return Missile(pygame.Rect(self.center, self.missile_size), Vector(0, -1),
                       self.tag)

    def rocket_prefab(self):
        return Rocket(pygame.Rect(self.center, (12, 24)))

    def shoot(self):
        res = super().shoot()
        if res and (pygame.key.get_pressed()[self.controls[5]] or pygame.mouse.get_pressed()[2]):
            return self.rocket_prefab()
        return res

    def shoot_trigger(self):
        if self.controls[4] != -1 and pygame.key.get_pressed()[self.controls[4]]:
            return True
        elif self.controls[4] == -1 and (pygame.mouse.get_pressed()[0] or pygame.mouse.get_pressed()[2]):
            return True
        return False

    def set_state(self, new_state):
        self.state = new_state
        if self.state is self.State.FORWARD:
            self.animation = self.forward_anim
        elif self.state is self.State.EXPLODING:
            self.animation = self.explosion_anim
        elif self.state is self.State.TURNLEFT:
            self.animation = self.turning_left_anim
        elif self.state is self.State.TURNRIGHT:
            self.animation = self.turning_right_anim
        elif self.state is self.State.LEFT:
            self.animation = self.left_anim
        elif self.state is self.State.RIGHT:
            self.animation = self.right_anim

    def move_keyboard(self, screen):
        if self.move_dir[0] > 0:
            self.move_dir[0] -= 0.01
        elif self.move_dir[0] < 0:
            self.move_dir[0] += 0.01

        if self.move_dir[1] > 0:
            self.move_dir[1] -= 0.01
        elif self.move_dir[1] < 0:
            self.move_dir[1] += 0.01
#       RIGHT, LEFT, UP, DOWN
        if pygame.key.get_pressed()[self.controls[3]] and self.move_dir[0] < 1:
            self.move_dir[0] += 0.05
        if pygame.key.get_pressed()[self.controls[2]] and self.move_dir[0] > -1:
            self.move_dir[0] -= 0.05
        if pygame.key.get_pressed()[self.controls[0]] and self.move_dir[1] > -1:
            self.move_dir[1] -= 0.05
        if pygame.key.get_pressed()[self.controls[1]] and self.move_dir[1] < 1:
            self.move_dir[1] += 0.05

        if 0 > self.center[0] and self.move_dir[0] < 0:
            self.move_dir[0] = 0
        if self.center[0] > screen.get_width() and self.move_dir[0] > 0:
            self.move_dir[0] = 0
        if 0 > self.center[1] and self.move_dir[1] < 0:
            self.move_dir[1] = 0
        if self.center[1] > screen.get_height() and self.move_dir[1] > 0:
            self.move_dir[1] = 0

        self.velocity = self.move_dir * self.speed

    def move_mouse(self, mouse_pos):
        self.move_dir.v = [mouse_pos[i] - self.center[i] for i in range(2)]
        vel_magni = self.move_dir.magnitude()
        if vel_magni < self.precision:
            self.set_state(Player.State.FORWARD)
            self.velocity[0] = mouse_pos[0] - self.center[0]
            self.velocity[1] = mouse_pos[1] - self.center[1]
        else:
            self.move_dir = self.move_dir / vel_magni
            self.velocity = self.velocity + self.move_dir * self.speed * 2.0
            if self.velocity.magnitude() != 0:
                self.velocity = self.velocity.normalized() * self.speed

    def update(self, d_time):
        if abs(self.velocity[0]) > abs(self.velocity[1]):
            if self.velocity[0] < 0 and self.state is not self.State.LEFT:
                self.set_state(Player.State.TURNLEFT)
            elif self.velocity[0] > 0 and self.state is not self.State.RIGHT:
                self.set_state(Player.State.TURNRIGHT)
        else:
            self.set_state(Player.State.FORWARD)

        if self.state in (Player.State.FORWARD, Player.State.LEFT, Player.State.RIGHT):
            super().update(d_time)
            self.animation.animate_circular()
        elif self.state is Player.State.TURNLEFT or self.state is Player.State.TURNRIGHT:
            super().update(d_time)
            if self.animation.animate_serial():
                self.set_state(self.State(self.state.value + 4))
        elif self.state is Player.State.EXPLODING:
            self.animation.animate_serial()

    def update_keyboard(self, d_time, screen):
        # self.animation.animate_circular();
        self.update(d_time)
        self.move_keyboard(screen)

    def update_mouse(self, mouse_pos, d_time):
        self.update(d_time)
        self.move_mouse(mouse_pos)

    def draw(self, screen):
        self.animation.draw(screen, (self.center[0], self.top + self.size[1] * 3/4))
        #self.thruster_anim.draw(screen, (self.center[0],
        #    self.top+self.size[1] + self.thruster_anim.size[1]/2 ))
