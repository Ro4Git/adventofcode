#Advent of code 2021: Day 15
#https://adventofcode.com/2021/day/15
import re, time, copy, math, sys
import astar
import pygame

f = open('input_day15.txt', 'r')
lines = f.readlines()
lines = [line.rstrip("\n") for line in lines]
f.close()

grid = []
for line in lines:
    grid.append([int(c) for c in line])
width = len(grid[0])
height = len(grid)

directions = [(-1,0),(0,1),(1,0),(0,-1)]

def neighborsPart1(n):
    for dir in directions:
        pos = (n[0]+dir[0],n[1]+dir[1])
        if (pos[0] >= 0 and pos[0] < width and pos[1] >= 0 and pos[1] < height):
            yield pos

def distancePart1(n1, n2):
    return grid[n2[1]][n2[0]]

def neighborsPart2(n):
    for dir in directions:
        pos = (n[0]+dir[0],n[1]+dir[1])
        if (pos[0] >= 0 and pos[0] < width*5 and pos[1] >= 0 and pos[1] < height*5):
            yield pos

def distancePart2(n1, n2):
    x = n2[0] % width
    y = n2[1] % height
    dx = n2[0] // width
    dy = n2[1] // height
    risk = grid[y][x] + dx + dy
    while risk > 9:
        risk = risk - 9
    return risk

def cost(n1, n2):
    return 0


def part1():
    path = list(astar.find_path((0, 0), (width - 1, height - 1), neighbors_fnct=neighborsPart1,
                                heuristic_cost_estimate_fnct=cost, distance_between_fnct=distancePart1))

    print(path)

    totalCost = sum([grid[n2[1]][n2[0]] for n2 in path[1:]])
    print(totalCost)

    return path

def part2():
    path = list(astar.find_path((0, 0), (width*5 - 1, height*5 - 1), neighbors_fnct=neighborsPart2,
                                heuristic_cost_estimate_fnct=cost, distance_between_fnct=distancePart2))
    print(path)

    totalCost = sum([distancePart2((0,0),n2)  for n2 in path[1:]])
    print(totalCost)
    return

def drawGrid(surface,grid):
    for y,row in enumerate(grid):
        for x,val in enumerate(row):
            rect = (x*6,y*6,5,5)
            surface.fill((val*25,val*25,val*25),rect)

def drawPath(surface,path):
    for p in path:
        x = p[0]
        y = p[1]
        rect = (x*6,y*6,5,5)
        val = grid[y][x]
        surface.fill((val*25,0,0),rect)

pygame.init()
surface = pygame.display.set_mode((600,600))

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


while True:
    drawGrid(surface,grid)
    drawPath(surface,displayPath)
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
