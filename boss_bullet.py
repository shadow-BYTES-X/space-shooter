from main import * 
import pygame 

class BossBullet(pygame.sprite.Sprite):
    def __init__(self, x, y, screen):
        super().__init__() 
        self.screen = screen 
        self.HEIGHT = self.screen.get_height() 
        self.image = pygame.Surface((10, 20))
        self.image.fill((255, 0, 0)) 
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speedy = 5

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > self.HEIGHT: 
            self.kill()
