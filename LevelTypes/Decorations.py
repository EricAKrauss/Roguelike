from Feature import *

class Altar(Feature):
    def __init__(self):
        self.char = DECORATION
        self.name = "Altar"
    
    def isObstacle(self):
        return True

    def getInfo(self):
        return "A blood-stained altar"

class Statue(Feature):
    def __init__(self):
        self.char = DECORATION
        self.name = "Statue"

    def getInfo(self):
        return "A decorative statue"

    def isObstacle(self):
        return True

class Weapon_Rack(Feature):
    def __init__(self):
        self.char = DECORATION
        self.name = "Table"

    def getInfo(self):
        return "A near-empty rack of\n  crude, rusty weapons"

    def isObstacle(self):
        return True

class Table(Feature):
    def __init__(self):
        self.char = DECORATION
        self.name = "Table"

    def getInfo(self):
        return "A table covered in\n scraps of food"

    def isObstacle(self):
        return True

class Firepit(Feature):
    def __init__(self):
        self.char = DECORATION
        self.name = "Ritual Circle"
        
    def getInfo(self):
        return "Smoldering ashes suggest\n a recent fire"

class Ritual_Circle(Feature):
    def __init__(self):
        self.char = DECORATION
        self.name = "Ritual Circle"
        
    def getInfo(self):
        return "Blood-soaked carvings form\n  a ritual circle on\n  the ground"

class Sewer_Grate(Feature):
    def __init__(self):
        self.char = DECORATION
        self.name = "Sewer Grate"
        
    def getInfo(self):
        return "A metal grate leads below"

class Pile_of_Bones(Feature):
    def __init__(self):
        self.char = DECORATION
        self.name = "Pile of Bones"
        
    def getInfo(self):
        return "A pile of bones lies scattered"
