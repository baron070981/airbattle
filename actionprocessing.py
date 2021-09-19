import pygame
from random import randint
from pprint import pprint
import os
import os.path



class Collisions:
    
    """
    класс проверки столкновений
    """
    
    def __init__(self):
        pass
    
    def collide_groups(self, *groups):
        pass
    
    @classmethod
    def collide_rect(cls, obj1, obj2):
        if pygame.Rect.colliderect(obj1.collide, obj2.collide):
            return True, obj1, obj2
        return False, None, None



class Path:
    """
    класс обработки путей к файлам
    """
    def __init__(self):
        self.Home = os.path.abspath(os.path.dirname(__file__))
    
    def add(self, path_to_file):
        return os.path.join(self.Home, path_to_file)









