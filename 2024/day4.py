#Advent of code 2024: Day 4
#https://adventofcode.com/2024/day/4
import re, time, copy 
import aoc

lines = aoc.ReadPuzzleInput("input_day4.txt")


grid = aoc.ToGrid(lines)

key = ["X","M","A","S"]


def hasXMas(startPos): 
    nbValid = 0
    for i,dir in enumerate(aoc.dirs8):
        pos = startPos
        valid = True
        for k in key: 
            if grid.IsOut(pos):
                valid = False
                break
            if (grid.Val(pos) != k):
                valid = False
                break
            pos = aoc.addPos(pos,dir)
        if valid:
            nbValid += 1
    return nbValid

def hasXMas2(startPos): 
    nbValid = 0
    if (grid.Val(startPos) != "A"):
        return 0
    if (grid.ValNext(startPos, (-1,-1)) == "M" and grid.ValNext(startPos, (-1,1)) == "M" and grid.ValNext(startPos, (1,-1)) == "S" and grid.ValNext(startPos, (1,1)) == "S"):
        return 1
    if (grid.ValNext(startPos, (-1,-1)) == "S" and grid.ValNext(startPos, (-1,1)) == "S" and grid.ValNext(startPos, (1,-1)) == "M" and grid.ValNext(startPos, (1,1)) == "M"):
        return 1
    if (grid.ValNext(startPos, (-1,-1)) == "M" and grid.ValNext(startPos, (-1,1)) == "S" and grid.ValNext(startPos, (1,-1)) == "M" and grid.ValNext(startPos, (1,1)) == "S"):
        return 1
    if (grid.ValNext(startPos, (-1,-1)) == "S" and grid.ValNext(startPos, (-1,1)) == "M" and grid.ValNext(startPos, (1,-1)) == "S" and grid.ValNext(startPos, (1,1)) == "M"):
        return 1

    return 0

def part1():
    nbXmas = 0
    for y in range(grid.height):
        for x in range(grid.width):
            nbXmas = nbXmas + hasXMas((x,y))
    print(nbXmas)
    return 

def part2():
    nbXmas = 0
    for y in range(1,grid.height-1):
        for x in range(1,grid.width-1):
            nbXmas = nbXmas + hasXMas2((x,y))
    print(nbXmas)
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