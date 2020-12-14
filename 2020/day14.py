#Advent of code 2020: Day 14
#https://adventofcode.com/2020/day/14
import re
import time


f = open('input_day14.txt', 'r')
lines = f.readlines()
f.close()

memory = {}
currentMask = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
currentMaskZeros = 0    # mask where zeros should be forced 
currentMaskOnes = 0     # mask where ones should be forced 

def ReadMask(s):
    global currentMask,currentMaskZeros,currentMaskOnes
    currentMask = s.rstrip()
    zeros = currentMask.replace("1",'X').replace("0",'1').replace("X",'0')
    ones = currentMask.replace("X",'0')
    currentMaskZeros = int(zeros,2)
    currentMaskOnes = int(ones,2)
    #print("-- Mask Changed" , currentMask, currentMask.count("X"))

def WriteMemoryPart1(adress, value):
    val = value & ~currentMaskZeros
    val = val | currentMaskOnes
    memory[adress] = val

def WriteMemoryPart2(adress, value):
    adress = adress | currentMaskOnes
    possibles = [adress]

    #all possible combination for "X" in mask
    for i,c in enumerate(reversed(currentMask)):
        if c=="X":
            addedlist = []
            for adr in possibles:
                addedlist.append( adr ^ (1<<i))
            possibles.extend(addedlist)
    for adr in possibles:
        memory[adr] = value    

def part(writeFunc):
    global memory
    memory = {}    
    for line in lines:
        tokens = line.split(" = ")
        if (tokens[0] == "mask"):
            ReadMask(tokens[1])
        else:
            m = re.search('mem\[(\d+)] = (\d+)', line)
            if m != None and len(m.groups()) == 2:
                adress = int(int(m.groups()[0]))
                value = int(int(m.groups()[1]))
                writeFunc(adress, value)
    print("Sum : ",sum(memory.values()))
    return


print("----- Part1 ----")
startp1 = time.time()
part(WriteMemoryPart1)
endp1 = time.time()
print("{:.4f}s".format(endp1 - startp1))

#6386593869035

print("----- Part2 ----")
startp2 = time.time()
part(WriteMemoryPart2)
endp2 = time.time()
print("{:.4f}s".format(endp2 - startp2))

#4288986482164
