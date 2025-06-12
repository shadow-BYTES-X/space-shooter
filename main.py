from data import * 
from player import * 
from enemy import * 
from boss import * 
from bullet import * 
from boss_bullet import * 
import pygame 
import pygame.freetype 
import sys 
import random 
import time 

# -- app layer 
class Game:
    def __init__(self):
        pygame.init() 
        self.screen = pygame.display.set_mode(RES) 
        pygame.display.set_caption('space shooter') 
        self.define_colors() 
        self.init_game() 
        self.running = False 
        

    def define_colors(self):
        self.RED = (255, 0, 0) 
        self.BLACK = (0, 0, 0) 
        self.WHITE = (255, 255, 255) 
    

    def draw_text(self, surf, text, size, x, y, color=(255, 255, 255)):
        font = pygame.freetype.SysFont("helvetica neue, helvetica, Arial", size) 
        text_surface, text_rect = font.render(text, color) 
        text_rect.x = x 
        text_rect.y = y 
        surf.blit(text_surface, text_rect) 

    def init_game(self): 
        
        # -- reset variables 
        self.all_sprites = pygame.sprite.Group() 
        self.bullets = pygame.sprite.Group()
        self.boss_bullets = pygame.sprite.Group() 
        self.player = Player(self.all_sprites, self.bullets, Bullet, self.screen, "count dooku") 
        self.all_sprites.add(self.player) 
        self.enemies = pygame.sprite.Group() 
        for _ in range(5):
            enemy = Enemy(self.screen) 
            self.all_sprites.add(enemy)
            self.enemies.add(enemy) 
        self.boss = None
        self.level = 1 
        self.start_time = time.time() 
        self.score = 0 
    

    def update(self): 
        # -- update positions and state of the elements and actors 
        self.all_sprites.update() 
        pygame.display.flip() 

    def draw(self):
        self.screen.fill('black') 
        self.screen.fill(self.BLACK)
        self.all_sprites.draw(self.screen)
        self.draw_text(self.screen, f"Leben: {str(self.player.lives)}", 30, 10, 10) 
        self.draw_text(self.screen, f"Zeit: {60 - self.elapsed_time}", 30, WIDTH - 150, 10) 
        self.draw_text(self.screen, str(self.score), 30, WIDTH / 2, 10) 
        
        
    
    def check_events(self): 
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self.stop() 
                pygame.quit()
                sys.exit() 
    
    def check_collisions(self):
        hits = pygame.sprite.groupcollide(self.enemies, self.bullets, True, True)
        for _ in hits: 
            # -- update score 
            self.score += 1
            enemy = Enemy(self.screen) 
            self.all_sprites.add(enemy) 
            self.enemies.add(enemy)
    
        player_hits = pygame.sprite.spritecollide(self.player, self.boss_bullets, True)
        if player_hits:
            self.player.lives -= 1
            if self.player.lives <= 0:
                self.init_game() 
    
        enemy_hits = pygame.sprite.spritecollide(self.player, self.enemies, True)
        if enemy_hits:
            self.player.lives -= 1
            if self.player.lives <= 0: 
                self.init_game() 
        
        

    # -- handle level progrss 
    def progress(self): 
        self.elapsed_time = int(time.time() - self.start_time) 
        if self.level == 1 and self.elapsed_time >= 60:
            self.level = 2
            self.boss = Boss(self.all_sprites, self.boss_bullets, BossBullet, self.screen)  
            self.all_sprites.add(self.boss) 
            

    # -- start game processes and game loop 
    def run(self): 
        self.running = True
        clock = pygame.time.Clock() 
        while self.running: 
            clock.tick(FPS) 
            self.check_events()
            self.update() 
            self.check_collisions() 
            self.progress() 
            self.draw() 
    
    def stop(self):
        self.running = False 
        print("game was stopped") 
        print("\n") 
        #print(self.status()) 
    
    # -- optional status report containing information about the lives remaining, the time spent and if the boss was seen 
    def status(self): 
        boss_state = "No" 
        if self.boss != None:
            boss_state = "Yes" 
        lives = "lives: \t \t \t" + str(self.player.lives) 
        # -- add standard level length to make the time work 
        time = "time to next level: \t" + str(self.elapsed_time) 
        boss = "boss was seen: \t \t" + str(boss_state)
        report = lives + "\n" + time + "\n" + boss + "\n" 
        return report 

    

app = Game() 

if __name__ == '__main__':
    app.run() 

