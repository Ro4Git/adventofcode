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
        if data != None:
            self.data = data
        else:
            self.data = [[ "." for i in range(width)] for j in range(height)]
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
west = 2
south = 1
east = 0
dirsArrow = {'>':0,'v':1,'<':2,'^':3}
dirsCard = {'E':0,'S':1,'W':2,'N':3}

#  0: > , 1: v , 2: < , 3: ^
dirs4 = [(1,0),(0,1),(-1,0),(0,-1)]
invdirs4 = {(1,0):0,(0,1):1,(-1,0):2,(0,-1):3}

dirs8 = [(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1)]
turn90right = [1,2,3,0]
turn90left = [3,0,1,2]

def manDist(pos1,pos2):
    return sum([abs(coord1-coord2) for coord1,coord2 in zip(pos1,pos2)])

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

class OrientedSprite:
    def __init__(self,basefilename, nbFrames = 1, offset = 0):
        self.imgs = {}
        for letterDir, dir in dirsCard.items():
            image = pygame.image.load("images/" + basefilename + letterDir + ".png").convert_alpha()
            self.imgs[dir] = image
            self.sizeX = image.get_width() // nbFrames
            self.sizeY = image.get_height()
        self.offset = offset
        self.pos = (0,0)
        self.dir = 0
        self.currentFrame = 0
        self.nbFrames = nbFrames
    def setDir(self, dir):
        self.dir = dir  
    def step(self):
        self.currentFrame += 1
        self.currentFrame = self.currentFrame % self.nbFrames
    def imageRect(self):
        return self.imgs[self.dir] , (self.currentFrame * self.sizeX,0,self.sizeX,self.sizeY)
            

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
            self.screenSize = ((width+1)*elemSize,(height+1)*elemSize)
            if isoTile != 0:
                self.screenSize = ((width+height+1)*isoTile//2,(width+height+1)*isoTile//4+30)
            self.surface = pygame.display.set_mode(self.screenSize)              
            self.imgbox = pygame.image.load("images/tile32_box1.png").convert_alpha()
            self.imgwall = pygame.image.load("images/tile32_halfwall.png").convert_alpha()
            self.imgfloor = pygame.image.load("images/tile32_floor.png").convert_alpha()
            self.imgstart = pygame.image.load("images/tile32_start.png").convert_alpha()
            self.imgend = pygame.image.load("images/tile32_end.png").convert_alpha()
            self.imgs = {'#':self.imgwall,
                         ".":self.imgfloor,
                         'O':self.imgbox,
                         '[':self.imgbox,
                         ']':self.imgbox,
                         'S':self.imgstart,
                         'E':self.imgend,
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
                    
    def drawGridTiles(self, grid , eval = lambda x : x , sprites = None):
        if self.enabled and self.surface != None:
            halfTile = self.isoTileSize // 2
            quarterTile = self.isoTileSize // 4
            mid = (self.width+self.height+1) * quarterTile // 2
            for y,row in enumerate(grid.data):
                for x,val in enumerate(row):
                    if val == '.':
                        pos = (x * halfTile + y * halfTile , -x * quarterTile + y * quarterTile + mid)
                        self.surface.blit(self.imgs[eval(val)],pos)  
            
            for x in reversed(range(grid.width)):
                for y in range(grid.height):
                    val = grid.Val((x,y))
                    pos = (x * halfTile + y * halfTile , -x * quarterTile + y * quarterTile + mid)
                    if val != '.':
                        self.surface.blit(self.imgs[eval(val)],pos)  

                    if sprites != None and (x,y) in sprites:
                        for spriteAtPos in sprites[(x,y)]:
                            img, rect = spriteAtPos.imageRect()
                            ratio = (spriteAtPos.currentFrame / spriteAtPos.nbFrames) - 1
                            delta = sclPos(ratio,dirs4[spriteAtPos.dir])
                            npos = addPos(spriteAtPos.pos, delta)
                            
                            pos = (npos[0] * halfTile + npos[1] * halfTile , -npos[0] * quarterTile + npos[1] * quarterTile + mid)
                            self.surface.blit(img,(pos[0], pos[1] + spriteAtPos.offset),rect)  
                            

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

    def capture(self, ratio = 1):
        if (self.enabled):
            rgb = pygame.surfarray.array3d(self.surface)
            rgb = np.moveaxis(rgb, 0, 1)
            frameImage = Image.fromarray(np.uint8(rgb))
            if ratio > 1:
                frameImage = frameImage.resize((self.screenSize[0]//ratio, self.screenSize[1]//ratio), Image.Resampling.LANCZOS)
            self.frames.append(frameImage)                    
                        
    def saveGif(self , filename):
        if (self.enabled):
            self.frames[0].save(
                filename, save_all=True, optimize=False,
                append_images=self.frames[1:],
                loop=0, duration=int(1000 / 60))                    