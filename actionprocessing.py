import pygame
from random import randint
from pprint import pprint


'''
Модуль обработки взаимодействий объектов друг с другом.

'''

class Collisions:
    
    def __init__(self):
        pass
    
    def collide_groups(self, *groups):
        pass
    
    @classmethod
    def collide_rect(cls, obj1, obj2):
        if pygame.Rect.colliderect(obj1.collide, obj2.collide):
            return True, obj1, obj2
        return False, None, None














