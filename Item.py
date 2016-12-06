from Object import *
from Constants import *

class Item:    
    def pop(self, actor):
        for i in range(len(actor.items)):
            if actor.items[i] == self:
                actor.items.pop(i)
                return True
        return False

    def interact(self, actor, msg=None):            
        if hasattr(self, "pObject") and self.pObject != None:
            row = self.pObject.row
            col = self.pObject.col
            level=self.pObject.pLevel
            ID = self.pObject.ID
            level.Tiles[row][col].pop(ID)
            self.pObject = None

        if msg == None:
            r = actor.pObject.row
            c = actor.pObject.col
            msg = actor.pObject.pLevel.SeesMap[r][c]    
        actor.items.append(self)
        messager = actor.pObject.pLevel.messageSys
        if hasattr(self, "onEquip"):
            self.onEquip(actor, msg)
        elif msg:
            messager.push(actor.getName()+" picked up "+self.getName())
        return True

    def drop(self, actor, msg=True):
        row = actor.pObject.row
        col = actor.pObject.col
        level=actor.pObject.pLevel
        
        newObject = Object(self.name, row, col, level)
        newObject.char = self.char
        newObject.setObject(self)
        self.pObject = newObject
        level.addNew(row, col, newObject)
        messager = actor.pObject.pLevel.messageSys
        if msg:
            messager.push(actor.getName()+" dropped "+self.getName())
        self.pop(actor)

    def blocksSight(self):
        return False

    def isAlly(self, Actor):
        if hasattr(Actor, "playerControlled"):
            if self.playerControlled == Actor.playerControlled:
                return True
        elif hasattr(Actor, "isPlayerControlled"):
            if self.playerControlled == Actor.isPlayerControlled:
                return True
        return False

    def isActor(self):
        return False

    def isObstacle(self):
        return False

    def getChar(self):
        return self.char

    def getColor(self):
        return self.color

    def getName(self):
        return self.name
