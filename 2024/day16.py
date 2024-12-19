#Advent of code 2024: Day 16
#https://adventofcode.com/2024/day/16
import re, time, copy , functools, itertools
from collections import defaultdict
import aoc
import sortedcontainers

lines = aoc.ReadPuzzleInput("input_day16.txt")
grid = aoc.ToGrid(lines)

display = aoc.Display(True, grid.width, grid.height,    4 , 1 , 32)
deer = aoc.OrientedSprite("Tile32_deer",11,-10)

class pathNode:
    def __init__(self , pos, dir):
        self.pos = pos
        self.dir = dir
    def __eq__(self, other):
        return other and self.pos == other.pos and self.dir == other.dir
    def __ne__(self, other):
        return not self.__eq__(other)
    def __hash__(self):
        return hash((self.pos, self.dir))        
    def __str__(self):        
        return str(self.__dict__)        

startPos = pathNode(grid.Find('S'),aoc.east)
endPos = pathNode(grid.Find('E'),-1)
print(startPos,endPos)



def explore(startNode,endNode):
    scores = {startNode:0}
    toVisit = sortedcontainers.SortedList(key=lambda x: -scores[x])
    toVisit.add(startNode)
    while len(toVisit):
        currentNode = toVisit.pop()
        if currentNode != endNode:
            for n in neighbors(currentNode):
                if n.pos == endNode.pos:
                    n.dir = -1
                newscore = scores[currentNode] + distance(currentNode,n)
                if n in scores:
                    if newscore < scores[n]:
                        #add node to visit
                        scores[n] = newscore
                        toVisit.add(n)
                else:
                    scores[n] = newscore
                    toVisit.add(n)
    # follow the minimal trail path back
    maxScore = scores[endNode]
    potentials = []
    prevleft = pathNode(aoc.subPos(endNode.pos,aoc.dirs4[aoc.east]),aoc.east)
    prevdown = pathNode(aoc.subPos(endNode.pos,aoc.dirs4[aoc.north]),aoc.north)
    onMinPath = {endNode:maxScore}
    if scores[prevleft] < maxScore:
        potentials.append(prevleft)
        onMinPath[prevleft] = scores[prevleft]
    if scores[prevdown] < maxScore:        
        potentials.append(prevdown)
        onMinPath[prevdown] = scores[prevdown]
    
    reversePath = []
    resultPath = []
    while len(potentials):
        currentNode = potentials.pop()
        reversePath.append(currentNode)
        if currentNode != startNode:
            prevs = prev_neighbors(currentNode)
            for n in prevs:
                if scores[n] < scores[currentNode] and not n in onMinPath and scores[currentNode] == scores[n] + distance(n,currentNode):
                    potentials.append(n)
                    onMinPath[n] = scores[n]
        else:
            resultPath = reversePath.copy()

    uniquePos = {cell.pos:True for cell in onMinPath.keys()}
    print(len(uniquePos))
    return maxScore , resultPath

def neighbors(n):
    # check neighbour in current direction
    result = []
    nextPos = aoc.addPos(n.pos,aoc.dirs4[n.dir])
    if (grid.Val(nextPos)) != "#":
        result.append(pathNode(nextPos,n.dir))
    # 2 other neighbours are rotation
    result.append(pathNode(n.pos,aoc.turn90right[n.dir]))
    result.append(pathNode(n.pos,aoc.turn90left[n.dir]))
    return result

def prev_neighbors(n):
    # check neighbour in current direction
    result = []
    nextPos = aoc.subPos(n.pos,aoc.dirs4[n.dir])
    if (grid.Val(nextPos)) != "#":
        result.append(pathNode(nextPos,n.dir))
    # 2 other neighbours are rotation
    result.append(pathNode(n.pos,aoc.turn90right[n.dir]))
    result.append(pathNode(n.pos,aoc.turn90left[n.dir]))
    return result
    
def distance(n1, n2):
    if n2.dir != -1 and n1.dir != n2.dir:
        return 1000
    return 1

def drawStuff(grid, pos):
    display.clear()
    prevPos = aoc.subPos(pos,aoc.dirs4[deer.dir])
    deer.pos = pos
    display.drawGridTiles(grid, lambda x : x,   {pos:[deer],prevPos:[deer]})
    display.update()   
    deer.step()
    display.capture()  

def part1():
    deer.currentFrame = 10
    drawStuff(grid,startPos.pos)
    display.waitKey()
    score , resultpath = explore(startPos,endPos)
    print(score)
    prevPos = startPos
    for path in reversed(resultpath):
        deer.setDir(path.dir)
        if prevPos.pos!=path.pos:
            deer.currentFrame = 0
            for i in range(11):
                time.sleep(0.010)
                drawStuff(grid,path.pos)
            prevPos = path
    
    #display.saveGif("day16_p1.gif")
    return 

def part2():
    # for each node on the path, try one of the neighbour that was not selected as part of the path 
    # as alternaate
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
