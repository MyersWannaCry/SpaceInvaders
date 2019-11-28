import pygame
from time import *
from random import randint, choice
from tkinter import *
pygame.init()
display = pygame.display.set_mode((1280, 670))
pygame.display.set_caption('Space invaders')
background = pygame.image.load('background_space.png')

winscreen = pygame.image.load('winscreen.jpg')
lossscreen = pygame.image.load('lossscreen.jpg')
menu_img = pygame.image.load('menu.jpg')

pygame.mixer.music.load('Megalovania.mp3')

a=pygame.event.get()

bullet_sprite_2 = pygame.image.load('bullet_2.png')
bullet_sprite_3 = pygame.image.load('bullet_in.png')
bullet_sprite_4 = pygame.image.load('Bullet_boss.png')
bullet_sprite_5 = pygame.image.load('bullet_3.png')
player_sprite = pygame.image.load('ship.png')
enemy1_sprite = pygame.image.load('vrag1.png')
enemy2_sprite = pygame.image.load('vrag2.png')
enemy3_sprite = pygame.image.load('vrag3.png')
boss_sprite = pygame.image.load('boss.png')
bonus_1 = pygame.image.load('chips_2.png')
bonus_2 = pygame.image.load('chips_3.png')
bonus_3 = pygame.image.load('chips_4.png')
bonus_4 = pygame.image.load('chips_5.png')
bonus_5 = pygame.image.load('chips_6.png')

smallfont = pygame.font.SysFont("verdana",25)
bigfont = pygame.font.SysFont("verdana",40)
white = (255, 255, 255)
black = (0, 0, 0)
points=0

def scoreboard():
    t =  open('scoreboard.txt' , 'r')
    window = Tk()
    window.title("Scoreboard")
    window.geometry("200x250")
    L = Label(window, text = t.read(), font=("Arial Bold", 20) )
    L.pack()
    window.mainloop()

def creds():  
    window = Tk()  
    window.title("Creds")
    window.geometry('400x250')
    window.resizable(False, False)
    window.call('wm', 'attributes', '.', '-topmost', '1')
    lbl = Label(window, text="Вадим Чуков\n  Богдан Крят   \n         Игорь Ярошенко   \n      Диана Фатеева   \n          Михаил Микаэлян   \n      Влад Золотоноша",
        font=("Arial Bold", 25))  
    lbl.grid(column=0, row=0)  
    window.mainloop()
    
def leave():
    text=bigfont.render("Exit" , True, black)
    display.blit(text,[600,550])
    
def score(score):
    text=smallfont.render("Score:" +str(score), True, white)
    display.blit(text,[1095,0])
    
def timer(timer):
    text=smallfont.render("Time:" +str(timer), True, white)
    display.blit(text,[1095,30])
    
def boss_hp(boss_hp):
    text=smallfont.render("Boss hp:" +str(boss_hp), True, white)
    display.blit(text,[1095,60])
    
def player_hp(player_hp):
    text=smallfont.render("Your hp:" +str(player_hp), True, white)
    display.blit(text,[1095,90])

class Bullet:
    Bullets = []
    Player = []
    def __init__(self, display, x, y, sprite, directionY=-5, directionX=0):
        self.sprite = sprite
        self.display = display
        self.directionY = directionY
        self.directionX = directionX
        self.instance = self.sprite.get_rect(center=(x, y))
        display.blit(self.sprite, self.instance)
    

