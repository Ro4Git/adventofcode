#Advent of code 2021: Day 19
#https://adventofcode.com/2021/day/19
import re, time, copy, math, sys, ast
import numpy as np
from itertools import permutations 


f = open('input_day19.txt', 'r')
lines = f.readlines()
lines = [line.rstrip("\n") for line in lines]
f.close()

scanners = []
currentScanner = []
for line in lines[1:]: 
    if (line.startswith("--- scanner")):
        scanners.append(copy.copy(currentScanner))
        currentScanner = []
    else:
        tokens = line.split(",")
        if len(tokens) == 3: 
            currentScanner.append(np.array([int(n) for n in tokens]))
scanners.append(copy.copy(currentScanner))


print(scanners)


# from https://newbedev.com/how-to-calculate-all-24-rotations-of-3d-array
A = [[[1, 0, 0],[0, 1, 0],[0, 0, 1]], [[0, 1, 0],[0, 0, 1],[1, 0, 0]], [[0, 0, 1],[1, 0, 0],[0, 1, 0]]]
B = [[[ 1, 0, 0],[ 0, 1, 0],[ 0, 0, 1]],[[-1, 0, 0],[ 0,-1, 0],[ 0, 0, 1]],[[-1, 0, 0],[ 0, 1, 0],[ 0, 0,-1]],[[ 1, 0, 0], [ 0,-1, 0], [ 0, 0,-1]]]
C = [[[ 1, 0, 0],[ 0, 1, 0],[ 0, 0, 1]],[[ 0, 0,-1],[ 0,-1, 0],[-1, 0, 0]]]
rotMatrices = []
for a in A:
    for b in B:
        for c in C:
            m = np.matrix(a)*np.matrix(b)*np.matrix(c)
            rotMatrices.append(m)
print(len(rotMatrices))


def matchScanners(scan1,scan2): 
    scan1set = set([tuple(p.tolist()) for p in scan1])
    for i,mat in enumerate(rotMatrices):
        rotated = [np.asarray(np.dot(mat,p))[0]  for p in scan2]
        nbMatching = 0
        # for all probe in scanner 1
        for j,p1 in enumerate(scan1):
            for k,p2 in enumerate(rotated):
                delta = p2 - p1
                translated = [(p - delta) for p in rotated] 
                scan2set = set([tuple(p.tolist()) for p in translated])
                common = scan1set.intersection(scan2set)
                if len(common)>=12:
                    # returns position of scanner and list of positions
                    return (-delta,translated)
    return None

scannerPositions = {}
scannerPositions[0] = np.asarray([0,0,0])
doneCombo = {}
doneCombo[(0,0)] = True

def part1():
    while len(scannerPositions) != len(scanners):
        for i in range(len(scanners)):            
            if i in scannerPositions:
                for j in range(len(scanners)):            
                    if not j in scannerPositions and not (i,j) in doneCombo:
                        doneCombo[(i,j)] = True
                        res = matchScanners(scanners[i],scanners[j])
                        if res != None:
                            # update scanner to ref 0
                            scanners[j] = res[1]
                            scannerPositions[j] = res[0]
                            print("Match",i,j,res[0])
    
    beaconSet = set([tuple(p.tolist()) for p in scanners[0]])
    for scan in scanners[1:]:
        beaconSet = beaconSet.union(set([tuple(p.tolist()) for p in scan]))
    print(len(beaconSet))    
    return

def manhattan(v1):
    return abs(v1[0])+abs(v1[1])+abs(v1[2])

def part2():
    distances = [manhattan(p[0]-p[1]) for p in permutations(scannerPositions.values(),2)]
    maxDist = max(distances)
    print(maxDist)

    return


print("----- Part1 ----")
startp1 = time.time()
displayPath  = part1()
endp1 = time.time()
print("{:.4f}s".format(endp1 - startp1))

print("----- Part2 ----")
startp2 = time.time()
part2()
endp2 = time.time()
print("{:.4f}s".format(endp2 - startp2))

