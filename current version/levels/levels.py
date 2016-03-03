from constants import colors, w_width, w_height
import pygame, cutscenes

class levels():

    def __init__(self,screen):
        self.screen = screen
        self.music = ["assets/music/keithDenial.mp3","assets/music/BargainingKeith.mp3"]
        self.font =  pygame.font.SysFont("monospace", 15)

    def drawEnemies(self,enemies):
        for enemy in enemies:
            pygame.draw.rect(self.screen,colors['blue'],enemy.detection,3)
            self.screen.blit(enemy.image, enemy.rectangle)

    def drawItems(self,crystalList,sink,bg):
        sink.draw(self.screen,bg.x,bg.y,bg.offset)

        for crystal in crystalList:
            crystal.rect.x = crystal.origX + (bg.x + bg.offset)
            crystal.rect.y = crystal.origY + (bg.y + bg.offset)
            pygame.draw.rect(self.screen,colors['green'],crystal.rect,3)
            self.screen.blit(crystal.sheet, crystal.rect)

    def playLvlMusic(self,lvlNumber):
        pygame.mixer.music.load(self.music[lvlNumber-1])
        pygame.mixer.music.play(-1)

    def drawText(self,keith):
        text = self.font.render('You are carrying '+str(keith.itemsHeld)+' crystals', 1,colors['blue'])
        textpos = pygame.Rect(10,10,w_width/2,w_height/2)
        self.screen.blit(text, textpos)

    def playCutscene(self,level):
        if (level == 1):
            cutscenes.playCutscene1(self.screen,self.font)