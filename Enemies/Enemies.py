import Enemies.Goblins
import Enemies.Vermin
import Enemies.Undead

def genItemGoals(self):
    array = self.pObject.pLevel.maze
    tiles = self.pObject.pLevel.Tiles
    loc = [self.pObject.row, self.pObject.col]
    
    r = max(0, self.pObject.row-self.sightDist)
    r2= min(len(array), self.pObject.row+self.sightDist)
    c = max(0, self.pObject.col-self.sightDist)
    c2= min(len(array[0]), self.pObject.col+self.sightDist)
    goals = []

    for row in range(r, r2):
        for col in range(c, c2):
            if tiles[row][col].hasItem():
                if self.pObject.pLevel.canSee(loc, [row, col]):
                    goals.append([row, col])
    return goals

def genObjectGoals(self, objs):
    array = self.pObject.pLevel.maze
    tiles = self.pObject.pLevel.Tiles
    loc = [self.pObject.row, self.pObject.col]
    
    r = max(0, self.pObject.row-self.sightDist)
    r2= min(len(array), self.pObject.row+self.sightDist)
    c = max(0, self.pObject.col-self.sightDist)
    c2= min(len(array[0]), self.pObject.col+self.sightDist)
    goals = []

    for row in range(r, r2):
        for col in range(c, c2):
            if self.pObject.pLevel.canSee(loc, [row, col]):
                for obj in objs:
                    if isinstance(tiles[row][col], obj):
                        goals.append([row, col])
    return goals

enemyList = [*Enemies.Goblins.enemyList, *Enemies.Vermin.enemyList, *Enemies.Undead.enemyList]
eliteList = [*Enemies.Goblins.eliteList, *Enemies.Vermin.eliteList, *Enemies.Undead.eliteList]
