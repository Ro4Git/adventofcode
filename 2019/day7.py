import copy 
import itertools

verbose = False
programs = {}

class Program:
    def __init__(self, phase, name, code):
        self.program = copy.copy(code)
        self.name = name
        self.inputs = [phase]
        self.exec_pointer = 0
        self.output = 0
        self.inputIndex = 0

    def addInput(self, input):
        self.inputs.append(input)
 
    # opcode 1
    def opcode_Add(self, inmode1, inmode2, inmode3):
        value1 = int(self.program[self.exec_pointer + 1])
        value2 = int(self.program[self.exec_pointer + 2])
        retAdr = int(self.program[self.exec_pointer + 3])
        if (inmode1 == 0):
            value1 = int(self.program[value1])
        if (inmode2 == 0):
            value2 = int(self.program[value2])
        if inmode3 != 0:
            print("------- unenexpected param mode({0})".format(inmode3))

        if (verbose):
            print("Add {0}+{1} at Adr[{2}]".format(value1, value2 ,retAdr))
        self.program[retAdr] =  value1 + value2
        return self.exec_pointer + 4

    # opcode 2
    def opcode_Mul(self, inmode1, inmode2, inmode3):
        value1 = int(self.program[self.exec_pointer + 1])
        value2 = int(self.program[self.exec_pointer + 2])
        retAdr = int(self.program[self.exec_pointer + 3])
        if (inmode1 == 0):
            value1 = int(self.program[value1])
        if (inmode2 == 0):
            value2 = int(self.program[value2])    
        if inmode3 != 0:
            print("------- unenexpected param mode({0})".format(inmode3))
        
        if (verbose):
            print("Mul {0}*{1} at Adr[{2}]".format(value1, value2 ,retAdr))
        self.program[retAdr] =  value1 * value2
        return self.exec_pointer + 4

    # opcode 3
    def opcode_Write(self, inmode1, inmode2, inmode3):
        retAdr = int(self.program[self.exec_pointer + 1])
        if inmode1 != 0:
            print("------- unenexpected param mode({0})".format(inmode1))
        if (verbose):
            print("Write input {0}".format(self.inputIndex))
            print("Write {0} at Adr[{1}]".format(self.inputs[self.inputIndex],retAdr))
        self.program[retAdr] =  self.inputs[self.inputIndex]
        self.inputIndex = self.inputIndex + 1
        return self.exec_pointer + 2

    def opcode_Output(self, inmode1, inmode2, inmode3):
        value1 = int(self.program[self.exec_pointer + 1])
        if (inmode1 == 0):
            value1 = int(self.program[value1])
        if (verbose):
            print("Output=>{0}".format(value1))
        self.output =  value1
        return self.exec_pointer + 2

    def opcode_JumpT(self, inmode1, inmode2, inmode3):
        value1 = int(self.program[self.exec_pointer + 1])
        value2 = int(self.program[self.exec_pointer + 2])
        if (inmode1 == 0):
            value1 = int(self.program[value1])
        if (inmode2 == 0):
            value2 = int(self.program[value2])  
        
        if value1 != 0:
            if (verbose):
                print("JumpT to [{1}] because ({0}!=0)".format(value1,value2))
            return value2
        else:
            if (verbose):
                print("No JumpT because ({0}==0)".format(value1,value2))
            return self.exec_pointer + 3

    def opcode_JumpF(self, inmode1, inmode2, inmode3):
        value1 = int(self.program[self.exec_pointer + 1])
        value2 = int(self.program[self.exec_pointer + 2])
        if (inmode1 == 0):
            value1 = int(self.program[value1])
        if (inmode2 == 0):
            value2 = int(self.program[value2])  
        if value1 == 0:
            if (verbose):
                print("JumpF to [{1}] because ({0}==0)".format(value1,value2))
            return value2
        else:
            if (verbose):
                print("No JumpF because ({0}!=0)".format(value1,value2))
            return self.exec_pointer + 3        

    def opcode_LessThan(self, inmode1, inmode2, inmode3):
        value1 = int(self.program[self.exec_pointer + 1])
        value2 = int(self.program[self.exec_pointer + 2])
        retAdr = int(self.program[self.exec_pointer + 3])
        if (inmode1 == 0):
            value1 = int(self.program[value1])
        if (inmode2 == 0):
            value2 = int(self.program[value2])  
        if inmode3 != 0:
            print("------- unenexpected param mode({0})".format(inmode3))    
        if value1 < value2:
            if (verbose):
                print("[{2}]=1 because ({0}<{1})".format(value1,value2,retAdr))
            self.program[retAdr] = 1
        else:
            if (verbose):
                print("[{2}]=0 because ({0}>={1})".format(value1,value2,retAdr))
            self.program[retAdr] = 0
        return self.exec_pointer + 4     

    def opcode_Equals(self, inmode1, inmode2, inmode3):
        value1 = int(self.program[self.exec_pointer + 1])
        value2 = int(self.program[self.exec_pointer + 2])
        retAdr = int(self.program[self.exec_pointer + 3])
        if (inmode1 == 0):
            value1 = int(self.program[value1])
        if (inmode2 == 0):
            value2 = int(self.program[value2])  
        if inmode3 != 0:
            print("------- unenexpected param mode({0})".format(inmode3))        
        if value1 == value2:
            if (verbose):
                print("[{2}]=1 because ({0}=={1})".format(value1,value2,retAdr))
            self.program[retAdr] = 1
        else:
            if (verbose):
                print("[{2}]=0 because ({0}!={1})".format(value1,value2,retAdr))
            self.program[retAdr] = 0
        return self.exec_pointer + 4   


    # return value 
    # 1-8 - execptected opcode ( output = 4)
    # 99 - end of program
    # -1 - error 
    def decode_opcode(self):
        instruction = int(self.program[self.exec_pointer])
        opcode = instruction % 100
        inmode1 = int(instruction/100) % 10
        inmode2 = int(instruction/1000) % 10
        inmode3 = int(instruction/10000) % 10

        if opcode == 1: 
            self.exec_pointer = self.opcode_Add(inmode1, inmode2, inmode3)
        elif opcode == 2:  
            self.exec_pointer = self.opcode_Mul(inmode1, inmode2, inmode3)
        elif opcode == 3: 
            self.exec_pointer = self.opcode_Write(inmode1, inmode2, inmode3)
        elif opcode == 4: 
            self.exec_pointer = self.opcode_Output(inmode1, inmode2, inmode3)
        elif opcode == 5: 
            self.exec_pointer = self.opcode_JumpT(inmode1, inmode2, inmode3)
        elif opcode == 6: 
            self.exec_pointer=  self.opcode_JumpF(inmode1, inmode2, inmode3)               
        elif opcode == 7: 
            self.exec_pointer = self.opcode_LessThan(inmode1, inmode2, inmode3)
        elif opcode == 8: 
            self.exec_pointer = self.opcode_Equals(inmode1, inmode2, inmode3)                
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


initial_numbers= []
f = open('input_day7.txt','r')
for line in f:
    initial_numbers = line.split(",")


def test_program():

    print("---------- Starting --------")

    res = itertools.permutations(range(5,10)) 
    max_output = 0
    max_phase = []

    for perm in res:
        phase = list(perm)
        print(phase)

        ProgA = Program(phase[0], 'A', initial_numbers)
        ProgB = Program(phase[1], 'B', initial_numbers)
        ProgC = Program(phase[2], 'C', initial_numbers)
        ProgD = Program(phase[3], 'D', initial_numbers)
        ProgE = Program(phase[4], 'E', initial_numbers)

        res = 0

        while res != -1:
            ProgA.addInput(res)
            res = ProgA.execute_untiloutput()
            
            ProgB.addInput(res)
            res = ProgB.execute_untiloutput()

            ProgC.addInput(res)
            res = ProgC.execute_untiloutput()

            ProgD.addInput(res)
            res = ProgD.execute_untiloutput()        

            ProgE.addInput(res)
            res = ProgE.execute_untiloutput()

        if ProgE.output > max_output:
            max_output = ProgE.output
            max_phase = phase

    print("------ Result -------")
    print(max_phase)
    print(max_output)

test_program()
