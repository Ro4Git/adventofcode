#Advent of code 2021: Day 20
#https://adventofcode.com/2021/day/20
import re, time, copy, sys, math, pygame
from collections import defaultdict

f = open('input_day20.txt', 'r')
lines = f.readlines()
lines = [line.rstrip("\n") for line in lines]
f.close()

#input data in grid
algo = [1 if c=='#' else 0 for c in lines[0]]
grid = [[1 if c=='#' else 0 for c in line] for line in lines[2:]]
width = len(grid[0])
height = len(grid)
print(width,height)
outOfBoundsValue = 0 # special case for infinite out of bounds pixels that change value 

#input data in dictionary of lit positions
initGridDict = {}
for j,row in enumerate(grid):
    for i,v in enumerate(row):
        if v:
            initGridDict[(i,j)] = 1
print(len(initGridDict))

# display Data
minX,minY = 0,0
maxX = width
maxY = height
screenSize = 1300
cellSize = 3
cx= screenSize//2 - width*cellSize//2
cy= screenSize//2 - height*cellSize//2

neighbours = [(-1,-1),(0,-1),(1,-1),(-1,0),(0,0),(1,0),(-1,1),(0,1),(1,1)]


def getPixel(gridDict,x,y):
    if x>= minX and y>=minY and x<maxX and y<maxY:
        return gridDict.get((x,y)) or 0
    else:
        return outOfBoundsValue # all other pixels outside range are either all 1 or 0 depending on 

def pixelCode(gridDict,x,y):
   code = [str(getPixel(gridDict,x+dir[0],y+dir[1])) for dir in neighbours] 
   binaryStr = "".join(code)
   return int(binaryStr,2)

def evolveGrid(gridDict):
    newGrid = {}
    for x in range(minX-1,maxX+1):
        for y in range(minY-1,maxY+1):
            code = pixelCode(gridDict,x,y)
            val = algo[code]
            if (val):
                newGrid[(x,y)] = val
    return newGrid

def drawDict(surface,gridDict):
    size = screenSize//(cellSize*2)
    for x in range(50-size,50+size):
        for y in range(50-size,50+size):
            val = getPixel(gridDict,x,y)
            rect = (cx+x*cellSize,cy+y*cellSize,cellSize-1,cellSize-1)
            surface.fill((val*255,0,0),rect)

def drawDict2(surface,gridDict):
    for k,val in gridDict.items():
        rect = (cx+k[0]*cellSize,cy+k[1]*cellSize,cellSize-1,cellSize-1)
        surface.fill((val*255,0,0),rect)            

def displayCurrentStep(gridDict):
    surface.fill((0,0,0),(0,0,screenSize,screenSize))
    drawDict(surface,gridDict)
    pygame.display.update()

def doSteps(n):
    global minX,maxX,minY,maxY,outOfBoundsValue
    newGrid = initGridDict
    for i in range(n):
        print(len(newGrid))
#        if (i & 1) == 0:
        displayCurrentStep(newGrid)
        newGrid = evolveGrid(newGrid)
        minX -= 1
        maxX += 1
        minY -= 1
        maxY += 1       
        if algo[0]: # empty pixels become 1 and full pixels become 0 
            outOfBoundsValue = (outOfBoundsValue + 1) & 1
    print(len(newGrid))
    displayCurrentStep(newGrid)


def part1():
    doSteps(2)
    return

def part2():
    doSteps(50)
    return

pygame.init()
surface = pygame.display.set_mode((screenSize,screenSize))

print("----- Part1 ----")
startp1 = time.time()
displayPath  = part1()
endp1 = time.time()
print("{:.4f}s".format(endp1 - startp1))

print("----- Part2 ----")
startp2 = time.time()
part2()
endp2 = time.time()
print("{:.4f}s".format(endp2 - startp2))

