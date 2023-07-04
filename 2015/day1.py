#Advent of code 2015: Day 2
#https://adventofcode.com/2015/day/2
import re, time, copy

f = open('input_day1.txt', 'r')
lines = f.readlines()
lines = [line.rstrip("\n") for line in lines]
f.close()

dims = [1 if c=='(' else -1 for c in lines[0]]

def part1():
    print(sum(dims))

def part2():
    sum = 0
    for i,d in enumerate(dims):
        sum+=d
        if sum==-1:
            print(i+1)
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