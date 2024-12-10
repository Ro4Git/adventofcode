

def ReadPuzzleInput(filename): 
    f = open('./inputs/'+ filename, 'r')
    lines = f.readlines()
    lines = [line.rstrip("\n") for line in lines]
    f.close()
    return lines

def ToSections(lines): 
    sections = []
    section = []
    for line in lines:
        if len(line)>0:
            section.append(line)
        else:
            sections.append(section.copy())
            section.clear()
    sections.append(section)
    return sections

def ToList(lines, sep, eval = lambda x: x):
    return  [[eval(c) for c in line.split(sep)] for line in lines]


class Grid:
    def __init__(self, data, width, height):
        self.data = data
        self.width = width
        self.height = height 
    
    def Find(self, value):
        for y,row in enumerate(self.data):
            for x,c in enumerate(row):
                if (c == value):
                    return (x,y)
        return None

    def FindAll(self, value):
        result = []
        for y,row in enumerate(self.data):
            for x,c in enumerate(row):
                if (c == value):
                    result.append((x,y))
        return result

    def FindNeighbours(self, pos, eval):
        result = []
        for dirs in dirs4:
            newPos = addPos(pos,dirs)
            if not self.IsOut(newPos) and eval(self.data[newPos[1]][newPos[0]]):
                result.append(newPos)
        return result

    def IsOut(self, pos):
        return (pos[0] < 0 or pos[0]>=self.width or pos[1] < 0 or pos[1]>=self.height)

    def Val(self, pos):
        return self.data[pos[1]][pos[0]]

    def Set(self, pos, value):
        self.data[pos[1]][pos[0]] =  value

    def ValNext(self, pos , delta):
        nPos = addPos(pos,delta)
        if self.IsOut(pos):
            return None
        return self.Val(nPos)

def ToGrid(lines, eval = lambda x: x):
    grid = [[eval(c) for c in line] for line in lines]
    width = len(grid[0])
    height = len(grid)
    return Grid(grid,width,height)



# directions in grid
north = 3
west = 0
south = 1
east = 2
#  0: > , 1: v , 2: < , 3: ^
dirs4 = [(1,0),(0,1),(-1,0),(0,-1)]
dirs8 = [(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1)]
turn90right = [1,2,3,0]
turn90left = [3,0,1,2]

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