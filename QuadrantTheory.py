from random import randrange as rand
from random import randint
from random import shuffle, seed
from math import ceil, floor
from Constants import *
import sys
import os.path
import copy

sys.setrecursionlimit(10000)

_save = False ##If True, will Save Maps
_debug = False ##If True, will print more info
_doNavigate = False ##If True, play through level
_failCountMax = 100
_inceptionCnt= 1
_folder = "Dungeons_"+str(_inceptionCnt)+"\\"

_avgEnemies = 4
_varEnemies = 1
_eliteChance = .05
_brushChance = .15
_avgHealthPacks= 0
_varHealthPacks= 1
_avgWeapons = -1
_varWeapons = 2
_avgChests = 0
_varChests = 2

_roomsToRow = 7
_roomsToCol = 7
_dungeonCount = 1
_minRoomSize = 6
_maxRoomSize = 11
_avgConnections = 2
_permutationChance = 60 ##Chance that a room will be mutated
_decorationChance = 20


_minQuadrantSize = max(ceil(_maxRoomSize * 1.5)+1, _maxRoomSize+3)
_minPlaneSize = _minQuadrantSize * max(_roomsToRow, _roomsToCol)
_maxPlaneSize = _minQuadrantSize * max(_roomsToRow, _roomsToCol) ** _inceptionCnt

_allRooms = []
_allPlanes= []
_connectedRooms = {}
_allCorridors = []
_allQuadrants = []
_stairLocations = []

def gen2DArray(size, contents):
    outArray = []
    for row in range(size):
        outArray.append([])
        for col in range(size):
            outArray[row].append(contents)
    return outArray

def gen2DArray_var(height, width, contents):
    outArray = []
    for row in range(height):
        outArray.append([])
        for col in range(width):
            outArray[row].append(contents)
    return outArray

def stampRoom(array, room):
    for row in range(room.Row, room.Row+room.Height):
        for col in range(room.Col, room.Col+room.Width):
            if room.Stamp == True:
                if row not in range(room.StampR, room.StampR+room.StampH):
                    array[row][col] = SPACE
                elif col not in range(room.StampC, room.StampC+room.StampW):
                    array[row][col] = SPACE
            else:
                array[row][col] = SPACE
    makeDeco(array, room)

def makeDeco(array, room):
    if rand(100) >= _decorationChance:
        return
    
    rows = list(range(room.Row+1, room.Row+room.Height-1))
    cols = list(range(room.Col+1, room.Col+room.Width-1))
    shuffle(rows)
    shuffle(cols)
    for row in rows:
        for col in cols:
            if array[row][col] == WALL:
                array[row][col] = DECORATION
                if rand(100) > _decorationChance:
                    return

def ArrayToString(array, stampLoc=(-1, -1), stampChar='F'):
    outString = ""
    for row in range(len(array)):
        for col in range(len(array[row])):
            if row == stampLoc[0] and col == stampLoc[1]:
                if isValid(array, stampLoc[0], stampLoc[1]):
                    outString += stampChar
            else:
                outString += array[row][col]
        outString += '\n'
    return outString

def ArrayToStringHardNewLines(array, stampLoc=(-1, -1), stampChar='F'):
    outString = ""
    for row in range(len(array)):
        for col in range(len(array[row])):
            if row == stampLoc[0] and col == stampLoc[1]:
                if isValid(array, stampLoc[0], stampLoc[1]):
                    outString += stampChar
            else:
                outString += array[row][col]
                if array[row][col] == '\\':
                    outString += '\\'
        outString += '\\n'
    return outString

def isValid(array, row, col):
    if row < 0 or row >= len(array):
        return False
    if col < 0 or col >= len(array[0]):
        return False
    return True

def GenCSV():
    outString = ""
    for room in _allRooms:
        outString += str(room.Row)+", "+str(room.Col)+", "+str(room.Row+room.Height-1)+", "+str(room.Col+room.Width-1)
        if room.Stamp:
            outString += ', '
            outString += str(room.StampR)+", "+str(room.StampC)+", "+str(room.StampR+room.StampH-1)+", "+str(room.StampC+room.StampW-1)
        outString += '\n'
    return outString

