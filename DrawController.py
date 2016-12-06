import tdl
from math import floor
from random import randrange as rand
from random import seed
from copy import copy

import os
import psutil

from Constants import *
##from LevelTypes.Level import *
from Controls import *
from Player import *
from Player_Classes import *
from MessageSys import *
##from LevelManager import *

def initTDL(height, width, level):
    viewArea = level.getPlayerViewArea(1.5)
    r1 = viewArea[0]
    c1 = viewArea[1]
    r2 = viewArea[2]
    c2 = viewArea[3]

    console = tdl.init(c2-c1+width, r2-r1+height, "RogueLike")
    
    tdl.set_fps(0)
    ##tdl.set_fullscreen(True)
    console.set_colors([255,255,255], [0,0,0])
    tdl.flush()
    return console

def UI_Poll_String(console, message):
    width = len(message)
    question = "| "+message+" |"

    sides = "+" + "-"*(width+2) +"+\n"
    
    cursorX = console.width/2-int(len(sides)/2)

    cursorY = int(console.height/2+2)
    console.move( cursorX, cursorY )
    console.print_str(sides)

    cursorY +=1
    console.move( cursorX, cursorY )
    console.print_str(question)

    cursorY +=2
    console.move( cursorX, cursorY )
    console.print_str(sides)

    tdl.flush()

    string = ""
    cursorY -= 1
    while True:
        console.move( cursorX+1, cursorY )
        console.print_str(" "*20)
        console.move( cursorX, cursorY )
        
        key = getInput()
        if key.key == "F4":
            if key.alt == True:
                return "EXIT"
        if key.key == "ENTER":
            break
        if key.key == "BACKSPACE":
            if len(string) > 0:
                string = string[:-1]
        if key.char == None:
            continue
        else:
            if key.key == "SPACE" or key.key == "CHAR":
                if len(string) < 18:
                    string += str(key.char)


        outString = "|"+string + " "*max(width+2-len(string), 0) + "|"
        console.print_str(outString)
        tdl.flush()
    console.clear()
    tdl.flush()
    return string

def UI_Poll_Yes_or_No(console, message):

    question = "| "+message+" y/n |\n"
    sides = "+" + "-"*(len(question)-3)+"+\n"

    ##console.clear()
    cursorX = console.width/2-int(len(sides)/2)

    cursorY = int(console.height/2+2)
    console.move( cursorX, cursorY )
    console.print_str(sides)

    cursorY +=1
    console.move( cursorX, cursorY )
    console.print_str(question)

    cursorY +=1
    console.move( cursorX, cursorY )
    console.print_str(sides)
    tdl.flush()

    key = getInput("yn")
    console.clear()
    
    if key == "y":
        return True
    if key == "n":
        return False
    if key == "EXIT":
        return "EXIT"

def UI_View(console, array, level, obj, handler, height, width):
    row = obj.row
    col = obj.col

    if not hasattr(obj.Object, "prevTarget"):
        obj.Object.prevTarget = None
    elif obj.Object.prevTarget != None:
        if obj.Object.prevTarget.ID not in level.Objects.keys():
            obj.Object.prevTarget = None
    
    while True:
        char = array[row][col]
        if char == 0: char = SPACE
        if char == 1: char = WALL
                
        tile = level.Tiles[row][col]
        color= tile.getColor(True)
        if tile.getChar(True) != SPACE:
            char = level.Tiles[row][col].getChar(True)

        blitObjectInfo(console, None, height, 30, level, row, col)
        neoBlitMap(console, array, level, obj, None, [col, row, char, [0,0,0], color])
        blitMessages(console, handler)
        blitObjectSkills(console, obj, floor(width/3), height)
        blitBarriers(console, height, width)
        tdl.flush()

        skillNums = "1234567"
        scrollNums= "90"
        validInputs = "qewasdf"+skillNums+scrollNums
        key = getInput(validInputs)
        if key == "EXIT":
            return key
        if key == 'q':
            console.clear()
            return (obj.row, obj.col)
        if key == 'e':
            console.clear()
            return (row, col)
        if key == 'f':
            if obj.fight(level, row, col):
                return True

        if key in skillNums:
            lvl = obj.Object.skillLevels[key]
            skill = obj.Object.skills[key]
            level.messageSys.push(obj.getName() + " used " + skillName(skill))
            if skill(obj.Object, row, col, lvl):
                return True
            else:
                level.messageSys.pop()
                continue
        if key in scrollNums:
            
            if key == "9":
                scroll = "leftScroll"
            if key == "0":
                scroll = "rightScroll"
            if not hasattr(obj.Object, scroll) or getattr(obj.Object, scroll) == None:
                continue

            scrollItem = getattr(obj.Object, scroll)
            level.messageSys.push(obj.getName() + " cast " + scrollItem.getName())
            if scrollItem.cast(obj.Object, row, col):
                obj.Object.unequip(scroll)
                obj.Object.items.pop(-1)
                return True
            else:
                level.messageSys.pop()     
                    
        nrow = row
        ncol = col
        if key == 'w':
            nrow -=1
            nrow = max(0, nrow)
        if key == 's':
            nrow +=1
            nrow = min(nrow, len(array))
        if key == 'a':
            ncol -=1
            ncol = max(0, ncol)
        if key == 'd':
            ncol +=1
            ncol = min(ncol, len(array[row]))

        if level.SeesMap[nrow][ncol] == 1:
            row = nrow
            col = ncol

