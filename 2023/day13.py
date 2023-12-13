#Advent of code 2023: Day 13
#https://adventofcode.com/2023/day/13
import re, time, copy, math
from functools import cache

f = open('input_day13.txt', 'r')
lines = f.readlines()
lines = [line.rstrip("\n") for line in lines]
f.close()

patterns = []
curPattern = []
for line in lines: 
    if line == "": 
        patterns.append(curPattern.copy())
        curPattern = []
    else:
        curPattern.append(line)
patterns.append(curPattern)

print(len(patterns))

def rotatedPattern(pattern):
    rot = [''.join([line[j] for line in pattern]) for j in range(len(pattern[0]))] 
    return rot
    

def findReflectionRow(pattern, nbDifs):
    # try all potential lines of simmetry
    # take only one that has nbDifs difference (part 1: 0, part 2: 1)
    height = len(pattern)
    width = len(pattern[0])
    for pot in range(1,height):
            maxMirror = min(pot,height-pot)
            diffToBeMirrorable = 0 # number of difference characters 
            for i in range(maxMirror):
                diffs = [pattern[pot-1-i][j] == pattern[pot+i][j] for j in range(width)]
                diffToBeMirrorable += diffs.count(False) 
            if diffToBeMirrorable == nbDifs:
                return pot
    return 0 

def solve(nbDif):
    sum = 0
    for pat in patterns:
        rowIndex = findReflectionRow(pat,nbDif)
        rotatedPat =rotatedPattern(pat)
        ColumnIndex = findReflectionRow(rotatedPat,nbDif)
        print(rowIndex,ColumnIndex)
        sum += ColumnIndex + 100 * rowIndex
    print(sum)

def part1():
    solve(0)
    return 

def part2():
    solve(1)
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