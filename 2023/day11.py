#Advent of code 2023: Day 11
#https://adventofcode.com/2023/day/11
import re, time, copy, math

f = open('input_day11.txt', 'r')
lines = f.readlines()
lines = [line.rstrip("\n") for line in lines]
f.close()

startGrid = [[int(c=='#') for c in line] for line in lines]
width = len(startGrid[0])
height = len(startGrid)
print(startGrid)

def findExpandSpot(grid):
    toExpandY = []
    for i,line in enumerate(grid):
        if not 1 in line:
            toExpandY.append(i)
    #expand horizontally
    toExpandX = []
    for i in range(len(grid[0])):
        row = [line[i] for line in grid]
        if not 1 in row:
            toExpandX.append(i)
    return (toExpandX,toExpandY)

def findGalaxies(grid):
    galaxies = []
    for y,line in enumerate(grid):
        for x,c in enumerate(line):
            if c==1:
                galaxies.append([x,y])
    return galaxies

def expandGalaxies(galaxies,expandSpots,expansion):
    for g in galaxies:
        gInit = g.copy()
        for i in range(2):
            for ex in expandSpots[i]: 
                if ex<gInit[i]:
                    g[i] = g[i] + expansion
                else: 
                    break


def dist(g1,g2):
    return abs(g2[0]-g1[0]) + abs(g2[1]-g1[1])


def part1():
    expandSpots = findExpandSpot(startGrid)
    print(expandSpots)
    galaxies = findGalaxies(startGrid)
    expandGalaxies(galaxies,expandSpots,1)
    pairs =[(a, b) for i,a in enumerate(galaxies) for b in galaxies[i + 1:]]
    dists = [dist(pair[0],pair[1]) for pair in pairs]
    print(sum(dists))
    return 

def part2():
    expandSpots = findExpandSpot(startGrid)
    print(expandSpots)
    galaxies = findGalaxies(startGrid)
    expandGalaxies(galaxies,expandSpots,999999)
    pairs =[(a, b) for i,a in enumerate(galaxies) for b in galaxies[i + 1:]]
    dists = [dist(pair[0],pair[1]) for pair in pairs]
    print(sum(dists))
    
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