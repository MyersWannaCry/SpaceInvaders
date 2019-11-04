import pygame
from random import choice

pygame.init()
display = pygame.display.set_mode((1280, 670))
pygame.display.set_caption('Space invaders')
display.fill((255, 255, 255))
x = 640  # корды нашей ракеты
y = 600
width = 40
height = 60
##########################
class Bullet:
    Bullets = []
    def __init__(self, display, x, y, sprite, directionY = -10, directionX = 0):
        self.sprite = sprite
        self.display = display
        self.directionY = directionY  
        self.directionX = directionX  
        self.instance = self.sprite.get_rect(topleft = (x, y))
        display.blit(sprite, self.instance)  
class Player:
    def __init__(self, display, x, y, sprite):
        self.sprite = sprite
        self.display = display
        self.instance = self.sprite.get_rect(topleft = (x, y))
        display.blit(sprite, self.instance)  
    def shoot(self, sprite):
        Bullet.Bullets.append(Bullet(self.display, self.instance.centerx - 2, self.instance.y, sprite))
        
class EnemyLevelOne(Player):
    def __init__(self, *args, **kwargs):
        Player.__init__(self, *args, **kwargs)
    def shoot(self, sprite):
        Bullet.Bullets.append(Bullet(self.display, self.instance.centerx - 2, self.instance.bottomleft[1], sprite, 10))

class EnemyLevelTwo(EnemyLevelOne):
    def __init__(self, *args, **kwargs):
        EnemyLevelOne.__init__(self, *args, **kwargs)
        self.is_active = False  
    def shoot(self, sprite):
        Bullet.Bullets.append(Bullet(self.display, self.instance.centerx - 2, self.instance.bottomleft[1],  sprite, 10, -1))
        Bullet.Bullets.append(Bullet(self.display, self.instance.centerx - 2, self.instance.bottomleft[1],  sprite, 10, 1))

class EnemyLevelThree(EnemyLevelTwo):
    def __init__(self, *args, **kwargs):
        EnemyLevelTwo.__init__(self, *args, **kwargs)
    def shoot(self, sprite):
        Bullet.Bullets.append(Bullet(self.display, self.instance.centerx - 2, self.instance.bottomleft[1], sprite, 10))
        Bullet.Bullets.append(Bullet(self.display, self.instance.centerx - 2, self.instance.bottomleft[1], sprite, 10, -1))
        Bullet.Bullets.append(Bullet(self.display, self.instance.centerx - 2, self.instance.bottomleft[1], sprite, 10, 1))
class Boss(EnemyLevelTwo): #Наследуемся от класса EnemyLevelTwo, так как нам необходима атрибута is_active
    def __init__(self, *args, **kwargs):
        EnemyLevelTwo.__init__(self, *args, **kwargs)
        self.hp = 100
    def shoot(self, sprite):
        Bullet.Bullets.append(Bullet(self.display, self.instance.centerx - 2, self.instance.bottomleft[1], sprite, 10, -2))
        Bullet.Bullets.append(Bullet(self.display, self.instance.centerx - 2, self.instance.bottomleft[1], sprite, 10, -1))
        Bullet.Bullets.append(Bullet(self.display, self.instance.centerx - 2, self.instance.bottomleft[1], sprite, 10))
        Bullet.Bullets.append(Bullet(self.display, self.instance.centerx - 2, self.instance.bottomleft[1], sprite, 10, 1))
        Bullet.Bullets.append(Bullet(self.display, self.instance.centerx - 2, self.instance.bottomleft[1], sprite, 10, 2))
def rotate(instance, angle):
    instance = pygame.transform.rotate(instance.sprite, angle)
    x, y = instance.instance.center
    instance.instance = instance.sprite.get_rect()
    instance.instance.center = (x, y)
#############################
player = Player(display, x, y, pygame.Surface((width, height)))

invaders = [[], [], []]
current_x = 5
for i in range(11):
    invaders[2].append(EnemyLevelThree(display, current_x, 5, pygame.Surface((40, 60))))
    invaders[1].append(EnemyLevelTwo(display, current_x, 75, pygame.Surface((40, 60))))
    invaders[0].append(EnemyLevelOne(display, current_x, 145, pygame.Surface((40, 60))))
    current_x += 45

clock = pygame.time.Clock()
run = True
while run:
    display.fill((255, 255, 255))
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and x < 50:
                pass
            elif event.key == pygame.K_RIGHT and x < 1200:
                pass
            if event.key == pygame.K_UP and len(Bullet.Bullets) < 10:
                 player.shoot(pygame.Surface((5, 5)))
#            if event.key == pygame.K_DOWN:  Vlad
        elif event.type == pygame.KEYUP:
            pass

    for bullet in Bullet.Bullets:
        if bullet.instance.y > 0 and 0 < bullet.instance.x < 1280:
            bullet.instance.y += bullet.directionY
            bullet.instance.x += bullet.directionX
        else:
            Bullet.Bullets.pop(Bullet.Bullets.index(bullet))
        display.blit(bullet.sprite, bullet.instance)
# Diana
        for row in invaders:
            for elem in row:
                if bullet.instance.colliderect(elem.instance):
                    row.remove(elem)
                    Bullet.Bullets.remove(bullet)

    for row in invaders:
        if row[-1] == None:
            row.pop(-1)
        for invader in row:
            display.blit(invader.sprite, invader.instance)
            
    if keys[pygame.K_LEFT]:
        player.instance.x -= 15
    if keys[pygame.K_RIGHT]:
        player.instance.x += 15
    display.blit(player.sprite, player.instance)
    pygame.display.update()
    clock.tick(30)


pygame.quit()

#Справка
"""
=В процессе=
1) Стрельба врагов
2) Попадание во врагов

=Изменения=:
1) Добалена фунция вращения объектов на экране pygame.transform.rotate() 
2) Добавлен класс босса

=ЧтоНужноСделать=
1) Маштабировать картинки врагов(github.com/MyersWannaCry/SpaceInvaders)
2) Логика босса

=Аргументация=
1)Нет ни логики, ни взаимодействия с врагами и боссом, так как мы это пока
не реализовываем, сам факт подстановки спрайта и возможность определения
сущностей
2)event'ы до сих пор не оформлены, так как анимаций пока нет
"""
