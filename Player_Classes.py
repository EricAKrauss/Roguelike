from Player import *
from Item import *
from Items.Consumables import *
from Items.Armors import *
from Items.Weapons import *
from Effects import *
from Abilities import *
from QuadrantTheory import getAdjSpaces

baseSkillLevels = {
            "1":0,
            "2":0,
            "3":0,
            "4":0,
            "5":0,
            "6":0,
            "7":0
            }

class Fighter():
    def genEquipment(self):
        newItem = Longsword
        newItem = newItem(self.level)
        self.equip(newItem)

        newItem = Wooden_Shield
        newItem = newItem(self.level)
        self.equip(newItem)

        newItem = Leather_Shirt
        newItem = newItem(self.level)
        self.equip(newItem)

        newItem = Iron_Helm
        newItem = newItem(self.level)
        self.equip(newItem)

        newItem = GreenHerb
        self.items.append(newItem())
        self.items.append(newItem())

    def onSpawn(self):        
        self.baseHealth = 300
        self.health = self.baseHealth
        self.healthCurve = 0.50
        self.level = 1
        self.skills = {
            "1":Charge,
            "2":Mighty_Blow,
            "3":Cleave,
            "4":Intimidate,
            "5":Block,
            "6":Rending_Blow,
            "7":Ready_for_Battle
            }
        self.skillLevels = baseSkillLevels

class Fencer():
    def genEquipment(self):
        newItem = Longsword
        newItem = newItem(self.level)
        self.equip(newItem)

        newItem = Dagger
        newItem = newItem(self.level)
        self.equip(newItem)

        newItem = Leather_Shirt
        newItem = newItem(self.level)
        self.equip(newItem)

        newItem = Leather_Helm
        newItem = newItem(self.level)
        self.equip(newItem)

        newItem = GreenHerb
        self.items.append(newItem())
        self.items.append(newItem())

    def onSpawn(self):        
        self.baseHealth = 300
        self.health = self.baseHealth
        self.healthCurve = 0.55
        self.level = 1
        self.skills = {
            "1":Charge,
            "2":Hemorrhage,
            "3":Flurry_of_Blows,
            "4":Intimidate,
            "5":Counter,
            "6":Rending_Blow,
            "7":Ready_for_Battle
            }
        self.skillLevels = baseSkillLevels

class Spellsword():
    def genEquipment(self):
        newItem = Greatsword
        newItem = newItem(self.level)
        self.equip(newItem)

        newItem = Tome
        newItem = newItem(self.level)
        self.equip(newItem)

        newItem = Cloth_Shirt
        newItem = newItem(self.level)
        self.equip(newItem)

        newItem = Leather_Helm
        newItem = newItem(self.level)
        self.equip(newItem)

        newItem = GreenHerb
        self.items.append(newItem())
        self.items.append(newItem())

    def onSpawn(self):        
        self.baseHealth = 275
        self.health = self.baseHealth
        self.healthCurve = 0.6
        self.level = 1
        self.skills = {
            "1":Charge,
            "2":Shocking_Grasp,
            "3":Fireball,
            "4":Lightning_Bolt,
            "5":Block,
            "6":Rending_Blow,
            "7":Ready_for_Battle
            }
        self.skillLevels = baseSkillLevels

class Rogue():
    def genEquipment(self):
        newItem = Dagger
        newItem = newItem(self.level)
        self.equip(newItem)

        newItem = Dagger
        newItem = newItem(self.level)
        self.equip(newItem)

        newItem = Leather_Shirt
        newItem = newItem(self.level)
        self.equip(newItem)

        newItem = Leather_Helm
        newItem = newItem(self.level)
        self.equip(newItem)

        newItem = GreenHerb
        self.items.append(newItem())
        self.items.append(newItem())

    def onSpawn(self):
        self.baseHealth = 250
        self.health = self.baseHealth
        self.healthCurve = 0.75
        self.level = 1
        self.skills = {
            "1":Stealth,
            "2":Hemorrhage,
            "3":Flurry_of_Blows,
            "4":Knife_Toss,
            "5":Counter,
            "6":Smoke_Bomb,
            "7":Already_Dead
            }
        self.skillLevels = baseSkillLevels

class Mage():
    def genEquipment(self):
        newItem = Staff
        newItem = newItem(self.level)
        self.equip(newItem)

        newItem = Tome
        newItem = newItem(self.level)
        self.equip(newItem)

        newItem = Cloth_Shirt
        newItem = newItem(self.level)
        self.equip(newItem)

        newItem = Cloth_Hat
        newItem = newItem(self.level)
        self.equip(newItem)

        newItem = GreenHerb
        self.items.append(newItem())
        self.items.append(newItem())

    def onSpawn(self):
        self.baseHealth = 250
        self.health = self.baseHealth
        self.healthCurve = 0.75
        self.level = 1
        self.skills = {
            "1":Blink,
            "2":Shocking_Grasp,
            "3":Fireball,
            "4":Lightning_Bolt,
            "5":Wall_of_Force,
            "6":Flash_Freeze,
            "7":Arcane_Reservoir
            }

        self.skillLevels = baseSkillLevels

class Trickster():
    def genEquipment(self):
        newItem = Longsword
        newItem = newItem(self.level)
        self.equip(newItem)

        newItem = Wand
        newItem = newItem(self.level)
        self.equip(newItem)

        newItem = Cloth_Shirt
        newItem = newItem(self.level)
        self.equip(newItem)

        newItem = Cloth_Hat
        newItem = newItem(self.level)
        self.equip(newItem)

        newItem = GreenHerb
        self.items.append(newItem())
        self.items.append(newItem())

    def onSpawn(self):
        self.baseHealth = 250
        self.health = self.baseHealth
        self.healthCurve = 0.75
        self.level = 1
        self.skills = {
            "1":Stealth,
            "2":Shocking_Grasp,
            "3":Flurry_of_Blows,
            "4":Lightning_Bolt,
            "5":Smoke_Bomb,
            "6":Flash_Freeze,
            "7":Arcane_Reservoir
            }

        self.skillLevels = baseSkillLevels

ClassList = ["Mage", "Fighter", "Rogue"]
Classes = {"Mage":Mage, "Fighter":Fighter, "Rogue":Rogue,
           "Spellsword":Spellsword, "Fencer":Fencer, "Trickster":Trickster}
