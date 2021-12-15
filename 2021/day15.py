#Advent of code 2021: Day 15
#https://adventofcode.com/2021/day/15
import re, time, copy, math
from collections import defaultdict
import astar

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

    return

def part2():
    path = list(astar.find_path((0, 0), (width*5 - 1, height*5 - 1), neighbors_fnct=neighborsPart2,
                                heuristic_cost_estimate_fnct=cost, distance_between_fnct=distancePart2))
    print(path)

    totalCost = sum([distancePart2((0,0),n2)  for n2 in path[1:]])
    print(totalCost)

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