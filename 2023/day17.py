#Advent of code 2023: Day 17
#https://adventofcode.com/2023/day/17
import re, time, copy, math
import astar

f = open('input_day17.txt', 'r')
lines = f.readlines()
lines = [line.rstrip("\n") for line in lines]
f.close()

grid = [[int(c) for c in line] for line in lines]
width = len(grid[0])
height = len(grid)
dirs = [(1,0),(0,1),(-1,0),(0,-1)]
oppdirs = [2,3,0,1]

def addDelta(pos,delta):
    return (pos[0]+delta[0],pos[1]+delta[1])

def getGrid(node):
    return grid[node[0][1]][node[0][0]]

def neighborsPart1(n):
    pos = n[0]
    prevDir = n[1]
    nbPrevDir = n[2]
    for newDir,dirDelta in enumerate(dirs):
        newNbPrevDir = 1
        if oppdirs[newDir] != prevDir:
            newPos = addDelta(pos,dirDelta)
            if (newPos[0] >= 0 and newPos[0] < width and newPos[1] >= 0 and newPos[1] < height):
                if newDir == prevDir:
                    newNbPrevDir = nbPrevDir + 1 
                if newNbPrevDir<4:
                    yield (newPos,newDir,newNbPrevDir)

def neighborsPart2(n):
    pos = n[0]
    prevDir = n[1]
    nbPrevDir = n[2]
    for newDir,dirDelta in enumerate(dirs):
        if oppdirs[newDir] != prevDir:
            newPos = addDelta(pos,dirDelta)
            if (newPos[0] >= 0 and newPos[0] < width and newPos[1] >= 0 and newPos[1] < height):
                if newDir == prevDir or prevDir < 0:
                    if nbPrevDir<10:
                        yield (newPos,newDir,nbPrevDir + 1)
                else:
                    #trying to turn, can only do that if prevDir was at least 4
                    if nbPrevDir>=4:
                        yield (newPos,newDir,1)


def is_goal_reached( current, goal):
    return current[0] == goal[0]

def distancePart1(n1, n2):
    return getGrid(n2)

def cost(n1, n2):
    #heuristic: average heat loss per cell (5) x number of cells to parse to reach the goal
    return 5 * (abs(n2[0][0]-n1[0][0]) + abs(n2[0][1]-n1[0][1]))  

def part1():
    startPos = ((0,0),-1,0)
    endPos = ((width-1,height-1),-1,0)
    resAStar = astar.find_path(startPos, endPos, neighbors_fnct=neighborsPart1,
                                heuristic_cost_estimate_fnct=cost, distance_between_fnct=distancePart1, is_goal_reached_fnct=is_goal_reached)

    path = list(resAStar)
    heatloss = sum(getGrid(n) for n in path[1:])
    #print(path)
    print("Heatloss :",heatloss)
    return 

def part2():
    startPos = ((0,0),-1,0)
    endPos = ((width-1,height-1),-1,0)
    resAStar = astar.find_path(startPos, endPos, neighbors_fnct=neighborsPart2,
                                heuristic_cost_estimate_fnct=cost, distance_between_fnct=distancePart1, is_goal_reached_fnct=is_goal_reached)

    path = list(resAStar)
    heatloss = sum(getGrid(n) for n in path[1:])
    #print(path)
    print("Heatloss :",heatloss)
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