def skillName(skill):
    string = skill.__name__
    string = string.replace('_', ' ')
    return string


def UI_Map(console, array, level):
    console.clear()

    radiusW = floor(console.width/2)
    radiusH = floor(console.height/2)
    row = max(0, level.thePlayer.pObject.row-radiusH)
    col = max(0, level.thePlayer.pObject.col-radiusW)
    row = min(row, len(array)-console.height)
    col = min(col, len(array[0])-console.width)

    while True:
        ##console.clear()
        for R in range(row, min(row+console.height+2, len(array))):
            for C in range(col, min(col+console.width+2, len(array[0]))):
                if R >= 0 and R < len(array):
                    if C >= 0 and C < len(array[R]):
                        char = array[R][C]
                        if char == 0: char = SPACE
                        if char == 1: char = WALL
                        
                        tile = level.Tiles[R][C]
                        color= tile.getColor(True)
                        if tile.getChar(True) != SPACE:
                            char = level.Tiles[R][C].getChar(True)
                        
                        console.draw_char(C-col, R-row, char, color)
        tdl.flush()
        key = getInput("qwasd")
        if key == "EXIT":
            return key
        if key == 'q':
            console.clear()
            return key
        if len(array) > console.height:
            if key == 'w':
                row -=1
                row = max(0, row)
            if key == 's':
                row +=1
                row = min(row, len(array)-console.height)
        if len(array[0]) > console.width:
            if key == 'a':
                col -=1
                col = max(0, col)
            if key == 'd':
                col +=1
                col = min(col, len(array[0])-console.width)

def UI_Skills(console, obj, width, height):
    if not hasattr(obj, "Object"):
        return False
    actor = obj.Object

    if not hasattr(actor, "skills"):
        return False

    while True:
        console.clear()
        console.move(0, 0)
        console.print_str("+----------+\n|  Skills  |\n+----------+\n|\n|\n")
        blitObjectSkills(console, obj, floor(width/3), height, True)
        console.print_str("| "+obj.getName()+"\n")
        console.print_str("|   Level: "+str(actor.level)+"\n")
        console.print_str("|   Skill Points: "+str(actor.skillPoints)+"\n|\n")
        if actor.skillPoints > 0:
            console.print_str("|   Press a skill's corresponding\n")
            console.print_str("|   Number to advance it's level\n|\n")
            console.print_str("|    One point to buy a skill\n")
            console.print_str("|    Two points to upgrade to level 2,\n")
            console.print_str("|    Three points to upgrade to level 3\n")
            console.print_str("|    Six points to buy your ultimate\n")

        tdl.flush()

        skills = actor.skills
        key = getInput("q1234567")
        if key == "EXIT":
            return "EXIT"
        if key == "q":
            return False
        if key in skills.keys():
            skill = skills[key]
            if actor.skillLevels[key] == 0:
                if not hasattr(skill, "isUltimate") or not skill.isUltimate:
                    if actor.skillPoints >= actor.skillLevels[key]+1:
                        actor.skillPoints -= actor.skillLevels[key]+1
                        actor.skillLevels[key] += 1
                if hasattr(skill, "isUltimate") and skill.isUltimate:
                    if actor.skillPoints >= 6:
                        actor.skillPoints -= 6
                        actor.skillLevels[key] += 1
            elif actor.skillLevels[key] < 3:
                if not hasattr(skill, "isUltimate") or not skill.isUltimate:
                    if actor.skillPoints >= actor.skillLevels[key]+1:
                        actor.skillPoints -= actor.skillLevels[key]+1
                        actor.skillLevels[key] += 1
            skill.update(actor.skillLevels[key], False)
        
        
        

