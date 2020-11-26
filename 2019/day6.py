import copy 
import numpy
import pygame
import itertools
import anytree
from anytree import Node, RenderTree, AsciiStyle

#array of line segment 
#cross all segments with one another and keep the one closest to start point

def countOrbit(node, prevOrbit):
    nbOrbit = prevOrbit + node.depth
    for child in node.children:
        nbOrbit = nbOrbit + countOrbit(child, prevOrbit)
    return nbOrbit

orbits= []
com = Node('COM')
f = open('input_day6.txt','r')
parents ={}
lines = f.readlines()
for l in lines:
    p = l.rstrip('\n').split(')')
    p0 = p[0]
    p1 = p[1]
    res0 = anytree.search.find_by_attr(com, p0)
    res1 = anytree.search.find_by_attr(com, p1)
    parents[p1] = p0
    parent = com
    child = com
    if (res0 is None):
        print("No parent found {0}".format(p0))
        parent = Node(p0 , com)
    else:
        parent = res0
    if (res1 is None):
        print("No child found {0}".format(p1))
        child = Node(p1,parent)
    else:
        child = res1
        child.parent = parent

#print(countOrbit(com,0))
sanNode = anytree.search.find_by_attr(com, 'SAN')
youNode = anytree.search.find_by_attr(com, 'YOU')
print(sanNode)
print(youNode)
w = anytree.walker.Walker()
res = w.walk(sanNode,youNode)
print(res)
print(len(res[0])-1+len(res[2])-1)
#print(RenderTree(com, style=AsciiStyle()).by_attr())
#print(parents)




