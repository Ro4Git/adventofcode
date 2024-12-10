#Advent of code 2024: Day 8
#https://adventofcode.com/2024/day/8
import re, time, copy , functools, itertools
from collections import defaultdict
import aoc

lines = aoc.ReadPuzzleInput("input_day8.txt")
grid = aoc.ToGrid(lines)

antennas = defaultdict(list)
for y,row in enumerate(grid.data):
    for x,c in enumerate(row):
        if c != '.':
            antennas[c].append((x,y))

print(antennas)

antinodes = defaultdict(int)

def addNode(pos): 
    global antinodes
    if not grid.IsOut(pos):
        antinodes[pos] += 1
 

def findAntinodes(positions):
    couples = list(itertools.combinations(positions, 2))
    for couple in couples: 
        delta = aoc.subPos(couple[1],couple[0])
        antinode1 = aoc.subPos(couple[0],delta)
        antinode2 = aoc.addPos(couple[1],delta)
        addNode(antinode1)
        addNode(antinode2)
    
def findAntinodes2(positions):
    couples = list(itertools.combinations(positions, 2))
    for couple in couples: 
        delta = aoc.subPos(couple[1],couple[0])
        
        antinode1 = couple[0]
        while not grid.IsOut(antinode1):
            addNode(antinode1)    
            antinode1 = aoc.subPos(antinode1,delta)
            
        antinode2 = couple[1]
        while not grid.IsOut(antinode2):
            addNode(antinode2)    
            antinode2 = aoc.addPos(antinode2,delta)        
        
    



def part1():
    for antenna,positions in antennas.items():
        findAntinodes(positions)
    print(len(antinodes.keys()))
    return 

def part2():
    for antenna,positions in antennas.items():
        findAntinodes2(positions)
    print(len(antinodes.keys()))    
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

