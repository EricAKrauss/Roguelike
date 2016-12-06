from Constants import *
from Controls import *

from Items.Armors import *
from Items.Weapons import *
from Actor import *

from random import randrange as rand
from math import ceil, floor

class Player(Actor):
    def setClass(self, Class):
        Class.onSpawn(self)
        Class.genEquipment(self)
        self.deriveStats()
        self.Class = Class
    
    def getAction(self):
        return self.userInput()

    def onUpdate(self):
        if hasattr(self, "Class"):
            skills = self.skills.keys()
            for skillNum in skills:
                self.skills[skillNum].update(self.skillLevels[skillNum])

    def getExp(self, exp):
        self.exp+= exp
        if self.exp >= self.expNext:
            self.pObject.pLevel.messageSys.push(self.getName()+" leveled up!")
            self.level+=1

            self.skillPoints += 1
            if (self.level-1)%4 == 0:
                self.skillPoints += 2
            
            self.expNext = int(self.expNext*(1+pow(0.95, self.level)))
            self.exp = 0
            oldMax = self.healthMax
            self.deriveStats()
            self.modHealth(self.healthMax-oldMax)

    def deriveStats(self):
        self.armorVal = 0
        HPperLevel = self.level*int(self.level/self.healthCurve)
        if self.level == 1: HPperLevel = 0
        self.healthMax = floor(self.baseHealth + max(HPperLevel, 25*(self.level-1)))
        self.health = min(self.healthMax, self.health)
        self.power = int(self.level*max(1, self.level/4))

        if self.rightHand == None:
            if self.leftHand == None:
                self.range = 1
            else:
                self.range = self.leftHand.range
        else:
            self.range = self.rightHand.range

    def throw(self, actor):
        item = self.canThrow()
        if item == None:
            return False
        if not actor.isAlive():
            return False
        if not actor.isActor():
            return False
        actor = actor.Object

        if actor.isAlly(self):
            return False

        actItem = item
        actItem = actItem.replace(' ', '')
        actItem = actItem[0].lower()+actItem[1:]
        print(actItem)
        
        actor.getAttacked(self, getattr(self, actItem).power)
        outItem = getattr(self, actItem)
        self.unequip(item)
        
        outItem.drop(actor, False)
        return True

    def isAlly(self, Actor):
        if isinstance(Actor, Player) or Actor.playerControlled:
            return True
        return False

    def getInfo(self):
        return "Stands in good health\n"

    
