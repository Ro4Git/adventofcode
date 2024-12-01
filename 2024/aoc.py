

def ReadPuzzleInput(filename): 
    f = open('./inputs/'+ filename, 'r')
    lines = f.readlines()
    lines = [line.rstrip("\n") for line in lines]
    f.close()
    return lines

def ToGrid(lines, eval = lambda x: x):
    grid = [[eval(c) for c in line] for line in lines]
    width = len(grid[0])
    height = len(grid)
    return grid,width,height

#  0: > , 1: v , 2: < , 3: ^
dirs4 = [(1,0),(0,1),(-1,0),(0,-1)]
dirs8 = [(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1)]

def minPos(pos1,pos2):
    return tuple([min(coord1,coord2) for coord1,coord2 in zip(pos1,pos2)])

def maxPos(pos1,pos2):
    return tuple([max(coord1,coord2) for coord1,coord2 in zip(pos1,pos2)])

def addPos(pos1,pos2):
    return tuple([coord1 + coord2 for coord1,coord2 in zip(pos1,pos2)])

def subPos(pos1,pos2):
    return tuple([coord1 - coord2 for coord1,coord2 in zip(pos1,pos2)])

def mulPos(pos1,pos2):
    return tuple([coord1 * coord2 for coord1,coord2 in zip(pos1,pos2)])

def negPos(pos1):
    return tuple([-coord1 for coord1 in pos1])