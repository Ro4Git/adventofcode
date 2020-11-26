import copy 
import itertools
import time
from curses import wrapper

memSize = 10000000
verbose = False
programs = {}
verboseprint = print if verbose else lambda *a, **k: None

#parameter modes 
modes = []
for i in range(1000):
    modes.append([int(i % 10),int(i//10) % 10,int(i/100)]) 

#----------------
# main program class 
class Program:
    def __init__(self, input, name, code):
        temp = [] 
        for c in code:
            temp.append(int(c))
        for i in range(memSize):
            temp.append(0)
        self.program = temp
        self.adressableSize = len(self.program)
        self.memStart = len(code)
        self.name = name
        self.inputs = [input]
        self.execPointer = 0
        self.output = 0
        self.inputIndex = 0
        self.relativeBase = 0
        self.dispatchMap = [None,
                            self.opcode_Add,
                            self.opcode_Mul,
                            self.opcode_Write,
                            self.opcode_Output,
                            self.opcode_JumpT,
                            self.opcode_JumpF,
                            self.opcode_LessThan,
                            self.opcode_Equals,
                            self.opcode_RelativeBase]

    def reset(self):
        self.inputs = []
        self.execPointer = 0
        self.inputs = []
        self.output = 0
        self.inputIndex = 0
        self.relativeBase = 0

    def setMem(self,index,value):
        self.program[index] = int(value)

    def addInput(self, input):
        self.inputs.append(input)

    def resetInput(self, input):
        self.inputs = [input]
        self.inputIndex = 0

    def writeAdr(self, adr, value):
        self.program[adr] = value

    def decodeParam(self, mode, value):
        if (mode == 0):
            if value >= self.adressableSize:
                print("invalid read index {0}({1})".format(value,self.adressableSize))
            return int(self.program[value])
        elif (mode == 1):
            return int(value)
        elif (mode == 2):
            if self.relativeBase+value >= self.adressableSize:
                print("invalid read index {0}+{1}(max={2})".format(value, self.relativeBase+value,self.adressableSize))           
            return int(self.program[self.relativeBase + value])

    def decodeAdr(self, mode, value):
        if (mode == 0):
            return value
        elif (mode == 2):
            return int(self.relativeBase + value)            
        else:
            print("------- unenexpected param mode for address param({0})".format(mode))
            return int(value)
 
    #--------------------------------------------
    # opcode 1 : Add 
    def opcode_Add(self, inmodes):
        value1 = int(self.program[self.execPointer + 1])
        value2 = int(self.program[self.execPointer + 2])
        retAdr = int(self.program[self.execPointer + 3])

        value1 = self.decodeParam(inmodes[0],value1)
        value2 = self.decodeParam(inmodes[1],value2)
        retAdr = self.decodeAdr(inmodes[2], retAdr)

        verboseprint("Add {0}+{1} at Adr[{2}]".format(value1, value2 ,retAdr))

        self.writeAdr(retAdr, value1 + value2)
        return self.execPointer + 4

    #--------------------------------------------
    # opcode 2 : Mul 
    def opcode_Mul(self, inmodes):
        value1 = int(self.program[self.execPointer + 1])
        value2 = int(self.program[self.execPointer + 2])
        retAdr = int(self.program[self.execPointer + 3])
        value1 = self.decodeParam(inmodes[0],value1)
        value2 = self.decodeParam(inmodes[1],value2)   
        retAdr = self.decodeAdr(inmodes[2], retAdr)
        
        verboseprint("Mul {0}*{1} at Adr[{2}]".format(value1, value2 ,retAdr))
        
        self.writeAdr(retAdr, value1 * value2)
        
        return self.execPointer + 4

    #--------------------------------------------
    # opcode 3 : Write input
    def opcode_Write(self, inmodes):
        retAdr = int(self.program[self.execPointer + 1])
        retAdr = self.decodeAdr(inmodes[0], retAdr)

        verboseprint("Write input {0}".format(self.inputIndex))
        verboseprint("Write {0} at Adr[{1}]".format(self.inputs[self.inputIndex],retAdr))
        print("input " + str(self.inputIndex) + " = " + chr(self.inputs[self.inputIndex]))
        self.writeAdr(retAdr, self.inputs[self.inputIndex])
        self.inputIndex = self.inputIndex + 1
        return self.execPointer + 2

    #--------------------------------------------
    # opcode 4 : Output  
    def opcode_Output(self, inmodes):
        value1 = int(self.program[self.execPointer + 1])
        value1 = self.decodeParam(inmodes[0],value1)

        verboseprint("Output=>{0}".format(value1))
        self.output =  value1
        return self.execPointer + 2

    #--------------------------------------------
    # opcode 5 : Jump if true 
    def opcode_JumpT(self, inmodes):
        value1 = int(self.program[self.execPointer + 1])
        value2 = int(self.program[self.execPointer + 2])
        value1 = self.decodeParam(inmodes[0],value1)
        value2 = self.decodeParam(inmodes[1],value2)
        
        if value1 != 0:
            verboseprint("JumpT to [{1}] because ({0}!=0)".format(value1,value2))
            return value2
        else:
            verboseprint("No JumpT because ({0}==0)".format(value1,value2))
            return self.execPointer + 3

    #--------------------------------------------
    # opcode 6 : Jump if False 
    def opcode_JumpF(self, inmodes):
        value1 = int(self.program[self.execPointer + 1])
        value2 = int(self.program[self.execPointer + 2])
        value1 = self.decodeParam(inmodes[0],value1)
        value2 = self.decodeParam(inmodes[1],value2)
        
        if value1 == 0:
            verboseprint("JumpF to [{1}] because ({0}==0)".format(value1,value2))
            return value2
        else:
            verboseprint("No JumpF because ({0}!=0)".format(value1))
            return self.execPointer + 3        

    #--------------------------------------------
    # opcode 7 : Less than
    def opcode_LessThan(self, inmodes):
        value1 = int(self.program[self.execPointer + 1])
        value2 = int(self.program[self.execPointer + 2])
        retAdr = int(self.program[self.execPointer + 3])
        value1 = self.decodeParam(inmodes[0],value1)
        value2 = self.decodeParam(inmodes[1],value2)
        retAdr = self.decodeAdr(inmodes[2], retAdr)

        verboseprint("[{2}]= ({0}<{1})".format(value1,value2,retAdr))
        self.writeAdr(retAdr, int(value1 < value2))

        return self.execPointer + 4     

    #--------------------------------------------
    # opcode 8 : Equals
    def opcode_Equals(self, inmodes):
        value1 = int(self.program[self.execPointer + 1])
        value2 = int(self.program[self.execPointer + 2])
        retAdr = int(self.program[self.execPointer + 3])
        value1 = self.decodeParam(inmodes[0],value1)
        value2 = self.decodeParam(inmodes[1],value2)
        retAdr = self.decodeAdr(inmodes[2], retAdr)

        verboseprint("[{2}]= ({0}=={1})".format(value1,value2,retAdr))
        self.writeAdr(retAdr, int(value1 == value2))
        return self.execPointer + 4   

    #--------------------------------------------
    # opcode 9 : Sets relative base 
    def opcode_RelativeBase(self, inmodes):
        value1 = int(self.program[self.execPointer + 1])
        value1 = self.decodeParam(inmodes[0],value1)    

        verboseprint("relativeBase = {0} + {1}".format(self.relativeBase,value1))
        self.relativeBase = self.relativeBase + value1
        return self.execPointer + 2  


    # return value 
    # 1-9 - execptected opcode ( output = 4)
    # 99 - end of program
    # -1 - error 
    def decode_opcode(self):
        instruction = int(self.program[self.execPointer])
        parammodes = instruction//100
        opcode = instruction - (parammodes * 100)

        if (opcode>=1 and opcode<=9):
            self.execPointer = self.dispatchMap[opcode](modes[parammodes])
        elif opcode == 99: 
            if (verbose):
                print("End Of Program")
        else:
            print("unsupported opcode")
        return opcode  

    def execute_untiloutput(self):
        res = 0
        while (res!=4 and res!=99 and res!=-1): 
            res = self.decode_opcode()
        
        if (res == 4):
            return self.output
        else:
            return -1

    def execute_move(self, dir):
        res = 0
        self.resetInput(dir)
        while (res!=4 and res!=99 and res!=-1): 
            res = self.decode_opcode()
        
        if (res == 4):
            return self.output
        else:
            return -1

 
    def execute_untilhalt(self):
        res = 0
        while (res!=99 and res!=-1): 
            res = self.decode_opcode()
    
        return self.output

    def execute_cameraView(self):
        res = 0
        str = ""
        while (res!=99 and res!=-1): 
            res = self.decode_opcode()
        
            if (res == 4):
                str += chr(self.output)
        return str

def add(v,w):
    x,y = v
    X,Y = w
    return (x+X, y+Y)

def minPos(v,w):
    x,y = v
    X,Y = w
    return (min(x,X), min(y,Y))

def maxPos(v,w):
    x,y = v
    X,Y = w
    return (max(x,X), max(y,Y))


initial_numbers= []
f = open('input_day17.txt','r')
for line in f:
    initial_numbers = line.split(",")


def test_program(stdscr):

    start_time = time.time()
    width = 55
    height = 37
    buffer = [0] * width * height
    distbuffer = [0] * width * height

    # Only four movement commands are understood: 
    # north (1), south (2), west (3), and east (4). 
    dirs = [(0,0),(0,-1),(0,1),(-1,0),(1,0)]
    masks = [0,2,4,8,16]
    nextDirRight = [0,4,3,1,2]
    nextDirLeft = [0,3,4,2,1]

    # 0 : void
    # 1 : scaffold 
    # 2 : scaffold intersection
    # 3,4,5,6 robot dir
    chars = ('','#',
            'o','x',
            'v','x',
            '│','x',
            '<','x',
            '┘','x',
            '┐','x',
            '┤','x',
            '>','x',
            '└','x',
            '┌','x',
            '├','x',
            '─','x',
            '┴','x',
            '┬','x',
            '┼','x',
            'O','O','O','O','O','O','O','O',
            'O','O','O','O','O','O','O','O',
            'O','O','O','O','O','O','O','O',
            'O','O','O','O','O','O','O','O',
            'O','O','O','O','O','O','O','O'
            )
    


    def paint(pixelpos, col):
        x,y = pixelpos
        buffer[y*width + x] = col
 
    def getColor(pixel):
        x,y = pixel
        return buffer[y*width + x]

    def setDist(pixelpos, col):
        x,y = pixelpos
        distbuffer[y*width + x] = col
 
    def getDist(pixel):
        x,y = pixel
        return distbuffer[y*width + x]

    def printBoard(displayWidth,displayHeight,score):
        for row in range(displayHeight):
            string = ""
            for column in range(displayWidth):
                pixel = buffer[row * width + column]
                string += chars[pixel]
            string += '\n'
            stdscr.addstr(string)
        string = str(score)
        string += '\n'
        stdscr.addstr(string)
        return len(string)

    def countBoard(displayWidth,displayHeight):
        res = 0
        for row in range(displayHeight):
            for column in range(displayWidth):
                pixel = buffer[row * width + column]
                res += (pixel != 0) 
        return res

    def countBoardOxy(displayWidth,displayHeight):
        res = 0
        for row in range(displayHeight):
            for column in range(displayWidth):
                pixel = buffer[row * width + column]
                res += (pixel & 33) != 0 or pixel == 0
        return res


    def expandOxygen(displayWidth,displayHeight):
        res = 0
        bufferTmp = copy.copy(buffer)
        for row in range(1,displayHeight-1):
            for column in range(1,displayWidth-1):
                if (bufferTmp[row * width + column] & 32) != 0:
                    #propagate to neighbours
                    for i in range(1,5):
                        dir = dirs[i]
                        if (buffer[(row + dir[0]) * width + (column + dir[1])]) != 1:
                            buffer[(row + dir[0]) * width + (column + dir[1])] = 32
        return res

    Prog = Program(-1, 'Prog', initial_numbers)
    start_time = time.time()
    
    res = 0
    topleft = (1000,1000)   
    bottomright = (-1000,-1000)
    score = 0
    nbblocks = 100
    direction = 1
    position = (21,21)
    oxygenPos = (0,0)
    oxygenDist = 0
    nbIteration = 0
    for i in range(0):
        paint((i,0),1)
        paint((i,width-1),1)
        paint((width-1,i),1)
        paint((0,i),1)
    nbBlock = 0

    Prog.execute_cameraView()
    while res != -1 and nbIteration < 3000:
        # update current pos with value will visit
        val = getColor(position)
        val = val | masks[direction]
        paint(position, val)
        res = Prog.execute_move(direction)

        topleft = minPos(topleft,position)
        bottomright = maxPos(bottomright,position)
        nbBlock = countBoard(width,height)
        nbIteration += 1

        stdscr.clear()
        printBoard(width,height,(nbIteration,nbBlock, oxygenDist,oxygenPos,topleft,bottomright))
        stdscr.refresh()
        
        #time.sleep(0.016)

    # count nbPixel of type 2
    stdscr.getch()
    nbIteration = 0
    nbOxy = countBoardOxy(width, height)
    while nbOxy!= width * height:
        nbIteration += 1
        expandOxygen(width,height)
        stdscr.clear()
        printBoard(width,height,(nbIteration,nbBlock, oxygenDist,oxygenPos,topleft,bottomright))
        stdscr.refresh()
        nbOxy = countBoardOxy(width, height)
        time.sleep(0.016)
        

    stdscr.getch()
    
    print("------ Result -------")
    print(oxygenPos)
    print(oxygenDist)
    print("--- {0:.3f} seconds ---".format((time.time() - start_time)))


def printView():
    Prog = Program(-1, 'Prog', initial_numbers)
    #str = Prog.execute_cameraView()
#    inputsStr = ["A,B,A,C,B,C,B,A,C,B" + chr(10), 
#                "L,6,R,8,R,12,L,6,L,8" + chr(10), 
#                "L,10,L,8,R,12" + chr(10),
#                "L,8,L,10,L,6,L,6" + chr(10),
#                "n" + chr(10)]

    inputsStr = ["A,B,A,C,B,C,B,A,C,B" + chr(10) + "L,6,R,8,R,12,L,6,L,8" + chr(10) + "L,10,L,8,R,12" + chr(10) + "L,8,L,10,L,6,L,6" + chr(10) + "n" + chr(10)]
    Prog.reset()
    Prog.setMem(0,2)

    currentInput = 0
    for c in inputsStr[currentInput]:
        Prog.addInput(ord(c))
    res = 0
    string = ""

    while (res<128 and res != -1):
        if res == 10:
            print(string)
            string = ""
        elif chr(res) in ['.','#','<','>','v','^']:
            string += chr(res)
        else:
            print(res,chr(res))

        res = Prog.execute_untiloutput()
    print(res)





    # L,6,R,8,R,12

#wrapper(test_program)
printView()