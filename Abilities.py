from QuadrantTheory import getAdjSpaces
from copy import deepcopy
from math import ceil
from Object import Object
from Features.Features import *
from Effects import *


##          WIZARD ABILITIES

##teleport a long distance
def Blink(self, row, col, lvl=1, useCD=True):
    Blink_Stats(lvl, False)
    if lvl <= 0:
        return False
    if useCD and Blink.cd < Blink.cdMax:
        return False
    
    level = self.pObject.pLevel
    tile = level.Tiles[row][col]
    loc = [self.pObject.row, self.pObject.col]
    end = [row, col]
    line = level.getLine(loc, end)

    dist = Blink.range
    if len(line) - 1 > dist:
        return False
    if abs(loc[0]- end[0])+abs(loc[1]-end[1]) > dist:
        return False
    if tile.isObstacle():
        return False
    if tile.isActor():
        return False

    if useCD:
        Blink.cd = 0
    return self.pObject.setpos(row, col)

def Blink_Stats(lvl, useCD=True):
    self = Blink

    if useCD:
        self.cdMax = 11-2*(lvl-1)
        if not hasattr(self, "cd"):
            self.cd = self.cdMax
        else:
            self.cd += 1
        
    self.level = lvl
    self.range = 3 + lvl * 2
    self.desc= "Teleport "+str(self.range)+" spaces"
Blink.update = Blink_Stats

##turn an enemy to your will for a time
def Mindslave(self, row, col, lvl=1, useCD=True):
    Mindslave_Stats(lvl, False)
    if lvl <= 0:
        return False
    if useCD and Mindslave.cd < Mindslave.cdMax:
        return False
    
    level = self.pObject.pLevel
    loc = [self.pObject.row, self.pObject.col]
    end = [row, col]
    line = level.getLine(loc, end)
    if len(line) - 1 > lvl:
        return False
    if not level.Tiles[row][col].isActor():
        return False
    obj = level.Tiles[row][col].getActor()
    if obj.isAlly(self):
        return False
    obj.Object.effects.append(MindSlave(Mindslave.dur))
    if useCD:
        Mindslave.cd = 0
    return True

def Mindslave_Stats(lvl, useCD=True):
    self = Mindslave

    if useCD:
        self.cdMax = 11-2*(lvl-1)
        if not hasattr(self, "cd"):
            self.cd = self.cdMax
        else:
            self.cd += 1
    
    self.level = lvl
    self.range = lvl
    self.dur = 1+lvl*2
    self.desc= "Control an enemy within "+str(self.range)+ " spaces for "+str(self.dur)+" turns"
Mindslave.update = Mindslave_Stats

##Deal significant magic damage to a target in melee range
def Shocking_Grasp(self, row, col, lvl=1, useCD=True):
    Shocking_Grasp_Stats(lvl, False)
    if lvl <= 0:
        return False
    if useCD and Shocking_Grasp.cd < Shocking_Grasp.cdMax:
        return False
    
    level = self.pObject.pLevel
    loc = [self.pObject.row, self.pObject.col]
    end = [row, col]
    line = level.getLine(loc, end)
    if len(line) - 1 > 1:
        return False
    if not level.Tiles[row][col].isActor():
        return False
    obj = level.Tiles[row][col].getActor()
    if obj.isAlly(self):
        return False
    messager = self.pObject.pLevel.messageSys
    messager.push(self.getName()+" used Shocking Grasp")
    
    obj.Object.getAttacked(self, self.getMagPower() * (lvl + 1), magic=True)
    if useCD: Shocking_Grasp.cd = 0
    return True

def Shocking_Grasp_Stats(lvl, useCD=True):
    self = Shocking_Grasp

    if useCD:
        self.cdMax = 11-2*(lvl-1)
        if not hasattr(self, "cd"):
            self.cd = self.cdMax
        else:
            self.cd += 1
            
    self.level = lvl
    self.range = 1
    self.desc = "Deal significant magic damage to a target in melee range"
Shocking_Grasp.update = Shocking_Grasp_Stats

