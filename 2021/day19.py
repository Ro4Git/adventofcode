#Advent of code 2021: Day 19
#https://adventofcode.com/2021/day/19
import re, time, copy, math
import numpy as np
from itertools import combinations 


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


# from https://newbedev.com/how-to-calculate-all-24-rotations-of-3d-array
# all 24 possible rotation matrices
def matrices():
    for a in [[[1, 0, 0],[0, 1, 0],[0, 0, 1]], [[0, 1, 0],[0, 0, 1],[1, 0, 0]], [[0, 0, 1],[1, 0, 0],[0, 1, 0]]]:
        for b in [[[ 1, 0, 0],[ 0, 1, 0],[ 0, 0, 1]],[[-1, 0, 0],[ 0,-1, 0],[ 0, 0, 1]],[[-1, 0, 0],[ 0, 1, 0],[ 0, 0,-1]],[[ 1, 0, 0], [ 0,-1, 0], [ 0, 0,-1]]]:
            for c in [[[ 1, 0, 0],[ 0, 1, 0],[ 0, 0, 1]],[[ 0, 0,-1],[ 0,-1, 0],[-1, 0, 0]]]:
                yield np.matrix(a)*np.matrix(b)*np.matrix(c)
# all 24 possible list of positions for each scanner
scannersOriented = [[[tuple((np.asarray(np.dot(mat,p))[0]).tolist())  for p in scan] for mat in matrices()] for scan in scanners]

def manhattan(v1):
    return abs(v1[0])+abs(v1[1])+abs(v1[2])

def sub(p2,p1):
    return (p2[0] - p1[0],p2[1] - p1[1],p2[2] - p1[2])

def matchScanners(ref,scan2): 
    for rotated in scan2:
        for k,p2 in enumerate(rotated):
            for j,p1 in enumerate(ref):
                delta = sub(p2,p1)
                scan2set = set([sub(p,delta) for p in rotated])
                common = ref.intersection(scan2set)
                if len(common)>=12:
                    # returns position of scanner and list of positions
                    return ((-delta[0],-delta[1],-delta[2]),scan2set)
    return None

scannerPositions = {}
scannerPositions[0] = np.asarray([0,0,0])
scanners[0] = set([tuple(p.tolist()) for p in scanners[0]])

def part1():
    while len(scannerPositions) != len(scanners):
        for j in range(len(scanners)):            
            if not j in scannerPositions:
                res = matchScanners(scanners[0],scannersOriented[j])
                if res != None:
                    # update scanner to ref 0
                    scanners[0] = scanners[0].union(res[1])
                    scannerPositions[j] = res[0]
                    print("Match",j,res[0])        

    print(len(scanners[0]))    
    return

def part2():
    distances = [manhattan(sub(p[0],p[1])) for p in combinations(scannerPositions.values(),2)]
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

