#Advent of code 2024: Day 7
#https://adventofcode.com/2024/day/7
import re, time, copy , functools
from collections import defaultdict
import aoc

lines = aoc.ReadPuzzleInput("input_day7.txt")
equationsStr = aoc.ToList(lines,": ")
equations = [[int(a),[int(c) for c in b.split(" ")]] for a,b in equationsStr]

def explore(test, val, remaining):
    if (val > test):
        return False
    if len(remaining) == 0: 
        return test == val
    val1 = val * remaining[0]
    val2 = val + remaining[0]
    return explore(test, val1, remaining[1:]) or explore(test, val2, remaining[1:])

def explore2(test, val, remaining):
    if (val > test):
        return False
    if len(remaining) == 0: 
        return test == val
    val1 = val * remaining[0]
    val2 = val + remaining[0]
    val3 = int( str(val) + str(remaining[0]))
    return explore2(test, val1, remaining[1:]) or explore2(test, val2, remaining[1:]) or explore2(test, val3, remaining[1:])

def part(exploreFunc):
    validEquations = []
    validResults =  []
    for equation in equations:
        if (exploreFunc(equation[0],equation[1][0],equation[1][1:])):
            validEquations.append(equation)
            validResults.append(equation[0])
    print(sum(validResults))    

def part1():
    part(explore)
    return 

def part2():
    part(explore2)
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