##Deal magic damage to targets in an area around a location
def Fireball(self, row, col, lvl=1, useCD=True):
    Fireball_Stats(lvl, False)
    if lvl <= 0:
        return False
    if useCD and Fireball.cd < Fireball.cdMax:
        return False

    level = self.pObject.pLevel
    loc = [self.pObject.row, self.pObject.col]
    end = [row, col]
    line = level.getLine(loc, end)
    if len(line) - 1 > Fireball.range:
        return False
    
    spots = [[row, col]]
    outSpots = [[row, col]]
    for i in range(Fireball.radius):
        for spot in spots:
            outSpots += getAdjSpaces(level.maze, spot[0], spot[1])
        spots = deepcopy(outSpots)
    
    idsHit = []
    targets = []
    hit = False
    for loc in outSpots:
        tile = level.Tiles[loc[0]][loc[1]]
        target = tile.getActor()
        if target != None and target.ID not in idsHit:
            idsHit.append(target.ID)
            targets.append(target)

    for t in targets:
        if not t.isAlly(self):
            hit = True
    if hit:
        for tar in targets:
            tar.Object.getAttacked(self, max(1, self.getMagPower()*(lvl/2)), True, True)
        if useCD: Fireball.cd = 0
        
    return hit

def Fireball_Stats(lvl, useCD=True):
    self = Fireball

    if useCD:
        self.cdMax = 11-2*(lvl-1)
        if not hasattr(self, "cd"):
            self.cd = self.cdMax
        else:
            self.cd += 1
        
    self.level = lvl
    self.radius= lvl
    self.desc = "Deal magic damage to targets in an area around a location"
    self.range = 4+self.level
Fireball.update = Fireball_Stats

##Deals magic damage to enemies in a line
def Lightning_Bolt(self, row, col, lvl=1, useCD=True):
    Lightning_Bolt_Stats(lvl, False)
    if lvl <= 0:
        return False
    if useCD and Lightning_Bolt.cd < Lightning_Bolt.cdMax:
        return False

    level = self.pObject.pLevel
    loc = [self.pObject.row, self.pObject.col]
    end = [row, col]
    line = level.getLine(loc, end)
    if len(line) - 1 > Lightning_Bolt.range:
        return False
    
    hit = False
    for spot in line:
        tile = level.Tiles[spot[0]][spot[1]]
        target = tile.getActor()
        if target != None and not target.isAlly(self):
            target.Object.getAttacked(self, max(1, self.getMagPower()*(lvl/2)), True, True)
            hit = True

    if useCD: Lightning_Bolt.cd = 0
    return hit

def Lightning_Bolt_Stats(lvl, useCD=True):
    self = Lightning_Bolt

    if useCD:
        self.cdMax = 11-2*(lvl-1)
        if not hasattr(self, "cd"):
            self.cd = self.cdMax
        else:
            self.cd += 1

    self.level = lvl
    self.range = 3+lvl*2
    self.desc = "Deals magic damage to enemies in a line of "+str(self.range)+" spaces"
Lightning_Bolt.update = Lightning_Bolt_Stats

def Wall_of_Force(self, row, col, lvl=1, useCD=True):
    Wall_of_Force_Stats(lvl, False)
    if lvl <= 0:
        return False
    if useCD and Wall_of_Force.cd < Wall_of_Force.cdMax:
        return False
    
    level = self.pObject.pLevel
    loc = [self.pObject.row, self.pObject.col]
    pR = loc[0]
    pC = loc[1]
    adjLocs = []
    end = [row, col]
    if loc == end:
        return False
    line = level.getLine(loc, end)
    if len(line) - 1 > 1:
        return False
    rRow = end[0] - loc[0]
    rCol = end[1] - loc[1]
    positions = [
     (pR - 1, pC - 1), (pR - 1, pC + 0), (pR - 1, pC + 1),
     (pR + 0, pC - 1),                   (pR + 0, pC + 1),
     (pR + 1, pC - 1), (pR + 1, pC + 0), (pR + 1, pC + 1)]
    hitPositions = []

    difR = row-pR
    difC = col-pC

    if lvl == 1:
        adjLocs = [(row, col)]
    if lvl == 2:
        adjLocs = getAdjSpaces(level.maze, row, col, None)
        adjLocs.append((row, col))
    if lvl == 3:
        adjLocs = []
        oppLocs = getAdjSpaces(level.maze, pR-difR, pC-difC, None)
        oppLocs.append((pR-difR, pC-difC))
        altLocs = getAdjSpaces(level.maze, pR, pC, None, True)
        for lc in altLocs:
            if lc not in oppLocs:
                adjLocs.append(lc)

    for spot in adjLocs:
        if spot in positions:
            hitPositions.append(spot)

    for pos in hitPositions:
        outR = pos[0]
        outC = pos[1]
        if level.Tiles[outR][outC].getActor() == None:
            newObject = Object("Wall of Force", outR, outC, level)
            newObject.setObject(TempWall(4+lvl))
            level.addNew(outR, outC, newObject)
        else:
            return False

    if useCD: Wall_of_Force.cd = 0
    return True

