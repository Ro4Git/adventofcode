#Advent of code 2021: Day 18
#https://adventofcode.com/2021/day/18
import re, time, copy, math, sys, ast
from itertools import permutations 


f = open('input_day18.txt', 'r')
lines = f.readlines()
lines = [line.rstrip("\n") for line in lines]
f.close()

pairs = [ast.literal_eval(line) for line in lines]
print(pairs[0])

def addPair(pair1,pair2):
    return [copy.deepcopy(pair1),copy.deepcopy(pair2)]

def fixFirstNumberToTheRight(pair,num):
    if type(pair) is list:
        if type(pair[0]) is int:
            pair[0] = pair[0] + num
            return True
        else: 
            res = fixFirstNumberToTheRight(pair[0],num)
            if res:
                return True
            else:
                return fixFirstNumberToTheRight(pair[1],num)
    
def fixFirstNumberToTheLeft(pair,num):
    if type(pair) is list:
        if type(pair[1]) is int:
            pair[1] = pair[1] + num
            return True
        else: 
            res = fixFirstNumberToTheLeft(pair[1],num)
            if res:
                return True
            else:
                return fixFirstNumberToTheLeft(pair[0],num)


def parseExplosion(pair,depth,changes):
    #find first left most pair with 2 regular numbers 
    if type(pair) is list:
        if len(changes)==0 and depth > 4 and type(pair[0]) is int and type(pair[1]) is int:
            #explose it
            changes.append(pair[0])
            changes.append(pair[1])
            return True
        if (parseExplosion(pair[0],depth+1,changes)):
            pair[0] = 0
        if (len(changes)>0):
            if changes[1]>0:
                #there was an explosion in this left branch and some value has to be propagated to the right
                if type(pair[1]) is int:
                    pair[1] = pair[1] + changes[1]
                    changes[1] = -1
                else:
                    if fixFirstNumberToTheRight(pair[1],changes[1]):
                        changes[1] = -1
                return False
        else:
            if (parseExplosion(pair[1],depth+1,changes)):
                pair[1] = 0
            if (len(changes)>0 and changes[0]>0):
                #there was an explosion in this right branch and some value has to be propagated to the left
                if type(pair[0]) is int:
                    pair[0] = pair[0] + changes[0]
                    changes[0] = -1
                else:
                    if fixFirstNumberToTheLeft(pair[0],changes[0]):
                        changes[0] = -1
                return False       
    return False                         
 

def splitPairs(pair,changes):
    if (len(changes)!=0):
        return 
    if (type(pair) is list):
        pair[0] = splitPairs(pair[0],changes)
        if (len(changes)==0):
            pair[1] = splitPairs(pair[1],changes)
    else:
        if (pair>=10):
            #regular number split
            changes.append(pair)
            return [int(math.floor(pair/2)),int(math.ceil(pair/2))]
    return pair


def magnitude(pair):
    if (type(pair) is list):
        return 3* magnitude(pair[0]) + 2 * magnitude(pair[1])
    return pair

def addAndReduce(pair1,pair2):
    result = addPair(pair1,pair2)
    changes = []
    parseExplosion(result,1,changes)
#       if (len(changes)>0):
#           print("Explosion: " + str(result))
    while(len(changes)>0):
        changes = []
        parseExplosion(result,1,changes)
        if (len(changes)>0):
#               print("Explosion: " + str(result))
            continue
        result = splitPairs(result,changes)
#           if (len(changes)>0):
#               print("Split: " + str(result))
    return result

def part1():
    result = pairs[0]
    for p in pairs[1:]:
        result = addAndReduce(result,p)
    print(magnitude(result))
    return

def part2():
    result = [magnitude(addAndReduce(p[0],p[1])) for p in permutations(pairs,2)]
    print(max(result))    
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

