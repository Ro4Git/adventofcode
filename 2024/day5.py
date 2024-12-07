#Advent of code 2024: Day 5
#https://adventofcode.com/2024/day/5
import re, time, copy , functools
from collections import defaultdict
import aoc

lines = aoc.ReadPuzzleInput("input_day5.txt")
sections = aoc.ToSections(lines)
rules = aoc.ToList(sections[0], int, "|") 
updates = aoc.ToList(sections[1], int, ",")

afters = defaultdict(set)
befores = defaultdict(set)

for left,right in rules: 
    afters[left].add(right)
    befores[right].add(left)

def compare(a,b):
    if a in afters[b]:
        return 1
    elif a in befores[b]:
        return -1
    return 0

def checkUpdate(update): 
    sorted_update = sorted(update,key = functools.cmp_to_key(compare))
    return sorted_update == update

def fixUpdate(update): 
    if checkUpdate(update):
        return [0]
    fixed2 = sorted(update,key = functools.cmp_to_key(compare))
    return fixed2

def part1():
    mids = [ update[len(update)//2] for update in updates if checkUpdate(update)]
    print(sum(mids))
    return 

def part2():
    mids = []
    for update in updates:
        fixed = fixUpdate(update)
        mids.append(fixed[len(fixed)//2])
    print(sum(mids))    
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