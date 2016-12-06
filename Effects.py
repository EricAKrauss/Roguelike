class Invisible:
    def __init__(self, duration):
        self.duration = duration+1

    def update(self, actor):
        actor.visible = False
        self.duration -= 1
        if self.duration == 0:
            actor.visible = True
        
    def isActive(self):
        if self.duration == 0:
            return False
        return True

class Death:
    def __init__(self, duration):
        self.duration = duration+1

    def update(self, actor):
        self.duration -= 1
        if self.duration == 0:
            actor.health = 0
            actor.die()

    def isActive(self):
        if self.duration == 0:
            return False
        return True

class TemporaryHP:
    def __init__(self, actor, duration, health):
        self.duration = duration+1
        self.health = health
        actor.healthTemp += health

    def update(self, actor):
        self.duration -= 1
        if self.duration == 0:
            actor.healthTemp -= self.health

    def isActive(self):
        if self.duration == 0:
            return False
        return True

class TemporaryPwr:
    def __init__(self, duration, power):
        self.duration = duration+1
        self.power = power

    def update(self, actor):
        self.duration -= 1
        actor.power += self.power

    def isActive(self):
        if self.duration == 0:
            return False
        return True

class ArmorReduction:
    def __init__(self, duration, amount):
        self.duration = duration+1
        self.amount = amount

    def update(self, actor):
        actor.armorVal -= self.amount
        self.duration -= 1
        if self.duration == 0:
            actor.armorVal += self.amount
        
    def isActive(self):
        if self.duration == 0:
            return False
        return True

class Frozen:
    def __init__(self, duration):
        self.duration = duration+1

    def update(self, actor):
        actor.canMove = False
        self.duration -= 1
        if self.duration == 0:
            actor.canMove = True
        
    def isActive(self):
        if self.duration == 0:
            return False
        return True

class Blocking:
    def __init__(self, duration):
        self.duration = duration+1

    def update(self, actor):
        actor.blocking = True
        self.duration -= 1
        if self.duration == 0:
            actor.blocking = False
        
    def isActive(self):
        if self.duration == 0:
            return False
        return True

class Countering:
    def __init__(self, duration):
        self.duration = duration+1

    def update(self, actor):
        actor.countering = True
        self.duration -= 1
        if self.duration == 0:
            actor.countering = False
        
    def isActive(self):
        if self.duration == 0:
            return False
        return True
    
class MindSlave:
    def __init__(self, duration):
        self.duration = duration+1

    def update(self, actor):
        actor.playerControlled = True
        self.duration -= 1
        if self.duration == 0:
            actor.playerControlled = False
        
    def isActive(self):
        if self.duration == 0:
            return False
        return True

class Terror:
    def __init__(self, duration):
        self.duration = duration+1

    def update(self, actor):
        actor.isAfraid = True
        self.duration -= 1
        if self.duration == 0:
            actor.isAfraid = actor.getAfraid()
        
    def isActive(self):
        if self.duration == 0:
            return False
        return True

class DoT:
    def __init__(self, dur, dmg):
        self.duration = dur+1
        self.damage = dmg

    def update(self, actor):
        actor.modHealth(-self.damage)
        self.duration -= 1
        
    def isActive(self):
        if self.duration == 0:
            return False
        return True
