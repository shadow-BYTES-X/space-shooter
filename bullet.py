import pygame 

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 10))
        self.image.fill((255,255,255)) 
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speedy = -7

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()
