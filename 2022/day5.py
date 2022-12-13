#Advent of code 2022: Day 5
#https://adventofcode.com/2022/day/5
import re, time, copy

f = open('input_day5.txt', 'r')
lines = f.readlines()
lines = [line.rstrip("\n") for line in lines]
f.close()

stacks = []
for j in range(9): 
    stacks.append([])

for i in reversed(range(8)): 
    for j in range(9): 
        c = lines[i][j*4+1]
        if c != " ":
            stacks[j].append(c)
print(stacks)

moves = [re.findall(r"\d+",line) for line in lines[10:]]
print(moves)


def part1():
    tmpStacks = copy.deepcopy(stacks)
    for move in moves:
        nb = int(move[0])
        src = int(move[1])-1
        dst = int(move[2])-1
        for i in range(nb):
            tmpStacks[dst].append(tmpStacks[src].pop())
    str = ""
    for stack in tmpStacks:
        str += stack[-1]
    print(str)            
    return 

def part2():
    tmpStacks = copy.deepcopy(stacks)
    for move in moves:
        nb = int(move[0])
        src = int(move[1])-1
        dst = int(move[2])-1
        toMove = tmpStacks[src][-nb:]
        tmpStacks[src] = tmpStacks[src][:-nb]
        tmpStacks[dst].extend(toMove)
    str = ""
    for stack in tmpStacks:
        str += stack[-1]
    print(str)      
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