def GenJS():
    outString = "var level_ = {\n"

    outString += "\"layout\":"
    outString += str(_array)
    outString += ",\n"

    outString += "\"rooms\":["
    for room in _allRooms:
        outString += "["
        outString += str(room.Row)+", "+str(room.Col)+", "+str(room.Row+room.Height-1)+", "+str(room.Col+room.Width-1)
        if room.Stamp:
            outString += ', '
            outString += str(room.StampR)+", "+str(room.StampC)+", "+str(room.StampR+room.StampH-1)+", "+str(room.StampC+room.StampW-1)
        outString += "],"

    outString = outString[0:-1]
    outString += "],\n"

    outString += "\"corridors\":"
    outString += str(_allCorridors)
    outString += "\n"
    
    outString += "}"
    return outString

def getAdjSpaces(array, row, col, target=None, diag=False):
    spaces = []
    for r in range(-1, 2, 2):
        if isValid(array, row+r, col) and (array[row+r][col] == target or target == None):
            spaces.append((row+r, col))
        if isValid(array, row, col+r) and (array[row][col+r] == target or target == None):
            spaces.append((row, col+r))
        if diag:
            if isValid(array, row-r, col+r) and (array[row-r][col+r] == target or target == None):
                spaces.append((row-r, col+r))
            if isValid(array, row+r, col+r) and (array[row+r][col+r] == target or target == None):
                spaces.append((row+r, col+r))

    return spaces

def viewArea(row, col, radius):
        viewArea = []
        valArea = []
        for i in range(radius*2+1):
            viewArea.append([])
            valArea.append([])
            for j in range(radius*2+1):
                if isValid(_array, row-radius+i, col-radius+j):
                    char = _array[row-radius+i][col-radius+j]
                    viewArea[i].append(char)
                else:
                    viewArea[i].append(WALL)
                valArea[i].append(radius+1)
        viewArea[radius][radius] = '@'
        valArea[radius][radius] = 0

        getSight(radius, radius, viewArea, valArea)

        for r in range(len(valArea)):
            for c in range(len(valArea[r])):
                if valArea[r][c] > radius:
                    viewArea[r][c] = WALL
        
        return viewArea

def getSight(row, col, viewArea, valArea):
        tRow = row-1
        tCol = col
        if isValid(valArea, tRow, tCol):
            if (valArea[tRow][tCol]):
                if viewArea[row][col] != WALL:
                    if (valArea[tRow][tCol] > valArea[row][col]+1):
                        valArea[tRow][tCol] = valArea[row][col]+1
                        getSight(tRow, tCol, viewArea, valArea)
        tRow = row+1
        tCol = col
        if isValid(valArea, tRow, tCol):
            if (valArea[tRow][tCol]):
                if viewArea[row][col] != WALL:
                    if (valArea[tRow][tCol] > valArea[row][col]+1):
                        valArea[tRow][tCol] = valArea[row][col]+1
                        getSight(tRow, tCol, viewArea, valArea)
        tRow = row
        tCol = col+1
        if isValid(valArea, tRow, tCol):
            if (valArea[tRow][tCol]):
                if viewArea[row][col] != WALL:
                    if (valArea[tRow][tCol] > valArea[row][col]+1):
                        valArea[tRow][tCol] = valArea[row][col]+1
                        getSight(tRow, tCol, viewArea, valArea)
        tRow = row
        tCol = col-1
        if isValid(valArea, tRow, tCol):
            if (valArea[tRow][tCol]):
                if viewArea[row][col] != WALL:
                    if (valArea[tRow][tCol] > valArea[row][col]+1):
                        valArea[tRow][tCol] = valArea[row][col]+1
                        getSight(tRow, tCol, viewArea, valArea)

