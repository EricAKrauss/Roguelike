from Object import *
from Player import *
from Feature import *

import DrawController

class StairDown(Feature):
    def __init__(self, name, R, C, level):
        self.Object = None
        self.name = "Stairs"
        self.moveCost = 1
        self.row = R
        self.col = C
        self.ID = -1
        self.pLevel = level

    def getInfo(self):
        return "Stairs leading deeper\n"
    
    def interact(self, Actor):
        if isinstance(Actor, Player):
            if Actor.pObject.row == self.row:
                if Actor.pObject.col == self.col:
                    console = self.pLevel.gameState.console
                    if DrawController.UI_Poll_Yes_or_No(console, "Use stairs?"):
                        self.pLevel.levelManager.nextLevel()

class StairUp(Feature):
    def __init__(self, name, R, C, level):
        self.Object = None
        self.name = "Stairs"
        self.row = R
        self.col = C
        self.moveCost = 1
        self.ID = -1
        self.pLevel = level

    def getInfo(self):
        return "Stairs leading back towards the entrance\n"
    
    def interact(self, Actor):
        if isinstance(Actor, Player):
            if Actor.pObject.row == self.row:
                if Actor.pObject.col == self.col:
                    console = self.pLevel.gameState.console
                    if DrawController.UI_Poll_Yes_or_No(console, "Use stairs?"):
                        self.pLevel.levelManager.prevLevel()

##bill = StairUp("Bill", 0, 0, None)
