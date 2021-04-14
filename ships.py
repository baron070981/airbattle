import pygame
from random import randint
import math
from abc import abstractmethod





class HeroShip(pygame.sprite.Sprite):
    
    def __init__(self, filename, pos, angle=0, speed = 6, speed_rot=None, health=3, group=None):
        super().__init__()
        self.original_image = pygame.image.load(filename).convert_alpha()
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect(center=pos)
        self.angle = angle
        self.speed = speed
        if speed_rot is None:
            self.speed_rot = self.speed-2
        else:
            self.speed_rot = speed_rot
        self.direction = pygame.Vector2()
        self.rotate()
        self.update_direction()
        self.x = self.rect[0]
        self.y = self.rect[1]
        self.health = health
        self.damage = 1
        if group is not None:
            self.group = group
            self.add(group)
        self.collide = self.set_collide()
        self.alpha = 255
        self.score = 0
    
    def add_score(self, score):
        self.score += score
    
    def sub_score(self, score):
        self.score -= score
        if self.score < 0:
            self.score = 0
    
    def scores(self):
        return self.score
    
    
    def set_collide(self):
        w, h = self.image.get_size()
        w = w/2
        h = h/2
        collide = pygame.Rect((self.rect.x+w/2, self.rect.y+h/2, w, h))
        return collide
    
    def set_damage(self, damage):
        self.damage = damage
    
    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))
    
    def update(self, screen):
        self.update_direction()
    
    def update_direction(self):
        tmp_dir = pygame.Vector2(0,-1).rotate(self.angle)
        self.direction.update(pygame.Vector2(tmp_dir.x*-1*self.speed_rot, tmp_dir.y*1*self.speed_rot))
    
    def rotate(self, angle=None):
        if angle is not None:
            self.angle += angle
        if self.angle >= 359.9:
            self.angle = 0
        elif self.angle <= -0.1:
            self.angle = 359
        
        center = self.rect.center
        self.update_direction()
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        
        new_rect = self.image.get_rect(center=center)
        self.rect = pygame.Rect(new_rect)
        self.x = self.rect[0]
        self.y = self.rect[1]
    
    def move_updown(self, screen_size, state=True):
        w,h = self.rect[2], self.rect[3]
        self.update_direction()
        if state:
            x = 1*self.direction.x + self.x
            y = 1*self.direction.y + self.y
        elif not state:
            x = -1*self.direction.x + self.x
            y = -1*self.direction.y + self.y
        new_rect = pygame.Rect((x, y, w, h))
        self.rect = new_rect.copy()
        self.x = x
        self.y = y
        self.collide = self.set_collide()
        return self.check_move(screen_size)
    
    def check_move(self, screen):
        screen_rect = pygame.Rect((0, 0, screen[0], screen[1]))
        if self.rect.x <= 0:
            self.rect.x = 0
            self.x = 0
        elif self.rect.x+self.rect.width >= screen[0]:
            self.rect.x = screen[0] - self.rect.width
            self.x = self.rect.x
        if self.rect.y <= 0:
            self.rect.y = 0
            self.y = 0
        elif self.rect.y+self.rect.height >= screen[1]:
            self.rect.y = screen[1]-self.rect.height
            self.y = self.rect.y
    
    def get_pos(self, step = (0, 0)):
        return self.rect.center[0], self.rect.center[1]
    
    def get_pos(self):
        return self.rect.center[0], self.rect.center[1]
    
    def decrease_health(self, num):
        self.health -= num
        if self.health <= 0:
            return False
        return True
    
    def new_life(self, pos, health):
        self.health = health
        self.rect = self.image.get_rect(center=pos)
        self.angle = 0
        self.rotate()
        self.update_direction()



class EnemyShip(HeroShip):
    def __init__(self, screensize, filename, pos, angle=0, speed = 3, speed_rot=None, health=3, score=1, group=None):
        super().__init__(filename, (0,0), angle=0, speed = speed, health=3)
        self.rect = self.__create_ship(screensize)
        self.pos = pos
        self._rotate(pos)
        if group is not None:
            self.add(group)
        self.score = score
        self.health = health
        self.dec_health = health
    
    def __create_ship(self, screensize, speed=None):
        if isinstance(screensize, pygame.Surface):
            w, h = screensize.get_size()
        else:
            w, h = screensize[0], screensize[1]
        if speed is not None:
            self.speed = speed
        side = randint(1, 4)
        self.width = self.image.get_size()[0]
        self.height = self.image.get_size()[1]
        if side == 1:
            y = -self.height-5
            x = randint(-self.width-5, w+5)
        elif side == 2:
            x = w+5
            y = randint(-self.height-5, self.height+5)
        elif side == 3:
            x = randint(-self.width-5, w+5)
            y = h+5
        elif side == 4:
            x = -self.width-5
            y = randint(-self.height-5, h+5)
        print(side, x, y)
        return pygame.Rect((x, y, self.width, self.height))
    
    def move_ship(self, screen):
        self.rect = self.__create_ship(screen)
        # print('',rect)
        # self.rect.move_ip(rect.x, rect.y)

    def _rotate(self, pos):
        self.pos = pygame.Vector2(pos[0],pos[1])
        this_position = pygame.Vector2(self.rect.center[0], self.rect.center[1])
        sub_len = self.pos-this_position
        normal = pygame.Vector2(0,-1)
        self.angle = math.degrees(math.atan2(sub_len.x,sub_len.y))+180
        self.rotate()

    def move(self, screensize):
        if isinstance(screensize, pygame.Surface):
            screensize = screensize.get_size()
        w,h = self.rect[2], self.rect[3]
        self.update_direction()
        x = self.direction.x + self.x
        y = self.direction.y + self.y
        new_rect = pygame.Rect((x, y, w, h))
        self.rect = new_rect.copy()
        self.x = x
        self.y = y
        self.collide = self.set_collide()
        self.check_move(screensize)
    
    def update(self, screen, pos):
        self._rotate(pos)
        self.move(screen)
    
    def _decrease_health(self, num):
        self.dec_health -= num
        if self.dec_health <= 0:
            self.dec_health = self.health
            return False
        return True
    




















