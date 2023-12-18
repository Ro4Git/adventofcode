#Advent of code 2023: Day 14
#https://adventofcode.com/2023/day/14
import re, time, copy, math
from functools import cache

f = open('input_day14.txt', 'r')
lines = f.readlines()
lines = [line.rstrip("\n") for line in lines]
f.close()

grid = [[c for c in line] for line in lines]
width = len(grid[0])
height = len(grid)

rocks = []
for y,line in enumerate(grid):
    for x,c in enumerate(line):
        if c == 'O':
            rocks.append((x,y))

dirs = [(-1,0),(1,0),(0,-1),(0,1)]

def addDelta(pos,delta):
    return (pos[0]+delta[0],pos[1]+delta[1])

def oppDelta(delta):
    return (-delta[0],-delta[1])

def getGrid(pos):
    return grid[pos[1]][pos[0]]

def gridLoad():
    totalLoad = 0
    for i,line in enumerate(grid):
        rowLoad = height - i 
        totalLoad += rowLoad * line.count('O')
    return totalLoad

def tiltGridNorth():
    nbMove = 0
    for x in range(width):
        for y in range(1,height):
            if grid[y][x] == 'O': 
                # check if free cell to move to 
                if grid[y-1][x] == '.':
                    grid[y-1][x] = 'O'
                    grid[y][x] = '.'
                    nbMove += 1
    return nbMove

def tiltGridSouth():
    nbMove = 0
    for x in range(width):
        for y in reversed(range(0,height-1)):
            if grid[y][x] == 'O': 
                # check if free cell to move to 
                if grid[y+1][x] == '.':
                    grid[y+1][x] = 'O'
                    grid[y][x] = '.'
                    nbMove += 1
    return nbMove

def tiltGridWest():
    nbMove = 0
    for y in range(height):
        for x in range(1,width):
            if grid[y][x] == 'O': 
                # check if free cell to move to 
                if grid[y][x-1] == '.':
                    grid[y][x-1] = 'O'
                    grid[y][x] = '.'
                    nbMove += 1
    return nbMove

def tiltGridEast():
    nbMove = 0
    for y in range(height):
        for x in reversed(range(0,width-1)):
            if grid[y][x] == 'O': 
                # check if free cell to move to 
                if grid[y][x+1] == '.':
                    grid[y][x+1] = 'O'
                    grid[y][x] = '.'
                    nbMove += 1
    return nbMove

def doCycle():
    nbTilt = 0
    while tiltGridNorth():
        nbTilt += 1
    while tiltGridWest():
        nbTilt += 1
    while tiltGridSouth():
        nbTilt += 1
    while tiltGridEast():
        nbTilt += 1
    return gridLoad()

def part1():
    nbTilt = 0
    while tiltGridNorth():
        nbTilt += 1
    print(gridLoad())
    return 

def part2():
    cycleResults = []
    #run cycles until a patterns appear:
    startRepeat = 0
    currentLength = 0
    for i in range(6000):
        load = doCycle()
        if load in cycleResults: 
            if startRepeat <= 0:
                print("potential repeat :",i)
                startRepeat = i
                currentLength = 1
            else: 
                currentLength+=1
                if cycleResults[startRepeat] == load:
                    print("repeats on ",i,currentLength-1)
                    break
        else: 
            startRepeat = 0
            currentLength = 0
        cycleResults.append(load)

    period = currentLength-1
    
    startIndex = 0
    while cycleResults[startIndex] != cycleResults[startIndex+period]:
        startIndex += 1

    finalLoad = cycleResults[startIndex + ((1000000000-1-startIndex) % period)]
    print(finalLoad)
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