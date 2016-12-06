from random import randrange as rand
from random import shuffle
from QuadrantTheory import getAdjSpaces
from copy import deepcopy
from Constants import *
from Feature import *

##from Enemies.Vermin import *
from Items.Weapons import *
from Items.Armors import *
import Items.Consumables

class Brush(Feature):
    def __init__(self):
        self.char = BRUSH
        self.name = "Brush"
        self.color= COLOR_BRUSH

    def blocksSight(self):
        return True

class Smoke(Feature):
    def __init__(self, duration=1):
        self.char = SMOKE
        self.name = "Smoke"
        self.color= COLOR_SMOKE
        self.duration= duration

    def update(self):
        if self.duration <= 0:
            self.pObject.remove()
            return False
        self.duration-=1
        return True

    def blocksSight(self):
        return True

class TempWall(Feature):
    def __init__(self, duration=1):
        self.char = WALL
        self.name = "Smoke"
        self.color= COLOR_GHOST
        self.duration= duration

    def update(self):
        if self.duration <= 0:
            self.pObject.remove()
            return False
        self.duration-=1
        return True

    def isObstacle(self):
        return True

class Bomb(Feature):
    def __init__(self, duration=3, radius=1, damage=1):
        self.char = BOMB
        self.name = "Bomb"
        self.color= COLOR_HAZARD
        self.duration= duration
        self.damage = damage
        self.radius = radius

    def update(self):
        if self.duration < 3:
            self.char = str(self.duration)
        if self.duration <= 0:
            self.explode()
            self.pObject.remove()
            return False
        self.duration-=1
        return True

    def explode(self):
        level = self.pObject.pLevel
        row = self.pObject.row
        col = self.pObject.col
        spots = [[row, col]]
        outSpots = [[row, col]]
        for i in range(self.radius):
            for spot in spots:
                outSpots += getAdjSpaces(level.maze, spot[0], spot[1])
            spots = deepcopy(outSpots)

        idsHit = []
        for loc in outSpots:
            r = loc[0]
            c = loc[1]
            level.CollisionMap[r][c] = 0
            tile = level.Tiles[r][c]
            target = tile.getActor()
            if target != None and target.ID not in idsHit:
                idsHit.append(target.ID)
                target.Object.takeDamage(self.damage)
            

class Chest(Feature):
    def __init__(self, cLevel):
        self.char = CHEST
        self.name = "Chest"
        self.color= COLOR_CHEST
        self.items = []

        allItems = [*weaponList, *Items.Consumables.consumableList, *armorList]
        for i in range(3):
            val = rand(100)
            if val <= 33: allItems = weaponList
            elif val <= 66: allItems = armorList
            elif val <= 99: allItems = Items.Consumables.consumableList
            self.items.append(allItems[rand(len(allItems))](cLevel))
        self.items.append(Items.Consumables.Gold_Coins(cLevel))

    def isObstacle(self):
        return True

    def interact(self, Actor):
        if len(self.items) == 0:
            return False
        
        while(len(self.items) > 0):
            item = self.items.pop(0)
            item.interact(Actor)
        self.color = COLOR_DEFAULT
        return True