def mkMove(move, playerLoc):
        if move in "wW":
            if isValid(_array, playerLoc[0]-1, playerLoc[1]):
                spot = _array[playerLoc[0]-1][playerLoc[1]]
                if spot != WALL:
                    playerLoc[0] -= 1
                    if (move == "W"):
                        mkMove(move, playerLoc)
        if move in "aA":
            if isValid(_array, playerLoc[0], playerLoc[1]-1):
                spot = _array[playerLoc[0]][playerLoc[1]-1]
                if spot != WALL:
                    playerLoc[1] -= 1
                    if (move == "A"):
                        mkMove(move, playerLoc)
        if move in "sS":
            if isValid(_array, playerLoc[0]+1, playerLoc[1]):
                spot = _array[playerLoc[0]+1][playerLoc[1]]
                if spot != WALL:
                    playerLoc[0] += 1
                    if (move == "S"):
                        mkMove(move, playerLoc)
        if move in "dD":
            if isValid(_array, playerLoc[0], playerLoc[1]+1):
                spot = _array[playerLoc[0]][playerLoc[1]+1]
                if spot != WALL:
                    playerLoc[1] += 1
                    if (move == "D"):
                        mkMove(move, playerLoc)

class Room:
    def __init__(this, row, col, height, width):
        this.Row = row
        this.Col = col
        this.Height = height
        this.Width = width
        this.Connections = []
        _allRooms.append(this)
        this.Stamp = False
        this.genStamp()

    def genStamp(this):
        chance = rand(0, 100)
        this.Stamp = False
        if (chance <= _permutationChance):
            this.Stamp = True
            this.StampW = rand(2, max(ceil(min(this.Height, this.Width)/2), 2+1))
            this.StampH = this.StampW
            this.StampR = rand(this.Row, this.Row+this.Height-this.StampH)
            this.StampC = rand(this.Col, this.Col+this.Width-this.StampW)
            this.validStamp()

    def validStamp(this):
        if (this.Row+this.Height - (this.StampR+this.StampH)) == 1:
            if not (this.Col+this.Width - (this.StampC+this.StampW)) == 1:
                this.StampR += 1
        if (this.StampR - this.Row) == 1:
            if not (this.StampC - this.Col) == 1:
                this.StampR -= 1
        if (this.Col+this.Width - (this.StampC+this.StampW)) == 1:
            if not (this.Row+this.Height - (this.StampR+this.StampH)) == 1:
                this.StampC += 1
        if (this.StampC - this.Col) == 1:
            if not (this.StampR - this.Row) == 1:
                this.StampC -= 1

class Quadrant:
    def __init__(this, row, col, size):
        _allQuadrants.append(this)
        this.Row = int(row)
        this.Col = int(col)
        this.Size = int(size)
        this.Type = "Quadrant"

        this.roomW = int(rand(_minRoomSize, _maxRoomSize))
        this.roomH = int(rand(_minRoomSize, _maxRoomSize))
        this.roomR = this.Row+rand(1, size-this.roomH)
        this.roomC = this.Col+rand(1, size-this.roomW)


        this.roomR = this.Row+2
        if row+2 < int(this.Row+size-this.roomH-1):
            this.roomR = rand(this.Row+2, int(this.Row+size-this.roomH-1))
        this.roomC = this.Col+2
        if col+2 < int(this.Col+size-this.roomW-1):
            this.roomC = rand(this.Col+2, int(this.Col+size-this.roomW-1))

        this.Room = Room(this.roomR, this.roomC, this.roomH, this.roomW)

        this.getLeftEdge()
        this.getRightEdge()
        this.getTopEdge()
        this.getBottomEdge()

    def getLeftEdge(this):
        col = this.roomC
        validSpots = []
        ##print(this.roomR, this.roomH)
        for spot in range(this.roomR, this.roomR+this.roomH):
            if this.Room.Stamp == False:
                validSpots.append(spot)
            else:
                if spot not in range(this.Room.StampR, this.Room.StampR+this.Room.StampH):
                    validSpots.append(spot)
                elif this.Room.StampC > this.Room.Col:
                    validSpots.append(spot)
        shuffle(validSpots)
        return (validSpots[0], col-1)

    def getRightEdge(this):
        col = this.roomC+this.roomW
        validSpots = []
        for spot in range(this.roomR, this.roomR+this.roomH):
            if this.Room.Stamp == False:
                validSpots.append(spot)
            else:
                if spot not in range(this.Room.StampR, this.Room.StampR+this.Room.StampH):
                    validSpots.append(spot)
                elif this.Room.StampC+this.Room.StampW < this.Room.Col+this.Room.Width:
                    validSpots.append(spot)
        shuffle(validSpots)
        return (validSpots[0], col)

    def getTopEdge(this):
        row = this.roomR
        validSpots = []
        for spot in range(this.roomC, this.roomC+this.roomW):
            if this.Room.Stamp == False:
                validSpots.append(spot)
            else:
                if spot not in range(this.Room.StampC, this.Room.StampC+this.Room.StampW):
                    validSpots.append(spot)
                elif this.Room.StampR > this.Room.Row:
                    validSpots.append(spot)
        shuffle(validSpots)
        return (row-1, validSpots[0])

    def getBottomEdge(this):
        row = this.roomR+this.roomH
        validSpots = []
        for spot in range(this.roomC, this.roomC+this.roomW):
            if this.Room.Stamp == False:
                validSpots.append(spot)
            else:
                if spot not in range(this.Room.StampC, this.Room.StampC+this.Room.StampW):
                    validSpots.append(spot)
                elif this.Room.StampR+this.Room.StampH < this.Room.Row+this.Room.Height:
                    validSpots.append(spot)
        shuffle(validSpots)
        return (row, validSpots[0])

    def getRoom(this):
        return this.Room

