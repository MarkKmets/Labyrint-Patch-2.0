#підключаємо модуль
from time import *
from pygame import *
#змінні з кольором
green=(0,255,0)
#музика
mixer.init()
mixer.music.load('main.mp3')
mixer.music.play()
over=mixer.Sound('over.wav')
#створення та іменування вікна
width=1050
height=750
window=display.set_mode((width,height))
display.set_caption('Лабіринт')

#змінні прапорці
bullets=sprite.Group()
finish = False
play=True
#класи
class GameSprite(sprite.Sprite):
    def __init__(self,x,y,width,height,name):
        super().__init__()
        self.image=transform.scale(image.load(name),(width,height))
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
    def draw(self):
        window.blit(self.image,(self.rect.x,self.rect.y))
class Player(GameSprite):
    def __init__(self,x,y,width,height,x_speed,y_speed,name):
        GameSprite.__init__(self,x,y,width,height,name)
        self.x_speed=x_speed
        self.y_speed=y_speed
    def update(self):
        if ghost.rect.x <= width-50 and ghost.x_speed > 0 or ghost.rect.x >= 0 and ghost.x_speed < 0:
            self.rect.x += self.x_speed
        touched = sprite.spritecollide(self, walls, False)
        if self.x_speed > 0:
            for p in touched:
                self.rect.right = min(self.rect.right, p.rect.left)
        elif self.x_speed < 0:
            for p in touched:
                self.rect.left = max(self.rect.left, p.rect.right)
        if ghost.rect.y <= height-50 and ghost.y_speed > 0 or ghost.rect.y >= 0 and ghost.y_speed < 0:
            self.rect.y += self.y_speed
        touched = sprite.spritecollide(self, walls, False)
        if self.y_speed > 0:
            for p in touched:
                self.y_speed = 0
                if p.rect.top < self.rect.bottom:
                    self.rect.bottom = p.rect.top
        elif self.y_speed < 0:
            for p in touched:
                self.y_speed = 0
                self.rect.top = max(self.rect.top, p.rect.bottom)
    def fire(self):
        bullets.add(Bullet(self.rect.right,self.rect.centery,15,20,"bullet.png",15))

        
class Enemy(GameSprite):
    def __init__(self,x,y,width,height,name,x1,x2,side):
        GameSprite.__init__(self,x,y,width,height,name)
        self.start=x1
        self.end=x2
        self.speed=5
        self.side=side
    def update(self):
        if self.rect.x <=self.start:
            self.side='right'
        elif self.rect.x >=self.end:
            self.side='left'
        if self.side=='left':
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed

class Bullet(GameSprite):
    def __init__(self,x,y,width,height,name,speed):
        GameSprite.__init__(self,x,y,width,height,name)
        self.speed=speed
    def update(self):
        self.rect.x += self.speed
        if self.rect.x > width+10:
            self.kill()



#створення гравця
picture=GameSprite(0,0,width,height,"display.jpg")       
ghost=Player(75,610,50,50,0,0,"ghost.png")
final=GameSprite(900,600,75,75,'door.png')
#створення демонів
demons=sprite.Group()
demons.add(Enemy(155,10,50,60,'enemy.png',150,850,'right'))
demons.add(Enemy(230,160,50,60,'enemy.png',225,775,'right'))
demons.add(Enemy(5,310,50,60,'enemy.png',0,325,'right'))
#створення стін
walls=sprite.Group()
walls.add(GameSprite(0,450,225,75,"wall2.png"))
walls.add(GameSprite(225,675,225,75,"wall2.png"))
walls.add(GameSprite(450,675,225,75,"wall2.png"))
walls.add(GameSprite(375,525,225,75,"wall2.png"))
walls.add(GameSprite(225,75,225,75,"wall2.png"))
walls.add(GameSprite(225,225,225,75,"wall2.png"))
walls.add(GameSprite(450,75,225,75,"wall2.png"))
walls.add(GameSprite(675,75,225,75,"wall2.png"))
walls.add(GameSprite(825,450,225,75,"wall2.png"))
walls.add(GameSprite(525,225,225,75,"wall2.png"))
walls.add(GameSprite(225,375,75,225,"wall1.png"))
walls.add(GameSprite(675,300,75,225,"wall1.png"))
walls.add(GameSprite(375,300,75,225,"wall1.png"))
walls.add(GameSprite(525,300,75,225,"wall1.png"))
walls.add(GameSprite(150,75,75,225,"wall1.png"))
walls.add(GameSprite(825,150,75,225,"wall1.png"))
secretwall=GameSprite(675,525,75,225,"wall1.png")

#основний ігровий цикл
while play: 
    #обробка подій
    for e in event.get():
        if e.type == QUIT:
            play=False
        elif e.type==KEYDOWN:
            if e.key==K_LEFT:
                ghost.x_speed=-7
            elif e.key==K_RIGHT:
                ghost.x_speed=7
            elif e.key==K_UP:
                ghost.y_speed=-7
            elif e.key==K_DOWN:
                ghost.y_speed=7
            elif e.key==K_SPACE:
                ghost.fire()
        elif e.type==KEYUP:
            if e.key==K_LEFT:
                ghost.x_speed=0
            elif e.key==K_RIGHT:
                ghost.x_speed=0
            elif e.key==K_UP:
                ghost.y_speed=0
            elif e.key==K_DOWN:
                ghost.y_speed=0
    if not finish:
        picture.draw()
        ghost.draw()
        walls.draw(window)
        demons.draw(window)
        bullets.draw(window)
        secretwall.draw()
        bullets.update()
        demons.update()
        ghost.update()
        final.draw()
    sprite.groupcollide(bullets,walls,True,False)
    sprite.groupcollide(bullets,demons,True,True)

    if sprite.spritecollide(ghost, demons, False):
        finish = True
        mixer.music.stop()
        over.play()
        # обчислюємо ставлення
        img = image.load('game_over.png')
        window.blit(transform.scale(img, (width, height)), (0, 0))
        display.update()
        sleep(30)
        break

    if sprite.collide_rect(ghost, final):
        finish = True
        img = image.load('winner.png')
        window.blit(transform.scale(img, (width, height)), (0, 0))
        display.update()
        sleep(30)
        break
    # оновлення сцени
    time.delay(30)
    display.update()
display.update()
