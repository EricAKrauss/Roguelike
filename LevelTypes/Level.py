import QuadrantTheory
from Constants import *

from Object import *
from Items.Consumables import *
from Items.Weapons import *
from Items.Armors import *
from Enemies.Enemies import *
from Tile import *
from Enemy import *
from Features.Stairs import *
from Feature import *
from Features.Features import *
from QuadrantTheory import getAdjSpaces, gen2DArray, ArrayToString, isValid
from math import floor

class Level:
    def __init__(self, gameState, playerObj, challengeLevel, inSeed, args=None):
        self.args = args
        self.inSeed = inSeed
        self.name = "Default Dungeon"
        self.gameState = gameState
        self.itemList = [*consumableList, *weaponList, *armorList]
        self.equipList =[*weaponList, *armorList]
        self.consumeList=[*consumableList]
        self.healingList=[*healingList]
        self.enemyList = [*enemyList]
        self.eliteList = [*eliteList]
        self.textSpace = "Dusty stone floor\n"
        self.textWall =  "Grimy stone wall\n"
        self.maze = None
        if hasattr(self, "onInit"):
            self.onInit()

        if self.maze == None:
            if self.args == None:
                self.maze = QuadrantTheory.generateLevel(inSeed)
            else:
                self.maze = QuadrantTheory.generateLevel(inSeed, *self.args)
        self.thePlayer = playerObj
        self.master_Changed_Tiles = []

        self.stairsDown=[]
        self.stairsUp = []

        self.CollisionMap = QuadrantTheory.gen2DArray_var(len(self.maze), len(self.maze[0]), 0)
        self.SeenMap = QuadrantTheory.gen2DArray_var(len(self.maze), len(self.maze[0]), 0)
        self.SeesMap = QuadrantTheory.gen2DArray_var(len(self.maze), len(self.maze[0]), 0)
        self.tilesSeen= []

        self.cLevel = challengeLevel
        self.Objects = {}
        self.Tiles = {}

        self.formMaps()

        self.djikstra_Stairs_Up = self.formDjikstra( [(self.stairsUp[0], self.stairsUp[1])] )        
        if len(self.stairsDown) > 0:
            self.djikstra_Stairs_Down=self.formDjikstra( [(self.stairsDown[0], self.stairsDown[1])] )        
        self.djikstra_Player = self.formDjikstra( [(self.thePlayer.pObject.row, self.thePlayer.pObject.col)] )
        self.djikstra_Player_Adj = self.formDjikstra( getAdjSpaces(self.maze, self.thePlayer.pObject.row, self.thePlayer.pObject.col) )
        self.djikstra_Player_Away = self.transformMap(self.djikstra_Player, -1.2)

    def formMaps(self):
        for row in range(len(self.maze)):
            for col in range(len(self.maze[row])):
                if row not in self.Tiles.keys():
                    self.Tiles[row] = {}
                self.Tiles[row][col] = Tile(self, row, col)
                if self.maze[row][col] == WALL or self.maze[row][col] == TREE:
                    self.CollisionMap[row][col] = 1
                else:
                    self.CollisionMap[row][col] = 0
                    if self.maze[row][col] != SPACE:
                        self.generateContent(row, col)

    def getPlayerViewArea(self, multiplier, obj=None):
        if obj == None:
            obj = self.thePlayer
            
        radius = floor(obj.sightDist*multiplier)
        row = obj.pObject.row
        col = obj.pObject.col

        r1 = max(0, row-radius)
        c1 = max(0, col-radius)

        r2 = min(row+radius+1, len(self.maze)-1)
        c2 = min(col+radius+1, len(self.maze[0])-1)

        return (r1, c1, r2, c2)

    def getViewArea(self, obj=None):
        if obj == None:
            obj = self.thePlayer
            
        radius = floor(obj.sightDist)
        row = obj.pObject.row
        col = obj.pObject.col

        r1 = max(0, row-radius)
        c1 = max(0, col-radius)

        r2 = min(row+radius+1, len(self.maze)-1)
        c2 = min(col+radius+1, len(self.maze[0])-1)

        return (r1, c1, r2, c2)

    def updateSight(self, radius, obj=None):
        self.SeesMap = QuadrantTheory.gen2DArray(len(self.maze), 0)
        for an_obj in self.Objects.values():
            obj = an_obj
            if an_obj.isPlayerControlled():
                if obj.Object.health > 0:
                    radius=obj.Object.sightDist
                    accuracyDist = floor(radius*1.5)
                    
                    row = obj.row
                    col = obj.col

                    cL = col-accuracyDist
                    cR = col+accuracyDist
                    for r in range(row-accuracyDist, row+accuracyDist+1):
                        self.sightLine([row, col], [r, cL], radius)
                        self.sightLine([row, col], [r, cR], radius)

                    rU = row-accuracyDist
                    rD = row+accuracyDist
                    for c in range(col-accuracyDist, col+accuracyDist+1):
                        self.sightLine([row, col], [rU, c], radius)
                        self.sightLine([row, col], [rD, c], radius)
                        
            

    def sightLine(self, start, end, radius):
        line = self.getLine(start, end)
        self.SeenMap[start[0]][start[1]] = 1
        self.SeesMap[start[0]][start[1]] = 1
            
        for tile in line[1:radius+1]:
            if not isValid(self.maze, tile[0], tile[1]):
                return
            self.SeenMap[tile[0]][tile[1]] = 1
            self.SeesMap[tile[0]][tile[1]] = 1
            self.master_Changed_Tiles.append([tile[0], tile[1]])
            if self.Tiles[tile[0]][tile[1]].blocksSight():
                return

    def canSee(self, start, end, sightDist):
        line = self.getLine(start, end)

        if len(line) > sightDist:
            return False

        ##print(line, end)
        for tile in line:
            if tile[0] == end[0] and tile[1] == end[1]:
                return True
            if self.Tiles[tile[0]][tile[1]].blocksSight():
                return False
        return False

    def distanceToMove(self, obj, row, col):
        djikMap = self.formDjikstra([[row, col]])
        return djikMap[obj.row][obj.col]

    def getLine(self, start, end):
        """Bresenham's Line Algorithm
        Produces a list of tuples from start and end
        """
        # Setup initial conditions
        x1, y1 = start
        x2, y2 = end
        dx = x2 - x1
        dy = y2 - y1
        # Determine how steep the line is
        is_steep = abs(dy) > abs(dx)
        # Rotate line
        if is_steep:
            x1, y1 = y1, x1
            x2, y2 = y2, x2
        # Swap start and end points if necessary and store swap state
        swapped = False
        if x1 > x2:
            x1, x2 = x2, x1
            y1, y2 = y2, y1
            swapped = True
        # Recalculate differentials
        dx = x2 - x1
        dy = y2 - y1
        # Calculate error
        error = int(dx / 2.0)
        ystep = 1 if y1 < y2 else -1
        # Iterate over bounding box generating points between start and end
        y = y1
        points = []
        for x in range(x1, x2 + 1):
            coord = (y, x) if is_steep else (x, y)
            points.append(coord)
            error -= abs(dy)
            if error < 0:
                y += ystep
                error += dx
        # Reverse the list if the coordinates were swapped
        if swapped:
            points.reverse()
        return points

    def formDjikstra(self, goals, inArray=None, offset=0, diag=False, limit=None):
        if inArray == None:
            outArray = gen2DArray(len(self.maze), None)
        else:
            outArray = inArray
            
        for spot in goals:
            outArray[spot[0]][spot[1]] = offset
            outArray = self.formDjikstraHelper(outArray, [spot], diag)

        return outArray

    def formDjikstraHelper(self, array, changes, diag=False, limit=None):
        if len(changes) == 0:
            return array
        
        actualChanges =[]
        adjToChanges = []
        for loc in changes:
            adjToChanges = []
            for newLoc in getAdjSpaces(array, loc[0], loc[1], None, diag):
                if not self.CollisionMap[newLoc[0]][newLoc[1]]:
                    adjToChanges.append(newLoc)
                
            for spot in adjToChanges:
                adjToSpot = getAdjSpaces(array, spot[0], spot[1], None, diag)
                values = []
                for adjSpot in adjToSpot:
                    if array[adjSpot[0]][adjSpot[1]] != None:
                        if not self.CollisionMap[adjSpot[0]][adjSpot[1]]:
                            values.append(array[adjSpot[0]][adjSpot[1]])

                if len(values) > 0:
                    cost = self.Tiles[spot[0]][spot[1]].getMoveCost()
                    if (array[spot[0]][spot[1]] == None) or (min(values)+cost < array[spot[0]][spot[1]]):
                        array[spot[0]][spot[1]] = min(values)+cost
                        if limit == None or array[spot[0]][spot[1]] < limit:
                            actualChanges.append((spot[0], spot[1]))

        return self.formDjikstraHelper(array, actualChanges)

    def transformMap(self, djikMap, mult, startPoint=None):
        lowestPoints = []
        lowestPoint = 100
        for row in range(len(djikMap)):
            for col in range(len(djikMap[row])):
                if djikMap[row][col] != None:
                    djikMap[row][col] = djikMap[row][col]*mult
                    if djikMap[row][col] < lowestPoint:
                        lowestPoint = djikMap[row][col]
                        lowestPoints = []
                    if djikMap[row][col] <= lowestPoint+1:
                        lowestPoints.append([row, col])
                    
        self.formDjikstra(lowestPoints, djikMap)
        return djikMap

    def testDjikstra(self, array):
        outString = ""
        for row in array:
            for col in row:
                if col == None:
                    outString += '#'
                else:
                    outString += str(col)[-1]
            outString+="\n"
        return outString

    def followMap(self, array, row, col):
        outSpots = []
        adjToSpot = getAdjSpaces(array, row, col)
        for spot in adjToSpot:
            if array[spot[0]][spot[1]] == 0:
                return [spot]
            if array[spot[0]][spot[1]] != None:
                if not self.Tiles[spot[0]][spot[1]].isObstacle():
                    if array[row][col] > array[spot[0]][spot[1]]:
                        outSpots.append(spot)

        if len(outSpots) == 0:
            cursoryAdj = []
            for spot in adjToSpot:
                if array[spot[0]][spot[1]] != None:
                    if not self.Tiles[spot[0]][spot[1]].isObstacle():
                        cursoryAdj = getAdjSpaces(array, spot[0], spot[1])
                        for subSpot in cursoryAdj:
                            if array[subSpot[0]][subSpot[1]] != None:
                                if array[row][col] >= array[subSpot[0]][subSpot[1]]:
                                    outSpots.append(spot)

        if len(outSpots) == 0:
            return []
        
        minVal = array[outSpots[0][0]][outSpots[0][1]]
        for i in range(len(outSpots)):
            tile = outSpots[i]
            if array[tile[0]][tile[1]] < minVal:
                minVal = array[tile[0]][tile[1]]

        reallyOutSpots = []
        for i in range(len(outSpots)):
            tile = outSpots[i]
            if array[tile[0]][tile[1]] == minVal:
                reallyOutSpots.append(tile)
                

        return reallyOutSpots
            

    def generateContent(self, row, col):
        char = self.maze[row][col]
        newThing = None
