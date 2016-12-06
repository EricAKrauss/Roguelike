from Constants import *

class Feature:
    def interact(self, Actor):
        return False

    def isActor(self):
        return False

    def isAlly(self):
        return False

    def isAlive(self):
        return False

    def isObstacle(self):
        return False

    def blocksSight(self):
        return False

    def isPlayerControlled(self):
        return False

    def getAction(self):
        return False

    def getInitiative(self):
        return 3

    def getInfo(self):
        return ""

    def getName(self):
        if hasattr(self, "name"):
            return self.name
        else:
            return ""

    def getChar(self):
        if hasattr(self, "char"):
            return self.char
        else:
            return ''

    def getColor(self):
        if not hasattr(self, "color"):
            return COLOR_DEFAULT
        else:
            return self.color