def UI_Character(console, actor):
    if not hasattr(actor, "Object"):
        return False
    actor = actor.Object    

    while True:
        console.clear()
        console.move(0, 0)
        console.print_str("+---------+\n|CHARACTER|\n+---------+\n\n|\n")

        slots = ["Helmet", "Armor", "Right Hand", "Left Hand", "Right Ring", "Left Ring", "Necklace", "Left Scroll", "Right Scroll"]
        items = [actor.helmet, actor.armor, actor.rightHand, actor.leftHand, actor.rightRing, actor.leftRing, actor.necklace, actor.leftScroll, actor.rightScroll]
        for i in range(len(slots)):
            itemNum = '0'+str(i)
            itemName = "None"
            itemInfo = "\n"
            if items[i] != None:
                itemName = items[i].getName()
                itemInfo = items[i].getInfo()

            firstString = "|" + " "*39 + "|\n"
            string = "| "+itemNum+" "+slots[i]+": "+itemName
            string += ' '*(40-len(string))
            string += '| '+itemInfo
            console.print_str(firstString+string)
        tdl.flush()
        
        console.move(0,3)
        console.print_str("+-> quit, unequip")
        console.draw_char(4,3,'q', COLOR_ALLY)
        console.draw_char(10,3,'u',COLOR_ALLY)
        tdl.flush()
        key = getInput("qu")
        if key == "EXIT": return "EXIT"
        if key == 'q':
            return False
        if key == 'u':
            console.move(0,3)
            console.print_str("+->Unequip:"+' '*15)
            tdl.flush()
            index = getInput("0123456789q")
            if index == "EXIT": return "EXIT"
            if index == 'q': continue
            index+= getInput("0123456789q")
            if "EXIT" in index: return "EXIT"
            if 'q' in index: continue
            if int(index) < len(items):
                item = items[int(index)]
                if key == 'u':
                    actor.unequip(slots[int(index)])
                    continue

def UI_Inventory(console, actor):
    if not hasattr(actor, "Object"):
        return False

    rDif = 20
    L = 0
    R = rDif
    
    actor = actor.Object
    key = ""
    mode = "ALL"
    while True:
        R = L+rDif
        console.clear()
        console.move(0, 0)
        console.print_str("+---------+\n|INVENTORY|\n+---------+\n\n|\n")

        if L > 0:
            console.print_str("^\n")
        else:
            console.print_str("|\n")

        allItems = copy(actor.items)
        for itemI in range(len(allItems)):
            iType = allItems[itemI].type
            if mode == "WEAPONS" and not (iType == "1H" or iType == "2H" or iType == "0H"):
                allItems[itemI] = None
                continue
            if mode == "CONSUME" and not (iType == "consumable" or iType == "scroll"):
                allItems[itemI] = None
                continue
            if mode == "ARMOR" and not (iType == "armor" or iType == "helmet"):
                allItems[itemI] = None
                continue

        itemsPrinted = 0
        i = L
        while itemsPrinted < min(rDif, len(allItems)) and i < len(allItems):
            if allItems[i] == None:
                R += 1
                i += 1
                continue
            itemsPrinted+=1

            if R < len(allItems):
                R += 1

            iType = actor.items[i].type
            
            itemNum = str(i)
            while len(itemNum) < len(str(len(allItems))):
                itemNum = '0'+itemNum

            string = "| "+itemNum+": "+str(actor.items[i].getName())
            string += " "*(30-len(string))
            string += "| "+actor.items[i].getInfo()
            console.print_str(string)
            i += 1
        if L+rDif < len(actor.items):
            console.print_str("V\n")
        tdl.flush()
        
        console.move(0,3)
        console.print_str("+-> quit, use, drop, w/s move view")
        console.draw_char(4,3,'q', COLOR_ALLY)
        console.draw_char(10,3,'u',COLOR_ALLY)
        console.draw_char(15,3,'d',COLOR_ALLY)
        console.draw_char(21,3,'w',COLOR_ALLY)
        console.draw_char(23,3,'s',COLOR_ALLY)
        tdl.flush()
        if key != "d":
            key = getInput("qudwscafg")
        if key == "EXIT": return "EXIT"
        if key == 'q':
            return False
        if len(actor.items) > 0:
            if key == 's':
                if L+rDif < len(actor.items) and itemsPrinted == rDif:
                    L+=1
                    R+=1
            if key == 'w':
                if L > 0:
                    L-=1
                    R-=1

            if key == "c":
                L = 0
                mode = "CONSUME"
            if key == "a":
                L = 0
                mode = "ALL"
            if key == "g":
                L = 0
                mode = "ARMOR"
            if key == "f":
                L = 0
                mode = "WEAPONS"
                
            if key in 'ud':
                iLen = len(str(len(allItems)))
                index = ""
                for i in range(iLen):
                    console.move(0,3)
                    if key == 'u':
                        console.print_str("+->Use: "+index+" "*25)
                    if key == 'd':
                        console.print_str("+->Drop: "+index+" "*25)
                    tdl.flush()

                    index+= getInput("0123456789q")
                    if "EXIT" in index: return "EXIT"
                    if 'q' in index: break
                if 'q' in index:
                    key = ""
                    continue
                
                if int(index) < len(actor.items):
                    item = actor.items[int(index)]
                    if key == 'u':
                        if item.use(actor):
                            return True
                    if key == 'd':
                        item.drop(actor)
                        if L > 0:
                            L -= 1
                        continue

