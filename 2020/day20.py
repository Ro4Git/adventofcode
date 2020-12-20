#Advent of code 2020: Day 20    
#https://adventofcode.com/2020/day/20
import re,sys
import math,time,itertools
from functools import reduce

f = open('input_day20.txt', 'r')
lines = f.readlines()
f.close()

tiles = {}

#####   
# 0 #
#3 1#
# 2 #
#####   
flippedH = [0,3,2,1]
flippedV = [2,1,0,3]
rotateCW = [3,0,1,2]

class Tile:
    def __init__(self):
        self.id = 0
        self.tileData = []
        self.borderCodes = [0]*4        # int code of each border bits
        self.fborderCodes = [0]*4       # int code of each border bits (flipped)
        self.potentialNeighbours = 0    # number of tiles around
        self.borderNeighbours = [0]*4   # who is around in that direction
        self.flipV = False
        self.flipH = False
        self.rotated90CW = False

    def getPixel(self,x,y):
        if self.flipV:
            x,y = (x,9-y)
        if self.flipH:
            x,y = (9-x,y)
        if self.rotated90CW:
            x,y = (y,9-x)
        return self.tileData[y][x]

    #rotate,  flip tile until it fits the surrounding constrain
    # update the border codes once done
    def matchConstrain(self,left,top):
        if self.borderNeighbours[3] != left and self.borderNeighbours[1] != left: 
            #rotation required
            self.rotated90CW = True
            self.borderNeighbours = [self.borderNeighbours[i] for i in rotateCW]
        if self.borderNeighbours[3] != left: 
            #fliph required
            self.flipH = True
            self.borderNeighbours = [self.borderNeighbours[i] for i in flippedH]
        if self.borderNeighbours[0] != top: 
            #flipv required
            self.flipV = True
            self.borderNeighbours = [self.borderNeighbours[i] for i in flippedV]
        #orientation done
        backup = self.borderNeighbours
        if (self.borderNeighbours[3] != left and self.borderNeighbours[0]!= top):
            print("error matching constrain")
        self.resetOrientation()
        if (backup != self.borderNeighbours):
            print("error matching constrain")

    def updatePotentialNeighbours(self):
        self.potentialNeighbours = 0
        self.borderNeighbours = [0]*4
        for i in range(4):
            for c in codeToTiles[self.borderCodes[i]]:
                if c != self.id: 
                    self.potentialNeighbours += 1
                    if (self.borderNeighbours[i] != 0): 
                        print("problem") 
                    else:
                        self.borderNeighbours[i] = c
        return

    # reset the pixel data to match flip/rotations
    def resetOrientation(self):
        newTileData = [[]]*10
        for y in range(10):
            newTileData[y] = [0]*10
            for x in range(10):
                newTileData[y][x] = self.getPixel(x,y)
        self.tileData = newTileData
        self.flipH = False
        self.flipV = False
        self.rotated90CW = False
        self.borderCodes = [0]*4
        self.fborderCodes = [0]*4        
        for i in range(10):
            self.borderCodes[0] += (1<<i) * self.tileData[0][i]    
            self.borderCodes[1] += (1<<i) * self.tileData[i][9]     
            self.borderCodes[2] += (1<<i) * self.tileData[9][i]     
            self.borderCodes[3] += (1<<i) * self.tileData[i][0]          
        self.updatePotentialNeighbours()
        return 

    def readTile(self, index):
        m = re.match("Tile (\d+)\:",lines[index])
        self.id = int(m.groups()[0])
        self.tileData = [[]]*10
        for i in range(10):
            self.tileData[i] = [1 if c =="#" else 0 for c in lines[index+i+1].rstrip() ]
        self.borderCodes = [0]*4
        self.fborderCodes = [0]*4
        for i in range(10):
            self.borderCodes[0] += (1<<i) * self.tileData[0][i]    
            self.borderCodes[1] += (1<<i) * self.tileData[i][9]     
            self.borderCodes[2] += (1<<i) * self.tileData[9][i]     
            self.borderCodes[3] += (1<<i) * self.tileData[i][0]     
            self.fborderCodes[0] += (1<<(9-i)) * self.tileData[0][i]    
            self.fborderCodes[1] += (1<<(9-i)) * self.tileData[i][9]     
            self.fborderCodes[2] += (1<<(9-i)) * self.tileData[9][i]     
            self.fborderCodes[3] += (1<<(9-i)) * self.tileData[i][0]     
        return index + 12

codeToTiles = [[]]*1024
for i in range(1024):
    codeToTiles[i] = []

# read from file
index = 0 
while index < len(lines):
    tile = Tile()
    tile.readTile(index)
    index += 12
    tiles[tile.id] = tile

# mark all tiles with common "border codes" (flipped or not )
nbSideTiles = int(math.sqrt(len(tiles.values())))
nbSidePixels = nbSideTiles*8
for t in tiles.values():
    for i in range(4):
        codeToTiles[t.borderCodes[i]].append(t.id)
        codeToTiles[t.fborderCodes[i]].append(t.id)

