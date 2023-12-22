#Advent of code 2023: Day 21
#https://adventofcode.com/2023/day/21
import re, time, copy, math, numpy
import json

f = open('input_day21.txt', 'r')
lines = f.readlines()
lines = [line.rstrip("\n") for line in lines]
f.close()

def translate(c):
    if (c=="S"):
        return 2
    return int(c=="#")

def findStart():
    for j,row in enumerate(grid):
        for i,val in enumerate(row): 
            if val == 2: 
                return (i,j)
    return None

def addDelta(pos,delta):
    return (pos[0]+delta[0],pos[1]+delta[1])

def getGrid_part1(pos):
    if (pos[0] < 0 or pos[0]>=width):
        return -1
    if (pos[1] < 0 or pos[1]>=height):
        return -1    
    return grid[pos[1]][pos[0]]

def getGrid_part2(pos):
    return grid[(pos[1] + height)%height][(pos[0]+width)%width]

grid = [[translate(c) for c in line] for line in lines]
width = len(grid[0])
height = len(grid)
dirs = [(1,0),(0,1),(-1,0),(0,-1)]

def expandGrid(plots,gridFunc): 
    toExtend = {}
    for pos in plots:
        for dir in dirs:
            nPos = addDelta(pos,dir)
            if gridFunc(nPos) !=1:
                toExtend[nPos] = True
    return toExtend.keys()        

def part1():
    plots = [findStart()]
    for i in range(64):
        plots = expandGrid(plots,getGrid_part1)
    print(len(plots))
    return 

def quad(x, a):
    return (a[2] - 2*a[1] + a[0]) * (x*(x-1)//2)  + (a[1]-a[0]) * x + a[0]

def part2():
# width = height = 131 (prime?)   
# 26501365 % width = 65 (start pos & grid middle)
    sPos = findStart()
    plots = [sPos]
    quadFactors = [0]*4
    for i in range(1,width * 3 + sPos[0]+1):
           plots = expandGrid(plots,getGrid_part2)
           if (i % width == sPos[0]):
               print(i,len(plots))
               quadFactors[i//width] = len(plots)
               if i//width == 3:
                    # sanity check 
                    print("check",quad(i//width,quadFactors))

# 65 3877
# 196 34674
# 327 96159         
# 458 188332         
    result = quad(26501365 // width,quadFactors)
    # 627960837809732 (off by one iteration :-( ))
    # 627960775905777
    print(result)


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