def Wall_of_Force_Stats(lvl, useCD=True):
    self = Wall_of_Force

    if useCD:
        self.cdMax = 11-2*(lvl-1)
        if not hasattr(self, "cd"):
            self.cd = self.cdMax
        else:
            self.cd += 1
    
    self.level = lvl
    if lvl <= 1:
        self.desc = "Create a wall on a tile for 5 turns"
    if lvl == 2:
        self.desc = "Create walls in a narrow arc for 6 turns"
    if lvl == 3:
        self.desc = "Create walls in a wide arc for 7 turns"
    self.range = 1
Wall_of_Force.update = Wall_of_Force_Stats

##Freeze the movements of a target
def Flash_Freeze(self, row, col, lvl=1, useCD=True):
    Flash_Freeze_Stats(lvl, False)
    if lvl <= 0:
        return False
    if useCD and Flash_Freeze.cd < Flash_Freeze.cdMax:
        return False
    
    level = self.pObject.pLevel
    loc = [self.pObject.row, self.pObject.col]
    end = [row, col]
    line = level.getLine(loc, end)
    if len(line) - 1 > lvl:
        return False
    if not level.Tiles[row][col].isActor():
        return False
    obj = level.Tiles[row][col].getActor()
    if obj.isAlly(self):
        return False
    obj.Object.effects.append(Frozen(Flash_Freeze.dur))
    if useCD:
        Flash_Freeze.cd = 0
    return True

def Flash_Freeze_Stats(lvl, useCD=True):
    self = Flash_Freeze

    if useCD:
        self.cdMax = 11-2*(lvl-1)
        if not hasattr(self, "cd"):
            self.cd = self.cdMax
        else:
            self.cd += 1
    
    self.level = lvl
    self.range = 1+lvl*2
    self.dur = 4+lvl
    self.desc= "Freeze the movements of a target within "+str(self.range)+ " spaces for "+str(self.dur)+" turns"
Flash_Freeze.update = Flash_Freeze_Stats

##Refresh cooldowns of other spells
def Arcane_Reservoir(self, row, col, lvl=1, useCD=True):
    Arcane_Reservoir_Stats(lvl, useCD)
    reset = False
    if lvl <= 0:
        return False
    if useCD and Arcane_Reservoir.cd < Arcane_Reservoir.cdMax:
        return False

    for skill in self.skills.values():
        reset = reset or skill.cd < skill.cdMax
        skill.cd = skill.cdMax
    Arcane_Reservoir.cd = 0
    return reset

def Arcane_Reservoir_Stats(lvl, useCD=True):
    self = Arcane_Reservoir

    if useCD:
        self.cdMax = 30
        if not hasattr(self, "cd"):
            self.cd = self.cdMax
        else:
            self.cd += 1
    
    self.level = lvl
    self.isUltimate = True
    self.range = 0
    self.desc= "Refreshes the cooldowns of all spells"
Arcane_Reservoir.update = Arcane_Reservoir_Stats

##          ROGUE ABILITIES

##Become invisible for a short while
def Stealth(self, row, col, lvl=1, useCD=True):
    Stealth_Stats(lvl, False)
    if lvl <= 0:
        return False
    if useCD and Stealth.cd < Stealth.cdMax:
        return False
    
    self.visible = False
    self.effects.append(Invisible(4 + lvl))
    if useCD: Stealth.cd = 0
    return True

def Stealth_Stats(lvl, useCD=True):
    self = Stealth

    if useCD:
        self.cdMax = 11-2*(lvl-1)
        if not hasattr(self, "cd"):
            self.cd = self.cdMax
        else:
            self.cd += 1
        
    self.level = lvl
    self.range = 0
    self.dur = 4+lvl
    self.desc = "Become invisible for "+str(self.dur)+" turns"
Stealth.update = Stealth_Stats

