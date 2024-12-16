#Advent of code 2024: Day 12
#https://adventofcode.com/2024/day/12
import re, time, copy , functools, itertools
from collections import defaultdict
import aoc

lines = aoc.ReadPuzzleInput("input_day12.txt")

class Cell:
    def __init__(self, value, pos):
        self.value = value
        self.pos = pos
        self.parsed = False
        self.perimeters = []
        self.neighbours = []
        self.area = None

class Area: 
    def __init__(self):
        self.cells = []
        self.perimeter = 0
        self.area = 0
        self.sides = 0
        self.index = 0
        
    def measure(self):
        self.area = len(self.cells)
        self.perimeter = sum([len(c.perimeters) for c in self.cells])
        return self.area * self.perimeter

    def computeSides(self):
        # find all perimeters 
        perims = [[] for i in range(4)]
        for c in self.cells: 
            for p in c.perimeters: 
                delta = aoc.subPos(c.pos,p.pos)
                perims[aoc.invdirs4[delta]].append(c)
        # all vertical perimeters
        perims[aoc.west].sort(key = lambda cell: cell.pos[0] * grid.height + cell.pos[1] )
        perims[aoc.east].sort(key = lambda cell: cell.pos[0] * grid.height + cell.pos[1] )
        # all horizontal perimeters
        perims[aoc.north].sort(key = lambda cell: cell.pos[1] * grid.width + cell.pos[0])
        perims[aoc.south].sort(key = lambda cell: cell.pos[1] * grid.width + cell.pos[0])
        return nbIntervals(perims[0],1) + nbIntervals(perims[2],1) + nbIntervals(perims[1],0) + nbIntervals(perims[3],0)

    def measure2(self):
        self.area = len(self.cells)
        self.sides = self.computeSides()
        return self.area * self.sides
            
def nbIntervals( listCells, index):
    if len(listCells) ==0 :
        return
    prev = listCells[0]
    otherIndex = 1 if index == 0 else 0
    nbSides = 1
    for c in listCells[1:]:
        if prev.pos[index]+1 != c.pos[index] or prev.pos[otherIndex] != c.pos[otherIndex]:
            nbSides += 1
        prev = c
    return nbSides
        
        
grid = aoc.ToGridPos(lines, lambda v,x,y: Cell(v,(x,y)))
areas = []

display = aoc.Display(True, grid.width, grid.height,    4 , 1)


def exploreAreaFromCell(cell, area = None):
    global areas
    if cell.parsed:
        return
    for d in aoc.dirs4:
        next = grid.ValNext(cell.pos,d)
        if next == None:
            cell.perimeters.append(Cell("",aoc.addPos(cell.pos,d)))
        elif next.value != cell.value:
            cell.perimeters.append(next)
        else:
            cell.neighbours.append(next)
    cell.parsed = True
    if area == None:
        cell.area = Area()
        cell.area.index = len(areas)
        areas.append(cell.area)
    else:
        cell.area = area
    cell.area.cells.append(cell)
    # extend the entire area
    for c in cell.neighbours:
        exploreAreaFromCell(c,cell.area)
    

for row in grid.data:
    for c in row:
        before = len(areas)
        exploreAreaFromCell(c)
        if (len(areas) != before):
            display.drawGrid(grid,lambda c : aoc.colorFromRange(c.area.index,500) if c.area != None else (0,0,0))
            display.update()
        
def part1():
    print(len(areas))
    print(sum([area.measure() for area in areas]))
    return 

def part2():
    result = 0
    for area in areas:
        result = result + area.measure2()
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

display.wait()