#Advent of code 2024: Day 24
#https://adventofcode.com/2024/day/24
import re, time, copy , functools, itertools
from collections import defaultdict
import aoc

lines = aoc.ReadPuzzleInput("input_day24.txt")
sections = aoc.ToSections(lines)
inputs = {a:int(b) for a,b in aoc.ToList(sections[0],': ')}

operations =  {op[1]:tuple(op[0].split(' ')) for op in aoc.ToList(sections[1],' -> ')}

print(inputs)
print(operations)


def doOp(a, op, b):
    if op == "AND":
        return a & b
    elif op == "OR":
        return a | b
    elif op == "XOR":
        return a ^ b

def eval(results, x):
    if x in results:
        return results[x]
    op = operations[x]
    results[x] = doOp(eval(results,op[0]),op[1],eval(results,op[2]))
    return results[x]

def addtNumbers(indexBit, val1 , val2):
    results = {}
    outputs= []
    for i in range(46):
        results["x"+str(i).zfill(2)] = 0 if i != indexBit else val1
        results["y"+str(i).zfill(2)] = 0 if i != indexBit else val2
        outputs.append("z"+str(45-i).zfill(2))
    outputValues = [eval(results,out) for out in outputs]
    binaryString = ''.join([str(i) for i in outputValues])
    number = int(binaryString, 2)
    checkNumber = (val1+val2)<<indexBit
    print("bit"+str(indexBit).zfill(2) , binaryString, "!!!!!!" if number != checkNumber else "")
    if number != checkNumber:
        return "z"+str(indexBit)
    else:
        return None

def part1():
    results = inputs.copy()
    outputs = sorted([out for out in operations.keys() if out[0] ==  "z"], reverse=True)
    print(outputs)
    outputValues = [eval(results,out) for out in outputs]
    binaryString = ''.join([str(i) for i in outputValues])
    number = int(binaryString, 2)
    print(number)
    return 

def part2():
    ## solve manually with some help identifying error outputs
    errors = defaultdict(int)
    print("---------- 1 + 0 ----------")
    for i in range(46):
        res = addtNumbers(i,1,0)
        if res != None:
            errors[res] += 1
            
    print("---------- 0 + 1 ----------")
    for i in range(46):
        res = addtNumbers(i,0,1)
        if res != None:
            errors[res] += 1
    print("---------- 1 + 1 ----------")
    for i in range(46):
        res = addtNumbers(i,1,1)
        if res != None:
            errors[res] += 1
    print(errors.items())
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

