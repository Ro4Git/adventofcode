#Advent of code 2020: Day 11
#https://adventofcode.com/2020/day/11
import copy,time

f = open('input_day11.txt', 'r')
lines = f.readlines()
f.close()

grid = []

def initGrid():
    global grid
    grid = []
    for line in lines:
        grid.append(list(line))


initGrid()
width = len(grid[0])
height = len(grid)
gridnextgen = []
dirs = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]

def gridPixel(pos):
    return grid[pos[1]][pos[0]]

def nbOccupiedNeighbours(pos):
    nbOccupied = 0
    for y in range(max(0,pos[1]-1),min(height,pos[1]+2)):
        for x in range(max(0,pos[0]-1),min(width,pos[0]+2)):
            if ((x,y) != pos) and (grid[y][x] == '#'):
                nbOccupied += 1
    return nbOccupied

def nbOccupiedNeighbours2(pos):
    nbOccupied = 0
    for d in dirs: 
        npos = pos
        while True:        
            npos = (npos[0]+d[0],npos[1]+d[1]) 
            if (npos[0] < 0 or npos[0] >= width or npos[1] < 0 or npos[1] >= height):
                break
            if grid[npos[1]][npos[0]] == "L":
                break
            if grid[npos[1]][npos[0]] == "#":
                nbOccupied += 1
                break        
    return nbOccupied


def evolveGrid(func,limit):
    global grid
    global gridnextgen
    gridnextgen = copy.deepcopy(grid)
    nbChanges = 0
    for y in range(0,height):
        for x in range(0,width):
            nbOccupied = func((x,y))
            cell = gridPixel((x,y))
            if (cell == "L") and nbOccupied == 0:
                nbChanges += 1
                gridnextgen[y][x] = "#"
            if (cell == "#") and nbOccupied >= limit: 
                nbChanges += 1
                gridnextgen[y][x] = "L"
    grid = gridnextgen
    return nbChanges


def part(n,func, limit):
    nbChanges = 1
    nbIteration = 0
    nbOccupied = 0

    while nbChanges != 0:
        nbChanges = evolveGrid(func,limit)
        nbIteration += 1
        nbOccupied = 0
        for l in grid:
            for c in l: 
                if (c == '#'):
                    nbOccupied += 1

    print("part: ",n, nbIteration,nbOccupied)


print("----- Part1 ----")
initGrid()
startp1 = time.time()
part(1,nbOccupiedNeighbours,4)
endp1 = time.time()
print("{:.4f}s".format(endp1 - startp1))

print("----- Part2 ----")
initGrid()
startp2 = time.time()
part(2,nbOccupiedNeighbours2,5)
endp2 = time.time()
print("{:.4f}s".format(endp2 - startp2))