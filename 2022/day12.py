#Advent of code 2022: Day 12
#https://adventofcode.com/2022/day/12
import re, time, copy
import astar


f = open('input_day12.txt', 'r')
lines = f.readlines()
lines = [line.rstrip("\n") for line in lines]
f.close()

grid = []
startPos = (0,0)
endPos = (0,0)
for i,line in enumerate(lines):
    grid.append([ord(c) for c in line])
    for j,c in enumerate(line):
        if c == "S": 
            startPos = (j,i)
            grid[i][j] = ord('a')
        if c == "E": 
            endPos = (j,i)
            grid[i][j] = ord('z')

width = len(grid[0])
height = len(grid)

directions = [(-1,0),(0,1),(1,0),(0,-1)]

def neighborsPart1(n):
    for dir in directions:
        pos = (n[0]+dir[0],n[1]+dir[1])
        valN = grid[n[1]][n[0]]
        if (pos[0] >= 0 and pos[0] < width and pos[1] >= 0 and pos[1] < height):
            valP = grid[pos[1]][pos[0]]
            cost = valP - valN
            if cost <= 1:
                yield pos

def neighborsPart2(n):
    for dir in directions:
        pos = (n[0]+dir[0],n[1]+dir[1])
        valN = grid[n[1]][n[0]]
        if (pos[0] >= 0 and pos[0] < width and pos[1] >= 0 and pos[1] < height):
            valP = grid[pos[1]][pos[0]]
            cost = valP - valN
            if cost <= 1 and valP != ord('a'):
                yield pos                

def distancePart1(n1, n2):
    return 1

def cost(n1, n2):
    return 1



def part1():
    resAStar = astar.find_path(startPos, endPos, neighbors_fnct=neighborsPart1,
                                heuristic_cost_estimate_fnct=cost, distance_between_fnct=distancePart1)

    path = list(resAStar)
    print(len(path)-1)
    return


def part2():
    minSteps = 100000
    for i in range(height):
        for j in range(width):
            if (grid[i][j] == ord('a')):            
                resAStar = astar.find_path((j,i), endPos, neighbors_fnct=neighborsPart2,
                                            heuristic_cost_estimate_fnct=cost, distance_between_fnct=distancePart1)

                if (resAStar != None):
                    path = list(resAStar)
                    steps = len(path)-1
                    if (steps < minSteps):
                        minSteps = steps
                        print(minSteps)
            
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