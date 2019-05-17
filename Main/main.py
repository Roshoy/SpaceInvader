import pygame
from Main.Engine import Engine
from Main.menu import Menu

class A:
    heh = dict()
    a = 0
    @classmethod
    def m(cls):
        cls.heh = dict()
        cls.inc(4)
        print(str(cls.heh))

    @classmethod
    def inc(cls, k):
        cls.a += k
        cls.heh.update({k: 1})

class B(A):
    @classmethod
    def m(cls):
        cls.inc(1)
        print(cls.a)
        print(str(cls.heh))

class C(A):
    @classmethod
    def m(cls):
        cls.heh = dict()
        #cls.heh.clear()
        print("B.heh = " + str(B.heh))
        cls.inc(2)
        print(cls.a)
        print(str(cls.heh))

# class C(A, B):
#     def __init__(self):
#         A.__init__(self)
#         B.__init__(self)
#         print("C")

B.m()
C.m()
A.m()
C.m()
print(str(A.heh))
B.m()





pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
# comment

menu = Menu(screen, "Space Invaders Deluxe")
menu.run()

# #while true:
#     ##events


#engine = Engine(screen)
#engine.run_single()
