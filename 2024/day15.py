#Advent of code 2024: Day 15
#https://adventofcode.com/2024/day/15
import re, time, copy , functools, itertools
from collections import defaultdict
import aoc

#  0: > , 1: v , 2: < , 3: ^
dirs = {'>':0,'v':1,'<':2,'^':3}
colors = {'.': (0,0,0),'#':(180,180,180),'O':(255,50,0), '[':(255,100,0), ']':(255,0,100)}

lines = aoc.ReadPuzzleInput("input_day15.txt")
sections = aoc.ToSections(lines)

#### grid for part 1 ##########
grid = aoc.ToGrid(sections[0])
startPos = grid.Find('@')
grid.Set(startPos,'.')

#### grid for part 2 ##########
newLines = [line.replace("#",'##').replace("O",'[]').replace(".",'..').replace("@",'@.') for line in sections[0]]
grid2 = aoc.ToGrid(newLines)
startPos2 = grid2.Find('@')
grid2.Set(startPos2,'.')

#### movements ##########
movements = []
[movements.extend(list(mov)) for mov in sections[1]]

print(grid.width,grid.height)
print(grid2.width,grid2.height)
print(len(movements))

display = aoc.Display(True, grid.width*2, grid.height,    6 , 1 , 32)

def moveRobot(startPos, dir): 
    delta = aoc.dirs4[dirs[dir]]
    nextPos = aoc.addPos(startPos,delta)
    nextVal = grid.Val(nextPos)
    # hitting a wall 
    if nextVal == "#":
        return startPos
    if nextVal == "O":
        # there is a box 
        # keep going in that direction until we find an empty space 
        upToPos = nextPos
        while nextVal == 'O':
            upToPos = aoc.addPos(upToPos,delta)
            nextVal = grid.Val(upToPos)
        if nextVal == '.':
            # there is empty space where boxes can be pushed
            grid.Fill(nextPos,upToPos,'O')
            grid.Set(nextPos,'.')
            return nextPos
        elif nextVal == "#":
            # this cannot be pushed 
            return startPos
        else: 
            print("problem")
            return startPos
    else:
        return nextPos


def drawStuff(grid,currentPos,mov):
    display.clear()
    display.drawGridTiles(grid)
    display.drawListPosTiles([currentPos],mov)
    display.update()   
    display.capture()   
    
def gpsCoordsVal(grid , obstacle):
    gpsCoords = 0
    for y,row in enumerate(grid.data):
        for x,v in enumerate(row):
            if v == obstacle:
                gpsCoords += 100 * y + x
    print(gpsCoords)  
    
def part1():
    currentPos = startPos
    for i,mov in enumerate(movements):
        currentPos = moveRobot(currentPos,mov) 
        if i % 100 == 0:
            drawStuff(grid,currentPos, mov)
    display.saveGif("day15_p1.gif")
    gpsCoordsVal(grid,"O")
    return 

def moveCells(listCells, dir):
    for pos,v in listCells.items():
        grid2.Set(pos,'.')
    for pos,v in listCells.items():
        grid2.Set(aoc.addPos(pos,dir),v)
    
def moveableCells(listCells, dir):
    # all cells should have either a free neighbour or another box
    # to be able to move
    for pos,v in listCells.items():
        next = grid2.ValNext(pos,dir)
        if next=='#':
            return False
    return True

def findNextCellsToMove(listCells, dir): 
    newCells = {}
    for pos,v in listCells.items():
        nextPos = aoc.addPos(pos,dir)
        if not nextPos in newCells and not nextPos in listCells:
            nextVal = grid2.Val(nextPos)
            if nextVal == "[" or nextVal == "]":
                # add the first 2 cells of the box to the list of moveables and repeat process
                newCells[nextPos] = nextVal
                if nextVal == "]":
                    newCells[(nextPos[0]-1,nextPos[1])] = '['
                else:
                    newCells[(nextPos[0]+1,nextPos[1])] = ']'   
    return newCells   
    
def moveRobot2(startPos, dir): 
    delta = aoc.dirs4[dirs[dir]]
    nextPos = aoc.addPos(startPos,delta)
    nextVal = grid2.Val(nextPos)
    # hitting a wall 
    if nextVal == "#":
        return startPos
    if nextVal == "[" or nextVal == "]":
        # add the first 2 cells of the box to the list of moveables and repeat process
        allCells = {}
        exploreCells = { nextPos:nextVal}
        if nextVal == "]":
            exploreCells[(nextPos[0]-1,nextPos[1])] = '['
        else:
            exploreCells[(nextPos[0]+1,nextPos[1])] = ']'
        allCells.update(exploreCells)
        while len(exploreCells):
            exploreCells = findNextCellsToMove(exploreCells , delta)
            allCells.update(exploreCells)
            
        if moveableCells(allCells,delta):
            moveCells(allCells,delta)
            return nextPos
        else:
            return startPos

    else:
        return nextPos

def part2():
    currentPos = startPos2
    for i,mov in enumerate(movements):
        currentPos = moveRobot2(currentPos,mov) 
        if i % 100 == 0:
            drawStuff(grid2,currentPos,mov)
    
    display.saveGif("day15_p2.gif")
    gpsCoordsVal(grid2,"[")
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
