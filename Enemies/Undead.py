from Items.Weapons import *
from Items.Armors import *
from Items.Consumables import *
from Enemy import *
import Enemies.Enemies

from random import randrange as rand

class Zombie(Enemy):
    def onSpawn(self):
        self.name = "Zombie"
        self.char = 'z'
        self.cowardice = 0.0
        self.sightDist = 9

    def deriveStats(self):
        self.healthMax = 4 + self.level*int(self.level/3)
        self.health = min(self.health, self.healthMax)
        self.power = int(self.level*max(1, self.level/4))
        self.deriveRange()

    def genEquipment(self):
        newItem = Longsword(self.level)
        self.equip(newItem)

        newItem = Leather_Shirt(self.level)
        self.equip(newItem)

        newItem = Leather_Helm(self.level)
        self.equip(newItem)

class Skeleton_Knight(Enemy):
    def onSpawn(self):
        self.name = "Skeleton Knight"
        self.char = 's'
        self.cowardice = 0.0
        self.sightDist = 8

    def deriveStats(self):
        self.healthMax = 6 + self.level*int(self.level/2)
        self.health = min(self.health, self.healthMax)
        self.power = 1+int(self.level*max(1, self.level/3.5))
        self.deriveRange()

    def genEquipment(self):
        newItem = Longsword(self.level)
        self.equip(newItem)

        newItem = Wooden_Shield(self.level)
        self.equip(newItem)

        newItem = Leather_Shirt(self.level)
        self.equip(newItem)

        newItem = Iron_Helm(self.level)
        self.equip(newItem)

class Cultist(Enemy):
    def onSpawn(self):
        print("Yo, Cultist here")
        self.name = "Robed Cultist"
        self.char = 'C'
        self.cowardice = 0.0
        self.sightDist = 8
        self.healNum = max(10, int(22.5+(self.level*5)*self.level/2))
        self.cdMax = 6
        self.cd = self.cdMax
        self.healCDMax = 3
        self.healCD = self.healCDMax

    def onAI(self, target):
        self.cd += 1
        self.healCD += 1
        messager  = self.pObject.pLevel.messageSys
        if target != None:
            target = target.Object
            if self.cd >= self.cdMax:
                target.modHealth(-(self.power + self.getMagPower()))
                self.cd = 0
                messager.push(self.getName() + " shocked "+ target.getName() +" for "+str(self.power + self.getMagPower()))
                return True
        
        lowestHealth = self.health/self.healthMax
        healTarget = self
        if self.healCD >= self.healCDMax:
            for ally in self.alliesList:
                ally = ally.Object
                if ally.health/ally.healthMax:
                    lowestHealth = ally.health/ally.healthMax
                    healTarget = ally
            if lowestHealth <= .9:
                self.healCD = 0
                healTarget.modHealth(self.healNum)
                messager.push(self.getName() + " healed " + healTarget.getName())
                return True
        

    def deriveStats(self):
        self.healthMax = 6 + self.level*int(self.level/2)
        self.health = min(self.health, self.healthMax)
        self.power = 1+int(self.level*max(1, self.level/3.5))
        self.deriveRange()

    def genEquipment(self):
        newItem = Staff(self.level)
        self.equip(newItem)

        newItem = Tome(self.level)
        self.equip(newItem)

        newItem = Cloth_Shirt(self.level)
        self.equip(newItem)

        newItem = Cloth_Hat(self.level)
        self.equip(newItem)

enemyList = [Zombie, Skeleton_Knight]
eliteList = [Cultist]
