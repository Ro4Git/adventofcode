#Advent of code 2023: Day 10
#https://adventofcode.com/2023/day/10
import re, time, copy, math

f = open('input_day10.txt', 'r')
lines = f.readlines()
lines = [line.rstrip("\n") for line in lines]
f.close()


#| is a vertical pipe connecting north and south.
#- is a horizontal pipe connecting east and west.
#L is a 90-degree bend connecting north and east.
#J is a 90-degree bend connecting north and west.
#7 is a 90-degree bend connecting south and west.
#F is a 90-degree bend connecting south and east.

grid = [[c for c in line] for line in lines]
width = len(grid[0])

codes = {
    "|": ((0,-1),(0,1)),
    "-": ((-1,0),(1,0)),
    "L": ((0,-1),(1,0)),
    "J": ((0,-1),(-1,0)),
    "7": ((-1,0),(0,1)),
    "F": ((1,0),(0,1))
}

dirs = [(-1,0),(1,0),(0,-1),(0,1)]

def addDelta(pos,delta):
    return (pos[0]+delta[0],pos[1]+delta[1])

def oppDelta(delta):
    return (-delta[0],-delta[1])

def getGrid(pos):
    return grid[pos[1]][pos[0]]

# find startPos
startPos = (0,0)
for i,line in enumerate(lines): 
    index  = line.find('S')
    if index>=0:
        startPos = (index,i)
        break
print(startPos)

# find startNeightbours
neighbours = []
for delta in dirs:
   nPos = addDelta(startPos,delta)
   code = getGrid(nPos)
   if oppDelta(delta) in codes[code]:
       #this cell connects to startPos
       neighbours.append(nPos)
       break

#hardcoded, in our case S is actually a "|"
grid[startPos[1]][startPos[0]] = '|'
print(neighbours)       

def getNextInLoop(fromNode,currentNode):
    currentNodeCode = getGrid(currentNode)
    n1 = addDelta(currentNode,codes[currentNodeCode][0])
    n2 = addDelta(currentNode,codes[currentNodeCode][1])
    if n1 == fromNode: 
        return n2
    else:
        return n1

def buildLoop():
    currentNode = neighbours[0]
    prevNode = startPos
    while currentNode != startPos:
        nextNode = getNextInLoop(prevNode,currentNode)
        neighbours.append(nextNode)
        prevNode = currentNode
        currentNode = nextNode

# return number of inside cell in a row 
def parseLine(lineIndex):
    nbInOuts = [0,0]
    currentlyInside = 0
    startBlockChar = ''
    i = 0
    while i < len(grid[0]):
        newChar = getGrid((i,lineIndex))
        # cell is not loop, add it to respective counter
        if not (i,lineIndex) in neighbours:
            nbInOuts[currentlyInside] = nbInOuts[currentlyInside] +1
        else:
            if newChar == '|':
                currentlyInside = (currentlyInside + 1) & 1
            elif newChar == 'F':
                #advance until finding either "J" or "7"
                while newChar != 'J' and newChar != '7':
                    i = i + 1
                    newChar = getGrid((i,lineIndex))
                if newChar == 'J':
                    currentlyInside = (currentlyInside + 1) & 1
            elif newChar == 'L':
                #advance until finding either "J" or "7"
                while newChar != 'J' and newChar != '7':
                    i = i + 1
                    newChar = getGrid((i,lineIndex))
                if newChar == '7':
                    currentlyInside = (currentlyInside + 1) & 1
        i = i + 1     
    return nbInOuts[1]

def part1():
    buildLoop()
    print(neighbours)
    print(len(neighbours)/2)
    return 

def part2():
    ins = [parseLine(i) for i in range(len(grid))]
    print(sum(ins))

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