def blitMessages(console, handler):
    messages = handler.retrieve()
    messages.reverse()
    
    newConsole = tdl.Console(console.width, len(messages))
    cursorY = 0
    for string in messages:
        newConsole.move(0, cursorY)
        newConsole.print_str(string)
        cursorY+=1
    console.blit(newConsole, 0, -20)

def neoBlitMap(console, array, level, obj=None, hardView=None, specChar=None):
    if obj == None:
        obj = level.thePlayer
    else:
        obj = obj.Object

    newConsole = tdl.Console(26, 25)
    objR = obj.pObject.row
    objC = obj.pObject.col

    for row in range(-12, 14):
        r = min(max(0, objR+row), len(array)-1)
        for col in range(-13, 15):
            c = min(max(0, objC+col), len(array[r])-1)

            char = array[r][c]
            if char == 0: char = SPACE
            if char == 1: char = WALL
                    
            tile = level.Tiles[r][c]
            color= tile.getColor(True)
            invert=tile.getInvertColor()
            if tile.getChar(True) != SPACE:
                char = level.Tiles[r][c].getChar(True)
            
            if not invert:
                newConsole.draw_char(col+13, row+12, char, color)
            else:
                newConsole.draw_char(col+13, row+12, char, COLOR_BLACK, color)

    if specChar != None:
        sR = specChar[1]-objR
        sC = specChar[0]-objC
        newConsole.draw_char(sC+13,sR+12, specChar[2], specChar[3], specChar[4])
    
    console.blit(newConsole, 32,0)

def blitObjectSkills(console, obj, height, width, showAll=False):
    if obj == None:
        return False
    if obj.Object == None:
        return False
    actor = obj.Object

    if not hasattr(actor, "skills"):
        return False

    height+=1
    height = height*5
    
    newConsole = tdl.Console(width+9, height)
    cursorY = 1
    newConsole.move(0, cursorY)

    keys = list(actor.skills.keys())
    keys.sort()
    for i in keys:
        skill = actor.skills[i]
        if not hasattr(skill, "level"):
            continue
        if actor.skillLevels[i] < 1 and not showAll:
            continue
        
        cooldown = skill.cdMax - skill.cd
        
        newConsole.print_str(str(i)+" "+skillName(skill)+": ")
        if cooldown > 0:
            newConsole.print_str("  Cooldown "+str(cooldown)+"\n")
        else:
            newConsole.print_str("\n")
        newConsole.print_str("  Level "+str(skill.level)+"\n")
        if skill.range > 0:
            newConsole.print_str("  Range "+str(skill.range)+"\n")
        newConsole.print_str("  "+str(skill.desc)+"\n\n")

    for btn, scroll in [["0", "rightScroll"], ["9", "leftScroll"]]:
        if hasattr(obj.Object, scroll):
            item = getattr(obj.Object, scroll)
            if item != None:
                newConsole.print_str(btn+" "+item.getName()+"\n")

    console.blit(newConsole, 31+28, 0)

