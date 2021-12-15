#Advent of code 2021: Day 13
#https://adventofcode.com/2021/day/13
import re, time, copy, math
from collections import defaultdict

f = open('input_day13.txt', 'r')
lines = f.readlines()
lines = [line.rstrip("\n") for line in lines]
f.close()

cells = []
folds = []
for line in lines:
    tokens = line.split(',')
    if len(tokens) == 2:
        cells.append((int(tokens[0]),int(tokens[1])))
    elif line.startswith("fold along x="):
        x = int(line[13:])
        folds.append((x,0))
    elif line.startswith("fold along y="):
        y = int(line[13:])
        folds.append((0,y))


print(cells)
print(folds)



def foldX(axis,cells):
    newcells = [c if c[0]<axis else (2*axis-c[0],c[1])for c in cells]
    return list(dict.fromkeys(newcells))

def foldY(axis,cells):
    newcells = [c if c[1]<axis else (c[0],2*axis-c[1])for c in cells]
    return list(dict.fromkeys(newcells))

def fold(axis,cells):
    if (axis[0] != 0):
        return foldX(axis[0],cells)
    else:
        return foldY(axis[1],cells)

def part1():
    newcells = fold(folds[0],cells)
    print(len(newcells))
    return

def printGrid(cells):
    width = max([c[0] for c in cells])
    height = max([c[1] for c in cells])
    for y in range(height+1):
        str = ""
        for x in range(width+1):
            if ((x,y) in cells):
                str += '█'
            else:
                str += '..'
        print(str)



def part2():
    newcells = cells
    for f in folds:
        newcells = fold(f,newcells)

    printGrid(newcells)
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