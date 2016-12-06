from Item import Item
from math import floor, ceil
from random import randrange as rand

from Object import *
from Constants import *
from Items.ItemEffects import *

def weaponGetInfo(self):
        outString = "level "+str(self.level)+": "

        if self.power > 0 and self.power >= self.magPower:
                outString+= str(self.power)+" power, "
        if self.magPower > self.power:
                outString+= str(self.magPower)+" magic power, "
        if hasattr(self, "armorVal"):
                outString+= str(self.armorVal)+" armor, "
        if self.type == "2H":
                outString+= "2H, "
        if self.type == "0H":
                outString+= "can be used w/ a 2H weapon, "
        if self.range > 1:
                outString+= str(self.range)+" reach, "
                
        outString+= str(self.weight)+" weight"
        if self.throwable:
            outString+= ", can be thrown"
        if self.usesArrows:
            outString+= ", uses arrows"
        return outString+'\n'

def weaponGenBonuses(self, bonus):
        effectList = WeaponEffects(self.level)
        for i in range(bonus):
                options = range(len(effectList))
                effectI = options.pop(rand(len(options)))
                self.hitEffects.append(effectList[effectI])
                

def weaponUse(self, actor):
    if not actor.equip(self):
        return False
    self.pop(actor)
    messager = actor.pObject.pLevel.messageSys
    messager.push(actor.getName()+" equipped "+self.getName())
    return True

class Longsword(Item):
    def __init__(self, lvl=1, bonus=0):
        self.power = max(2, int(1+lvl*lvl/2))
        self.armorPen = floor(int(lvl*5))
        self.magPower = 1
        self.level = lvl
        
        self.color= COLOR_DEFAULT
        self.char = '?'
        self.type = "1H"
        self.name = "Longsword"

        self.equippable = True
        self.consumable = False
        self.throwable = False
        self.addPower = True
        self.usesArrows = False
        
        self.range = 1
        self.weight= 8
        
        if bonus > 0:
            self.name = "+"+str(bonus)+" "+self.name
            weaponGenBonuses(self, bonus)

    def getInfo(self):
        return weaponGetInfo(self)

    def use(self, actor):
        return weaponUse(self, actor)

class Buckler(Item):
    def __init__(self, lvl=1, bonus=0):
        self.level = lvl
        
        self.color= COLOR_DEFAULT
        self.char = '?'
        self.type = "0H"
        self.name = "Buckler"

        self.equippable = True
        self.consumable = False
        self.throwable = False
        self.addPower = True
        self.usesArrows = False

        self.power = 0
        self.magPower = 0
        self.range = 1
        self.armorVal = 3
        self.weight= 4
        
        if bonus > 0:
            self.name = "+"+str(bonus)+" "+self.name

    def getInfo(self):
        return weaponGetInfo(self)

    def use(self, actor):
        return weaponUse(self, actor)

class Iron_Shield(Item):
    def __init__(self, lvl=1, bonus=0):
        self.level = lvl
        
        self.color= COLOR_DEFAULT
        self.char = '?'
        self.type = "1H"
        self.name = "Iron Shield"

        self.equippable = True
        self.consumable = False
        self.throwable = False
        self.addPower = True
        self.usesArrows = False

        self.power = 0
        self.magPower = 0
        self.range = 1
        self.armorVal = 12
        self.weight= 15
        
        if bonus > 0:
            self.name = "+"+str(bonus)+" "+self.name

    def getInfo(self):
        return weaponGetInfo(self)

    def use(self, actor):
        return weaponUse(self, actor)

class Wooden_Shield(Item):
    def __init__(self, lvl=1, bonus=0):
        self.level = lvl
        
        self.color= COLOR_DEFAULT
        self.char = '?'
        self.type = "1H"
        self.name = "Wooden Shield"

        self.equippable = True
        self.consumable = False
        self.throwable = False
        self.addPower = True
        self.usesArrows = False

        self.power = 0
        self.magPower = 0
        self.range = 1
        self.armorVal = 6
        self.weight= 7
        
        if bonus > 0:
            self.name = "+"+str(bonus)+" "+self.name

    def getInfo(self):
        return weaponGetInfo(self)

    def use(self, actor):
        return weaponUse(self, actor)

class Staff(Item):
    def __init__(self, lvl=1, bonus=0):
        self.power = max(1, int(1+lvl*lvl/3))
        self.magPower = max(3, int(1+lvl*lvl/1.5))
        self.armorPen = floor(int(lvl*5))
        self.level = lvl
        
        self.color= COLOR_DEFAULT
        self.char = '?'
        self.type = "2H"
        self.name = "Staff"

        self.equippable = True
        self.consumable = False
        self.throwable = False
        self.addPower = True
        self.usesArrows = False
        
        self.range = 1
        self.weight= 8
        
        if bonus > 0:
            self.name = "+"+str(bonus)+" "+self.name
            weaponGenBonuses(self, bonus)

    def getInfo(self):
        return weaponGetInfo(self)

    def use(self, actor):
        return weaponUse(self, actor)