##        if char == DOOR:
##            newThing = Object("Door", row, col, self)
##            newThing.char = char
        if char == DECORATION:
            newThing = Object("Decoration", row, col, self)
            newThing.char = char
        if char == STAIRS[0]:
            self.stairsUp = [row, col]
            newThing = Object("Stairs Up", row, col, self)
            newThing.setObject(StairUp("Stairs Up", row, col, self))
            newThing.char = char
            self.addNew(row, col, newThing)
            
            newThing = Object("Player", row, col, self)
            self.pObject = newThing
            newThing.setObject(self.thePlayer)
        if char == STAIRS[1]:
            self.stairsDown = [row, col]
            newThing = Object("Stairs Down", row, col, self)
            newThing.setObject(StairDown("Stairs Down", row, col, self))
            newThing.char = char

        if char == BRUSH:
            newThing = Object("Brush", row, col, self)
            newThing.char = char
            newThing.setObject(Brush())
        if char == HEALTH:
            newThing = Object("Health", row, col, self)
            newThing.char = char
            newItem = self.healingList[rand(len(self.healingList))]
            newThing.setObject(newItem(self.cLevel))
        if char == DECORATION:
            newItem = self.decorList[rand(len(self.decorList))]()
            newThing = Object(newItem.name, row, col, self)
            newThing.setObject(newItem)
        if char == ITEM:
            newThing = Object("Item", row, col, self)
            newThing.char = char
            newItem = self.equipList[rand(len(self.equipList))]
            newThing.setObject(newItem(self.cLevel))
        if char == GOLD:
            newThing = Object("Gold", row, col, self)
            newThing.char = char
            newThing.setObject(Gold())
        if char == CHEST:
            newThing = Object("Chest", row, col, self)
            newThing.char = char
            newThing.setObject(Chest(self.cLevel))

        if char == ENEMY:
            newThing = Object("Enemy", row, col, self)
            newThing.char = char
            newEnemy = self.enemyList[rand(len(self.enemyList))]
            newThing.setObject(newEnemy("Enemy", self.cLevel))
            newThing.Object.char = char
        if char == ENEMY_ELITE:
            newThing = Object("Enemy", row, col, self)
            newThing.char = char
            newEnemy = self.eliteList[rand(len(self.eliteList))]
            newThing.setObject(newEnemy("Enemy", self.cLevel))
            newThing.Object.char = char

        if newThing != None:
            self.addNew(row, col, newThing)

    def createNew(self, row, col, newPayload):
        name = newPayload.name
        newObject = Object(name, row, col, self)
        newObject.char = newPayload.char
        newObject.setObject(newPayload)
        self.addNew(row, col, newObject)

    def addNew(self, row, col, newThing):
        if row not in self.Tiles.keys():
            self.Tiles[row] = {}
        if col not in self.Tiles[row].keys():
            self.Tiles[row][col] = Tile(self, row, col)

        global IDCounter
        ID = IDCounter
        IDCounter += 1
        newThing.ID = ID
        self.Objects[ID] = newThing
        self.Tiles[row][col].add(ID)