class Player:
    def __init__(self, display, x, y, sprite):
        self.sprite = sprite
        self.display = display
        self.instance = self.sprite.get_rect(center=(x, y))
        self.win = False
        self.loss = False
        self.speed = 10
        self.normal_moving = True
        self.bullet_limit = 5
        self.bullet_limit_LevelThree=3
        self.damage = 1
        self.bullet_amount = 1
        self.bullet_counter = self.bullet_limit * self.bullet_amount
        self.hp = 3
        display.blit(self.sprite, self.instance)
        
    def shoot_1(self):
        Bullet.Player.append(Bullet(self.display, self.instance.centerx, self.instance.y, bullet_sprite_2))
    def shoot_2(self):
        Bullet.Player.append(Bullet(self.display, self.instance.centerx, self.instance.y, bullet_sprite_5, -5, -1))
        Bullet.Player.append(Bullet(self.display, self.instance.centerx, self.instance.y, bullet_sprite_5, -5, 1))
        
    def shoot_3(self):
        Bullet.Player.append(Bullet(self.display, self.instance.centerx, self.instance.y, bullet_sprite_5, -5, -1))
        Bullet.Player.append(Bullet(self.display, self.instance.centerx, self.instance.y, bullet_sprite_5))
        Bullet.Player.append(Bullet(self.display, self.instance.centerx, self.instance.y, bullet_sprite_5, -5, 1))
        
    def shoot_4(self):
        Bullet.Player.append(Bullet(self.display, self.instance.centerx, self.instance.y, bullet_sprite_5, -5, -2))
        Bullet.Player.append(Bullet(self.display, self.instance.centerx, self.instance.y, bullet_sprite_5, -5, -1))
        Bullet.Player.append(Bullet(self.display, self.instance.centerx, self.instance.y, bullet_sprite_5, -5, 1))
        Bullet.Player.append(Bullet(self.display, self.instance.centerx, self.instance.y, bullet_sprite_5, -5, 2))
        
    def shoot_5(self):
        Bullet.Player.append(Bullet(self.display, self.instance.centerx, self.instance.y, bullet_sprite_5, -5, -2))
        Bullet.Player.append(Bullet(self.display, self.instance.centerx, self.instance.y, bullet_sprite_5, -5, -1))
        Bullet.Player.append(Bullet(self.display, self.instance.centerx, self.instance.y, bullet_sprite_5))
        Bullet.Player.append(Bullet(self.display, self.instance.centerx, self.instance.y, bullet_sprite_5, -5, 1))
        Bullet.Player.append(Bullet(self.display, self.instance.centerx, self.instance.y, bullet_sprite_5, -5, 2))
        
    def cleanup(self):
        self.instance.x = 3000
        self.instance.y = 0


class EnemyLevelOne(Player):
    def __init__(self, display, x, y, sprite):
        Player.__init__(self, display, x, y, sprite)
        self.instance = self.sprite.get_rect(topleft=(x, y))
        self.shoot_time = randint(5, 10)
      
        
    def shoot(self):
        Bullet.Bullets.append(Bullet(self.display, self.instance.centerx, self.instance.bottomleft[1], bullet_sprite_3, 5))

class EnemyLevelTwo(EnemyLevelOne):
    def __init__(self, *args, **kwargs):
        EnemyLevelOne.__init__(self, *args, **kwargs)
        self.is_active = False
        
    def shoot(self):
        Bullet.Bullets.append(Bullet(self.display, self.instance.centerx, self.instance.bottomleft[1], bullet_sprite_3, 5, -1))
        Bullet.Bullets.append(Bullet(self.display, self.instance.centerx, self.instance.bottomleft[1], bullet_sprite_3, 5, 1))


class EnemyLevelThree(EnemyLevelTwo):
    def __init__(self, *args, **kwargs):
        EnemyLevelTwo.__init__(self, *args, **kwargs)
        
    def shoot(self):
        Bullet.Bullets.append(Bullet(self.display, self.instance.centerx, self.instance.bottomleft[1], bullet_sprite_3, 5))
        Bullet.Bullets.append(
            Bullet(self.display, self.instance.centerx, self.instance.bottomleft[1], bullet_sprite_3, 5, -1))
        Bullet.Bullets.append(
            Bullet(self.display, self.instance.centerx, self.instance.bottomleft[1], bullet_sprite_3, 5, 1))


class Boss(EnemyLevelTwo):
    def __init__(self, display, x, y, sprite):
        EnemyLevelTwo.__init__(self, display, x, y, sprite)
        self.sprite = sprite
        self.instance = self.sprite.get_rect(topleft=(x, y))
        self.hp = 100
        self.speed = 5
        self.shoot_time = randint(1, 2)
        self.solo_movement = False
        self.moving = False
        self.move = True
        self.down = False
        
    def shoot(self):
        Bullet.Bullets.append(
            Bullet(self.display, self.instance.centerx, self.instance.bottomleft[1], bullet_sprite_4, 10, -2))
        Bullet.Bullets.append(
            Bullet(self.display, self.instance.centerx, self.instance.bottomleft[1], bullet_sprite_4, 10, -1))
        Bullet.Bullets.append(Bullet(self.display, self.instance.centerx, self.instance.bottomleft[1], bullet_sprite_4, 10))
        Bullet.Bullets.append(
            Bullet(self.display, self.instance.centerx, self.instance.bottomleft[1], bullet_sprite_4, 10, 1))
        Bullet.Bullets.append(
            Bullet(self.display, self.instance.centerx, self.instance.bottomleft[1], bullet_sprite_4, 10, 2))
        
    def cleanup(self):
        self.instance.x=3000
        self.instance.y=0