# and find out who is next to who
for t in tiles.values():
    t.updatePotentialNeighbours()
                
#part 1 is just about finding tiles which only have 2 neighbours
potentialCorners = [t.id for t in tiles.values() if t.potentialNeighbours == 2]
potentialBorders = [t.id for t in tiles.values() if t.potentialNeighbours == 3]
potentialInside = [t.id for t in tiles.values() if t.potentialNeighbours == 4]
print(len(tiles))
print(len(potentialCorners))
print(len(potentialBorders))
print(len(potentialInside))

#rebuild the image
image = [[]] * nbSideTiles
for i in range(nbSideTiles): 
    image[i] = [0] *nbSideTiles

#find a valid top left corner
startingCorner = 0
for c in potentialCorners:
    if tiles[c].borderNeighbours[0] == 0 and tiles[c].borderNeighbours[3] == 0:
        startingCorner = c
        break
image[0][0] = startingCorner

# expand first row and column
for i in range(1,nbSideTiles):
    leftTileIndex = image[0][i-1]
    nextTileIndex = tiles[leftTileIndex].borderNeighbours[1]
    nextTile = tiles[nextTileIndex]
    nextTile.matchConstrain(leftTileIndex,0)
    image[0][i] = nextTileIndex
    #expand first column
    topTileIndex = image[i-1][0]
    nextTileIndex = tiles[topTileIndex].borderNeighbours[2]
    nextTile = tiles[nextTileIndex]
    nextTile.matchConstrain(0,topTileIndex)
    image[i][0] = nextTileIndex

# expand the rest of the image
for i in range(1,nbSideTiles):
    for j in range(1,nbSideTiles):
        leftTileIndex = image[i][j-1]
        topTileIndex  = image[i-1][j]
        nextTileIndex = tiles[leftTileIndex].borderNeighbours[1]
        if (nextTileIndex != tiles[topTileIndex].borderNeighbours[2]):
            nextTileIndex = tiles[topTileIndex].borderNeighbours[2]
            print("problem")

        nextTile = tiles[nextTileIndex]
        nextTile.matchConstrain(leftTileIndex,topTileIndex)
        image[i][j] = nextTileIndex


def part1():
    mul = 1
    for c in potentialCorners:
        mul = mul * c
    print(mul)    

def passThrough(pos):
    return pos

def flipV(pos):
    return (pos[0],-pos[1])

def flipH(pos):
    return (-pos[0],pos[1])

def flipVH(pos):
    return (-pos[0],-pos[1])

def rotateCW(pos):
    return (pos[1],-pos[0])

def rotateCWFlipV(pos):
    return rotateCW(flipV(pos))

def rotateCWFlipH(pos):
    return rotateCW(flipH(pos))

def rotateCWFlipVFlipH(pos):
    return rotateCW(flipH(flipV(pos)))

combinations =  [passThrough,flipV,flipH,flipVH,rotateCW,rotateCWFlipV,rotateCWFlipVFlipH,rotateCWFlipH]    

def patternMatch(picture,patternSpots,x,y,func):
    for xd,yd in [func(pos) for pos in patternSpots]: 
        if (y+yd < 0 or y+yd>=nbSidePixels or x+xd <0 or x+xd >= nbSidePixels):
            return False
        if picture[y+yd][x+xd] != '#' and picture[y+yd][x+xd] != '■':
            return False    
    return True

def seaMonsterPrint(picture,patternSpots,x,y,func):
    for xd,yd in [func(pos) for pos in patternSpots]: 
       s = list(picture[y+yd])
       s[x+xd] = '■'
       picture[y+yd] = "".join(s)

def part2():
    #copy everything back into a single picture 
    picture = []
    for i in range(nbSideTiles):
        for y in range(8):
            str = ""
            for j in range(0,nbSideTiles):
                t = tiles[image[i][j]]
                for x in range(8):
                    str += "#" if t.getPixel(x+1,y+1) else "."
            picture.append(str)

    #compute location of # in seaMonster
    seaMonster = ["                  # "
                 ,"#    ##    ##    ###",
                  " #  #  #  #  #  #   "]
    patternSpots = []
    for i,line in enumerate(seaMonster): 
        for j,c in enumerate(line): 
            if c == "#": 
                patternSpots.append((j,i))
    
    # test all pixels for pattern applying the given transform func 
    def testPicture(func):
        nbFound = 0
        for y in range(nbSidePixels):
            for x in range(nbSidePixels):
                if patternMatch(picture,patternSpots,x,y,func):
                    nbFound += 1
                    seaMonsterPrint(picture,patternSpots,x,y,func)
        print(nbFound)
        return nbFound
    
    #try all potential flip/rotate
    for func in combinations:
        nbFound = testPicture(func)
        if nbFound > 0:
            for l in picture:
                print(l)
            sum = 0 
            for l in picture:
                for c in l:
                    if c == "#":
                        sum += 1
            print(nbFound, sum)                
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