class Plane:
    def __init__(this, row, col, size):
        this.HasSubPlane = (size > _minPlaneSize)
        this.Col = col
        this.Row = row
        this.Size= size
        this.QuadSize = floor(this.Size / _roomsToRow)
        this.QuadSizeW =floor(this.Size / _roomsToCol)
        this.Type = "Plane"

        this.containers = []

        this.genQuadrants()
        this.connectContainers()

    ##This returns a tuple with the lower and upper bounds of size in a quadrant
    ##  relative to the starting position of the Plane object
    def getQuadrantRowRange(this, quadR):
        outR = this.Row + (this.QuadSize * quadR)
        outH = this.Row + (this.QuadSize * quadR+1)
        return (outR, outH)

    def getQuadrantColRange(this, quadR):
        outR = this.Col + (this.QuadSizeW * quadR)
        outH = this.Col + (this.QuadSizeW * quadR+1)
        return (outR, outH)

    def genQuadrants(this):
        if this.HasSubPlane:
            containerObject = Plane
        else:
            containerObject = Quadrant

        for r in range(0,_roomsToRow):
            for c in range(0,_roomsToCol):
                newR = this.getQuadrantRowRange(r)[0]
                newC = this.getQuadrantColRange(c)[0]
                this.containers.append(containerObject(newR, newC, this.QuadSize))

    def getRelativeQuadrant(this, row, col):
        index = row*_roomsToCol+col
        if index == len(this.containers):
            for i in range(len(this.containers)):
                room = this.containers[i]
                ##print(room.Row, room.Col)
            ##(row, col)
            
        return this.containers[index]

    def connectContainers(this):
        connected = []
        for aRow in range(0, _roomsToRow):
            connected.append([])
            for aCol in range(0, _roomsToCol):
                connected[-1].append(0)
        
        failCount = 0
        summary = 0
        for nRow in range(len(connected)):
            summary+=sum(connected[nRow])
            
        while summary < _roomsToRow*_roomsToCol:
            if failCount >= _failCountMax:
                return False
            r = rand(0,_roomsToRow)
            c = rand(0,_roomsToCol)
            if summary > 0:
                while connected[r][c] != 0:
                    r = rand(0,_roomsToRow)
                    c = rand(0,_roomsToCol)
            options = []
            for r2 in range(-1,2):
                for c2 in range(-1,2):
                    if r2 == 0 or c2 == 0:
                        if isValid(connected, r+r2, c+c2):
                            options.append((r+r2, c+c2))
            shuffle(options)
            for option in range(0, min(len(options), max(1, _avgConnections+rand(-1,2)))):
                if this.connect(r,c, options[option][0], options[option][1]):
                    connected[r][c] = 1
                else:
                    failCount+=1

            summary = 0
            for nRow in range(len(connected)):
                summary+=sum(connected[nRow])
        return True

    def getAllRooms(this):
        outRooms = []
        for r in range(0,_roomsToRow):
            for c in range(0,_roomsToCol):
                Quadrant = this.getRelativeQuadrant(r,c)
                if Quadrant.Type == "Quadrant":
                    outRooms.append(Quadrant)
                else:
                    deeperRooms = Quadrant.getAllRooms()
                    for room in deeperRooms:
                        outRooms.append(room)
        return outRooms

    def connect(this, r, c, r2, c2):
        for i in [r, r2]:
            if i < 0 or i >= _roomsToRow:
                return False
        for j in [c, c2]:
            if j < 0 or j >= _roomsToCol:
                return False
        
        _allCorridors.append([])
        quadA = this.getRelativeQuadrant(r, c)
        quadB = this.getRelativeQuadrant(r2, c2)

        if quadA not in _connectedRooms.keys():
            _connectedRooms[quadA] = []
        if quadB not in _connectedRooms.keys():
            _connectedRooms[quadB] = []
        if quadB not in _connectedRooms[quadA] and quadA not in _connectedRooms[quadB]:
            _connectedRooms[quadA].append(quadB)
            _connectedRooms[quadB].append(quadB)
        else:
            _allCorridors.pop(-1)
            return False
        
        if r > r2:
            locA = quadA.getTopEdge()
            locB = quadB.getBottomEdge()
            _allCorridors[-1].append([locA[0],locA[1]])
            _allCorridors[-1].append([locB[0],locB[1]])
            return this.MakeConnectVertically(_array, [locA[0],locA[1]], [locB[0], locB[1]])
        elif r < r2:
            locA = quadA.getBottomEdge()
            locB = quadB.getTopEdge()
            _allCorridors[-1].append([locA[0],locA[1]])
            _allCorridors[-1].append([locB[0],locB[1]])
            return this.MakeConnectVertically(_array, [locA[0],locA[1]], [locB[0], locB[1]])
        elif c > c2:
            locA = quadA.getLeftEdge()
            locB = quadB.getRightEdge()
            _allCorridors[-1].append([locA[0],locA[1]])
            _allCorridors[-1].append([locB[0],locB[1]])
            return this.MakeConnectHorizontally(_array, [locA[0],locA[1]], [locB[0], locB[1]])
        elif c < c2:
            locA = quadA.getRightEdge()
            locB = quadB.getLeftEdge()
            _allCorridors[-1].append([locA[0],locA[1]])
            _allCorridors[-1].append([locB[0],locB[1]])
            return this.MakeConnectHorizontally(_array, [locA[0],locA[1]], [locB[0], locB[1]])
        else:
            _allCorridors.pop(-1)
            return False

    def MakeConnectVertically(this, array, pointA, pointB):
        r1 = pointA[0]
        c1 = pointA[1]
        r2 = pointB[0]
        c2 = pointB[1]
        if not isValid(array, r1, c1):
            return False
        if not isValid(array, r2, c2):
            return False
        
        array[r1][c1] = CORRIDOR
        if rand(0,2) == 2:
            array[r2][c2] = DOOR
        else:
            array[r2][c2] = CORRIDOR
        return this.ConnectVertically(array, pointA, pointB)

    def MakeConnectHorizontally(this, array, pointA, pointB):
        r1 = pointA[0]
        c1 = pointA[1]
        r2 = pointB[0]
        c2 = pointB[1]
        if not isValid(array, r1, c1):
            return False
        if not isValid(array, r2, c2):
            return False
        
        array[r1][c1] = CORRIDOR
        if rand(0,2) == 2:
            array[r2][c2] = DOOR
        else:
            array[r2][c2] = CORRIDOR
        return this.ConnectHorizontally(array, pointA, pointB)

    def ConnectVertically(this, array, pointA, pointB, brushed=False):
        outChar = CORRIDOR
        newBrushed = False
        if brushed:
            if (rand(100) >= _brushChance):
                outChar = BRUSH
                newBrushed = True
        if not brushed:
            if (rand(100) <= _brushChance):
                outChar = BRUSH
                newBrushed = True
        brushed = newBrushed
            
        if pointA[0] == pointB[0]:
            if pointA[1] == pointB[1]:
                return True
            else:
                _allCorridors[-1].insert(-1, [pointA[0],pointA[1]])
                _allCorridors[-1].insert(-1, [pointB[0],pointB[1]])
                return this.ConnectHorizontally(array, pointA, pointB, brushed)
        if pointA[0] > pointB[0]:
            if rand(2) == 0:
                pointB[0] += 1
            else:
                pointA[0] -= 1
        else:
            if rand(2) == 0:
                pointB[0] -= 1
            else:
                pointA[0] += 1

        if array[pointA[0]][pointA[1]] != DOOR:	
            array[pointA[0]][pointA[1]] = outChar
        if array[pointB[0]][pointB[1]] != DOOR:
            array[pointB[0]][pointB[1]] = outChar
	
        return this.ConnectVertically(array, pointA, pointB, brushed)

    def ConnectHorizontally(this, array, pointA, pointB, brushed=False):
        outChar = CORRIDOR
        newBrushed = False
        if brushed:
            if (rand(100) >= _brushChance):
                outChar = BRUSH
                newBrushed = True
        if not brushed:
            if (rand(100) <= _brushChance):
                outChar = BRUSH
                newBrushed = True
        brushed = newBrushed
        
        
        if pointA[1] == pointB[1]:
            if pointA[0] == pointB[0]:
                return True
            else:
                _allCorridors[-1].insert(-1, [pointA[0],pointA[1]])
                _allCorridors[-1].insert(-1, [pointB[0],pointB[1]])
                return this.ConnectVertically(array, pointA, pointB, brushed)
        if pointA[1] > pointB[1]:
            if rand(2) == 0:
                pointB[1] += 1
            else:
                pointA[1] -= 1
        else:
            if rand(2) == 0:
                pointB[1] -= 1
            else:
                pointA[1] += 1
        if array[pointA[0]][pointA[1]] != DOOR:	
            array[pointA[0]][pointA[1]] = outChar
        if array[pointB[0]][pointB[1]] != DOOR:
            array[pointB[0]][pointB[1]] = outChar
        return this.ConnectHorizontally(array, pointA, pointB, brushed)  

    def getLeftEdge(this):
        options = []
        for i in range(_roomsToRow):
            options.append(this.getRelativeQuadrant(i,0))
        return options[rand(len(options))].getLeftEdge()
    def getRightEdge(this):
        options = []
        for i in range(_roomsToRow):
            options.append(this.getRelativeQuadrant(i, _roomsToCol-1))
        return options[rand(len(options))].getRightEdge()
    def getTopEdge(this):
        options = []
        for i in range(_roomsToCol):
            options.append(this.getRelativeQuadrant(0,i))
        return options[rand(len(options))].getTopEdge()
    def getBottomEdge(this):
        options = []
        for i in range(_roomsToCol):
            options.append(this.getRelativeQuadrant(_roomsToRow,i))
        return options[rand(len(options))].getBottomEdge()

