import random
from LevelTypes import *
from DrunkardsWalk import *
from Wilderness import *
from QuadrantTheory import *
from LevelTypes.Decorations import *
import Enemies.Goblins
import Enemies.Vermin
import Enemies.Undead
import Enemies.Bandits

class Sewer(Level.Level):
    def onInit(self):
        self.name = "B: Rank Sewer"
        self.args = [
        random.randrange(4, 6), ##Width
        random.randrange(4, 6), ##Height
        4,                      ##MinRoomSize
        7,                      ##MaxRoomSize
        3,                      ##avgRoomCnx
        3                       ##avgEnemies
        ]
        self.enemyList = Enemies.Vermin.enemyList
        self.eliteList = Enemies.Vermin.eliteList
        self.decorList = [Pile_of_Bones, Sewer_Grate, Statue]        

        self.textSpace = "Muddy stone floor\n"
        self.textWall =  "Grimy stone wall\n"

class Crypt(Level.Level):
    def onInit(self):
        self.name = "B: Dark Crypt"
        self.args = [
        random.randrange(2, 4), ##Width
        random.randrange(2, 5), ##Height
        5,                      ##MinRoomSize
        11,                      ##MaxRoomSize
        2,                      ##avgRoomCnx
        2                       ##avgEnemies
        ]
        self.enemyList = Enemies.Undead.enemyList
        self.eliteList = Enemies.Undead.eliteList
        self.decorList = [Ritual_Circle, Altar, Pile_of_Bones]
        
        self.textSpace = "Ornate mosaic floor\n"
        self.textWall =  "Ornate stone wall\n"

class Tower(Level.Level):
    def onInit(self):
        self.name = "A: Sacked Tower"
        self.args = [
            random.randrange(3,5), ##Width
            random.randrange(3,5)  ##Height
            ]
        self.enemyList = Enemies.Bandits.enemyList
        self.eliteList = Enemies.Bandits.eliteList
        self.decorList = [Table, Weapon_Rack, Firepit]
        self.textSpace = "Dusty stone floor\n"
        self.textWall =  "Cracked stone wall\n"

class Wild(Level.Level):
    def onInit(self):
        self.name = "B: Forest"
        size = random.randrange(6, 10)
        self.args = [
            size,
            size
            ]
        if rand(2) == 0:
            self.enemyList = Enemies.Goblins.enemyList
            self.eliteList = Enemies.Goblins.eliteList
        else:
            self.enemyList = Enemies.Bandits.enemyList
            self.eliteList = Enemies.Bandits.eliteList
            
        self.decorList = [Table, Firepit, Weapon_Rack]
        
        self.textSpace = "ground, covered in leaves\n"
        self.textWall =  "Bricks\n"
        self.maze = Wilderness(self.inSeed, self.args[0], self.args[1], TREE).maze
        
class Cave(Level.Level):    
    def onInit(self):
        self.name = "A: Sacked Tower"
        self.args = [
            random.randrange(4,7), ##Width
            random.randrange(4,7)  ##Height
            ]
        features = min(self.args)+1
        self.enemyList = Enemies.Goblins.enemyList
        self.eliteList = Enemies.Goblins.eliteList
        self.decorList = [Pile_of_Bones, Table, Firepit]
        
        self.textSpace = "dirt floor\n"
        self.textWall =  "Sharp, wall of bedrock\n"
        self.maze = GenLevel(self.inSeed, self.args[0], self.args[1], 3)

levelTypes = [Tower, Sewer, Cave, Crypt, Wild]
##levelTypes = [Tower]
