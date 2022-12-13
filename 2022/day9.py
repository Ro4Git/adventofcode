#Advent of code 2022: Day 9
#https://adventofcode.com/2022/day/9
import re, time, copy
from collections import defaultdict

f = open('input_day9.txt', 'r')
lines = f.readlines()
lines = [line.rstrip("\n") for line in lines]
f.close()

moves = [line.split(" ") for line in lines]
dirs = {}
dirs["R"] = (1,0)
dirs["L"] = (-1,0)
dirs["U"] = (0,-1)
dirs["D"] = (0,1)

visited = defaultdict(int)

def addDir(pos, dir):
    return (pos[0]+dir[0],pos[1]+dir[1])

def addVisited(pos):
    global visited
    visited[pos] += 1

def keepUp(knotPosH,knotPosT):
    newPosX = knotPosT[0]
    newPosY = knotPosT[1]
    testY = int(abs(knotPosT[0] - knotPosH[0]) <= 1)
    testX = int(abs(knotPosT[1] - knotPosH[1]) <= 1)

    if knotPosT[0] < knotPosH[0]-testX:
        newPosX += 1
    elif knotPosT[0] > knotPosH[0]+testX:
         newPosX -= 1
    if knotPosT[1] < knotPosH[1]-testY:
        newPosY += 1
    elif knotPosT[1] > knotPosH[1]+testY:
         newPosY -= 1   
    return (newPosX,newPosY)

def doMove1(move): 
    global posH,posT
    delta = dirs[move[0]]
    steps = int(move[1])
    for i in range(steps):
        posH = addDir(posH,delta)
        posT = keepUp(posH,posT)
        addVisited(posT)


def part1():
    global visited
    visited = defaultdict(int)
    posH = posT = (0,0)
    addVisited(posT)
    for move in moves:
        delta = dirs[move[0]]
        steps = int(move[1])
        for i in range(steps):
            posH = addDir(posH,delta)
            posT = keepUp(posH,posT)
            addVisited(posT)
    print(len(visited))

    return 

def part2():
    global visited
    visited = defaultdict(int)
    kPos = [(0,0)]*10
  
    addVisited(kPos[9])

    for move in moves:
        delta = dirs[move[0]]
        steps = int(move[1])
        for i in range(steps):
            kPos[0] = addDir(kPos[0],delta)
            for k in range(9):
                kPos[k+1] = keepUp(kPos[k],kPos[k+1])
            addVisited(kPos[9])

    print(len(visited))
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