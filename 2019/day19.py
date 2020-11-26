import copy 
import itertools
import time
from curses import wrapper

memSize = 10000
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

    def resetPointer(self):
        self.inputs = []
        self.execPointer = 0
        self.output = 0
        self.inputIndex = 0
        self.relativeBase = 0

    def reboot(self, code):
        for i,c in enumerate(code):
            self.program[i] = c 
        self.inputs = []
        self.execPointer = 0
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
f = open('input_day19.txt','r')
for line in f:
    initial_numbers = line.split(",")

chars = ['.','#','O']

def test_program(stdscr):

    start_time = time.time()
    width = 100
    height = 100
    buffer = [0] * width * height

    def paint(pixelpos, col):
        x,y = pixelpos
        buffer[y*width + x] = col
 
    def getColor(pixel):
        x,y = pixel
        return buffer[y*width + x]


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

    Prog = Program(0, 'Prog', initial_numbers)
    start_time = time.time()
    
    def getProgPixel(i,j):
        Prog.reboot(initial_numbers)
        Prog.addInput(i)
        Prog.addInput(j)
        res = Prog.execute_untiloutput()
        return res

    for i in range(100):
        for j in range(100):
            res = getProgPixel(i,j)
            if (res==0 or res ==1):
                paint((i,j), res)
            else:
                print(res)

    searchy = 150
    start_searchx = 0
    found = False
    twidth = 99
    pos = ()
    # find first pixel on this line 
    while not found:
        searchx = start_searchx
        res = getProgPixel(searchx,searchy)
        while res != 1 and searchx < start_searchx + 10:
            searchx = searchx + 1 
            res = getProgPixel(searchx,searchy)
        start_searchx = searchx

        cx = getProgPixel(searchx + twidth,searchy)
        while cx != 0:
            cx = getProgPixel(searchx + twidth,searchy)
            cy = getProgPixel(searchx,searchy + twidth)
            if cx == 0:
                #not point in continuing on this lines
                break
            else:
                if cy == 0:
                    searchx += 1
                else:
                    found = True
                    pos = (searchx,searchy)
                    #paint(pos,2)
                    print("Found",pos , pos[0] * 10000 + pos[1])
                    break
        searchy += 1
        print(searchy,start_searchx)


    #for row in range(height):
    #    string = ""
    #    for column in range(width):
    #        pixel = buffer[row * width + column]
    #        string += chars[pixel]
    #    print(string)
    #print(countBoard(width,height))


test_program(None)
