#Advent of code 2023: Day 23
#https://adventofcode.com/2023/day/23
import re, time, copy, math
from collections import defaultdict


f = open('input_day23.txt', 'r')
lines = f.readlines()
lines = [line.rstrip("\n") for line in lines]
f.close()

grid = [[c for c in line] for line in lines]
width = len(grid[0])
height = len(grid)
dirs = [(1,0),(0,1),(-1,0),(0,-1)]
validSlopes = ['>','v','<','^']

def addDelta(pos,delta):
    return (pos[0]+delta[0],pos[1]+delta[1])

def getGrid(node):
    if node[1] <0 or node[1]>=width:
         return '#'
    return grid[node[1]][node[0]]

def neighborsPart1(n):
    pos = n[-1]
    value = getGrid(pos)
    nexts = []
    for dirDelta,validSlope in zip(dirs,validSlopes):
        if value == '.' or validSlope == value:
            newPos = addDelta(pos,dirDelta)
            newValue = getGrid(newPos)
            if newValue != '#' and not newPos in n:
                nexts.append(newPos)
    return nexts


def part(exploreFct):
    startPos = (1,0)
    endPos = (width-2,height-1)
    openPaths = [[startPos]]
    resultPaths = []
    highestSoFar = defaultdict(int)
    while len(openPaths):
        path = openPaths.pop(-1)
        nexts = exploreFct(path)
        for n in nexts:
                highestSoFar[n] = len(path)+1
                if n == endPos:
                    if len(path) > len(resultPaths):
                        path.append(endPos)
                        resultPaths = path
                        print(len(resultPaths))
                else:
                    nPath = path
                    if len(nexts)>1:
                        nPath = path.copy()
                    nPath.append(n)
                    openPaths.append(nPath)
                    openPaths.sort(key = lambda x : len(x))
    print(highestSoFar[endPos])
    print(len(resultPaths)-1)
    return 


def neighborsPart2(n,visited):
    pos = n[-1]
    value = getGrid(pos)
    nexts = []
    for dirDelta in dirs:
        newPos = addDelta(pos,dirDelta)
        newValue = getGrid(newPos)
        if newValue != '#' and not newPos in n:
            nexts.append(newPos)
    return nexts


def part2():
    startPos = (1,0)
    endPos = (width-2,height-1)
    openPaths = [[startPos]]
    visited = set()
    visited.add(startPos)
    resultPaths = []

    while len(openPaths):
        path = openPaths.pop(-1)
        nexts = neighborsPart2(path,visited)
        while len(nexts) == 1:
            path.append(nexts[0])
            visited.add(nexts[0])
            nexts = neighborsPart2(path,visited)
        else:
            resultPaths.append(path)
            for newP in nexts:
                if not newP in visited:
                    visited.add(newP)
                    openPaths.append([path[-1],newP])
    
    graph = {}
    for path in resultPaths:
        if not path[0] in graph: 
            graph[path[0]] = {}
        if not path[-1] in graph: 
            graph[path[-1]] = {}            
        graph[path[0]][path[-1]] = len(path)-1
        graph[path[-1]][path[0]] = len(path)-1

    def neighborsPart3(n):
        pos = n[-1]
        return [k for k in graph[pos].keys() if not k in n]

    openPaths = [([startPos],0)]
    resultPaths = []
    maxLength = 0
    while len(openPaths):
        path,length = openPaths.pop(-1)
        nexts = neighborsPart3(path)
        for n in nexts:
                newLength = length + graph[path[-1]][n]
                if n == endPos:
                    if newLength > maxLength:
                        path.append(endPos)
                        resultPaths = path
                        maxLength = newLength
                        print(maxLength)
                else:
                    nPath = path
                    if len(nexts)>1:
                        nPath = path.copy()
                    nPath.append(n)
                    openPaths.append((nPath,newLength))
                    openPaths.sort(key = lambda x : x[1])
  
    print(maxLength)

    return 


def part1():
    part(neighborsPart1)
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