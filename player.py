import pygame 

class Player(pygame.sprite.Sprite):
    def __init__(self, game_sprites, game_bullets, bullet_type, screen, name="Player"): 
        super().__init__() 
        self.screen = screen 
        self.img_data = pygame.image.load("./img/player.png") 
        self.image = pygame.transform.scale(self.img_data, (50, 50)) 
        self.rect = self.image.get_rect() 
        self.WIDTH = self.screen.get_width() 
        self.HEIGHT = self.screen.get_height()
        self.rect.centerx = self.WIDTH // 2 
        self.rect.bottom = self.HEIGHT - 10
        self.speed = 8
        self.lives = 3 
        self.game_sprites = game_sprites 
        self.game_bullets = game_bullets 
        self.bullet_type = bullet_type 
        self.shoot_counter = 30 
        
    # -- maybe change controls to W A S D 
    def update(self): 
        self.shoot_counter += 1 
        keys = pygame.key.get_pressed() 
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < self.WIDTH:
            self.rect.x += self.speed 
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.bottom < self.HEIGHT:
            self.rect.y += self.speed 
        
        if keys[pygame.K_SPACE]: 
            if self.shoot_counter > 10:
                self.shoot() 
                self.shoot_counter = 0 
            
    
    def shoot(self): 
        # -- type of bullet passed as a class 
        bullet = self.bullet_type(self.rect.centerx, self.rect.top) 
        self.game_sprites.add(bullet) 
        self.game_bullets.add(bullet) 

# -- skins would be subclasses of this Player class with customized values according to the selected skin 
# -- the skins could be stored as player classes in a collection in the Game class 
# -- the images are stored in ./img/skins/ 
# -- dimensions could be changed to fractions of the view -- self.WIDTH / 10 