def clearArray(contents):
    for row in range(len(_array)):
        for col in range(len(_array[row])):
            _array[row][col] = contents

    _allRooms.clear()
    _allPlanes.clear()
    _connectedRooms.clear()
    _allCorridors.clear()
    _allQuadrants.clear()
    _stairLocations.clear()

def makeDungeon():
    highPlane = Plane(0, 0, _maxPlaneSize)
    
    for room in _allRooms:
        stampRoom(_array, room)

    if highPlane not in _connectedRooms:
        _connectedRooms[highPlane] = []

    keyList = list(_connectedRooms.keys())
    for key in range(len(keyList)):
        if (keyList[key].Type == "Plane"):
            _allPlanes.append(keyList[key])

def saveDungeon(filename):
    
    if os.path.isfile(_folder+filename+".txt"):
        return saveDungeon(filename+"-1")
    
    file = open(_folder+filename+".txt", "w")
    file.write(ArrayToString(_array))
    file.close()

def saveCSV(filename):
    
    if os.path.isfile(_folder+filename+".csv"):
        return saveCSV(filename+"-1")
    
    file = open(_folder+filename+".csv", "w")
    file.write(GenCSV())
    file.close()

def saveJS(filename):
    if os.path.isfile(_folder+filename+".js"):
        return saveCSV(filename+"-1")
    
    file = open(_folder+filename+".js", "w")
    file.write(GenJS())
    file.close()


