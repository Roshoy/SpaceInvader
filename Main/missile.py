import pygame


class Missile(pygame.Rect):
    def __init__(self, rect, direction, texture_path):
        super().__init__(rect)
        self.speed = 7
        self.active = True
        self.color = (0, 255, 0)
        self.velocity = direction
        self.velocity = self.velocity * self.speed
        self.textures = []
        texture = pygame.image.load("../Textures/" + texture_path + "_missile2_1.png")
        self.textures.append(pygame.transform.scale(texture,
                                                    (self.size[0]+1,self.size[1]+1)))
        texture = pygame.image.load("../Textures/" + texture_path + "_missile2_2.png")
        self.textures.append(pygame.transform.scale(texture,
                                                    (self.size[0] + 1, self.size[1] + 1)))
        self.animation_speed = 10
        self.animation_time = 0
        self.current_texture = 0

    def animate(self):
        self.animation_time += 1
        if self.animation_time >= self.animation_speed:
            self.animation_time = 0
            self.current_texture = (self.current_texture + 1) % len(self.textures)

    def update(self, screen):
        self.animate()
        self.move_ip(self.velocity[0], self.velocity[1])
        if not (self.height + screen.get_height() > self.y > -self.height and
                self.width + screen.get_width() > self.x > -self.width):
            self.active = False
        return self.active

    def draw(self, screen):
        #pygame.draw.rect(screen, self.color, self)
        screen.blit(self.textures[self.current_texture], (self.left, self.top))
