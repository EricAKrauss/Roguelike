from random import seed, randint
from LevelTypes.Level import *
from LevelTypes.LevelTypes import *

class LevelManager:
    def __init__(self, gameState, playerObj, messageSys, inSeed=None):
        self.messageSys = messageSys
        self.levelList = []
        self.nextSeed = inSeed
        self.gameState = gameState
        self.cursor = 0

        self.genNewLevel(playerObj)

    def genNewLevel(self, playerObj=None):
        if self.nextSeed == None:
            inSeed = randint(0, 25500)
        else:
            inSeed = self.nextSeed
        seed(inSeed)

        if playerObj == None:
            currentLevel = self.getLevel()
            playerObj = currentLevel.thePlayer

        outLevel = levelTypes[rand(len(levelTypes))]
        print("Level", len(self.levelList)+1, inSeed)

        challengeLevel = max(len(self.levelList)+1, playerObj.level)
        newLevel = outLevel(self.gameState, playerObj, challengeLevel, inSeed)
        newLevel.name = str(len(self.levelList)+1)+newLevel.name
        self.levelList.append(newLevel)
        newLevel.levelManager = self
        newLevel.inSeed= inSeed
        newLevel.messageSys = self.messageSys
        self.nextSeed = randint(0, 25500)
        seed(randint(0, 25500))

    def getLevel(self):
        return self.levelList[self.cursor]

    def nextLevel(self):
        while self.cursor+1 >= len(self.levelList):
            self.genNewLevel()
        self.cursor+=1
        
        newLevel = self.getLevel()
        newLevel.thePlayer.pObject = newLevel.pObject

    def prevLevel(self):
        self.cursor-=1
        if self.cursor <= 0:
            self.cursor = 0

        newLevel = self.getLevel()
        newLevel.thePlayer.pObject = newLevel.pObject
