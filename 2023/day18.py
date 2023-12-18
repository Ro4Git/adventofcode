#Advent of code 2023: Day 18
#https://adventofcode.com/2023/day/18
import re, time, copy, math
import pygame 
import numpy as np

f = open('input_day18.txt', 'r')
lines = f.readlines()
lines = [line.rstrip("\n") for line in lines]
f.close()

dirs = {
    "U": 0,
    "R": 1,
    "D": 2,
    "L": 3}

dirDeltas = [(0,-1),(1,0),(0,1),(-1,0)]
dirCodes = ['R','D','L','U']
instructions = [line.split(" ") for line in lines]

def addDelta(pos,delta,l):
    return (pos[0]+delta[0]*l,pos[1]+delta[1]*l)

# from https://stackoverflow.com/a/30408825
def PolyArea(x,y):
    return 0.5*np.abs(np.dot(x,np.roll(y,1))-np.dot(y,np.roll(x,1)))

def decoder_part1(instr):
    delta = dirDeltas[dirs[instr[0]]]
    length = int(instr[1])
    col = instr[2]
    return delta,length,col

def decoder_part2(instr):
    length = int(instr[2][2:7],16)
    dirCode = int(instr[2][7])
    delta = dirDeltas[dirs[dirCodes[dirCode]]]
    col = instr[2]
    return delta,length,col

def buildLoop(decoder):
    loop = []
    polyX = []
    polyY = []
    startNode = currentNode = ((0,0),"")
    loop.append(startNode)
    borderPixelCount = 0
    for instr in instructions:
        delta,length,col = decoder(instr)
        nextNodePos = addDelta(currentNode[0],delta,length)
        borderPixelCount += length
        currentNode = (nextNodePos,col)
        loop.append(currentNode)
        polyX.append(float(nextNodePos[0]))
        polyY.append(float(nextNodePos[1]))

    pixelCount = PolyArea(polyX,polyY)
    print(pixelCount)
    print(borderPixelCount)
    print(1 + borderPixelCount//2 + pixelCount)

def part1():
    buildLoop(decoder_part1)
    return 

def part2():
    buildLoop(decoder_part2)
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