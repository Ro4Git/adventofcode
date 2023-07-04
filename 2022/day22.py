#Advent of code 2022: Day 22
#https://adventofcode.com/2022/day/22
import re, time, copy, functools,sys
import pygame

f = open('input_day22.txt', 'r')
lines = f.readlines()
lines = [line.rstrip("\n") for line in lines]
f.close()

dirs = [(1,0),(0,1),(-1,0),(0,-1)]
turns = {'R':1,'L':-1}
code = {' ':-1,'.':0,'#':1}
#    1  2
#    3  
# 5  4
# 6
# rotations : 0: none , 1: 90 CW, 2: 180 , 3: 90 CCW
facesPos = [(50,0),(100,0),(50,50),(50,100),(0,100),(0,150)]
faceNeighbours = [[(1,0),(2,0),(4,2),(5,3)],
                    [(3,2),(2,3),(0,0),(5,0)],
                    [(1,1),(3,0),(4,1),(0,0)],
                    [(1,2),(5,3),(4,0),(2,0)],
                    [(3,0),(5,0),(0,2),(2,3)],
                     [(3,1),(1,0),(0,1),(4,0)]]

instructions = re.split("([LR])",lines[-1])
print(instructions[-1])

lines = lines[:-2]
width = max([len(line) for line in lines])
height = len(lines)

grid =[]
for line in lines: 
    grid.append([code[line[i]] if i<len(line) else -1 for i in range(width)])

faces = []
for f in range(6):
    faces.append([])
    for y in range(50):
        faces[f].append(grid[facesPos[f][1]+y][facesPos[f][0]:facesPos[f][0]+50])

def add(pos1,pos2):
    return (pos1[0]+pos2[0],pos1[1]+pos2[1])

def doMovePart2(pos,face,dir):
    delta = dirs[dir]
    newPos = add(pos,delta)
    newFace = face
    newDir = dir
    if newPos[0]>49:
        newFace = faceNeighbours[face][0][0]
        newDir = ccwDir(dir,faceNeighbours[face][0][1])
        newPos = rotatedCoordsCCW((0,newPos[1]),faceNeighbours[face][0][1])
        print("transition right",(pos,face,dir),' => ', (newPos,newFace,newDir))
    elif newPos[1]>49:
        newFace = faceNeighbours[face][1][0]
        newDir = ccwDir(dir,faceNeighbours[face][1][1]) 
        newPos = rotatedCoordsCCW((newPos[0],0),faceNeighbours[face][1][1])    
        print("transition down",(pos,face,dir),' => ', (newPos,newFace,newDir)) 
    elif newPos[0]<0:
        newFace = faceNeighbours[face][2][0]
        newDir = ccwDir(dir,faceNeighbours[face][2][1])
        newPos = rotatedCoordsCCW((49,newPos[1]),faceNeighbours[face][2][1])
        print("transition left",(pos,face,dir),' => ', (newPos,newFace,newDir))
    elif newPos[1]<0:
        newFace = faceNeighbours[face][3][0]
        newDir = ccwDir(dir,faceNeighbours[face][3][1])
        newPos = rotatedCoordsCCW((newPos[0],49),faceNeighbours[face][3][1])
        print("transition up",(pos,face,dir),' => ', (newPos,newFace,newDir))

    if faces[newFace][newPos[1]][newPos[0]] == 1:
        return (pos,face,dir)
    return (newPos,newFace,newDir)

def rotatedCoordsCCW(pos,rotation):
    rotatedPos = pos
    if rotation == 3:
        rotatedPos = (49-pos[1],pos[0])
    elif rotation == 2:
        rotatedPos = (49-pos[0],49-pos[1])
    elif rotation == 1:
        rotatedPos = (pos[1],49-pos[0])
    return rotatedPos

def rotatedCoordsCW(pos,rotation):
    rotatedPos = pos
    if rotation == 1:
        rotatedPos = (49-pos[1],pos[0])
    elif rotation == 2:
        rotatedPos = (49-pos[0],49-pos[1])
    elif rotation == 3:
        rotatedPos = (pos[1],49-pos[0])
    return rotatedPos

def getPixelPart1(pos):
    if  not (height > pos[1] >= 0):
        return -1
    if  not (width > pos[0] >= 0):
        return -1
    return grid[pos[1]][pos[0]]

def doMovePart1(pos,add):
    newPos = (pos[0]+add[0],pos[1]+add[1])
    newVal = getPixelPart1(newPos)
    if newVal == -1:
        # out of bound, wrap around
        tPos = pos
        while (getPixelPart1(tPos) != -1):
            newPos = tPos
            tPos = (tPos[0]-add[0],tPos[1]-add[1])
        if getPixelPart1(newPos) == 1:
            return pos
        return newPos
    elif newVal == 1:
        return pos
    return newPos

def cwDir(dir,turn):
    return  (dir + turn) % 4

def ccwDir(dir,turn):
    return  (dir - turn) % 4

def applyInstructionsPart1(pos):
    currentDirIndex = 0
    newPos = pos
    for instr in instructions: 
        if instr in ['L','R']:
            currentDirIndex = cwDir(currentDirIndex,turns[instr])
        else:
            move = int(instr)
            if move>0: 
                for i in range(move):
                    newPos = doMovePart1(newPos,dirs[currentDirIndex])  
                    grid[newPos[1]][newPos[0]] = 2
       # display1()          
    return (newPos,currentDirIndex)

pygame.init()
surface = pygame.display.set_mode((width*4,height*4))

def drawGrid(surface,grid,xoffset =0,yoffset=0):
    for y,row in enumerate(grid):
        for x,val in enumerate(row):
            rect = ((x+xoffset)*4,(y+yoffset)*4,4,4)
            if val>=0:
                surface.fill((val*127,(val&1)*255,(val&1)*255),rect)

def display1():
    drawGrid(surface,grid)
    pygame.display.update()     
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()     

def display2():
    for i in range(6):
        drawGrid(surface,faces[i],facesPos[i][0],facesPos[i][1])
    pygame.display.update()     
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()           
      


def part1():
    startPos = (50,0)
    endPos = applyInstructionsPart1(startPos)
    endPos = ((endPos[0][0]+1,endPos[0][1]+1),endPos[1])
    print(endPos)
    print(1000*endPos[0][1]+4*endPos[0][0]+endPos[1])
    return

def applyInstructionsPart2():
    currentDirIndex = 0
    currentFace = 0
    currentPos = (0,0)
    for instr in instructions: 
        if instr in ['L','R']:
            currentDirIndex = cwDir(currentDirIndex,turns[instr])
        else:
            move = int(instr)
            if move>0: 
                for i in range(move):
                    currentPos,currentFace,currentDirIndex = doMovePart2(currentPos,currentFace,currentDirIndex)  
                    faces[currentFace][currentPos[1]][currentPos[0]] = 2
                #    display2()  
                
    return (currentPos,currentFace,currentDirIndex)

def part2():
    result = applyInstructionsPart2()
    print(result)
    endPos =  add(facesPos[result[1]],result[0])
    print(endPos)

    print(1000*(endPos[1]+1)+4*(endPos[0]+1)+result[2])

    # too high 116011
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
