# -- -- -- Prototype for skin selector component 
# -- -- -- -- in final version move skins array into app layer and move img skins directory into main directory 
# -- -- -- -- add game state to final version like selecting, ... 
# -- -- -- -- example images used 
import pygame 
import pygame.freetype 
import sys


RES = WIDTH, HEIGHT = 1200, 700 

# -- app layer 
class Game:
    def __init__(self):
        pygame.init() 
        self.screen = pygame.display.set_mode(RES) 
        pygame.display.set_caption('skin') 
        self.skin_selector = Selector(self.screen) 

    def update(self):
        pygame.display.flip() 

    def draw(self):
        self.screen.fill('black') 
        self.skin_selector.draw(self.screen) 
        
    
    def check_events(self):
        for event in pygame.event.get(): 

            self.skin_selector.check_events(event) 

            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit() 
            

    # -- start game processes 
    def run(self): 
        while True:
            self.check_events()
            self.update()
            self.draw() 
    



# -- skin selector UI 
class Selector:
    def __init__(self, screen):
        self.screen = screen 
        # -- canvas dimensions 
        self.WIDTH = self.screen.get_width() 
        self.HEIGHT = self.screen.get_height() 
        
        # -- move this into the game layer for reusing the skin objects in the game 
        # -- here goes the skin name which has to match the image name 
        self.skinNames = ['patrick', 'bird', 'count-dooku', 'sailer']
        self.skins = [] 
        for i, skinName in enumerate(self.skinNames):
            self.skins.append(Skin(skinName, i)) 
        self.selectedSkin = 0 
        self.initUI() 
        
        
            

    # -- draw the whole component including the currently selected skin 
    def draw(self, screen): 
        self.drawUI(screen) 
        temp_skin = self.skins[self.selectedSkin]
        screen.blit(temp_skin.image, (self.WIDTH / 2 - temp_skin.dimensions[0] / 2, HEIGHT / 2 - temp_skin.dimensions[1] / 2)) 
        
        

    # -- load arrows and other images 
    def initUI(self): 
        self.arrowDimensions  = (100, 100) 
        self.arrow_left_img = pygame.image.load('./img/arrow-left.png') 
        self.arrow_right_img = pygame.image.load('./img/arrow-right.png') 
        self.initText() 
        
        
        
        
        
    def initText(self): 
        # -- font definition 
        self.titleFont = pygame.freetype.SysFont("helvetica neue, helvetica, arial", 65) 
        self.normal_font = pygame.freetype.SysFont("helvetica neue, helvetica, arial", 22) 
        self.next_text, _ = self.normal_font.render("next", (240, 245, 250)) 
        
        # -- draw the name of the first skin 
        self.update_selection() 
    
    
    # -- draw UI of Selector 
    def drawUI(self, screen): 
        # -- size image transformation 
        pygame.transform.scale(self.arrow_left_img, self.arrowDimensions) 
        pygame.transform.scale(self.arrow_right_img, self.arrowDimensions) 
        # -- arrows 
        self.left_arrow = screen.blit(self.arrow_left_img, (self.WIDTH / 10 * 0, self.HEIGHT / 2 - self.arrowDimensions[0] / 2)) 
        self.right_arrow = screen.blit(self.arrow_right_img, (self.WIDTH / 10 * 9 , self.HEIGHT / 2 - self.arrowDimensions[0] / 2)) 
        self.button = pygame.draw.rect(self.screen, (20, 40, 240), pygame.Rect(self.WIDTH / 2 - 100, self.HEIGHT / 8 * 7, 200, 50), 0, 6) 
        # -- text 
        self.drawText() 

    # -- draw text from init text function 
    def drawText(self):
        # -- draw title text 
        self.screen.blit(self.titleText, (self.WIDTH / 2 - self.titleText.get_width() / 2, HEIGHT / 8)) 
        # -- draw text on the button 
        self.screen.blit(self.next_text, (self.button.center[0] - self.next_text.get_rect().width / 2, self.button.center[1] - self.next_text.get_rect().height / 2)) 
        
    def update_selection(self): 
        self.titleText, _ = self.titleFont.render(self.skins[self.selectedSkin].name, (255, 255, 255))  
        
        
    # -- action when next button was pressed 
    def select(self, skin_index): 
        skin_ID = skin_index + 1 
        print("skin " + str(skin_ID) + " was selected ") 
        # -- handle outside communication that the selector exits out and disappears and hands over the information about the selected skin 


    # -- event handling 
    def check_events(self, event): 
        # -- click event 
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos() 
            # -- handle arrow click -- 
            # -- left increase self.selectedSkin by 1 -- 
            # -- right decrease by 1 if not 0, in this case set it to len(self.skins) 
            print(pos) 
            if self.right_arrow.collidepoint(pos):
                print("clicked") 
                if(self.selectedSkin != (len(self.skins) - 1)):
                    self.selectedSkin += 1 
                    self.update_selection() 
                    
                else:
                    self.selectedSkin = 0 
            
            if self.left_arrow.collidepoint(pos):
                print("clicked") 
                if(self.selectedSkin != 0):
                    self.selectedSkin -= 1 
                    self.update_selection()  
                else:
                    self.selectedSkin = len(self.skins) - 1 
            
            if self.button.collidepoint(pos):
                self.select(self.selectedSkin) 
            
             
    

# -- skin object 
class Skin:
    def __init__(self, name, ID):
        self.name = name 
        self.ID = ID 
        # -- define file directory for skins as ./img/skins/ followed by 
        # -- the naming pattern for the skin image files as png 
        # -- $name+of+skin-skin.png 
        self.imagePath = './img/skins/' + name + '-skin.png' 
        self.imageRaw = pygame.image.load(self.imagePath) # -- no size customized 
        self.dimensions = (300, 400)
        self.image = pygame.transform.scale(self.imageRaw, (self.dimensions[0], self.dimensions[1])) 
        # -- maybe add presentation image for the skin for different view than in the game 
        # -- maybe also add a sound that could be played on selection 
        
    
    def getImage(self):
        return self.image 
    
    


game = Game() 
game.run() 


