#Advent of code 2021: Day 5
#https://adventofcode.com/2021/day/5
import re, time, copy,numpy as np, math
from collections import defaultdict

f = open('input_day5.txt', 'r')
lines = f.readlines()
lines = [line.rstrip("\n") for line in lines]
f.close()

segments = [tuple(tuple(int(a) for a in b.split(',')) for b in line.split("->")) for line in lines]

hor_segmemts =[a for a in segments if a[0][1] == a[1][1]]
ver_segmemts =[a for a in segments if a[0][0] == a[1][0]]
diag_segmemts =[a for a in segments if abs(a[0][0] - a[1][0]) == abs(a[0][1] - a[1][1])]
print(diag_segmemts)


grid = defaultdict(int) 

def part1():
    global grid

    for seg in hor_segmemts:
        sort_seg = sorted((seg[0][0],seg[1][0]))
        for x in range(sort_seg[0],sort_seg[1]+1):
            grid[(x,seg[1][1])] += 1 

    for seg in ver_segmemts:
        sort_seg = sorted((seg[0][1],seg[1][1]))
        for y in range(sort_seg[0],sort_seg[1]+1):
            grid[(seg[1][0],y)] += 1 

    intersect = [k for k,v in grid.items() if v >= 2]
    print(len(intersect))
    return 

def part2():
    global grid

    for seg in diag_segmemts:
        x1 = seg[0][0]
        x2 = seg[1][0]    
        delta = math.copysign(1,seg[1][1]-seg[0][1])
        ys = seg[0][1]
        if x2 < x1: 
            delta = -delta
            ys = seg[1][1]
            x1 = seg[1][0]
            x2 = seg[0][0]  

        for x in range(x1,x2+1):
            grid[(x,ys)] += 1 
            ys += delta


    intersect = [k for k,v in grid.items() if v >= 2]
    print(len(intersect))

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