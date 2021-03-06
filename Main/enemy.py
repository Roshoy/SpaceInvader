
import random
from Main.simple_missiles import EnemyMissile
from Main.spaceship import SpaceShip
from enum import Enum
from Main.vector import Vector


class Enemy(SpaceShip):

    class State(Enum):
        ALIVE = 0
        EXPLODING = 1
        DEAD = 2

    points = 100

    tag = "enemy"
    missile_size = (16, 16)
    stat_size = (30, 30)

    def __init__(self, rect, speed=5):
        super().__init__(rect, speed)
        self.restraining = random.randrange(100, 200, 1)
        self.acceleration = self.speed / 18.0
        self.state = None
        self.set_state(self.State.ALIVE)

    @classmethod
    def init(cls):
        cls.frame_sets = dict()
        cls.add_frames(cls.tag, 1, cls.State.ALIVE, cls.stat_size)
        cls.add_frames("explosion", 5, cls.State.EXPLODING, tuple([int(i * 1.5) for i in cls.stat_size]))

    def missile_prefab(self):
        return EnemyMissile(self.rect.center, self.velocity.normalized())

    def move_auto(self, player_pos):
        move_dir = Vector(0, 0)
        move_dir.v = [player_pos[i] - self.rect.center[i] for i in range(len(player_pos))]
        vel_magni = move_dir.magnitude()
        if vel_magni > self.restraining:
            move_dir = move_dir.normalized()
            self.velocity = self.velocity + move_dir * self.acceleration
        vel_magni = self.velocity.magnitude()
        if vel_magni != 0:
            self.velocity = self.velocity * self.speed / vel_magni

    def set_state(self, new_state):
        if self.state is new_state:
            return
        self.state = new_state
        if self.state is not self.State.DEAD:
            self.set_frame_set(self.state)

    def update(self, d_time, player_pos):
        if self.state is self.state.ALIVE:
            self.move_auto(player_pos)
            super().update(d_time)
            self.animate_circular()
        elif self.state is self.state.EXPLODING:
            if self.animate_serial():
                self.set_state(self.State.DEAD)
