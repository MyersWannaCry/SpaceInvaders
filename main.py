import pygame

pygame.init()
background = pygame.display.set_mode((1280, 670))
pygame.display.set_caption('Space invaders')
x = 640  # корды нашей ракеты
y = 600
width = 40
height = 60
speed = 15
bullets = []
##########################
class Player:
    def __init__(self, display, x, y, width, height, sprite):
        self.sprite = sprite
        self.display = display
        self.instance = pygame.Rect(x, y, x + width, y + height)
        display.blit(sprite, self.instance)  #Должно быть в главном цикле
    def shoot(self, sprite):
        Bullet.Bullets.add(Bullet(self.display, self.instance.centerx - 7, self.instance.y, 5, 5, sprite))
        
class EnemyLevelOne(Player):
    def __init__(self, *args, **kwargs):
        Player.__init__(*args, **kwargs)
    def shoot(self, sprite):
        Bullet.Bullets.add(Bullet(self.display, self.instance.centerx - 7, self.instance.bottomleft[1], 5, 5, sprite, 2))

class EnemyLevelTwo(EnemyLevelOne):
    def __init__(self, *args, **kwargs):
        EnemyLevelOne.__init__(*args, **kwargs)
        self.is_active = False  #Для проверки активности ряда врагов
    def shoot(self, sprite):
        Bullet.Bullets.add(Bullet(self.display, self.instance.centerx - 7, self.instance.bottomleft[1], 5, 5, sprite, 2, -1))
        Bullet.Bullets.add(Bullet(self.display, self.instance.centerx - 7, self.instance.bottomleft[1], 5, 5, sprite, 2, 1))

class EnemyLevelThree(EnemyLevelTwo):
    def __init__(self, *args, **kwargs):
        EnemyLevelTwo.__init__(*args, **kwargs)
    def shoot(self, sprite):
        Bullet.Bullets.add(Bullet(self.display, self.instance.centerx - 7, self.instance.bottomleft[1], 5, 5, sprite, 2))
        Bullet.Bullets.add(Bullet(self.display, self.instance.centerx - 7, self.instance.bottomleft[1], 5, 5, sprite, 2, -1))
        Bullet.Bullets.add(Bullet(self.display, self.instance.centerx - 7, self.instance.bottomleft[1], 5, 5, sprite, 2, 1))
#############################
def draw_window():
    background.fill((0, 0, 0))
    pygame.draw.rect(background, (32, 178, 170), (x, y, width, height))
    for bullet in bullets:
        bullet.draw_bullet(background)
    pygame.display.update()


class pulya():
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.speed = 10

    def draw_bullet(self, background):
        pygame.draw.circle(background, self.color, (self.x, self.y - height), self.radius)


# глав цикл
run = True
while run:
    pygame.time.delay(35)
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False


    def shot():
        for bullet in bullets:
            if bullet.y > 0:
                bullet.y -= bullet.speed
            else:
                bullets.pop(bullets.index(bullet))

        if keys[pygame.K_SPACE]:
            if len(bullets) < 1:
                bullets.append(pulya(round(x + width // 2), round(y + height // 2), 5, (255, 0, 0)))


    if keys[pygame.K_LEFT] and x > 45:
        x -= speed
    if keys[pygame.K_RIGHT] and x < 1200:
        x += speed
    shot()
    draw_window()

pygame.quit()

