#Advent of code 2022: Day 18
#https://adventofcode.com/2022/day/18
import re, time, copy, functools
import astar

f = open('input_day18.txt', 'r')
lines = f.readlines()
lines = [line.rstrip("\n") for line in lines]
f.close()

coords = [[int(c) for c in line.split(",")] for line in lines]


width = 20
height = 20
depth = 20

#5 => outside 
#4 => free air and sure to reach
#3 => free air
#2 => trapped
#1 => cube 

grid = [3]*width*height*depth

def coordToIndex3(x,y,z): 
    return (z)*height*width+(y)*width+(x)

def coordToIndex(pos): 
    return coordToIndex3(pos[0],pos[1],pos[2])

def getPixel(pos):
    if (pos[0]<0 or pos[0]>=width):
        return 5
    if (pos[1]<0 or pos[1]>=height):
        return 5
    if (pos[2]<0 or pos[2]>=depth):
        return 5            
    return grid[coordToIndex(pos)]

def setPixel(pos,val):
    global grid
    grid[coordToIndex(pos)] = val

for coord in coords: 
    setPixel(coord,1)

neigbours = [(1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)]

def addPos(a,b):
    return (a[0]+b[0],a[1]+b[1],a[2]+b[2])

def freeFaces(pos):
    free = 6
    for delta in neigbours:
        test = addPos(pos,delta)
        if getPixel(test) < 3:
            free -= 1
    return free

def nbSurfaces():
    nbSurface = 0
    for coord in coords:
        nbSurface+=freeFaces(coord)
    return nbSurface

def part1():
    print(nbSurfaces())
    return

def neighborsPart2(n):
    for delta in neigbours:
        test = addPos(n,delta)
        if (test[0]<0 or test[0]>=width):
            continue
        if (test[1]<0 or test[1]>=height):
            continue
        if (test[2]<0 or test[2]>=depth):
            continue                
        if getPixel(test) >= 3:
            yield test
    
def distancePart2(n1, n2):
    return 1

def goalFunction(n1, goal):
    if (getPixel(n1)==4) or n1==goal:
        return True
    return False

def cost(n1, n2):
    return abs(n1[0]-n2[0]) + abs(n1[1]-n2[1]) + abs(n1[2]-n2[2])


def initGridFreeAir():
    # check all cube neighbours for access to 0,0,0
    for coord in coords:
        for delta in neigbours:
            pos = addPos(coord,delta)        
            val = getPixel(pos)
            if (val == 3):
                # unprocessed cell, check for a path to 0 
                resAStar = astar.find_path(pos, (0,0,0), neighbors_fnct=neighborsPart2,
                                            heuristic_cost_estimate_fnct=cost, distance_between_fnct=distancePart2, is_goal_reached_fnct=goalFunction)
                if resAStar != None:
                    for path in list(resAStar):
                        setPixel(path,4)
                else:
                    setPixel(pos,2)



def part2():
    initGridFreeAir()
    print(nbSurfaces())
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
