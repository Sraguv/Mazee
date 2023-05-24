from pygame import *

LIGHT_GREEN = (200, 255, 200)
LIGHT_RED = (250, 128, 114)
GREEN = (0, 255, 51)
RED = (255,0,0)
TEAL = (0,128,128)
YELLOW = (255,255,0)
CYAN = (200,255,255)
MAGENTA = (255,0,255)
SILVER = (192,192,192)
NAVY = (10, 55, 100)

window = display.set_mode((700, 500))
window.fill(NAVY)
display.set_caption('Replika')
back = (NAVY)
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
p1 = GameSprite('walls.png', 70, 100, 141, 105)
p2 = GameSprite('walls.png', 120, 5, 141, 105)
p3 = GameSprite('walls_vert.png', 140, 25, 105, 141)
p4 = GameSprite('walls_vert.png', 180, 60, 105, 141)
final = GameSprite('princess.png', 600, 400, 60, 85)

class Player(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_x_speed, player_y_speed):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.x_speed = player_x_speed
        self.y_speed = player_y_speed
    def update(self):
        if player.rect.x <= 700 - 80 and player.x_speed > 0 or player.rect.x >= 0 and player.x_speed < 0:
            self.rect.x += self.x_speed
        platforms_touched = sprite.spritecollide(self, barriers, False)
        if self.x_speed > 0:
            for p in platforms_touched:
                self.rect.right = min(self.rect.right, p.rect.left)
        elif self.x_speed < 0:
            for p in platforms_touched:
                self.rect.left = max(self.rect.left, p.rect.right)
        if player.rect.y <= 700 - 80 and player.y_speed > 0 or player.rect.y >= 0 and player.y_speed < 0:
            self.rect.y += self.y_speed
        platforms_touched = sprite.spritecollide(self, barriers, False)
        if self.y_speed > 0: 
            for p in platforms_touched:
                self.rect.bottom = min(self.rect.bottom, p.rect.top)
        elif self.y_speed < 0:
            for p in platforms_touched:
                self.rect.top = max(self.rect.top, p.rect.bottom)
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.right, self.rect.centery, 25, 20, 15)
        bullets.add(bullet)
player = Player('player.png', 80, 80, 80, 80, 0, 0)

class Enemy(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, speed):
        super().__init__(player_image, player_x, player_y, size_x, size_y)
        self.speed = speed
    def update(self):
        if self.rect.x < 470:
            self.direction = "right"
        if self.rect.x > 640:
            self.side = "left"
        if self.side == "left":
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed
enemy = Enemy('enemy.png', 400, 465, 80, 80, 4)
class Bullet(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, speed):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.speed = speed
    def update(self):
        self.rect.x += self.speed
        if self.rect.x > 710:
            self.kill()

loose = transform.scale(image.load('loose.png'), (700, 500))
win = transform.scale(image.load('finale.png'), (700, 500))
monsters = sprite.Group()
monsters.add(enemy)
barriers = sprite.Group()
monsters.add(p1)
monsters.add(p2)
monsters.add(p3)
monsters.add(p4)
bullets = sprite.Group()
run = True
finish = False
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYUP:
            if e.key == K_UP:
                player.y_speed = 0
            if e.key == K_DOWN:
                player.y_speed = 0
            if e.key == K_RIGHT:
                player.x_speed = 0
            if e.key == K_LEFT:
                player.x_speed = 0
        elif e.type == KEYDOWN:
            if e.key == K_UP:
                player.y_speed = -5
            if e.key == K_SPACE:
                player.fire()
            if e.key == K_DOWN:
                player.y_speed = 5
            if e.key == K_RIGHT:
                player.x_speed = 5
            if e.key == K_LEFT:
                player.x_speed = -5
    if finish != True:
        bullets.update()
        window.fill(back)
        player.update()
        player.reset()
        p1.reset()
        p2.reset()
        p3.reset()
        p4.reset()
        final.reset()
        barriers.draw(window)
        bullets.draw(window)
        monsters.draw(window)
        sprite.groupcollide(bullets, barriers, True, False)
        sprite.groupcollide(bullets, monsters, True, True)
        if sprite.collide_rect(player, final):
            finish = True
            window.blit(win, (0, 0))
        if sprite.spritecollide(player, monsters, False):
            finish = True
            window.blit(loose, (0, 0))

    time.delay(50)
    display.update()
