from Object import *
from Constants import *
from Abilities import *
from Item import Item
from random import randrange as rand
import Features.Features

class Bundle_Of_Arrows(Item):
    def __init__(self, count=0, extra=0):
        self.name = "Bundle of Arrows"
        self.color= COLOR_DEFAULT
        self.char = 'i'
        self.type = "consumable"
        self.arrowCount = (count+1)*2 + rand(4)
        if extra > 0:
            self.arrowCount = extra

        self.equippable = False
        self.consumable = True

    def getInfo(self):
        return "contains "+str(self.arrowCount)+" arrows\n"

    def use(self, actor, msg=False):
        if not hasattr(actor, "arrows"):
            actor.arrows = self.arrowCount
        else:
            actor.arrows+= self.arrowCount

        self.pop(actor)
        if msg:
            messager = actor.pObject.pLevel.messageSys
            messager.push(actor.getName()+" acquired "+str(self.arrowCount)+" Arrows")
        return True

    def onEquip(self, Actor, msg=False):
        self.use(Actor, msg)

class Gold_Coins(Item):
    def __init__(self, count=0, extra=0):
        self.name = "Gold Coins"
        self.color= COLOR_GOLD
        self.char = GOLD
        self.type = "consumable"
        self.coins = (count+1)*4 + rand(9)
        if extra > 0:
            self.coins = extra
            
        self.equippable = False
        self.consumable = True

    def getInfo(self):
        return "contains "+str(self.coins)+" coins\n"

    def use(self, actor, msg=False):
        if not hasattr(actor, "gold"):
            actor.gold = self.coins
        else:
            actor.gold += self.coins

        self.pop(actor)
        if msg:
            messager = actor.pObject.pLevel.messageSys
            messager.push(actor.getName()+" acquired "+str(self.coins)+" coins")
        return True

    def onEquip(self, Actor, msg=False):
        self.use(Actor, msg)

class Time_Bomb(Item):
    def __init__(self, lvl=1):
        self.name = "Bomb"
        self.color= COLOR_DEFAULT
        self.char = BOMB
        self.type = "consumable"
        self.equippable = False
        self.consumable = True

        self.level = lvl
        self.range = 0
        self.dur = 3
        self.radius = 2
        self.damage = max(1, int(lvl*lvl/4))
        self.desc = "Explodes up after 3 turns"

    def getInfo(self):
        return self.desc+"\n"

    def use(self, actor):
        level = actor.pObject.pLevel
        row = actor.pObject.row
        col = actor.pObject.col

        newObject = Object("Bomb", row, col, level)
        newObject.setObject(Features.Features.Bomb(self.dur, self.radius, self.damage))
        level.addNew(row, col, newObject)
        
        messager = actor.pObject.pLevel.messageSys
        messager.push(actor.getName()+" used a "+self.getName())
        return True

class GreenHerb(Item):
    def __init__(self, lvl=1):
        self.name = "Green Herb"
        self.color= COLOR_DEFAULT
        self.char = '+'
        self.type = "consumable"
        self.healNum = max(10, int(22.5+(lvl*5)*lvl/2))
        self.equippable = False
        self.consumable = True

    def getInfo(self):
        return "heals for "+str(self.healNum)+"\n"

    def use(self, actor):
        if actor.health == actor.healthMax:
            return False
        actor.modHealth(self.healNum)
        self.pop(actor)
        messager = actor.pObject.pLevel.messageSys
        messager.push(actor.getName()+" used a "+self.getName())
        return True

def scrollUse(self, actor):
    if not actor.equip(self):
        return False
    self.pop(actor)
    messager = actor.pObject.pLevel.messageSys
    messager.push(actor.getName()+" equipped "+self.getName())
    return True

class Scroll_of_Lightning_Bolt(Item):
    def __init__(self, lvl=1):
        self.name = "Scroll of Lightning Bolt"
        self.color= COLOR_DEFAULT
        self.char = 's'
        self.type = "scroll"
        self.level = lvl
        if self.level > 3:
            self.level = 3
        self.spell = Lightning_Bolt

        self.equippable = True
        self.consumable = False

    def getInfo(self):
        return "Use to cast a level "+str(self.level)+" Lightning Bolt\n"

    def cast(self, actor, row, col):
        return self.spell(actor, row, col, self.level, False)

    def use(self, actor):
        return scrollUse(self, actor)

class Scroll_of_Fireball(Item):
    def __init__(self, lvl=1):
        self.name = "Scroll of Fireball"
        self.color= COLOR_DEFAULT
        self.char = 's'
        self.type = "scroll"
        self.level = lvl
        self.spell = Fireball

        self.equippable = True
        self.consumable = False

    def getInfo(self):
        return "Use to cast a level "+str(self.level)+" Fireball\n"

    def cast(self, actor, row, col):
        return self.spell(actor, row, col, self.level, False)

    def use(self, actor):
        return scrollUse(self, actor)
        

consumableList = [GreenHerb, Bundle_Of_Arrows, Time_Bomb, Scroll_of_Fireball, Scroll_of_Lightning_Bolt]
healingList = [GreenHerb]
scrollList = [Scroll_of_Fireball, Scroll_of_Lightning_Bolt]
