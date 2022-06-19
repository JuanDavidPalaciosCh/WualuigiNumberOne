# import libraries
import pygame
import os
import random
from pygame import mixer
from constants import *

# initialize pygame
pygame.init()

# create window
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Waluigi number one')


wah_sound = pygame.mixer.Sound('assets/sounds/WahSound.mp3')
wah_sound.set_volume(0.1)
gameover_sound = pygame.mixer.Sound('assets/sounds/GameOver.mp3')
gameover_sound.set_volume(0.5)

# game_variables
bg_scroll: int = 0
score: int = 0
fade_counter: int = 0
if os.path.exists('score.txt'):
    with open('score.txt', 'r') as file:
        high_score = int(file.read())
else:
    high_score: int = 0

# load images
bg_image = pygame.image.load('assets/images/MarioBg.jpg').convert_alpha()
wualuigi_game_over = pygame.image.load('assets/images/WualuigiGameOver.png').convert_alpha()
wualuigi_game_over2 = pygame.image.load('assets/images/WualuigiGameOver2.png').convert_alpha()
wualuigi_game_over3 = pygame.image.load('assets/images/WualuigiGameOver3.png').convert_alpha()
wualuigi_image = pygame.image.load('assets/images/wualuigi.png').convert_alpha()
shyguy_image = pygame.image.load('assets/images/FlyingShyGuy.png').convert_alpha()
goomba_image = pygame.image.load('assets/images/FlyingGoomba.png').convert_alpha()
koopa_image = pygame.image.load('assets/images/FlyingKoopa.png').convert_alpha()
bonus_image = pygame.image.load('assets/images/Bonus.png').convert_alpha()
floor_image = pygame.image.load('assets/images/floor.png').convert_alpha()
menu_image = pygame.image.load('assets/menu/WaluigiMenu.png').convert_alpha()
bg_menu = pygame.image.load('assets/menu/MenuBg.jpg').convert_alpha()

# game over image
game_over_img: tuple = (wualuigi_game_over, wualuigi_game_over2, wualuigi_game_over3)

# enemy list with percentage
enemy_list: list = [shyguy_image, shyguy_image, shyguy_image, shyguy_image, shyguy_image,
shyguy_image, shyguy_image, shyguy_image, shyguy_image, shyguy_image,
shyguy_image, shyguy_image, shyguy_image, shyguy_image, shyguy_image,
shyguy_image, shyguy_image, shyguy_image, shyguy_image, shyguy_image,
shyguy_image, shyguy_image, shyguy_image, shyguy_image, shyguy_image]

#Menu font
def get_font(size):
    return pygame.font.Font("assets/menu/font.ttf", size)


# Pantalla inicio
def intro_game(run):
    while not run:
        window.blit(bg_menu, (0,0))
        draw_text('WALUIGI ', get_font(20), YELLOW, 125 , 25)
        draw_text('NUMBER ONE', get_font(20), YELLOW, 100  , 50)
        draw_text('Made by:', FONT_SMALL, WHITE, 160 , 90 )
        draw_text('Juan David Palacios', FONT_SMALL, WHITE, 110 , 120 )
        draw_text('Mauro Bohorquez', FONT_SMALL, WHITE, 120 , 140 )
        draw_text('Gabriel Estupiñan', FONT_SMALL, WHITE, 115 , 160 )
    
        image_menu = pygame.transform.scale(menu_image, (200, 200))
        window.blit(image_menu, (100,200))
    
        draw_text('HIGHSCORE: {}'.format(high_score), FONT_BIG, WHITE, 100, 420)
        draw_text('PRESS SPACE TO PLAY ', FONT_BIG, WHITE, 90, 450)
        pygame.display.update()
        CLOCK.tick(FPS)
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE]:
            run = True

        # event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
    return True
        

def initialize_music():
    #load music and sounds
    pygame.mixer.music.load('assets/sounds/BgMusic.mp3')
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1, 0.0)

