from main import * 
from data import * 
from boss_bullet import * 
import pygame 


class Boss(pygame.sprite.Sprite):
    def __init__(self, game_sprites, game_bullets, bullet_type, screen, name="Boss"):
        super().__init__() 
        self.screen = screen 
        self.img_data = pygame.image.load("./img/boss.png") 
        self.image = pygame.transform.scale(self.img_data, (100, 100)) 
        self.WIDTH = self.screen.get_width() 
        self.HEIGHT = self.screen.get_height()
        self.rect = self.image.get_rect()
        self.rect.centerx = self.WIDTH // 2
        self.rect.y = 50
        self.speedx = 3
        self.shoot_timer = 0 
        self.game_sprites = game_sprites 
        self.game_bullets = game_bullets 
        self.bullet_type = bullet_type 

    def update(self):
        self.rect.x += self.speedx
        if self.rect.right > self.WIDTH or self.rect.left < 0:
            self.speedx *= -1
        
        self.shoot_timer += 1
        if self.shoot_timer > 60:
            self.shoot()
            self.shoot_timer = 0
    
    def shoot(self): 
        #bullet = BossBullet(self.rect.centerx, self.rect.bottom) 
        # -- type of bullet passed as a class 
        bullet = self.bullet_type(self.rect.centerx, self.rect.bottom, self.screen) 
        self.game_sprites.add(bullet)
        self.game_bullets.add(bullet) 
        
