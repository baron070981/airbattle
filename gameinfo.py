import pygame





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
    
    def next_pos(self):
        x = self.rect.center[0]+self.rect.width+10
        return x, self.rect.y
    


class LifeBar:
    
    def __init__(self, lenght, group):
        self.group = group
        self.lenght = lenght
    
    def add_life(self, life):
        life.add(self.group)
    
    def life(self):
        pass
    
    
    
    
    