def addStairs():
    minConnections = -1
    relevantPlanes = []
    selectedRooms = []
    for plane in _allPlanes:
        relevantPlanes.append(plane)
        if len(_connectedRooms[plane]) < minConnections:
            relevantPlanes = []
            minConnections = len(_connectedRooms[plane])+1
        if len(_connectedRooms[plane]) <= minConnections:
            relevantPlanes.append(plane)
    shuffle(relevantPlanes)
    planeA = relevantPlanes[0]
    planeB = relevantPlanes[-1]

    planeARooms = planeA.getAllRooms()
    relevantRooms = []
    minConnections = -100
    for room in planeARooms:
        relevantRooms.append(room)
        if len(_connectedRooms[room]) < minConnections:
            relevantRooms = []
            minConnections = len(_connectedRooms[room])+1
        if len(_connectedRooms[room]) <= minConnections:
            relevantRooms.append(room)
    shuffle(relevantRooms)
    selectedRooms.append(relevantRooms[0])

    planeBRooms = planeB.getAllRooms()
    relevantRooms = []
    minConnections = 100
    for room in planeBRooms:
        if len(_connectedRooms[room]) < minConnections:
            relevantRooms = []
            minConnections = len(_connectedRooms[room])+1
        if len(_connectedRooms[room]) <= minConnections:
            relevantRooms.append(room)
    shuffle(relevantRooms)
    if relevantRooms[0] not in selectedRooms:
        selectedRooms.append(relevantRooms[0])
    else:
        selectedRooms.append(relevantRooms[-1])
    
    for rm in range(len(selectedRooms)):
        room = selectedRooms[rm].getRoom()
        allSpaces = []
        for row in range(room.Row, room.Row+room.Height):
            for col in range(room.Row, room.Row+room.Height):
                if _array[row][col] == SPACE:
                    if len(getAdjSpaces(_array, row, col, SPACE)) > 2:
                        allSpaces.append([row, col])
        shuffle(allSpaces)
        spot = allSpaces[0]
        _array[spot[0]][spot[1]] = STAIRS[rm]
        _stairLocations.append((spot[0], spot[1]))

