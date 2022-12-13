#Advent of code 2022: Day 1
#https://adventofcode.com/2022/day/1
import re, time, copy

f = open('input_day1.txt', 'r')
lines = f.readlines()
lines = [line.rstrip("\n") for line in lines]
f.close()

calories = []
currentElve = []
for line in lines:
    if len(line)>1:
        currentElve.append(int(line))
    else:
        calories.append(currentElve)
        currentElve = []

def part1():
    print(len(calories))
    return 

def part2():
    elveCal = []
    for elve in calories:
        cal = sum(elve)
        elveCal.append(cal)

    elveCal.sort()    
    topThreee = elveCal[-1]+elveCal[-2]+elveCal[-3]
    print(topThreee)
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