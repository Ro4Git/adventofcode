#Advent of code 2022: Day 24
#https://adventofcode.com/2022/day/24
import re, time, copy, functools,sys
from collections import defaultdict
import pygame
import astar

maxFuture = 800

f = open('input_day24.txt', 'r')
lines = f.readlines()
lines = [line.rstrip("\n") for line in lines]
f.close()

code = {'.':0,'#':-1,'>':1,'v':2,'<':3,'^':4}
dirs = [(1,0),(0,1),(-1,0),(0,-1)]
currentOrder = 0
width = max([len(line) for line in lines])
height = len(lines)
grid = [[code[c] for c in line] for line in lines]
emptyGrid = [[min(c,0) for c in row] for row in grid]
blizzards = [[] for d in dirs]
futureGrids = [grid]

def add(pos1,pos2):
    return (pos1[0]+pos2[0],pos1[1]+pos2[1])

for y,row in enumerate(grid):
    for x,c in enumerate(row):
        if c>0:
            blizzards[c-1].append((x,y))

def computeFutureGrids(future):
    global blizzards
    global futureGrids
    for f in range(future):
        for index,dir in enumerate(dirs):
            newblizzard = []
            for bliz in blizzards[index]:
                newPos = add(bliz,dir)
                if newPos[0] <= 0: newPos = (width-2, newPos[1])
                if newPos[0] >= width-1: newPos =  (1, newPos[1])
                if newPos[1] <= 0: newPos = (newPos[0], height-2)
                if newPos[1] >= height-1:  newPos = (newPos[0], 1)
                newblizzard.append(newPos)
            blizzards[index] = newblizzard
        tempGrid = copy.deepcopy(emptyGrid)
        for index in range(4):
            for bliz in blizzards[index]:
                tempGrid[bliz[1]][bliz[0]] = index + 1
        #display1(tempGrid)
        futureGrids.append(tempGrid)

pygame.init()
surface = pygame.display.set_mode((width*8,height*8))

colors = [(0,0,0),(255,0,0),(0,255,0),(255,0,255),(0,255,255)]
arrows = [((0,0),(8,4),(0,8)),((0,0),(8,0),(4,8)),((8,0),(8,8),(0,4)),((0,8),(4,0),(8,8))]

def arrowPolygon(x,y,dir):
    return [(x+dx,y+dy) for dx,dy in arrows[dir]]

def drawGrid(surface,grid):
    for y,row in enumerate(grid):
        for x,val in enumerate(row):
            rect = ((x)*8,(y)*8,8,8)
            surface.fill((0,0,0),rect)
            if val<0:
                surface.fill((255,255,255),rect)
            elif val>0:
                pygame.draw.polygon(surface,(128,128,128),arrowPolygon(x*8,y*8,val-1))

def display1(path):
    for p in path:
        time.sleep(0.1)
        drawGrid(surface,futureGrids[p[0]])
        rect = ((p[1][0])*8,(p[1][1])*8,8,8)
        surface.fill((255,0,0),rect)
        pygame.display.update()     
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()     

def neighbors(n):
    currentTime = n[0]
    futureTime = currentTime + 1
    if futureTime >= maxFuture:
        return 
    currentPos = n[1]
    futureGrid = futureGrids[futureTime]
    for dir in dirs: 
        newPos = add(currentPos,dir)
        if 0 <= newPos[0] <= width-1 and 0 <= newPos[1] <= height-1 and futureGrid[newPos[1]][newPos[0]]==0:
            yield (futureTime,newPos)
    if futureGrid[currentPos[1]][currentPos[0]]==0:
        yield (futureTime,currentPos)

def distance(n1, n2):
    return 1

def goalFunction(n1, goal): 
    if n1[1] == goal[1]:
        return True
    return False

def cost(n1, n2):
    return abs(n2[1][0]-n1[1][0]) + abs(n2[1][1]-n1[1][1])


startPos = (1,0)
endPos = (width-2,height-1)
lastVisitedNode = None

def part1():
    global lastVisitedNode
    computeFutureGrids(maxFuture)
    resAStar = astar.find_path((0,startPos), (0,endPos), neighbors_fnct=neighbors,
                                heuristic_cost_estimate_fnct=cost, distance_between_fnct=distance, is_goal_reached_fnct=goalFunction)
    if resAStar != None:
        path = list(resAStar)
        lastVisitedNode = path[-1]
        print(lastVisitedNode[0])
        display1(path)
    return

def part2():
    global lastVisitedNode
    resAStarBack = astar.find_path(lastVisitedNode, (0,startPos), neighbors_fnct=neighbors,
                                heuristic_cost_estimate_fnct=cost, distance_between_fnct=distance, is_goal_reached_fnct=goalFunction)
    if resAStarBack != None:
        path = list(resAStarBack)
        lastVisitedNode = path[-1]
        print(lastVisitedNode[0])
        display1(path)

        resAStarSecond = astar.find_path(lastVisitedNode, (0,endPos), neighbors_fnct=neighbors,
                                    heuristic_cost_estimate_fnct=cost, distance_between_fnct=distance, is_goal_reached_fnct=goalFunction)

        if resAStarSecond != None:
            path = list(resAStarSecond)
            lastVisitedNode = path[-1]
            print(lastVisitedNode[0])
            display1(path)
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
