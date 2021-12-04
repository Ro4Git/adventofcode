#Advent of code 2021: Day 1
#https://adventofcode.com/2021/day/1
import re, time, copy

f = open('input_day1.txt', 'r')
lines = f.readlines()
f.close()

values = [int(v) for v in lines]

def part1():
    preval = values[0]
    increased = 0
    for i,val in enumerate(values):
        if val > preval:
            increased += 1
        preval = val
    print(increased)
    return 

def part2():
    preval = values[0] + values[1] + values[2]
    increased = 0
    for i,val in enumerate(values[3:]):
        newsum = preval + val - values[i]
        if newsum > preval:
            increased += 1
        preval = newsum
    print(increased)
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