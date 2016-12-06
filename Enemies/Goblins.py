from Items.Weapons import *
from Items.Armors import *
from Items.Consumables import *
from Enemy import *
import Enemies.Enemies

from random import randrange as rand
    
class Goblin_Grunt(Enemy):
    def onSpawn(self):
        self.name = "Goblin Grunt"
        self.cowardice = 0.33
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

class Goblin_Knight(Enemy):
    def onSpawn(self):
        self.name = "Goblin Knight"
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

class Goblin_Archer(Enemy):
    def onSpawn(self):
        self.name = "Goblin Archer"
        self.cowardice = 0.5
        self.sightDist = 10

    def deriveStats(self):
        self.healthMax = 3 + self.level*int(self.level/3)
        self.health = min(self.health, self.healthMax)
        self.power = int(self.level*max(1, self.level/4))
        self.deriveRange()

    def genEquipment(self):
        newItem = Bow(self.level)
        self.equip(newItem)

        self.arrows = rand(4, 10)

        newItem = Leather_Shirt(self.level)
        self.equip(newItem)

        newItem = Cloth_Hat(self.level)
        self.equip(newItem)

class Goblin_Berserker(Enemy):
    def onSpawn(self):
        self.name = "Goblin Berserker"
        self.cowardice = 0.0
        self.sightDist = 8
        self.hearingDist=7

    def deriveStats(self):
        self.healthMax = 6 + self.level*int(self.level/2)
        self.health = min(self.health, self.healthMax)
        self.power = 1+int(self.level*max(1, self.level/3))
        self.deriveRange()

    def genEquipment(self):
        newItem = Greatsword(self.level)
        self.equip(newItem)

        newItem = Leather_Shirt(self.level)
        self.equip(newItem)

        newItem = Leather_Helm(self.level)
        self.equip(newItem)

class Goblin_Lancer(Enemy):
    def onSpawn(self):
        self.name = "Goblin Lancer"
        self.cowardice = 0.1
        self.sightDist = 9

    def deriveStats(self):
        self.healthMax = 4 + self.level*int(self.level/3)
        self.health = min(self.health, self.healthMax)
        self.power = int(self.level*max(1, self.level/4))
        self.deriveRange()

    def genEquipment(self):
        newItem = Spear(self.level)
        self.equip(newItem)

        newItem = Buckler(self.level)
        self.equip(newItem)

        newItem = Leather_Shirt(self.level)
        self.equip(newItem)

        newItem = Leather_Helm(self.level)
        self.equip(newItem)

class Goblin_Stonewall(Enemy):
    def onSpawn(self):
        self.name = "Goblin Stonewall"
        self.cowardice = 0.0
        self.sightDist = 6

    def deriveStats(self):
        self.healthMax = 8 + self.level*int(self.level/3)
        self.health = min(self.health, self.healthMax)
        self.power = int(self.level*max(1, self.level/3.5))
        self.deriveRange()

    def genEquipment(self):
        newItem = Mace(self.level)
        self.equip(newItem)

        newItem = Iron_Shield(self.level)
        self.equip(newItem)

        newItem = Iron_Breastplate(self.level)
        self.equip(newItem)

        newItem = Iron_Helm(self.level)
        self.equip(newItem)

class Goblin_Thief(Enemy):
    def onSpawn(self):
        self.name = "Goblin Thief"
        self.cowardice = 1.0
        self.sightDist = 9
        self.optionalTargets = [Item]
        self.isAfraid = False

    def deriveStats(self):
        self.healthMax = 4 + self.level*int(self.level/3)
        self.health = min(self.health, self.healthMax)
        self.power = int(self.level*max(1, self.level/4))
        self.deriveRange()

    def genEquipment(self):
        newItem = Dagger(self.level)
        self.equip(newItem)

        newItem = Dagger(self.level)
        self.equip(newItem)
        
        newItem = Leather_Shirt(self.level)
        self.equip(newItem)

        newItem = Leather_Helm(self.level)
        self.equip(newItem)

    def genGoals(self):
        return Enemies.Enemies.genItemGoals(self)

enemyList = [Goblin_Lancer, Goblin_Berserker,
             Goblin_Archer, Goblin_Knight, Goblin_Grunt,
             Goblin_Thief]

eliteList = [Goblin_Stonewall]
##enemyList = [Goblin_Thief]