##Make an attack, if it deals damage, the target will suffer DoT
def Hemorrhage(self, row, col, lvl=1, useCD=True):
    Hemorrhage_Stats(lvl, False)
    if lvl <= 0:
        return False
    if useCD and Hemorrhage.cd < Hemorrhage.cdMax:
        return False
    
    level = self.pObject.pLevel
    loc = [self.pObject.row, self.pObject.col]
    end = [row, col]
    line = level.getLine(loc, end)
    if len(line) - 1 > 1:
        return False
    if not level.Tiles[row][col].isActor():
        return False
    obj = level.Tiles[row][col].getActor()
    if obj.isAlly(self):
        return False
    hp = obj.Object.health
    obj.Object.getAttacked(self)
    if obj.Object != None:
        if obj.Object.health < hp:
            obj.Object.effects.append(DoT(lvl, self.getPower()))

    if useCD: Hemorrhage.cd = 0
    return True

def Hemorrhage_Stats(lvl, useCD=True):
    self = Hemorrhage

    if useCD:
        self.cdMax = 11-2*(lvl-1)
        if not hasattr(self, "cd"):
            self.cd = self.cdMax
        else:
            self.cd += 1
        
    self.level = lvl
    self.dur = lvl
    self.range = 1
    self.desc = "Make an attack, if it deals damage, the target will bleed for "+str(self.dur)+" turns"
Hemorrhage.update = Hemorrhage_Stats

##Attack an enemy multiple times
def Flurry_of_Blows(self, row, col, lvl=1, useCD=True):
    Flurry_of_Blows_Stats(lvl, False)
    if lvl <= 0:
        return False
    if useCD and Flurry_of_Blows.cd < Flurry_of_Blows.cdMax:
        return False
    
    level = self.pObject.pLevel
    loc = [self.pObject.row, self.pObject.col]
    end = [row, col]
    line = level.getLine(loc, end)
    if len(line) - 1 > 1:
        return False
    if not level.Tiles[row][col].isActor():
        return False
    obj = level.Tiles[row][col].getActor()
    if obj.isAlly(self):
        return False
    for i in range(Flurry_of_Blows.count):
        if obj.isAlive():
            obj.Object.getAttacked(self)
    if useCD: Flurry_of_Blows.cd = 0
    return True

def Flurry_of_Blows_Stats(lvl, useCD=True):
    self = Flurry_of_Blows

    if useCD:
        self.cdMax = 11-2*(lvl-1)
        if not hasattr(self, "cd"):
            self.cd = self.cdMax
        else:
            self.cd += 1

    self.level = lvl
    self.range = 1
    self.count = 2+lvl
    self.desc = "Attack a target in melee range"
    if lvl > 0:
        self.desc += " "+str(self.count)+" times"
Flurry_of_Blows.update = Flurry_of_Blows_Stats

##Throw a knife to damage an enemy
def Knife_Toss(self, row, col, lvl=1, useCD=True):
    Knife_Toss_Stats(lvl, False)
    if useCD and Knife_Toss.cd < Knife_Toss.cdMax:
        return False
    
    if lvl <= 0:
        return False
    
    level = self.pObject.pLevel
    loc = [self.pObject.row, self.pObject.col]
    end = [row, col]
    line = level.getLine(loc, end)
    if len(line) - 1 > Knife_Toss.range:
        return False
    if not level.Tiles[row][col].isActor():
        return False
    obj = level.Tiles[row][col].getActor()
    if obj.isAlly(self):
        return False
    obj.Object.getAttacked(self, self.power*(lvl+1)/2)
    if useCD: Knife_Toss.cd = 0
    return True

def Knife_Toss_Stats(lvl, useCD=True):
    self = Knife_Toss

    if useCD:
        self.cdMax = 11-2*(lvl-1)
        if not hasattr(self, "cd"):
            self.cd = self.cdMax
        else:
            self.cd += 1

    self.level = lvl
    self.range = 3+lvl*2
    self.desc = "Throw a knife "+str(self.range)+" spaces"
Knife_Toss.update = Knife_Toss_Stats

##Counter the next attack
def Counter(self, row, col, lvl=1, useCD=True):
    Counter_Stats(lvl, False)
    if lvl <= 0:
        return False
    if useCD and Counter.cd < Counter.cdMax:
        return False

    self.blocking = True
    self.effects.append(Countering(Counter.dur))
    if useCD: Counter.cd = 0
    return True

