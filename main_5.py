import pygame
from time import time
from random import randint

pygame.init()
display = pygame.display.set_mode((1280, 670))
pygame.display.set_caption('Space invaders')
background = pygame.image.load('background_space.png')
pygame.mixer.music.load('Megalovania.mp3')
pygame.mixer.music.play(-1)
#__________________________________________________________Vazgen
bullet_sprite = pygame.image.load('bullet.png')
player_sprite = pygame.image.load('ship.png')
enemy1_sprite = pygame.image.load('vrag1.png')
enemy2_sprite = pygame.image.load('vrag2.png')
enemy3_sprite = pygame.image.load('vrag3.png')
boss_sprite = pygame.image.load('boss.png')
#__________________________________________________________Vazgen
smallfont = pygame.font.SysFont("verdana",25)
white = (255,255,255)
points=0
start_time=time()
def score(score):
    text=smallfont.render("Score:" +str(score), True, white)
    display.blit(text,[1095,0])
def timer(timer):
    text=smallfont.render("Time:" +str(timer), True, white)
    display.blit(text,[1095,30])
##########################
#__________________________________________________________Vazgen
class Bullet:
    Bullets = []
    Player = []

    def __init__(self, display, x, y, sprite, directionY=-5, directionX=0):
        self.sprite = sprite
        self.display = display
        self.directionY = directionY
        self.directionX = directionX
        self.instance = self.sprite.get_rect(topleft=(x, y))
        display.blit(self.sprite, self.instance)

class Player:
    def __init__(self, display, x, y, sprite):
        self.sprite = sprite
        self.display = display
        self.instance = self.sprite.get_rect(center=(x, y))
        display.blit(self.sprite, self.instance)
    def shoot(self):
        Bullet.Player.append(Bullet(self.display, self.instance.centerx - 5, self.instance.y, bullet_sprite))


class EnemyLevelOne(Player):
    def __init__(self, display, x, y, sprite):
        Player.__init__(self, display, x, y, sprite)
        self.instance = self.sprite.get_rect(topleft=(x, y))
        self.shoot_time = randint(5, 10)
    def shoot(self):
        Bullet.Bullets.append(Bullet(self.display, self.instance.centerx - 6, self.instance.bottomleft[1], bullet_sprite, 5))


class EnemyLevelTwo(EnemyLevelOne):
    def __init__(self, *args, **kwargs):
        EnemyLevelOne.__init__(self, *args, **kwargs)
        self.is_active = False
    def shoot(self):
        Bullet.Bullets.append(Bullet(self.display, self.instance.centerx - 5, self.instance.bottomleft[1], bullet_sprite, 5, -1))
        Bullet.Bullets.append(Bullet(self.display, self.instance.centerx - 5, self.instance.bottomleft[1], bullet_sprite, 5, 1))


class EnemyLevelThree(EnemyLevelTwo):
    def __init__(self, *args, **kwargs):
        EnemyLevelTwo.__init__(self, *args, **kwargs)
    def shoot(self):
        Bullet.Bullets.append(Bullet(self.display, self.instance.centerx - 6.5, self.instance.bottomleft[1], bullet_sprite, 5))
        Bullet.Bullets.append(
            Bullet(self.display, self.instance.centerx - 6.5, self.instance.bottomleft[1], bullet_sprite, 5, -1))
        Bullet.Bullets.append(
            Bullet(self.display, self.instance.centerx - 6.5, self.instance.bottomleft[1], bullet_sprite, 5, 1))


class Boss(EnemyLevelTwo):
    def __init__(self, display, x, y, sprite):
        EnemyLevelTwo.__init__(self, display, x, y, sprite)
        self.instance = self.sprite.get_rect(topleft=(x, y))
        self.hp = 100
        self.shoot_time = randint(1, 2)
        self.move = True
        self.down = False
    def shoot(self):
        Bullet.Bullets.append(
            Bullet(self.display, self.instance.centerx - 6.5, self.instance.bottomleft[1], bullet_sprite, 10, -2))
        Bullet.Bullets.append(
            Bullet(self.display, self.instance.centerx - 6.5, self.instance.bottomleft[1], bullet_sprite, 10, -1))
        Bullet.Bullets.append(Bullet(self.display, self.instance.centerx - 6.5, self.instance.bottomleft[1], bullet_sprite, 10))
        Bullet.Bullets.append(
            Bullet(self.display, self.instance.centerx - 6.5, self.instance.bottomleft[1], bullet_sprite, 10, 1))
        Bullet.Bullets.append(
            Bullet(self.display, self.instance.centerx - 6.5, self.instance.bottomleft[1], bullet_sprite, 10, 2))
