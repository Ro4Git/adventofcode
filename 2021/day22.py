#Advent of code 2021: Day 22
#https://adventofcode.com/2021/day/22
import re, time, copy, sys, math, pygame
from collections import defaultdict
from functools import reduce,cmp_to_key
from itertools import combinations, combinations_with_replacement

f = open('input_day22.txt', 'r')
lines = f.readlines()
lines = [line.rstrip("\n") for line in lines]
f.close()

cuboids=[]
for line in lines: 
    state = int(line.startswith("on"))
    corners = [[int(value) for value in tokens[2:].split("..")] for tokens in line[4-state:].split(",")]
    cuboids.append((state,corners))
#print(cuboids)    

limitCube = [[-50,50],[-50,50],[-50,50]]

# display Data
screenSize = 1300
cellSize = 5
angle = 0
cx= screenSize//2
cy= screenSize//2


def fullyIn(cube1,cube2): # is cube 2 fully in cube1
    for i in range(3):
        if not (cube2[i][0]>=cube1[i][0] and cube2[i][1]<=cube1[i][1]):
            return False 
    return True

def splitCubeOnAxis(cube1,cube2,axis):
    for i in range(3):
        if cube1[i][1]<cube2[i][0] or cube2[i][1] < cube1[i][0]:
            return [cube2]
    if cube2[axis][0]<cube1[axis][0]:
        if cube2[axis][1]<=cube1[axis][1]:
            #  [     +------+     ]
            #  [+------+          ]
            ncube1 = copy.deepcopy(cube2)
            ncube2 = copy.deepcopy(cube2)
            ncube1[axis][1] = cube1[axis][0]-1 
            ncube2[axis][0] = cube1[axis][0] 
            return [ncube1,ncube2]
        else:
            #  [     +------+        ]
            #  [  +------------+     ]
            ncube1 = copy.deepcopy(cube2)
            ncube2 = copy.deepcopy(cube2)
            ncube3 = copy.deepcopy(cube2)
            ncube1[axis][1] = cube1[axis][0]-1 
            ncube2[axis][0] = cube1[axis][0] 
            ncube2[axis][1] = cube1[axis][1] 
            ncube3[axis][0] = cube1[axis][1]+1 
            return [ncube1,ncube2,ncube3]
    else:
        if cube2[axis][1]>cube1[axis][1]:
            #  [     +----------+      ]
            #  [        +-----------+  ]
            ncube1 = copy.deepcopy(cube2)
            ncube2 = copy.deepcopy(cube2)
            ncube1[axis][1] = cube1[axis][1] 
            ncube2[axis][0] = cube1[axis][1]+1 
            return [ncube1,ncube2]
        else:
            #  [     +----------+    ]
            #  [        +----+       ]
            return [cube2]

# do "+" of cube 1 and cube 2 and returns the generated cubes
def cuboidsUnion(cube1,cube2):
    # fully disssociated cubes
    for i in range(3):
        if cube1[i][1]<cube2[i][0] or cube2[i][1] < cube1[i][0]:
            return None
    toSplit = [cube2]
    #--- divide cube2 in sub cubes 
    for i in range(3):
        newCubes = []
        for cube in toSplit:
            res = splitCubeOnAxis(cube1,cube,i)
            newCubes.extend(res)
        toSplit = newCubes
    #--- union: remove fully cubes still inside cube1
    return [cube for cube in toSplit if not fullyIn(cube1,cube)]

# do "-" of cube 1 and cube 2 and returns the generated cubes
def cuboidsRemove(cube1,cube2):
    #--- intersection: remove fully overlapping cubes 
    # fully disssociated cubes
    for i in range(3):
        if cube1[i][1]<cube2[i][0] or cube2[i][1] < cube1[i][0]:
            return [cube1]
    toSplit = [cube1]
    #--- divide cube1 in sub cubes 
    for i in range(3):
        newCubes = []
        for cube in toSplit:
            res = splitCubeOnAxis(cube2,cube,i)
            newCubes.extend(res)
        toSplit = newCubes
    return [cube for cube in toSplit if not fullyIn(cube2,cube)]



def sizeCube(cube):
    return reduce((lambda x, y: x * y),[(c[1]-c[0])+1 for c in cube])

def info(cubes):
    totalLit = sum([sizeCube(c) for c in cubes])
    print(f"{len(cubes)} cubes = {totalLit} lit cells")


pygame.init()
surface = pygame.display.set_mode((screenSize,screenSize))

def project3D(pos3d):
    cosa  = math.cos((math.pi * angle / 180))
    sina  = math.sin((math.pi * angle / 180))
    return  ( ((pos3d[0]*cosa + pos3d[1]*sina) * cellSize) + cx , -0.7*((pos3d[2] - pos3d[0]*sina + pos3d[1]*cosa) * cellSize) + cy)


