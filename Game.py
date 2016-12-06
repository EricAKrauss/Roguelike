import pip

pip.main(['install', "tdl"])
pip.main(['install', "psutil"])

import tdl
from random import randrange as rand
from random import seed
from math import floor

import os
import time
import psutil
import pickle

from Constants import *
from LevelTypes.Level import *
from Controls import *
from Player import *
from Player_Classes import *
from MessageSys import *
from LevelManager import *
from DrawController import *
from QuadrantTheory import ArrayToString

def save(gameState):
    print("Saving file")
    file = open("Saves/"+gameState.thePlayer.getName()+"_World.sv", "w+b")
    fileB= open("Saves/"+gameState.thePlayer.getName()+"_Player.sv", "w+b")
    pickle.dump(gameState, file, 4)
    pickle.dump(gameState.thePlayer, fileB, 4)
    file.close()
    fileB.close()

def load(gameState):
    print("Loading file")
    file = open("Saves/"+gameState.thePlayer.getName()+"_World.sv", "r+b")
    fileB= open("Saves/"+gameState.thePlayer.getName()+"_Player.sv", "r+b")
    gameState = pickle.load(file)
    print("Loaded World")
    gameState.thePlayer = pickle.load(fileB)
    print("Loaded Player")
    file.close()
    fileB.close()
    print("Closed Files")
    gameState.console = initTDL(gameState.xConst, gameState.yConst, gameState.levelList.getLevel())
    print("Reinitialize Window")    
    return gameState

def gameLoopStart(gameState):
        key = True
        while key != False:
            key = gameState.gameLoop()
            if key == "SAVE":
                save(gameState)
            if key == "LOAD":
                gameState = load(gameState)
            if key == "EXIT":
                break

        gameState.killConsole()