def addChars(char, placeAvg, placeVar, options=[]):
    allSpaces = []
    stairs= False
    for room in _allRooms:
        stairs = False
        allSpaces = []
        allSpaces.clear()
        for row in range(room.Row, room.Row+room.Height):
            for col in range(room.Col, room.Col+room.Width):
                if _array[row][col] == SPACE:
                    allSpaces.append([row, col])
                if _array[row][col] == STAIRS[0]:
                    stairs = True
        if stairs:
            continue
        shuffle(allSpaces)
        placeCnt = rand(placeAvg-placeVar, placeAvg+1+placeVar)
        if placeCnt < 1:
            continue
        placeCnt = min(len(allSpaces), placeCnt)
        for i in range(placeCnt):
            spot = allSpaces[i]
            if (abs(_stairLocations[0][0] - _stairLocations[1][0]) > _maxRoomSize):
                if (abs(_stairLocations[0][1] - _stairLocations[1][1]) > _maxRoomSize):
                    _array[spot[0]][spot[1]] = char
                    if len(options) > 1:
                        if rand(0,100) < options[1]*100:
                            _array[spot[0]][spot[1]] = options[0]
                    

def Navigate():
    playerLoc = [_stairLocations[0][0], _stairLocations[0][1]]
    print(ArrayToString(viewArea(playerLoc[0], playerLoc[1], _minQuadrantSize)))
    while True:
        move = input("wasd: move | m: map | q: quit \n")
        if len(move) == 1:
            if move in "wasdWASD":
                mkMove(move, playerLoc)
                print(ArrayToString(viewArea(playerLoc[0], playerLoc[1], _minQuadrantSize)))
            if move == "q":
                break
            if move == "m":
                print(ArrayToString(_array, playerLoc, PLAYER))

