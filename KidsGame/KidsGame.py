# Game Created by Lawson, Ryker, Asher and Izzy. 

import pygame
import random
import os
from os import path


#-------------------------------
# define colors used in the game
#-------------------------------
white = (255,255,255)
black = (0,0,0)
red = (255, 0, 0)
green = (0,255,0)
blue = (0,0,255)
yellow = (255,255,0)

width = 480
height = 600
FPS = 60
BackgroundScroll_Y = 0



score = 0

TheWindowName = "SpaceBoat by Ryker, Izzy and Asher"
backgroundcolor = black
respawn = pygame.USEREVENT + 2

#----------------------------------------
# The path to the image and sound folders
#----------------------------------------
imgfolder = path.join(path.dirname(__file__), 'img')
EnemyShipFolder = path.join(imgfolder, "EnemyShips")
ExplosionFolder = path.join(imgfolder, "Explosions")
RedExplosionFolder = path.join(ExplosionFolder, "RedUp") 
PlayerExplosionFolder = path.join(ExplosionFolder, "PlayerBlowUp") 
print(imgfolder)
snd_dir = path.join(path.dirname(__file__), 'snd')

#--------------
# Starts pygame 
#--------------
pygame.init()

#---------------------------------------------
# pygame module for loading and playing sounds
#---------------------------------------------
pygame.mixer.init()

#------------------------
# pygame module for fonts 
#------------------------
pygame.font.init() 
font_name = pygame.font.match_font('arial')

#------------------------
# Creates the game window
#------------------------
screen = pygame.display.set_mode((width,height))

#-----------------------------
# Sets the name of the window.
#----------------------------- 
pygame.display.set_caption(TheWindowName)

#------------------------------------------------------------------------
# Creates a new Clock object that can be used to track an amount of time.
#------------------------------------------------------------------------
clock = pygame.time.Clock()

#-------------------------
# Write Text To The Screen
#-------------------------
def DisplayText(surface, text, size, x, y):
    
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, white)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x,y)
    surface.blit(text_surface, text_rect)

def SpawnEnemy():
    m = Mob()
    e = EnemyShips()
    all_sprites.add(m)
    all_sprites.add(e)
    mobs.add(m)
    enemyships.add(e) 

def DrawShieldBar(surface, x, y, pct): 
   if pct < 0:
       pct = 0
   BAR_LENGTH = 100
   BAR_HEIGHT = 10
   fill = (pct / 100) * BAR_LENGTH
   outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
   fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
   pygame.draw.rect(surface, green, fill_rect)
   pygame.draw.rect(surface, white, outline_rect, 2)

def ScrollingBackGround_UP(BackGroundImage, x, y, x1, y1):
    
    screen.blit(BackGroundImage, (x, y))
    screen.blit(BackGroundImage, (x1,y1))
    if y > h:
        y = -h
    if y1 > h:
        y1 = -h
    return BackgroundScroll_Y - 1

def load_images(path_to_directory):
    #Load images and return them as a dict.
    image_dict = {}
    for filename in os.listdir(path_to_directory):
        if filename.endswith('.png'):
            path = os.path.join(path_to_directory, filename)
            key = filename
            image_dict[key] = pygame.image.load(path).convert()
    return image_dict

def loadingAnimations(rangeStart, rangeStop, imgFolderPath, formatString, dicArray, dickey, colorKey, transformSize):
    for i in range(rangeStart, rangeStop):
        filename = formatString.format(i)
        img = pygame.image.load(path.join(imgFolderPath, filename)).convert()
        img.set_colorkey(colorKey)
        img_lg = pygame.transform.scale(img, transformSize)
        dicArray[dickey].append(img_lg)

