from Object import *
from Constants import *
from Item import Item
from math import floor, ceil

def armorGetInfo(self):
    outString = "level "+str(self.level)+": "
    outString+= str(self.armorVal)+" armor, "
    outString+= str(self.weight)+" weight"
    if self.throwable:
        outString+= ", can be thrown"
    return outString+'\n'

def armorUse(self, actor):
    if not actor.equip(self):
        return False
    self.pop(actor)
    messager = actor.pObject.pLevel.messageSys
    messager.push(actor.getName()+" equipped "+self.getName())
    return True

class Cloth_Shirt(Item):
    def __init__(self, lvl=1):
        self.level = lvl
        
        self.color= COLOR_DEFAULT
        self.char = '?'
        self.type = "armor"
        self.name = "Cloth Shirt"

        self.equippable = True
        self.consumable = False
        self.throwable = False

        self.armorVal = 7 + floor(int(5*lvl))
        self.weight= 5
        
        if lvl > 1:
            self.name = "+"+str(lvl-1)+" "+self.name

    def getInfo(self):
        return armorGetInfo(self)

    def use(self, actor):
        return armorUse(self, actor)


class Cloth_Hat(Item):
    def __init__(self, lvl=1):
        self.level = lvl
        
        self.color= COLOR_DEFAULT
        self.char = '?'
        self.type = "helmet"
        self.name = "Cloth Hat"

        self.equippable = True
        self.consumable = False
        self.throwable = False

        self.armorVal = 2 + floor(int(5*lvl))
        self.weight= 1
        
        if lvl > 1:
            self.name = "+"+str(lvl-1)+" "+self.name

    def getInfo(self):
        return armorGetInfo(self)

    def use(self, actor):
        return armorUse(self, actor)

class Leather_Shirt(Item):
    def __init__(self, lvl=1):
        self.level = lvl
        
        self.color= COLOR_DEFAULT
        self.char = '?'
        self.type = "armor"
        self.name = "Leather Shirt"

        self.equippable = True
        self.consumable = False
        self.throwable = False

        self.armorVal = 20 + floor(int(5*lvl))
        self.weight= 20
        
        if lvl > 1:
            self.name = "+"+str(lvl-1)+" "+self.name

    def getInfo(self):
        return armorGetInfo(self)

    def use(self, actor):
        return armorUse(self, actor)


class Leather_Helm(Item):
    def __init__(self, lvl=1):
        self.level = lvl
        
        self.color= COLOR_DEFAULT
        self.char = '?'
        self.type = "helmet"
        self.name = "Leather Helm"

        self.equippable = True
        self.consumable = False
        self.throwable = False

        self.armorVal = 5 + floor(int(5*lvl))
        self.weight= 5
        
        if lvl > 1:
            self.name = "+"+str(lvl-1)+" "+self.name

    def getInfo(self):
        return armorGetInfo(self)

    def use(self, actor):
        return armorUse(self, actor)

class Chain_Shirt(Item):
    def __init__(self, lvl=1):
        self.level = lvl
        
        self.color= COLOR_DEFAULT
        self.char = '?'
        self.type = "armor"
        self.name = "Chain Shirt"

        self.equippable = True
        self.consumable = False
        self.throwable = False

        self.armorVal = 30 + floor(int(5*lvl))
        self.weight= 35
        
        if lvl > 1:
            self.name = "+"+str(lvl-1)+" "+self.name

    def getInfo(self):
        return armorGetInfo(self)

    def use(self, actor):
        return armorUse(self, actor)


class Chain_Helm(Item):
    def __init__(self, lvl=1):
        self.level = lvl
        
        self.color= COLOR_DEFAULT
        self.char = '?'
        self.type = "helmet"
        self.name = "Chain Helm"

        self.equippable = True
        self.consumable = False
        self.throwable = False

        self.armorVal = 7 + floor(int(5*lvl))
        self.weight= 10
        
        if lvl > 1:
            self.name = "+"+str(lvl-1)+" "+self.name

    def getInfo(self):
        return armorGetInfo(self)

    def use(self, actor):
        return armorUse(self, actor)

class Iron_Breastplate(Item):
    def __init__(self, lvl=1):
        self.level = lvl
        
        self.color= COLOR_DEFAULT
        self.char = '?'
        self.type = "armor"
        self.name = "Iron Breastplate"

        self.equippable = True
        self.consumable = False
        self.throwable = False

        self.armorVal = 45 + floor(int(5*lvl))
        self.weight= 55
        
        if lvl > 1:
            self.name = "+"+str(lvl-1)+" "+self.name

    def getInfo(self):
        return armorGetInfo(self)

    def use(self, actor):
        return armorUse(self, actor)


class Iron_Helm(Item):
    def __init__(self, lvl=1):
        self.level = lvl
        
        self.color= COLOR_DEFAULT
        self.char = '?'
        self.type = "helmet"
        self.name = "Iron Helm"

        self.equippable = True
        self.consumable = False
        self.throwable = False

        self.armorVal = 12 + floor(int(5*lvl))
        self.weight= 15
        
        if lvl > 1:
            self.name = "+"+str(lvl-1)+" "+self.name

    def getInfo(self):
        return armorGetInfo(self)

    def use(self, actor):
        return armorUse(self, actor)

armorList = [Cloth_Shirt, Cloth_Hat, Leather_Shirt, Leather_Helm, Iron_Breastplate, Iron_Helm, Chain_Shirt, Chain_Helm]
