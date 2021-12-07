#Advent of code 2021: Day 7
#https://adventofcode.com/2021/day/7
import re, time, copy
from collections import defaultdict

f = open('input_day7.txt', 'r')
lines = f.readlines()
lines = [line.rstrip("\n") for line in lines]
f.close()

positions = [int(n) for n in lines[0].split(',')]
posmin = min(positions)
posmax = max(positions)


def moveCost(n):
    distances = [abs(p-n) for p in positions]
    return sum(distances)

def moveCost2(n):
    distances = [(abs(p-n)*(1+abs(p-n)))//2 for p in positions]
    return sum(distances)

def part1():
    minCost = min([moveCost(p) for p in range(posmin,posmax)])
    print(minCost)
    return 

def part2():
    minCost = min([moveCost2(p) for p in range(posmin,posmax)])
    print(minCost)
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