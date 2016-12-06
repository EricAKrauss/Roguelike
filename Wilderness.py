from random import randrange as rand
from random import shuffle, seed
from QuadrantTheory import *
from Constants import *

class Wilderness:
    def __init__(self, inSeed, width, height, bkgType):
        if inSeed == None:
            inSeed = rand(255400)
        seed(inSeed)
        
        self.width = width
        self.height= height
        self.bkgType = bkgType

        self.bkgTypes =    [TREE, '.']
        self.borderTypes = ['.', '~']
        self.featureTypes= ['C', 'B']
        self.featList = []
        self.regionSize = 8
        self.regionGrid = gen2DArray_var(height, width, bkgType)
        self.maze = gen2DArray_var(height*self.regionSize, width*self.regionSize, SPACE)

        self.features = 0
        while self.features < 6:
            self.defRegions()
        self.regToMaze()
        self.fillFeatures()
        self.maze = self.package(self.maze)
        self.placeEntrance()
        self.maze = self.package(self.maze, 1, TREE)

    def package(self, array, buffer=1, default=SPACE):
        newArray = gen2DArray_var(len(array)+buffer*2, len(array[0])+buffer*2, default)
        for row in range(len(array)):
            for col in range(len(array[0])):
                newArray[row+buffer][col+buffer] = array[row][col]
        return newArray

    def placeEntrance(self):
        rMax = len(self.maze)-2
        cMax = len(self.maze[0])-2
        rHalf = int(len(self.maze)/2)
        cHalf = int(len(self.maze[0])/2)
        locs = [ [1, cHalf], [rHalf, 1],
                 [rMax, cHalf], [rHalf, cMax]]
        shuffle(locs)
        self.maze[locs[0][0]][locs[0][1]] = STAIRS[0]
        self.maze[locs[1][0]][locs[1][1]] = STAIRS[1]
        

    def defRegions(self):
        r = rand(self.height)
        c = rand(self.width)

        newType = self.bkgType
        while newType == self.bkgType:
            newType = self.featureTypes[rand(len(self.featureTypes))]
                
        if self.regionGrid[r][c] == self.bkgType:
            self.regionGrid[r][c] = newType
            self.features += 1
            self.featList.append([])
            self.featList[-1].append((r, c))
            for spot in getAdjSpaces(self.regionGrid, r, c, self.bkgType):
                row = spot[0]
                col = spot[1]
                self.expRegion(row, col, newType)

    def fillFeatures(self):
        for feature in self.featList:
            i = rand(len(feature))
            r = feature[i][0]
            c = feature[i][1]

            if self.regionGrid[r][c] not in self.featureTypes:
                continue
            
            rows = list(range(r*self.regionSize))
            cols = list(range(c*self.regionSize))
            doorPlaced = not (self.regionGrid[r][c] == 'B')
            shuffle(feature)
            for reg in range(len(feature)):
                if not doorPlaced:
                    doorPlaced = self.placeDoor(feature[reg][0], feature[reg][1])
                self.fillEnemies(feature[reg][0], feature[reg][1])

    def fillEnemies(self, row, col):
        enemies =0
        eneMax = 2
        row = row*self.regionSize
        col = col*self.regionSize
        rMax= row+self.regionSize-1
        cMax= col+self.regionSize-1
        row = row+1
        col = col+1
        itemPlaced = False
        elitePlaced= False
        if rand(100) > 33:
            elitePlaced = True
        
        while enemies < eneMax:
            if itemPlaced == True:
                if not elitePlaced:
                    elitePlaced = True
                    val = ENEMY_ELITE
                else:
                    val = ENEMY
                enemies += 1
                    
            if itemPlaced == False:
                index = rand(10)
                itemPlaced = True
                if index < 3:
                    val = CHEST
                elif index < 7:
                    val = HEALTH
                else:
                    val = ITEM
        
            r = rand(row, rMax)
            c = rand(col, cMax)
            if self.maze[r][c] == SPACE:
                self.maze[r][c] = val
            

    def expRegion(self, row, col, typ):
        if rand(100) > 25:
            newType = self.borderTypes[rand(len(self.borderTypes))]
            self.regionGrid[row][col] = newType
            return
        else:
            self.featList[-1].append((row, col))
            newType = typ
            self.regionGrid[row][col] = newType
            for spot in getAdjSpaces(self.regionGrid, row, col, self.bkgType):
                r = spot[0]
                c = spot[1]
                self.expRegion(r, c, newType)

    def regToMaze(self):
        for row in range(len(self.regionGrid)):
            for col in range(len(self.regionGrid[row])):
                spotAbove =False
                spotBelow =False
                spotLeft = False
                spotRight =False
                inType = self.regionGrid[row][col]
                adjSpots = getAdjSpaces(self.regionGrid, row, col, inType)
                if (row-1, col) in adjSpots: spotAbove=True
                if (row+1, col) in adjSpots: spotBelow=True
                if (row, col-1) in adjSpots: spotLeft =True
                if (row, col+1) in adjSpots: spotRight=True
                self.fillRegion(row, col, inType, spotAbove, spotBelow, spotLeft, spotRight)

    def fillRegion(self, row, col, inType, spotAbove, spotBelow, spotLeft, spotRight):
        if inType == TREE:
            self.buildForest(row, col, spotAbove, spotBelow, spotLeft, spotRight)
        if inType == 'B':
            self.buildBuilding(row, col, spotAbove, spotBelow, spotLeft, spotRight)
        if inType == WATER:
            self.buildWater(row, col, spotAbove, spotBelow, spotLeft, spotRight)

    def placeDoor(self, r, c):
        row = r*self.regionSize
        col = c*self.regionSize
        rEnd= row+self.regionSize-1
        cEnd= col+self.regionSize-1
        locs = [[row+int((rEnd-row)/2), col],
                [row+int((rEnd-row)/2), cEnd],
                [row, col+int((cEnd-col)/2)],
                [rEnd, col+int((cEnd-col)/2)]]

        while len(locs) > 0:
            loc = locs.pop(0)
            if self.maze[loc[0]][loc[1]] == WALL:
                self.maze[loc[0]][loc[1]] = DOOR
                return True
        return False
        

    def buildForest(self, row, col, spotAbove, spotBelow, spotLeft, spotRight):
        rStart = row*self.regionSize
        cStart = col*self.regionSize
        for i in range(self.regionSize):
            r = rand(rStart, rStart+self.regionSize)
            c = rand(cStart, cStart+self.regionSize)
            self.maze[r][c] = TREE

    def buildWater(self, row, col, spotAbove, spotBelow, spotLeft, spotRight):
        rStart = row*self.regionSize
        cStart = col*self.regionSize
        for r in range(rStart+2, rStart+self.regionSize-2):
            for c in range(cStart+2, cStart+self.regionSize-2):
                self.maze[r][c] = WATER

    def buildBuilding(self, row, col, spotAbove, spotBelow, spotLeft, spotRight):
        rStart = row*self.regionSize
        cStart = col*self.regionSize
        for r in range(rStart, rStart+self.regionSize):
            for c in range(cStart, cStart+self.regionSize):
                if r == rStart and (not spotAbove or c == cStart):
                    self.maze[r][c] = WALL
                if c == cStart and (not spotLeft or r == cStart):
                    self.maze[r][c] = WALL
                if r == rStart+self.regionSize-1 and (not spotBelow or c == cStart+self.regionSize-1):
                    self.maze[r][c] = WALL
                if c == cStart+self.regionSize-1 and (not spotRight or r == rStart+self.regionSize-1):
                    self.maze[r][c] = WALL
                if c == cStart and r == rStart+self.regionSize-1:
                    self.maze[r][c] = WALL
                if r == rStart and c == cStart+self.regionSize-1:
                    self.maze[r][c] = WALL


if __name__ == "__main__":
    wild = Wilderness(None, 6, 6, TREE)
    print(ArrayToString(wild.regionGrid))
    print(ArrayToString(wild.maze))
