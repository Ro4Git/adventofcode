#Advent of code 2024: Day 10
#https://adventofcode.com/2024/day/10
import re, time, copy , functools, itertools
from collections import defaultdict
import aoc

lines = aoc.ReadPuzzleInput("input_day10.txt")
grid = aoc.ToGrid(lines, lambda x : int(x) )

startPoints = grid.FindAll(0)
print(len(startPoints))


def findTrailHeads(startPos, part):
    explore = [startPos]
    for i in range(1,10):
        nextPath = []
        for pos in explore:
            nextPath.extend(grid.FindNeighbours(pos, lambda x : (x == i) ))
                            
        if (part == 1):
            explore = list(set(nextPath))
        else:
            explore = nextPath
        if len(explore) == 0:
            break
    
    return len(explore)


def part1():
    scoreTrailheads  = [findTrailHeads(startPos,1) for startPos in startPoints]
    print(scoreTrailheads)
    print(sum(scoreTrailheads))
    return 

def part2():
    ratingTrailheads  = [findTrailHeads(startPos,2) for startPos in startPoints]
    print(ratingTrailheads)
    print(sum(ratingTrailheads))    
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

