import pygame
from random import randint
from pprint import pprint

from ships import HeroShip, EnemyShip
from weapons import Rocket
from actionprocessing import Collisions
from gameinfo import Life


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
GAME_OVER = False
JOYSTICK = False


pygame.init()
dispinfo = pygame.display.Info()
SCREEN_SIZE = (dispinfo.current_w, dispinfo.current_h)
screen = pygame.display.set_mode((SCREEN_SIZE), pygame.DOUBLEBUF | pygame.RESIZABLE)
print(type(screen.get_size()))
bgimage = pygame.image.load('./media/background_sources/background2_2.jpg').convert()
clock = pygame.time.Clock()

# =====================================================================================
# ================================ ОТРИСОВКА ФИГУР ====================================
# =====================================================================================





# =====================================================================================
# =====================================================================================


lives = pygame.sprite.Group()


bullet_image = './media/sprites/raketa24x33.png'

heros = pygame.sprite.Group()
airplan_image = HeroShip('./media/sprites/airplanx60.png',(300,300),angle=0, speed=4, speed_rot=9, group=heros)


for i in range(airplan_image.health):
    pos = (20,20)
    life = Life('./media/sprites/life10x15.png', pos, lives)
    pos = life.next_pos()


bullets = pygame.sprite.Group()


target = pygame.sprite.Group()
sp = 4
for i in range(2):
    sp += 0.5
    tar = EnemyShip(screen, './media/sprites/redship60.png',(300,300),angle=90,speed=sp, group=target)
    tar.set_damage(0.2)

angle = 0
count_interval = 0

target_list = []
cnt = 0


if pygame.joystick.get_count() > 0:
    JOYSTICK = True
    joy = pygame.joystick.Joystick(0)
    joy.init()

# joy = pygame.joystick.Joystick(0)

HAT = (0,0)

while True:
    
    screen.fill(LIGHT_BLUE)
# ============================================
# ======= ОБРАБОТКА СОБЫТИЙ ==================
# ============================================
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            WORK = False
            break
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                WORK = False
                break
        elif event.type == pygame.JOYBUTTONDOWN:
            if joy.get_button(0):
                if count_interval >= 10 or count_interval == 0:
                    # bullets.add(fig.Bullet( bullet_image, airplan_image.get_pos((0,0)),30,90,airplan_image.angle,speed=20))
                    # bullets.add(fig.Bullet( bullet_image, airplan_image.get_pos((0,0)),-30,90,airplan_image.angle,speed=20))
                    for h in heros.sprites():
                        Rocket(bullet_image, h.get_pos(), 30, 90, h.angle, speed=20, group=bullets)
                        Rocket(bullet_image, h.get_pos(), -30, 90, h.angle, speed=20, group=bullets)
                        Rocket(bullet_image, h.get_pos(), 0, 0, h.angle, speed=20, group=bullets)
                    count_interval = 0
        elif event.type == pygame.JOYHATMOTION:
                HAT = event.dict['value']
            
    if JOYSTICK:
        if HAT == (0,1):
            airplan_image.move_updown((SCREEN_X,SCREEN_Y), True)
        elif HAT == (0,-1):
            airplan_image.move_updown((SCREEN_X,SCREEN_Y), False)
        if HAT == (1,0):
            airplan_image.rotate(-airplan_image.speed-1)
        elif HAT == (-1,0):
            airplan_image.rotate(airplan_image.speed-1)
        if HAT == (1,1):
            airplan_image.move_updown((SCREEN_X,SCREEN_Y), True)
            airplan_image.rotate(-airplan_image.speed-1)
        elif HAT == (-1,1):
            airplan_image.move_updown((SCREEN_X,SCREEN_Y), True)
            airplan_image.rotate(airplan_image.speed-1)
        elif HAT == (-1,-1):
            airplan_image.move_updown((SCREEN_X,SCREEN_Y), False)
            airplan_image.rotate(airplan_image.speed-1)
        elif HAT == (1,-1):
            airplan_image.move_updown((SCREEN_X,SCREEN_Y), False)
            airplan_image.rotate(-airplan_image.speed-1)
    
    keys_pressed = pygame.key.get_pressed()
    if keys_pressed[pygame.K_UP]:
        airplan_image.move_updown((SCREEN_X,SCREEN_Y), True)
    if keys_pressed[pygame.K_DOWN]:
        airplan_image.move_updown((SCREEN_X, SCREEN_Y),False)
    if keys_pressed[pygame.K_RIGHT]:
        airplan_image.rotate(-airplan_image.speed-1)
    if keys_pressed[pygame.K_LEFT]:
        airplan_image.rotate(airplan_image.speed-1)
    if keys_pressed[pygame.K_SPACE]:
        if count_interval >= 10 or count_interval == 0:
            # bullets.add(fig.Bullet( bullet_image, airplan_image.get_pos((0,0)),30,90,airplan_image.angle,speed=20))
            # bullets.add(fig.Bullet( bullet_image, airplan_image.get_pos((0,0)),-30,90,airplan_image.angle,speed=20))
            for h in heros.sprites():
                Rocket(bullet_image, h.get_pos(), 30, 90, h.angle, speed=20, group=bullets)
                Rocket(bullet_image, h.get_pos(), -30, 90, h.angle, speed=20, group=bullets)
            count_interval = 0
    count_interval += 1
    
    
    
# ==============================================
# ==============================================
    if not WORK:
        break
# ==============================================
# =========== ОТРИСОВКА ОБЪЕКТОВ ===============
# ==============================================
    
    for blt in bullets.sprites():
        blt.check_collide(target, True)
    
    
    # airplan_image.check_collisions(target)
    
    for hero in heros.sprites():
        for tar in target.sprites():
            state, h, t = Collisions.collide_rect(hero, tar)
            if state:
                if not h.decrease_health(t.damage):
                    WORK = False
                    break
                t.move_ship(screen)
            if not WORK:
                break
    
    
    for blt in bullets.sprites():
        for ship in target.sprites():
            state, b, s = Collisions.collide_rect(blt, ship)
            if state:
                b.kill()
                s.move_ship(screen)
    
    
    screen.blit(bgimage, (0,0))
    
    lives.update(Life.ALPHA)
    lives.draw(screen)
    
    heros.update()
    heros.draw(screen)
    
    target.update(screen, airplan_image.rect.center)
    target.draw(screen)
    
    bullets.update(screen)
    bullets.draw(screen)
    
    
    
# ==============================================
# ==============================================
    pygame.display.flip()
    clock.tick(FPS)


pygame.display.quit()
pygame.quit()
exit(0)
















