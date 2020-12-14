#Advent of code 2020: Day 8
#https://adventofcode.com/2020/day/8
import re, time, copy

f = open('input_day8.txt','r')
lines = f.readlines()
f.close()


opcodes = {"acc":0,"jmp":1,"nop":2}

class Program:
    def __init__(self, sources):
        temp = [] 
        nopjmpindex = 0
        self.fixedinstruction = 0
        for line in sources:
            g = re.search("(...) ([+-]\d+)",line)
            op = opcodes[g.groups()[0]]
            value = int(g.groups()[1])
            nopjmpindex += op>0
            temp.append((op,value))
        
        self.visited = [0]*len(temp)
        self.program = temp
        self.accumulator = 0
        self.codepointer = 0
        self.nbjmpornop = nopjmpindex


    def fixinstruction(self,fixup):
        nopjmpindex = 0
        self.fixedinstruction = 0
        for i,instr in enumerate(self.program):
            op = instr[0]
            value = instr[1]
            #fix nop or jmp if required
            if op>0:
                nopjmpindex += 1
                if fixup == nopjmpindex:
                    op = (op & 1) + 1
                    self.fixedinstruction = i
                    self.program[i] = (op,value)
                    break

    def executeOp(self):
        if (self.codepointer >= len(self.program)):
            return -1
        op = self.program[self.codepointer][0]
        value = self.program[self.codepointer][1]
        visited = self.visited[self.codepointer]
        self.visited[self.codepointer] = 1
        if visited:
            return 1
        if (op == 0):
            self.accumulator += value
            self.codepointer += 1
        elif (op == 1):
            self.codepointer += value
        elif (op == 2):
            self.codepointer += 1
        return 0

    def execute_untillooporend(self):
        res = 0
        while (res == 0): 
            res = self.executeOp()
        return (res,self.accumulator)


def part1():
    prog = Program(lines)
    print(prog.execute_untillooporend()[1])

def part2_bruteforce():
    prog = Program(lines)
    for i in range(1,prog.nbjmpornop):
        #attemp fix
        newprog = copy.deepcopy(prog)
        newprog.fixinstruction(i)
        code = newprog.execute_untillooporend()
        if code[0] == -1:
            print("fixed instruction",newprog.fixedinstruction)
            return code[1]
    return 0    


print("----- Part1 ----")
startp1 = time.time()
part1()
endp1 = time.time()
print("{:.4f}s".format(endp1 - startp1))

print("----- Part2 ----")
startp2 = time.time()
part2_bruteforce()
endp2 = time.time()
print("{:.4f}s".format(endp2 - startp2))