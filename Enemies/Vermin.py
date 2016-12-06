from Items.Weapons import *
from Items.Armors import *
from Items.Consumables import *
from Enemy import *
from Items.ItemEffects import *

from random import randrange as rand

class Rat_Nest(Enemy):
    def onSpawn(self):
        self.name = "Rat's Nest"
        self.char = NEST
        self.color= COLOR_HAZARD
        self.cowardice = 0.0
        self.sightDist = 9

        self.rats = []
        self.ratsMax = 5

        self.cdMax=4
        self.cd=self.cdMax

    def deriveStats(self):
        self.healthMax = 4 + self.level*int(self.level/3)
        self.health = min(self.health, self.healthMax)
        self.power = int(self.level*max(1, self.level/4))
        self.deriveRange()

    def genEquipment(self):
        pass        

    def getAction(self):
        if self.cd < self.cdMax:
            self.cd += 1
            return True

        for i in range(len(self.rats)):
            if not self.rats[i].health <= 0:
                self.rats.pop(i)
                i -= 1

        row = self.pObject.row
        col = self.pObject.col
        level = self.pObject.pLevel
        if len(self.rats) < self.ratsMax:
            adjSpots = getAdjSpaces(level.maze, row, col)
            shuffle(adjSpots)
            for spot in adjSpots:
                r = spot[0]
                c = spot[1]
                if not level.Tiles[r][c].isObstacle():
                    self.cd = 0
                    cLevel = level.cLevel
                    newRat = Rat_Large("Large Rat", cLevel)
                    newRat.char = 'x'
                    level.createNew(r, c, newRat)
                    self.rats.append(newRat)
                    return True

class Rat_Large(Enemy):
    def onSpawn(self):
        self.name = "Large Rat"
        self.cowardice = 0.66
        self.sightDist = 9

    def deriveStats(self):
        self.healthMax = 4 + self.level*int(self.level/3)
        self.health = min(self.health, self.healthMax)
        self.power = int(self.level*max(1, self.level/4))
        self.deriveRange()

    def genEquipment(self):
        pass

    def genGoals(self):
        return genObjectGoals(Rat_Queen)

class Rat_Queen(Enemy):
    def onSpawn(self):
        self.name = "Rat Queen"
        self.cowardice = 0.66
        self.sightDist = 9

    def deriveStats(self):
        self.healthMax = 4 + self.level*int(self.level/3)
        self.health = min(self.health, self.healthMax)
        self.power = int(self.level*max(1, self.level/4))
        self.deriveRange()

    def genEquipment(self):
        pass

class Slime_Green(Enemy):
    def onSpawn(self):
        self.name = "Green Slime"
        self.cowardice = 0.0
        self.sightDist = 9
        self.hitEffects.append(hitArmorRend(15))

    def deriveStats(self):
        self.healthMax = 7 + self.level*int(self.level/2)
        self.health = min(self.health, self.healthMax)
        self.power = int(self.level*max(2, self.level/3))
        self.deriveRange()

    def genEquipment(self):
        pass


enemyList = [Rat_Large, Rat_Queen, Slime_Green]
eliteList = [Rat_Nest]
