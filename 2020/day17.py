#Advent of code 2020: Day 17
#https://adventofcode.com/2020/day/17
import re,sys
import time,itertools
from functools import reduce



f = open('input_day17.txt', 'r')
lines = f.readlines()
f.close()

activeList = {}
def initList():
    global activeList   
    activeList = {} 
    for coordy,line in enumerate(lines):
        for coordx,c in enumerate(line):
            if (c =='#'):
                activeList[(coordx,coordy,0,0)] = 1

def vec3Add(a,b):
    return (a[0]+b[0],a[1]+b[1],a[2]+b[2],0)

def vec4Add(a,b):
    return (a[0]+b[0],a[1]+b[1],a[2]+b[2],a[3]+b[3])

def markCell(list,pos):
    if not pos in list:
        list[pos] = 1
    else:
        list[pos] += 1

def cycle(deltas,addFunc):
    #parse all active cells and add them to their neighbours 
    global activeList
    newActiveList = {}
    neightbourCount = {}
    for k,v in activeList.items():
        for delta in deltas:
            npos = addFunc(k,delta)
            markCell(neightbourCount,npos)
    for k,v in neightbourCount.items():
        if k in activeList:
            if v == 2 or v == 3:
                newActiveList[k] = 1
        else:
            if v == 3:
                newActiveList[k] = 1
    return newActiveList                
        

def part1():
    global activeList
    initList()
    deltas = [c for c in itertools.product((0, 1, -1), repeat=3) if c != (0, 0, 0)]
    print(len(activeList))
    for i in range(6):
        activeList = cycle(deltas,vec3Add)
        print(len(activeList))
    return len(activeList)

def part2():
    global activeList
    initList()
    deltas = [c for c in itertools.product((0, 1, -1), repeat=4) if c != (0, 0, 0, 0)]
    print(len(activeList))
    for i in range(6):
        activeList = cycle(deltas,vec4Add)
        print(len(activeList))
           
    return len(activeList)

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

