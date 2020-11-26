import copy 
import itertools
import time
import bisect
from curses import wrapper

def add(v,w):
    x,y = v
    X,Y = w
    return (x+X, y+Y)

dirs = [(0,-1),(1,0),(0,1),(-1,0)]
oppdirs = [2,3,0,1]
startletter = '@'
nbkeysToFind = 0
grid= []

f = open('input_day18.txt','r')
for line in f:
    grid.append(list(line))
width = len(grid[0])
height = len(grid)

nodes = {} 

class node:
    def __init__(self, pos, letter):
        self.pos = pos
        self.arcs = []
        self.letter = letter

    def h(self, solution):
        # number of unique keys found so far
        res = set(solution.lower())
        return nbkeysToFind - len(res)

    def addArc(self,arc):
        self.arcs.append(arc)

    def removeArc(self,arc):
        self.arcs.remove(arc)

    def getArcTo(self, node):
        for arc in self.arcs:
            if (arc.node1 == self and arc.node2 == node) or (arc.node2 == self and arc.node1 == node):
                return arc
        return None

class arc:
    def __init__(self,node1,node2,cost):
        self.node1 = node1
        self.node2 = node2 
        self.cost = cost




def addNode(pos,letter):
    if letter in nodes:
        return nodes[letter]
    else:
        n = node(pos,letter)
        nodes[letter] = n
        return n

def gridPixel(pos):
    return grid[pos[1]][pos[0]]


def explorePos(dir, n, pos, cost, sofar):
    while True:
        sofar.append(pos)
        pix = gridPixel(pos)
        if (pix == '#'):
            return -1
    
        nbfreecell = 0
        for i in range(4):
            if i != oppdirs[dir]:
                npos = add(pos,dirs[i])
                nbfreecell += gridPixel(npos) != '#'
        newnode = n 
        if (pix >= 'A' and pix <= '~'):
            #letter found, open a new node and register the arc to it
            # if path to existing node
            if pix in nodes:
                newnode = nodes[pix]
                oldarc = n.getArcTo(newnode)
                if (oldarc == None):
                    # no existing link, create one
                    newarc = arc(n,newnode,cost)
                    n.addArc(newarc)
                    newnode.addArc(newarc)                   
                else:
                    oldarc.cost = min(oldarc.cost,cost)
                return 1
            else:      
                newnode = addNode(pos,pix)
                newarc = arc(n,newnode,cost)
                n.addArc(newarc)
                newnode.addArc(newarc)
                n = newnode
                cost = 0
 
        if (nbfreecell>=2):
            for i in range(4):
                if i != oppdirs[dir]:
                    npos = add(pos,dirs[i])
                    if not npos in sofar:
                        explorePos(i,newnode,npos,cost+1,sofar)  
            return 2
        elif nbfreecell == 1:
            for i in range(4):
                if i != oppdirs[dir]:
                    npos = add(pos,dirs[i])
                    if (gridPixel(npos) != '#'):
                        pos = npos
                        dir = i
                        cost = cost + 1 
                        break
        else:
            return 0
    #end wihle                    
            
    return 0

def nextnode(node,arc):
    return arc.node2 if arc.node1 == node else arc.node1


def printTree(inString):
    for node in nodes.values():
        inString += node.letter + " - "
        for arc in node.arcs:
            inString += nextnode(node,arc).letter + "(" + str(arc.cost) +"),"
        inString += "\n"
    return inString

def isLowChar(x):
    return x >= 'a' and x <= 'z'

def isUpChar(x):
    return x >= 'A' and x <= 'Z'

def findNextKeys(nodeIn,solution,prevarcs,costIn):
    #look for a key along this arc
    res = []
    toTest = [(nodeIn,costIn)]
    while len(toTest):
        node, cost = toTest.pop(0)
        for arc in node.arcs:
            if arc in prevarcs:
                continue
            n = nextnode(node,arc)       
            if n.letter != '@' and not isLowChar(n.letter) and not (chr(ord(n.letter) + 32)) in solution:
                # path is blocked
                continue  
            if isLowChar(n.letter) and not n.letter in solution:
                # a key we didn't find yet
                res.append((n,cost + arc.cost))
                continue
            prevarcs.append(arc)
            toTest.append((n,cost+arc.cost))
    return res

def resolveTreeOrder(rootNode, heuristic):
    totalCost = 0
    # A* node []
    openList = [(rootNode,rootNode.letter,nbkeysToFind,0)]
    closeList = []
    step = 0
    
    while len(openList) > 0:
        node, solution, f, g = openList.pop(0)
        print(solution, f,g, len(closeList), len(openList))
        
        if (len(set(solution.lower())) == nbkeysToFind+1):
            print("found:",node,solution,f,g)
            break
        closeList.append((node, solution, f, g))

        nextKeys = findNextKeys(node, solution, [], 0)
        for n,cost in nextKeys:
            newg = g + cost
            newsolution = solution + n.letter                
            cexists = [(nd,sol,nf,ng) for nd,sol,nf,ng in closeList if nd ==n and (set(sol)==set(newsolution))]
            oexists = [(nd,sol,nf,ng) for nd,sol,nf,ng in openList if nd ==n and (set(sol)==set(newsolution))]

            if (not (len(oexists) or len(cexists))) or (len(oexists) and (newg < oexists[0][3])) or (len(cexists) and (newg < cexists[0][3])):

                newf  = newg + n.h(newsolution)
                if len(oexists):
                    openList.remove(oexists[0])
                if len(cexists):
                    closeList.remove(cexists[0])                       
                openList.append((n,newsolution,newf,newg))

        openList.sort(key=lambda x: x[2])
        #print(openList)

def printView():
    global nbkeysToFind
    nbkeysToFind = 0
    startPos = (0,0)
    for j,line in enumerate(grid):
        for i,c in enumerate(line):    
            if isLowChar(c):
                nbkeysToFind += 1
            if c == '@':
                startPos=(i,j)

    string = ""
    for line in grid:
        string += "".join(line)
    print(string)

    startletter = '@'
    root = addNode(startPos,startletter)
    for i in range(4):
        npos = add(startPos,dirs[i])
        explorePos(i,root,npos,1,[])

    for node in nodes.values():
        for i in range(4):
            npos = add(node.pos,dirs[i])
            explorePos(i,node,npos,1,[])

    print("Nodes : ",len(nodes))

    str = printTree("")
    print(str)

    print("---------------------------------------------")
    resolveTreeOrder(root,1)

printView()