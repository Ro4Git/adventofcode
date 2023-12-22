#Advent of code 2023: Day 22
#https://adventofcode.com/2023/day/22
import re, time, copy, math, numpy
import json
from collections import defaultdict

f = open('input_day22.txt', 'r')
lines = f.readlines()
lines = [line.rstrip("\n") for line in lines]
f.close()

def min3D(pos1,pos2):
    return tuple([min(coord1,coord2) for coord1,coord2 in zip(pos1,pos2)])

def max3D(pos1,pos2):
    return tuple([max(coord1,coord2) for coord1,coord2 in zip(pos1,pos2)])

def add3D(pos1,pos2):
    return tuple([coord1 + coord2 for coord1,coord2 in zip(pos1,pos2)])

def downBrick(brick):
    return ((brick[0][0],brick[0][1],brick[0][2]-1),(brick[1][0],brick[1][1],brick[1][2]-1))


bricks = []
droppedBricks = []
supportedBy = []
criticalBricks = set()
minCoord = (1000,1000,1000)
maxCoord = (0,0,0)

for line in lines:
    a,b = line.split('~')
    brick = (tuple([int(c) for c in a.split(',')]),tuple([int(c) for c in b.split(',')]))
    minCoord = min3D(minCoord,min3D(brick[0],brick[1]))
    maxCoord = max3D(maxCoord,max3D(brick[0],brick[1]))
    bricks.append(brick)

bricks.sort(key=lambda brick: min(brick[0][2],brick[1][2]))
#print(bricks)
print(minCoord)
print(maxCoord)

grid = [[[0 for i in range(10)] for j in range(10)] for k in range(maxCoord[2]+1)]


def brickCollide(brick):
    start = min3D(brick[0],brick[1])
    end = max3D(brick[0],brick[1])
    if start[2] <= 0: 
        return set([-1])
    touched = set()
    for x in range(start[0],end[0]+1):
        for y in range(start[1],end[1]+1):
            for z in range(start[2],end[2]+1):
                touch = grid[z][y][x]
                if touch != 0:
                    touched.add(touch-1)
    return touched

def brickPrint(brick,index):
    start = min3D(brick[0],brick[1])
    end = max3D(brick[0],brick[1])
    for x in range(start[0],end[0]+1):
        for y in range(start[1],end[1]+1):
            for z in range(start[2],end[2]+1):
                grid[z][y][x] = index

def dropBrick(brick):
    curBrick = brick
    nBrick = brick
    indexResting = []
    while len(indexResting) == 0:
        curBrick = nBrick
        nBrick = downBrick(curBrick)
        indexResting = brickCollide(nBrick)
    return curBrick,indexResting

def part1():
    global droppedBricks,criticalBricks

    for i,brick in enumerate(bricks):
        dropped,restingOn = dropBrick(brick)
        brickPrint(dropped,i+1)
        droppedBricks.append(dropped)
        supportedBy.append(restingOn)
        if len(restingOn) == 1 and list(restingOn)[0]!=-1:
            criticalBricks.update(restingOn)
    print(len(bricks) - len(criticalBricks))
    return 


def part2():
    movedBricks = []
    for brick in criticalBricks:
        moved = set()
        moved.add(brick)
        # parse all bricks from the bottom up 
        # if all supports of a brick are being moved, this brick will move too and is added to the "moved" set
        for indexBrick, supports in enumerate(supportedBy):
            if supports.issubset(moved):
                moved.add(indexBrick)
        movedBricks.append(len(moved)-1)
    print(sum(movedBricks))
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