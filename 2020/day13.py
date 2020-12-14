#Advent of code 2020: Day 13
#https://adventofcode.com/2020/day/13
from functools import reduce
import time

f = open('input_day13.txt', 'r')
lines = f.readlines()
f.close()

earliest_ts = int(lines[0]) 
numbers = [int(a) for a in lines[1].replace(",x","").split(",")]
numbersall = [int(a) if a != "x" else 0 for a in lines[1].split(",")]
print("-----------")
print(numbers)
print(numbersall)
print("-----------")


def part1():
    nearests_up = [(1+(earliest_ts // n)) * n for n in numbers]
    deltas = [n - earliest_ts  for n in nearests_up]
    minindex = deltas.index(min(deltas)) 
    print(minindex, deltas[minindex], numbers[minindex], deltas[minindex] * numbers[minindex])


def part2():
    remainders = [(delta,val) if val!=0 else (0,0) for delta,val in enumerate(numbersall)]
    remainders = list(filter(lambda a: a != (0,0), remainders)) 
    print(remainders)
    currentProd = 1
    global earliest_ts
    for remainder,val in remainders:
        while ((earliest_ts + remainder) % val != 0):
            earliest_ts += currentProd
        currentProd *= val
    print(earliest_ts)

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