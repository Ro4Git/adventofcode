#Advent of code 2024: Day 18
#https://adventofcode.com/2024/day/18
import re, time, copy , functools, itertools
from collections import defaultdict
import aoc
import astar

lines = aoc.ReadPuzzleInput("input_day18.txt")
corruptPlaces = aoc.ToList(lines,',',lambda x:int(x))

width = 71
height = 71
grid = aoc.Grid(None, width,height)
display = aoc.Display(True, width, height,    4 , 1)

startPos = (0,0)
endPos = (width-1,height-1)

def corrupt(places, n):
    for pos in places[:n]:
        grid.Set(pos,'#')

def neighbors(n):
    result = []
    for dir in aoc.dirs4:
        nPos = aoc.addPos(n,dir)
        if not grid.IsOut(nPos):
            if grid.Val(nPos) == '.':
                result.append(nPos)
    return result

def distance(n1, n2):
    return 1

def goalFunction(n1, goal): 
    return n1 == goal

def cost(n1, n2):
    return aoc.manDist(n1,n2)

def part1():
    corrupt(corruptPlaces,min(1024,len(corruptPlaces)))
    
    resAStar = astar.find_path(startPos, endPos, neighbors_fnct=neighbors,
                                heuristic_cost_estimate_fnct=cost, distance_between_fnct=distance, is_goal_reached_fnct=goalFunction)
        
    if resAStar != None:
        path = list(resAStar)
        display.clear()
        display.drawGrid(grid, lambda x: (0,0,0) if x=='.' else (194,100,0))
        display.drawListPos(path,(100,255,100))
        display.update()
        print(len(path)-1)
    return 

def part2():
    global grid
    grid = aoc.Grid(None, width,height)
    
    prevResult = []
    for i in range(0,len(corruptPlaces)):
        pos = corruptPlaces[i]
        grid.Set(pos,'#')
        resAStar = astar.find_path(startPos, endPos, neighbors_fnct=neighbors,
            heuristic_cost_estimate_fnct=cost, distance_between_fnct=distance, is_goal_reached_fnct=goalFunction)
        print(i)
        if resAStar != None:
            path = list(resAStar)
            if path != prevResult:
                display.clear()
                display.drawGrid(grid, lambda x: (0,0,0) if x=='.' else (194,100,0))
                display.drawListPos(path,(100,255,100))
                display.update()
                display.capture()
                prevResult = path
        else:
            print("no path after",pos)
            break
    display.saveGif("day18_p2.gif")
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

display.wait()