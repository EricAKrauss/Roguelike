from Constants import *
##import Features.Features

class Object:
    def __init__(self, name, R, C, level):
        self.Object = None
        self.name = name
        self.row = R
        self.col = C
        self.ID = -1
        self.pLevel = level

    def setObject(self, newObj):
        self.Object = newObj
        newObj.pObject = self
        if hasattr(newObj, "char"):
            if len(newObj.char) > 0:
                self.char = newObj.char

    def remove(self):
        tile = self.pLevel.Tiles[self.row][self.col]
        tile.pop(self.ID)
        self.pLevel.Objects.pop(self.ID, None)
        self.row = -1
        self.col = -1
        self.Object = None

    def move(self, dRow, dCol):
        newRow = self.row + dRow
        newCol = self.col + dCol
        return self.setpos(newRow, newCol)

    def setpos(self, R, C):
        if R < 0 or R >= len(self.pLevel.maze):
            return False
        if C < 0 or C >= len(self.pLevel.maze[R]):
            return False
        
        cTile = self.pLevel.Tiles[self.row][self.col]
        nTile = self.pLevel.Tiles[R][C]

        if nTile.isObstacle():
            if self.Object != None:
                self.pLevel.master_Changed_Tiles.append([R, C])
                return nTile.interact(self.Object)
            return False
        else:
            self.pLevel.master_Changed_Tiles.append([self.row, self.col])
            self.pLevel.master_Changed_Tiles.append([R, C])
            nTile.add(self.ID)
            cTile.pop(self.ID)
            moved = not (self.row == R and self.col == C)
            self.row = R
            self.col = C
            interacted = nTile.interact(self.Object)
            return moved or interacted
        return False

    def fight(obj, level, row, col):
        line = level.getLine([row, col], [obj.row, obj.col])
        if len(line) <= obj.Object.range+1:
            if level.Tiles[row][col].isActor():
                if level.Tiles[row][col].getActor().Object.visible:
                    weapons = obj.Object.getWeapons()
                    if len(weapons) > 0:
                        if len(line)-1 > 1:
                            if weapons[0].usesArrows:
                                if hasattr(obj.Object, "arrows"):
                                    if obj.Object.arrows <= 0:
                                        return False
                                    obj.Object.arrows -= 1
                                else:
                                    return False
                            else:
                                if obj.Object.canThrow() == None:
                                    if  level.distanceToMove(obj, row, col) > obj.Object.range:
                                        return False
                        
                    obj.Object.prevTarget = level.Tiles[row][col].getActor()
                    obj.Object.prevTarget.Object.getAttacked(obj.Object)
                    return True
        elif obj.Object.canThrow() != None:
            line = level.getLine([row, col], [obj.row, obj.col])
            if len(line)-1 <= max(4, obj.Object.power):
                if level.Tiles[row][col].isActor():
                    if obj.Object.throw(level.Tiles[row][col].getActor()):
                        return True
        return False

    def update(self):
        if self.Object == None:
            return False
        if not hasattr(self.Object, "update"):
            return False
        self.Object.update()

    def interact(self, Actor):
        if self.Object == None:
            return False
        return self.Object.interact(Actor)

    def getMoveCost(self):
        if self.Object == None:
            return 1
        if not hasattr(self.Object, "moveCost"):
            return 1
        else:
            return self.Object.moveCost

    def isActor(self):
        if self.Object == None:
            return False
        return self.Object.isActor()

    def isAlly(self, actor):
        if not self.isActor():
            return None
        return self.Object.isAlly(actor)
        

    def hasItem(self):
        if self.Object == None:
            return False

        item = False
        item = item or isinstance(self.Object, Item)
        item = item or (isinstance(self.Object, Features.Features.Chest and len(self.Object.allItems) > 0))
        return 

    def isAlive(self):
        if self.Object == None:
            return False
        if not hasattr(self.Object, "health"):
            return False
        return self.Object.health > 0

    def isObstacle(self):
        if self.Object == None:
            return False
        return self.Object.isObstacle()

    def isPlayerControlled(self):
        if self.Object == None:
            return False
        if not hasattr(self.Object, "playerControlled"):
            return False
        if not hasattr(self.Object, "health"):
            return False
        if self.Object.health <= 0:
            return False
        return self.Object.playerControlled

    def getAction(self):
        if self.Object == None:
            return False
        if not hasattr(self.Object, "getAction"):
            return False
        return self.Object.getAction()

    def getInitiative(self):
        if self.Object == None:
            return -1
        if not hasattr(self.Object, "getAction"):
            return -1
        return self.Object.getInitiative()

    def blocksSight(self):
        if self.Object == None:
            return False
        return self.Object.blocksSight()

    def getInfo(self):
        if self.Object == None:
            return ""
        return self.Object.getInfo()

    def getName(self):
        if self.Object == None:
            return ""
        return self.Object.getName()

    def getChar(self):
        if hasattr(self, "char"):
            return self.char
        
        if self.Object == None:
            return ''
        return self.Object.getChar()

    def getColor(self):
        if self.Object == None:
            return COLOR_DEFAULT
        return self.Object.getColor()
