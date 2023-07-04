#Advent of code 2015: Day 2
#https://adventofcode.com/2015/day/2
import re, time, copy

f = open('input_day2.txt', 'r')
lines = f.readlines()
lines = [line.rstrip("\n") for line in lines]
f.close()

dims = [sorted([int(n) for n in line.split('x')]) for line in lines]

def part1():
    surfaces = [3*d[0]*d[1]+2*d[1]*d[2]+2*d[2]*d[0] for d in dims]
    print(sum(surfaces))

def part2():
    ribbon = [2*(d[0]+d[1])+d[1]*d[2]*d[0] for d in dims]
    print(sum(ribbon))

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