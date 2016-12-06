from Constants import *

class Messages:
    def __init__(self):
        self.messages = []
        self.messageLimit = 1000
        self.retrieveLimit= 20

    def push(self, string):
        self.messages.insert(0, str(string))
        if len(self.messages) > self.messageLimit:
            self.messages.pop(-1)

    def insert(self, string, index):
        self.messages.insert(index, str(string))
        if len(self.messages) > self.messageLimit:
            self.messages.pop(-1)

    def retrieve(self, count=-1):
        if count == -1:
            count = self.retrieveLimit
        
        outStrings = []
        for string in range(min(count, len(self.messages))):
            outStrings.append(self.messages[string])
        return outStrings

    def pop(self, index=0):
        if index >= len(self.messages):
            return False
        if index < 0 and abs(index)-1 >= len(self.messages):
            return False
        self.messages.pop(index)

    
