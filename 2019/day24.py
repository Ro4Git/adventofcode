import copy 

width = 5
height = 5
grid = [0] * width * height
grids = {0:grid}

def printGrid(grid):
    str = ""
    for i,pix in enumerate(grid):
        if i == 12:
            str += "?"
        else:
            if i % 5 == 0:
                str += chr(10)
            str += "#" if pix else "."
    print(str)

def countBugs(grid):
    val = 0
    for i,pix in enumerate(grid):
        if i != 12:
            val += pix
    return val

#00,01,02,03,04
#05,06,07,08,09
#10,11,12,13,14
#15,16,17,18,19
#20,21,22,23,24
def countInnerBugs(grid):
    return grid[7] + grid[11] + grid[13] + grid[17]

def countOuterBugs(grid):
    val = 0
    for k in range(5):
        val += grid[k]
        val += grid[20+k]
        val += grid[k*width]
        val += grid[4+k*width]
    return val


def getPix(grids, level, i, j):
    if i==2 and j==2:
        print("error",level,i,j)
    if (not level in grids):
            return 0
    return grids[level][j*width +i]

def getNextPix(grids, level, x, y, dx, dy):
    i = x + dx
    j = y + dy
    if i<0:
        return getPix(grids, level-1, 1,2)
    elif i >= width:
        return getPix(grids, level-1, 3,2)
    elif j<0:
        return getPix(grids, level-1, 2,1)
    elif j>=height:
        return getPix(grids, level-1, 2,3)
    else:
        if i == 2 and j == 2:
            val = 0
            # neighbour is center cell
            # one level down
            if dx < 0:
                for k in range(5):
                    val += getPix(grids, level + 1, 4,k)
            elif dx > 0:
                for k in range(5):
                    val += getPix(grids, level + 1, 0,k)
            elif dy > 0:
                for k in range(5):
                    val += getPix(grids, level + 1, k, 0)
            elif dy < 0:
                for k in range(5):
                    val += getPix(grids, level + 1, k, 4)
            return val
        return getPix(grids,level,i,j)

def setPix(grids, layer, i, j, col):
    if not layer in grids:
        grids[layer] = [0] * width * height
    grids[layer][j*width +i] = col

def rating(grid):
    power = 1
    score = 0 
    for i,pix in enumerate(grid):
        score = score + pix * power
        power = power << 1
    return score

def iterateGrid(grids):
    
    # if a layer has bugs on the outer/inner circle 
    # make sure sub layers exist
    toCreate =[]
    for layer,grid in grids.items():
        innerbugs = countInnerBugs(grid)
        outerbugs = countOuterBugs(grid)
        if innerbugs >0:
            #make sure there is another level down
            if not layer+1 in grids:
                toCreate.append(layer+1)
        if outerbugs >0:
            #make sure there is another level down
            if not layer-1 in grids:
                toCreate.append(layer-1)

    for layer in toCreate:
        grids[layer] = [0] * width * height

    nGrids = copy.deepcopy(grids)
    
    for layer,grid in grids.items():
        for j in range(height):
            for i in range(width):
                if not (i==2 and j==2):
                    pix = getPix(grids,layer,i,j)
                    nbNeighbours = (getNextPix(grids, layer, i , j, -1, 0) + 
                                    getNextPix(grids, layer, i , j, +1, 0) + 
                                    getNextPix(grids, layer, i , j, 0, -1) + 
                                    getNextPix(grids, layer, i , j, 0, 1))
                    if pix and nbNeighbours != 1:
                        # bug dies
                        setPix(nGrids,layer,i,j,0)
                    elif not pix and (nbNeighbours == 1 or nbNeighbours == 2):
                        setPix(nGrids,layer,i,j,1)
    return nGrids


f = open("input_day24.txt","r")
lines = f.readlines()

index = 0
for line in lines:
    for c in line: 
        if (c == '.'):
            grid[index] = 0
            index += 1
        elif (c == '#'):
            grid[index] = 1
            index += 1   

printGrid(grids[0])

for i in range(200):
    grids = iterateGrid(grids)

nbBugs = 0
for layer,grid in grids.items():
    print("--------")
    print("Layer ",layer)
    printGrid(grid)    
    nbBugs += countBugs(grid)

print(nbBugs)