player = Player(display, 640, 600, player_sprite)
boss = Boss(display, 545, -200, boss_sprite)
class Bonus:
    def __init__(self, display, x, stun_time = 10):
        self.display = display
        self.stun_time = stun_time
        self.is_active = False
        self.function = choice([self.damage_increase, self.change_direction, self.hp_increase, self.speed_increase, self.bullet_increase, self.speed_decrease, self.bullet_limit_increase])
        if self.function == self.hp_increase:
            self.sprite = bonus_1
        elif self.function == self.change_direction:
            self.sprite = bonus_2
        elif self.function == self.speed_decrease:
            self.sprite = bonus_3
        elif self.function == self.damage_increase or self.function == self.bullet_limit_increase or self.function == self.bullet_increase:
            self.sprite = bonus_4
        elif self.function == self.speed_increase:
            self.sprite = bonus_5
        self.instance = self.sprite.get_rect(center = (x, -40))
    def hp_increase(self, player):
        player.hp += 1
    def speed_increase(self, player):
        player.speed += 5
    def bullet_increase(self, player):
        player.bullet_amount += 1
    def damage_increase(self, player):
        player.damage += 1
    def bullet_limit_increase(self, player):
        player.bullet_limit += 3
    def speed_decrease(self, player):
        player.speed -= 5
    def change_direction(self, player):
        player.normal_moving = not player.normal_moving
    def cleanup():
        self.instance.x = 3000
        self.instance.y = 2000

