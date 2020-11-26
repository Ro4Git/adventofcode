import copy 
import itertools
import time
import bisect
from curses import wrapper



def add(v,w):
    x,y = v
    X,Y = w
    return (x+X, y+Y)

def minPos(v,w):
    x,y = v
    X,Y = w
    return (min(x,X), min(y,Y))

def maxPos(v,w):
    x,y = v
    X,Y = w
    return (max(x,X), max(y,Y))

dirs = [(0,-1),(1,0),(0,1),(-1,0)]
oppdirs = [2,3,0,1]

grid= []
f = open('input_day18.txt','r')
for line in f:
    grid.append(list(line))
width = len(grid[0])
height = len(grid)

class node:
    def __init__(self, pos, letter):
        self.pos = pos
        self.arcs = []
        self.letter = letter

    def addArc(self,arc):
        self.arcs.append(arc)

class arc:
    def __init__(self,node1,node2,cost):
        self.node1 = node1
        self.node2 = node2 
        self.cost = cost

nodes = {} 

def addNode(pos,letter):
    n = node(pos,letter)
    if (letter != ''):
        nodes[letter] = n
    return n



def gridPixel(pos):
    return grid[pos[1]][pos[0]]

def explorePos(dir, n, pos, cost):
    pix = gridPixel(pos)
    if (pix == '#'):
        return -1
    else:
        nbfreecell = 0
        for i in range(4):
            if i != oppdirs[dir]:
                npos = add(pos,dirs[i])
                nbfreecell += gridPixel(npos) != '#'
        newnode = n 
        if (pix >= 'A' and pix <= 'z'):
            #letter found, open a new node and register the arc to it
            newnode = addNode(pos,pix)
            newarc = arc(n,newnode,cost)
            n.addArc(newarc)
            newnode.addArc(newarc)
            cost = 0
        elif nbfreecell>=2:
            newnode = addNode(pos,'')
            newarc = arc(n,newnode,cost)
            newnode.addArc(newarc)
            n.addArc(newarc)
            cost = 0
        for i in range(4):
            if i != oppdirs[dir]:
                npos = add(pos,dirs[i])
                explorePos(i,newnode,npos,cost+1)
    return 0     

def nextnode(node,arc):
    return arc.node2 if arc.node1 == node else arc.node1

def printTree(inString, node, depth, prevarc):
    if (node.letter==''):
        inString += '-.'
    else:
        inString += "-" + node.letter

    for arc in node.arcs:
        if (prevarc != arc):
            if prevarc == None or len(node.arcs) >2:
                inString += '\n' + '  ' * depth + '+' 
            #inString += '-' + str(arc.cost)
            inString = printTree(inString, nextnode(node,arc),depth+1,arc) 
         

    return inString

def compressTree(node, prevarc):
    toRemove = []
    res = 0
    for arc in node.arcs:
        if (prevarc != arc):
            n2 = nextnode(node,arc)
            if n2.letter == '' and len(n2.arcs) <= 2:
                # remove next node 
                for arc2 in n2.arcs:
                    if arc2 != arc:
                        n3 = nextnode(n2,arc2)
                        n3.arcs.remove(arc2)
                        n3.arcs.append(arc)
                        arc.cost += arc2.cost
                        arc.node1 = node
                        arc.node2 = n3
                        res = compressTree(n3, arc) 
                        if res == 0:
                            toRemove.append(arc)
                        break
                if len(n2.arcs) <= 1:
                    toRemove.append(arc)
            else:              
                sres = compressTree(n2, arc) 
                res += sres
                if (sres == 0):
                    toRemove.append(arc)
    
    for x in toRemove:
        node.arcs.remove(x)

    return res + (node.letter != '')


#parse entire tree, once it finds a key, unlock the door and 
def findLowestCostNode(curNode, incomingArc, branchCost, curSolution):
    if (curNode.letter >= 'a' and curNode.letter <= 'z' and (not curNode.letter in curSolution)):
        return [[branchCost,curNode,curSolution + curNode.letter]]

    if (curNode.letter >= 'A' and curNode.letter <= 'Z' and (not curNode.letter.lower() in curSolution)):
        #cannot go further this way
       return []

    solutions = []
    for arc in curNode.arcs:
        if (incomingArc != arc):
            n2 = nextnode(curNode,arc)
            res = findLowestCostNode(n2, arc, branchCost + arc.cost, curSolution)
            solutions = solutions + res

    return solutions
  


def resolveTreeOrder(rootNode, heuristic):
    totalCost = 0
    # A* node []
    openList = [[0,rootNode,""]]
    keysToFind = 1 + ord('z') - ord('a')
    solutions = []
    step = 0
    
    while len(openList) > 0:
        node = openList.pop(0)
        res = []
        if len(node[2]) == keysToFind:
            there = [item for item in solutions if item[0] == node[0]]
            if (len(there) == 0):
                solutions.append((node[0],node[2]))
                print(solutions)
                break
        else:
            res = findLowestCostNode(node[1],None,node[0],node[2])
       
        # pickup next node by the following heuristic 
        # f = costSoFar + (costSoFar / nbkeys) * nbremainingKeys
        for toInsert in res:
            #fToInsert = toInsert[0] + (keysToFind - len(toInsert[2])) * 10
            # fToInsert = toInsert[0]/ len(toInsert[2])
            fToInsert = toInsert[0]  + (keysToFind - len(toInsert[2]))  * heuristic
            if len(openList) == 0:
                openList.append(toInsert)
            else:
                for i,prevNode in enumerate(openList):    
                    #f = prevNode[0]+ (keysToFind - len(prevNode[2]))  * 10
                    # f = prevNode[0] / len(prevNode[2])
                    f = prevNode[0] + (keysToFind - len(prevNode[2]))  * heuristic
                    if fToInsert <= f:
                        openList.insert(i,toInsert)
                        break
                else:
                    openList.append(toInsert)

        #openList.sort(key=lambda x: x[0] + (keysToFind - len(x[2])) * (x[0]/len(x[2])))
        step += 1
        if (step % 100) == 0:
            print(len(openList), node[2])
        #print(openList)

    solutions.sort(key=lambda x: x[0])
    print(solutions)



def getCenterPos():
    for j,line in enumerate(grid):
        for i,c in enumerate(line):
            if c == '@':
                return (i,j)
    return (0,)

def printView():


    startPos = getCenterPos()
    root = addNode(startPos,'@')
    pos = startPos
    for i in range(4):
        npos = add(pos,dirs[i])
        explorePos(i,root,npos,1)

    print(len(nodes))
    #compressTree(root, None)
    
    str = printTree("", root, 1, None)
    print(str)

    print("---------------------------------------------")

    
    for h in reversed(range(0,100,10)):
        resolveTreeOrder(root,h)
    print("---------------------------------------------")
    #str = printTree("", root, 1, None)
    #print(str)
     

printView()