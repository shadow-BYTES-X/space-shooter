import pygame
import random
import time

# Initialisierung
pygame.init()

# Bildschirmgröße
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Advanced Shmup")

# Farben
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Lade Bilder
player_img = pygame.image.load("player.png")
enemy_img = pygame.image.load("enemy.png")
boss_img = pygame.image.load("boss.png")

font = pygame.font.SysFont(None, 36)

def draw_text(surf, text, size, x, y, color=WHITE):
    font = pygame.font.SysFont(None, size)
    text_surface = font.render(text, True, color)
    surf.blit(text_surface, (x, y))

# Spielerklasse
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(player_img, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 10
        self.speed = 5
        self.lives = 3

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed
    
    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)

# Gegnerklasse
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(enemy_img, (40, 40))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.speedy = random.randint(2, 6)

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.rect.y = random.randint(-100, -40)
            self.rect.x = random.randint(0, WIDTH - self.rect.width)
            self.speedy = random.randint(2, 6)

# Bullet-Klasse
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 10))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speedy = -7

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

# Boss-Klasse
class Boss(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(boss_img, (100, 100))
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.y = 50
        self.speedx = 3
        self.shoot_timer = 0

    def update(self):
        self.rect.x += self.speedx
        if self.rect.right > WIDTH or self.rect.left < 0:
            self.speedx *= -1
        
        self.shoot_timer += 1
        if self.shoot_timer > 60:
            self.shoot()
            self.shoot_timer = 0
    
    def shoot(self):
        bullet = BossBullet(self.rect.centerx, self.rect.bottom)
        all_sprites.add(bullet)
        boss_bullets.add(bullet)

# Boss-Bullet-Klasse
class BossBullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 20))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speedy = 5

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.kill()

# Neustart-Funktion
def restart_game():
    global all_sprites, enemies, bullets, boss_bullets, player, boss, level, start_time
    all_sprites = pygame.sprite.Group()
    player = Player()
    all_sprites.add(player)
    enemies = pygame.sprite.Group()
    for _ in range(5):
        enemy = Enemy()
        all_sprites.add(enemy)
        enemies.add(enemy)
    bullets = pygame.sprite.Group()
    boss_bullets = pygame.sprite.Group()
    boss = None
    level = 1
    start_time = time.time()

restart_game()

# Spiel-Schleife
running = True
clock = pygame.time.Clock()
while running:
    clock.tick(60)
    
    # Events verarbeiten
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()
    
    # Updates
    all_sprites.update()
    
    # Kollisionen prüfen
    hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
    for hit in hits:
        enemy = Enemy()
        all_sprites.add(enemy)
        enemies.add(enemy)
    
    player_hits = pygame.sprite.spritecollide(player, boss_bullets, True)
    if player_hits:
        player.lives -= 1
        if player.lives <= 0:
            restart_game()
    
    enemy_hits = pygame.sprite.spritecollide(player, enemies, True)
    if enemy_hits:
        player.lives -= 1
        if player.lives <= 0:
            restart_game()
    
    elapsed_time = int(time.time() - start_time)
    if level == 1 and elapsed_time >= 60:
        level = 2
        boss = Boss()
        all_sprites.add(boss)
    
    # Zeichnen
    screen.fill(BLACK)
    all_sprites.draw(screen)
    draw_text(screen, f"Leben: {player.lives}", 30, 10, 10)
    draw_text(screen, f"Zeit: {60 - elapsed_time}", 30, WIDTH - 150, 10)
    pygame.display.flip()
    
pygame.quit()
