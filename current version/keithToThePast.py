import pygame, sys,items,random
sys.path.insert(0,'levels/')
from constants import w_width, w_height, colors, playerSpeed, playerPath1, playerPath2
import player, level1, level2, sounds
import cutscenes, cutsceneText

def reset(sink,soundEffects,initRect,initCrystal,crystalList):
    sink = items.Sink(150,font,10)
    soundEffects = sounds.SoundFX()
    initRect = pygame.Rect(-4000,-4000,25,25)
    initCrystal = items.Crystal(initRect)
    crystalList= [initCrystal]


# Return array of keys pressed
def getKeys(keys):
    pressed = []
    if keys[pygame.K_a]:
        pressed.append(pygame.K_a)
    if keys[pygame.K_d]:
        pressed.append(pygame.K_d)
    if keys[pygame.K_w]:
        pressed.append(pygame.K_w)
    if keys[pygame.K_s]:
        pressed.append(pygame.K_s)
    return pressed
    


if __name__ == '__main__':
    pygame.init()

    # initialize font; must be called after 'pygame.init()' to avoid 'Font not Initialized' error
    font = pygame.font.SysFont("monospace", 15)
    gameClock = pygame.time.Clock()
    screen = pygame.display.set_mode([w_width,w_height])
    screen.fill(colors['black'])
    # screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)

    pygame.display.set_caption('Use WASD to move, collect crystals by pressing SPACE, drop crystals into the red box by pressing K, avoid the bears and wolves!! (oh my!) Press ESCAPE to QUIT')

    # play intro cutscene
    cutscenes.playCutscene(screen, cutsceneText.text["intro_cutscene"])

    level = level1.level(screen)
    levelNum = 1

    # play level cutscene
    level.playCutscene(levelNum)

    keith = player.Player((level.startingPosX,level.startingPosY), playerPath2, playerSpeed)
    #keith = player.Player((x,y), playerPath1, playerSpeed)

    sink = items.Sink(150,font,10)
    soundEffects = sounds.SoundFX()
    initRect = pygame.Rect(-4000,-4000,25,25)
    initCrystal = items.Crystal(initRect)
    crystalList= [initCrystal]

    pygame.draw.rect(screen,colors['green'],initRect,3)
    #sink.draw(screen)
    pygame.display.update()

    frameCount = 0

    while True:

        if pygame.mixer.music.get_busy() == False:
            level.playLvlMusic(levelNum)

        frameCount+=1
        if sink.itemsHeld == 10:
              # print "player score is : " + str(keith.score)
              # sys.exit()
            reset(sink,soundEffects,initRect,initCrystal,crystalList)
            level = level2.level(screen)
            levelNum = 2;
            sink.itemsHeld += 1
            level.playLvlMusic(levelNum)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print "player score is : " + str(keith.score)
                sys.exit()

        keys = pygame.key.get_pressed()
        pressed = getKeys(keys)

        # Check for obstacle collisions
        index = 0
        # blocked = False
        # for obstacle in level.obstacles:
        #     if obstacle.rect.colliderect(keith.rectangle):
        #         blocked = True
        #         break

        # React to key press
        level.background.handle(keys,keith)
        update = keith.handle(keys,level.background)
        level.updateEnemies(keith,keys,crystalList)

        # generate new crystal that does not collide with player or sink
        if(frameCount == 90):
            frameCount = 0
            if(len(crystalList) < 10): # quick way of limiting us to 10 items (or however many crystals, can be changed depending on level.)
                crystalList.append(items.createRandomRect(w_width,w_height,41,36,keith.rectangle,sink.rect))
            elif(len(crystalList) > 0):
                del crystalList[1]
                crystalList.append(items.createRandomRect(w_width,w_height,41,36,keith.rectangle,sink.rect))

        # Check for collisions, update speed and score
        index = 0
        while index < len(crystalList):
            if(crystalList[index].rect.colliderect(keith.rectangle)):
                if(keys[pygame.K_SPACE]):
                    soundEffects.playChime()
                    del crystalList[index]
                    index = index-1
                    keith.itemsHeld = keith.itemsHeld + 1
                    if keith.speed > 5 :
                        keith.updateSpeed()
                    else:
                        keith.speed = 5
            index+=1


        if update is not None:
            if sink.rect.colliderect(keith.rectangle): # dropping in the sink
                sink.take()
                keith.score += 1
            else:
                # player dropped an item and we need to re-draw it
                crystalList.append(update)

        level.draw(crystalList,sink,keith)
        pygame.display.update()
        gameClock.tick(30)
