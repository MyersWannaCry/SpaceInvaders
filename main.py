import pygame

pygame.init()
display = pygame.display.set_mode((1280, 670))
pygame.display.set_caption('Space invaders')
background = pygame.image.load('background_space.png')
pygame.mixer.music.load('Megalovania.mp3')
pygame.mixer.music.play(-1)
#-----------------------------------------------Igoryasik
smallfont = pygame.font.SysFont("verdana",25)
white = (255,255,255)
points=0
def score(score):
    text=smallfont.render("Score:" +str(score), True, white)
    display.blit(text,[1150,0])
#-----------------------------------------------
##########################
class Bullet:
    Bullets = []
    Player = []  # new

    def __init__(self, display, x, y, directionY=-5, directionX=0):
        self.sprite = pygame.image.load('bullet.png')
        self.display = display
        self.directionY = directionY
        self.directionX = directionX
        self.instance = self.sprite.get_rect(topleft=(x, y))
        display.blit(self.sprite, self.instance)

class Player:
    def __init__(self, display, x, y):
        self.sprite = pygame.image.load('ship.png')
        self.display = display
        self.instance = self.sprite.get_rect(center=(x, y))
        display.blit(self.sprite, self.instance)
    def shoot(self):
        Bullet.Player.append(Bullet(self.display, self.instance.centerx - 5, self.instance.y))


class EnemyLevelOne:
    def __init__(self, display, x, y):
        self.sprite = pygame.image.load('vrag1.png')
        self.display = display
        self.instance = self.sprite.get_rect(topleft=(x, y))
        display.blit(self.sprite, self.instance)
    def shoot(self):
        Bullet.Bullets.append(Bullet(self.display, self.instance.centerx - 6, self.instance.bottomleft[1], 5))


class EnemyLevelTwo(EnemyLevelOne):
    def __init__(self, *args, **kwargs):
        EnemyLevelOne.__init__(self, *args, **kwargs)
        self.is_active = False
        self.sprite = pygame.image.load('vrag2.png')
    def shoot(self):
        Bullet.Bullets.append(Bullet(self.display, self.instance.centerx - 5, self.instance.bottomleft[1], 5, -1))
        Bullet.Bullets.append(Bullet(self.display, self.instance.centerx - 5, self.instance.bottomleft[1], 5, 1))


class EnemyLevelThree(EnemyLevelTwo):
    def __init__(self, *args, **kwargs):
        EnemyLevelTwo.__init__(self, *args, **kwargs)
        self.sprite = pygame.image.load('vrag3.png')
    def shoot(self):
        Bullet.Bullets.append(Bullet(self.display, self.instance.centerx - 6.5, self.instance.bottomleft[1], 5))
        Bullet.Bullets.append(
            Bullet(self.display, self.instance.centerx - 6.5, self.instance.bottomleft[1], 5, -1))
        Bullet.Bullets.append(
            Bullet(self.display, self.instance.centerx - 6.5, self.instance.bottomleft[1], 5, 1))


class Boss(EnemyLevelTwo):
    def __init__(self, *args, **kwargs):
        EnemyLevelTwo.__init__(self, *args, **kwargs)
        self.hp = 100
    def shoot(self):
        Bullet.Bullets.append(
            Bullet(self.display, self.instance.centerx - 6.5, self.instance.bottomleft[1], 10, -2))
        Bullet.Bullets.append(
            Bullet(self.display, self.instance.centerx - 6.5, self.instance.bottomleft[1], 10, -1))
        Bullet.Bullets.append(Bullet(self.display, self.instance.centerx - 6.5, self.instance.bottomleft[1], sprite, 10))
        Bullet.Bullets.append(
            Bullet(self.display, self.instance.centerx - 6.5, self.instance.bottomleft[1], 10, 1))
        Bullet.Bullets.append(
            Bullet(self.display, self.instance.centerx - 6.5, self.instance.bottomleft[1], 10, 2))

#############################
player = Player(display, 640, 600)
#boss = Boss(display, x, y)

invaders = [[], [], []]
current_x = 5
for i in range(11):
    invaders[2].append(EnemyLevelThree(display, current_x, 5))
    invaders[1].append(EnemyLevelTwo(display, current_x, 75))
    invaders[0].append(EnemyLevelOne(display, current_x, 145))
    current_x += 45
del current_x

clock = pygame.time.Clock()
#____________________________Diana,movement
down = False
move = False
#____________________________
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
            if event.key == pygame.K_UP and len(Bullet.Player) < 10:
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
            if len(invaders) == 0:
                boss.is_active = True
        if None in row and invaders.index(row) != len(invaders) - 1:
            for invader in invaders[invaders.index(row) + 1]:
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
        #---------------------------------------------------------Igoryasik
                    points+=1
        # ________________________________________________________Diana movement
        for row in invaders:
            for elem in row:
                if row[row.index(elem)] != None:
                    if row[row.index(elem)].instance.x >= 1240:
                        move = True
                        down = True
                    if row[row.index(elem)].instance.x < 0:
                        move = False
                        down = True
                    if move:
                        row[row.index(elem)].instance.x -= 5
                    if move == False:
                        row[row.index(elem)].instance.x += 5
        if down:
            for row in invaders:
                for elem in row:
                    if row[row.index(elem)] != None:
                        row[row.index(elem)].instance.y += 15
            down = False
    # ________________________________________________________

    if keys[pygame.K_LEFT] and player.instance.x > 0:
        player.instance.x -= 10
    if keys[pygame.K_RIGHT] and player.instance.x < 1280 - player.instance.width:
        player.instance.x += 10
    if keys[pygame.K_DOWN]:
        invaders[0][0].shoot()
        invaders[1][4].shoot()
        invaders[2][10].shoot()
   #-----------------------------------------Igoryasik
    score(points)
    #----------------------------------------- 
    display.blit(player.sprite, player.instance)
    pygame.display.update()
    clock.tick(60)

    '''
    for row in invaders:
            for elem in row:
                if row[row.index(elem)]!=None: 
                    if row[row.index(elem)].instance.x>=1220:
                        move = True
                        down = True
                    if row[row.index(elem)].instance.x<20:
                        move = False
                        down = True
                    if move :
                        row[row.index(elem)].instance.x-=5
                    if move == False:
                        row[row.index(elem)].instance.x+=5
        if down:
            for row in invaders:
                for elem in row:
                    if row[row.index(elem)]!=None:
                        row[row.index(elem)].instance.y+=30
            down = False




    for row in invaders:
            for elem in row:
                if row[row.index(elem)]!=None and row[row.index(elem)].instance.x>=1220:
                    move = True
                    down = True
                if row[row.index(elem)]!=None and row[row.index(elem)].instance.x<20:
                    move = False
                    down = True
                if move and row[row.index(elem)]!=None:
                    row[row.index(elem)].instance.x-=5
                if move == False and row[row.index(elem)]!=None:
                    row[row.index(elem)].instance.x+=5
        if down:
            for row in invaders:
                for elem in row:
                    if row[row.index(elem)]!=None:
                        row[row.index(elem)].instance.y+=30
            down = False



    for row in invaders:
                for elem in row:
                    if row[row.index(elem)]!=None and row[row.index(elem)].instance.x<1200:
                        row[row.index(elem)].instance.x+=1'''

pygame.quit()
