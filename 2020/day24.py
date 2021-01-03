#Advent of code 2020: Day 24  
#https://adventofcode.com/2020/day/24
import re,sys,copy
import math,time,itertools
from functools import reduce

f = open('input_day24.txt', 'r')
lines = f.readlines()
f.close()

dirs = {"e":(1,0),"se":(1,-1),"sw":(0,-1),"w":(-1,0),"nw":(-1,1),"ne":(0,1)}

def dir2Coord(directions):
    index = 0 
    c = directions[index]
    pos = (0,0)
    while c!= "\n":
        if c == "n" or c == "s":
            c += directions[index+1]
            index += 2
        else:
            index += 1
        d = dirs[c]
        pos = (pos[0]+d[0],pos[1]+d[1])
        c = directions[index]
    return pos


def part1():
    flipTile = {}
    allPos = []
    for l in lines:
        npos = dir2Coord(l)
        if npos in flipTile:
            flipTile[npos] += 1
        else:
            flipTile[npos] = 1
        allPos.append(npos)

    print(allPos)
    print("--- flipped --- ")
    print(flipTile)
    print(len(flipTile))
    print("--- flipped --- ")
    blackTile = [k for k,v in flipTile.items() if (v % 2) == 1]
    print(blackTile)
    print(len(blackTile))
    return blackTile


def dayPass(startingSet):
    blackNeighbours = {}
    resultSet = []
    # mark all cells by the number of blackneighbours
    for pos in startingSet:
        for d in dirs.values():
            npos = (pos[0]+d[0],pos[1]+d[1])
            if npos in blackNeighbours:
                blackNeighbours[npos] += 1
            else:
                blackNeighbours[npos] = 1

    for pos,nbBlackNeighbours in blackNeighbours.items():
        # white ones
        if not pos in startingSet and nbBlackNeighbours == 2:
            resultSet.append(pos)

    for pos in startingSet:
        # existing black ones
        if pos in blackNeighbours and blackNeighbours[pos] <= 2:
            resultSet.append(pos)
    return resultSet


def part2(startingSet):
# Any black tile with zero or more than 2 black tiles immediately adjacent to it is flipped to white.
# Any white tile with exactly 2 black tiles immediately adjacent to it is flipped to black.
    newSet = startingSet
    for day in range(1,101):
        newSet = dayPass(newSet)
        print("day ",day,":",len(newSet))
    return 

print("----- Part1 ----")
startp1 = time.time()
startBlackTiles = part1()
endp1 = time.time()
print("{:.4f}s".format(endp1 - startp1))

print("----- Part2 ----")
startp2 = time.time()
part2(startBlackTiles)
endp2 = time.time()
print("{:.4f}s".format(endp2 - startp2))

