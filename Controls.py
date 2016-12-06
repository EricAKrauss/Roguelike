import tdl

def getInput(inpList=None):
    while True:
        key = tdl.event.keyWait()
        if inpList == None:
            return key
        
        if key.char != '':
            if key.char in inpList:
                return key.char

        else:
            if key.key == "F4":
                if key.alt == True:
                    return "EXIT"
