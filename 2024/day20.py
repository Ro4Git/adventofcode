#Advent of code 2024: Day 20
#https://adventofcode.com/2024/day/20
import re, time, copy , functools, itertools
from collections import defaultdict
import aoc
import sortedcontainers
import astar

lines = aoc.ReadPuzzleInput("input_day20.txt")
grid = aoc.ToGrid(lines)


display = aoc.Display(True, grid.width, grid.height,    4 , 1)

startPos = grid.Find('S')
endPos = grid.Find('E')
print(startPos,endPos)

def neighbors(n):
    result = []
    for dir in aoc.dirs4:
        nPos = aoc.addPos(n,dir)
        if not grid.IsOut(nPos):
            if grid.Val(nPos) != '#':
                result.append(nPos)
    return result

def distance(n1, n2):
    return 1

def goalFunction(n1, goal): 
    return n1 == goal

def cost(n1, n2):
    return aoc.manDist(n1,n2) 

resAStar = astar.find_path(startPos, endPos, neighbors_fnct=neighbors,
                            heuristic_cost_estimate_fnct=cost, distance_between_fnct=distance, is_goal_reached_fnct=goalFunction)

path = list(resAStar)

distToGoal = {}
startTime = len(path) - 1
print(startTime)

for i,pos in enumerate(path):
    distToGoal[pos] = (len(path)-1) - i
     
display.clear()
display.drawGrid(grid, lambda x: (0,0,0) if x=='.' else (194,100,0))
display.drawListPos(path,(100,255,100))
display.update()

def getShortcutSave(pos1,pos2):
    # oldCost = distToGoal[pos1]
    # new cost would be : length so far + shortcut cost + remaining from new pos
    # =  (startTime - distToGoal[pos1]) + aoc.manDist(pos1,pos2) + distToGoal[pos2]
    oldCost = distToGoal[pos1]
    newCost = aoc.manDist(pos1,pos2) + distToGoal[pos2] 
    return oldCost - newCost
 

def hasShortcuts(pos, dist):
    result = grid.FindValidInRange(pos,dist, lambda p,v: aoc.manDist(pos,p)<=dist and v != "#" and getShortcutSave(pos,p)>=100)
    return result
    
def part1():
    # for each position in path, check if there is another position within distance which 
    # dist is below 
    shortcutsPerPos = [hasShortcuts(pos,2) for pos in path]
    print(shortcutsPerPos)
    print(sum([len(pos) for pos in shortcutsPerPos]))

    return 

def part2():
    # for each node on the path, try one of the neighbour that was not selected as part of the path 
    # as alternaate
    shortcutsPerPos = [hasShortcuts(pos,20) for pos in path]
    print(shortcutsPerPos)
    print(sum([len(pos) for pos in shortcutsPerPos]))
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
