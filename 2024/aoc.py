import pygame
import colorsys
import sys
from PIL import Image
import numpy as np

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

    def ValWrap(self, pos):
        return self.data[pos[1]%self.height][pos[0]%self.width]

    def Set(self, pos, value):
        self.data[pos[1]][pos[0]] =  value

    def Fill(self, pos1, pos2, value):
        minx = min(pos1[0],pos2[0])
        maxx = max(pos1[0],pos2[0])
        miny = min(pos1[1],pos2[1])
        maxy = max(pos1[1],pos2[1])
        for i in range(minx,maxx+1):
            for j in range(miny,maxy+1):
                self.data[j][i] =  value

    def ValNext(self, pos , delta):
        nPos = addPos(pos,delta)
        if self.IsOut(nPos):
            return None
        return self.Val(nPos)


def ToGrid(lines, eval = lambda x: x):
    grid = [[eval(c) for c in line] for line in lines]
    width = len(grid[0])
    height = len(grid)
    return Grid(grid,width,height)

def ToGridPos(lines, eval = lambda v,x,y: v):
    grid = [[eval(c,x,y) for x,c in enumerate(line)] for y,line in enumerate(lines)]
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
invdirs4 = {(1,0):0,(0,1):1,(-1,0):2,(0,-1):3}

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

def sclPos(scl,pos2):
    return tuple([scl * coord2 for coord2 in pos2])

def dotPos(pos1,pos2):
    return tuple(sum([coord1 * coord2 for coord1,coord2 in zip(pos1,pos2)]))

def negPos(pos1):
    return tuple([-coord1 for coord1 in pos1])

def crossPos2(pos1,pos2):
    return pos1[0] * pos2[1] - pos1[1] * pos2[0]

def colorFromRange(val, maxVal):
    c = pygame.Color(0,0,0)
    c.hsva = ((val * 360 / maxVal)%360 , 100,100,100)
    return c

class Display:
    def __init__(self , enabled , width, height , cellSize, border , isoTile = 0 ):
        self.enabled = enabled
        self.width = width
        self.height = height
        self.cellSize = cellSize
        self.border = border
        self.frames = []
        self.isoTileSize = isoTile
         
        if enabled:
            pygame.init()
            elemSize = cellSize + border 
            screenSize = ((width+1)*elemSize,(height+1)*elemSize)
            if isoTile != 0:
                screenSize = ((width+height+1)*isoTile//2,(width+height+1)*isoTile//4)
            self.surface = pygame.display.set_mode(screenSize)              
            self.imgbox = pygame.image.load("tile32_box2.png").convert_alpha()
            self.imgwall = pygame.image.load("tile32_wall.png").convert_alpha()
            self.imgfloor = pygame.image.load("tile32_floor.png").convert_alpha()
            self.imgleft = pygame.image.load("tile32_west.png").convert_alpha()
            self.imgright = pygame.image.load("tile32_east.png").convert_alpha()
            self.imgup = pygame.image.load("tile32_south.png").convert_alpha()
            self.imgdown = pygame.image.load("tile32_north.png").convert_alpha()
            self.imgs = {'#':self.imgwall,
                         ".":self.imgfloor,
                         'O':self.imgbox,
                         '[':self.imgbox,
                         ']':self.imgbox,
                         "<":self.imgright,
                         '>':self.imgleft,
                         '^':self.imgup,
                         'v':self.imgdown
                         }

        else:
            self.surface = None
            
    def clear(self, color = (120,120,120)):
        if self.enabled:
            self.surface.fill(color)

    def drawGrid(self, grid , eval):
        if self.enabled and self.surface != None:
            elemSize = self.cellSize + self.border
            for y,row in enumerate(grid.data):
                for x,val in enumerate(row):
                    rect = (self.border + x*elemSize , self.border + y * elemSize,self.cellSize,self.cellSize)
                    self.surface.fill(eval(val),rect)  
                    
    def drawGridTiles(self, grid , eval = lambda x : x):
        if self.enabled and self.surface != None:
            halfTile = self.isoTileSize // 2
            quarterTile = self.isoTileSize // 4
            mid = (self.width+self.height+1) * quarterTile // 2
            for y,row in enumerate(grid.data):
                for x,val in reversed(list(enumerate(row))):
                    pos = (x * halfTile + y * halfTile , -x * quarterTile + y * quarterTile + mid)
                    self.surface.blit(self.imgs[eval(val)],pos)  
                    
    def drawListPosTiles(self, listPos , key , eval = None):
        if self.enabled and self.surface != None:
            halfTile = self.isoTileSize // 2
            quarterTile = self.isoTileSize // 4
            mid = (self.width+self.height+1) * quarterTile // 2
            for posg in listPos:
                pos = (posg[0] * halfTile + posg[1] * halfTile , -posg[0] * quarterTile + posg[1] * quarterTile + mid)
                lkey = key
                if eval != None:
                    lkey = eval(pos)
                self.surface.blit(self.imgs[key],pos)        
       
    def drawListPos(self, listPos , col , eval = None):
        if self.enabled and self.surface != None:
            elemSize = self.cellSize + self.border
            for pos in listPos:
                rect = (self.border + pos[0] * elemSize , self.border + pos[1] * elemSize,self.cellSize,self.cellSize)
                lcol = col
                if eval != None:
                    lcol = eval(pos)
                self.surface.fill(lcol,rect)                      
                    
    def update(self):     
        if self.enabled:   
            pygame.display.update()     
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()     

    def wait(self):
        if (self.enabled):
            while True:
                pygame.display.update()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        return
                    
    def waitKey(self):
        if (self.enabled):
            while True:
                pygame.display.update()
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        return

    def capture(self):
        rgb = pygame.surfarray.array3d(self.surface)
        rgb = np.moveaxis(rgb, 0, 1)
        frameImage = Image.fromarray(np.uint8(rgb))
        self.frames.append(frameImage)                    
                        
    def saveGif(self , filename):
        self.frames[0].save(
            filename, save_all=True, optimize=False,
            append_images=self.frames[1:],
            loop=0, duration=int(1000 / 60))                    