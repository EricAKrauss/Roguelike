from Constants import *
from QuadrantTheory import isValid

class Tile:
    def __init__(self, level, R, C):
        self.Objects = []
        self.row = R
        self.col = C
        self.pLevel = level

    def __iter__(self):
        return self.Objects

    def pop(self, ID):
        for i in range(len(self.Objects)):
            obj_ID = self.Objects[i]
            if obj_ID == ID:
                return self.Objects.pop(i)
        return None

    def add(self, ID):
        return self.Objects.append(ID)
                

    def interact(self, Actor):
        success = False
        for obj_ID in self.Objects:
            an_object = self.pLevel.Objects[obj_ID]
            success = success or an_object.interact(Actor)
        return success
        
    def hasItem(self):
        for obj_ID in self.Objects:
            an_obj = self.pLevel.Objects[obj_ID]
            if an_obj.isItem():
                return True
        return False

    def isActor(self):
        for obj_ID in self.Objects:
            an_obj = self.pLevel.Objects[obj_ID]
            if an_obj.isActor():
                return True
        return False

    def getActor(self):
        for obj_ID in self.Objects:
            an_obj = self.pLevel.Objects[obj_ID]
            if an_obj.isActor():
                return an_obj
        return None

    def hasObjectOf(self, objType):
        return self.getObjectOf(objType) == True

    def getObjectOf(self, objType):
        for obj_ID in self.Objects:
            an_obj = self.pLevel.Objects[obj_ID]
            if an_obj.Object != None:
                if isinstance(an_obj.Object, objType):
                    return an_obj
        return None

    def getMoveCost(self):
        cost = 1
        for obj_ID in self.Objects:
            an_obj = self.pLevel.Objects[obj_ID]
            cost = max(cost, an_obj.getMoveCost())
            
        return cost

    def isObstacle(self):
        if self.pLevel.CollisionMap[self.row][self.col]:
            return True
        if len(self.Objects) == 0:
            return False

        obstacle = False
        for obj_ID in self.Objects:
            an_object = self.pLevel.Objects[obj_ID]
            obstacle = obstacle or an_object.isObstacle()
        return obstacle

    def blocksSight(self):
        if self.pLevel.CollisionMap[self.row][self.col] == 1:
            return True
        elif len(self.Objects) == 0:
            return False

        obstacle = False
        for obj_ID in self.Objects:
            an_object = self.pLevel.Objects[obj_ID]
            obstacle = obstacle or an_object.blocksSight()
        return obstacle

    def getInfo(self):
        if len(self.Objects) == 0:
            char = self.getCharBase()
            if char == SPACE:
                return self.pLevel.textSpace
            if char == WALL:
                return self.pLevel.textWall
        else:
            string = ""
            for obj_ID in self.Objects:
                obj = self.pLevel.Objects[obj_ID]
                string += obj.getName()+"\n"
                string += "  "+obj.getInfo()
            return string

    def getCharBase(self, fog=False):
        if not fog:
            char = SPACE
            if self.pLevel.CollisionMap[self.row][self.col]:
                char = WALL
        else:
            if self.pLevel.SeenMap[self.row][self.col] == 1:
                char = SPACE
                if self.pLevel.CollisionMap[self.row][self.col]:
                    char = self.pLevel.maze[self.row][self.col]
            else:
                char = UNKNOWN
        return char

    def getChar(self, fog=False):        
        char = self.getCharBase(fog)
            
        if len(self.Objects) == 0:
            return char

        for obj_ID in self.Objects:
            an_object = self.pLevel.Objects[obj_ID]
            newChar = ''
            if fog:
                if an_object.isActor():
                    if self.pLevel.SeesMap[self.row][self.col] == 1:
                        return an_object.getChar()
                    else:
                        newChar = self.getCharBase(fog)
                else:
                    if self.pLevel.SeenMap[self.row][self.col] == 1:
                        newChar = an_object.getChar()
                    else:
                        newChar = self.getCharBase(fog)
            if not fog:
                newChar = an_object.getChar()
                if an_object.isActor():
                    return newChar

            if newChar != self.getCharBase(fog):
                char = newChar
        return char

    def getInvertColor(self):
        for obj_ID in self.Objects:
            an_object = self.pLevel.Objects[obj_ID]
            if an_object.Object != None:
                if hasattr(an_object.Object, "invertColor") and an_object.Object.invertColor:
                    return True
        return False

    def getColorBase(self, fog=False):
        color = COLOR_DEFAULT
        if self.row >= len(self.pLevel.SeesMap): return color
        if self.col >= len(self.pLevel.SeesMap[0]): return color
        
        if fog:
            if self.pLevel.SeesMap[self.row][self.col] == 1:
                if self.pLevel.CollisionMap[self.row][self.col] == 1:
                    if self.pLevel.maze[self.row][self.col] == WALL:
                        color = COLOR_WALL
                    if self.pLevel.maze[self.row][self.col] == TREE:
                        color = COLOR_TREE
                else:
                    color = COLOR_DEFAULT
            else:
                color = COLOR_FOW
        return color

    def getColor(self, fog=False):        
        color = self.getColorBase(fog)
            
        if len(self.Objects) == 0:
            return color

        for obj_ID in self.Objects:
            an_object = self.pLevel.Objects[obj_ID]
            if an_object.getColor() != COLOR_DEFAULT:
                if fog:
                    if isValid(self.pLevel.SeesMap, self.row, self.col) and self.pLevel.SeesMap[self.row][self.col] == 1:
                        color= an_object.getColor()
                        if an_object.isActor():
                            return color
                    else:
                        color= self.getColorBase(fog)
                if not fog:
                    color= an_object.getColor()
                    if an_object.isActor():
                        return color
        return color

    def getName(self):
        if len(self.Objects) == 0:
            return "Empty Tile"

        name = ""
        for obj_ID in self.Objects:
            an_object = self.pLevel.Objects[obj_ID]
            name += an_object.getName() + " "
        name = name[:-1]
        if len(name) > 1:
            return name
        else:
            return "Empty Tile"
