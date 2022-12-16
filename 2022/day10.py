#Advent of code 2022: Day 10
#https://adventofcode.com/2022/day/10
import re, time, copy
from collections import defaultdict

f = open('input_day10.txt', 'r')
lines = f.readlines()
lines = [line.rstrip("\n") for line in lines]
f.close()


cycles = []
value = 1 
cycle = 0
for line in lines: 
    cycles.append(value)
    tokens = line.split(" ")
    if len(tokens) == 2: 
        cycles.append(value)
        value += int(tokens[1])

print(cycles)


def part1():
    checks = [20,60,100,140,180,220]
    checkValues = [cycles[check-1]*check for check in checks]
    print(checkValues)
    print(sum(checkValues))
    return 

def part2():
    crt = ""
    for i,x in enumerate(cycles):
        pos = i % 40
        if (x-1 <= pos <= x+1):
            crt += "▓"
        else:
            crt += "."
        if ((i+1) % 40 == 0):
            print(crt)
            crt = "" 
    
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