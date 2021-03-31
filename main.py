import pygame
from random import randint
from pprint import pprint

from ships import HeroShip, EnemyShip
from weapons import Rocket
from actionprocessing import Collisions
from gameinfo import Life, LifeBar, GameOver




FPS = 30
WORK = True
GAME_OVER = False
JOYSTICK = False
GAME_OVER = False
PAUSE = False


pygame.init()
dispinfo = pygame.display.Info()
SCREEN_SIZE = (dispinfo.current_w, dispinfo.current_h)
SCREEN_X, SCREEN_Y = SCREEN_SIZE
screen = pygame.display.set_mode((SCREEN_SIZE), pygame.DOUBLEBUF | pygame.RESIZABLE | pygame.NOFRAME)
WIN_WIDTH, WIN_HEIGHT = screen.get_size()

im_lifebar = './media/sprites/life10x15.png'
im_gameover = './media/background_sources/gameover.png'
im_rokket = './media/sprites/raketa24x33.png'
im_hero = './media/sprites/airplanx60.png'
im_redship = './media/sprites/redship60.png'
im_bg_map = './media/background_sources/bgmap.png'


bgimage = pygame.image.load(im_bg_map).convert()
bgimage = pygame.transform.scale(bgimage,(WIN_WIDTH, WIN_HEIGHT))

clock = pygame.time.Clock()
angle = 0
count_interval = 0
HAT = (0,0)

# =====================================================================================
# ================================ СОЗДАНИЕ ОБЕКТОВ ====================================
# =====================================================================================

gameover = GameOver(im_gameover, SCREEN_SIZE)

lifebar = LifeBar(im_lifebar, (10,10), 10)
lifebar.create_bar()

heros = pygame.sprite.Group()
airplane = HeroShip(im_hero,(300,300),angle=0, speed=4, 
                    speed_rot=9, group=heros, health=10)

target = pygame.sprite.Group()
sp = 4
for i in range(2):
    sp += 0.5
    tar = EnemyShip(screen, im_redship,(300,300),
                    angle=90,speed=sp, group=target)

bullets = pygame.sprite.Group()

# =====================================================================================
# =====================================================================================

if pygame.joystick.get_count() > 0:
    JOYSTICK = True
    joy = pygame.joystick.Joystick(0)
    joy.init()

while True:
    
# =====================================================================
# ======================= ОБРАБОТКА СОБЫТИЙ ===========================
# =====================================================================

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            WORK = False
            break
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                WORK = False
                break
            if event.key == pygame.K_p:
                PAUSE = not PAUSE
            if GAME_OVER and event.key == pygame.K_RETURN:
                GAME_OVER = False
        elif event.type == pygame.JOYBUTTONDOWN:
            if joy.get_button(0) and not GAME_OVER:
                if count_interval >= 10 or count_interval == 0:
                    for h in heros.sprites():
                        Rocket(im_rokket, h.get_pos(), 30, 90, h.angle, speed=20, group=bullets)
                        Rocket(im_rokket, h.get_pos(), -30, 90, h.angle, speed=20, group=bullets)
                        Rocket(im_rokket, h.get_pos(), 0, 0, h.angle, speed=20, group=bullets)
                    count_interval = 0
        elif event.type == pygame.JOYHATMOTION:
                HAT = event.dict['value']
            
    if JOYSTICK and not GAME_OVER:
        if HAT == (0,1):
            airplane.move_updown((SCREEN_X,SCREEN_Y), True)
        elif HAT == (0,-1):
            airplane.move_updown((SCREEN_X,SCREEN_Y), False)
        if HAT == (1,0):
            airplane.rotate(-airplane.speed-1)
        elif HAT == (-1,0):
            airplane.rotate(airplane.speed-1)
        if HAT == (1,1):
            airplane.move_updown((SCREEN_X,SCREEN_Y), True)
            airplane.rotate(-airplane.speed-1)
        elif HAT == (-1,1):
            airplane.move_updown((SCREEN_X,SCREEN_Y), True)
            airplane.rotate(airplane.speed-1)
        elif HAT == (-1,-1):
            airplane.move_updown((SCREEN_X,SCREEN_Y), False)
            airplane.rotate(airplane.speed-1)
        elif HAT == (1,-1):
            airplane.move_updown((SCREEN_X,SCREEN_Y), False)
            airplane.rotate(-airplane.speed-1)
    
    if not GAME_OVER and not PAUSE:
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_UP]:
            airplane.move_updown((SCREEN_X,SCREEN_Y), True)
        if keys_pressed[pygame.K_DOWN]:
            airplane.move_updown((SCREEN_X, SCREEN_Y),False)
        if keys_pressed[pygame.K_RIGHT]:
            airplane.rotate(-airplane.speed-1)
        if keys_pressed[pygame.K_LEFT]:
            airplane.rotate(airplane.speed-1)
        if keys_pressed[pygame.K_SPACE]:
            if count_interval >= 10 or count_interval == 0:
                for h in heros.sprites():
                    Rocket(im_rokket, h.get_pos(), 30, 90, h.angle, speed=20, group=bullets)
                    Rocket(im_rokket, h.get_pos(), -30, 90, h.angle, speed=20, group=bullets)
                    Rocket(im_rokket, h.get_pos(), 0, 0, h.angle, speed=23, group=bullets)
                count_interval = 0
        count_interval += 1
    
    
    
# =====================================================================
# =====================================================================
    if not WORK:
        break
# =====================================================================
# ======================= ОТРИСОВКА ОБЪЕКТОВ ==========================
# =====================================================================
    
    screen.blit(bgimage, (0,0))
    
    if not GAME_OVER and not PAUSE:
        for blt in bullets.sprites():
            blt.check_collide(target, True)
        
        
        for hero in heros.sprites():
            for tar in target.sprites():
                state, h, t = Collisions.collide_rect(hero, tar)
                if state:
                    if not h.decrease_health(t.damage):
                        h.new_life((300,300), 10)
                        lifebar.reset_bar()
                        GAME_OVER = True
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
        
        
        lifebar.update(airplane.health)
        lifebar.draw(screen)
        
        heros.update(screen)
        heros.draw(screen)
        
        target.update(screen, airplane.rect.center)
        target.draw(screen)
        
        bullets.update(screen)
        bullets.draw(screen)
    
    gameover.set_state(GAME_OVER)
    gameover.draw_gameover(screen)
    
    
    
# =====================================================================
# =====================================================================
    pygame.display.flip()
    clock.tick(FPS)


pygame.display.quit()
pygame.quit()
exit(0)
















