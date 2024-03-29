import pygame
from random import randint
from pprint import pprint

from ships import HeroShip, EnemyShip
from weapons import Rocket
from actionprocessing import Collisions, Path
from gameinfo import Life, LifeBar, GameOver, Scores, Pause




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

# получение путей к изображениям
im_lifebar = Path().add('./media/sprites/life10x15.png')
im_gameover = Path().add('./media/background_sources/gameover.png')
im_rokket = Path().add('./media/sprites/raketa24x33.png')
im_hero = Path().add('./media/sprites/airplanx60.png')
im_redship = Path().add('./media/sprites/redship60.png')
im_yellowship = Path().add('./media/sprites/yellowship60.png')
im_grayship = Path().add('./media/sprites/grayship60.png')
im_bg_map = Path().add('./media/background_sources/bgmap.png')
im_pause = Path().add('./media/background_sources/pause.png')


# загрузка фонового изображения
bgimage = pygame.image.load(im_bg_map).convert()
bgimage = pygame.transform.scale(bgimage,(WIN_WIDTH, WIN_HEIGHT))

clock = pygame.time.Clock()
angle = 0
count_interval = 0
HAT = (0,0)

# =====================================================================================
# ================================ СОЗДАНИЕ ОБЕКТОВ ====================================
# =====================================================================================

# загрузка счетчика очков
scores = Scores(screen, pos=(500,50))
scores.calculate_position(SCREEN_SIZE)

# загрузка изображений gameover и pause
gameover = GameOver(im_gameover, SCREEN_SIZE)
pause = Pause(im_pause, SCREEN_SIZE)

# загрузка изображения уровня жизни
lifebar = LifeBar(im_lifebar, (10,10), 10)
lifebar.create_bar()


# загрузка изображения самолета игрока
heros = pygame.sprite.Group()
airplane = HeroShip(im_hero,(300,300),angle=0, speed=4, 
                    speed_rot=9, group=heros, health=10)


# загрузка самолетов противника
target = pygame.sprite.Group()
sp = 3
for i in range(2):
    sp += 0.4
    tar = EnemyShip(screen, im_redship,(300,300),
                    angle=90,speed=sp, group=target, score=1, health=1)
sp = 3

for i in range(2):
    sp += 0.4
    tar = EnemyShip(screen, im_yellowship,(300,300),
                    angle=90,speed=sp, group=target, score=2, health=2)

sp = 4
for i in range(2):
    sp += 0.4
    tar = EnemyShip(screen, im_grayship,(300,300),
                    angle=90,speed=sp, group=target, score=2, health=3)


bullets = pygame.sprite.Group()

# =====================================================================================
# =====================================================================================

# проверка подключения джойстика
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
                pause.set_pause()
            if GAME_OVER and event.key == pygame.K_RETURN:
                GAME_OVER = False
        elif event.type == pygame.JOYBUTTONDOWN:
            if joy.get_button(0) and not GAME_OVER:
                if count_interval >= 10 or count_interval == 0:
                    for h in heros.sprites():
                        Rocket(im_rokket, h.get_pos(), 30, 90, h.angle, speed=20, group=bullets, damage=1)
                        Rocket(im_rokket, h.get_pos(), -30, 90, h.angle, speed=20, group=bullets,damage=1)
                        Rocket(im_rokket, h.get_pos(), 0, 0, h.angle, speed=20, group=bullets, damage=2)
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
                    airplane.sub_score(t.score)
                    scores.calculate_position(SCREEN_SIZE)
                    scores.render(airplane.scores())
                    t.move_ship(screen)
                    if not h.decrease_health(t.damage):
                        h.new_life((300,300), 10)
                        lifebar.reset_bar()
                        GAME_OVER = True
                        for trg in target.sprites():
                            trg.move_ship(screen)
                        break
                    t.move_ship(screen)
                if not WORK:
                    break
        
        
        for blt in bullets.sprites():
            for ship in target.sprites():
                state, b, s = Collisions.collide_rect(blt, ship)
                if state:
                    b.kill()
                    if not s._decrease_health(1):
                        s.move_ship(screen)
                        airplane.add_score(s.score)
                        scores.calculate_position(SCREEN_SIZE)
                        scores.render(airplane.scores())
        
        
        scores.draw(screen)
        
        lifebar.update(airplane.health)
        lifebar.draw(screen)
        
        heros.update(screen)
        heros.draw(screen)
        
        target.update(screen, airplane.rect.center)
        target.draw(screen)
        
        bullets.update(screen)
        bullets.draw(screen)
    
    elif GAME_OVER:
        gameover.set_state(GAME_OVER)
        gameover.draw_gameover(screen)
    
    elif PAUSE:
        pause.draw_pause(screen)
    
    
    
# =====================================================================
# =====================================================================
    pygame.display.flip()
    clock.tick(FPS)


pygame.display.quit()
pygame.quit()
exit(0)
