invaders = [[], [], []]
invader_speed = 5
current_x = 5
clock = pygame.time.Clock()
down = False
move = False
new_time = True
run = True
main= True
menu=True
bonus = Bonus(display, randint(50, 1230))
while main:
    while menu:
        display.blit(menu_img,(0,0))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pos()[0] >= 12 and pygame.mouse.get_pos()[1] >= 166:
                    if pygame.mouse.get_pos()[0] <= 227 and pygame.mouse.get_pos()[1] <= 241:
                        pygame.mixer.music.play(-1)
                        invader_speed = 5
                        player.hp = 3
                        player.speed = 10
                        boss.hp = 100
                        boss.speed = 5
                        for i in range(7):
                            invaders[2].append(EnemyLevelThree(display, current_x, 5, enemy3_sprite))
                            invaders[1].append(EnemyLevelTwo(display, current_x, 75, enemy2_sprite))
                            invaders[0].append(EnemyLevelOne(display, current_x, 145, enemy1_sprite))
                            current_x += 45
                            
                        del current_x
                        start_time=time()
                        menu = False
                        run = True
                if pygame.mouse.get_pos()[0] >= 227 and pygame.mouse.get_pos()[1] >= 166:
                    if pygame.mouse.get_pos()[0] <= 442 and pygame.mouse.get_pos()[1] <= 241:
                        pygame.mixer.music.play(-1)
                        invader_speed = 7
                        player.hp = 2
                        player.speed = 7
                        boss.hp = 250
                        boss.speed = 7
                        for i in range(11):
                            invaders[2].append(EnemyLevelThree(display, current_x, 5, enemy3_sprite))
                            invaders[1].append(EnemyLevelTwo(display, current_x, 75, enemy2_sprite))
                            invaders[0].append(EnemyLevelOne(display, current_x, 145, enemy1_sprite))
                            current_x += 45
                            
                        del current_x
                        start_time=time()
                        menu = False
                        run = True
                if pygame.mouse.get_pos()[0] >= 442 and pygame.mouse.get_pos()[1] >= 166:
                    if pygame.mouse.get_pos()[0] <= 657 and pygame.mouse.get_pos()[1] <= 241:
                        pygame.mixer.music.play(-1)
                        invader_speed = 10
                        player.hp = 1
                        player.speed = 5
                        boss.hp = 500
                        boss.speed = 10
                        for i in range(15):
                            invaders[2].append(EnemyLevelThree(display, current_x, 5, enemy3_sprite))
                            invaders[1].append(EnemyLevelTwo(display, current_x, 75, enemy2_sprite))
                            invaders[0].append(EnemyLevelOne(display, current_x, 145, enemy1_sprite))
                            current_x += 45
                            
                        del current_x
                        start_time=time()
                        menu = False
                        run = True
                if pygame.mouse.get_pos()[0] >= 12 and pygame.mouse.get_pos()[1] >= 285:
                    if pygame.mouse.get_pos()[0] <= 355 and pygame.mouse.get_pos()[1] <= 360:
                        scoreboard()
                if pygame.mouse.get_pos()[0] >= 12 and pygame.mouse.get_pos()[1] >= 391:
                    if pygame.mouse.get_pos()[0] <= 210 and pygame.mouse.get_pos()[1] <= 466:
                        creds()
                if pygame.mouse.get_pos()[0] >= 12 and pygame.mouse.get_pos()[1] >= 497:
                    if pygame.mouse.get_pos()[0] <= 180 and pygame.mouse.get_pos()[1] <= 572:
                        run = False
                        main = False
                        menu = False                        
                if event.type == pygame.QUIT:
                    run = False
                    main = False
                    menu = False
    while run:
        pygame.display.flip()   
        if player.win == True:
            display.blit(winscreen,(0,0))
            player.cleanup()
            boss.cleanup()
            invaders = []
            Bullet.Bullets = []
            quit_button = pygame.draw.rect(display,(244,0,0),(300,550,700,60));
            leave()
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pos()[0] >= 300 and pygame.mouse.get_pos()[1] >= 550:
                        if pygame.mouse.get_pos()[0] <= 1000 and pygame.mouse.get_pos()[1] <= 710:
                            run = False
                            main = False
                            menu = False
                    #if pygame.mouse.get_pos()[0] >= 800 and pygame.mouse.get_pos()[1] >= 550:
                        #if pygame.mouse.get_pos()[0] <= 1000 and pygame.mouse.get_pos()[1] <= 710:
                            #boss_hp = boss.hp_LevelOne
                           
        elif player.loss == True:
            display.blit(lossscreen,(0,0))
            player.cleanup()
            boss.cleanup()
            invaders=[]
            Bullet.Bullets = []
            quit_button = pygame.draw.rect(display,(244,0,0),(300,550,700,60));
            leave()
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pos()[0] >= 300 and pygame.mouse.get_pos()[1] >= 550:
                        if pygame.mouse.get_pos()[0] <= 1000 and pygame.mouse.get_pos()[1] <= 710:
                            run = False
                            main = False
                            menu = False
        else:
            display.blit(background,(0,0))
            keys = pygame.key.get_pressed()
            player.bullet_counter = player.bullet_limit * player.bullet_amount
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        pass
                    elif event.key == pygame.K_RIGHT:
                        pass
                    if not boss.solo_movement and event.key == pygame.K_UP and len(Bullet.Player) < player.bullet_counter:
                        if player.bullet_amount == 1:
                            player.shoot_1()
                        elif player.bullet_amount == 2:
                            player.shoot_2()
                        elif player.bullet_amount == 3:
                            player.shoot_3()
                        elif player.bullet_amount == 4:
                            player.shoot_4()
                        elif player.bullet_amount == 5:
                            player.shoot_5()
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
                        boss.solo_movement = True
                if None in row and invaders.index(row) != len(invaders) - 1:
                    for invader in invaders[invaders.index(row) + 1]:
                        if invader is not None:
                            invader.is_active = True
                for elem in row:
                    if elem != None:
                        if elem.instance.colliderect(player.instance) or elem.instance.y>=670:
                            player.loss = True
                        if elem.instance.x >= 1280 - elem.instance.width:
                            move = True
                            down = True
                        if elem.instance.x <= 0:
                            move = False
                            down = True
                        if move:
                            elem.instance.x -= invader_speed
                        else:
                            elem.instance.x += invader_speed

                        if int(time() - start_time) % elem.shoot_time == 0 and int(time() - start_time) != 0 and (invaders.index(row) == 0 or elem.is_active):
                            elem.shoot()
                            elem.shoot_time += randint(5, 10)

                    if down:
                        for row in invaders:
                            for elem in row:
                                if elem != None:
                                    elem.instance.y += 15
                        down = False
                        
            display.blit(boss.sprite, boss.instance)
            if boss.solo_movement and boss.instance.y < 10:
                boss.instance.y += 1
                boss.moving = True
            else:
                boss.solo_movement = False
                if boss.moving:
                    boss_time = time()
                    boss.is_active = True
                    new_time = True
                    boss.moving = False
            if boss.is_active:
                if boss.instance.x >= 1280 - boss.instance.width:
                    boss.move = True
                    boss.down = True
                elif boss.instance.x <= 0:
                    boss.move = False
                    boss.down = True
                if boss.move:
                    boss.instance.x -= boss.speed
                else:
                    boss.instance.x += boss.speed
                if boss.down:
                    boss.instance.y += 15
                    boss.down = False
                if int(time() - boss_time) % boss.shoot_time == 0 and int(time() - boss_time) != 0:
                    boss.shoot()
                    boss.shoot_time += randint(1, 2)
                if boss.instance.y>=640-boss.instance.height or boss.instance.colliderect(player.instance):
                    player.loss = True


            for bullet in Bullet.Bullets + Bullet.Player:
                if boss.is_active:
                    if bullet.instance.colliderect(boss.instance) and bullet in Bullet.Player:
                        boss.hp -= player.damage
                        Bullet.Player.remove(bullet)
                        if boss.hp <= 0:
                            player.win = True

                if bullet.instance.y > 0 and bullet.instance.bottomleft[1] < 1280:
                    bullet.instance.y += bullet.directionY
                    bullet.instance.x += bullet.directionX
                else:
                    if bullet in Bullet.Player:
                        Bullet.Player.remove(bullet)
                    elif bullet in Bullet.Bullets:
                        Bullet.Bullets.remove(bullet)
                display.blit(bullet.sprite, bullet.instance)
                if not boss.solo_movement and bullet in Bullet.Bullets and bullet.instance.colliderect(player.instance):
                    player.hp -= 1
                    Bullet.Bullets.remove(bullet)
                    if player.hp <= 0:
                        player.loss = True
                for row in invaders:
                    for elem in row:
                        if bullet in Bullet.Player and elem != None and bullet.instance.colliderect(elem.instance):
                            row[row.index(elem)] = None
                            Bullet.Player.remove(bullet)
                            invader_speed += 0.5
                            points+=100
            display.blit(bonus.sprite, bonus.instance)
            if not bonus.is_active and int(time() - start_time) % bonus.stun_time == 0:
                bonus.is_active = True
            if bonus.is_active and not boss.solo_movement:
                if bonus.instance.topleft[1] <= 670:
                    bonus.instance.y += 3
                else:
                    if not player.loss:
                        bonus = Bonus(display, randint(50, 1230))
                if bonus.instance.colliderect(player.instance):
                    bonus.function(player)
                    bonus = Bonus(display, randint(50, 1230))
            if player.normal_moving:
                if not boss.solo_movement and keys[pygame.K_LEFT] and player.instance.x > 0:
                    player.instance.x -= player.speed
                if not boss.solo_movement and keys[pygame.K_RIGHT] and player.instance.x < 1280 - player.instance.width:
                    player.instance.x += player.speed
            else:
                if not boss.solo_movement and keys[pygame.K_LEFT] and player.instance.x < 1280 - player.instance.width:
                    player.instance.x += player.speed
                if not boss.solo_movement and keys[pygame.K_RIGHT] and player.instance.x > 0:
                    player.instance.x -= player.speed

            if player.win != True and player.loss != True:
                score(points)
                timer(str(round(time()-start_time))+" sec")
                boss_hp(boss.hp)
                player_hp(player.hp)
            else:
                pygame.mixer.music.pause()
                Bullet.Bullets.clear()
                Bullet.Player.clear()
            display.blit(player.sprite, player.instance)
    pygame.display.update()
    clock.tick(120)
    pygame.quit()
