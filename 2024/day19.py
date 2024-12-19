#Advent of code 2024: Day 19
#https://adventofcode.com/2024/day/19
import re, time, copy , functools, itertools
from collections import defaultdict
import aoc

lines = aoc.ReadPuzzleInput("input_day19.txt")
sections = aoc.ToSections(lines)
patterns = sections[0][0].split(", ")
designs = sections[1]

#white (w), blue (u), black (b), red (r), or green (g).
patterns.sort(reverse = False, key = lambda x : len(x) + x.count('u')*100)
print(patterns)
print(len(designs))

@functools.cache
def isPossible(design):
    if len(design) == 0:
        return 1
    else:
        valids = 0
        for pat in patterns:
            if design.startswith(pat):
                valids += isPossible(design[len(pat):])
        return valids
    
valids = []

def part1():
    global valids
    valids = [isPossible(design) for design in designs]
    print(sum([c>0 for c in valids]))
    return 

def part2():
    print(sum([c for c in valids]))
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