# function for write text
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    window.blit(img, (x, y))

# info panel
def draw_panel():
    pygame.draw.rect(window, BLACK, (0, 0, WINDOW_WIDTH, 25))
    pygame.draw.line(window, PURPLE, (0, 25), (WINDOW_WIDTH, 25), 2)
    draw_text('SCORE: {}'.format(score), FONT_PANEL, PURPLE, 10, 0)

# function of drawing of the background
def draw_bg(bg_scroll):
    window.blit(bg_image, (0, 0 + bg_scroll))
    window.blit(bg_image, (0, -600 + bg_scroll))

# chose image of game over
def choose_image(game_over_img):
    img = random.choice(game_over_img)
    return img


# player class
class Player ():
    def __init__(self, x, y):

        self.image = pygame.transform.scale(wualuigi_image, WUALUIGI_SCALE)
        self.width = 25
        self.height = 55
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
        
        if key[pygame.K_LEFT] and not key[pygame.K_RIGHT]:
           dx = -5
           self.flip = True

        if key[pygame.K_RIGHT] and not key[pygame.K_LEFT]:
           dx = +5
           self.flip = False

        # gravity
        self.vel_y += GRAVITY
        dy += self.vel_y

        #check player x
        if self.rect.x < 0:
            self.rect.x = 400
        if self.rect.x > 400:
            self.rect.x = 0

        #check collision with enemies        
        for enemy in enemy_group:
           # y collision
           if enemy.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
               # check if above enemy
               if self.rect.bottom < enemy.rect.centery:
                    if self.vel_y > 0:
                        self.rect.bottom = enemy.rect.top
                        wah_sound.play()
                        dy = 0
                        self.vel_y = -19
                        enemy.die()
                        enemy.bonus()

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

        window.blit(pygame.transform.flip(self.image, self.flip, False), (self.rect.x - 15, self.rect.y))
        #pygame.draw.rect(window, PURPLE, self.rect, 2)

# enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, picture, scale, orientation= False):
        pygame.sprite.Sprite.__init__(self)
        self.picture = picture
        self.image = pygame.transform.scale(self.picture, scale)
        self.orientation = orientation
        self.look = pygame.transform.flip(self.image, self.orientation, False)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, scroll):
        #update vertical position
        self.rect.y += scroll

        # check if platform has gome off the window
        if self.rect.top > WINDOW_HEIGHT:
            self.kill()
    
    def draw_enemy(self):
        window.blit(self.look, (self.rect.x, self.rect.y))

    
    def die(self):
        if self.picture == goomba_image:
            self.rect.y += 500
    

    def bonus(self):
        if self.picture == bonus_image:
            wualuigi.vel_y -= 30


    def move(self):
        if self.picture == koopa_image:
            if self.orientation == True:
                speed_x = -1
            if self.orientation == False:
                speed_x = 1
            self.rect.x += speed_x
            if self.rect.x > WINDOW_WIDTH - 50:
                self.orientation = True
                self.look = pygame.transform.flip(self.image, self.orientation, False)
            if self.rect.x < 0:
                self.orientation = False
                self.look = pygame.transform.flip(self.image, self.orientation, False)
         
# player instance
wualuigi = Player(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 150)

# create sprite groups
enemy_group = pygame.sprite.Group()

# create floor platform
enemy = Enemy(0, WINDOW_HEIGHT - 30, floor_image, FLOOR_SCALE)
enemy_group.add(enemy)

# Game loop
run = False
game_over = False 

run = intro_game(run)


if run:
    initialize_music()

