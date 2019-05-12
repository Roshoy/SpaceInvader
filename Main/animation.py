import pygame


class Animation:
    def __init__(self, size, speed = 5):
        self.size = (int(size[0]), int(size[1]))
        self.speed = speed
        self.time_from_last_frame = 0
        self.current_frame = 0
        self.frames = []

    def add_frames(self, path: str, count: int):
        if count == 1:
            self.frames.append(pygame.transform.scale(
                pygame.image.load("../Textures/" + path + ".png"), self.size))
            return
        for i in range(count):
            self.frames.append(pygame.transform.scale(
                pygame.image.load("../Textures/" + path + "_" + str(i+1) + ".png"), self.size))

    def animate_circular(self):
        self.time_from_last_frame += 1
        if self.time_from_last_frame >= self.speed:
            self.time_from_last_frame = 0
            self.current_frame = (self.current_frame + 1) % len(self.frames)

    def animate_serial(self):
        self.time_from_last_frame += 1
        if self.time_from_last_frame >= self.speed and \
                self.current_frame < len(self.frames)-1:
            self.time_from_last_frame = 0
            self.current_frame += 1
        return self.time_from_last_frame >= self.speed

    def draw(self, screen: pygame.Surface, dest):
        screen.blit(self.frames[self.current_frame], (dest[0]-self.size[0]/2, dest[1]-self.size[1]/2))
