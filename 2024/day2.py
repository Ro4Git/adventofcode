#Advent of code 2024: Day 2
#https://adventofcode.com/2024/day/2
import re, time, copy 
import aoc

lines = aoc.ReadPuzzleInput("input_day2.txt")

nums = [[int(num) for num in line.split(" ")] for line in lines]

def safeList(report): 
    prev = report[0]
    prevdelta = 0
    for i in range(1,len(report)): 
        cur = report[i]
        delta = cur - prev
        # at least one and at most 3
        if abs(delta) < 1 or abs(delta)>3:
            return False
        # increasing or decreasing
        if delta * prevdelta < 0:
            return False
        prevdelta = delta
        prev = cur
    return True
        
def safeList2(report): 
    for i,n in enumerate(report):
        newreport = report.copy()
        newreport.pop(i)
        if safeList(newreport):
            return True
    return False


def part1():
    valids = [1 if safeList(num) else 0 for num in nums]
    print(valids.count(1))

    return 

def part2():
    valids = [1 if safeList2(num) else 0 for num in nums]
    print(valids.count(1))
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