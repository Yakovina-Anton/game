from pygame import *
from random import *
window = display.set_mode((1920, 1880), FULLSCREEN)
screen_size = window.get_rect().size

background = transform.scale(image.load('bg.jpg'), screen_size)

clock = time.Clock()
font.init()
myFont = font.Font(None, 36)

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        # каждый спрайт должен хранить свойство image - изображение
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        # каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Bullet(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__(player_image, player_x, player_y, size_x, size_y, player_speed)

    def move(self):
        global catchFire
        self.rect.y -= self.speed

        if self.rect.y < 0:
            if self in myPlayer.bulletList:
                myPlayer.bulletList.remove(self)

        for fire in enemyList:
            if self.rect.colliderect(fire.rect):
                enemyList.remove(fire)
                catchFire += 1
                if self in myPlayer.bulletList:
                    myPlayer.bulletList.remove(self)




class Player(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__(player_image, player_x, player_y, size_x, size_y, player_speed)
        self.bulletList = []
        self.reloadCount = 0
        self.boost_1 = 0

    def move(self):
        if self.reloadCount > 0:
            self.reloadCount -= 1
        if self.boost_1 > 0:
            self.boost_1 -= 1

        keys = key.get_pressed()
        if keys[K_LEFT]:
            self.rect.x -= self.speed
        if keys[K_RIGHT]:
            self.rect.x += self.speed
        if keys[K_SPACE]:
            if self.reloadCount == 0:
                self.bulletList.append(Bullet('water.png', self.rect.x, self.rect.y, 25, 25, 1))
                if self.boost_1 > 0:
                    self.reloadCount = 10
                else:
                    self.reloadCount = 50

    def giveBoost(self, boosterType):
        if boosterType == 1:
            self.boost_1 += 360


class Enemy(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__(player_image, player_x, player_y, size_x, size_y, player_speed)
    def move(self):
        global missFire
        self.rect.y += self.speed
        if self.rect.y > screen_size[1]:
            enemyList.remove(self)
            missFire += 1

class Booster(GameSprite):
    def __init__(self, image, x, y, size_x, size_y, speed, boosterType):
        super().__init__(image, x, y, size_x, size_y, speed)
        self.boosterType = boosterType
    def move(self):
        self.rect.y += self.speed
        if self.rect.y > screen_size[1]:
            boosterList.remove(self)

        if self.rect.colliderect(myPlayer.rect):
            myPlayer.giveBoost(self.boosterType)
            boosterList.remove(self)


myPlayer = Player('stone.png', (screen_size[0]/2)-(50/2), screen_size[1]-(screen_size[1]/10), 50, 50, 5)

enemyList = []
boosterList = []


def spawnFire():
    value = randint(1, 5)
    for i in range(value):
        fire = Enemy('fire.png', randint(0, screen_size[0]), 0, 40, 40, 3)
        enemyList.append(fire)

def spawnBoost():
    boosterList.append(Booster('camp.png', randint(0, screen_size[0]), 0, 40, 40, 1, 1))


run = True
finish = False
screenCount = 0
screenBoostCount = 0

catchFire = 0
missFire = 0

while run:
    display.update()
    for e in event.get():
        if e.type == QUIT:
            run = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                if finish == True:
                    catchFire = 0
                    missFire = 0
                    enemyList = []
                    myPlayer.bulletList = []
                    finish = False

  #  if missFire >= 10:
  #      window.fill((0, 0, 0))
  #      looseText = myFont.render("Вы набрали: " + str(catchFire) + " очков", 1, (255, 255, 255))
  #      window.blit(looseText, (screen_size[0]/2-looseText.get_size()[0]/2, screen_size[1]/2-looseText.get_size()[1]/2))
  #      looseText2 = myFont.render("Нажмите пробел для рестарта", 1, (255, 255, 255))
  #      window.blit(looseText2, (screen_size[0]/2-looseText2.get_size()[0]/2, screen_size[1]/2-looseText2.get_size()[1]/2+30))
  #      finish = True

    if finish == False:
        window.blit(background, (0, 0))

        if screenBoostCount == 0:
            screenBoostCount = randint(120, 600)
            spawnBoost()
        screenBoostCount -= 1

        screenCount += 1
        if screenCount == 60:
            spawnFire()
            screenCount = 0

        missText = myFont.render("Пропущенно:" + str(missFire), 1, (0, 0, 0))
        window.blit(missText, (10, 20))

        catchText = myFont.render("Потушено:" + str(catchFire), 1, (0, 0, 0))
        window.blit(catchText, (10, 50))

        myPlayer.move()
        for e in enemyList:
            e.move()
        for b in boosterList:
            b.move()

        myPlayer.reset()
        for p in myPlayer.bulletList:
            p.move()
            p.reset()
        for e in enemyList:
            e.reset()
        for b in boosterList:
            b.reset()
    clock.tick(120)