#Advent of code 2023: Day 8
#https://adventofcode.com/2023/day/8
import re, time, copy, math

f = open('input_day8.txt', 'r')
lines = f.readlines()
lines = [line.rstrip("\n") for line in lines]
f.close()

instructions = lines[0]

nodes = {line[0:3] : (line[7:10],line[12:15]) for line in lines[2:]}
dir = {'L':0,'R':1}
print(nodes)

def part1():
    nbStep = 0

    currentNode = "AAA"
    while currentNode != "ZZZ":
        currentInstr = instructions[nbStep%len(instructions)]
        currentNode = nodes[currentNode][dir[currentInstr]] 
        nbStep = nbStep + 1

    print(nbStep)
    return 

def part2():
    nbStep = 0

    currentNodes = [node for node in nodes.keys() if node[2]=='A']
    allModulos = []
    for currentNode in currentNodes:
        nbStep = 0
        modulos = []
        while (currentNode[2] != "Z") or not nbStep in modulos:
            if currentNode[2] == "Z":
                modulos.append(nbStep)
                nbStep = 0
            currentInstr = instructions[nbStep%len(instructions)]
            currentNode = nodes[currentNode][dir[currentInstr]] 
            nbStep = nbStep + 1
        allModulos.extend(modulos)
        
    print(allModulos)
    print(math.lcm(*allModulos))
    
    
 #   while not all(node[2]=='Z' for node in currentNodes):
 #       currentInstr = instructions[nbStep%len(instructions)]
 #       currentNodes = [nodes[currentNode][dir[currentInstr]] for currentNode in currentNodes]  
 #       nbStep = nbStep + 1

    print(nbStep)
 

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