def blitObjectInfo(console, obj, height, width, level=None, row=None, col=None):
    height+=1
    newConsole = tdl.Console(width*3, height)
    cursorY = 1
    newConsole.move(0, cursorY)

    if obj != None:
        newConsole.print_str(obj.getName()+"\n")
        newConsole.print_str("  Floor "+obj.pLevel.name)
        if obj.Object != None:
            if hasattr(obj.Object, "level"):
                cursorY+=3
                newConsole.move(0, cursorY)
                newConsole.print_str("Level: "+str(obj.Object.level))
            if hasattr(obj.Object, "exp"):
                cursorY+=1
                newConsole.move(0, cursorY)
                newConsole.print_str("Exp: "+str(obj.Object.exp)+'/'+str(obj.Object.expNext))
            if hasattr(obj.Object, "health"):                    
                cursorY+=2
                newConsole.move(0, cursorY)
                newConsole.print_str("Health: "+str(int(obj.Object.health))+'/'+str(obj.Object.healthMax))
            if hasattr(obj.Object, "healthTemp") and obj.Object.healthTemp > 0:
                cursorY+=1
                newConsole.move(0, cursorY)
                newConsole.print_str("Temp Health: "+str(int(obj.Object.healthTemp)))
            if hasattr(obj.Object, "arrows"):
                cursorY+=2
                newConsole.move(0, cursorY)
                newConsole.print_str("Arrows: "+str(obj.Object.arrows))
            if hasattr(obj.Object, "range"):
                cursorY+=1
                newConsole.move(0, cursorY)
                newConsole.print_str("Range: "+str(obj.Object.range))
            if hasattr(obj.Object, "power"):
                cursorY+=1
                newConsole.move(0, cursorY)
                newConsole.print_str("Power: "+str(obj.Object.getPower()))
            if hasattr(obj.Object, "getArmorPen"):
                cursorY+=1
                newConsole.move(0, cursorY)
                newConsole.print_str("Armor Pen: "+str(obj.Object.getArmorPen()))
            if hasattr(obj.Object, "getArmor"):
                cursorY+=2
                newConsole.move(0, cursorY)
                newConsole.print_str("Armor: "+str(obj.Object.getArmor()))
            if hasattr(obj.Object, "getWeight"):
                cursorY+=1
                newConsole.move(0, cursorY)
                newConsole.print_str("Weight: "+str(obj.Object.getWeight()))

            if hasattr(obj.Object, "gold"):
                cursorY+=2
                newConsole.move(0, cursorY)
                newConsole.print_str("Gold: "+str(obj.Object.gold))
                

    elif (row != None) and (col != None) and (level != None):
        string = level.Tiles[row][col].getInfo()
        strings = string.split('\n')
        for i in range(min(newConsole.height-1, len(strings))):
            newConsole.print_str(str(strings[i])+'\n')

    console.blit(newConsole)

def blitBarriers(console, height, width):
    for row in range(0, height+1):
        console.draw_char(31, row, '|', COLOR_DEFAULT)
        console.draw_char(31+27, row, '|', COLOR_DEFAULT)
    for col in range(0, 31+27+1):
        console.draw_char(col, height+1, '-', COLOR_DEFAULT)

def blitMap(console, array, level):
    ##print(len(level.master_Changed_Tiles))
    newConsole = tdl.Console(1,1)
    for tile in level.master_Changed_Tiles:
        row = tile[0]
        col = tile[1]
        
        char = array[row][col]
        if char == 0: char = SPACE
        if char == 1: char = WALL
                
        tile = level.Tiles[row][col]
        color= tile.getColor(True)
        if tile.getChar(True) != SPACE:
            char = level.Tiles[row][col].getChar(True)
        
        newConsole.draw_char(0, 0, char, color)
        console.blit(newConsole, col, row)

def printMap(console, array, level):    
    for row in range(len(array)):
            for col in range(len(array[row])):
                char = array[row][col]
                if char == 0: char = SPACE
                if char == 1: char = WALL
                
                tile = level.Tiles[row][col]
                color= tile.getColor(True)
                if tile.getChar(True) != SPACE:
                    char = tile.getChar(True)
                console.draw_char(col, row, char, color)
    tdl.flush()
