import pygame
from random import randint
from pprint import pprint
from abc import ABC, abstractmethod



class Weapon(pygame.sprite.Sprite):
    
    def __init__(self, filename, position:tuple=(0,0), 
                            offset:int=0, offset_angle:float=0,
                            angle:float=0, speed:int=1):
        super().__init__()
        self.original_image = pygame.image.load(filename).convert_alpha()
        self.image = self.original_image.copy()
        self.pos = pygame.Vector2(position)
        self.offset = offset
        self.offset_angle = offset_angle
        self.angle = angle
        self.speed = speed
        self.rect = self.getrect()
        self.damage = 1
        self.direction = pygame.Vector2()
        self.rotate()
        self.x = self.rect[0]
        self.y = self.rect[1]
        self.collide = self.set_collide()
    
    def set_collide(self):
        w, h = self.image.get_size()
        w = w/2
        h = h/2
        collide = pygame.Rect((self.rect.x+w/2, self.rect.y+h/2, w, h))
        return collide
    
    # def set_collide(self, rect):
        # if isinstance(rect, tuple) or isinstance(rect, list):
            # self.collide = pygame.Rect(tuple(rect))
        # elif isinstance(rect, pygame.Rect):
            # self.collide = rect.copy()
        # else:
            # raise TypeError('Функция ожидает tuple, list или pygame.Rect')
    
    def getrect(self):
        if self.offset_angle < 0:
            self.offset_angle = 360 + self.offset_angle
        self.offset_angle += self.angle
        
        tmp_dir = pygame.Vector2(0,-1).rotate(self.offset_angle)
        ofs = pygame.Vector2(tmp_dir.x*-1*self.offset,
                             tmp_dir.y*1*self.offset)
        ofs = pygame.Vector2(ofs.x+self.pos.x,
                             ofs.y+self.pos.y)
        w,h = self.image.get_size()
        return pygame.Rect((ofs.x-w/2, ofs.y-h/2, w, h))
    
    def update_direction(self):
        tmp_dir = pygame.Vector2(0,-1).rotate(self.angle)
        self.direction.update(pygame.Vector2(tmp_dir.x*-1*self.speed, tmp_dir.y*1*self.speed))
    
    def rotate(self):
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.update_direction()
        new_rect = self.image.get_rect(center=self.rect.center)
        self.rect = pygame.Rect(new_rect)
        self.x = self.rect[0]
        self.y = self.rect[1]
    
    def move(self):
        raise NotImplementedError('Необходимо определить метод move')
    
    def update(self):
        raise NotImplementedError('Необходимо определить метод update')
    
    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))
    
    def check_collide(self, group, state):
        if state:
            self.remove(group)
            return True



class Rocket(Weapon):
    def __init__(self, filename, position:tuple=(0,0), 
                            offset:int=0, offset_angle:float=0,
                            angle:float=0, speed:int=1, group=None):
        super().__init__(filename, position, offset, offset_angle, angle, speed)
        self.group = group
        self.group.add(self)
    
    def set_damage(self, damage):
        self.damage = damage
    
    def update(self, screen):
        self.move(screen)
    
    def move(self, screen):
        w,h = self.rect[2], self.rect[3]
        self.update_direction()
        x = self.direction.x + self.x
        y = self.direction.y + self.y
        new_rect = pygame.Rect((x, y, w, h))
        self.rect = new_rect.copy()
        self.x = x
        self.y = y
        self.collide = self.set_collide()
        self.check_screen(screen)
    
    def check_screen(self, screen):
        if isinstance(screen, pygame.Surface):
            w, h = screen.get_size()
        else:
            w, h = screen[0], screen[1]
        w = w - 30
        h = h - 30
        if self.rect.x >= w or self.rect.width+self.rect.x <= 10:
            self.kill()
        if self.rect.y >= h or self.rect.height+self.rect.y <= 10:
            self.kill()





if __name__ == '__main__':
    SCREEN_X, SCREEN_Y = 1200, 720
    SCREEN_SIZE = (SCREEN_X, SCREEN_Y)

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GRAY = (125, 125, 125)
    LIGHT_BLUE = (64, 128, 255)
    GREEN = (0, 200, 64)
    YELLOW = (225, 225, 0)
    PINK = (230, 50, 230)

    FPS = 30
    WORK = True
    JOYSTICK = False


    pygame.init()
    screen = pygame.display.set_mode((SCREEN_SIZE), pygame.DOUBLEBUF | pygame.RESIZABLE)
    print(type(screen.get_size()))
    bgimage = pygame.image.load('./background_sources/bgmap.png').convert()
    clock = pygame.time.Clock()
    
    
    g = pygame.sprite.Group()
    w = Rocket('./sprites/redship60.png', group=g)
    w1 = Rocket('./sprites/redship60.png', group=g)
    w2 = Rocket('./sprites/redship60.png', group=g)
    print(w)
    print(g)

















