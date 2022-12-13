#Advent of code 2022: Day 4
#https://adventofcode.com/2022/day/4
import re, time, copy

f = open('input_day4.txt', 'r')
lines = f.readlines()
lines = [line.rstrip("\n") for line in lines]
f.close()

#range [Elve1_start,Elve1_end,Elve2_start,Elve2_end]
ranges = [[int(n) for n in rng] for rng in [rng[0].split("-") + rng[1].split("-") for rng in [line.split(",") for line in lines]]]
print(ranges)

def part1():
    fullOverlaps = 0
    fullOverlaps =  sum([int((rng[2]>=rng[0] and rng[3]<=rng[1]) or (rng[2]<=rng[0] and rng[3]>=rng[1])) for rng in ranges])
    print(fullOverlaps)
    return 

def part2():
    partialOverlaps = 0
    partialOverlaps =  sum([int(not (rng[3]<rng[0] or rng[2]>rng[1])) for rng in ranges])
    print(partialOverlaps)    
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