#template/skeleton
import pygame
import random
import os
import asyncio


WIDTH = 480
HEIGHT = 600
FPS = 60

#colors   R    G    B
WHITE = (255, 255, 255)
BLACK = (000, 000, 000)
RED   = (255, 000, 000)
GREEN = (000, 255, 000)
BLUE  = (000, 000, 255)
YELLOW= (255, 255, 000)
CYAN  = (000, 255, 255)
MAGENTA=(255, 000, 255)

#set up imgses
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, "img")
snd_dir = os.path.join(game_folder, "snd")

async def main():
    #initial pygame and window
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("SHUMUP!")
    clock = pygame.time.Clock()


    font_name = pygame.font.match_font('arial')
    def draw_text(surf, text, size, x, y):
        font = pygame.font.Font(font_name, size)
        text_surface = font.render(text, True, WHITE)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        surf.blit(text_surface, text_rect)
        
    class Player(pygame.sprite.Sprite):
        #sprite for player
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.transform.scale(player_img, (50, 38))
            self.image.set_colorkey(BLACK)
            self.rect = self.image.get_rect()
            self.radius = 20
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
            self.rect.centerx = WIDTH / 2       
            self.rect.bottom = HEIGHT - 10
            self.speedx = 0
            self.speedy = 0
            
        def update(self):
            self.speedx = 0
            self.speedy = 0
            keystate = pygame.key.get_pressed()
            if keystate[pygame.K_LEFT]:
                self.speedx = -5
            if keystate[pygame.K_RIGHT]:
                self.speedx = 5
            if keystate[pygame.K_UP]:
                self.speedy = -5
            if keystate[pygame.K_DOWN]:
                self.speedy = 5
            self.rect.x += self.speedx
            self.rect.y += self.speedy
            if self.rect.right > WIDTH:
                self.rect.right = WIDTH
            if self.rect.left < 0:
                self.rect.left = 0
            if self.rect.bottom > HEIGHT:
                self.rect.bottom = HEIGHT
            if self.rect.top < 0:
                self.rect.top = 0
            #self.rect.x += 5
            #self.rect.y += self.y_speed
            #if self.rect.bottom > HEIGHT -200:
            #    self.y_speed = -4
            #if self.rect.top < 200:
            #   self.y_speed = 4
            #if self.rect.x > WIDTH:
            #   self.rect.right = 0
        def shoot(self):
            bullet = Bullet(self.rect.centerx, self.rect.top)
            all_sprites.add(bullet)
            bullets.add(bullet)
            shoot_sound.play()
            
    class Mob(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            #self.image = pygame.Surface((40, 50))
            #self.image.fill(RED)
            self.image_orig = random.choice(meteor_images)      
            #self.image_orig.set_colorkey(WHITE)
            self.image = self.image_orig.copy()
            self.rect = self.image.get_rect()
            self.radius = int(self.rect.width *0.9 / 2)
            #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-150, -100)
            self.speedy = random.randrange(1,8)  
            self.speedx = random.randrange(-3, 3)
            self.rot = 0
            self.rot_speed = random.randrange(-8,8)
            self.last_update = pygame.time.get_ticks()
            
        def rotate(self):
            now = pygame.time.get_ticks()
            if now - self.last_update > 50:
                self.last_update = now
                self.rot = (self.rot + self.rot_speed) %360
                new_image = pygame.transform.rotate(self.image_orig, self.rot)
                old_center = self.rect.center
                self.image = new_image
                self.rect = self.image.get_rect()
                self.rect.center = old_center
                
        def update(self):
            self.rotate()
            self.rect.y += self.speedy
            self.rect.x += self.speedx
            if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
                self.rect.x = random.randrange(WIDTH - self.rect.width)
                self.rect.y = random.randrange(-100, -40)
                self.speedy = random.randrange(1, 8)
            
    class Bullet(pygame.sprite.Sprite):
        def __init__(self, x, y):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.transform.scale(bullet_img, (7, 27))
            #self.image = bullet_img
            self.image.set_colorkey(BLACK)
            self.rect = self.image.get_rect()
            self.rect.bottom = y
            self.rect.centerx = x
            self.speedy = -10
            
        def update(self):
            self.rect.y +=self.speedy
            #kill if goes off top
            if self.rect.bottom < 0:
                self.kill()
                
    #initial pygame and window
    #pygame.init()
    #pygame.mixer.init()
    #screen = pygame.display.set_mode((WIDTH, HEIGHT))
    #pygame.display.set_caption("SHUMUP!")
    #clock = pygame.time.Clock()    

    # game graphics
    background = pygame.image.load(os.path.join(img_folder, "starfield.png")).convert()
    background_rect = background.get_rect()  
    player_img = pygame.image.load(os.path.join(img_folder, "playerShip1_blue.png")).convert()
    meteor_img = pygame.image.load(os.path.join(img_folder, "meteorBrown_med1.png")).convert()
    bullet_img = pygame.image.load(os.path.join(img_folder, "laserBlue16.png")).convert()
    meteor_images = []
    #meteor_list = ["meteorBrown_big1.png", "meteorBrown_big3.png",
    #            "meteorBrown_big4.png", "meteorBrown_med1.png", "meteorBrown_med3.png",
    #            "meteorBrown_small1.png", "meteorBrown_small2.png", "meteorGrey_big1.png",
    #            #"meteorGrey_big2.png",
    #            "meteorGrey_big3.png", "meteorGrey_big4.png", "meteorGrey_med1.png",
    #            "meteorGrey_med2.png"]
    meteor_list = ["Asteroids_32x32_001.png", "Asteroids_32x32_002.png", "Asteroids_32x32_003.png",
                    "Asteroids_32x32_004.png", "Asteroids_32x32_005.png", "Asteroids_32x32_006.png", 
                    "Asteroids_32x32_007.png", "Asteroids_32x32_008.png", 
                    "Asteroids_64x64_001.png", "Asteroids_64x64_002.png", "Asteroids_64x64_003.png",
                    "Asteroids_64x64_004.png", "Asteroids_64x64_005.png", "Asteroids_64x64_006.png", 
                    "Asteroids_64x64_007.png", "Asteroids_64x64_008.png",
                    "Asteroids_128x128_001.png", "Asteroids_128x128_002.png", "Asteroids_128x128_003.png",
                    "Asteroids_128x128_004.png", "Asteroids_128x128_005.png", "Asteroids_128x128_006.png", 
                    "Asteroids_128x128_007.png", "Asteroids_128x128_008.png"                ]
    meteor_image_paths = []
    for img in meteor_list:
        meteor_image_paths.append(os.path.join(img_folder, img))
    # Load and process images
    for path in meteor_image_paths:
        img = pygame.image.load(path)
        new_img = pygame.Surface(img.get_size(), pygame.SRCALPHA)
        for x in range(img.get_width()):
            for y in range(img.get_height()):
                color = img.get_at((x, y))
                if color != WHITE and color != BLACK:
                    new_img.set_at((x, y), color)
        meteor_images.append(new_img)

    #for img in meteor_list:
    #    meteor_images.append(pygame.image.load(os.path.join(img_folder, img)).convert())

    shoot_sound = pygame.mixer.Sound(os.path.join(snd_dir, 'laser1.wav'))
    shoot_sound.set_volume(0.1)
    expl_sounds = []
    for snd in ['explosion07.wav', 'explosion09.wav']:
        sound = pygame.mixer.Sound(os.path.join(snd_dir, snd))
        expl_sounds.append(sound)
        sound.set_volume(0.1)
    #pygame.mixer.music.load(os.path.join(snd_dir, 'frozenjam-seamlessloop.ogg'))
    pygame.mixer.music.load(os.path.join(snd_dir, 'ymca.ogg'))
    pygame.mixer.music.set_volume(0.2)

    all_sprites = pygame.sprite.Group()
    mobs = pygame.sprite.Group()
    player = Player()
    bullets = pygame.sprite.Group()
    all_sprites.add(player)
    for i in range(10):
        m = Mob()
        all_sprites.add(m)
        mobs.add(m)
    
    # **New: Add game state and countdown setup**
    game_state = "start"  # Initial state is "start"
    countdown = 3         # 3-second countdown
    pygame.time.set_timer(pygame.USEREVENT + 1, 1000)  # Timer triggers every 1 second

    pygame.mixer.music.play(loops = -1)
    #game loop
    running = True
    score = 0
    while running:
        #keep loop running at same time
        clock.tick(FPS)
        #process events
        for event in pygame.event.get():
            #check for closing window
            if event.type == pygame.QUIT:
                running = False
            # **New: Handle countdown timer event**
            elif event.type == pygame.USEREVENT + 1:
                if game_state == "start":
                    countdown -= 1
                    if countdown <= 0:
                        game_state = "playing"
                        pygame.time.set_timer(pygame.USEREVENT + 1, 0)  # Stop the timer
            # **Modified: Only shoot when playing**                
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and game_state == "playing":
                    player.shoot()

        # **Modified: Update only when playing**
        if game_state == "playing":                    
            #update
            all_sprites.update()
            #if bullet hit mob
            hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
            for hit in hits:
                score += 50 - hit.radius
                random.choice(expl_sounds).play()
                m = Mob()
                all_sprites.add(m)
                mobs.add(m)
                
                
                
            #if mob hits player
            hits = pygame.sprite.spritecollide(player,mobs, False, pygame.sprite.collide_circle)
            if hits:
                running = False
        
        
        #render
        screen.fill(BLACK)
        screen.blit(background, background_rect)
        all_sprites.draw(screen)
        # **New: Display countdown during start state**
        if game_state == "start":
            draw_text(screen, str(countdown), 50, WIDTH / 2, HEIGHT / 2)
        draw_text(screen, str(score), 18, WIDTH / 2, 10)
        #flip display after drawing everything
        pygame.display.flip()
        # **New: Add this line to yield control to the browser**
        await asyncio.sleep(0)        
    pygame.quit()

asyncio.run(main())