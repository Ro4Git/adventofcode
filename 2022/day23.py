#Advent of code 2022: Day 23
#https://adventofcode.com/2022/day/23
import re, time, copy, functools,sys
from collections import defaultdict
import pygame

f = open('input_day23.txt', 'r')
lines = f.readlines()
lines = [line.rstrip("\n") for line in lines]
f.close()

checks = [ ((0,-1),[(-1,-1),(0,-1),(1,-1)]),
             ((0,1),[(-1,1),(0,1),(1,1)]), 
             ((-1,0),[(-1,-1),(-1,0),(-1,1)]),
             ((1,0),[(1,-1),(1,0),(1,1)])
             ]
code = {'.':0,'#':1}
around = [(-1,-1),(0,-1),(1,-1),(-1,0),(1,0),(-1,1),(0,1),(1,1)]
currentOrder = 0

width = max([len(line) for line in lines])
height = len(lines)
grid = [[code[c] for c in line] for line in lines]
elves = {}

for y,row in enumerate(grid):
    for x,c in enumerate(row):
        if c:
            elves[(x,y)] = 1

def add(pos1,pos2):
    return (pos1[0]+pos2[0],pos1[1]+pos2[1])

def hasElfIn(pos,checkPos):
    for delta in checkPos:
        tpos = add(pos,delta)
        if tpos in elves:
            return True
    return False

def getProposals():
    global elves
    result = defaultdict(int)

    for elf in elves.keys():
        # if no neighbours
        if not hasElfIn(elf,around):
            elves[elf] = elf
            continue
        for i in range(4):
            order = (i + currentOrder) % 4
            check = checks[order]
            if not hasElfIn(elf,check[1]):
                proposedPos = add(elf,check[0])
                elves[elf] = proposedPos
                result[proposedPos] += 1
                break
    return result

def doMoves(proposals):
    newElves = {}
    for elf,proposal in elves.items():
        if not proposal in proposals or proposals[proposal] > 1:
            # do not move
            newElves[elf] = 1 
        else:
            newElves[proposal] = 1 
    return newElves
               

pygame.init()
surface = pygame.display.set_mode((width*8,height*8))

def drawElves(surface,elfList,xoffset =0,yoffset=0,val = 1):
    for x,y in elfList.keys():
        rect = ((x+xoffset)*4,(y+yoffset)*4,4,4)
        surface.fill((val*127,(val&1)*255,(val&1)*255),rect)

def display1(elves,newElves):
    rect = (0,0,width*8,height*8)
    surface.fill((0,0,0),rect)
#    drawElves(surface,elves,width//4,height//4,1)
    drawElves(surface,newElves,width//4,height//4,2)
    pygame.display.update()     
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()     

def part1():
    global elves
    global currentOrder

    display1(elves,elves)
    for i in range(10):
        proposals = getProposals()
        newElves = doMoves(proposals)
        currentOrder += 1
        display1(elves,newElves)
        elves = newElves
    
    minx = min([x for x,y in elves.keys()])
    miny = min([y for x,y in elves.keys()])
    maxx = max([x for x,y in elves.keys()])
    maxy = max([y for x,y in elves.keys()])
    emptyCells = (maxx+1 - minx) * (maxy+1-miny) - len(elves.keys())
    print(emptyCells)
    return



def part2():
    global elves
    global currentOrder

    while True:
        proposals = getProposals()
        if len(proposals.keys()) == 0:
            print(currentOrder)
            break
        newElves = doMoves(proposals)
        currentOrder += 1
        display1(elves,newElves)
        elves = newElves


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
