#Advent of code 2021: Day 25
#https://adventofcode.com/2021/day/25
import re, time, copy, sys, math, pygame

f = open('input_day25.txt', 'r')
lines = f.readlines()
lines = [line.rstrip("\n") for line in lines]
f.close()

convert = {".":0,">":1,"v":2}
grid = []
grid = [ [convert[c] for c in line] for line in lines]
width = len(grid[0])
height = len(grid)

# display Data
screenSize = 800
cellSize = 3
cx = screenSize//2 - width*cellSize//2
cy = screenSize//2 - height*cellSize//2

def stepHorizontal():
    global hasChanged
    ngrid = copy.deepcopy(grid)
    for y,row in enumerate(grid):
        for x,c in enumerate(row[:-1]):
            if c == 1 and row[x+1] == 0: 
                ngrid[y][x+1] = 1
                ngrid[y][x] = 0
                hasChanged = True
        if row[width-1] == 1 and row[0] == 0:    
            ngrid[y][0] = 1
            ngrid[y][width-1] = 0
            hasChanged = True
    return ngrid

def stepVertical():
    global hasChanged
    ngrid = copy.deepcopy(grid)
    for x in range(width):
        for y in range(height-1):
            if grid[y][x] == 2 and grid[y+1][x] == 0: 
                ngrid[y+1][x] = 2
                ngrid[y][x] = 0
                hasChanged = True
        if grid[height-1][x] == 2 and grid[0][x] == 0: 
            ngrid[0][x] = 2
            ngrid[height-1][x] = 0
            hasChanged = True
    return ngrid


pygame.init()
surface = pygame.display.set_mode((screenSize,screenSize))

def drawGrid(surface,grid):
    for y,row in enumerate(grid):
        for x,val in enumerate(row):
            rect = (cx+x*cellSize,cy+y*cellSize,cellSize-1,cellSize-1)
            surface.fill((val*127,255 if val==1 else 0,val*127),rect)

def displayCurrentStep(grid):
    surface.fill((0,0,0),(0,0,screenSize,screenSize))
    drawGrid(surface,grid)
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

def part1():
    global grid
    global hasChanged
    hasChanged = True
    stepCount = 0
    while hasChanged:
        hasChanged = False
        grid = stepHorizontal()
        grid = stepVertical()
        displayCurrentStep(grid)
        stepCount += 1
        print(stepCount)
    return

def part2():
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

