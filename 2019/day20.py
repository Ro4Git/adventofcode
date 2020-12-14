import copy 
import itertools
import time
import bisect



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
startletter = 'a'
endletter = 'z'
grid= []

f = open('input_day20.txt','r')
for line in f:
    grid.append(list(line))
width = len(grid[0])
height = len(grid)
visited = [0] * width * height

nodes = {} 
portals = {}
oldNames = [{},{}]
newNames = {}

class node:
    def __init__(self, pos, letter):
        self.pos = pos
        self.arcs = []
        self.letter = letter
        self.solution =""

    def h(self, layer):
        return layer * 10
        

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


def isUpChar(x):
    return x >= 'A' and x <= 'Z'

def addPortal(letter, pos):
    portals[letter] = pos


def otherPortalLetter(letter):
    return chr(ord(letter)-32) if (letter >= 'a') else chr(ord(letter)+32)

def otherPortal(letter, pos):
    letter = otherPortalLetter(letter)
    return portals[letter] if letter in portals else None


def addLetter(code, outer):
    outer = int(outer)
    if code in oldNames[outer]:
        return oldNames[outer][code]
    elif code in oldNames[1 - outer]:
        letter = otherPortalLetter(oldNames[1 - outer][code])
        oldNames[outer][code] = letter
        newNames[letter]= code
        return letter
    else:
        delta = outer * 32 
        delta2 = 32 - delta 
        for c in range(ord('B') , ord('^')+1):
            letter = chr(c+delta)
            letter2 = chr(c+delta2)
            
            if letter != 'Z' and not letter in portals and not letter2 in portals:
                newNames[letter]= code
                oldNames[outer][code] = letter
                return letter
    return "_"

def addNode(pos,letter):
    if letter in nodes:
        return nodes[letter]
    else:
        n = node(pos,letter)
        nodes[letter] = n
        return n

def gridPixel(pos):
    return grid[pos[1]][pos[0]]

def getVisited(pos):
    return visited[pos[1]*height + pos[0]]

def setVisited(pos):
    visited[pos[1]*height + pos[0]] = 1

def explorePos(dir, n, pos, cost):
    while True:
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

                pos = otherPortal(pix, pos)

                if pos != None:
                    pix = otherPortalLetter(pix)
                    newnode2 = addNode(pos,pix)
                    newarc2 = arc(newnode,newnode2,1)
                    newnode2.addArc(newarc2)
                    newnode.addArc(newarc2)

                    # go to the other side of the portal and keep going from there
                    cost = 0
                    for i in range(4):
                        npos = add(pos,dirs[i])
                        explorePos(i,newnode2,npos,cost+1)
                return 0
        else:
            if (nbfreecell>=2):
                for i in range(4):
                    if i != oppdirs[dir]:
                        npos = add(pos,dirs[i])
                        explorePos(i,newnode,npos,cost+1)  
                return 2
            if nbfreecell == 1:
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

def isOuter(letter):
    return letter >= 'a'

def isValidAtLayer(n, layer):
    #return True
    if (layer == 0):
        #only inner or a or z
        return not isOuter(n.letter) or n.letter == 'a' or n.letter == 'z'
    else:
        return not (n.letter == 'a' or n.letter == 'z')

def resolveTreeOrder(rootNode, heuristic):
    totalCost = 0
    # A* node []
    openList = [(rootNode,0,0,0)]
    closeList = []
    step = 0
    rootNode.solution = rootNode.letter
    





    while len(openList) > 0:
        node, layer, f, g = openList.pop(0)
        print(node.solution, layer, f,g, len(closeList), len(openList))
        if (node.letter == endletter):
            print("found:",node,layer,f,g)
            break
        closeList.append((node, layer, f, g))

        for arc in node.arcs:
            n = nextnode(node,arc)
            sublayer = layer
            if (arc.cost == 1): 
                # going through portal, layer will change
                if isOuter(node.letter):
                    sublayer = sublayer - 1
                else:
                    sublayer = sublayer + 1
                
            if isValidAtLayer(n,sublayer):
                newg = g + arc.cost
                
                cexists = [(nd,ly,nf,ng) for nd,ly,nf,ng in closeList if ly == sublayer and nd ==n]
                oexists = [(nd,ly,nf,ng) for nd,ly,nf,ng in openList if ly == sublayer and nd ==n]

                if (not (len(oexists) or len(cexists))) or (len(oexists) and (newg < oexists[0][3])) or (len(cexists) and (newg < cexists[0][3])):
                    n.solution = node.solution + n.letter + str(sublayer)
                    newf  = newg + n.h(sublayer)
                    if len(oexists):
                        openList.remove(oexists[0])
                    if len(cexists):
                        closeList.remove(cexists[0])                       
                    openList.append((n,sublayer,newf,newg))

        openList.sort(key=lambda x: x[2])
        #print(openList)


def preProcessTree():
    newGrid = copy.copy(grid)
    for j,line in enumerate(grid):
        for i,c in enumerate(line):    
            if c == ' ':
                newGrid[j][i] = '#'
            elif isUpChar(c):
                outer = False
                if i==0 or i >= width-4 or j==0 or j >= height-4:
                    outer = True

                if i<width-1 and isUpChar(grid[j][i+1]):
                    #horizontal ?
                    code = c + grid[j][i+1]
                    # was this code already found? 
                    letter = addLetter(code, outer)
           
                    if i>0 and grid[j][i-1] == '.':
                        newGrid[j][i-1] = letter
                        addPortal(letter,(i-1,j))
                    elif i<width-2 and grid[j][i+2] == '.':
                        newGrid[j][i+2] = letter
                        addPortal(letter,(i+2,j))
                    newGrid[j][i]   = '#'
                    newGrid[j][i+1] = '#'
                elif j<height-1 and isUpChar(grid[j+1][i]): 
                    #vertical 
                    code = c + grid[j+1][i]
                    # was this code already found? 
                    letter = addLetter(code, outer)
                    if j>0 and grid[j-1][i] == '.':
                        newGrid[j-1][i] = letter
                        addPortal(letter,(i,j-1))
                    elif j<height-2 and grid[j+2][i] == '.':
                        newGrid[j+2][i] = letter
                        addPortal(letter,(i,j+2))
                    newGrid[j][i]   = '#'
                    newGrid[j+1][i] = '#'

                # found a character replace it by a portal 
    return newGrid

def printView():
    oldNames[1]['AA'] = 'a'
    oldNames[1]['ZZ'] = 'z'
    newNames['a'] = 'AA'
    newNames['z'] = 'ZZ'
    grid = preProcessTree()

    string = ""
    for line in grid:
        string += "".join(line)
    print(string)
    print(portals)
    print(oldNames)

    startletter = 'a'
    endletter = 'z'
    startPos = portals[startletter]
    root = addNode(startPos,startletter)
    for i in range(4):
        npos = add(startPos,dirs[i])
        explorePos(i,root,npos,1)

    for node in nodes.values():
        for i in range(4):
            npos = add(node.pos,dirs[i])
            explorePos(i,node,npos,1)

    print("Nodes : ",len(nodes))

    str = printTree("")
    print(str)

    #print("---------------------------------------------")

    
    
    resolveTreeOrder(root,1)
    print(nodes[endletter])

    print("---------------------------------------------")
    print(nodes[endletter].solution)
    str = ""
    for c in nodes[endletter].solution:
        if not c.isdigit():
            str += newNames[c] + "-"
    print(str)

    

     

printView()