def makeLevel(inSeed, debugging=False, save=False):
    _debug = debugging
    _save = save
    successes = 0
    seed(inSeed)
    nextSeed = randint(0, 25500)
    while successes < _dungeonCount:
        seed(nextSeed)
        nextSeed = randint(0, 52500)
        
        fail = False
        try:
            makeDungeon()
            addStairs()
            addChars(ENEMY, _avgEnemies, _varEnemies, [ENEMY_ELITE, _eliteChance])
            addChars(HEALTH, _avgHealthPacks, _varHealthPacks)
            addChars(ITEM, _avgWeapons, _varWeapons)
            addChars(CHEST, _avgChests, _varChests)
        except IndexError:
            if _debug:
                print("Failed to Decorate Rooms")
            clearArray(WALL)
            continue

        enemySeen = False
        itemSeen = False
        healthSeen = False
        for row in _array:
            for col in row:
                if col == ENEMY: enemySeen = True
                if col == HEALTH: healthSeen=True
                if col == ITEM: enemySeen = True
        if not enemySeen:
            fail = True
        
            
        if (abs(_stairLocations[0][0] - _stairLocations[1][0]) < _maxRoomSize):
            if (abs(_stairLocations[0][1] - _stairLocations[1][1] < _maxRoomSize)):
                if _debug:
                    print("Failure:  Stairs too close", _stairLocations)
                _stairLocations.clear()
                fail = True
        if not fail:
            if _debug:
                print(ArrayToString(_array))
            successes+=1
            if _debug:
                print(successes)
            if _save:
                saveDungeon("DungeonLevel_"+str(successes))
                saveCSV("DungeonLevel_"+str(successes))
                saveJS("DungeonLevel_"+str(successes))
        if _doNavigate:
            Navigate()
        if _debug:
            for corridor in _allCorridors:
                print(corridor)
        outArray = copy.deepcopy(_array)
        clearArray(WALL)
    return outArray

def generateLevel(inSeed, width=3, height=3, minSize=6, maxSize=11, avgCnx=2, avgEn=4, varEn=1):
    if height < width:
        nHeight = width
        width = height
        height = nHeight

    global _roomsToRow
    global _roomsToCol
    global _minRoomSize
    global _maxRoomSize
    global _avgConnections
    global _permutationChance
    global _decorationChance
    global _avgEnemies
    global _varEnemies
    global _eliteChance
    global _avgHealthPacks
    global _varHealthPacks
    global _avgWeapons
    global _varWeapons
    global _minQuadrantSize
    global _minPlaneSize
    global _maxPlaneSize
    global _array
    
    _roomsToRow = height
    _roomsToCol = width
    _minRoomSize = minSize
    _maxRoomSize = maxSize
    _avgConnections = avgCnx
    _permutationChance =60 ##Chance that a room will be mutated
    _decorationChance = 65

    _avgEnemies = avgEn
    _varEnemies = varEn
    _eliteChance = .075
    _avgHealthPacks= -1
    _varHealthPacks= 2
    _avgWeapons = -1
    _varWeapons = 2

    _minQuadrantSize = max(ceil(_maxRoomSize * 1.5)+1, _maxRoomSize+3)
    _minPlaneSize = _minQuadrantSize * max(_roomsToRow, _roomsToCol)
    _maxPlaneSize = _minQuadrantSize * max(_roomsToRow, _roomsToCol) ** _inceptionCnt
    _array = gen2DArray(ceil(_maxPlaneSize*1.1), WALL)
    
    return makeLevel(inSeed)



_array = gen2DArray(ceil(_maxPlaneSize*1.1), WALL)
##generateLevel()
