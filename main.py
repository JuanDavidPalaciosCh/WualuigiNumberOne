# import libraries
from platform import platform
import pygame
import random
from constants import *

# initialize pygame
pygame.init()

# create window
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Waluigi number one')

# game_variables
bg_scroll: int = 0

# load images
bg_image = pygame.image.load('assets/MarioBg.jpg').convert_alpha()
wualuigi_image = pygame.image.load('assets/wualuigi.png').convert_alpha()
shyguy_image = pygame.image.load('assets/FlyingShyGuy.png').convert_alpha()
floor_image = pygame.image.load('assets/floor.png').convert_alpha()


# function of drawing of the background
def draw_bg(bg_scroll):
    window.blit(bg_image, (0, 0 + bg_scroll))
    window.blit(bg_image, (0, -600 + bg_scroll))


# player class
class Player ():
    def __init__(self, x, y):

        self.image = pygame.transform.scale(wualuigi_image, (30, 50))
        self.width = 28
        self.height = 50
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = (x, y)
        self.vel_y = 0
        self.flip = False

    def move(self):

       # process key pressed
        key = pygame.key.get_pressed() 

        # reset variable
        scroll: int = 0
        dx: int = 0
        dy: int = 0
        
        if key[pygame.K_LEFT]:
           dx = -7
           self.flip = True

        if key[pygame.K_RIGHT]:
           dx = +7
           self.flip = False

        # gravity
        self.vel_y += GRAVITY
        dy += self.vel_y

        #check player x
        if self.rect.x < 0:
            self.rect.x = 400
        elif self.rect.x > 400:
            self.rect.x = 0

        #check collision with enemies        
        for enemy in enemy_group:
           # y collision
           if enemy.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
               # check if above enemy
               if self.rect.bottom < enemy.rect.centery:
                    if self.vel_y > 0:
                        self.rect.bottom = enemy.rect.top
                        dy = 0
                        self.vel_y = -20

   
        #check player floor
        if self.rect.bottom + dy > WINDOW_HEIGHT:
            dy = 0
            self.vel_y = -20

        # check if the player  has bounced to the top of the screen
        if self.rect.top <= SCROLL_THRESH:
            # if player is jumping
            if self.vel_y < 0:
                scroll = -dy

        # update rect position
        self.rect.x += dx
        self.rect.y += dy + scroll

        return scroll

    def draw(self):

        window.blit(pygame.transform.flip(self.image, self.flip, False), (self.rect.x - 5, self.rect.y))
        pygame.draw.rect(window, PURPLE, self.rect, 2)


# enemies class

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, picture, scale):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(picture, scale)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, scroll):
        #update vertical position
        self.rect.y += scroll

        # check if platform has gome off the window
        if self.rect.top > WINDOW_HEIGHT:
            self.kill()

            
# player instance
wualuigi = Player(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 150)

# create sprite groups
enemy_group = pygame.sprite.Group()

# create floor platform
enemy = Enemy(0, WINDOW_HEIGHT - 30, floor_image, FLOOR_SCALE)
enemy_group.add(enemy)

# Game loop
run = True

while run:

    CLOCK.tick(FPS)

    scroll = wualuigi.move()

    # draw background
    bg_scroll += scroll
    draw_bg(bg_scroll)
    if bg_scroll >= 600:
        bg_scroll = 0

    # Generate enemies
    if len(enemy_group) < MAX_ENEMIES:
        e_x = random.randint(0, WINDOW_WIDTH - 50)
        e_y = enemy.rect.y - random.randint(80, 120)
        enemy = Enemy(e_x, e_y, shyguy_image, ENEMY_SCALE)
        enemy_group.add(enemy)

    # update enemies
    enemy_group.update(scroll)

    # draw sprites
    enemy_group.draw(window)
    wualuigi.draw()

    # event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False


    # update display window
    pygame.display.update()

    


pygame.quit()
