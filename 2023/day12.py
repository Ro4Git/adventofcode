#Advent of code 2023: Day 12
#https://adventofcode.com/2023/day/12
import re, time, copy, math
from functools import cache

f = open('input_day12.txt', 'r')
lines = f.readlines()
lines = [line.rstrip("\n") for line in lines]
f.close()

codes = []
for line in lines:
    m = line.split(' ')
    mask = m[0]
    damaged = [int(c) for c in m[1].split(',')]
    codes.append((mask,damaged))

def possInLines(mask,damagedList):
    nbDamageBlocks = len(damagedList)
    lenMask = len(mask)

    @cache
    def recurse(maskIndex, damageIndex, nbSol = 0):
        if maskIndex >=  lenMask:
            #reached the end, 1 solution found if all blocks were placed
            return damageIndex == nbDamageBlocks
        
        if mask[maskIndex] == '.' or mask[maskIndex] == '?':
            # try skipping til next damage block
            nbSol += recurse(maskIndex+1,damageIndex,0)
        
        if damageIndex == nbDamageBlocks:
            return nbSol
        
        if mask[maskIndex] == '?' or mask[maskIndex] == '#':
            # potential block start
            damBlockSize = damagedList[damageIndex]
            if maskIndex + damBlockSize <= lenMask and not '.' in mask[maskIndex:maskIndex+damBlockSize]:
                # continuous block, check ending condition
                if maskIndex + damBlockSize == lenMask or mask[maskIndex+damBlockSize] != '#':
                    #valid damage block, try next possibilities
                    nbSol += recurse(maskIndex + damBlockSize+1,damageIndex+1)
        return nbSol
    
    return recurse(0,0)
       

def part1():
    possibilities = [possInLines(code[0],code[1]) for code in codes]
    #print(possibilities)
    print(sum(possibilities))
    return 

def part2():
    possibilities = []
    for code in codes: 
        newDamage = code[1]*5 
        newMask = (code[0] + "?") *4 + code[0]
        poss = possInLines(newMask,newDamage)
        #print(poss)
        possibilities.append(poss)
   # print(possibilities)
    print(sum(possibilities))    
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