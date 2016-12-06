from Constants import *
from Actor import *
from Controls import *
from Items.Consumables import *
from Items.Weapons import *
from Items.Armors import *
from random import randrange as rand

class Enemy(Actor):
    def __init__(self, name, cLevel):
        self.char = ''
        self.color= COLOR_ENEMY
        self.name = name
        self.playerControlled = False
        self.dropChance = 40

        self.effects = []
        self.hitEffects = []
        self.visible = True
        self.canMove = True
        self.invertColor = False
        self.blocking = False
        self.countering=False
        self.stealthVal = 0
        self.sightDist = 9
        self.hearingDist = 5
        self.initiative = 3
        self.range = 1

        self.health = 2
        self.healthMax=2
        self.healthTemp=0
        self.items = []
        self.gold = rand(cLevel*4, cLevel*6+9)

        self.rightHand =None
        self.leftHand = None
        self.armor = None
        self.helmet= None
        self.rightRing =None
        self.leftRing = None
        self.necklace = None

        self.isAfraid = False
        self.cowardice = 0.0
        self.alliesList = []
        
        self.arrows = 0
        self.power = 1
        self.accuracy = 0
        self.armorPen = 0
        self.dodge = 0
        self.armorVal = 0

        self.level = cLevel
        self.exp = 0
        self.expNext=100
        while(self.level < cLevel):
            self.getExp(self.expNext)

        self.genEquipment()
        self.lastPlayerLoc = None
        self.lastPlayerMap = None

        self.pObject = None
        if hasattr(self, "onSpawn"):
            self.onSpawn()
            
        self.deriveStats()
        self.health = self.healthMax
        self.isAfraid = self.getAfraid()
    
    def onModHealth(self, difHP, Actor=None):
        if self.getAfraid() and self.isAfraid == False:
            self.isAfraid = True
            self.pObject.pLevel.messageSys.push(self.getName()+" is afraid!")
        return True

    def genEquipment(self):
        newItem = weaponList[rand(len(weaponList))]
        newItem = newItem(self.level)
        self.equip(newItem)
        if newItem.usesArrows:
            self.arrows += rand(3, 11)

        newItem = armorList[rand(len(armorList))]
        self.equip(newItem(self.level))

    def getAction(self):
        if self.health <= 0:
            return False
        
        if self.playerControlled:
            return self.userInput()
        else:
            return self.getAI()

    def getTarget(self):
        level = self.pObject.pLevel
        array = level.maze
        tiles = level.Tiles
        loc = [self.pObject.row, self.pObject.col]
        self.alliesList = []
        
        r = max(0, self.pObject.row-self.sightDist)
        r2= min(len(array), self.pObject.row+self.sightDist)
        c = max(0, self.pObject.col-self.sightDist)
        c2= min(len(array[0]), self.pObject.col+self.sightDist)
        target = None
        for row in range(r, r2):
            for col in range(c, c2):
                if len(tiles[row][col].Objects) > 0:
                    if level.canSee(loc, [row, col], self.sightDist):
                        tile = tiles[row][col]
                        if tile.isActor():
                            if not tile.getActor().isAlly(self):
                                if tile.getActor().Object.visible:
                                    target = tile.getActor()
                            elif tile.getActor().isAlly(self):
                                self.alliesList.append(tile.getActor())
                        if not tile.isActor():
                            if hasattr(self, "optionalTargets"):
                                for option in self.optionalTargets:
                                    if target == None:
                                        target = tile.getObjectOf(option)
                                    
        return target

    def getDjikMap(self, targTile):
        level = self.pObject.pLevel
        thisTile = [self.pObject.row, self.pObject.col]
        
        if self.isAfraid:
            return level.djikstra_Player_Away
        if targTile != self.lastPlayerLoc or self.lastPlayerLoc == None:
            self.lastPlayerLoc = targTile
            self.lastPlayerMap = level.formDjikstra([self.lastPlayerLoc], None, 0, False, self.sightDist)
            for ally in self.alliesList:
                ally.Object.inform(self.lastPlayerLoc, self.lastPlayerMap)
        return self.lastPlayerMap     

    def getAI(self):
        if self.health <= 0:
            return False

        level = self.pObject.pLevel
        thisTile = [self.pObject.row, self.pObject.col]
        target = self.getTarget()

        if hasattr(self, "onAI"):
            if self.onAI(target):
                return True

        djikMap = None
        if self.isAfraid:
            djikMap = level.djikstra_Player_Away
        else:
            if target != None:
                targTile = [target.row, target.col]
                if target.isActor():
                    if self.pObject.fight(level, targTile[0], targTile[1]):
                        return "AI_MOVE"
                djikMap = self.getDjikMap(targTile)
            if target == None:
                if self.lastPlayerLoc != None:
                    djikMap = self.getDjikMap(self.lastPlayerLoc)

        if djikMap == None:
            return False

        paths = level.followMap(djikMap, self.pObject.row, self.pObject.col)
        if len(paths) == 0:
            return False
        newLoc = paths[rand(len(paths))]
        if self.canMove:
            self.pObject.setpos(newLoc[0], newLoc[1])
        return "AI_MOVE"

    def inform(self, loc, djikMap):
        if self.lastPlayerLoc != loc:
            self.lastPlayerLoc = loc
            self.lastPlayerMap = djikMap
            for ally in self.alliesList:
                if ally.Object != None:
                    ally.Object.inform(loc, djikMap)

    def die(self, Actor=None):
        self.removeEquipment(self.dropChance)
        if rand(100) <= self.dropChance:
            newItems = consumableList
            newItem = newItems[rand(len(newItems))]
            self.items.append(newItem(self.level))

        if self.arrows > 0:
            self.items.append(Bundle_Of_Arrows(self.level, self.arrows))
            self.arrows = 0
        if self.gold > 0:
            self.items.append(Gold_Coins(self.level, self.gold))
            self.gold = 0
        
        for item in self.items:
            item.drop(self)
        if Actor != None:
            Actor.getExp(int(self.expNext/17))
            if hasattr(Actor, "prevTarget"):
                Actor.prevTarget == None
        self.pObject.remove()

    def removeEquipment(self, keepChance=100):
        slots = ["Helmet", "Armor", "Right Hand", "Left Hand", "Right Ring", "Left Ring", "Necklace"]
        for slot in slots:
            gotItem = self.unequip(slot)
            if rand(100) >= keepChance:
                if len(self.items) > 0 and gotItem != None:
                    self.items.pop(-1)

    def getExp(self, exp):
        self.exp+= exp
        if self.exp >= self.expNext:
            self.level+=1
            self.expNext = int(self.expNext*(1+pow(0.95, self.level)))
            self.exp = 0
            oldMax = self.healthMax
            self.deriveStats()
            self.modHealth(self.healthMax-oldMax)

    def deriveStats(self):
        self.armorVal = 0
        self.healthMax = 4 + self.level*int(self.level/3)
        self.health = min(self.health, self.healthMax)
        self.power = int(self.level*max(1, self.level/4))
        self.deriveRange()

    def deriveRange(self):       
        if self.rightHand == None:
            if self.leftHand == None:
                self.range = 1
            else:
                self.range = self.leftHand.range
        else:
            self.range = self.rightHand.range

    def getAfraid(self):
        return self.health <= (self.cowardice * self.healthMax)

    def isAlly(self, Actor):
        if hasattr(Actor, "playerControlled"):
            if self.playerControlled == Actor.playerControlled:
                return True
        if hasattr(Actor, "isPlayerControlled"):
            if self.playerControlled == Actor.isPlayerControlled():
                return True
        return False

    def getInfo(self):
        outString = ""

        if self.isAfraid:
            outString+= "is visibly afraid\n  "
        elif self.health < self.healthMax/2:
            outString+= "crouches, wounded\n  "
        if self.lastPlayerLoc == None:
            outString+= "is peering around aimlessly\n  "
        else:
            outString+= "has spotted you!\n  "

        if self.rightHand != None:
            outString+= "is carrying a "+self.rightHand.getName()+"\n  "

        armor = self.getArmor()
        if armor > 0 and armor <= 25:
            outString+= "is lightly armored\n  "
        elif armor > 25 and armor <= 50:
            outString+= "is wearing armor\n  "
        elif armor > 50 and armor <= 75:
            outString+= "is heavily armored\n  "
        elif armor > 75:
            outString+= "is extremely heavily armored\n  "
        return outString

    def getColor(self):
        if self.playerControlled:
            return COLOR_ALLY
        return self.color
