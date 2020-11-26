import copy 
import itertools
import time
from curses import wrapper

memSize = 100000
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
        self.packetqueue = []
        self.outputs= []
        self.lastOpcode = 0
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
        self.relativeBase = 0

    def setMem(self,index,value):
        self.program[index] = int(value)

    def addInput(self, input):
        self.inputs.append(input)

    def addCommandInput(self, string):
        for c in string:
            self.inputs.append(ord(c))

    def resetInput(self, input):
        self.inputs = [input]

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

        if len(self.inputs):
            input = self.inputs.pop(0)
            verboseprint("Write {0} at Adr[{1}]".format(input,retAdr))
            #print("input = " + str(input))
            self.writeAdr(retAdr, input)
        else:
            self.writeAdr(retAdr, -1)
     
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
        self.lastOpcode = opcode

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

 
    def execute_untilhalt(self):
        res = 0
        while (res!=99 and res!=-1): 
            res = self.decode_opcode()
    
        return self.output


initial_numbers= []
f = open('input_day25.txt','r')
for line in f:
    initial_numbers = line.split(",")

def printView():

    prog = Program(0, 'Prog', initial_numbers)
    prog.resetInput()
   
    while (res!= 99 and res != -1):
        res = prog.execute_untiloutput()
        print(chr(res))
            
printView()