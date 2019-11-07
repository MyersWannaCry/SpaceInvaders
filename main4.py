import pygame
from random import choice

pygame.init()
display = pygame.display.set_mode((1280, 670))
pygame.display.set_caption('Space invaders')
background = pygame.image.load('background_space.png')

x = 640  # корды нашей ракеты
y = 600
width = 40
height = 60

pygame.mixer.music.load('Test.mp3')
pygame.mixer.music.play()
##########################
class Bullet:
    Bullets = []
    Player = []  # new

    def __init__(self, display, x, y, sprite, directionY=-5, directionX=0):
        self.sprite = pygame.image.load('bullet.png')
        self.display = display
        self.directionY = directionY
        self.directionX = directionX
        self.instance = self.sprite.get_rect(topleft=(x, y))
        display.blit(sprite, self.instance)


class Player:
    def __init__(self, display, x, y, sprite):
        self.sprite = sprite
# pygame.image.load('ship.png')
        self.display = display
        self.instance = self.sprite.get_rect(topleft=(x, y))
        display.blit(sprite, self.instance)

    def shoot(self, sprite):
        Bullet.Player.append(Bullet(self.display, self.instance.centerx - 2, self.instance.y, sprite))


class EnemyLevelOne(Player):
    def __init__(self, *args, **kwargs):
        Player.__init__(self, *args, **kwargs)
        self.sprite = pygame.image.load('vrag1.png')
    def shoot(self, sprite):
        Bullet.Bullets.append(Bullet(self.display, self.instance.centerx - 2, self.instance.bottomleft[1], sprite, 5))


class EnemyLevelTwo(EnemyLevelOne):
    def __init__(self, *args, **kwargs):
        EnemyLevelOne.__init__(self, *args, **kwargs)
        self.is_active = False
        self.sprite = pygame.image.load('vrag2.png')
    def shoot(self, sprite):
        Bullet.Bullets.append(Bullet(self.display, self.instance.centerx - 2, self.instance.bottomleft[1], sprite, 5, -1))
        Bullet.Bullets.append(Bullet(self.display, self.instance.centerx - 2, self.instance.bottomleft[1], sprite, 5, 1))


class EnemyLevelThree(EnemyLevelTwo):
    def __init__(self, *args, **kwargs):
        EnemyLevelTwo.__init__(self, *args, **kwargs)
        self.sprite = pygame.image.load('vrag3.png')
    def shoot(self, sprite):
        Bullet.Bullets.append(Bullet(self.display, self.instance.centerx - 2, self.instance.bottomleft[1], sprite, 5))
        Bullet.Bullets.append(
            Bullet(self.display, self.instance.centerx - 2, self.instance.bottomleft[1], sprite, 5, -1))
        Bullet.Bullets.append(
            Bullet(self.display, self.instance.centerx - 2, self.instance.bottomleft[1], sprite, 5, 1))


class Boss(EnemyLevelTwo):
    def __init__(self, *args, **kwargs):
        EnemyLevelTwo.__init__(self, *args, **kwargs)
#        self.sprite = sprite
        self.hp = 100

    def shoot(self, sprite):
        Bullet.Bullets.append(
            Bullet(self.display, self.instance.centerx - 2, self.instance.bottomleft[1], sprite, 10, -2))  # Класс босса
        Bullet.Bullets.append(
            Bullet(self.display, self.instance.centerx - 2, self.instance.bottomleft[1], sprite, 10, -1))
        Bullet.Bullets.append(Bullet(self.display, self.instance.centerx - 2, self.instance.bottomleft[1], sprite, 10))
        Bullet.Bullets.append(
            Bullet(self.display, self.instance.centerx - 2, self.instance.bottomleft[1], sprite, 10, 1))
        Bullet.Bullets.append(
            Bullet(self.display, self.instance.centerx - 2, self.instance.bottomleft[1], sprite, 10, 2))


#############################
player = Player(display, x, y, pygame.Surface((width, height)))
boss = Boss(display, x, y, pygame.Surface((width, height)))

invaders = [[], [], []]
current_x = 5
for i in range(11):
    invaders[2].append(EnemyLevelThree(display, current_x, 5, pygame.Surface((40, 60))))
    invaders[1].append(EnemyLevelTwo(display, current_x, 75, pygame.Surface((40, 60))))
    invaders[0].append(EnemyLevelOne(display, current_x, 145, pygame.Surface((40, 60))))
    current_x += 45
del current_x

clock = pygame.time.Clock()
run = True
while run:
    display.blit(background,(0,0))
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and x < 50:
                pass
            elif event.key == pygame.K_RIGHT and x < 1200:
                pass
            if event.key == pygame.K_UP and len(Bullet.Player) < 10:
                player.shoot(pygame.Surface((5, 5)))

# ----------------------------------------------------------MAIN_4----Bogdan
            if event.key == pygame.K_DOWN:
                invaders[0][0].shoot(pygame.Surface((5, 5)))
                invaders[1][4].shoot(pygame.Surface((5, 5)))
                invaders[2][10].shoot(pygame.Surface((5, 5)))
# ----------------------------------------------------------

        elif event.type == pygame.KEYUP:
            pass

    for row in invaders:
        if row and row[-1] == None:
            row.pop(-1)
        for invader in row:
            if invader is not None:
                display.blit(invader.sprite, invader.instance)
        if not row:
            invaders.remove(row)  # Активация босса
            if len(invaders) == 0:
                boss.is_active = True
        if None in row and invaders.index(row) != len(invaders) - 1:
            for invader in invaders[invaders.index(row) + 1]:  # Активация врагов
                if invader is not None:
                    invader.is_active = True

    for bullet in Bullet.Bullets + Bullet.Player:
        if bullet.instance.y > 0 and bullet.instance.bottomleft[1] < 1280:
            bullet.instance.y += bullet.directionY
            bullet.instance.x += bullet.directionX
        else:
            if bullet in Bullet.Player:
                Bullet.Player.remove(bullet)
            else:
                Bullet.Player.remove(bullet) 
        display.blit(bullet.sprite, bullet.instance)
        if bullet not in Bullet.Player and bullet.instance.colliderect(player.instance):  # Попадание в игрока
            run = False
        for row in invaders:
            for elem in row:
                if bullet in Bullet.Player and elem != None and bullet.instance.colliderect(
                        elem.instance):  # Попадание во врагов(переделано)
                    row[row.index(elem)] = None
                    Bullet.Player.remove(bullet)

    if keys[pygame.K_LEFT] and player.instance.x > 0:  # Немного переделал логику для удобства
        player.instance.x -= 10
    if keys[pygame.K_RIGHT] and player.instance.x < 1280 - player.instance.width:
        player.instance.x += 10
    # ----------------------------------------------------------MAIN_4----Bogdan
    if keys[pygame.K_DOWN]:
        invaders[0][0].shoot(pygame.Surface((5, 5)))
        invaders[1][4].shoot(pygame.Surface((5, 5)))
        invaders[2][10].shoot(pygame.Surface((5, 5)))
# ----------------------------------------------------------
    display.blit(player.sprite, player.instance)
    pygame.display.update()
    clock.tick(60)

pygame.quit()

# Справка
"""
=В процессе=
1)Анимация-спрайты
2)Логика босса и врагов

=Изменения=
1)Класс босса
2)Реализовано попадение в игрока
3)Активация босса и врагов
4)Дополнена логика патронов

=ЧтоНужноСделать=
1)Звуки и музыка
"""
