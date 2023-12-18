#Advent of code 2023: Day 16
#https://adventofcode.com/2023/day/16
import re, time, copy, math
from functools import cache

f = open('input_day16.txt', 'r')
lines = f.readlines()
lines = [line.rstrip("\n") for line in lines]
f.close()

grid = [[c for c in line] for line in lines]
width = len(grid[0])
height = len(grid)

energized = [[0 for c in line] for line in lines]

dirs = [(1,0),(0,1),(-1,0),(0,-1)]

effects = {
    ".": [[0],[1],[2],[3]],
    "/": [[3],[2],[1],[0]],
    "\\": [[1],[0],[3],[2]],
    "-": [[0],[0,2],[2],[0,2]],
    "|": [[1,3],[1],[1,3],[3]]}

def addDelta(pos,delta):
    return (pos[0]+delta[0],pos[1]+delta[1])

def getGrid(pos):
    return grid[pos[1]][pos[0]]

beams = [((0,0),0)]

def advanceBeam(beam):
    global energized

    if (energized[beam[0][1]][beam[0][0]] & (1 << beam[1])) != 0:
        # we already passed through this cell in that direction, skip 
        return []

    energized[beam[0][1]][beam[0][0]] |= (1 << beam[1]) 

    newPos = addDelta(beam[0] , dirs[beam[1]])

    if (newPos[0] < 0 or newPos[0] >= width or newPos[1] < 0 or newPos[1] >= height):
        return []
    
    code = getGrid(newPos)
    if (not code in effects):
        print("error")
    newDirs = effects[code][beam[1]]
    return [(newPos,dir) for dir in newDirs]

def processBeams():
    global beams
    while len(beams):
        beam = beams.pop(0)
        newBeams = advanceBeam(beam)
        beams.extend(newBeams)
#        print(beams)


def checkPos(pos,dir):
    global beams
    global energized
    beams = [(pos,dir)]
    energized = [[0 for c in line] for line in lines]
    processBeams()
    totalEnergized = sum(sum(1 for c in row if c != 0) for row in energized)
    return totalEnergized

def part1():
    totalEnergized = checkPos((0,0),0)
    print(totalEnergized)
    return 



def part2():
    maxEnergized = 0
    for i in range(width):
        maxEnergized = max(maxEnergized, checkPos((i,0),1))
        maxEnergized = max(maxEnergized, checkPos((i,height-1),3))
        maxEnergized = max(maxEnergized, checkPos((0,i),0))
        maxEnergized = max(maxEnergized, checkPos((width-1,i),2))
    print(maxEnergized)

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