#__________________________________________________________Vazgen
#############################
player = Player(display, 640, 600, player_sprite)
boss = Boss(display, 545, 10, boss_sprite)

invaders = [[], [], []]
current_x = 5
for i in range(11):
    invaders[2].append(EnemyLevelThree(display, current_x, 5, enemy3_sprite))
    invaders[1].append(EnemyLevelTwo(display, current_x, 75, enemy2_sprite))
    invaders[0].append(EnemyLevelOne(display, current_x, 145, enemy1_sprite))
    current_x += 45
del current_x

clock = pygame.time.Clock()
down = False
move = False
new_time = True
run = True
while run:
    display.blit(background,(0,0))
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                pass
            elif event.key == pygame.K_RIGHT:
                pass
            if event.key == pygame.K_UP and len(Bullet.Player) < 5:
                player.shoot()
        elif event.type == pygame.KEYUP:
            pass

    for row in invaders:
        if row and row[-1] == None:
            row.pop(-1)
        for invader in row:
            if invader is not None:
                display.blit(invader.sprite, invader.instance)
        if not row:
            invaders.remove(row)
            if len(invaders) == 0 and new_time:
                boss.is_active = True
                boss_time = time()
                new_time = False
        if None in row and invaders.index(row) != len(invaders) - 1:
            for invader in invaders[invaders.index(row) + 1]:
                if invader is not None:
                    invader.is_active = True
        for elem in row:
            if elem != None:
                if elem.instance.x >= 1280 - elem.instance.width:
                    move = True
                    down = True
                if elem.instance.x <= 0:
                    move = False
                    down = True
                if move:
                    elem.instance.x -= 5
                else:
                    elem.instance.x += 5
#__________________________________________________________Vazgen
                if int(time() - start_time) % elem.shoot_time == 0 and int(time() - start_time) != 0 and (invaders.index(row) == 0 or elem.is_active):
                    elem.shoot()
                    elem.shoot_time += randint(5, 10)
#__________________________________________________________Vazgen
            if down:
                for row in invaders:
                    for elem in row:
                        if elem != None:
                            elem.instance.y += 15
                down = False
#__________________________________________________________Vazgen
    display.blit(boss.sprite, boss.instance)
    if boss.is_active:
        if boss.instance.x >= 1280 - boss.instance.width:
            boss.move = True
            boss.down = True
        elif boss.instance.x <= 0:
            boss.move = False
            boss.down = True
        if boss.move:
            boss.instance.x -= 5
        else:
            boss.instance.x += 5
        if boss.down:
            boss.instance.y += 15
            boss.down = False
        if int(time() - boss_time) % boss.shoot_time == 0 and int(time() - boss_time) != 0:
            boss.shoot()
            boss.shoot_time += randint(1, 2)
#__________________________________________________________Vazgen
    for bullet in Bullet.Bullets + Bullet.Player:
        if bullet.instance.y > 0 and bullet.instance.bottomleft[1] < 1280:
            bullet.instance.y += bullet.directionY
            bullet.instance.x += bullet.directionX
        else:
            if bullet in Bullet.Player:
                Bullet.Player.remove(bullet)
            else:
                Bullet.Bullets.remove(bullet)
        display.blit(bullet.sprite, bullet.instance)
        if bullet not in Bullet.Player and bullet.instance.colliderect(player.instance):
            run = False
        for row in invaders:
            for elem in row:
                if bullet in Bullet.Player and elem != None and bullet.instance.colliderect(
                        elem.instance):
                    row[row.index(elem)] = None
                    Bullet.Player.remove(bullet)
                    points+=100

    if keys[pygame.K_LEFT] and player.instance.x > 0:
        player.instance.x -= 10
    if keys[pygame.K_RIGHT] and player.instance.x < 1280 - player.instance.width:
        player.instance.x += 10
    score(points)
    timer(str(round(time()-start_time))+" sec")
    
    display.blit(player.sprite, player.instance)
    pygame.display.update()
    clock.tick(60)

pygame.quit()