faceColors = [(128,128,128),(128,128,128),(255,128,128),(192,192,128),(128,255,128),(128,128,255)]
faceIndex = [[0,1,2,3],[4,5,6,7],[5,6,2,1],[6,7,3,2],[7,4,0,3],[4,5,1,0]]
faceShift = [(0,0,1),(0,0,1),(1,0,0),(0,1,0),(1,0,0),(0,1,0)]
facesPerQuadrant = [[5,2],[2,3],[3,4],[4,5]]


def drawCube(cube):
    points = [(cube[0][0],cube[1][0],cube[2][0]),(cube[0][1],cube[1][0],cube[2][0]),(cube[0][1],cube[1][1],cube[2][0]),(cube[0][0],cube[1][1],cube[2][0]),\
            (cube[0][0],cube[1][0],cube[2][1]),(cube[0][1],cube[1][0],cube[2][1]),(cube[0][1],cube[1][1],cube[2][1]),(cube[0][0],cube[1][1],cube[2][1])]
    points2D = [project3D(point) for point in points]
    
    def drawFace(index):
        pts = [points2D[i] for i in faceIndex[index]]
        color = tuple([min(255,faceShift[index][i] * points[faceIndex[index][0]][i]  + faceColors[index][i]) for i in range(3)])
        pygame.draw.polygon(surface, color, pts)    
    #drawOrder = [0,1,2,3,0,4,5,6,7,4,0,3,7,6,2,1,5]
    #points2D = [project3D(points[index]) for index in drawOrder]
    #pygame.draw.aalines(surface, (255,255,255), False,points2D)
    quad = int(angle / 90) &  3
    drawFace(facesPerQuadrant[quad][0])
    drawFace(facesPerQuadrant[quad][1])
    drawFace(1)


def compFuncIncX(cube1,cube2):
    if cube1[0][1] <= cube2[0][0]:
        return -1
    if cube1[0][0] >= cube2[1][1]:
        return 1
    return 0 

def compFuncIncY(cube1,cube2):
    if cube1[1][1] <= cube2[1][0]:
        return -1
    if cube1[1][0] >= cube2[1][1]:
        return 1
    return 0 

def compFuncIncZ(cube1,cube2):
    if cube1[2][1] <= cube2[2][0]:
        return -1
    if cube1[2][0] >= cube2[2][1]:
        return 1
    return 0 


def drawCubes(cubes):
    global angle
    pause = False

    while True:
        surface.fill((0,0,0),(0,0,screenSize,screenSize))

        # sort along z axis 
        
        quadrant1 = int(angle / 90) &  3
        quadrant2 = int(((angle+45)%360) / 90) &  3
        xsign = 1 if angle < 180 else -1
        ysign = -1 if quadrant1==0 or quadrant1==3 else 1

        cubes.sort(key = cmp_to_key(compFuncIncZ))

        if (quadrant2 & 1):
            cubes.sort(key = cmp_to_key(compFuncIncY),reverse = (ysign==-1))
            cubes.sort(key = cmp_to_key(compFuncIncX),reverse = (xsign==-1))
        else:
            cubes.sort(key = cmp_to_key(compFuncIncX),reverse = (xsign==-1))
            cubes.sort(key = cmp_to_key(compFuncIncY),reverse = (ysign==-1))
      
        pygame.display.set_caption(f"Quadrants({quadrant1},{quadrant2}) - angle {angle}")

        for cube in cubes:
            drawCube(cube)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                return 
            if event.type == pygame.MOUSEBUTTONDOWN:
                pause = True
            if event.type == pygame.MOUSEBUTTONUP:
                pause = False
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()              
        if not pause:
            angle += 0.1
            while (angle >= 360):
                angle = angle - 360


def part1():
    onCubes = [cuboids[0][1]]
    info(onCubes)

    for cuboid in cuboids[1:]:
        newCubes = []
        if cuboid[0]:
            toTest = [cuboid[1]]
            newCubes.extend(onCubes) # adding so all existing cubes will be kept
            while len(toTest)>0:
                cube = toTest.pop()
                noInter = True
                for existingCube in onCubes:
                    res = cuboidsUnion(existingCube,cube)
                    if (res != None):
                        toTest.extend(res)
                        noInter = False
                        break
                if noInter:
                    newCubes.append(cube)
        else:
            for existingCube in onCubes:
                res = cuboidsRemove(existingCube,cuboid[1])
                newCubes.extend(res)
        onCubes = newCubes
        if (fullyIn(limitCube,cuboid[1])):
            info(onCubes)
            drawCubes(onCubes)
    info(onCubes)
    return

def part2():
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

