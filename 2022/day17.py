#Advent of code 2022: Day 17
#https://adventofcode.com/2022/day/17
import re, time, copy, functools
import pygame

f = open('input_day17.txt', 'r')
lines = f.readlines()
lines = [line.rstrip("\n") for line in lines]
f.close()

pieces = [((4,1),[[1,1,1,1]]),((3,3),[[0,1,0],[1,1,1],[0,1,0]]),((3,3),[[0,0,1],[0,0,1],[1,1,1]]),((1,4),[[1],[1],[1],[1]]),((2,2),[[1,1],[1,1]])]
jetStream = lines[0]
currentMaxHeight = 0
gridOffset = 0
grid = []
currentJet = 0
windowSize = 20000

for i in range(windowSize):
    grid.append(0)  

def getGridPixel(posX,posY):
    return (grid[posY-gridOffset] & (1 << posX)) >> posX

def putGridPixel(posX,posY):
    grid[posY-gridOffset] |= (1 << posX)   

def collidePieceGrid(piece, posX,posY):
    if posX < 0 or (posX + piece[0][0]) > 7: 
        return True
    if posY < 0:
        return True 
    pieceHeight = piece[0][1]
    for y in range(piece[0][1]):
        for x in range(piece[0][0]):
            if piece[1][y][x] == 1:
                if getGridPixel(posX+x,posY+(pieceHeight-1)-y) == 1:
                    return True
    return False

def printPieceInGrid(piece, posX,posY):
    pieceHeight = piece[0][1]
    for y in range(pieceHeight):
        for x in range(piece[0][0]):
            if piece[1][y][x] == 1:
                putGridPixel(posX+x,posY+(pieceHeight-1)-y)

def initGrid(): 
    global grid
    global gridOffset
    global currentMaxHeight
    global currentJet
    
    grid = []
    for i in range(windowSize):
        grid.append(0)  
    currentJet = 0
    currentMaxHeight = 0
    gridOffset = 0

def checkGrid(): 
    global grid
    global gridOffset
    halfWindow = windowSize//2
    if currentMaxHeight + 8  - gridOffset > windowSize:
        gridOffset += halfWindow
        grid = grid[halfWindow:] 
        for i in range(halfWindow):
            grid.append(0)  

def dropPiece(piece): 
    global currentMaxHeight
    global currentJet
    posX = 2
    posY = currentMaxHeight+3
    checkGrid()
    notPlaced = True
    while notPlaced:
        nposX = posX
        nposY = posY
        # apply JetStream
        jet = jetStream[currentJet]
        if jet == '>': 
            nposX += 1
        else:
            nposX -= 1
        currentJet +=1
        currentJet = currentJet % len(jetStream)
        if collidePieceGrid(piece,nposX,posY):
            nposX = posX
        # fall by one
        if collidePieceGrid(piece,nposX,posY-1):
            
            printPieceInGrid(piece,nposX,posY)
            currentMaxHeight = max(currentMaxHeight,posY+(piece[0][1]))
            if currentMaxHeight < 0: 
                currentMaxHeight = 0 

            notPlaced = False
        else:
            posY = posY-1
            posX = nposX
        
def drawGrid(surface,grid):
    for y,row in enumerate(grid):
        if (y > 900):
            break
        for x in range(7):
            val = ((1 << x) & row) >> x
            rect = (x*10,790-y,10,1)
            surface.fill((val*127,(val & 1)*255,(val & 1)*255),rect)

pygame.init()
surface = pygame.display.set_mode((80,800))

def display():
    drawGrid(surface,grid)
    pygame.display.update()     
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()           


def part1():
    initGrid()
    for i in range(2022):
        piece = pieces[i % len(pieces)]
        dropPiece(piece)
        #if (i<500):
        #    display()
    print(currentMaxHeight)
    return

def searchRepeats(array):
    halfLen = len(array) // 2
    for x in range(2, halfLen):
        if array[0:x] == array[x:2*x] :
            return x,array[0:x]
    return 0

def part2():
    initGrid()
    for i in range(10000):
        piece = pieces[i % len(pieces)]
        dropPiece(piece)

    #repeats?
    #search for the first occurence of repeat
    start = 0
    end = 2000
    nbReps = 0
    seqRep = []
    while start != end:
        pos = (start + end) // 2
        reps = searchRepeats(grid[pos:currentMaxHeight-gridOffset])
        if reps == 0: 
             # too low
            if (pos == end -1):
                start = end
                reps = searchRepeats(grid[start:currentMaxHeight-gridOffset])
                nbReps = reps[0]
                seqRep = reps[1]
            else:
                start = pos
        else:
            # too high
            end = pos
    # repetitions start after height start and occur every nbReps
    print(start,nbReps)
    
    initGrid()
    seqDelta = []
    startingi = 0
    deltaInSequence = 0
    nbDropPerSequence = 0
    for i in range(10000):
        piece = pieces[i % len(pieces)]
        if (startingi ==0) and (currentMaxHeight>=nbReps) and grid[start:start+nbReps] == seqRep:
            startingi = i
        if (startingi >0) and grid[start+nbReps:start+nbReps+nbReps] == seqRep:
            nbDropPerSequence = i - startingi
            break
        prevIndex = currentMaxHeight
        dropPiece(piece)
        newIndex = currentMaxHeight
        if (i>=startingi and startingi>0):
            deltaInSequence+=newIndex-prevIndex
            seqDelta.append(deltaInSequence)


    nbDropPerSequence = len(seqDelta)
    startingi = startingi - nbDropPerSequence
    print(startingi, nbDropPerSequence,nbReps)
    totalHeight = 0
    totalDrop = 1000000000000

    nbDropSequence = (totalDrop-startingi)//nbDropPerSequence
    remainingDrop = (totalDrop-startingi) - nbDropSequence * nbDropPerSequence

    initGrid()
    for i in range(startingi + nbDropPerSequence + remainingDrop):
        piece = pieces[i % len(pieces)]
        dropPiece(piece)
    totalHeight = currentMaxHeight + nbReps * (nbDropSequence-1)

    print(totalHeight)

#    initGrid()
#    for i in range(totalDrop):
#        piece = pieces[i % len(pieces)]
#        dropPiece(piece)
#     totalHeight = currentMaxHeight
#     print(totalHeight)


    
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

