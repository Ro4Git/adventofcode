#Advent of code 2022: Day 14
#https://adventofcode.com/2022/day/14
import re, time, copy, functools
import pygame

f = open('input_day14.txt', 'r')
lines = f.readlines()
lines = [line.rstrip("\n") for line in lines]
f.close()

minx = miny = 100000
maxx = maxy = -100000
startPos = (500,0)
rocks = []
walls = [line.split("->") for line in lines]
for wall in walls:
    rockGroup = []
    for coords in wall: 
        tokens = coords.split(",")
        x = int(tokens[0])
        y = int(tokens[1])
        minx = min(minx,x)
        maxx = max(maxx,x)
        miny = min(miny,y)
        maxy = max(maxy,y)
        rockGroup.append((x,y))

    rocks.append(rockGroup)

print(minx,miny,maxx,maxy)
height = (maxy - miny)+5
width = 2*height + (maxx - minx)+1

grid =[]


def putRocks():
    global grid
    grid =[]
    clearLine = [0]*width
    for i in range(maxy+10):
        grid.append(clearLine.copy())    
    for rockGroup in rocks:
        for i in range(len(rockGroup)-1):
            putline(rockGroup[i],rockGroup[i+1])

def putline(pos1,pos2):
    xStart = min(pos1[0],pos2[0])
    xEnd = max(pos1[0],pos2[0])+1
    yStart = min(pos1[1],pos2[1])
    yEnd = max(pos1[1],pos2[1])+1
    for y in range(yStart,yEnd):
        for x in range(xStart,xEnd):
            putPixel((x,y),1)

def getPixel(pos):
    if (pos[1] >= maxy+2):
        return 1
    return grid[pos[1]][pos[0]-500+width//2]

def putPixel(pos,color):
    global grid
    
    grid[pos[1]][pos[0]-500+(width//2)] = color

def drawGrid(surface,grid):
    for y,row in enumerate(grid):
        for x,val in enumerate(row):
            rect = (x*2,y*2,2,2)
            surface.fill((val*127,(val & 1)*255,(val & 1)*255),rect)

def addPos(pos,add):
    return (pos[0]+add[0],pos[1]+add[1])

def addSalt(limit):
    pos = startPos
    testPos = [(0,1),(-1,1),(1,1)]
    
    while pos[1]<limit:
        npos = pos
        tpos = pos
        for test in testPos:
            tpos = addPos(pos,test)
            if getPixel(tpos)==0:
                pos = tpos
                break
        if npos == pos:
            putPixel(npos,2)
            return npos
    return pos





pygame.init()
surface = pygame.display.set_mode(((width+height)*2,height*2))

def display():
    drawGrid(surface,grid)
    pygame.display.update()     
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()           


def part1():
    putRocks()

    nbGrainStable = 0
    pos = startPos
    while pos[1]<maxy:
        nbGrainStable+=1
        pos = addSalt(maxy)

        if (nbGrainStable % 10)==0:
            display() 

    print(nbGrainStable-1)
    return

def part2():
    putRocks()

    nbGrainStable = 0
    pos = (0,0)
    while pos != startPos:
        nbGrainStable+=1
        pos = addSalt(maxy+2)

        if (nbGrainStable % 300)==0:
            display()

    print(nbGrainStable)    
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

while True:
    drawGrid(surface,grid)
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()