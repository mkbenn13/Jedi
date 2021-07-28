import pygame
import random
import math
import time
pygame.font.init()

WIDTH = 540
HEIGHT = 480
FPS = 60

Blue = (0, 0, 225)
Red = (225, 0, 0)
Green = (0, 225, 0)
White = (225, 225, 225)
Black = (0, 0, 0)
Font = pygame.font.Font('Starjedi.ttf', 30)

# init pygame and create screen
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()
points = 0 
spawnNum = 0
spawnNum2 = 5
spawnNum3 = 3
text = Font.render(("Points: " + str(points)), False, (0, 0, 0))

def new_enemy():
    spawnPoints = [445, 370, 295, 220, 145, 70]
    global spawnNum
    global points
    enemy = Stormtrooper(spawnPoints[spawnNum])
    enemies.add(enemy)
    if spawnNum >= 5:
        spawnNum = 0
    else:
        spawnNum += 1
    points += 1
    print(spawnPoints[spawnNum])

def new_enemy2():
    spawnPoints = [445, 370, 295, 220, 145, 70]
    global spawnNum2
    global points
    spawnAt = spawnPoints[spawnNum2]
    enemy = Stormtrooper(spawnAt)
    enemies.add(enemy)
    if spawnNum2 >= 5:
        spawnNum2 = 0
    else:
        spawnNum2 += 1
    points += 1

def new_enemy3():
    spawnPoints = [445, 370, 295, 220, 145, 70]
    global spawnNum3
    global points
    spawnAt = spawnPoints[spawnNum3]
    enemy = Stormtrooper(spawnAt)
    enemies.add(enemy)
    if spawnNum3 >= 5:
        spawnNum3 = 0
    else:
        spawnNum3 += 1
    points += 1

class Background(pygame.sprite.Sprite):
    def __init__(self, location):
        self.image = pygame.image.load('Background.png')
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

class Stormtrooper(pygame.sprite.Sprite):
    def __init__(self, rectleft):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('Enemy.png').convert_alpha()
        self.original_image = self.image
        self.rect = self.image.get_rect()
        self.rect.left = rectleft
        self.rect.top = 50
        self.y = self.rect.top
        self.x = self.rect.left
        self.position = [self.x, self.y]
        self.dead = False
        self.shotClock = random.choice( [0, 120, 150, 90, 60] )
        self.mask = pygame.mask.from_surface(self.image)

    def rotate(self):
        player_x = WIDTH/2
        player_y = 441
        rel_x, rel_y = player_x - self.x, player_y - self.y
        angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)
        self.image = pygame.transform.rotate(self.original_image, int(angle))
        self.rect = self.image.get_rect(center = self.position)

    def shoot(self):
        bullet = BulletEnemy(self.rect.centerx, self.rect.bottom)
        bullets.add(bullet)
        self.shotClock = random.choice( [0, 120, 150, 90, 60] )

    def update(self):
        self.rotate()
        enemy_hit_list = pygame.sprite.spritecollide(self, bullets, False, pygame.sprite.collide_mask)
        for enemy in enemy_hit_list:
            new_enemy()
            self.kill() 
        if self.shotClock >= 180:
            self.shoot()
        else:
            self.shotClock += 1
        

class BulletEnemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('Bullet.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.position = [self.rect.centerx, self.rect.bottom]
 
        self.floating_point_x = self.rect.centerx
        self.floating_point_y = self.rect.bottom

        x_diff = WIDTH/2 - x
        y_diff = 441 - y
        angle = math.atan2(y_diff, x_diff)

        self.velocity = 10
        self.change_x = math.cos(angle) * self.velocity
        self.change_y = math.sin(angle) * self.velocity

        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.floating_point_y += self.change_y
        self.floating_point_x += self.change_x
 
        # The rect.x and rect.y are converted to integers.
        self.rect.y = int(self.floating_point_y)
        self.rect.x = int(self.floating_point_x)
        # If the bullet flies of the screen, get rid of it.
        
        if self.rect.x < 0 or self.rect.x > WIDTH or self.rect.y < 0 or self.rect.y > HEIGHT:
            self.kill()

class Saber(pygame.sprite.Sprite):
    def __init__(self, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.width = width
        self.height = height
        self.image = pygame.image.load('Saber.png').convert_alpha()
        self.original_image = self.image
        self.rect = self.image.get_rect()
        self.y = 441
        self.x = WIDTH/2
        self.position = [self.x, self.y]
        

    def rotate(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        rel_x, rel_y = mouse_x - self.x, mouse_y - self.y
        angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)
        self.image = pygame.transform.rotate(self.original_image, int(angle))
        self.rect = self.image.get_rect(center = self.position)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rotate()
      
        
class Player(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.width = width
        self.height = height
        self.image = pygame.image.load('Body4.png').convert_alpha()
        self.original_image = self.image
        self.rect = self.image.get_rect()
        self.angle = 0
        self.y = 441
        self.x = WIDTH/2
        self.position = [self.x, self.y]
        self.lives = 5

    def update(self):
        self.image = pygame.transform.rotate(self.original_image, 90)
        self.rect = self.image.get_rect(center = self.position)


background = Background([0,0])
player = Player(Red, 13, 13)
saber = Saber(13, 13)
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()
players = pygame.sprite.Group()
sabers = pygame.sprite.Group()

running = True
all_sprites.add(player)
all_sprites.add(saber)
players.add(player)
sabers.add(saber)

new_enemy()
new_enemy2()
new_enemy3()
while running:
    # Keep loop running at the FPS
    clock.tick(FPS)

    # Process input (events)
    for event in pygame.event.get():
        # If user presses 'X'
        if event.type == pygame.QUIT:
            running = False
    # Update
    # if enemy.shotClock >= 180:
    #     bullet = BulletEnemy(enemy.rect.left, enemy.rect.bottom)
    #     bullets.add(bullet)
    #     enemy.shotClock = random.choice( [0, 120, 150, 90, 60] )
    # else:
    #     enemy.shotClock += 1
    saber_hit_list = pygame.sprite.spritecollide(saber, bullets, False, pygame.sprite.collide_mask)
    for bullet in saber_hit_list:
        bullet.change_x *= -1
        bullet.change_y *= -1 
    player_hit_list = pygame.sprite.spritecollide(player, bullets, False, pygame.sprite.collide_mask)
    for bullet in player_hit_list:
        player.lives -= 1
        bullet.kill()
        if player.lives == 0:
            time.sleep(3)
            running = False
    print(pygame.mouse.get_pos())
    all_sprites.update()
    enemies.update()
    bullets.update()
    text = Font.render(("Points: " + str(points)), False, (0, 0, 0))
    # Draw/render
    screen.fill(Black)
    screen.blit(background.image, background.rect)
    screen.blit(text ,(19, 415))
    all_sprites.draw(screen)
    enemies.draw(screen)
    bullets.draw(screen)
    pygame.display.flip()
