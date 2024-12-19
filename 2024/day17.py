#Advent of code 2024: Day 17
#https://adventofcode.com/2024/day/17
import re, time, copy , functools, itertools
from collections import defaultdict
import aoc

lines = aoc.ReadPuzzleInput("input_day17.txt")
sections = aoc.ToSections(lines)

class Computer:
    def __init__(self, regA, regB, regC, program):
        self.regA = regA
        self.regB = regB
        self.regC = regC
        self.program = program 
        self.output = []
        self.ip = 0
    
        # Combo operands 0 through 3 represent literal values 0 through 3.
        # Combo operand 4 through 6 represents the value of register A,B,C.
        self.comboOperands = [lambda :0,lambda :1,lambda :2,lambda :3,lambda :self.regA,lambda :self.regB,lambda :self.regC] 
        self.opcodes = [lambda x:self.adv(x),
                        lambda x:self.bxl(x),
                        lambda x:self.bst(x),
                        lambda x:self.jnz(x),
                        lambda x:self.bxc(x),
                        lambda x:self.out(x),
                        lambda x:self.bdv(x),
                        lambda x:self.cdv(x)] 

    def process(self):
        while self.ip<len(self.program):
            opcode = self.program[self.ip]
            operand = self.program[self.ip+1]
            self.opcodes[opcode](operand)
        

    # 0 The adv instruction (opcode 0) performs division. 
    #The numerator is the value in the A register. 
    #The denominator is found by raising 2 to the power of the instruction's combo operand. 
    #(So, an operand of 2 would divide A by 4 (2^2); an operand of 5 would divide A by 2^B.) 
    #The result of the division operation is truncated to an integer and then written to the A register
    def adv(self,op):
        comboOp = self.comboOperands[op]()
        num = self.regA 
        den = 1 << comboOp 
        self.regA = int(num / den)
        self.ip += 2
        
    # 1 The bxl instruction (opcode 1) calculates the bitwise XOR of register B and the instruction's literal operand, 
    # then stores the result in register B
    def bxl(self,op):
        self.regB = self.regB ^ op
        self.ip += 2

    # 2 The bst instruction (opcode 2) calculates the value of its combo operand modulo 8 (thereby keeping only its lowest 3 bits),
    # then writes that value to the B register.
    def bst(self,op):
        comboOp = self.comboOperands[op]()
        self.regB = comboOp & 7
        self.ip += 2

    # 3 The jnz instruction (opcode 3) does nothing if the A register is 0. 
    #However, if the A register is not zero, it jumps by setting the instruction pointer to the value of its literal operand; 
    #if this instruction jumps, the instruction pointer is not increased by 2 after this instruction.
    def jnz(self,op):
        if self.regA == 0:
            self.ip += 2
        else:
            self.ip = op

    # 4 The bxc instruction (opcode 4) calculates the bitwise XOR of register B and register C, then stores the result in register B. 
    # (For legacy reasons, this instruction reads an operand but ignores it.)
    def bxc(self,op):
        self.regB = self.regB ^ self.regC
        self.ip += 2
        
    # 5 The out instruction (opcode 5) calculates the value of its combo operand modulo 8, then outputs that value. 
    # (If a program outputs multiple values, they are separated by commas.)
    def out(self,op):
        comboOp = self.comboOperands[op]()
        self.output.append(comboOp & 7)
        self.ip += 2

    # 6 The bdv instruction (opcode 6) works exactly like the adv instruction except that the result is stored in the B register. 
    #(The numerator is still read from the A register.)
    def bdv(self,op):
        comboOp = self.comboOperands[op]()
        num = self.regA 
        den = 1 << comboOp 
        self.regB = int(num / den)
        self.ip += 2
        
    # 7 The cdv instruction (opcode 7) works exactly like the adv instruction except that the result is stored in the C register.
    # (The numerator is still read from the A register.)
    def cdv(self,op):
        comboOp = self.comboOperands[op]()
        num = self.regA 
        den = 1 << comboOp 
        self.regC = int(num / den)
        self.ip += 2
    
def part1():
    comp = Computer(22571680,0,0,[2,4,1,3,7,5,0,3,4,3,1,5,5,5,3,0])
   # comp = Computer(729,0,0,[0,1,5,4,3,0] )
    
    comp.process()
    resultString = (',').join([str(x) for x in comp.output])
    print(resultString)
    return 

def part2():
 #2,4 b = a % 8 = a & 7
 #1,3 b = b ^ 3
 #7,5 c = a / (2^b)
 #0,3 a = a / (2^3) = a/8 = a >> 3
 #4,3 b = b ^ c
 #1,5 b = b ^ 5
 #5,5 out b % 8 = b & 7
 #3,0 jnz (a != 0)
 # each output digit is influenced by the binary part of A above 1 << 3 * indexDigit 
 # last digit should only be influenced by the top 3 bits of A
    digits = [2,4,1,3,7,5,0,3,4,3,1,5,5,5,3,0]
    nbDigits = len(digits)
    validASoFar =[0]
    
    for digit in reversed(range(nbDigits)): 
        nextPotentialA = []
        mask = 7 << digit*3
        
        for i in range(8): 
            for currentA in validASoFar:
                currentA = (currentA & ~mask) | i << digit*3
                
                comp = Computer(currentA,0,0,digits)
                comp.process()
                
                if len(digits) == len(comp.output):
                    if digits[digit:] == comp.output[digit:]:
                        # keep value that still generate correct ouputs 
                        # from this digit to the last
                        nextPotentialA.append(currentA)
        validASoFar = nextPotentialA
    A = min(validASoFar)
    
    print(A)
    return 

print("----- Part1 ----")
startp1 = time.time()
part1()
endp1 = time.time()
print("{:.4f}s".format(endp1 - startp1))

print("----- Part2 ----")
startp2 = time.time()
part2()
endp2 = time.time()
print("{:.4f}s".format(endp2 - startp2))

