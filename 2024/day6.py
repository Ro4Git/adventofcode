#Advent of code 2024: Day 6
#https://adventofcode.com/2024/day/6
import re, time, copy , functools
from collections import defaultdict
import aoc

lines = aoc.ReadPuzzleInput("input_day6.txt")
grid = aoc.ToGrid(lines)

startingPos = grid.Find('^')
startingDir = aoc.north
visitedpart1 = {}
enableVisu = False

display = aoc.Display(enableVisu, grid.width, grid.height,    4 , 1)

def DoRound(obsPos = None):
    visited = {}
    visitedAndDir = {}
    pos = startingPos
    dir = startingDir
    loopDetected = False

    while not grid.IsOut(pos):
        visited[pos] = 1
        if (pos,dir) in visitedAndDir:
            loopDetected = True
            break
        else:
            visitedAndDir[(pos,dir)] = 1
        npos = aoc.addPos(pos,aoc.dirs4[dir])
        if grid.IsOut(npos):
            break
        if grid.Val(npos) == "#":
            dir = aoc.turn90right[dir]
        elif obsPos != None  and npos == obsPos:
            dir = aoc.turn90right[dir]
        else:
            pos = npos
    return visited, visitedAndDir, loopDetected


def part1():
    global visitedpart1
    visitedpart1, visitedAndDir, loop = DoRound()
    
    display.drawGrid(grid, lambda x: (150,80,122) if x !='.' else (0,0,0))
    display.drawListPos(visitedpart1.keys(),(255,255,255))
    display.update()
    
    print(len(visitedpart1))
    return 

def part2():
    potentialObstacles = list(visitedpart1.keys())
    potentialObstacles.remove(startingPos)
    
    validObsPos = []
    for obsPos in potentialObstacles:
        visited, visitedAndDir, loop = DoRound(obsPos)
        if loop: 
            display.clear()
            display.drawGrid(grid, lambda x: (150,80,122) if x !='.' else (0,0,0))
            display.drawListPos(visited.keys(),(255,255,255))
            display.update()            
            validObsPos.append(obsPos)
    print(len(validObsPos))

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

display.wait()