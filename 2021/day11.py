#Advent of code 2021: Day 11
#https://adventofcode.com/2021/day/11
import re, time, copy, math
from collections import defaultdict
import pygame

f = open('input_day11.txt', 'r')
lines = f.readlines()
lines = [line.rstrip("\n") for line in lines]
f.close()

grid = []
for line in lines:
    grid.append([int(c) for c in line])
width = len(grid[0])
height = len(grid)

neighbours = [(-1,0),(-1,1),(0,1),(1,1),(1,0),(1,-1),(0,-1),(-1,-1)]

def increasePixel(pos):
    global grid
    if (pos[0] >= 0 and pos[0] < width and pos[1] >= 0 and pos[1] < height):
        h = grid[pos[1]][pos[0]]
        if (h > 9):
            return False
        grid[pos[1]][pos[0]] += 1
        if (grid[pos[1]][pos[0]] > 9):
            return True
    return False

def doStep():
    global grid
    flashThisStep = []
    #start by increasing all cells
    for y in range(height):
        for x in range(width):
            grid[y][x] += 1
            if grid[y][x]>9:
                flashThisStep.append((x,y))

    # flashes any one that reached 9
    while (len(flashThisStep)):
        pos = flashThisStep.pop()
        for delta in neighbours:
            pos2 = (pos[0] + delta[0], pos[1] + delta[1])
            if increasePixel(pos2):
                flashThisStep.append(pos2)
    #any cell that flashed is reset to 0
    for y in range(height):
        for x in range(width):
            if grid[y][x]>9:
                grid[y][x] = 0
                flashThisStep.append((x,y))
    return flashThisStep


def drawGrid(surface,grid, gridCellSize = 10):
    for y,row in enumerate(grid):
        for x,val in enumerate(row):
            rect = (x*(gridCellSize+1),y*(gridCellSize+1),gridCellSize,gridCellSize)
            surface.fill((val*25,val*25,val*25),rect)

def drawPath(surface,path, gridCellSize = 10):
    for p in path:
        x = p[0]
        y = p[1]
        rect = (x*(gridCellSize+1),y*(gridCellSize+1),gridCellSize,gridCellSize)
        surface.fill((255,0,0),rect)

pygame.init()
surface = pygame.display.set_mode((600,600))



def part1():
    totalFlash = 0
    for i in range(100):
        flashes = doStep()
        totalFlash += len(flashes)
        drawGrid(surface,grid,30)
        drawPath(surface,flashes,30)
        pygame.display.update()
        pygame.time.delay(25)

    print(totalFlash)
    return

def part2():
    step = 100
    sumGrid = sum([sum(row) for row in grid])
    while sumGrid != 0:
        flashes = doStep()
        step += 1
        sumGrid = sum([sum(row) for row in grid])
        drawGrid(surface,grid,30)
        drawPath(surface,flashes,30)
        pygame.display.update()
        pygame.time.delay(25)        
    print(step)
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

pygame.quit()
