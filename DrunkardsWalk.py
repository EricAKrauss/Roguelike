from QuadrantTheory import *
from Constants import *
from random import randrange as rand
from random import shuffle, seed

def GenLevel(inSeed, height, width, features, downStairs=True):
    seed(inSeed)
    height = height * 8
    width = width * 8
    array = gen2DArray_var(height*2, width*2, WALL)

    tileRatio = 0.5
    tileGoal = height*width*tileRatio
    ##cursor = [rand(height), rand(width)]
    cursor = [int(height/2), int(width/2)]
    orig = [cursor[0], cursor[1]]
    walk(array, cursor, tileGoal)

    array[orig[0]][orig[1]] = STAIRS[0]
    end = GenLevel.end
    if downStairs:
        array[end[0]][end[1]] = STAIRS[1]
    
    genFeatures(array, height, width, features+1, [orig])
    array = package(array)
    return array

def walk(array, cursor, goal, count=0):
    row = cursor[0]
    col = cursor[1]
    if array[row][col] == WALL:
        count+=1
        array[row][col] = SPACE

    if count >= goal:
        GenLevel.end = cursor
        return array
        
    adjSpots = getAdjSpaces(array, row, col)
    shuffle(adjSpots)
    cursor = adjSpots[0]
    walk(array, cursor, goal, count)

def genFeatures(array, height, width, features, pntList=[], attempts=0):
    ##print(ArrayToString(array))
    attempts+=1
    if len(pntList) >= features:
        return array
    if attempts > 25:
        return array
    
    point = [rand(height), rand(width)]
    if array[point[0]][point[1]] != SPACE:
        return genFeatures(array, height, width, features, pntList, attempts)
    
    for pnt in pntList:
        if abs(pnt[0]-point[0]) < min(height, width)/8:
            if abs(pnt[1]-point[1] < min(height, width)/8):
                return genFeatures(array, height, width, features, pntList, attempts)

    maxR = min(5, height-point[0])
    maxC = min(5, width-point[1])
    rowRange = list(range(-4, maxR))
    colRange = list(range(-4, maxC))
    shuffle(rowRange)
    shuffle(colRange)

    index = rand(10)
    if index < 3:
        loot = CHEST
    elif index < 7:
        loot = HEALTH
    else:
        loot = ITEM
    array[point[0]][point[1]] = loot

    elitePlaced = False
    enemiesPlaced = 0
    enemiesMax = 3
    while len(rowRange) > 0 and len(colRange) > 0:
        r = max(0, point[0] + rowRange.pop(0))
        c = max(0, point[1] + colRange.pop(0))
        if array[r][c] == SPACE:
            if not elitePlaced:
               elitePlaced = True
               array[r][c] = ENEMY_ELITE
            else:
               array[r][c] = ENEMY
            enemiesPlaced += 1
        if enemiesPlaced >= enemiesMax:
            break

    pntList.append(point)
    return genFeatures(array, height, width, features, pntList, attempts)
                   
def package(array, buffer=4):
    newArray = gen2DArray_var(len(array)+buffer*2, len(array[0])+buffer*2, WALL)
    for row in range(len(array)):
        for col in range(len(array[0])):
            newArray[row+buffer][col+buffer] = array[row][col]
    return newArray
                       


if __name__ == "__main__":
    maze = GenLevel(rand(25400), 4, 4, 4)
    print(ArrayToString(maze))
    
