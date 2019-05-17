import pygame
from enum import Enum

class Animation:
    frame_sets = dict()

    def __init__(self, speed=5):
        self.animation_speed = speed
        self.time_from_last_frame = 0
        self.current_frame = 0
        self.current_frame_set = 0
        self.image = None

    @classmethod
    def add_frames(cls, path: str, count: int, key: Enum, size):
        size = (int(size[0]), int(size[1]))
        frames = []
        if count == 1:
            frames.append(pygame.transform.scale(
                pygame.image.load("../Textures/" + path + ".png"), size))
        else:
            for i in range(count):
                frames.append(pygame.transform.scale(
                    pygame.image.load("../Textures/" + path + "_" + str(i+1) + ".png"), size))

        if key in cls.frame_sets.keys():
            cls.frame_sets.update({key: cls.frame_sets[key] + frames})
        else:
            cls.frame_sets.update({key: frames})
            # if cls.image is None:
            #     cls.image = cls.frame_sets[key][0]

    def set_frame_set(self, key: Enum):
        self.current_frame_set = key
        self.current_frame = 0
        self.image = self.current_img()

    def current_img(self):
        if self.current_frame_set in self.frame_sets.keys():
            return self.frame_sets[self.current_frame_set][self.current_frame]
        else:
            return None

    def animate_circular(self):
        self.time_from_last_frame += 1
        if self.time_from_last_frame >= self.animation_speed:
            self.time_from_last_frame = 0
            self.current_frame = (self.current_frame + 1) % len(self.frame_sets[self.current_frame_set])
            self.image = self.current_img()

    def animate_serial(self):
        self.time_from_last_frame += 1
        if self.time_from_last_frame >= self.animation_speed and \
                self.current_frame < len(self.frame_sets[self.current_frame_set])-1:
            self.time_from_last_frame = 0
            self.current_frame += 1
            self.image = self.current_img()
        return self.time_from_last_frame >= self.animation_speed

    #
    # def draw(self, screen: pygame.Surface, dest):
    #     screen.blit(self.frames[self.current_frame], (dest[0]-self.size[0]/2, dest[1]-self.size[1]/2))
