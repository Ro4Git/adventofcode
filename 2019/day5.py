import copy 


global_input = 5
global_output = 0

initial_numbers= []
f = open('input_day5.txt','r')
for line in f:
    initial_numbers = line.split(",")

def opcode_Add(exec_pointer,program, inmode1, inmode2, inmode3):
    value1 = int(program[exec_pointer + 1])
    value2 = int(program[exec_pointer + 2])
    retAdr = int(program[exec_pointer + 3])
    if (inmode1 == 0):
        value1 = int(program[value1])
    if (inmode2 == 0):
        value2 = int(program[value2])
    if inmode3 != 0:
        print("------- unenexpected param mode({0})".format(inmode3))

    print("Add {0}+{1} at Adr[{2}]".format(value1, value2 ,retAdr))
    program[retAdr] =  value1 + value2
    return exec_pointer + 4

def opcode_Mul(exec_pointer,program, inmode1, inmode2, inmode3):
    value1 = int(program[exec_pointer + 1])
    value2 = int(program[exec_pointer + 2])
    retAdr = int(program[exec_pointer + 3])
    if (inmode1 == 0):
        value1 = int(program[value1])
    if (inmode2 == 0):
        value2 = int(program[value2])    
    if inmode3 != 0:
        print("------- unenexpected param mode({0})".format(inmode3))

    print("Mul {0}*{1} at Adr[{2}]".format(value1, value2 ,retAdr))
    program[retAdr] =  value1 * value2
    return exec_pointer + 4

def opcode_Write(exec_pointer,program, inmode1, inmode2, inmode3):
    retAdr = int(program[exec_pointer + 1])
    if inmode1 != 0:
        print("------- unenexpected param mode({0})".format(inmode1))
    print("Write {0} at Adr[{1}]".format(global_input,retAdr))
    program[retAdr] =  global_input
    return exec_pointer + 2

def opcode_Output(exec_pointer,program, inmode1, inmode2, inmode3):
    value1 = int(program[exec_pointer + 1])
    if (inmode1 == 0):
        value1 = int(program[value1])
    print("Output=>{0}".format(value1))
    global_output =  value1
    return exec_pointer + 2

def opcode_JumpT(exec_pointer,program, inmode1, inmode2, inmode3):
    value1 = int(program[exec_pointer + 1])
    value2 = int(program[exec_pointer + 2])
    if (inmode1 == 0):
        value1 = int(program[value1])
    if (inmode2 == 0):
        value2 = int(program[value2])  
    
    if value1 != 0:
        print("JumpT to [{1}] because ({0}!=0)".format(value1,value2))
        return value2
    else:
        print("No JumpT because ({0}==0)".format(value1,value2))
        return exec_pointer + 3

def opcode_JumpF(exec_pointer,program, inmode1, inmode2, inmode3):
    value1 = int(program[exec_pointer + 1])
    value2 = int(program[exec_pointer + 2])
    if (inmode1 == 0):
        value1 = int(program[value1])
    if (inmode2 == 0):
        value2 = int(program[value2])  
    if value1 == 0:
        print("JumpF to [{1}] because ({0}==0)".format(value1,value2))
        return value2
    else:
        print("No JumpF because ({0}!=0)".format(value1,value2))
        return exec_pointer + 3        

def opcode_LessThan(exec_pointer,program, inmode1, inmode2, inmode3):
    value1 = int(program[exec_pointer + 1])
    value2 = int(program[exec_pointer + 2])
    retAdr = int(program[exec_pointer + 3])
    if (inmode1 == 0):
        value1 = int(program[value1])
    if (inmode2 == 0):
        value2 = int(program[value2])  
    if inmode3 != 0:
        print("------- unenexpected param mode({0})".format(inmode3))    
    if value1 < value2:
        print("[{2}]=1 because ({0}<{1})".format(value1,value2,retAdr))
        program[retAdr] = 1
    else:
        print("[{2}]=0 because ({0}>={1})".format(value1,value2,retAdr))
        program[retAdr] = 0
    return exec_pointer + 4     

def opcode_Equals(exec_pointer,program, inmode1, inmode2, inmode3):
    value1 = int(program[exec_pointer + 1])
    value2 = int(program[exec_pointer + 2])
    retAdr = int(program[exec_pointer + 3])
    if (inmode1 == 0):
        value1 = int(program[value1])
    if (inmode2 == 0):
        value2 = int(program[value2])  
    if inmode3 != 0:
        print("------- unenexpected param mode({0})".format(inmode3))        
    if value1 == value2:
        print("[{2}]=1 because ({0}=={1})".format(value1,value2,retAdr))
        program[retAdr] = 1
    else:
        print("[{2}]=0 because ({0}!={1})".format(value1,value2,retAdr))
        program[retAdr] = 0
    return exec_pointer + 4   


def decode_opcode(exec_pointer,program):
    instruction = int(program[exec_pointer])
    opcode = instruction % 100
    inmode1 = int(instruction/100) % 10
    inmode2 = int(instruction/1000) % 10
    inmode3 = int(instruction/10000) % 10

    if opcode == 1: 
        return opcode_Add(exec_pointer, program, inmode1, inmode2, inmode3)
    if opcode == 2: 
        return opcode_Mul(exec_pointer, program, inmode1, inmode2, inmode3)
    if opcode == 3: 
        return opcode_Write(exec_pointer, program, inmode1, inmode2, inmode3)
    if opcode == 4: 
        return opcode_Output(exec_pointer, program, inmode1, inmode2, inmode3)
    if opcode == 5: 
        return opcode_JumpT(exec_pointer, program, inmode1, inmode2, inmode3)
    if opcode == 6: 
        return opcode_JumpF(exec_pointer, program, inmode1, inmode2, inmode3)               
    if opcode == 7: 
        return opcode_LessThan(exec_pointer, program, inmode1, inmode2, inmode3)
    if opcode == 8: 
        return opcode_Equals(exec_pointer, program, inmode1, inmode2, inmode3)                
    if opcode == 99: 
        print("End Of Program")
        return -1
    print("unsupported opcode")
    return -1    

def test_program():
    numbers = copy.copy(initial_numbers)
    i = 0
    instr_length = 0
    print len(numbers)
    print("---------- Starting --------")

    while i != -1: 
        i = decode_opcode(i, numbers)


test_program()
