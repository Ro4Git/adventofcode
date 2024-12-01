#Advent of code 2024: Day 1
#https://adventofcode.com/2024/day/1
import re, time, copy 
import aoc

lines = aoc.ReadPuzzleInput("input_day1.txt")

numsL = [int(line.split("   ")[0]) for line in lines]
numsR = [int(line.split("   ")[1]) for line in lines]

def part1():
    numsL.sort()
    numsR.sort()
    dists = [abs(l-r) for l,r in zip(numsL,numsR)]
    print (sum(dists))
    return 

def part2():
    occurences = [numsR.count(l)*l for l in numsL]
    print (sum(occurences))


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