def Counter_Stats(lvl, useCD=True):
    self =Counter

    if useCD:
        self.cdMax = 11-2*(lvl-1)
        if not hasattr(self, "cd"):
            self.cd = self.cdMax
        else:
            self.cd += 1
        
    self.level = lvl
    self.range = 0
    self.dur = lvl
    self.desc = "Counter the next attack for "+str(self.dur)+" turns"
    if lvl == 0:
        self.desc = "Counter the next attack"
Counter.update = Counter_Stats

##Create a short-lasting cloud of smoke
def Smoke_Bomb(self, row, col, lvl=1, useCD=True):
    Smoke_Bomb_Stats(lvl, False)
    if lvl <= 0:
        return False
    if useCD and Smoke_Bomb.cd < Smoke_Bomb.cdMax:
        return False
    
    level = self.pObject.pLevel
    row = self.pObject.row
    col = self.pObject.col
    spots = [[row, col]]
    outSpots = [[row, col]]
    for i in range(lvl):
        for spot in spots:
            outSpots += getAdjSpaces(level.maze, spot[0], spot[1])
        spots = deepcopy(outSpots)

    locsHit = []
    for loc in outSpots:
        if not loc in locsHit:
            locsHit.append(loc)
            newObject = Object("smoke", loc[0], loc[1], level)
            newObject.setObject(Smoke(lvl*2+1))
            level.addNew(loc[0], loc[1], newObject)

    if useCD: Smoke_Bomb.cd = 0
    return True

def Smoke_Bomb_Stats(lvl, useCD=True):
    self = Smoke_Bomb

    if useCD:
        self.cdMax = 11-2*(lvl-1)
        if not hasattr(self, "cd"):
            self.cd = self.cdMax
        else:
            self.cd += 1
        
    self.level = lvl
    self.range = 0
    self.radius = lvl
    self.dur = lvl*2+1
    self.desc = "Create a cloud of smoke for "+str(self.dur)+" turns"
Smoke_Bomb.update = Smoke_Bomb_Stats

##Target enemy dies in 7 turns
def Already_Dead(self, row, col, lvl=1, useCD=True):
    Already_Dead_Stats(lvl, False)
    if useCD and Already_Dead.cd < Already_Dead.cdMax:
        return False
    
    if lvl <= 0:
        return False
    
    level = self.pObject.pLevel
    loc = [self.pObject.row, self.pObject.col]
    end = [row, col]
    line = level.getLine(loc, end)
    if len(line) - 1 > Already_Dead.range:
        return False
    if not level.Tiles[row][col].isActor():
        return False
    obj = level.Tiles[row][col].getActor()
    if obj.isAlly(self):
        return False
    obj.Object.effects.append(Death(Already_Dead.dur))
    if useCD: Already_Dead.cd = 0
    return True

def Already_Dead_Stats(lvl, useCD=True):
    self = Already_Dead
    self.isUltimate = True

    if useCD:
        self.cdMax = 30
        if not hasattr(self, "cd"):
            self.cd = self.cdMax
        else:
            self.cd += 1

    self.level = lvl
    self.dur = 7
    self.desc = "Target enemy dies in 7 turns"
    self.range = 1
Already_Dead.update = Already_Dead_Stats

##          FIGHTER ABILITIES

##Travel a short distance and make an attack
def Charge(self, row, col, lvl=1, useCD=True):
    Charge_Stats(lvl, False)
    if lvl <= 0:
        return False
    if useCD and Charge.cd < Charge.cdMax:
        return False
    
    level = self.pObject.pLevel
    loc = [self.pObject.row, self.pObject.col]
    end = [row, col]
    line = level.getLine(loc, end)
    dist =  Charge.range
    if len(line) - 1 > dist:
        return False
    if len(line) - 1 <= 0:
        return False
    if abs(loc[0]- end[0])+abs(loc[1]-end[1]) > dist:
        return False
    move = not level.Tiles[line[1][0]][line[1][1]].isActor()
    self.pObject.setpos(line[1][0], line[1][1])
    if useCD: Charge.cd = 0
    if not move:
        return True
    if len(line) < 3:
        return True
    for i in range(2, len(line)):
        move = not level.Tiles[line[i][0]][line[i][1]].isActor()
        self.pObject.setpos(line[i][0], line[i][1])
        if not move:
            return True

    return True

