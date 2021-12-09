#Advent of code 2021: Day 9
#https://adventofcode.com/2021/day/9
import re, time, copy, math
from collections import defaultdict

f = open('input_day9.txt', 'r')
lines = f.readlines()
lines = [line.rstrip("\n") for line in lines]
f.close()

grid = []
for line in lines:
    grid.append([int(c) for c in line])
width = len(grid[0])
height = len(grid)
dirs = [(-1,0),(0,1),(1,0),(0,-1)]

lowPoints = []

def gridPixelDelta(pos,dir):
    h = grid[pos[1]][pos[0]]
    pos2 = (pos[0]+dir[0],pos[1]+dir[1])
    if (pos2[0] >= 0 and pos2[0]<width and pos2[1]>=0 and pos2[1]<height):
        if grid[pos2[1]][pos2[0]] <= h:
            return 0
    return 1

def expandFromLow(pos):
    global grid
    nbcell = 1
    h = grid[pos[1]][pos[0]]
    if (h>=9):
        return 0
    for expand_dir in dirs:
        # try expanding to this neighbour
        pos2 = (pos[0] + expand_dir[0], pos[1] + expand_dir[1])
        if (pos2[0] >= 0 and pos2[0] < width and pos2[1] >= 0 and pos2[1] < height):
            if grid[pos2[1]][pos2[0]] > h:
                nbcell += expandFromLow(pos2)
                grid[pos2[1]][pos2[0]] = 9
    return nbcell

def part1():
    global lowPoints
    totalRiskFactor = 0
    for y in range(height):
        for x in range(width):
            pos = (x,y)    
            riskFactor = grid[pos[1]][pos[0]] + 1
            for dir in dirs:
                if gridPixelDelta(pos,dir) <= 0:
                    riskFactor = 0
                    break
            totalRiskFactor += riskFactor
            if (riskFactor):
                lowPoints.append(pos)
    print(lowPoints)
    print(totalRiskFactor)



def part2():
    bassins = []
    for pos in lowPoints:
        nbcells = expandFromLow(pos)
        bassins.append(nbcells)
    print(bassins)
    top3 = sorted(bassins,reverse=True)[:3]
    print(top3)
    result = 1
    for r in top3:
        result *= r
    print(result)
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