class Wand(Item):
    def __init__(self, lvl=1, bonus=0):
        self.power = max(1, int(1+lvl*lvl/3))
        self.magPower = max(3, int(1+lvl*lvl/2.25))
        self.armorPen = floor(int(lvl*5))
        self.level = lvl
        
        self.color= COLOR_DEFAULT
        self.char = '?'
        self.type = "1H"
        self.name = "Wand"

        self.equippable = True
        self.consumable = False
        self.throwable = False
        self.addPower = False
        self.usesArrows = False
        
        self.range = 1
        self.weight= 8
        
        if bonus > 0:
            self.name = "+"+str(bonus)+" "+self.name
            weaponGenBonuses(self, bonus)

    def getInfo(self):
        return weaponGetInfo(self)

    def use(self, actor):
        return weaponUse(self, actor)

class Tome(Item):
    def __init__(self, lvl=1, bonus=0):
        self.power = 0
        self.magPower = max(2, int(1+lvl*lvl/3))
        self.armorPen = 0
        self.level = lvl
        
        self.color= COLOR_DEFAULT
        self.char = '?'
        self.type = "0H"
        self.name = "Tome"

        self.equippable = True
        self.consumable = False
        self.throwable = False
        self.addPower = False
        self.usesArrows = False
        
        self.range = 1
        self.weight= 8
        
        if bonus > 0:
            self.name = "+"+str(bonus)+" "+self.name
            weaponGenBonuses(self, bonus)

    def getInfo(self):
        return weaponGetInfo(self)

    def use(self, actor):
        return weaponUse(self, actor)

class Dagger(Item):
    def __init__(self, lvl=1, bonus=0):
        self.power = max(1, ceil(0.6*int(1+lvl*lvl/2)))
        self.armorPen = floor(int(lvl*5))
        self.magPower = 1
        self.level = lvl
        
        self.color= COLOR_DEFAULT
        self.char = '?'
        self.type = "1H"
        self.name = "Dagger"

        self.equippable = True
        self.consumable = False
        self.throwable = False
        self.addPower = True
        self.usesArrows = False

        self.range = 1
        self.weight= 2
        
        if bonus > 0:
            self.name = "+"+str(bonus)+" "+self.name
            weaponGenBonuses(self, bonus)

    def getInfo(self):
        return weaponGetInfo(self)

    def use(self, actor):
        return weaponUse(self, actor)

class Spear(Item):
    def __init__(self, lvl=1, bonus=0):
        self.power = max(1, floor(1.1*int(1+lvl*lvl/2)))
        self.armorPen = floor(int(lvl*5))
        self.magPower = 1
        self.level = lvl
        
        self.color= COLOR_DEFAULT
        self.char = '?'
        self.type = "2H"
        self.name = "Spear"
        
        self.equippable = True
        self.consumable = False
        self.throwable = False
        self.addPower = True
        self.usesArrows = False

        self.range = 2
        self.weight= 15
        
        if bonus > 0:
            self.name = "+"+str(bonus)+" "+self.name
            weaponGenBonuses(self, bonus)

    def getInfo(self):
        return weaponGetInfo(self)

    def use(self, actor):
        return weaponUse(self, actor)

class Mace(Item):
    def __init__(self, lvl=1, bonus=0):
        self.power = max(2, int(1+lvl*lvl/2))
        self.armorPen = 15 + floor(int(lvl*5))
        self.magPower = 1
        self.level = lvl
        
        self.color= COLOR_DEFAULT
        self.char = '?'
        self.type = "1H"
        self.name = "Mace"

        self.equippable = True
        self.consumable = False
        self.throwable = False
        self.addPower = True
        self.usesArrows = False
        
        self.range = 1
        self.weight= 12
        
        if bonus > 0:
            self.name = "+"+str(bonus)+" "+self.name
            weaponGenBonuses(self, bonus)

    def getInfo(self):
        return weaponGetInfo(self)

    def use(self, actor):
        return weaponUse(self, actor)

class Greatsword(Item):
    def __init__(self, lvl=1, bonus=0):
        self.power = max(1, ceil(2.1*int(1+lvl*lvl/2)))
        self.armorPen = floor(int(lvl*5))
        self.magPower = 1
        self.level = lvl
        
        self.color= COLOR_DEFAULT
        self.char = '?'
        self.type = "2H"
        self.name = "Greatsword"
        
        self.equippable = True
        self.consumable = False
        self.throwable = False
        self.addPower = True
        self.usesArrows = False

        self.range = 1
        self.weight= 15
        
        if bonus > 0:
            self.name = "+"+str(bonus)+" "+self.name
            weaponGenBonuses(self, bonus)

    def getInfo(self):
        return weaponGetInfo(self)

    def use(self, actor):
        return weaponUse(self, actor)

class Bow(Item):
    def __init__(self, lvl=1, bonus=0):
        self.power = max(1, ceil(0.8*int(1+lvl*lvl/2)))
        self.armorPen = floor(int(lvl*5))
        self.magPower = 1
        self.level = lvl
        
        self.color= COLOR_DEFAULT
        self.char = '?'
        self.type = "2H"
        self.name = "Bow"
        
        self.equippable = True
        self.consumable = False
        self.throwable = False
        self.addPower = False
        self.usesArrows = True

        self.range = 5
        self.weight= 8
        
        if bonus > 0:
            self.name = "+"+str(bonus)+" "+self.name
            weaponGenBonuses(self, bonus)

    def getInfo(self):
        return weaponGetInfo(self)

    def use(self, actor):
        return weaponUse(self, actor)


weaponList = [Staff, Iron_Shield, Buckler, Wooden_Shield, Longsword, Greatsword, Bow, Spear, Dagger]