def Charge_Stats(lvl, useCD=True):
    self = Charge

    if useCD:
        self.cdMax = 11-2*(lvl-1)
        if not hasattr(self, "cd"):
            self.cd = self.cdMax
        else:
            self.cd += 1
        
    self.level = lvl
    self.range = 1 + lvl * 2
    self.desc = "Travel "+str(self.range)+" spaces and make a melee attack"
Charge.update = Charge_Stats

##Attack a target and adjacent targets within reach
def Cleave(self, row, col, lvl=1, useCD=True):
    Cleave_Stats(lvl, False)
    if lvl <= 0:
        return False
    if useCD and Cleave.cd < Cleave.cdMax:
        return False
    
    level = self.pObject.pLevel
    loc = [self.pObject.row, self.pObject.col]
    pR = loc[0]
    pC = loc[1]
    end = [row, col]
    if loc == end:
        return False
    line = level.getLine(loc, end)
    if len(line) - 1 > 1:
        return False
    rRow = end[0] - loc[0]
    rCol = end[1] - loc[1]
    positions = [
     (pR - 1, pC - 1), (pR - 1, pC + 0), (pR - 1, pC + 1),
     (pR + 0, pC - 1),                   (pR + 0, pC + 1),
     (pR + 1, pC - 1), (pR + 1, pC + 0), (pR + 1, pC + 1)]
    hitPositions = []

    difR = row-pR
    difC = col-pC

    if lvl == 1:
        adjLocs = getAdjSpaces(level.maze, row, col, None)
        adjLocs.append((row, col))
    if lvl == 2:
        adjLocs = []
        oppLocs = getAdjSpaces(level.maze, pR-difR, pC-difC, None)
        oppLocs.append((pR-difR, pC-difC))
        altLocs = getAdjSpaces(level.maze, pR, pC, None, True)
        for lc in altLocs:
            if lc not in oppLocs:
                adjLocs.append(lc)
    if lvl == 3:
        adjLocs = getAdjSpaces(level.maze, pR, pC, None, True)

    for spot in adjLocs:
        if spot in positions:
            hitPositions.append(spot)

    for pos in hitPositions:
        self.pObject.fight(level, pos[0], pos[1])

    if useCD: Cleave.cd = 0
    return True

def Cleave_Stats(lvl, useCD=True):
    self = Cleave

    if useCD:
        self.cdMax = 11-2*(lvl-1)
        if not hasattr(self, "cd"):
            self.cd = self.cdMax
        else:
            self.cd += 1
    
    self.level = lvl
    if lvl <= 1:
        self.desc = "Attack a target and adjacent targets within reach"
    if lvl == 2:
        self.desc = "Attack a target and targets in a wide arc"
    if lvl == 3:
        self.desc = "Attack all targets within reach"
    self.range = 1
Cleave.update = Cleave_Stats

##Deal tremendous damage to a single target
def Mighty_Blow(self, row, col, lvl=1, useCD=True):
    Mighty_Blow_Stats(lvl, False)
    if lvl <= 0:
        return False
    if useCD and Mighty_Blow.cd < Mighty_Blow.cdMax:
        return False
    
    level = self.pObject.pLevel
    loc = [self.pObject.row, self.pObject.col]
    end = [row, col]
    line = level.getLine(loc, end)
    if len(line) - 1 > 1:
        return False
    if not level.Tiles[row][col].isActor():
        return False
    obj = level.Tiles[row][col].getActor()
    if obj.isAlly(self):
        return False
    obj.Object.getAttacked(self, self.getPower() * (lvl + 1))
    if useCD: Mighty_Blow.cd = 0
    return True

def Mighty_Blow_Stats(lvl, useCD=True):
    self = Mighty_Blow

    if useCD:
        self.cdMax = 11-2*(lvl-1)
        if not hasattr(self, "cd"):
            self.cd = self.cdMax
        else:
            self.cd += 1

    self.level = lvl
    self.desc = "Deal tremendous damage to a single target in melee range"
    self.range = 1
Mighty_Blow.update = Mighty_Blow_Stats