class Game:
    def __init__(self):
        print("Game Initiate")
        self.MessageHandler = Messages()
        self.MessageHandler.push("Game Start")

        self.thePlayer = Player("NO_NAME")
        ##self.thePlayer.setClass(Fighter)

        masterSeed = rand(255420)
        ##masterSeed = 200566
        self.levelList = LevelManager(self, self.thePlayer, self.MessageHandler, masterSeed)
        level = self.levelList.getLevel()
        array = level.CollisionMap

        self.xConst = 44
        self.yConst = 75
    
        self.console = initTDL(self.xConst, self.yConst, self.levelList.getLevel())

        viewArea = level.getPlayerViewArea(1.5)
        r1 = viewArea[0]
        c1 = viewArea[1]
        r2 = viewArea[2]
        c2 = viewArea[3]
        self.height= 25
        ##self.width = max(c2-c1, 23)
        self.width = 35

        self.turn = 1
        
        self.thePlayer.name = UI_Poll_String(self.console, "Character Name: ")
        if os.path.isfile("Saves/"+self.thePlayer.name+".sv"):
            if UI_Poll_Yes_or_No(self.console, "Would you like to load this character?"):
                self.loadRequest = True
                return
        self.loadRequest = False        
        
        if self.thePlayer.name == "EXIT":
            return self.killConsole()
        message = ""
        for cls in ClassList:
            message += cls
            if cls != ClassList[-1]:
                message += ", "
            else:   
                message = message[:-len(cls)]
                message += "or "+cls+"?"
        
        classString = self.getStringFromStrings(message, ClassList)
        if classString == "EXIT":
            return self.killConsole()
        self.thePlayer.setClass(Classes[classString])
        self.MessageHandler.push("Player Ready: "+str(self.thePlayer.getName()))

        self.updateDisplay()

    def getStringFromStrings(self, message, strings):
        while True:
            string = UI_Poll_String(self.console, message)
            if string == "EXIT": return string
            if string in strings:
                return string

    def killConsole(self):
        del(self.console.console)
        self.console = None
        self.MessageHandler.push("Game Exit")
        return None

    def updateDisplay(self, obj=None):
        if obj == None:
            obj = self.thePlayer
        else:
            obj = obj.Object
            
        level = self.levelList.getLevel()
        array = level.CollisionMap
        
        level.updateSight(obj.sightDist)
        neoBlitMap(self.console, array, level, obj.pObject)
        blitObjectInfo(self.console, obj.pObject, self.height, 9)
        blitMessages(self.console, self.MessageHandler)
        blitObjectSkills(self.console, obj.pObject, floor(self.width/3), self.height)
        blitBarriers(self.console, self.height, 12)
        tdl.flush()

    def gameLoop(self):
        level = self.levelList.getLevel()
        array = level.CollisionMap        
        if self.levelList.getLevel() != level:
            self.updateDisplay()
            
        killReceived = False
        level.master_Changed_Tiles = []
        obj_list = list(level.Objects.values())
        for objI in range(len(obj_list)):
            obj = obj_list[objI]

            if obj.Object != None:
                if isinstance(obj.Object, Player):
                    if obj.Object.health <= 0:
                        return "EXIT"
            
            if self.turn%obj.getInitiative() == 0:
                obj.update()
            action = False
            keyReceived = None
            while not action:
                if self.turn%obj.getInitiative() == 0:
                    if obj.isPlayerControlled():
                        self.updateDisplay(obj)
                    
                    keyReceived = obj.getAction()
                    if keyReceived == "EXIT":
                        action=True
                        return "EXIT"

                    elif keyReceived == "SAVE":
                        return "SAVE"

                    elif keyReceived == "LOAD":
                        return "LOAD"

                    elif keyReceived == "FIGHT":
                        if hasattr(obj.Object, "prevTarget"):
                            if obj.Object.prevTarget != None:
                                r = obj.Object.prevTarget.row
                                c = obj.Object.prevTarget.col
                                action = obj.fight(level, r, c)

                    elif keyReceived == "INVENTORY":
                        action = UI_Inventory(self.console, obj)
                        self.console.clear()
                        if action == "EXIT":
                            keyReceived = "EXIT"
                            break

                    elif keyReceived == "SKILLS":
                        action = UI_Skills(self.console, obj, self.width, self.height)
                        self.console.clear()
                        if action == "EXIT":
                            keyReceived = "EXIT"
                            break

                    elif keyReceived == "CHARACTER":
                        action = UI_Character(self.console, obj)
                        self.console.clear()
                        if action == "EXIT":
                            keyReceived = "EXIT"
                            break
 
                    elif keyReceived == "MAP":
                        action = UI_Map(self.console, array, level)
                        self.console.clear()
                        if action == "EXIT":
                            keyReceived = "EXIT"
                            break
                        else:
                            action = False

                    elif keyReceived == "VIEW":
                        action = UI_View(self.console, array, level, obj, self.MessageHandler, self.height, self.width)
                        self.console.clear()
                        if action == "EXIT":
                            keyReceived = "EXIT"
                            break
                        else:
                            action = action == True

                    elif keyReceived == "INTERACT":
                        action = True
                        objRow = obj.row
                        objCol = obj.col
                        if not level.Tiles[objRow][objCol].interact(obj.Object):
                            self.MessageHandler.push(obj.getName()+" waited...")

                    elif keyReceived in ["1","2","3","4","5","6","7"]:
                        skillKey = keyReceived
                        skillLvl = obj.Object.skillLevels[skillKey]
                        skill = obj.Object.skills[skillKey]
                        if skill.range == 0:
                            action = skill(obj.Object, obj.row, obj.col, skillLvl)

                    elif keyReceived in ["9","0"]:
                        if keyReceived == "9":
                            scroll = "leftScroll"
                        if keyReceived == "0":
                            scroll = "rightScroll"
                        if not hasattr(obj.Object, scroll) or getattr(obj.Object, scroll) == None:
                            continue

                        scrollItem = getattr(obj.Object, scroll)
                        if scrollItem.spell.range > 0:
                            continue
                        
                        self.MessageHandler.push(obj.getName() + " cast " + scrollItem.getName())
                        if scrollItem.cast(obj.Object, obj.row, obj.col):
                            obj.Object.unequip(scroll)
                            obj.Object.items.pop(-1)
                            action = True
                        else:
                            self.MessageHandler.pop()

                    elif keyReceived == "STOOD_STILL":
                        action = False
                    else:
                        action=True

                    if obj.isPlayerControlled():
                        self.updateDisplay(obj)
                    
                    if self.levelList.getLevel() != level:
                        return True
                else:
                    action = True
                if self.thePlayer.health <= 0:
                    keyReceived = "EXIT"
                if keyReceived == "EXIT":
                    break
            if keyReceived == "EXIT":
                break

        self.turn+=1
        if keyReceived == "EXIT":
            return False
        return True


game = Game()
if game.loadRequest == True:
    game = load(game)
gameLoopStart(game)
