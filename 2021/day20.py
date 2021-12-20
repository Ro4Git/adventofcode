#Advent of code 2021: Day 20
#https://adventofcode.com/2021/day/20
import re, time, copy, sys, math, pygame
from collections import defaultdict

f = open('input_day20.txt', 'r')
lines = f.readlines()
lines = [line.rstrip("\n") for line in lines]
f.close()

algo = [1 if c=='#' else 0 for c in lines[0]]
grid = [[1 if c=='#' else 0 for c in line] for line in lines[2:]]
width = len(grid[0])
height = len(grid)

minX = 0
maxX = width
minY = 0
maxY = height
screenSize = 1300

cx= screenSize//2 - width*3
cy= screenSize//2 - height*3

print(width,height)

initGridDict = {}
for j,row in enumerate(grid):
    for i,v in enumerate(row):
        if v:
            initGridDict[(i,j)] = 1

print(len(initGridDict))
#algo[0] = 0

neighbours = [(-1,-1),(0,-1),(1,-1),(-1,0),(0,0),(1,0),(-1,1),(0,1),(1,1)]
defaultValue = 0

def getPixel(gridDict,x,y):
    if x>= minX and y>=minY and x<maxX and y<maxY:
        return gridDict.get((x,y)) or 0
    else:
        return defaultValue # all other pixels outside range are either all 1 or 0 depending on 

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
    size = screenSize//12
    for x in range(50-size,50+size):
        for y in range(50-size,50+size):
            val = getPixel(gridDict,x,y)
            rect = (cx+x*6,cy+y*6,5,5)
            surface.fill((val*255,0,0),rect)

def drawDict2(surface,gridDict):
    for k,val in gridDict.items():
        rect = (cx+k[0]*6,cy+k[1]*6,5,5)
        surface.fill((val*255,0,0),rect)            

def displayCurrentStep(gridDict):
    while True:
        surface.fill((0,0,0),(0,0,screenSize,screenSize))
        drawDict2(surface,gridDict)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                return

def part1():
    global minX,maxX,minY,maxY,defaultValue
    newGrid = initGridDict
    for i in range(2):
        print(len(newGrid))
        displayCurrentStep(newGrid)
        newGrid = evolveGrid(newGrid)
        minX -= 1
        maxX += 1
        minY -= 1
        maxY += 1       
        if algo[0]:
            defaultValue = (defaultValue + 1) & 1
    print(len(newGrid))
    displayCurrentStep(newGrid)
    return

def part2():
    global minX,maxX,minY,maxY,defaultValue
    newGrid = initGridDict
    for i in range(50):
        print(len(newGrid))
        displayCurrentStep(newGrid)
        newGrid = evolveGrid(newGrid)
        minX -= 1
        maxX += 1
        minY -= 1
        maxY += 1       
        if algo[0]:
            defaultValue = (defaultValue + 1) & 1
    print(len(newGrid))
    displayCurrentStep(newGrid)
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