def draw_lives(surf, x, y, lives, img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        surf.blit(img, img_rect)


class Shields(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(shield_img, (100, 100))
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        
        self.rect.centerx = width / 2
        self.rect.bottom = height - 10
        

    def update(self):
        self.rect.x = player.rect.x
        self.rect.y = player.rect.y
       



class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x 
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        #kill if it moves off the screen
        if self.rect.bottom < 0:
            self.kill()

class Player(pygame.sprite.Sprite):
    #----------------------
    # Sprite for the player
    #----------------------
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
      
        #---------------------
        # Create the spaceship
        #---------------------
        self.image = pygame.transform.scale(player_img, (100, 100))
        self.image.set_colorkey(black) 
        self.rect = self.image.get_rect()
        
        self.radius = 45
        #pygame.draw.circle(self.image, red, self.rect.center, self.radius)
        
        #---------------------------------------
        # Place ship in the center of the screen
        #---------------------------------------
        self.rect.centerx = width / 2
        self.rect.bottom = height - 10
        self.speedx = 0
        self.speedy = 0
        #------------------------------
        # Shields for The Player
        #------------------------------
        self.shield = 100
        #--------------------
        # Rapid Fire Shooting
        #--------------------
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()
        # player lives
        self.lives = 3
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()

        
    
    def update(self):
        #unhide if hidden
        

        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 2000:
            self.hidden = False
            self.rect.centerx = width / 2
            self.rect.bottom = height - 10
               
        self.speedx = 0
        self.speedy = 0
        #---------------------------
        # Get the keys being pressed
        #---------------------------
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -5
        if keystate[pygame.K_RIGHT]: 
            self.speedx = 5
        if keystate[pygame.K_UP]:
            self.speedy = -5
        if keystate[pygame.K_DOWN]:
            self.speedy = 5
        if keystate[pygame.K_SPACE]: 
            self.shoot()
        
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.right > width: 
            self.rect.right = width
        if self.rect.left < 0:
            self.rect.left = 0
        if  self.rect.bottom > height:
            if self.hidden == False:
                self.rect.bottom = height
        if self.rect.top < 0: 
            self.rect.top = 0
        

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            bullet = Bullet(self.rect.centerx, self.rect.top)
            all_sprites.add(bullet)
            bullets.add(bullet)
            shoot_sound.play()
    
   
    def hide(self):
        #hide the player temp
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (width / 2, height + 200)

class EnemyShips(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(random.choice(enemy_images), (50, 50)) 
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.radius = 20
        self.rect.x = random.randrange(width - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-3, 3)
       
    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > height + 10 or self.rect.left < -25 or self.rect.right > width + 20:
            self.rect.x = random.randrange(width - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)

    
        
class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        #self.image = pygame.Surface((30, 40))
        #self.image.fill(red)
        self.image_orig = pygame.transform.scale(random.choice(meteor_images), (50, 50)) 
        self.image_orig.set_colorkey(black)
        self.image = self.image_orig.copy() 
        self.rect = self.image.get_rect()
        self.radius = 20
        #pygame.draw.circle(self.image, red, self.rect.center, self.radius)
        self.rect.x = random.randrange(width - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-3, 3)
        self.rot = 0
        self.rot_speed = random.randrange(-8,8)
        self.last_update = pygame.time.get_ticks()
    
    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self):
        self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > height + 10 or self.rect.left < -25 or self.rect.right > width + 20:
            self.rect.x = random.randrange(width - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 25

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

        
#---------------------
# Load Images
#---------------------
background = pygame.image.load(path.join(imgfolder, "starfield.png")).convert()
background_rect = background.get_rect()
background_size = background.get_size()
w,h = background_size

# Player Image
player_img = pygame.image.load(path.join(imgfolder, "redfighter0005.png")).convert()

# Player lives Image
player_mini_img = pygame.transform.scale(player_img, (25,19))
player_mini_img.set_colorkey(black)

shield_img = pygame.image.load(path.join(imgfolder, "shield.png")).convert()
shield_img.set_alpha(50)


# Bullet Image
bullet_img = pygame.image.load(path.join(imgfolder, "laserRed16.png")).convert()

meteor_images = []
meteor_list = ["meteorBrown_med1.png", "rotationY15.png"]
for img in meteor_list: 
    meteor_images.append(pygame.image.load(path.join(imgfolder, img)).convert())

# Loading explosion animations 
explosion_anim = {}
player_anim = {}
explosion_anim['lg'] = []
explosion_anim['sm'] = []
explosion_anim['player'] = []



loadingAnimations(1, 19, RedExplosionFolder, "{}.png", explosion_anim, "lg", black, (75,75))
loadingAnimations(1, 19, RedExplosionFolder, "{}.png", explosion_anim, "sm", black, (35,35))
loadingAnimations(60, 99, PlayerExplosionFolder, "0000{}.png", explosion_anim, "player", black, (100,100))
  

enemy_images = []
enemyship_list = load_images(EnemyShipFolder)
for img in enemyship_list:
   enemy_images.append(pygame.image.load(path.join(EnemyShipFolder, img)).convert())

#-----------------
# Load Game Sounds
#-----------------
shoot_sound = pygame.mixer.Sound(path.join(snd_dir, "Laser_Shoot11.wav"))
expl_sounds = []
for snd in ['Explosion22.wav', 'Explosion40.wav']:
    expl_sounds.append(pygame.mixer.Sound(path.join(snd_dir, snd)))

#--------------------------
# Load the Background Music
#--------------------------
pygame.mixer.music.load(path.join(snd_dir, "Error Management.wav"))
pygame.mixer.music.set_volume(0.3)

#-------------------------------
# Create Groups for our sprites
#------------------------------    
all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
enemyships = pygame.sprite.Group()
shieldgrp = pygame.sprite.Group()


#Create an instance in our game of the player then add the player to the game

playershields = Shields()
all_sprites.add(playershields)

player = Player()
all_sprites.add(player)

# Start The Game by spawning 3 enemys
for i in range(8):
   SpawnEnemy()
    

pygame.mixer.music.play(loops = -1)

# Game loop
IsGameRunning = True
while IsGameRunning:
       
    clock.tick(FPS)
    
    # If the user does stuff then the our game looks here
    # Process input (events)
    for event in pygame.event.get():
        
        #Check if user has closed the window
        if event.type == pygame.QUIT:
            IsGameRunning = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()
        elif event.type == pygame.USEREVENT + 2:
                SpawnEnemy()
             

    # Update
    all_sprites.update()
    
    # Check to see if a bullet hit a bad guy
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True) or pygame.sprite.groupcollide(enemyships, bullets, True, True)
    #print(HitsMob)
    for hit in hits:
        score += 50 - hit.radius
        random.choice(expl_sounds).play()
        expl = Explosion(hit.rect.center, 'lg')
        all_sprites.add(expl)
        pygame.time.set_timer(respawn, 500)
        

    #-------------------------------------
    # Check to see if a mob hit the player
    #-------------------------------------
    hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle) or pygame.sprite.spritecollide(player, enemyships, True, pygame.sprite.collide_circle)
    for hit in hits: 
        player.shield -= hit.radius * 2
        expl = Explosion(hit.rect.center, 'sm')
        all_sprites.add(expl)
        if player.shield <= 0: 
            player_explodes = Explosion(player.rect.center, "player")
            all_sprites.add(player_explodes)
            player.hide()
            player.lives -= 1
            player.shield = 100
            
    
    # if player died and the explosion has finished then end game
    if player.lives == 0 and not player_explodes.alive():
        player.kill()
        IsGameRunning = False
 
    #----------------
    # Draw The Screen 
    #---------------- 
    screen.fill(backgroundcolor)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    DrawShieldBar(screen, 5, 5, player.shield)
    DisplayText(screen, "Score: " + str(score), 20, width / 2, 10)
    draw_lives(screen, width - 100, 5, player.lives, player_mini_img)
    
    # After drawing everything, flip the display
    pygame.display.flip()
    

pygame.quit()




