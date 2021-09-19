import pygame


# Модуль отображения информации (уровень жизни, очки...)


class Life(pygame.sprite.Sprite):
    
    ALPHA = 1
    NOTALPHA = 0
    
    def __init__(self, filename, pos, group):
        super().__init__()
        self.original_image = pygame.image.load(filename)
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect(center=pos)
        self.alpha = 255
        self.add(group)
    
    def update(self, flag=ALPHA):
        ''' Обновление альфа-канала'''
        if flag == self.ALPHA:
            self.image.set_alpha(255)
        elif flag == self.NOTALPHA:
            self.image.set_alpha(1)
    


class LifeBar:
    def __init__(self, filename, pos, lenbar=3, space=10):
        self.original = pygame.image.load(filename).convert_alpha()
        self.sizerect = self.original.get_size()
        self.filename = filename
        self.pos = pos
        self.lenbar = lenbar
        self.space = space
        self.group = pygame.sprite.Group()
    
    def update(self, lenbar):
        sprites = self.group.sprites()
        for i in range(lenbar, self.lenbar):
            sprites[i].update(0)
    
    def draw(self, screen):
        self.group.draw(screen)
    
    def create_bar(self):
        w, h = self.sizerect
        positions = self.__set_positions(w,h)
        for i in range(self.lenbar):
            Life(self.filename, positions[i], self.group)
    
    def remove_life(self):
        pass
    
    def reset_bar(self):
        sprites = self.group.sprites()
        for spr in sprites:
            spr.update(1)
    
    def __set_positions(self, w, h):
        positions = [self.pos]
        
        for i in range(1, self.lenbar):
            pos = (positions[i-1][0]+self.space, positions[i-1][1])
            positions.append(pos)
        return positions



class GameOver(pygame.sprite.Sprite):
    
    def __init__(self, filename, screensize, timeout=1):
        super().__init__()
        self.timeout = timeout
        self.center = (screensize[0]//2, screensize[1]//2)
        self.image = pygame.image.load(filename)
        self.rect = self.image.get_rect(center=self.center)
        self.state = False
    
    def set_state(self, state):
        self.state = state
    
    def draw_gameover(self, screen):
        if self.state:
            screen.blit(self.image, (self.rect.x,self.rect.y))

    
    
class Scores:
    
    def __init__(self,screen, filename=None, pos=(0,0), color=(255,0,0), text='0'):
        if isinstance(screen, pygame.Surface):
            self.size_rect = screen.get_size()
        elif isinstance(screen, tuple) or isinstance(screen, list):
            self.size_rect = screen
        self.pos = pos
        self.color = color
        self.text = text
        self.text_size = int(self.size_rect[1]/10)
        self.font = pygame.font.Font(filename, self.text_size)
        self.text_surface = self.font.render(self.text, True, self.color)
    
    def render(self, text):
        self.text_surface = self.font.render(str(text), True, self.color)
    
    def draw(self, screen):
        screen.blit(self.text_surface, self.pos)
    
    def calculate_position(self, screensize):
        width, height = self.text_surface.get_size()
        pos_y = 30
        pos_x = screensize[0] - width - 30
        self.pos = (pos_x, pos_y)


class Pause(pygame.sprite.Sprite):
    
    def __init__(self, filename, screensize):
        super().__init__()
        self.center = (screensize[0]//2, screensize[1]//2)
        self.image = pygame.image.load(filename)
        self.rect = self.image.get_rect(center=self.center)
        self.state = False
    
    def set_pause(self):
        self.state = not self.state
    
    def draw_pause(self, screen):
        if self.state:
            screen.blit(self.image, (self.rect.x,self.rect.y))

