while run:

    CLOCK.tick(FPS)

    if game_over == False:
        
        scroll = wualuigi.move()

        # draw background
        bg_scroll += scroll
        draw_bg(bg_scroll)
        if bg_scroll >= 600:
            bg_scroll = 0

        # Generate enemies
        if len(enemy_group) < MAX_ENEMIES:
            # increase dificult
            if score >= 500 and score < 2500:
                enemy_list.append(goomba_image)
                #print("goomba")

            if score >= 1000 and score < 2500:
                enemy_list.append(koopa_image)
                #print("koopa")
            
            if score >= 2000 and score < 2500:
                enemy_list.append(bonus_image)

            e_x = random.randint(0, WINDOW_WIDTH - 50)
            e_y = enemy.rect.y - random.randint(90, 95)
            orientation = bool(random.randint(0, 1))
            enemy_image = random.choice(enemy_list)
            if enemy_image == bonus_image:
                scale = BONUS_SCALE
            else:
                scale = ENEMY_SCALE
            enemy = Enemy(e_x, e_y, enemy_image, scale, orientation)
            enemy_group.add(enemy)

        # update enemies
        enemy_group.update(scroll)

        #update score
        if scroll > 0:
            score += scroll 

        # draw line at previous high score
        if high_score > 0:
            draw_text('HIGHSCORE: {}'.format(high_score), FONT_HIGH, WHITE, 0, score - high_score + SCROLL_THRESH - 20)
            pygame.draw.line(window, WHITE, (0, score - high_score + SCROLL_THRESH), (WINDOW_WIDTH, score - high_score + SCROLL_THRESH), 3)
        
        # draw sprites
        for e in enemy_group:
            e.draw_enemy()
        
        for koopa in enemy_group:
            koopa.move()
        wualuigi.draw()

        # draw panel
        draw_panel()

        #check game over
        if wualuigi.rect.top > WINDOW_HEIGHT:
            #Ser image
            img = choose_image(game_over_img)
            #Play music
            pygame.mixer.music.stop()
            gameover_sound.play()
            game_over = True


    else: # player dies
        if fade_counter < 400:
            fade_counter += 7
            for y in range(0, 6, 2):
                pygame.draw.rect(window, BLACK, (0, y * 100, fade_counter, 100))
                pygame.draw.rect(window, BLACK, (400 - fade_counter, y * 100 + 100, fade_counter, 100))

        else:
            # update highscore
            if score > high_score:
                high_score = score
                with open('score.txt', 'w') as file:
                    file.write(str(high_score))
                    
            game_over_image = pygame.transform.scale(img, (200, 400))
            window.blit(game_over_image, (80,200))

            draw_text('GAME OVER', FONT_BIG, PURPLE, 130, 30)
            draw_text('SCORE: {}'.format(score), FONT_BIG, WHITE, 140, 70)
            draw_text('HIGHSCORE: {}'.format(high_score), FONT_BIG, WHITE, 100, 110)
            draw_text('PRESS SPACE TO PLAY AGAIN', FONT_BIG, WHITE, 40, 150)

            # Play again        
            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE]:
                # stop death effect and play game music again
                gameover_sound.stop()
                pygame.mixer.music.play(-1, 0.0)
                # reset variables
                game_over = False
                score = 0
                scroll = 0
                fade_counter = 0
                # reposition wualuigi
                wualuigi.rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT - 150)
                # reset enemies
                enemy_group.empty()
                # reset enemies probabilities
                enemy_list: list = [shyguy_image, shyguy_image, shyguy_image, shyguy_image, shyguy_image,
                                        shyguy_image, shyguy_image, shyguy_image, shyguy_image, shyguy_image,
                                        shyguy_image, shyguy_image, shyguy_image, shyguy_image, shyguy_image,
                                        shyguy_image, shyguy_image, shyguy_image, shyguy_image, shyguy_image,
                                        shyguy_image, shyguy_image, shyguy_image, shyguy_image, shyguy_image]
                # create floor platform
                enemy = Enemy(0, WINDOW_HEIGHT - 30, floor_image, FLOOR_SCALE)
                enemy_group.add(enemy)


    # event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False


    # update display window
    pygame.display.update()

    


pygame.quit()
