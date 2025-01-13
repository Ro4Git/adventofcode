#Advent of code 2024: Day 25
#https://adventofcode.com/2024/day/25
import re, time, copy , functools, itertools
from collections import defaultdict
import aoc

lines = aoc.ReadPuzzleInput("input_day25.txt")

sections = aoc.ToSections(lines)

grids = [aoc.ToGrid(section, lambda x : 1 if x=='#' else 0) for section in sections]

locks = [grid for grid in grids if grid.Val((0,0))==1]
keys = [grid for grid in grids if grid.Val((0,0))==0]
overlaps = [key.Add(lock).Has(lambda x: x>=2) for lock,key in itertools.product(locks,keys)]

print(overlaps.count(False))

def part1():
    nbValid = 0
    overlapPairs = []
    for key in keys:
        for lock in locks:
            ngrid = key.Add(lock)
            if ngrid.Has(lambda x: x>=2):
                overlapPairs.append((key,lock))
            else:
                nbValid += 1
    print(nbValid)
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

