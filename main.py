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
screen = pygame.display.set_mode((SCREEN_SIZE), pygame.DOUBLEBUF | pygame.RESIZABLE)

bgimage = pygame.image.load('./media/background_sources/background2_2.jpg').convert()

clock = pygame.time.Clock()
angle = 0
count_interval = 0
target_list = []
cnt = 0

# =====================================================================================
# ================================ СОЗДАНИЕ ОБЕКТОВ ====================================
# =====================================================================================


lifebar = LifeBar('./media/sprites/life10x15.png', (10,10), 10)
lifebar.create_bar()

gameover = GameOver('./media/background_sources/gameover.png', SCREEN_SIZE)
bullet_image = './media/sprites/raketa24x33.png'

heros = pygame.sprite.Group()
airplane = HeroShip('./media/sprites/airplanx60.png',
                    (300,300),angle=0, 
                     speed=4, speed_rot=9, group=heros, health=10)




target = pygame.sprite.Group()
sp = 4
for i in range(2):
    sp += 0.5
    tar = EnemyShip(screen, './media/sprites/redship60.png',(300,300),
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
                        Rocket(bullet_image, h.get_pos(), 30, 90, h.angle, speed=20, group=bullets)
                        Rocket(bullet_image, h.get_pos(), -30, 90, h.angle, speed=20, group=bullets)
                        Rocket(bullet_image, h.get_pos(), 0, 0, h.angle, speed=20, group=bullets)
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
                    Rocket(bullet_image, h.get_pos(), 30, 90, h.angle, speed=20, group=bullets)
                    Rocket(bullet_image, h.get_pos(), -30, 90, h.angle, speed=20, group=bullets)
                    Rocket(bullet_image, h.get_pos(), 0, 0, h.angle, speed=23, group=bullets)
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
        
        heros.update()
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
