##Make an enemy afraid for a short time
def Intimidate(self, row, col, lvl=1, useCD=True):
    Intimidate_Stats(lvl, False)
    if useCD and Intimidate.cd < Intimidate.cdMax:
        return False
    
    if lvl <= 0:
        return False
    
    level = self.pObject.pLevel
    loc = [self.pObject.row, self.pObject.col]
    end = [row, col]
    line = level.getLine(loc, end)
    if len(line) - 1 > Intimidate.range:
        return False
    if not level.Tiles[row][col].isActor():
        return False
    obj = level.Tiles[row][col].getActor()
    if obj.isAlly(self):
        return False
    obj.Object.effects.append(Terror(Intimidate.dur))
    if useCD: Intimidate.cd = 0
    return True

def Intimidate_Stats(lvl, useCD=True):
    self = Intimidate

    if useCD:
        self.cdMax = 11-2*(lvl-1)
        if not hasattr(self, "cd"):
            self.cd = self.cdMax
        else:
            self.cd += 1

    self.level = lvl
    self.dur = 1+lvl*2
    self.desc = "Make an enemy afraid for "+str(self.dur)+" turns"
    self.range = 2+lvl
Intimidate.update = Intimidate_Stats

##Block the next attack
def Block(self, row, col, lvl=1, useCD=True):
    Block_Stats(lvl, False)
    if lvl <= 0:
        return False
    if useCD and Block.cd < Block.cdMax:
        return False

    self.blocking = True
    self.effects.append(Blocking(Block.dur))
    if useCD: Block.cd = 0
    return True

def Block_Stats(lvl, useCD=True):
    self = Block

    if useCD:
        self.cdMax = 11-2*(lvl-1)
        if not hasattr(self, "cd"):
            self.cd = self.cdMax
        else:
            self.cd += 1
        
    self.level = lvl
    self.range = 0
    self.dur = 2+lvl
    self.desc = "Block the next attack for "+str(self.dur)+" turns"
    if lvl == 0:
        self.desc = "Block the next attack"
Block.update = Block_Stats

##With an attack reduce target armor
def Rending_Blow(self, row, col, lvl=1, useCD=True):
    Rending_Blow_Stats(lvl, False)
    if lvl <= 0:
        return False
    if useCD and Rending_Blow.cd < Rending_Blow.cdMax:
        return False
    
    level = self.pObject.pLevel
    loc = [self.pObject.row, self.pObject.col]
    end = [row, col]
    line = level.getLine(loc, end)
    if len(line) - 1 > 1:
        return False
    if not level.Tiles[row][col].isActor():
        return False
    obj = level.Tiles[row][col].getActor()
    if obj.isAlly(self):
        return False
    hp = obj.Object.health
    obj.Object.getAttacked(self)
    if obj.Object != None:
        if obj.Object.health < hp:
            obj.Object.effects.append(ArmorReduction(Rending_Blow.dur, Rending_Blow.dmg))

    if useCD: Rending_Blow.cd = 0
    return True

def Rending_Blow_Stats(lvl, useCD=True):
    self = Rending_Blow

    if useCD:
        self.cdMax = 11-2*(lvl-1)
        if not hasattr(self, "cd"):
            self.cd = self.cdMax
        else:
            self.cd += 1
        
    self.level = lvl
    self.dur = 2+lvl
    self.dmg = 5+5*lvl
    self.range = 1
    self.desc = "With an attack reduce target armor by " +str(self.dmg)+" for "+str(self.dur)+" turns"
Rending_Blow.update = Rending_Blow_Stats

##Gain a shield of temporary health and a boost to power
def Ready_for_Battle(self, row, col, lvl=1, useCD=True):
    Ready_for_Battle_Stats(lvl, False)
    if lvl <= 0:
        return False
    if useCD and Ready_for_Battle.cd < Ready_for_Battle.cdMax:
        return False

    self.effects.append(TemporaryHP(self, 7, ceil(self.healthMax*.25)))
    self.effects.append(TemporaryPwr(7, ceil(self.power*.5)))
    return True

def Ready_for_Battle_Stats(lvl, useCD=True):
    self = Ready_for_Battle
    self.isUltimate = True

    if useCD:
        self.cdMax = 11-2*(lvl-1)
        if not hasattr(self, "cd"):
            self.cd = self.cdMax
        else:
            self.cd += 1
        
    self.level = lvl
    self.range = 0
    self.desc = "Boost power and health for 7 turns"
Ready_for_Battle.update = Ready_for_Battle_Stats
