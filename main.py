import pygame
from Main.game import Game
from Main.sound_manager import SoundManager

pygame.mixer.pre_init(44100, -16, 8, 1024)
pygame.mixer.init()
pygame.init()

sound_manager = SoundManager()
game = Game()
game.run()
pygame.quit()
#
# import pygame
#
# pygame.init()
#
#
# class TextBox(pygame.sprite.Sprite):
#     validChars = "`1234567890-=qwertyuiop[]\\asdfghjkl;'zxcvbnm,./"
#     shiftChars = '~!@#$%^&*()_+QWERTYUIOP{}|ASDFGHJKL:"ZXCVBNM<>?'
#
#     def __init__(self):
#         pygame.sprite.Sprite.__init__(self)
#         self.text = ""
#         self.font = pygame.font.Font(None, 50)
#         self.image = self.font.render("Enter your name", False, [255, 255, 255])
#         self.rect = self.image.get_rect()
#
#     def add_chr(self, char):
#         global shiftDown
#         if char in self.validChars and not shiftDown:
#             self.text += char
#         elif char in self.validChars and shiftDown:
#             self.text += self.shiftChars[self.validChars.index(char)]
#         self.update()
#
#     def update(self):
#         old_rect_pos = self.rect.center
#         self.image = self.font.render(self.text, False, [255, 255, 255])
#         self.rect = self.image.get_rect()
#         self.rect.center = old_rect_pos
#
#
# screen = pygame.display.set_mode([640, 480])
# textBox = TextBox()
# shiftDown = False
# textBox.rect.center = [320, 240]
#
# running = True
# while running:
#     screen.fill([255, 255, 255])
#     screen.blit(textBox.image, textBox.rect)
#     pygame.display.flip()
#     for e in pygame.event.get():
#         if e.type == pygame.QUIT:
#             running = False
#         if e.type == pygame.KEYUP:
#             if e.key in [pygame.K_RSHIFT, pygame.K_LSHIFT]:
#                 shiftDown = False
#         if e.type == pygame.KEYDOWN:
#             textBox.add_chr(pygame.key.name(e.key))
#             if e.key == pygame.K_SPACE:
#                 textBox.text += " "
#                 textBox.update()
#             if e.key in [pygame.K_RSHIFT, pygame.K_LSHIFT]:
#                 shiftDown = True
#             if e.key == pygame.K_BACKSPACE:
#                 textBox.text = textBox.text[:-1]
#                 textBox.update()
#             if e.key == pygame.K_RETURN:
#                 if len(textBox.text) > 0:
#                     print(textBox.text)
#                     running = False
# pygame.quit()
