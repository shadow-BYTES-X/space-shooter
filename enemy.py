import pygame 
import random 

class Enemy(pygame.sprite.Sprite):
    def __init__(self, screen, name="normal enemy"): 
        super().__init__() 
        self.screen = screen 
        self.img_data = pygame.image.load("./img/enemy.png") 
        self.image = pygame.transform.scale(self.img_data, (60, 60)) 
        self.WIDTH = self.screen.get_width() 
        self.HEIGHT = self.screen.get_height() 
        self.rect = self.image.get_rect() 
        self.rect.x = random.randint(0, self.WIDTH - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.speedy = random.randint(2, 6)

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > self.HEIGHT: 
            self.rect.y = random.randint(-100, -40)
            self.rect.x = random.randint(0, self.WIDTH - self.rect.width) 
            self.speedy = random.randint(2, 6)

# -- maybe add shots from the enemies in the next level 

