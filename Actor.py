from random import randrange as rand
from math import floor, ceil
from Constants import *
from Controls import *
##from Player import *

class Actor:
    def __init__(self, name):
        self.char = '@'
        self.color= COLOR_PLAYER
        self.name = name

        self.level = 1
        self.exp = 0
        self.expNext=100
        self.skillPoints = 3

        self.recalcMax = 0
        self.recalcTimer=self.recalcMax
        self.playerControlled = True
        self.visible = True
        self.canMove = True
        self.invertColor = False
        self.blocking = False
        self.countering=False
        self.sightDist = 8
        self.initiative = 3

        self.effects = []
        self.hitEffects = []
        self.baseHealth = 250
        self.healthCurve = 1.25
        self.health = 100
        self.healthMax=100
        self.healthTemp = 0
        self.items = []
        self.gold = 0

        self.arrows = 0
        self.range = 1
        self.power = 1
        self.dodge = 0
        self.armorVal = 0
        self.accuracy = 0
        self.armorPen = 0

        self.rightHand =None
        self.leftHand = None
        self.armor = None
        self.helmet= None
        self.rightRing =None
        self.leftRing = None
        self.necklace = None
        self.leftScroll=None
        self.rightScroll=None

        if hasattr(self, "genEquipment"):
            self.genEquipment()

        if hasattr(self, "onSpawn"):
            self.onSpawn()
    
        self.pObject = None
        self.deriveStats()
        self.health = self.healthMax
    
    def blocksSight(self):
        return False

    def isActor(self):
        return True

    def isObstacle(self):
        if self.health > 0:
            return True
        return False

    def update(self):
        self.invertColor = False
        self.armorVal = 0
        self.deriveStats()

        if self.healthTemp < 0:
            self.healthTemp =0
        
        i = 0
        while i < len(self.effects):
            effect = self.effects.pop(0)
            effect.update(self)
            if effect.isActive():
                self.effects.append(effect)
            i+= 1

        if hasattr(self, "onUpdate"):
            self.onUpdate()

    def modHealth(self, difHP, Actor=None):
        if difHP < 0:    
            if self.blocking:
                self.blocking = False
                self.pObject.pLevel.messageSys.push(self.getName()+" blocked "+Actor.getName()+"'s attack")
                return False
            if self.countering:
                self.countering = False
                self.pObject.pLevel.messageSys.push(self.getName()+" blocked "+Actor.getName()+"'s attack")
                Actor.getAttacked(self)

            while self.healthTemp > 0 and difHP < 0:
                difHP += 1
                self.healthTemp -= 1

            self.invertColor = True
        self.health += difHP
        if self.health > self.healthMax:
            self.health = self.healthMax

        if hasattr(self, "onModHealth"):
            self.onModHealth(difHP, Actor)
    
        if self.health <= 0:
            if Actor != None:
                self.pObject.pLevel.messageSys.push(self.getName()+" was killed by "+Actor.getName())
            if hasattr(self, "die"):
                self.die(Actor)

        return True

    def unequip(self, slot):
        item = None
        if slot == "Helmet":
            item = "helmet"
        if slot == "Armor":
            item = "armor"
        if slot == "Right Hand":
            item = "rightHand"
        if slot == "Left Hand":
            item = "leftHand"
        if slot == "Right Ring":
            item = "rightRing"
        if slot == "Left Ring":
            item = "leftRing"
        if slot == "Necklace":
            item = "necklace"
        if slot == "Left Scroll":
            item = "leftScroll"
        if slot == "Right Scroll":
            item = "rightScroll"
        if item == None:
            if hasattr(self, slot):
                item = slot

        if item != None:
            outItem = getattr(self, item)
            if outItem != None:
                setattr(self, item, None)
                self.items.append(outItem)

    def equip(self, item):
        if not item.equippable:
            return False
        if item.type == "1H":
            if self.rightHand == None:
                self.rightHand = item
                self.deriveStats()
                return True
            elif self.leftHand == None and self.rightHand.type != "2H":
                self.leftHand = item
                self.deriveStats()
                return True
        if item.type == "2H":
            if self.leftHand == None or self.leftHand.type == "0H":
                if self.rightHand == None:
                    self.rightHand = item
                    self.deriveStats()
                    return True
        if item.type == "0H":
            if self.leftHand == None:
                self.leftHand = item
                self.deriveStats()
                return True
        if item.type == "helmet":
            if self.helmet == None:
                self.helmet = item
                self.deriveStats()
                return True
        if item.type == "armor":
            if self.armor == None:
                self.armor = item
                self.deriveStats()
                return True
        if item.type == "scroll":
            if self.rightScroll == None:
                self.rightScroll = item
                self.deriveStats()
                return True
            elif self.leftScroll == None:
                self.leftScroll = item
                self.deriveStats()
                return True
        
        return False

    def userInput(self):
        skillNums  = "123456790"
        key = getInput("wasSLdmicvfek"+skillNums)
        dirs = {"w":0, "d":1, "s":2, "a":3}
        if (key == "EXIT"):
            return key
        if key == 'i':
            return "INVENTORY"
        if key in "wasd":
            if not self.move(dirs[key]):
                return "STOOD_STILL"
        if key == 'c':
            return "CHARACTER"
        if key == 'm':
            return "MAP"
        if key == 'v':
            return "VIEW"
        if key == 'f':
            return "FIGHT"
        if key == 'e':
            return "INTERACT"
        if key == 'k':
            return "SKILLS"
        if key == 'S':
            return "SAVE"
        if key == "L":
            return "LOAD"
            
        return key

    def canThrow(self):
        if self.leftHand != None:
            if self.leftHand.throwable:
                return "Left Hand"
        if self.rightHand !=None:
            if self.rightHand.throwable:
                return "Right Hand"
        return None

    def move(self, direction):
        if not self.canMove:
            return False
        loc = [self.pObject.row, self.pObject.col]
        moved = False
        if direction == 0:
            moved = self.pObject.move(-1, 0)
        if direction == 1:
            moved = self.pObject.move(0, 1)
        if direction == 2:
            moved = self.pObject.move(1, 0)
        if direction == 3:
            moved = self.pObject.move(0, -1)

        if loc != [self.pObject.row, self.pObject.col]:
            self.pObject.pLevel.updateSight(self.sightDist)
            player_objs = []
            if self.playerControlled:
                for obj in self.pObject.pLevel.Objects.values():
                    if obj.isPlayerControlled():
                        player_objs.append( (obj.row, obj.col) )

                self.pObject.pLevel.djikstra_Player = self.pObject.pLevel.formDjikstra(player_objs)
                self.pObject.pLevel.djikstra_Player_Away = self.pObject.pLevel.transformMap(self.pObject.pLevel.djikstra_Player, -1.5, loc)

        return moved

    def getWeaponEffects(self):
        effects = self.hitEffects
        weaps = self.getWeapons()
        for weap in weaps:
            if hasattr(weap, "hitEffects"):
                effects.append(*weap.hitEffects)
        return effects

    def getWeapons(self):
        weapons = []
        if self.rightHand != None:
            weapons.append(self.rightHand)
        if self.leftHand !=None:
            weapons.append(self.leftHand)
        return weapons

    def getMagPower(self):
        pwr = 0
        weapons = self.getWeapons()
        
        for weapon in weapons:
            if hasattr(weapon, "magPower"):
                pwr += weapon.magPower
        
        return int(abs(pwr))

    def getPower(self):
        pwr = 0
        weapons = self.getWeapons()
        addPower = False
        
        for weapon in weapons:
            pwr += weapon.power
            if weapon.addPower:
                addPower = True

        if len(weapons) == 0 or addPower:
            pwr += self.power        
        return int(abs(pwr))

    def getArmor(self):
        armor = self.armorVal
        slots = ["rightHand", "leftHand", "armor", "helmet"]
        for slot in slots:
            item = getattr(self, slot)
            if item != None:
                if hasattr(item, "armorVal"):
                    armor+= item.armorVal
        return armor

    def getArmorPen(self):
        armorPen = 0
        slots = ["rightHand", "leftHand", "leftRing", "rightRing", "necklace"]
        for slot in slots:
            item = getattr(self, slot)
            if item != None:
                if hasattr(item, "armorPen"):
                    armorPen+= item.armorPen
        return armorPen

    def getAccuracy(self):
        accuracy = 0
        slots = ["helmet", "armor", "rightHand", "leftHand", "rightRing", "leftRing", "necklace"]
        for slot in slots:
            item = getattr(self, slot)
            if item != None:
                if hasattr(item, "accuracy"):
                    accuracy+= item.accuracy

        accuracy = min(50, accuracy)
        accuracy = max(-10, accuracy)
        return accuracy

    def getWeight(self):
        weight = 0
        slots = ["helmet", "armor", "rightHand", "leftHand", "rightRing", "leftRing", "necklace"]
        for slot in slots:
            item = getattr(self, slot)
            if item != None:
                if hasattr(item, "weight"):
                    weight+= item.weight
        return weight

    def getDodge(self):
        weight = self.getWeight()
        dodge = 75 - weight
        dodge = min(50, dodge)
        dodge = max(-10, dodge)
        return dodge

    def takeDamage(self, damage, magic=False):
        if not magic:
            armor = min(90, (100 - self.getArmor()))
            armorModifier = armor/100
        if magic:
            armorModifier = 1

        enemyPower = ceil(damage*armorModifier)
        self.modHealth(-enemyPower)

        messager = self.pObject.pLevel.messageSys

    def getAttacked(self, Actor, dmg=None, magic=False, canMiss=True):
        hitNum = rand(100)
        if canMiss:
            target = 80 - Actor.getAccuracy()
        else:
            target = 80 - 90
        target += self.getDodge()
        target = min(90, target)
        target = max(25, target)

        messager = self.pObject.pLevel.messageSys
        if hitNum < target:
            outString = Actor.getName()+" attacked "
            if dmg == None:
                enemyPower = Actor.getPower()
            else:
                enemyPower = dmg
                
            armor = min(90, (100 - max(0, self.getArmor()-Actor.getArmorPen())))
            armorModifier = armor/100

            if magic:
                armorModifier = 1

            msgs = len(messager.messages)
            enemyPower = ceil(enemyPower*armorModifier)
            if self.modHealth(-enemyPower, Actor):
                outString+= self.getName()+" for "+str(enemyPower)
                difMsgs = len(messager.messages)-msgs
                if difMsgs == 0:
                    messager.push(outString)
                else:
                    messager.insert(outString, difMsgs)
                

            for effect in Actor.getWeaponEffects():
                args = []
                if len(effect) == 3:
                    for arg in effect[2]:
                        args.append(eval(arg))
                eval(effect[1]).effects.append(effect[0](*args))
                
        else:
            outString = Actor.getName()+" missed "
            outString+= self.getName()
            messager.push(outString)

    def interact(self, Actor):
        if not Actor.isAlly(self):
            self.getAttacked(Actor)
            return True
        else:
            return False

    def getInitiative(self):
        return min(10, self.initiative)

    def getChar(self):
        return self.char

    def getColor(self):
        if not self.visible:
            return COLOR_FOW
        return self.color

    def getName(self):
        return self.name
